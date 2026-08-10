import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix unescaped single quote in showToast call line 9188
old_line = "showToast(`Hoş geldiniz ${userObj.name}! (${isCustomerRole ? 'Müşteri Portalı'na aktarılıyorsunuz...' : 'Yönetim paneline aktarılıyorsunuz...'})`);"
new_line = "showToast(`Hoş geldiniz ${userObj.name}! (${isCustomerRole ? 'Müşteri Portalı alanına aktarılıyorsunuz...' : 'Yönetim paneline aktarılıyorsunuz...'})`);"

if old_line in content:
    content = content.replace(old_line, new_line)
    print("1. Successfully fixed unescaped single quote in showToast string literal!")
else:
    print("WARNING: Could not find old_line in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
