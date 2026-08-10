import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for modular fault-isolated block architecture ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "class BlockErrorBoundary extends React.Component" in html, "BlockErrorBoundary missing!"
assert "PublicHeroBlock" in html, "PublicHeroBlock component missing!"
assert "PublicWelcomeBlock" in html, "PublicWelcomeBlock component missing!"
assert "PublicServicesBlock" in html, "PublicServicesBlock component missing!"
assert "PublicHallsBlock" in html, "PublicHallsBlock component missing!"
assert "PublicMenusBlock" in html, "PublicMenusBlock component missing!"
assert "PublicTestimonialsBlock" in html, "PublicTestimonialsBlock component missing!"

# Check BlockErrorBoundary wraps
assert '<BlockErrorBoundary blockName="Video Hero Header">' in html, "Video Hero BlockErrorBoundary missing!"
assert '<BlockErrorBoundary blockName="Üst Navigasyon (Header)">' in html, "Navbar BlockErrorBoundary missing!"
assert '<BlockErrorBoundary blockName="Alt Footer & WhatsApp Destek">' in html, "Footer BlockErrorBoundary missing!"

print("   Modular Block Architecture Verification: PASS 100%!")

print("\n2. Testing HTTP GET / ...")
req = urllib.request.Request(f"{SERVER_URL}/")
with urllib.request.urlopen(req) as resp:
    assert resp.status == 200
    print("   HTTP 200 OK: PASS!")

print("\n3. Testing HTTP GET /salonlar ...")
req_halls = urllib.request.Request(f"{SERVER_URL}/salonlar")
with urllib.request.urlopen(req_halls) as resp_halls:
    assert resp_halls.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nMODULAR FAULT-ISOLATED BLOCKS ARCHITECTURE TESTS PASSED 100%!")
