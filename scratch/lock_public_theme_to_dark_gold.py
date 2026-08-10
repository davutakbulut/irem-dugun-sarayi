import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make sure inline init script always sets data-ui-theme to 'dark-gold'
target_str = "document.documentElement.setAttribute('data-ui-theme', d.themeColor);"
replacement_str = "document.documentElement.setAttribute('data-ui-theme', 'dark-gold');"

if target_str in content:
    content = content.replace(target_str, replacement_str)
    print("Locked data-ui-theme init script to 'dark-gold'!")

target_str2 = "document.documentElement.setAttribute('data-theme', d.themeColor);"
replacement_str2 = "document.documentElement.setAttribute('data-theme', 'dark-gold');"

if target_str2 in content:
    content = content.replace(target_str2, replacement_str2)
    print("Locked data-theme init script to 'dark-gold'!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
