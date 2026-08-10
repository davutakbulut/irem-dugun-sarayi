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

print("1. Testing initial GET /api/system-settings ...")
data1 = get_settings()
print(f"   Current themeColor: {data1.get('themeColor')}")

print("\n2. Updating theme to 'luxury-dark' via POST ...")
status = post_settings({'themeColor': 'luxury-dark'})
assert status == 200, f"Expected 200 OK, got {status}"

data2 = get_settings()
print(f"   Updated themeColor: {data2.get('themeColor')}")
assert data2.get('themeColor') == 'luxury-dark', f"Theme update failed! Got {data2.get('themeColor')}"

print("\n3. Updating theme back to 'classic_gold' via POST ...")
status = post_settings({'themeColor': 'classic_gold'})
assert status == 200

data3 = get_settings()
print(f"   Reverted themeColor: {data3.get('themeColor')}")
assert data3.get('themeColor') == 'classic_gold', f"Theme revert failed! Got {data3.get('themeColor')}"

print("\n4. Verifying db_system_settings.json file health on disk ...")
with open('scratch/db_system_settings.json', 'r', encoding='utf-8') as f:
    disk_data = json.load(f)
assert disk_data.get('themeColor') == 'classic_gold'

print("\nALL THEME PERSISTENCE AND DB HEALTH TESTS PASSED 100%!")
