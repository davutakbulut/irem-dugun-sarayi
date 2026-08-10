import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for DashboardComponent currentUser signature fix ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "function DashboardComponent({ activeRole, currentUser," in html, "currentUser parameter missing in DashboardComponent signature!"

print("   Source Code Verification: PASS!")

print("\n2. Testing HTTP GET /yonetim ...")
req = urllib.request.Request(f"{SERVER_URL}/yonetim")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nALL DASHBOARD CURRENT USER PROP FIX TESTS PASSED 100%!")
