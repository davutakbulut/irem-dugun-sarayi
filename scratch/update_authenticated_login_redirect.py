import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_cond = "else if ((cleanPath === '/giris' || cleanPath === '/login') && sessionUser) {"
new_cond = "else if ((cleanPath === '/giris' || cleanPath === '/login' || cleanPath === '/yonetim/giris' || cleanPath === '/yonetim/login') && sessionUser) {"

if old_cond in content:
    content = content.replace(old_cond, new_cond)
    print("1. Successfully updated authenticated login redirect condition.")
else:
    print("WARNING: Could not find old_cond in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
