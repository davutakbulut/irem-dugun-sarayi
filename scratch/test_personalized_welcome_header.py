import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for personalized welcome header banner ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "Hoş Geldiniz, {userName}! 👋" in html, "Personalized welcome title missing!"
assert "currentUser={currentUserState}" in html, "currentUser prop missing in DashboardComponent call!"
assert "Sayın ${userName}" in html, "Personalized subtitle missing!"

print("   Source Code Verification: PASS!")

print("\n2. Testing HTTP GET /yonetim ...")
req = urllib.request.Request(f"{SERVER_URL}/yonetim")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nALL PERSONALIZED WELCOME HEADER TESTS PASSED 100%!")
