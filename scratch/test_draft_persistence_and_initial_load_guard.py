import urllib.request
import json

SERVER_URL = "http://localhost:8001"

def get_settings():
    req = urllib.request.Request(f"{SERVER_URL}/api/system-settings")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def post_settings(payload):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(f"{SERVER_URL}/api/system-settings", data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

print("1. Creating persistent test draft from Device A ...")
test_draft = {
    "id": "RES-DRAFT-PERSIST-999",
    "refKey": "REF_PERSIST_999",
    "status": "DRAFT",
    "isDraft": True,
    "completionPercentage": 50,
    "customerInfo": {
        "name": "Kalıcı Taslak Müşteri Testi",
        "phone": "5329998877",
        "venueName": "Yakut Panorama Salon",
        "date": "2026-08-30"
    },
    "formData": {
        "newCustName": "Kalıcı Taslak Müşteri Testi"
    }
}
post_settings({"draftReservations": [test_draft]})

print("2. Simulating Device B initial page load ...")
# Device B fetches system settings
b_data = get_settings()
b_drafts = b_data.get("draftReservations", [])
print(f"   Device B fetched {len(b_drafts)} draft(s) on initial load.")

found = any(d.get("refKey") == "REF_PERSIST_999" for d in b_drafts)
assert found, "FAIL: Persistent draft was lost on initial load!"
print("   Initial load returned persistent draft successfully.")

print("3. Verifying database file on disk directly ...")
with open("scratch/db_draft_reservations.json", "r", encoding="utf-8") as f:
    disk_drafts = json.load(f)

disk_found = any(d.get("refKey") == "REF_PERSIST_999" for d in disk_drafts)
assert disk_found, "FAIL: Draft was not persisted on disk!"
print("   Disk file db_draft_reservations.json contains persistent draft!")

print("4. Cleaning up test draft ...")
post_settings({"draftReservations": []})
print("   Cleanup done.")

print("\nDRAFT PERSISTENCE & INITIAL LOAD GUARD TEST PASSED 100%!")
