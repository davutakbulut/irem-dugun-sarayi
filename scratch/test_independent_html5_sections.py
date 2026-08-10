import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for independent HTML5 section containers ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert '<section id="section-hero"' in html, "section-hero container missing!"
assert '<section id="section-welcome"' in html, "section-welcome container missing!"
assert '<section id="section-services"' in html, "section-services container missing!"
assert '<section id="section-halls"' in html, "section-halls container missing!"
assert '<section id="section-menus"' in html, "section-menus container missing!"
assert '<section id="section-testimonials"' in html, "section-testimonials container missing!"

print("   Independent HTML5 Section Containers Verification: PASS 100%!")

print("\n2. Testing HTTP GET / ...")
req = urllib.request.Request(f"{SERVER_URL}/")
with urllib.request.urlopen(req) as resp:
    assert resp.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nINDEPENDENT HTML5 SECTIONS TESTS PASSED 100%!")
