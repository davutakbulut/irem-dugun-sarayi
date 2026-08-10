import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for Fresh Nordic Light guest mode footer ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "FRESH NORDIC LIGHT PUBLIC GUEST FOOTER" in html, "Guest footer code block missing!"
assert "256-Bit SSL Korumalı Anı Galeri" in html, "SSL security badge missing!"
assert "Sapanca Göl Kenarı, Sakarya" in html, "Location badge missing!"
assert "+90 (264) 582 00 00" in html, "Phone badge missing!"

print("   Source Code Verification: PASS!")

print("\n2. Testing HTTP GET /medya/RES-2026-3791 ...")
req = urllib.request.Request(f"{SERVER_URL}/medya/RES-2026-3791")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nFRESH NORDIC LIGHT GUEST FOOTER TESTS PASSED 100%!")
