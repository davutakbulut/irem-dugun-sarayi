import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for high contrast Siteyi Gör button ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "Siteyi Gör ↗" in html, "New Siteyi Gör button text missing!"
assert "text-amber-900 dark:text-amber-300" in html, "High-contrast text color missing!"
assert "bg-amber-50 dark:bg-amber-500/10" in html, "Fresh Nordic Light background missing!"

print("   Source Code Verification: PASS (High contrast contrast button styling applied!)")

print("\n2. Testing HTTP GET /yonetim ...")
req = urllib.request.Request(f"{SERVER_URL}/yonetim")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nSITEYI GOR BUTTON CONTRAST TESTS PASSED 100%!")
