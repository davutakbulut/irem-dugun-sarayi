import re
import sys

# 1. Update index.html line 2 to clean <html lang="tr" class="light">
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(r'<html[^>]*>', '<html lang="tr" class="light">', html, count=1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Cleaned index.html html tag to <html lang=\"tr\" class=\"light\">!")

# 2. Update serve_fast_3g.py to cleanly replace <html lang="tr" class="light"> with active theme & menu layout
with open('scratch/serve_fast_3g.py', 'r', encoding='utf-8') as f:
    py_code = f.read()

old_injection = """                        active_t = sys_cfg.get('themeColor', 'nordic-light')
                        active_m = sys_cfg.get('menuLayout', 'vertical')
                        inject_str = f'<html lang="tr" data-ui-theme="{active_t}" data-menu-layout="{active_m}"'
                        
                        # Regex replace any <html... > tag on line 1 with our exact server DB injected attributes
                        content_str = content.decode('utf-8', errors='ignore')
                        content_str = re.sub(r'<html[^>]*>', inject_str + '>', content_str, count=1)
                        content = content_str.encode('utf-8')"""

new_injection = """                        active_t = sys_cfg.get('themeColor', 'nordic-light')
                        active_m = sys_cfg.get('menuLayout', 'vertical')
                        inject_str = f'<html lang="tr" class="light" data-ui-theme="{active_t}" data-menu-layout="{active_m}">'
                        
                        content_str = content.decode('utf-8', errors='ignore')
                        content_str = re.sub(r'<html[^>]*>', inject_str, content_str, count=1)
                        content = content_str.encode('utf-8')"""

if old_injection in py_code:
    py_code = py_code.replace(old_injection, new_injection)
    print("Cleaned serve_fast_3g.py html injection!")

with open('scratch/serve_fast_3g.py', 'w', encoding='utf-8') as f:
    f.write(py_code)

print("Updated HTML root tag cleaning successfully!")
