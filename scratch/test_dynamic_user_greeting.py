import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for dynamic user greeting on dashboard ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "const activeUser = currentUser || sessionUser;" in html, "Dynamic activeUser resolution missing!"
assert "const userName = activeUser?.name || 'Sayın Yöneticimiz';" in html, "Dynamic userName resolution missing!"
assert "Hoş Geldiniz, Mustafa Bey" not in html, "Hardcoded 'Hoş Geldiniz, Mustafa Bey' string still present in index.html!"

print("   Source Code Verification: PASS (Dynamic user greeting implemented!)")

print("\n2. Testing HTTP GET /yonetim ...")
req = urllib.request.Request(f"{SERVER_URL}/yonetim")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nDYNAMIC USER GREETING TESTS PASSED 100%!")
