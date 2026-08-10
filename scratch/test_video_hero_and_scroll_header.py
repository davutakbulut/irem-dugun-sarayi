import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for fullscreen video hero and scroll header ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "https://cdn.creafolks.com/svadba-davet/9e9fee9d-dc11-4bd5-bc7a-4614de2d7e2b.mp4" in html, "Full-screen video URL missing from index.html!"
assert "h-screen min-h-[100vh]" in html, "Full-screen video container height missing!"
assert "isTransparentMode = isHomePage && !isScrolled;" in html, "Dynamic transparent header mode logic missing!"
assert "transition-all duration-500 ease-in-out" in html, "Header scroll transition class missing!"

print("   Source Code Verification: PASS (Full-screen video hero & dynamic scroll header implemented!)")

print("\n2. Testing HTTP GET / (Public Landing Page) ...")
req = urllib.request.Request(f"{SERVER_URL}/")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nFULLSCREEN VIDEO HERO & DYNAMIC SCROLL HEADER TESTS PASSED 100%!")
