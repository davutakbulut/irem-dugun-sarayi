import http.server
import socketserver
import gzip
import io
import os
import sys
import json
import base64
import re

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8008

class Fast3GHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path == '/api/upload-media':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                payload = json.loads(post_data.decode('utf-8'))

                raw_res_id = payload.get('resId', 'GENERAL')
                # Clean res_id for safe directory creation (e.g. RES-2026-004)
                res_id = re.sub(r'[^A-Za-z0-9_-]', '_', str(raw_res_id))
                file_name = payload.get('fileName', f"upload_{int(os.times()[4]*1000)}.jpg")
                file_data = payload.get('fileData', '')

                # 1. Create target upload directory: uploads/<res_id>/
                upload_dir = os.path.join(os.getcwd(), 'uploads', res_id)
                os.makedirs(upload_dir, exist_ok=True)

                # 2. Sanitize filename
                safe_name = re.sub(r'[^A-Za-z0-9_.-]', '_', file_name)
                file_path = os.path.join(upload_dir, safe_name)

                # 3. Decode base64 binary content
                if ',' in file_data:
                    _, b64data = file_data.split(',', 1)
                else:
                    b64data = file_data

                binary_bytes = base64.b64decode(b64data)

                # 4. Save physical file to disk
                with open(file_path, 'wb') as f:
                    f.write(binary_bytes)

                relative_url = f"/uploads/{res_id}/{safe_name}"

                print(f"✅ Physical file saved on disk: {file_path} ({len(binary_bytes)} bytes)")

                response_data = {
                    "success": True,
                    "url": relative_url,
                    "fileName": safe_name,
                    "resId": res_id,
                    "size": len(binary_bytes)
                }

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
                return
            except Exception as e:
                print(f"❌ Upload Error: {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode('utf-8'))
                return

        super().do_GET()

    def do_GET(self):
        if self.path == '/' or self.path.startswith('/?'):
            self.path = '/index_prod.html' if os.path.exists('index_prod.html') else '/index.html'

        accept_encoding = self.headers.get('Accept-Encoding', '')
        filepath = self.translate_path(self.path)

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

print(f"Server starting on port {PORT} with Local Disk File Upload API Enabled...")
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("0.0.0.0", PORT), Fast3GHandler) as httpd:
    httpd.serve_forever()
