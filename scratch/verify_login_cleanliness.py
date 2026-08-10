import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for removal of demo preset buttons ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "Hızlı Canlı Rol Seçimi" not in html, "Demo preset buttons title still present!"
assert "mustafa@..." not in html, "Demo preset button text still present!"
assert "satis@..." not in html, "Demo preset button text still present!"

print("   Source Code Cleanliness Verification: PASS!")

print("\n2. Testing HTTP GET /yonetim/giris ...")
req = urllib.request.Request(f"{SERVER_URL}/yonetim/giris")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nALL LOGIN CLEANLINESS TESTS PASSED 100%!")
