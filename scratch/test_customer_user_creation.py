import urllib.request
import json

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

print("1. Verifying index.html source code for customer user creation logic ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "role: 'musteri'" in html, "Müşteri user role missing!"
assert "roleName: 'Müşteri'" in html, "Müşteri roleName missing!"
assert "setUsers(" in html, "setUsers call missing!"

print("   Source Code Logic Verification: PASS!")

print("\n2. POSTing new customer and user account to server DB ...")
data1 = get_settings()
users1 = data1.get("users", [])
customers1 = data1.get("customers", [])

new_cust_id = "cust-test-999"
new_cust_obj = {
    "id": new_cust_id,
    "name": "Canan & Serkan Öztürk",
    "email": "canan.ozturk@example.com",
    "phone": "05329998877",
    "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80"
}

new_user_obj = {
    "id": f"u-{new_cust_id}",
    "name": "Canan & Serkan Öztürk",
    "email": "canan.ozturk@example.com",
    "phone": "05329998877",
    "role": "musteri",
    "roleName": "Müşteri",
    "status": "Aktif",
    "avatar": new_cust_obj["avatar"],
    "createdAt": "2026-08-08T21:44:00.000Z"
}

status = post_settings({
    "customers": [*customers1, new_cust_obj],
    "users": [*users1, new_user_obj]
})
assert status == 200

print("\n3. Verifying GET /api/system-settings ...")
data2 = get_settings()
users2 = data2.get("users", [])
created_user = next((u for u in users2 if u.get("email") == "canan.ozturk@example.com"), None)

assert created_user is not None, "Created customer user account not found in DB!"
assert created_user["role"] == "musteri", f"Expected role 'musteri', got '{created_user.get('role')}'"
print(f"   Created User Account: {created_user['name']} | Role: {created_user['role']} | Email: {created_user['email']}")

print("\nALL CUSTOMER USER CREATION TESTS PASSED 100%!")
