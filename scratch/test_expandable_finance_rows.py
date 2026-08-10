import urllib.request

print("1. Checking index.html source code for expandable contract row features ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "toggleExpandRes" in html, "toggleExpandRes function missing from index.html!"
assert "Kalem Kalem Gider & Finansal Döküm Detayı" in html, "Itemized breakdown header missing!"
assert "💰 Kalan Tahsil Edilecek Bakiye:" in html, "Remaining balance summary block missing!"
assert "🏰 Salon İşletim Maliyeti" in html, "Venue cost itemization block missing!"
assert "🛠️ Seçilen Ek Hizmetler" in html, "Services cost itemization block missing!"
assert "📝 Harcama & Yevmiyeler" in html, "Custom expenses itemization block missing!"

print("   HTML Code Verification: PASS!")

print("\n2. Testing HTTP GET /yonetim/finans ...")
req = urllib.request.Request("http://localhost:8001/yonetim/finans")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nALL EXPANDABLE FINANCE ROWS TESTS PASSED 100%!")
