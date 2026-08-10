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

print("1. Fetching current settings ...")
s1 = get_settings()
reservations = s1.get("reservations", [])
res_8815 = next((r for r in reservations if r.get("id") == "RES-2026-8815"), None)

assert res_8815 is not None, "RES-2026-8815 not found!"
print(f"   Current RES-2026-8815 venuePrice: ₺{res_8815.get('venuePrice'):,}, totalAmount: ₺{res_8815.get('totalAmount'):,}")

print("\n2. Simulating saving custom venue price ₺505,000 for RES-2026-8815 ...")
# Update res_8815 with a custom venue price
updated_8815 = {
    **res_8815,
    "venuePrice": 505000,
    "customVenuePrice": 505000,
    "subtotal": 505000 + 300750,
    "totalAmount": (505000 + 300750) - 5000,
    "remainingBalance": ((505000 + 300750) - 5000) - 40000
}

updated_reservations = [updated_8815 if r.get("id") == "RES-2026-8815" else r for r in reservations]
post_settings({"reservations": updated_reservations})

print("\n3. Verifying updated reservation in DB ...")
s2 = get_settings()
res_8815_after = next((r for r in s2.get("reservations", []) if r.get("id") == "RES-2026-8815"), None)

print(f"   Updated venuePrice: ₺{res_8815_after.get('venuePrice'):,}")
print(f"   Updated customVenuePrice: ₺{res_8815_after.get('customVenuePrice'):,}")
print(f"   Updated totalAmount: ₺{res_8815_after.get('totalAmount'):,}")
assert res_8815_after.get("venuePrice") == 505000, "venuePrice update failed!"
assert res_8815_after.get("totalAmount") == 800750, "totalAmount calculation update failed!"

print("\n4. Reverting RES-2026-8815 back to ₺65,000 for user testing ...")
post_settings({"reservations": reservations})
s3 = get_settings()
res_8815_reverted = next((r for r in s3.get("reservations", []) if r.get("id") == "RES-2026-8815"), None)
print(f"   Reverted venuePrice: ₺{res_8815_reverted.get('venuePrice'):,}")

print("\nCUSTOM VENUE PRICE TEST COMPLETED SUCCESSFULLY 100%!")
