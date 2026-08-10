import urllib.request
import json

SERVER_URL = "http://localhost:8001"

def get_settings():
    req = urllib.request.Request(f"{SERVER_URL}/api/system-settings")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

print("1. Testing GET /api/system-settings after wipe ...")
data = get_settings()

res = data.get("reservations", [])
drafts = data.get("draftReservations", [])

print(f"   Reservations count: {len(res)}")
print(f"   Drafts count: {len(drafts)}")

assert len(res) == 0, f"Expected 0 reservations, got {len(res)}"
assert len(drafts) == 0, f"Expected 0 drafts, got {len(drafts)}"

print("\n2. Verifying disk files ...")
with open("scratch/db_reservations.json", "r", encoding="utf-8") as f:
    assert json.load(f) == []

with open("scratch/db_draft_reservations.json", "r", encoding="utf-8") as f:
    assert json.load(f) == []

print("\nALL WIPE AND REFRESH TESTS PASSED 100%!")
