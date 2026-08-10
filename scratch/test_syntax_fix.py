import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for single quote syntax fix ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "Müşteri Portalı'na" not in html, "Unescaped quote still present!"
assert "Müşteri Portalı alanına aktarılıyorsunuz..." in html, "Fixed string missing!"

print("   Source Code Syntax Verification: PASS!")

print("\n2. Testing HTTP GET /giris ...")
req = urllib.request.Request(f"{SERVER_URL}/giris")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nALL SYNTAX ERROR FIX TESTS PASSED 100%!")
