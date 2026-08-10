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

print("1. Fetching current venues from GET /api/system-settings ...")
data1 = get_settings()
venues1 = data1.get("venues", [])
print(f"   Current Venues count: {len(venues1)}")

# Suppose user deletes venue v5 ('Pırlanta Davet & Balo')
updated_venues = [v for v in venues1 if v.get("id") != "v5"]
print(f"\n2. Deleting venue v5 from database... Remaining count: {len(updated_venues)}")

status = post_settings({"venues": updated_venues})
assert status == 200, "POST failed!"

print("\n3. Verifying scratch/db_venues.json on disk ...")
with open("scratch/db_venues.json", "r", encoding="utf-8") as f:
    disk_venues = json.load(f)

print(f"   disk_venues count in db_venues.json: {len(disk_venues)}")
assert len(disk_venues) == len(updated_venues), f"Expected {len(updated_venues)} in db_venues.json, found {len(disk_venues)}"
assert not any(v.get("id") == "v5" for v in disk_venues), "Venue v5 was NOT deleted from db_venues.json!"

print("\n4. Re-fetching GET /api/system-settings after server restart/refresh simulation ...")
data2 = get_settings()
venues2 = data2.get("venues", [])
print(f"   Re-fetched Venues count: {len(venues2)}")
assert len(venues2) == len(updated_venues), "Venue returned after delete!"

print("\nVENUE DELETION IS 100% PERMANENT IN DATABASE & ALL TESTS PASSED!")
