import os
import json
import sys

# 1. Rewrite scratch/serve_fast_3g.py with a clean, rock-solid Fast3GHandler having SINGLE do_GET and SINGLE do_POST
server_code = """import http.server
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
                self.wfile.write(b'{"themeColor":"nordic-light"}')
            return

        # 2. API: Ping GET
        if parsed_path.path == '/api/ping':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
            return

        # 3. Main HTML & Routing
        if self.path == '/' or self.path.startswith('/?') or not os.path.splitext(parsed_path.path)[1]:
            target_html = 'index_prod.html' if os.path.exists('index_prod.html') else 'index.html'
            if os.path.exists(target_html):
                try:
                    with open(target_html, 'rb') as f:
                        content = f.read()
                    
                    # 0ms Server HTML data-ui-theme Injection from db_system_settings.json
                    db_file = os.path.join(os.path.dirname(__file__), 'db_system_settings.json')
                    if os.path.exists(db_file):
                        with open(db_file, 'r', encoding='utf-8') as dbf:
                            sys_cfg = json.load(dbf)
                        active_t = sys_cfg.get('themeColor', 'nordic-light')
                        if active_t and active_t != 'gold' and active_t != 'classic_gold':
                            content = content.replace(b'<html lang="tr"', f'<html lang="tr" data-ui-theme="{active_t}"'.encode('utf-8'))
                            content = content.replace(b'<html lang=\\"tr\\"', f'<html lang="tr" data-ui-theme="{active_t}"'.encode('utf-8'))

                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html; charset=utf-8')
                    self.send_header('Content-Length', str(len(content)))
                    self.end_headers()
                    self.wfile.write(content)
                    return
                except Exception as e:
                    pass

        filepath = self.translate_path(self.path)

        # 4. Range Requests for Video Streaming (HTTP 206)
        range_header = self.headers.get('Range', None)
        if range_header and os.path.isfile(filepath):
            try:
                file_size = os.path.getsize(filepath)
                range_match = re.search(r'bytes=(\d+)-(\d+)?', range_header)
                if range_match:
                    start_byte = int(range_match.group(1))
                    end_byte = int(range_match.group(2)) if range_match.group(2) else file_size - 1
                    end_byte = min(end_byte, file_size - 1)
                    length = end_byte - start_byte + 1

                    content_type = self.guess_type(filepath) or 'application/octet-stream'

                    self.send_response(206)
                    self.send_header('Content-Type', content_type)
                    self.send_header('Content-Range', f'bytes {start_byte}-{end_byte}/{file_size}')
                    self.send_header('Content-Length', str(length))
                    self.send_header('Accept-Ranges', 'bytes')
                    super().end_headers()

                    with open(filepath, 'rb') as f:
                        f.seek(start_byte)
                        self.wfile.write(f.read(length))
                    return
            except Exception as e:
                pass

        # 5. Gzip Compression for Static Assets
        accept_encoding = self.headers.get('Accept-Encoding', '')
        if os.path.isfile(filepath) and 'gzip' in accept_encoding and filepath.endswith(('.html', '.js', '.css', '.svg', '.json')):
            try:
                with open(filepath, 'rb') as f:
                    content = f.read()

                out = io.BytesIO()
                with gzip.GzipFile(fileobj=out, mode='wb', compresslevel=6) as gz:
                    gz.write(content)
                compressed = out.getvalue()

                self.send_response(200)
                self.send_header('Content-Type', self.guess_type(filepath))
                self.send_header('Content-Encoding', 'gzip')
                self.send_header('Content-Length', str(len(compressed)))
                self.end_headers()
                self.wfile.write(compressed)
                return
            except Exception as e:
                pass

        super().do_GET()

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)

        # 1. API: System Settings POST
        if parsed_path.path in ['/api/system-settings', '/api/system-config']:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                db_file = os.path.join(os.path.dirname(__file__), 'db_system_settings.json')
                
                existing = {}
                if os.path.exists(db_file):
                    try:
                        with open(db_file, 'r', encoding='utf-8') as f:
                            existing = json.load(f)
                    except Exception:
                        pass
                
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
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
                return

        # 2. API: Media Upload POST
        if parsed_path.path == '/api/upload-media':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode('utf-8'))
                res_id = payload.get('resId', 'GENERAL').replace('/', '_').replace('\\\\', '_')
                file_name = payload.get('fileName', 'uploaded_file.jpg')
                base64_data = payload.get('base64Data', '')

                if ',' in base64_data:
                    base64_data = base64_data.split(',', 1)[1]

                import base64
                file_bytes = base64.b64decode(base64_data)

                upload_dir = os.path.join(os.path.dirname(__file__), '..', 'uploads', res_id)
                os.makedirs(upload_dir, exist_ok=True)

                saved_filepath = os.path.join(upload_dir, file_name)
                with open(saved_filepath, 'wb') as f:
                    f.write(file_bytes)

                public_url = f"/uploads/{res_id}/{file_name}"

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                res_payload = {
                    "success": True,
                    "url": public_url,
                    "fileName": file_name,
                    "size": len(file_bytes)
                }
                self.wfile.write(json.dumps(res_payload).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode('utf-8'))
                return

        super().do_POST()

print(f"Server starting on port {PORT} with REST API System Settings DB & Video Streaming Enabled...")
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("0.0.0.0", PORT), Fast3GHandler) as httpd:
    httpd.serve_forever()
"""

with open('scratch/serve_fast_3g.py', 'w', encoding='utf-8') as f:
    f.write(server_code)
print("Rewrote scratch/serve_fast_3g.py with clean REST API endpoints for GET/POST /api/system-settings!")

# 2. Add checkTheme() console diagnostic tool in index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

check_theme_script = """
  <!-- THEME DIAGNOSTIC CONSOLE TOOL: Type checkTheme() in browser F12 console -->
  <script>
    window.checkTheme = function() {
      console.log('🔍 SYSTEM THEME DIAGNOSTIC REPORT:');
      console.log('----------------------------------------');
      var domTheme = document.documentElement.getAttribute('data-ui-theme') || 'classic_gold (default)';
      var localTheme = localStorage.getItem('irem_cache_theme_color') || localStorage.getItem('selected_theme') || 'None';
      console.log('1. HTML DOM Attribute (data-ui-theme):', domTheme);
      console.log('2. LocalStorage Cache:', localTheme);
      
      fetch('/api/system-settings')
        .then(r => r.json())
        .then(data => {
          console.log('3. Server Backend DB Theme (/api/system-settings):', data.themeColor || 'Unknown');
          console.log('----------------------------------------');
          if (data.themeColor === domTheme || (domTheme === 'classic_gold (default)' && data.themeColor === 'gold')) {
            console.log('✅ RESULT: THEME IS 100% MATCHED AND PERSISTENT IN BACKEND DB!');
          } else {
            console.warn('⚠️ WARNING: DOM theme does not match Backend DB theme.');
          }
        }).catch(err => console.error('❌ Failed to fetch backend DB theme:', err));
    };
  </script>
"""

if "window.checkTheme" not in html:
    html = html.replace('</head>', check_theme_script + '\n</head>')
    print("Added checkTheme() console diagnostic tool to index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated server 404 fix and checkTheme console tool successfully!")
