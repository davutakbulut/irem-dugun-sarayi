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

print("1. Initial state check ...")
data0 = get_settings()
print(f"   Drafts count before: {len(data0.get('draftReservations', []))}")

print("\n2. Device A opens 'Yeni Rezervasyon' and triggers autoSave ...")
draft_device_a = {
    "id": "RES-DRAFT-DEV-A-1234",
    "refKey": "REF_DEV_A_1234",
    "status": "DRAFT",
    "isDraft": True,
    "completionPercentage": 25,
    "customerInfo": {
        "name": "Cihaz A - Yeni Taslak Müşterisi",
        "phone": "5320000000",
        "venueName": "Salon Seçilmedi",
        "date": "2026-08-25"
    },
    "formData": {
        "newCustName": "Cihaz A - Yeni Taslak Müşterisi"
    }
}
post_settings({"draftReservations": [draft_device_a]})

print("\n3. Device B refreshes page (GET /api/system-settings) ...")
data_device_b = get_settings()
drafts_b = data_device_b.get("draftReservations", [])
print(f"   Device B received {len(drafts_b)} draft(s).")

found = False
for d in drafts_b:
    if d.get("refKey") == "REF_DEV_A_1234":
        found = True
        print(f"   Found draft from Device A: ID={d.get('id')}, Name={d.get('customerInfo', {}).get('name')}")

assert found, "CROSS-DEVICE DRAFT SYNC FAILED: Device B did not receive Device A draft!"
print("   CROSS-DEVICE DRAFT SYNC: PASS 100%!")

print("\n4. Cleaning up test draft ...")
post_settings({"draftReservations": []})
data_clean = get_settings()
print(f"   Cleaned Drafts count: {len(data_clean.get('draftReservations', []))}")

print("\nCROSS DEVICE DRAFT SYNC TEST COMPLETED SUCCESSFULLY!")
