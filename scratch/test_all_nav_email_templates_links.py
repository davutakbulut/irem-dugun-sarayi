import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for Email Templates across all navigation menus ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "#/eposta-sablonlari" in html, "Sidebar hash link missing!"
assert "/yonetim/eposta-sablonlari" in html, "URL route mapping missing!"
assert "badge: 'SMTP 200 OK'" in html, "Mega Menu item badge missing!"
assert "navigateTo('email-templates')" in html, "Navigation handler missing!"

print("   Source Code Verification: PASS (All navigation menus updated successfully!)")

print("\n2. Testing HTTP GET /yonetim/eposta-sablonlari ...")
req = urllib.request.Request(f"{SERVER_URL}/yonetim/eposta-sablonlari")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nALL NAVIGATION MENUS EMAIL TEMPLATES LINKS TESTS PASSED 100%!")
