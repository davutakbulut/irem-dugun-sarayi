import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for guaranteed circle button & bottom-24 popup position ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "borderRadius: '9999px'" in html, "Guaranteed circle inline style missing!"
assert "bottom-24 sm:bottom-28" in html, "Valid bottom-24 popup position missing!"
assert "rotate(360deg)" in html, "360 degree rotation transform missing!"
assert "Hızlı Randevu!" in html, "Hızlı Randevu! card missing!"
assert "Bilgi Al!" in html, "Bilgi Al! card missing!"

print("   Source Code Verification: PASS 100%!")

print("\n2. Testing HTTP GET / ...")
req = urllib.request.Request(f"{SERVER_URL}/")
with urllib.request.urlopen(req) as resp:
    assert resp.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nGUARANTEED CIRCLE & POPUP BOX TESTS PASSED 100%!")
