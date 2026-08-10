import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for WhatsApp pop-up support widget ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "isWhatsAppWidgetOpen" in html, "isWhatsAppWidgetOpen state missing from index.html!"
assert "WhatsApp Destek" in html, "WhatsApp Destek title missing!"
assert "Davut Akbulut - Hızlı Destek" in html, "Davut Akbulut contact card missing!"
assert "https://wa.me/905471440054" in html, "WhatsApp phone link missing!"

print("   Source Code Verification: PASS 100%!")

print("\n2. Testing HTTP GET / ...")
req = urllib.request.Request(f"{SERVER_URL}/")
with urllib.request.urlopen(req) as resp:
    assert resp.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nWHATSAPP POPUP SUPPORT WIDGET TESTS PASSED 100%!")
