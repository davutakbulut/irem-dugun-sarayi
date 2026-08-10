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

print("1. Testing GET /api/system-settings for users ...")
data1 = get_settings()
users1 = data1.get("users", [])
print(f"   Current users count in DB: {len(users1)}")
for u in users1:
    print(f"   - User: {u.get('name')} | Role: {u.get('role')} | Email: {u.get('email')}")

print("\n2. Checking scratch/db_users.json on disk ...")
db_users_path = os.path.join("scratch", "db_users.json")
assert os.path.exists(db_users_path), "scratch/db_users.json file does not exist!"

with open(db_users_path, "r", encoding="utf-8") as f:
    disk_users = json.load(f)

print(f"   scratch/db_users.json disk users count: {len(disk_users)}")
assert len(disk_users) == len(users1), "Disk users count does not match GET /api/system-settings count!"

print("\n3. Testing adding a new user to database ...")
test_user = {
    "id": "u-test-persistence-100",
    "name": "Burak Şahin (Test Kullanıcısı)",
    "email": "burak.sahin@example.com",
    "phone": "05421112233",
    "role": "musteri",
    "roleName": "Müşteri",
    "status": "Aktif",
    "createdAt": "2026-08-08T21:45:00.000Z"
}

status = post_settings({"users": [*users1, test_user]})
assert status == 200

with open(db_users_path, "r", encoding="utf-8") as f:
    disk_users2 = json.load(f)

assert any(u.get("id") == "u-test-persistence-100" for u in disk_users2), "New user not saved in db_users.json!"
print("   New user disk persistence: PASS!")

print("\n4. Re-fetching GET /api/system-settings ...")
data2 = get_settings()
users2 = data2.get("users", [])
fetched_user = next((u for u in users2 if u.get("id") == "u-test-persistence-100"), None)
assert fetched_user is not None, "New user not found in GET /api/system-settings response!"
print(f"   Server GET sync: PASS! ({fetched_user['name']})")

print("\n5. Cleaning up test user ...")
clean_users = [u for u in users2 if u.get("id") != "u-test-persistence-100"]
post_settings({"users": clean_users})
print("   Cleanup: PASS!")

print("\nALL USERS DATABASE PERSISTENCE TESTS PASSED 100%!")
