import http.server
import socketserver
import gzip
import io
import os
import sys
import json
import urllib.parse
import re

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8008

class Fast3GHandler(http.server.SimpleHTTPRequestHandler):
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

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        # 1. API: System Settings GET
        if parsed_path.path in ['/api/system-settings', '/api/system-config']:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            db_file = os.path.join(os.path.dirname(__file__), 'db_system_settings.json')
            if os.path.exists(db_file):
                with open(db_file, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b'{"themeColor":"nordic-light","menuLayout":"vertical"}')
            return

        # 2. API: Ping GET
        if parsed_path.path == '/api/ping':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
            return

        # 2b. Static uploads files serving (/uploads/...)
        if parsed_path.path.startswith('/uploads/'):
            rel_path = parsed_path.path.lstrip('/')
            full_path = os.path.abspath(rel_path)
            if os.path.exists(full_path) and os.path.isfile(full_path):
                try:
                    self.send_response(200)
                    if full_path.endswith('.png'):
                        self.send_header('Content-Type', 'image/png')
                    elif full_path.endswith('.jpg') or full_path.endswith('.jpeg'):
                        self.send_header('Content-Type', 'image/jpeg')
                    elif full_path.endswith('.webp'):
                        self.send_header('Content-Type', 'image/webp')
                    elif full_path.endswith('.mp4'):
                        self.send_header('Content-Type', 'video/mp4')
                    else:
                        self.send_header('Content-Type', 'application/octet-stream')
                    
                    with open(full_path, 'rb') as f:
                        file_data = f.read()
                    self.send_header('Content-Length', str(len(file_data)))
                    self.end_headers()
                    self.wfile.write(file_data)
                    return
                except Exception as e:
                    print("Error serving upload file:", e)

        # 3. Main HTML & Routing
        if self.path == '/' or self.path.startswith('/?') or not os.path.splitext(parsed_path.path)[1]:
            target_html = 'index_prod.html' if os.path.exists('index_prod.html') else 'index.html'
            if os.path.exists(target_html):
                try:
                    with open(target_html, 'rb') as f:
                        content = f.read()
                    
                    # 0ms Server HTML System Settings Injection (data-ui-theme & data-menu-layout) from db_system_settings.json
                    db_file = os.path.join(os.path.dirname(__file__), 'db_system_settings.json')
                    if os.path.exists(db_file):
                        with open(db_file, 'r', encoding='utf-8') as dbf:
                            sys_cfg = json.load(dbf)
                        active_t = sys_cfg.get('themeColor', 'nordic-light')
                        active_m = sys_cfg.get('menuLayout', 'vertical')
                        active_v = sys_cfg.get('systemVersion', 'v1.4.67')
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
                    print("Error serving HTML:", e)
                    
        # 4. Fallback to standard static file server
        super().do_GET()

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        # 1. API: System Settings POST
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
                self.wfile.write(b'{"status":"ok","message":"System settings saved to backend DB"}')
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(f'{{"error":"Failed to save settings: {str(e)}"}}'.encode('utf-8'))
                return

        # 2. API: Media Upload POST
        if parsed_path.path == '/api/upload-media':
            try:
                content_len = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_len)
                data = json.loads(body.decode('utf-8'))
                
                saved_url = None
                # Physical disk file save if fileData is present
                raw_b64 = data.get('fileData') or (data.get('mediaObj', {}).get('url') if isinstance(data.get('mediaObj'), dict) else None)
                if raw_b64 and isinstance(raw_b64, str) and raw_b64.startswith('data:'):
                    try:
                        header, b64_str = raw_b64.split(',', 1) if ',' in raw_b64 else ('', raw_b64)
                        ext = '.jpg'
                        if 'png' in header: ext = '.png'
                        elif 'gif' in header: ext = '.gif'
                        elif 'webp' in header: ext = '.webp'
                        elif 'video' in header or 'mp4' in header: ext = '.mp4'
                        
                        fname = data.get('fileName') or f"media_{int(time.time())}_{random.randint(100,999)}{ext}"
                        if not fname.endswith(ext): fname += ext
                        safe_fname = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', fname)
                        
                        uploads_dir = os.path.abspath('uploads')
                        os.makedirs(uploads_dir, exist_ok=True)
                        file_dest = os.path.join(uploads_dir, safe_fname)
                        
                        with open(file_dest, 'wb') as img_out:
                            img_out.write(base64.b64decode(b64_str))
                        
                        saved_url = f"/uploads/{safe_fname}"
                        print(f"💾 Physical media file saved to disk: {file_dest} ({len(b64_str)} bytes b64)")
                    except Exception as disk_err:
                        print("⚠️ Physical file save error:", disk_err)

                db_file = os.path.join(os.path.dirname(__file__), 'db_system_settings.json')
                existing = {}
                if os.path.exists(db_file):
                    try:
                        with open(db_file, 'r', encoding='utf-8') as f:
                            existing = json.load(f)
                    except Exception: pass
                
                if 'reservations' in data and isinstance(data['reservations'], list):
                    existing['reservations'] = data['reservations']
                elif 'resId' in data and 'mediaObj' in data:
                    res_id = data['resId']
                    media_obj = data['mediaObj']
                    if saved_url:
                        media_obj['url'] = saved_url
                        media_obj['thumbnail'] = saved_url
                    res_list = existing.get('reservations', [])
                    found = False
                    for r in res_list:
                        if r.get('id') == res_id or r.get('mediaKey') == res_id:
                            if 'mediaFiles' not in r: r['mediaFiles'] = []
                            r['mediaFiles'].insert(0, media_obj)
                            found = True
                            break
                    if not found:
                        res_list.insert(0, {
                            "id": res_id,
                            "mediaKey": res_id,
                            "customerName": "Özel Düğün & Balo Daveti",
                            "eventType": "Balo / Düğün Daveti",
                            "date": "2026-08-01",
                            "venueId": "v1",
                            "mediaFiles": [media_obj]
                        })
                    existing['reservations'] = res_list
                
                with open(db_file, 'w', encoding='utf-8') as f:
                    json.dump(existing, f, indent=2)
                    
                resp_payload = {"status":"ok","success": True, "message":"Media uploaded and saved to backend DB"}
                if saved_url: resp_payload["url"] = saved_url
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(resp_payload).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(f'{{"error":"Upload failed: {str(e)}"}}'.encode('utf-8'))
                return

        self.send_response(404)
        self.end_headers()

def run(server_class=http.server.HTTPServer, handler_class=Fast3GHandler, port=8008):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"🚀 FAST 3G SIMULATED SERVER STARTED ON PORT {port} WITH REST API SYSTEM SETTINGS DB...")
    httpd.serve_forever()

if __name__ == '__main__':
    run(port=PORT)
