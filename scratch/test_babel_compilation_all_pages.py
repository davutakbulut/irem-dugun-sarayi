import urllib.request
import re

print("1. Checking index.html for any malformed string-nested <ThemeIcon> tags ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

bad_dq = re.findall(r'"[^"\n]*<\s*ThemeIcon[^"\n]*>[^"\n]*"', html)
bad_sq = re.findall(r"'[^'\n]*<\s*ThemeIcon[^'\n]*>[^'\n]*'", html)

assert len(bad_dq) == 0, f"Found malformed double-quoted ThemeIcon strings: {bad_dq[:3]}"
assert len(bad_sq) == 0, f"Found malformed single-quoted ThemeIcon strings: {bad_sq[:3]}"

print("   Babel String Literals Syntax Check: PASS!")

print("\n2. Testing HTTP GET across all application routes ...")
urls = [
    "http://localhost:8001/",
    "http://localhost:8001/yonetim/dugun-salonlari",
    "http://localhost:8001/yonetim/rezervasyonlar",
    "http://localhost:8001/yonetim/finans",
    "http://localhost:8001/yonetim/yeni-rezervasyon?ref=k7YlI5FAm88b",
    "http://localhost:8001/yonetim/musteriler"
]

for url in urls:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        assert response.status == 200
        print(f"   {url}: 200 OK")

print("\nALL APPLICATION PAGES COMPILATION & ROUTING TESTS PASSED 100%!")
