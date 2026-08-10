import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for login page duplicate fix ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

showcase_count = html.count("RIGHT COLUMN: SINGLE FRESH NORDIC HERO SHOWCASE")
print(f"   Single Hero Showcase count in index.html: {showcase_count}")
assert showcase_count == 1, f"Expected exactly 1 hero showcase, but found {showcase_count}!"

assert "NORDIC LIGHT & FRESH LOGIN COMPONENT" in html, "Nordic Light login component marker missing!"
assert "Giriş Yapın" in html, "Login header text missing!"
assert "Hayallerinizin Ötesinde Bir" in html, "Nordic hero title missing!"

print("   Source Code Verification: PASS (No duplicates!)")

print("\n2. Testing HTTP GET /yonetim/giris ...")
req = urllib.request.Request(f"{SERVER_URL}/yonetim/giris")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nLOGIN PAGE DUPLICATE FIX & NORDIC LIGHT REDESIGN TESTS PASSED 100%!")
