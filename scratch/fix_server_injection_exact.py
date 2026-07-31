import re
import sys

with open('scratch/serve_fast_3g.py', 'r', encoding='utf-8') as f:
    py_code = f.read()

target_section = """                    # 0ms Server HTML data-ui-theme Injection from db_system_settings.json
                    db_file = os.path.join(os.path.dirname(__file__), 'db_system_settings.json')
                    if os.path.exists(db_file):
                        with open(db_file, 'r', encoding='utf-8') as dbf:
                            sys_cfg = json.load(dbf)
                        active_t = sys_cfg.get('themeColor', 'nordic-light')
                        if active_t and active_t != 'gold' and active_t != 'classic_gold':
                            content = content.replace(b'<html lang="tr"', f'<html lang="tr" data-ui-theme="{active_t}"'.encode('utf-8'))
                            content = content.replace(b'<html lang=\"tr\"', f'<html lang="tr" data-ui-theme="{active_t}"'.encode('utf-8'))"""

replacement_section = """                    # 0ms Server HTML System Settings Injection (data-ui-theme & data-menu-layout) from db_system_settings.json
                    db_file = os.path.join(os.path.dirname(__file__), 'db_system_settings.json')
                    if os.path.exists(db_file):
                        with open(db_file, 'r', encoding='utf-8') as dbf:
                            sys_cfg = json.load(dbf)
                        active_t = sys_cfg.get('themeColor', 'nordic-light')
                        active_m = sys_cfg.get('menuLayout', 'vertical')
                        inject_tag = f'<html lang="tr" class="light" data-ui-theme="{active_t}" data-menu-layout="{active_m}">'
                        content_str = content.decode('utf-8', errors='ignore')
                        content_str = re.sub(r'<html[^>]*>', inject_tag, content_str, count=1)
                        content = content_str.encode('utf-8')"""

if target_section in py_code:
    py_code = py_code.replace(target_section, replacement_section)
    print("Replaced serve_fast_3g.py HTML injection section successfully!")
else:
    print("target_section not found exactly, attempting regex replace...")
    py_code = re.sub(
        r'# 0ms Server HTML data-ui-theme Injection.*?\n\n',
        replacement_section + '\n\n',
        py_code,
        flags=re.DOTALL
    )

with open('scratch/serve_fast_3g.py', 'w', encoding='utf-8') as f:
    f.write(py_code)

print("Updated serve_fast_3g.py successfully!")
