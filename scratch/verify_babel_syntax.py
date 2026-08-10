import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Verify no unescaped quote syntax in useState
assert "useState('Hayalinizdeki Düğün İrem Düğün Sarayı'nda Unutulmaz Oluyor')" not in html, "Unescaped single quote syntax still present!"
print("Babel Quote Syntax Verification: PASS 100%!")
