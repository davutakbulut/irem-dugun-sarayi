import os
import json
import sys

# 1. Create scratch/db_system_settings.json
db_path = 'scratch/db_system_settings.json'
initial_db = {
    "themeColor": "nordic-light",
    "appName": "İrem Düğün Sarayı & Organizasyon",
    "cacheEnabled": True,
    "duplicateImagePrevention": True,
    "maxUploadSizeMB": 50,
    "defaultLanguage": "tr",
    "allowedFileTypes": ["image/jpeg", "image/png", "image/webp", "video/mp4", "video/quicktime"],
    "updatedAt": "2026-08-01T01:28:00Z",
    "updatedBy": "admin"
}

with open(db_path, 'w', encoding='utf-8') as f:
    json.dump(initial_db, f, indent=2)
print("Created scratch/db_system_settings.json persistent system database!")

# 2. Update scratch/serve_fast_3g.py to serve and accept /api/system-settings
server_path = 'scratch/serve_fast_3g.py'
with open(server_path, 'r', encoding='utf-8') as f:
    server_code = f.read()

# Update GET handler in server
old_get_endpoint = """        elif parsed_path.path == '/api/system-config':"""
new_get_endpoint = """        elif parsed_path.path == '/api/system-settings' or parsed_path.path == '/api/system-config':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            db_file = os.path.join(os.path.dirname(__file__), 'db_system_settings.json')
            if os.path.exists(db_file):
                with open(db_file, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b'{"themeColor":"nordic-light"}')
            return"""

if old_get_endpoint in server_code:
    server_code = server_code.replace(old_get_endpoint, new_get_endpoint)
    print("Updated GET /api/system-settings in serve_fast_3g.py!")

# Update POST handler in server
old_post_endpoint = """        elif parsed_path.path == '/api/system-config':"""
new_post_endpoint = """        elif parsed_path.path == '/api/system-settings' or parsed_path.path == '/api/system-config':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                db_file = os.path.join(os.path.dirname(__file__), 'db_system_settings.json')
                
                # Merge with existing settings if exists
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
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b'{"status":"ok","message":"System settings updated in database"}')
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
            return"""

if old_post_endpoint in server_code:
    server_code = server_code.replace(old_post_endpoint, new_post_endpoint)
    print("Updated POST /api/system-settings in serve_fast_3g.py!")

# Update HTML server injection to read db_system_settings.json
old_html_inject = """                cfg_file = os.path.join(os.path.dirname(__file__), 'system_config.json')
                if os.path.exists(cfg_file):
                    with open(cfg_file, 'r', encoding='utf-8') as f:
                        sys_cfg = json.load(f)"""

new_html_inject = """                cfg_file = os.path.join(os.path.dirname(__file__), 'db_system_settings.json')
                if not os.path.exists(cfg_file):
                    cfg_file = os.path.join(os.path.dirname(__file__), 'system_config.json')
                if os.path.exists(cfg_file):
                    with open(cfg_file, 'r', encoding='utf-8') as f:
                        sys_cfg = json.load(f)"""

if old_html_inject in server_code:
    server_code = server_code.replace(old_html_inject, new_html_inject)
    print("Updated HTML 0ms theme injection in serve_fast_3g.py!")

with open(server_path, 'w', encoding='utf-8') as f:
    f.write(server_code)

# 3. Update index.html to sync with /api/system-settings
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace /api/system-config calls with /api/system-settings
html = html.replace('/api/system-config', '/api/system-settings')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html System Settings DB integration successfully!")
