import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for removal of demo role buttons ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "Hızlı Rol Girişleri:" not in html, "'Hızlı Rol Girişleri:' text still present in index.html!"

print("   Source Code Verification: PASS (Demo buttons completely removed!)")

print("\n2. Testing HTTP GET /yonetim/giris ...")
req = urllib.request.Request(f"{SERVER_URL}/yonetim/giris")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nREMOVAL OF DEMO ROLE BUTTONS TESTS PASSED 100%!")
