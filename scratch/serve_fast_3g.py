import http.server
import socketserver
import gzip
import io
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8008

class Fast3GHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'public, max-age=3600')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

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

print(f"Server starting on port {PORT}...")
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("0.0.0.0", PORT), Fast3GHandler) as httpd:
    httpd.serve_forever()
