import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for Sales Manager Empty Days AI Recommendations ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "Yapay Zeka Boş Gün & Aksiyon Önerileri" in html, "Yapay Zeka Boş Gün Önerileri missing!"
assert "Tek Tıkla Kampanyaya Dönüştür" in html, "Tek tıkla kampanyaya dönüştür button missing!"

print("   Source Code Verification: PASS!")

print("\n2. Testing HTTP GET /yonetim ...")
req = urllib.request.Request(f"{SERVER_URL}/yonetim")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nALL SALES EMPTY DAYS RECOMMENDATIONS TESTS PASSED 100%!")
