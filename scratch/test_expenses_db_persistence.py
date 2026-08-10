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

print("1. Testing initial GET /api/system-settings for expenses ...")
data1 = get_settings()
print(f"   Current expenses count: {len(data1.get('expenses', []))}")

print("\n2. POSTing new expense to server database ...")
new_exp = {
    "id": "exp-test-01",
    "title": "Jeneratör Bakımı & Mazot Alımı",
    "category": "Faturalar & Enerji",
    "type": "gider",
    "amount": 12500,
    "date": "2026-08-08",
    "status": "Ödendi"
}

status = post_settings({"expenses": [new_exp]})
assert status == 200

print("\n3. Verifying scratch/db_expenses.json on disk ...")
with open("scratch/db_expenses.json", "r", encoding="utf-8") as f:
    disk_exp = json.load(f)

assert len(disk_exp) == 1, f"Expected 1 expense in db_expenses.json, got {len(disk_exp)}"
assert disk_exp[0]["id"] == "exp-test-01"
print("   db_expenses.json disk sync: PASS!")

print("\n4. Re-fetching GET /api/system-settings ...")
data2 = get_settings()
exp2 = data2.get("expenses", [])
assert len(exp2) == 1
assert exp2[0]["title"] == "Jeneratör Bakımı & Mazot Alımı"
print("   Server GET sync: PASS!")

print("\n5. Testing wiping expenses to [] ...")
status = post_settings({"expenses": []})
assert status == 200

with open("scratch/db_expenses.json", "r", encoding="utf-8") as f:
    assert json.load(f) == []

data3 = get_settings()
assert data3.get("expenses") == []
print("   Wiping expenses persistence: PASS!")

print("\nALL EXPENSES DATABASE PERSISTENCE TESTS PASSED 100%!")
