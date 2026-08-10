import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

bad_line = "const [publicTitle, setPublicTitle] = useState('Hayalinizdeki Düğün İrem Düğün Sarayı'nda Unutulmaz Oluyor');"
fixed_line = 'const [publicTitle, setPublicTitle] = useState("Hayalinizdeki Düğün İrem Düğün Sarayı\'nda Unutulmaz Oluyor");'

if bad_line in content:
    content = content.replace(bad_line, fixed_line, 1)
    print("Fixed unescaped single quote syntax error in publicTitle useState!")
else:
    print("WARNING: Could not find bad_line in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
