import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for 90vw right slide-in mobile drawer ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "animate-slide-in-right" in html, "Right slide-in animation class missing!"
assert "w-[90vw]" in html, "90vw drawer width missing!"
assert "backdrop-blur-2xl" in html, "Glassmorphism backdrop blur missing!"
assert "HIZLI İLETİŞİM & RANDEVU" in html, "Bottom quick contact section missing!"
assert "MÜŞTERİ VIP PORTALI" in html, "Complete nav links missing!"

print("   Mobile Drawer Source Code Verification: PASS 100%!")

print("\n2. Testing HTTP GET / ...")
req = urllib.request.Request(f"{SERVER_URL}/")
with urllib.request.urlopen(req) as resp:
    assert resp.status == 200
    print("   HTTP 200 OK: PASS!")

print("\n90VW RIGHT SLIDE-IN MOBILE DRAWER TESTS PASSED 100%!")
