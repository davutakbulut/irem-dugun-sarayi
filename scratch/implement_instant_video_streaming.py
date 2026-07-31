import sys
import os
import re

# 1. Update serve_fast_3g.py to support HTTP 206 Partial Content Range Requests for instant video streaming
server_code = """import http.server
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
        self.send_header('Cache-Control', 'public, max-age=3600')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Range')
        self.send_header('Accept-Ranges', 'bytes')
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
                res_id = re.sub(r'[^A-Za-z0-9_-]', '_', str(raw_res_id))
                file_name = payload.get('fileName', f"upload_{int(os.times()[4]*1000)}.jpg")
                file_data = payload.get('fileData', '')

                upload_dir = os.path.join(os.getcwd(), 'uploads', res_id)
                os.makedirs(upload_dir, exist_ok=True)

                safe_name = re.sub(r'[^A-Za-z0-9_.-]', '_', file_name)
                file_path = os.path.join(upload_dir, safe_name)

                if ',' in file_data:
                    _, b64data = file_data.split(',', 1)
                else:
                    b64data = file_data

                binary_bytes = base64.b64decode(b64data)

                with open(file_path, 'wb') as f:
                    f.write(binary_bytes)

                relative_url = f"/uploads/{res_id}/{safe_name}"

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
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode('utf-8'))
                return

        super().do_GET()

    def do_GET(self):
        if self.path == '/' or self.path.startswith('/?'):
            self.path = '/index_prod.html' if os.path.exists('index_prod.html') else '/index.html'

        filepath = self.translate_path(self.path)

        # INSTANT VIDEO STREAMING: Handle HTTP 206 Range Requests (Partial Content)
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
                    self.send_header('Cache-Control', 'public, max-age=3600')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    super().end_headers()

                    with open(filepath, 'rb') as f:
                        f.seek(start_byte)
                        self.wfile.write(f.read(length))
                    return
            except Exception as e:
                pass

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

print(f"Server starting on port {PORT} with HTTP 206 Video Range Streaming Enabled...")
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("0.0.0.0", PORT), Fast3GHandler) as httpd:
    httpd.serve_forever()
"""

with open('scratch/serve_fast_3g.py', 'w', encoding='utf-8') as f:
    f.write(server_code)

print("Updated serve_fast_3g.py with HTTP 206 Partial Content Video Range Streaming!")

# 2. Update index.html video element attributes to include preload="auto" and playsInline
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_lightbox_v = """                <video
                  src={mediaList[lightboxIndex].url}
                  controls
                  autoPlay
                  playsInline
                  className="max-w-full max-h-[70vh] rounded-2xl border-2 border-amber-500/40 shadow-2xl bg-black"
                />"""

new_lightbox_v = """                <video
                  src={mediaList[lightboxIndex].url}
                  controls
                  autoPlay
                  preload="auto"
                  playsInline
                  className="max-w-full max-h-[70vh] rounded-2xl border-2 border-amber-500/40 shadow-2xl bg-black"
                />"""

if old_lightbox_v in html:
    html = html.replace(old_lightbox_v, new_lightbox_v)
    print("Updated index.html video tag preload attribute!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html instant video streaming attributes successfully!")
