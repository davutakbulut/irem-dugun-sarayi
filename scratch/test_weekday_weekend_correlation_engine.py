import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for Weekday vs. Weekend Correlation Engine ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "Hafta İçi & Hafta Sonu Korelasyon Analizi" in html, "Hafta içi & hafta sonu korelasyon analizi missing!"
assert "HAFTAICI20" in html, "HAFTAICI20 campaign code missing!"
assert "Tek Tıkla Hafta İçi Kampanyasına Dönüştür" in html, "Hafta içi kampanya dönüştürme butonu missing!"

print("   Source Code Verification: PASS!")

print("\n2. Testing HTTP GET /yonetim ...")
req = urllib.request.Request(f"{SERVER_URL}/yonetim")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nALL WEEKDAY VS WEEKEND CORRELATION ENGINE TESTS PASSED 100%!")
