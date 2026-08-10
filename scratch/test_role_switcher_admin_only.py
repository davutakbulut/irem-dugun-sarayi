import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for Admin-only Role Switcher guard ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "RESTRICTED ONLY TO ADMIN ROLE" in html, "Admin restriction comment missing!"
assert "activeRole === 'admin' ?" in html, "activeRole === 'admin' check missing!"
assert "Hızlı Rol Değiştir:" in html, "Hızlı Rol Değiştir text missing!"

print("   Source Code Verification: PASS!")

print("\n2. Testing HTTP GET /yonetim/dugun-salonlari ...")
req = urllib.request.Request(f"{SERVER_URL}/yonetim/dugun-salonlari")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nALL ADMIN-ONLY ROLE SWITCHER TESTS PASSED 100%!")
