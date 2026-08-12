import os

files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for f_path in files:
    if not os.path.exists(f_path):
        continue
    with open(f_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace unescaped VPS'te in single-quoted string
    old_str = "summary: 'Kullanıcı profilinin (Ad, E-posta, Rol, Avatar) hem yerelde hem canlı VPS'te MySQL ile canlı senkronizasyonu.',"
    new_str = 'summary: "Kullanıcı profilinin (Ad, E-posta, Rol, Avatar) hem yerelde hem canlı VPS\'te MySQL ile canlı senkronizasyonu.",'

    if old_str in content:
        content = content.replace(old_str, new_str)
        with open(f_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully fixed single quote syntax error in {f_path}!")
    else:
        print(f"old_str not found in {f_path}!")

print("Syntax error fix completed!")
