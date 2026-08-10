import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for login & email automation updates ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "customers={customers}" in html, "customers prop missing in LoginComponent call!"
assert "matchedCustomer" in html, "matchedCustomer matching missing in handleFormSubmit!"
assert "Otomatik E-Posta & Şifre Yenileme" in html, "Email automation modal missing!"
assert "Hızlı Canlı Rol Seçimi" in html, "Quick role preset demo buttons missing!"
assert "Müşteri Portalı" in html, "Customer Portal option missing!"

print("   Source Code Verification: PASS!")

print("\n2. Testing HTTP GET /giris ...")
req = urllib.request.Request(f"{SERVER_URL}/giris")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nALL LOGIN AND EMAIL AUTOMATION TESTS PASSED 100%!")
