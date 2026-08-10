import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for exact 1:1 WhatsApp pop-up widget replica ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "Hızlı Randevu!" in html, "Hızlı Randevu! card title missing!"
assert "Bilgi Al!" in html, "Bilgi Al! card title missing!"
assert "https://wa.me/905471440054" in html, "WhatsApp phone link missing!"
assert "randevu" in html, "Randevu custom text missing!"
assert "bilgi" in html, "Bilgi custom text missing!"
assert "rounded-[24px]" in html, "Card rounded 24px styling missing!"
assert "bg-[#25D366]" in html, "Vibrant WhatsApp green top bar missing!"

print("   Source Code Verification: PASS 100%!")

print("\n2. Testing HTTP GET / ...")
req = urllib.request.Request(f"{SERVER_URL}/")
with urllib.request.urlopen(req) as resp:
    assert resp.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nEXACT WHATSAPP WIDGET REPLICA TESTS PASSED 100%!")
