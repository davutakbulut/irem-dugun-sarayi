import re

# 1. Update serve_fast_3g.py to inject data-system-version into <html> tag
with open('scratch/serve_fast_3g.py', 'r', encoding='utf-8') as f:
    server_code = f.read()

old_server_snippet = """                        active_t = sys_cfg.get('themeColor', 'nordic-light')
                        active_m = sys_cfg.get('menuLayout', 'vertical')
                        inject_tag = f'<html lang="tr" class="light" data-ui-theme="{active_t}" data-menu-layout="{active_m}">'"""

new_server_snippet = """                        active_t = sys_cfg.get('themeColor', 'nordic-light')
                        active_m = sys_cfg.get('menuLayout', 'vertical')
                        active_v = sys_cfg.get('systemVersion', 'v1.4.67')
                        inject_tag = f'<html lang="tr" class="light" data-ui-theme="{active_t}" data-menu-layout="{active_m}" data-system-version="{active_v}">'"""

if old_server_snippet in server_code:
    server_code = server_code.replace(old_server_snippet, new_server_snippet)
    with open('scratch/serve_fast_3g.py', 'w', encoding='utf-8') as f:
        f.write(server_code)
    print("Updated serve_fast_3g.py to inject data-system-version successfully!")
else:
    print("Could not find old_server_snippet in serve_fast_3g.py!")

# 2. Update index.html to read data-system-version synchronously on Frame 0 and purge hardcoded fallback version strings
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix useState initializer
html = html.replace(
    "const [systemVersion, setSystemVersion] = useState('v1.4.48');",
    "const [systemVersion, setSystemVersion] = useState(() => (typeof document !== 'undefined' && document.documentElement.getAttribute('data-system-version')) || 'v1.4.67');"
)

# Fix Header fallback
html = html.replace(
    "<span>Canlı Sistem ({systemVersion || 'v1.4.48'})</span>",
    "<span>Canlı Sistem ({systemVersion})</span>"
)

# Fix Footer call fallback
html = html.replace(
    "systemVersion={systemVersion || 'v1.4.62'}",
    "systemVersion={systemVersion}"
)

# Fix GlobalFooterComponent fallback
html = html.replace(
    "<span>Canlı Sistem ({systemVersion || 'v1.4.56'}) (Sürüm Notları 📋)</span>",
    "<span>Canlı Sistem ({systemVersion}) (Sürüm Notları 📋)</span>"
)

# Fix VersionHistoryModalComponent fallback
html = html.replace(
    "{systemVersion || \"v1.4.56\"}",
    "{systemVersion}"
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Synchronized all systemVersion states and purged hardcoded fallback strings in index.html successfully!")
