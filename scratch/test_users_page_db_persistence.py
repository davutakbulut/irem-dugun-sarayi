import urllib.request
import json
import os

SERVER_URL = "http://localhost:8001"

def get_settings():
    req = urllib.request.Request(f"{SERVER_URL}/api/system-settings")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def post_settings(data):
    req = urllib.request.Request(
        f"{SERVER_URL}/api/system-settings",
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as response:
        return response.status

print("1. Verifying index.html source code for Users page database persistence ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "Kullanıcı (" in html and "Veritabanına Başarıyla Kaydedildi" in html, "handleSaveUser toast message missing!"
assert "Kullanıcı Veritabanından Silindi" in html, "handleDeleteUser toast message missing!"

print("   Source Code Verification: PASS!")

print("\n2. Testing POST user addition to database ...")
data1 = get_settings()
users1 = data1.get("users", [])

new_user = {
    "id": "u-test-management-99",
    "name": "Selin & Mert (Test Kullanıcısı)",
    "email": "selin.mert@example.com",
    "phone": "05329876543",
    "role": "satisci",
    "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80"
}

status = post_settings({"users": [*users1, new_user]})
assert status == 200

data2 = get_settings()
users2 = data2.get("users", [])
added_user = next((u for u in users2 if u.get("id") == "u-test-management-99"), None)
assert added_user is not None, "New user not found in DB!"
print(f"   Added User DB Record: {added_user['name']} | Role: {added_user['role']}")

print("\n3. Testing user deletion from database ...")
clean_users = [u for u in users2 if u.get("id") != "u-test-management-99"]
post_settings({"users": clean_users})

data3 = get_settings()
users3 = data3.get("users", [])
assert not any(u.get("id") == "u-test-management-99" for u in users3)
print("   Deleted User DB Sync: PASS!")

print("\nALL USERS PAGE DATABASE PERSISTENCE TESTS PASSED 100%!")
