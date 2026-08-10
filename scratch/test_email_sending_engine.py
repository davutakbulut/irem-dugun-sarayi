import urllib.request
import json

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for /api/send-email API call ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "/api/send-email" in html, "/api/send-email API call missing in index.html!"
assert "SMTP Mail Sunucusu 200 OK" in html, "SMTP success toast missing!"

print("   Source Code Verification: PASS!")

print("\n2. Testing POST /api/send-email backend API ...")
email_payload = {
    "to": "test.musteri@iremdugunsarayi.com",
    "subject": "🔑 Test Şifre Yenileme ve Otomatik Giriş Bağlantısı",
    "body": "Test mail içeriği - İrem Düğün Sarayı SMTP Mail Engine"
}

req = urllib.request.Request(
    f"{SERVER_URL}/api/send-email",
    data=json.dumps(email_payload).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

with urllib.request.urlopen(req) as response:
    assert response.status == 200
    res_data = json.loads(response.read().decode('utf-8'))
    assert res_data.get("status") == "success"
    assert "mail.iremdugunsarayi.com" in res_data.get("smtp_server", "")
    print(f"   API Response 200 OK: Status='{res_data['status']}' | SMTP='{res_data['smtp_server']}' | Recipient='{res_data['recipient']}'")

print("\nALL EMAIL SENDING ENGINE TESTS PASSED 100%!")
