import os
import json
import sys

# 1. Ensure scratch/system_config.json exists with default nordic-light theme
config_path = 'scratch/system_config.json'
default_config = {
    "themeColor": "nordic-light",
    "updatedAt": "2026-08-01T01:16:00Z"
}
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(default_config, f, indent=2)
print("Created scratch/system_config.json with default nordic-light theme!")

# 2. Update scratch/serve_fast_3g.py to handle /api/system-config GET/POST and inject data-ui-theme into HTML
server_path = 'scratch/serve_fast_3g.py'
with open(server_path, 'r', encoding='utf-8') as f:
    server_code = f.read()

# Add GET/POST system-config handler to do_GET and do_POST in server
old_get_handler = """        elif parsed_path.path == '/api/ping':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
            return"""

new_get_handler = """        elif parsed_path.path == '/api/system-config':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            cfg_file = os.path.join(os.path.dirname(__file__), 'system_config.json')
            if os.path.exists(cfg_file):
                with open(cfg_file, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b'{"themeColor":"nordic-light"}')
            return
        elif parsed_path.path == '/api/ping':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
            return"""

if old_get_handler in server_code and "/api/system-config" not in server_code:
    server_code = server_code.replace(old_get_handler, new_get_handler)
    print("Added /api/system-config GET handler to serve_fast_3g.py!")

# Add POST handler for /api/system-config
old_post_handler = """        elif parsed_path.path == '/api/upload-media':"""
new_post_handler = """        elif parsed_path.path == '/api/system-config':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                cfg_file = os.path.join(os.path.dirname(__file__), 'system_config.json')
                with open(cfg_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b'{"status":"ok","message":"System config updated"}')
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
            return
        elif parsed_path.path == '/api/upload-media':"""

if old_post_handler in server_code and "path == '/api/system-config'" not in server_code.split('do_POST')[1]:
    server_code = server_code.replace(old_post_handler, new_post_handler)
    print("Added /api/system-config POST handler to serve_fast_3g.py!")

# Inject active theme into HTML response in server
old_html_serve = """            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)"""

new_html_serve = """            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            try:
                cfg_file = os.path.join(os.path.dirname(__file__), 'system_config.json')
                if os.path.exists(cfg_file):
                    with open(cfg_file, 'r', encoding='utf-8') as f:
                        sys_cfg = json.load(f)
                    active_t = sys_cfg.get('themeColor', 'nordic-light')
                    if active_t and active_t != 'gold' and active_t != 'classic_gold':
                        content = content.replace(b'<html lang="tr"', f'<html lang="tr" data-ui-theme="{active_t}"'.encode('utf-8'))
            except Exception as e:
                pass
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)"""

if old_html_serve in server_code and "data-ui-theme" not in server_code:
    server_code = server_code.replace(old_html_serve, new_html_serve)
    print("Added 0ms server HTML data-ui-theme injection to serve_fast_3g.py!")

with open(server_path, 'w', encoding='utf-8') as f:
    f.write(server_code)

# 3. Update index.html CSS rules to refine Nordic Light theme concept (Dropzone, Shadows, Badges, Buttons)
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

nordic_concept_css = """
    /* ------------------------------------------------------------------- */
    /* NORDIC LIGHT SCANDINAVIAN MINIMALIST ARCHITECTURE DESIGN SYSTEM    */
    /* ------------------------------------------------------------------- */
    html[data-ui-theme="nordic-light"] body {
      background-color: #FAFAFA !important;
      color: #0F172A !important;
    }

    html[data-ui-theme="nordic-light"] .glass-panel {
      background-color: #FFFFFF !important;
      border: 1px solid #CBD5E1 !important;
      box-shadow: 0 4px 20px rgba(15, 23, 42, 0.05) !important;
    }

    html[data-ui-theme="nordic-light"] .border-dashed {
      border-color: #0F172A !important;
    }

    html[data-ui-theme="nordic-light"] .border-dashed:hover {
      border-color: #0F172A !important;
      background-color: #F8FAFC !important;
    }

    html[data-ui-theme="nordic-light"] .gold-button {
      background: #0F172A !important;
      color: #FFFFFF !important;
      border: 2px solid #334155 !important;
      box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15) !important;
      border-radius: 8px !important;
    }

    html[data-ui-theme="nordic-light"] .gold-button:hover {
      background: #1E293B !important;
      color: #FFFFFF !important;
    }

    html[data-ui-theme="nordic-light"] .bg-slate-900\/90,
    html[data-ui-theme="nordic-light"] .bg-slate-950\/90 {
      background-color: #0F172A !important;
      border-color: #334155 !important;
    }

    html[data-ui-theme="nordic-light"] .text-amber-500,
    html[data-ui-theme="nordic-light"] .text-amber-600,
    html[data-ui-theme="nordic-light"] .text-amber-700 {
      color: #0F172A !important;
    }
"""

target_css_anchor = "    /* ------------------------------------------------------------------- */\n    /* NORDIC LIGHT THEME: PURE MONOCHROME SLATE & WHITE (NO ORANGE / AMBER) */"
if target_css_anchor in html and "NORDIC LIGHT SCANDINAVIAN MINIMALIST ARCHITECTURE" not in html:
    html = html.replace(target_css_anchor, nordic_concept_css + "\n" + target_css_anchor)
    print("Added Nordic Light Scandinavian Minimalist Design System CSS to index.html!")

# Update theme change handler in Settings (lines around 15570) to post to /api/system-config
old_theme_save_block = """                        CacheService.set('theme_color', draftTheme);
                        setThemeColor(draftTheme);"""

new_theme_save_block = """                        CacheService.set('theme_color', draftTheme);
                        CacheService.set('selected_theme', draftTheme);
                        setThemeColor(draftTheme);
                        try {
                          fetch('/api/system-config', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ themeColor: draftTheme, updatedAt: new Date().toISOString() })
                          }).catch(() => {});
                        } catch(e) {}"""

if old_theme_save_block in html:
    html = html.replace(old_theme_save_block, new_theme_save_block)
    print("Updated Settings theme save block to sync with /api/system-config!")

# Update App component mount to fetch /api/system-config
old_app_mount_effect = """      useEffect(() => {
        CacheService.set('theme_color', themeColor);
        CacheService.set('selected_theme', themeColor);"""

new_app_mount_effect = """      useEffect(() => {
        try {
          fetch('/api/system-config')
            .then(res => res.json())
            .then(data => {
              if (data && data.themeColor && data.themeColor !== themeColor) {
                setThemeColor(data.themeColor);
              }
            }).catch(() => {});
        } catch(e) {}
      }, []);

      useEffect(() => {
        CacheService.set('theme_color', themeColor);
        CacheService.set('selected_theme', themeColor);"""

if old_app_mount_effect in html:
    html = html.replace(old_app_mount_effect, new_app_mount_effect)
    print("Updated App component mount effect to fetch server global theme config!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Implemented Global System Config & Nordic Concept Refinement successfully!")
