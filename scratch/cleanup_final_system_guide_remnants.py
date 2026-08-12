import os

files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for f_path in files:
    if not os.path.exists(f_path):
        continue
    with open(f_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace("      'system-guide': 'system-guide',\n", "")

    with open(f_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Cleaned up line 1725 from {f_path}!")

print("Final cleanup completed!")
