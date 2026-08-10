import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix invalid JSX placeholder attributes
bad_p1 = 'placeholder="<ThemeIcon icon="search" className="w-4 h-4 inline-block shrink-0" /> Müşteri Adı, Tel veya Sözleşme Kodu..."'
good_p1 = 'placeholder="🔍 Müşteri Adı, Tel veya Sözleşme Kodu..."'

bad_p2 = 'placeholder="<ThemeIcon icon="search" className="w-4 h-4 inline-block shrink-0" /> Ad, Soyad, Telefon veya E-posta ile Hızlı Ara..."'
good_p2 = 'placeholder="🔍 Ad, Soyad, Telefon veya E-posta ile Hızlı Ara..."'

if bad_p1 in content:
    content = content.replace(bad_p1, good_p1)
    print("Fixed bad_p1 syntax error.")

if bad_p2 in content:
    content = content.replace(bad_p2, good_p2)
    print("Fixed bad_p2 syntax error.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
