import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for redesigned luxury Forgot Password modal ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "Şifremi Unuttum & Aktivasyon" in html, "New modal header missing!"
assert "bg-slate-900 border-2 border-amber-500/50" in html, "New modal high-contrast dark card container missing!"
assert "Kayıtlı E-Posta veya Telefon:" in html, "New input label text missing!"
assert "Otomatik E-Posta Gönder" in html, "Email send button text missing!"

print("   Source Code Verification: PASS!")

print("\n2. Testing HTTP GET /yonetim/giris ...")
req = urllib.request.Request(f"{SERVER_URL}/yonetim/giris")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nREDESIGNED LUXURY FORGOT PASSWORD MODAL TESTS PASSED 100%!")
