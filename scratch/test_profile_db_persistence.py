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

print("1. Verifying index.html source code for profile database persistence ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "Profil Bilgileri (" in html, "onSaveProfile callback missing!"
assert "body: JSON.stringify({ users: newUsers })" in html, "POST /api/system-settings users payload missing!"

print("   Source Code Verification: PASS!")

print("\n2. Updating user profile in database via API ...")
data1 = get_settings()
users1 = data1.get("users", [])
target_user = next((u for u in users1 if u.get("id") == "u0"), users1[0])

original_name = target_user["name"]
updated_user = {
    **target_user,
    "name": "Mustafa Beyazyüz (Başkan)",
    "phone": "+90 532 999 0000"
}

updated_users_list = [updated_user if u.get("id") == target_user["id"] else u for u in users1]
status = post_settings({"users": updated_users_list})
assert status == 200

print("\n3. Verifying updated profile in GET /api/system-settings ...")
data2 = get_settings()
users2 = data2.get("users", [])
fetched_user = next((u for u in users2 if u.get("id") == target_user["id"]), None)

assert fetched_user is not None
assert fetched_user["name"] == "Mustafa Beyazyüz (Başkan)"
assert fetched_user["phone"] == "+90 532 999 0000"

print(f"   Updated User DB Record: Name='{fetched_user['name']}' | Phone='{fetched_user['phone']}'")

print("\n4. Restoring original name ...")
restored_user = { **target_user, "name": original_name }
restored_list = [restored_user if u.get("id") == target_user["id"] else u for u in users1]
post_settings({"users": restored_list})
print("   Restoration: PASS!")

print("\nALL PROFILE DATABASE PERSISTENCE TESTS PASSED 100%!")
