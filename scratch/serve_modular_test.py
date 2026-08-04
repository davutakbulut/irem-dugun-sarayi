import http.server
import socketserver
import gzip
import io
import os
import sys
import json
import urllib.parse
import re
import time

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8002

class ModularTestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)

        # 1. REST API: System Settings GET
        if parsed_path.path in ['/api/system-settings', '/api/system-config']:
            try:
                db_file = os.path.join(os.path.dirname(__file__), 'db_system_settings.json')
                cfg_data = {}
                if os.path.exists(db_file):
                    try:
                        with open(db_file, 'r', encoding='utf-8') as f:
                            cfg_data = json.load(f)
                    except Exception: pass

                # Dynamic physical disk scan
                uploads_base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
                disk_media = {}
                if os.path.exists(uploads_base):
                    for res_id in os.listdir(uploads_base):
                        res_dir = os.path.join(uploads_base, res_id)
                        if os.path.isdir(res_dir):
                            items = []
                            for fname in os.listdir(res_dir):
                                if not fname.startswith('.'):
                                    ext = os.path.splitext(fname)[1].lower()
                                    file_url = f"/uploads/{res_id}/{fname}"
                                    items.append({
                                        'id': f"disk_{res_id}_{fname}",
                                        'name': fname,
                                        'url': file_url,
                                        'type': 'video' if ext in ['.mp4', '.mov', '.avi', '.mkv'] else 'photo',
                                        'source': 'disk',
                                        'uploadedAt': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(os.path.getmtime(os.path.join(res_dir, fname))))
                                    })
                            if items:
                                disk_media[res_id] = items
                
                cfg_data['diskMediaMap'] = disk_media

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(cfg_data, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                print("API GET Error:", e)

        # 2. HTML Routes (Strictly serves dist/index.html for Vite Modular build)
        is_html_route = (
            parsed_path.path == '/' or
            parsed_path.path.startswith('/yonetim') or
            parsed_path.path.startswith('/giris') or
            parsed_path.path.endswith('.html')
        )
        if is_html_route:
            dist_html = os.path.join(os.path.dirname(__file__), '..', 'dist', 'index.html')
            if os.path.exists(dist_html):
                try:
                    with open(dist_html, 'rb') as f:
                        content = f.read()
                    
                    db_file = os.path.join(os.path.dirname(__file__), 'db_system_settings.json')
                    if os.path.exists(db_file):
                        with open(db_file, 'r', encoding='utf-8') as dbf:
                            sys_cfg = json.load(dbf)
                        active_t = sys_cfg.get('themeColor', 'nordic-light')
                        active_m = sys_cfg.get('menuLayout', 'vertical')
                        active_v = sys_cfg.get('systemVersion', 'v1.5.31')
                        inject_tag = f'<html lang="tr" class="light" data-ui-theme="{active_t}" data-menu-layout="{active_m}" data-system-version="{active_v}">'
                        content_str = content.decode('utf-8', errors='ignore')
                        content_str = re.sub(r'<html[^>]*>', inject_tag, content_str, count=1)
                        content = content_str.encode('utf-8')

                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html; charset=utf-8')
                    self.send_header('Content-Length', str(len(content)))
                    self.end_headers()
                    self.wfile.write(content)
                    return
                except Exception as e:
                    print("Error serving dist HTML:", e)

        # 3. Static Assets Server
        # Check if asset exists in dist/ or root
        asset_rel = parsed_path.path.lstrip('/')
        dist_asset = os.path.join(os.path.dirname(__file__), '..', 'dist', asset_rel)
        if os.path.exists(dist_asset) and os.path.isfile(dist_asset):
            try:
                with open(dist_asset, 'rb') as f:
                    data = f.read()
                mime = 'text/css' if asset_rel.endswith('.css') else ('application/javascript' if asset_rel.endswith('.js') else 'application/octet-stream')
                self.send_response(200)
                self.send_header('Content-Type', mime)
                self.send_header('Content-Length', str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return
            except Exception: pass

        super().do_GET()

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)

        if parsed_path.path == '/api/delete-media':
            try:
                content_len = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_len)
                data = json.loads(body.decode('utf-8'))

                raw_res_id = str(data.get('resId', ''))
                raw_file_name = str(data.get('fileName', ''))
                media_id = str(data.get('mediaId', ''))
                media_key = str(data.get('mediaKey', ''))

                safe_file_name = os.path.basename(re.sub(r'[^A-Za-z0-9_.-]', '_', raw_file_name))

                possible_folders = []
                if raw_res_id: possible_folders.append(re.sub(r'[^A-Za-z0-9_-]', '', raw_res_id))
                if media_key: possible_folders.append(re.sub(r'[^A-Za-z0-9_-]', '', media_key))

                deleted_disk = False
                uploads_base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')

                for folder in possible_folders:
                    if not folder: continue
                    target_path = os.path.join(uploads_base, folder, safe_file_name)
                    if os.path.exists(target_path):
                        try:
                            os.remove(target_path)
                            deleted_disk = True
                            print(f"🗑️ DELETED FROM CANDIDATE FOLDER ({folder}): {target_path}")
                            break
                        except Exception as ex:
                            print("Error removing file:", ex)

                if not deleted_disk and safe_file_name and os.path.exists(uploads_base):
                    for folder_name in os.listdir(uploads_base):
                        sub_dir = os.path.join(uploads_base, folder_name)
                        if os.path.isdir(sub_dir):
                            candidate = os.path.join(sub_dir, safe_file_name)
                            if os.path.exists(candidate):
                                try:
                                    os.remove(candidate)
                                    deleted_disk = True
                                    print(f"🗑️ DELETED FROM SEARCHED SUBDIR ({folder_name}): {candidate}")
                                    break
                                except Exception as ex:
                                    print("Error removing file from subdir:", ex)

                db_file = os.path.join(os.path.dirname(__file__), 'db_system_settings.json')
                if os.path.exists(db_file):
                    try:
                        with open(db_file, 'r', encoding='utf-8') as f:
                            db_cfg = json.load(f)
                        
                        updated_db = False
                        res_list = db_cfg.get('reservations', [])
                        for r in res_list:
                            if r.get('mediaKey') == media_key or r.get('id') == raw_res_id or r.get('id') == media_key:
                                m_files = r.get('mediaFiles', [])
                                new_files = [m for m in m_files if str(m.get('id')) != media_id and str(m.get('url', '')).split('/')[-1] != safe_file_name]
                                if len(new_files) != len(m_files):
                                    r['mediaFiles'] = new_files
                                    updated_db = True
                        
                        stored_media = db_cfg.get('storedMedia', {})
                        for k in list(stored_media.keys()):
                            m_list = stored_media[k]
                            new_m_list = [m for m in m_list if isinstance(m, dict) and str(m.get('id')) != media_id and str(m.get('url', '')).split('/')[-1] != safe_file_name]
                            if len(new_m_list) != len(m_list):
                                stored_media[k] = new_m_list
                                updated_db = True
                        db_cfg['storedMedia'] = stored_media

                        if updated_db:
                            db_cfg['reservations'] = res_list
                            with open(db_file, 'w', encoding='utf-8') as f:
                                json.dump(db_cfg, f, indent=2, ensure_ascii=False)
                    except Exception as e_db:
                        print("Error updating db JSON on delete:", e_db)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'deletedDisk': deleted_disk, 'mediaId': media_id}).encode('utf-8'))
                return
            except Exception as e:
                print("DELETE API Error:", e)
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode('utf-8'))
                return

        if parsed_path.path in ['/api/system-settings', '/api/system-config']:
            try:
                content_len = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_len)
                data = json.loads(body.decode('utf-8'))
                
                db_file = os.path.join(os.path.dirname(__file__), 'db_system_settings.json')
                existing = {}
                if os.path.exists(db_file):
                    try:
                        with open(db_file, 'r', encoding='utf-8') as f:
                            existing = json.load(f)
                    except Exception: pass
                
                existing.update(data)
                with open(db_file, 'w', encoding='utf-8') as f:
                    json.dump(existing, f, indent=2)
                    
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'ok', 'updated': data}).encode('utf-8'))
                return
            except Exception as e:
                print("POST Error:", e)

        super().do_POST()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), ModularTestHandler) as httpd:
        print(f"🚀 MODULAR TEST SERVER RUNNING ON PORT {PORT} (Strictly serving Vite dist/index.html)")
        httpd.serve_forever()
