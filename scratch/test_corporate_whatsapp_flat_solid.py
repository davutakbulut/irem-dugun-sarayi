import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for Corporate WhatsApp redesign & solid glow-free buttons ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "bg-[#075E54]" in html, "Corporate WhatsApp dark green header missing!"
assert "borderRadius: '9999px'" in html, "Guaranteed circle inline style missing!"
assert "rotate(360deg)" in html, "360 degree rotation transform missing!"
assert "Hızlı Randevu!" in html, "Hızlı Randevu! contact card missing!"
assert "Bilgi Al!" in html, "Bilgi Al! contact card missing!"
assert "bg-[#B89B5E]" in html, "Solid gold phone button missing!"
assert "bg-[#25D366]" in html, "Solid green WhatsApp button missing!"

print("   Source Code Verification: PASS 100%!")

print("\n2. Testing HTTP GET / ...")
req = urllib.request.Request(f"{SERVER_URL}/")
with urllib.request.urlopen(req) as resp:
    assert resp.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nCORPORATE WHATSAPP REDESIGN & SOLID BUTTONS TESTS PASSED 100%!")
