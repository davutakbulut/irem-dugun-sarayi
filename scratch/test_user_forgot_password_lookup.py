import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for user lookup & password display in forgot modal ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "Sistemde Kayıtlı Aktif Şifreniz" in html, "Active password display box missing!"
assert "forgotSuccessMail.matchedUser.password" in html, "User matched password reference missing!"
assert "Bu Şifre ve Hesapla Doğrudan Giriş Yap" in html, "One-click login button missing!"

print("   Source Code Verification: PASS!")

print("\n2. Testing HTTP GET /yonetim/giris ...")
req = urllib.request.Request(f"{SERVER_URL}/yonetim/giris")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nFORGOT PASSWORD USER LOOKUP & INSTANT PASSWORD DISPLAY TESTS PASSED 100%!")
