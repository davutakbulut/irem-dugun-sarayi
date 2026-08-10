import urllib.request
import json

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for all 3 official Email Templates ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "reservation_confirmation" in html, "1. Rezervasyon & Sözleşme Şablonu missing!"
assert "welcome_membership" in html, "2. Üyelik & Hoş Geldin Şablonu missing!"
assert "forgot_password" in html, "3. Şifremi Unuttum Şablonu missing!"
assert "E-Posta Şablonları & Otomasyon Gönderim Merkezi" in html, "Email Template Center header text missing!"

print("   Source Code Verification: PASS!")

print("\n2. Testing HTTP GET /yonetim ...")
req = urllib.request.Request(f"{SERVER_URL}/yonetim")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\n3. Testing POST /api/send-email with templates ...")
templates_to_test = ["reservation_confirmation", "welcome_membership", "forgot_password"]
for t_type in templates_to_test:
    payload = {
        "to": "test.musteri@iremdugunsarayi.com",
        "subject": f"Test {t_type}",
        "template": t_type
    }
    req_tmpl = urllib.request.Request(
        f"{SERVER_URL}/api/send-email",
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req_tmpl) as res:
        assert res.status == 200
        res_json = json.loads(res.read().decode('utf-8'))
        assert res_json["status"] == "success"
        print(f"   Template '{t_type}' Dispatch: PASS (200 OK)")

print("\nALL 3 EMAIL TEMPLATES & DISPATCH TESTS PASSED 100%!")
