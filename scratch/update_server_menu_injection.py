import sys

with open('scratch/serve_fast_3g.py', 'r', encoding='utf-8') as f:
    py_code = f.read()

old_injection = """                        active_t = sys_cfg.get('themeColor', 'nordic-light')
                        if active_t and active_t != 'gold' and active_t != 'classic_gold':
                            content = content.replace(b'<html lang="tr"', f'<html lang="tr" data-ui-theme="{active_t}"'.encode('utf-8'))
                            content = content.replace(b'<html lang=\"tr\"', f'<html lang="tr" data-ui-theme="{active_t}"'.encode('utf-8'))"""

new_injection = """                        active_t = sys_cfg.get('themeColor', 'nordic-light')
                        active_m = sys_cfg.get('menuLayout', 'vertical')
                        inject_str = f'<html lang="tr" data-ui-theme="{active_t}" data-menu-layout="{active_m}"'
                        content = content.replace(b'<html lang="tr"', inject_str.encode('utf-8'))
                        content = content.replace(b'<html lang=\"tr\"', inject_str.encode('utf-8'))"""

if old_injection in py_code:
    py_code = py_code.replace(old_injection, new_injection)
    print("Updated server HTML injection in serve_fast_3g.py to inject both data-ui-theme and data-menu-layout!")

with open('scratch/serve_fast_3g.py', 'w', encoding='utf-8') as f:
    f.write(py_code)

print("Updated serve_fast_3g.py server script successfully!")
