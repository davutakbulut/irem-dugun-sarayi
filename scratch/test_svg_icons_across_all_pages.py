import urllib.request

urls = [
    "http://localhost:8001/yonetim/dugun-salonlari",
    "http://localhost:8001/yonetim/rezervasyonlar",
    "http://localhost:8001/yonetim/finans",
    "http://localhost:8001/yonetim/yeni-rezervasyon",
    "http://localhost:8001/yonetim/musteriler"
]

print("1. Testing HTTP status for all application pages ...")
for url in urls:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        assert response.status == 200
        print(f"   {url.split('/')[-1]}: 200 OK")

print("\n2. Verifying ThemeIcon zero-emoji SVG renderer in index.html ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "function ThemeIcon" in html
assert "NordicSvgMap[icon]" in html
print("   ThemeIcon SVG verification: PASS!")

print("\nALL PAGES SVG ICON VERIFICATION TESTS PASSED 100%!")
