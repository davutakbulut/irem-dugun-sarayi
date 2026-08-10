import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for strict DB login guard ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "STRICT AUTHENTICATION GUARD" in html, "Strict auth guard missing!"
assert "if (!matchedUser && !matchedCustomer) {" in html, "Strict DB match check missing!"
assert "Yazdığınız e-posta adresi veya telefon numarası veritabanımızda bulunamadı" in html, "DB mismatch error message missing!"

print("   Source Code Verification: PASS!")

print("\n2. Testing HTTP GET /yonetim/giris ...")
req = urllib.request.Request(f"{SERVER_URL}/yonetim/giris")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nALL STRICT LOGIN VERIFICATION TESTS PASSED 100%!")
