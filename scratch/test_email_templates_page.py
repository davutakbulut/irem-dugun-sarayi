import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for Email Templates Page & Menu ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "title=\"E-Posta Şablonları ve Otomasyon Gönderim Merkezini Aç\"" not in html, "Old topbar button still present in header!"
assert "E-Posta Şablonları & Otomasyon" in html, "New menu item missing in index.html!"
assert "EmailTemplatesPageComponent" in html, "EmailTemplatesPageComponent missing in index.html!"
assert "Test Maili Gönder (SMTP 200 OK)" in html, "Test Maili Gönder button missing!"
assert "#/eposta-sablonlari" in html, "eposta-sablonlari route link missing!"

print("   Source Code Verification: PASS!")

print("\n2. Testing HTTP GET /yonetim/eposta-sablonlari ...")
req = urllib.request.Request(f"{SERVER_URL}/yonetim/eposta-sablonlari")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nEMAIL TEMPLATES DEDICATED PAGE & MENU TESTS PASSED 100%!")
