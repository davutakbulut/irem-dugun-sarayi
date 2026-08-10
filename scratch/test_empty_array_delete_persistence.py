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

print("1. Sending empty array [] for reservations via POST ...")
status = post_settings({"reservations": []})
assert status == 200, "POST failed!"

print("2. Verifying scratch/db_reservations.json on disk ...")
with open("scratch/db_reservations.json", "r", encoding="utf-8") as f:
    disk_data = json.load(f)

assert disk_data == [], f"Expected [], got {disk_data}"

print("3. Re-fetching GET /api/system-settings ...")
data = get_settings()
assert data.get("reservations") == [], f"Expected [], got {data.get('reservations')}"

print("ALL EMPTY ARRAY DELETE PERSISTENCE TESTS PASSED 100%!")
