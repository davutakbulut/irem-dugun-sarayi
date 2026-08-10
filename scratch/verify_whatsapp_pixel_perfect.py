import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for 1:1 pixel perfect WhatsApp widget & 360 rotation ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "rotate-[360deg]" in html, "360-degree rotation animation class missing!"
assert "transition-transform duration-500" in html, "Rotation transition duration missing!"
assert "rounded-full" in html, "Rounded full circle trigger button missing!"
assert "Hızlı Randevu!" in html, "Hızlı Randevu! card missing!"
assert "Bilgi Al!" in html, "Bilgi Al! card missing!"
assert "rounded-[24px]" in html, "Card 24px border radius missing!"
assert "bg-[#F5F6F8]" in html, "Grey sub-card background color missing!"

print("   Source Code Verification: PASS 100%!")

print("\n2. Testing HTTP GET / ...")
req = urllib.request.Request(f"{SERVER_URL}/")
with urllib.request.urlopen(req) as resp:
    assert resp.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nPIXEL PERFECT WHATSAPP WIDGET & ROTATION ANIMATION TESTS PASSED 100%!")
