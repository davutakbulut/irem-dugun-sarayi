import urllib.request
import json
import time

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

print("=== STARTING FULL COMPREHENSIVE END-TO-END SYSTEM TEST ===")

# --- TEST 1: Initial DB fetch ---
print("\n[TEST 1] Testing Initial GET /api/system-settings ...")
data1 = get_settings()
print(f"   Venues count: {len(data1.get('venues', []))}")
print(f"   Services count: {len(data1.get('services', []))}")
print(f"   Customers count: {len(data1.get('customers', []))}")
print(f"   Reservations count: {len(data1.get('reservations', []))}")
print(f"   Draft Reservations count: {len(data1.get('draftReservations', []))}")

assert len(data1.get('venues', [])) > 0, "Venues should not be empty!"
assert len(data1.get('services', [])) > 0, "Services should not be empty!"

# --- TEST 2: Draft Creation ---
print("\n[TEST 2] Testing Draft Creation (Auto-save form payload) ...")
draft_item = {
    "id": "RES-DRAFT-TEST-99",
    "customerName": "Ayşe & Mehmet Test Draft",
    "venueId": "v1",
    "venueName": "Kraliyet Balo Salonu",
    "date": "2026-09-01",
    "guestCount": 500,
    "totalAmount": 50000,
    "status": "DRAFT",
    "createdAt": "2026-08-08T20:37:00.000Z"
}

status = post_settings({"draftReservations": [draft_item]})
assert status == 200, "Draft POST failed!"

data2 = get_settings()
drafts2 = data2.get("draftReservations", [])
print(f"   Drafts count after creation: {len(drafts2)}")
assert len(drafts2) == 1, f"Expected 1 draft, got {len(drafts2)}"
assert drafts2[0]["id"] == "RES-DRAFT-TEST-99", "Draft ID mismatch!"

with open("scratch/db_draft_reservations.json", "r", encoding="utf-8") as f:
    disk_drafts = json.load(f)
assert len(disk_drafts) == 1, "db_draft_reservations.json disk sync failed!"
print("   Draft Creation DB Persistence: PASS!")

# --- TEST 3: Finalize Draft -> Confirmed Reservation ---
print("\n[TEST 3] Testing Draft Finalization into Confirmed Reservation ...")
confirmed_item = {
    "id": "RES-2026-TEST-99",
    "customerName": "Ayşe & Mehmet Test Draft",
    "venueId": "v1",
    "venueName": "Kraliyet Balo Salonu",
    "date": "2026-09-01",
    "guestCount": 500,
    "totalAmount": 50000,
    "depositPaid": 15000,
    "paymentStatus": "Kapora Alındı",
    "createdAt": "2026-08-08T20:37:00.000Z"
}

# Post confirmed reservation AND clear drafts
status = post_settings({"reservations": [confirmed_item], "draftReservations": []})
assert status == 200, "Confirmed Reservation POST failed!"

data3 = get_settings()
res3 = data3.get("reservations", [])
drafts3 = data3.get("draftReservations", [])
print(f"   Confirmed Reservations count: {len(res3)}")
print(f"   Draft Reservations count: {len(drafts3)}")

assert len(res3) == 1, f"Expected 1 confirmed reservation, got {len(res3)}"
assert len(drafts3) == 0, f"Expected 0 drafts, got {len(drafts3)}"

with open("scratch/db_reservations.json", "r", encoding="utf-8") as f:
    disk_res = json.load(f)
assert len(disk_res) == 1, "db_reservations.json disk sync failed!"
print("   Draft Finalization & Isolation DB Persistence: PASS!")

# --- TEST 4: Edit Venue Price ---
print("\n[TEST 4] Testing Venue Custom Price Update ...")
updated_venues = data3.get("venues", [])
for v in updated_venues:
    if v["id"] == "v1":
        v["price"] = 125000

status = post_settings({"venues": updated_venues})
assert status == 200

data4 = get_settings()
v1_price = next(v["price"] for v in data4["venues"] if v["id"] == "v1")
print(f"   Updated v1 venue price: {v1_price:,} TL")
assert v1_price == 125000, "Venue price update failed!"

with open("scratch/db_venues.json", "r", encoding="utf-8") as f:
    disk_venues = json.load(f)
assert next(v["price"] for v in disk_venues if v["id"] == "v1") == 125000
print("   Venue Custom Price DB Persistence: PASS!")

# --- TEST 5: Clean Up Test Reservation ---
print("\n[TEST 5] Testing Clean Up (Wiping test reservation) ...")
status = post_settings({"reservations": []})
assert status == 200

data5 = get_settings()
assert len(data5.get("reservations", [])) == 0, "Clean up failed!"
with open("scratch/db_reservations.json", "r", encoding="utf-8") as f:
    assert json.load(f) == []
print("   Clean Up DB Persistence: PASS!")

print("\n=======================================================")
print("  ALL 5 COMPREHENSIVE END-TO-END DATABASE TESTS PASSED 100%!")
print("=======================================================")
