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

print("1. Checking current DB state ...")
data1 = get_settings()
res_before = len(data1.get("reservations", []))
drafts_before = len(data1.get("draftReservations", []))
print(f"   Reservations: {res_before}, Drafts: {drafts_before}")

print("\n2. Simulating auto-save of a new draft ...")
test_draft = {
    "id": "RES-DRAFT-TEST999",
    "refKey": "DRAFT_REF_TEST999",
    "status": "DRAFT",
    "isDraft": True,
    "customerInfo": {"name": "Taslak Test Müşterisi", "phone": "5551112233"},
    "formData": {"newCustName": "Taslak Test Müşterisi"}
}
current_drafts = data1.get("draftReservations", [])
post_settings({"draftReservations": [test_draft] + current_drafts})

print("\n3. Verifying DB state after draft auto-save ...")
data2 = get_settings()
res_after = len(data2.get("reservations", []))
drafts_after = len(data2.get("draftReservations", []))
print(f"   Reservations count: {res_after} (Expected: {res_before})")
print(f"   Drafts count: {drafts_after} (Expected: {drafts_before + 1})")

assert res_after == res_before, "CRITICAL BUG: Draft leaked into reservations list!"
assert drafts_after == drafts_before + 1, "Draft failed to save to draftReservations list!"
print("   DRAFT ISOLATION VERIFICATION: PASS 100%!")

print("\n4. Cleaning up test draft ...")
post_settings({"draftReservations": current_drafts})
data3 = get_settings()
print(f"   Cleaned Drafts count: {len(data3.get('draftReservations', []))}")

print("\nDRAFT ISOLATION TEST PASSED SUCCESSFULLY!")
