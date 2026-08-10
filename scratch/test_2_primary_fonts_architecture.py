import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for 2 primary fonts + system fallback ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "Cormorant+Garamond" in html, "Cormorant Garamond heading font missing!"
assert "Great+Vibes" in html, "Great Vibes script accent font missing!"
assert "Plus+Jakarta+Sans" in html, "Plus Jakarta Sans body font missing!"
assert "--font-heading" in html, "--font-heading CSS variable missing!"
assert "--font-body" in html, "--font-body CSS variable missing!"
assert "system-ui, -apple-system" in html, "Universal system fallback font missing!"

print("   Typography Architecture Verification: PASS 100%!")

print("\n2. Testing HTTP GET / ...")
req = urllib.request.Request(f"{SERVER_URL}/")
with urllib.request.urlopen(req) as resp:
    assert resp.status == 200
    print("   HTTP 200 OK: PASS!")

print("\n2 PRIMARY FONTS + SYSTEM FALLBACK TYPOGRAPHY TESTS PASSED 100%!")
