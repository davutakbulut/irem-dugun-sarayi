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

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
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
        # 3. Static Uploads Serving
        if parsed_path.path.startswith('/uploads/'):
            filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', parsed_path.path.lstrip('/'))
            if os.path.exists(filepath) and os.path.isfile(filepath):
                self.send_response(200)
                ext = os.path.splitext(filepath)[1].lower()
                mime = 'image/jpeg'
                if ext in ['.png']: mime = 'image/png'
                elif ext in ['.gif']: mime = 'image/gif'
                elif ext in ['.mp4', '.mov']: mime = 'video/mp4'
                elif ext in ['.webp']: mime = 'image/webp'
                self.send_header('Content-Type', mime)
                self.send_header('Content-Length', str(os.path.getsize(filepath)))
                self.end_headers()
                with open(filepath, 'rb') as f:
                    self.wfile.write(f.read())
                return

        # 4. Main HTML & Routing
        is_html_route = (
            self.path == '/' or
            self.path.startswith('/yonetim') or
            self.path.startswith('/giris') or
            self.path.startswith('/?') or
            not os.path.splitext(parsed_path.path)[1] or
            parsed_path.path.endswith('.html')
        )
        if is_html_route:
            target_html = 'index.html'
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
                        inject_tag = f'<html lang="tr" class="light" data-ui-theme="{active_t}" data-menu-layout="{active_m}">'
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
                import base64
                import time
                content_len = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_len)
                data = json.loads(body.decode('utf-8'))

                res_id = data.get('resId', 'GENERAL')
                file_name = data.get('fileName', f'file_{int(time.time())}.jpg')
                file_data = data.get('fileData', '')

                safe_name = re.sub(r'[^A-Za-z0-9_.-]', '_', file_name)
                uploads_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads', res_id)
                os.makedirs(uploads_dir, exist_ok=True)
                dest_path = os.path.join(uploads_dir, safe_name)

                if file_data and 'base64,' in file_data:
                    b64_str = file_data.split('base64,')[1]
                    with open(dest_path, 'wb') as f:
                        f.write(base64.b64decode(b64_str))

                rel_url = f'/uploads/{res_id}/{safe_name}'
                res_body = json.dumps({
                    'success': True,
                    'status': 'ok',
                    'url': rel_url,
                    'message': 'File uploaded and saved to disk successfully'
                }).encode('utf-8')

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(res_body)
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(f'{{"success":false,"error":"Upload failed: {str(e)}"}}'.encode('utf-8'))
                return

        self.send_response(404)
        self.end_headers()

def run(server_class=http.server.ThreadingHTTPServer, handler_class=Fast3GHandler, port=8008):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"🚀 FAST 3G SIMULATED THREADED SERVER STARTED ON PORT {port} WITH REST API SYSTEM SETTINGS DB...")
    httpd.serve_forever()

if __name__ == '__main__':
    run(port=PORT)
