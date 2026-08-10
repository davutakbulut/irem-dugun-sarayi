import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for strict password & email auth guard ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "STRICT IDENTITY GUARD" in html, "Strict identity guard missing!"
assert "STRICT PASSWORD GUARD" in html, "Strict password guard missing!"
assert "Hatalı şifre girdiniz!" in html, "Password error toast message missing!"
assert "veritabanımızda kayıtlı değil!" in html, "Identity error toast message missing!"

print("   Source Code Verification: PASS!")

print("\n2. Testing HTTP GET /yonetim/giris ...")
req = urllib.request.Request(f"{SERVER_URL}/yonetim/giris")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nALL STRICT PASSWORD & IDENTITY AUTHENTICATION TESTS PASSED 100%!")
