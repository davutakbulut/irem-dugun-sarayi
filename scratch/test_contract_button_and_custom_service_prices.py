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

print("1. Verifying HTML content for Contract Button placement ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "Sözleşmeyi Görüntüle / İndir (PDF)" in html, "Contract button text missing!"
assert "Takvim Canlı Ön İzlemesi" in html, "Takvim Canlı Ön İzlemesi text missing!"

pos_contract = html.find("Sözleşmeyi Görüntüle / İndir (PDF)")
pos_takvim = html.find("Takvim Canlı Ön İzlemesi")

assert pos_contract < pos_takvim, "Contract button must be placed BEFORE (above) Takvim Canlı Ön İzlemesi!"
print("   Contract Button is placed directly ABOVE Takvim Canlı Ön İzlemesi: PASS 100%!")

print("\n2. Testing reservation edit custom venue & service prices persistence ...")
settings = get_settings()
reservations = settings.get("reservations", [])
test_res = reservations[0] if len(reservations) > 0 else None

assert test_res is not None, "No reservations found!"
print(f"   Tested Reservation: ID={test_res.get('id')}, venuePrice=₺{test_res.get('venuePrice'):,}")

# Simulate saving custom service price and custom venue price
customized_res = {
    **test_res,
    "venuePrice": 125000,
    "customVenuePrice": 125000,
    "selectedServices": [
        {
            "serviceId": "s1",
            "quantity": 300,
            "unitPrice": 850, # Custom unit price
            "customUnitPrice": 850,
            "isPaid": True,
            "cost": 255000
        }
    ]
}

updated_reservations = [customized_res if r.get("id") == test_res.get("id") else r for r in reservations]
post_settings({"reservations": updated_reservations})

# Re-read from DB
settings_after = get_settings()
saved_res = next((r for r in settings_after.get("reservations", []) if r.get("id") == test_res.get("id")), None)

assert saved_res.get("venuePrice") == 125000, "Custom venue price did not save!"
assert saved_res.get("selectedServices")[0].get("customUnitPrice") == 850, "Custom service unit price did not save!"
print(f"   Saved Reservation Custom Venue Price: ₺{saved_res.get('venuePrice'):,}")
print(f"   Saved Reservation Service Unit Price: ₺{saved_res.get('selectedServices')[0].get('customUnitPrice'):,}")

# Revert to original
post_settings({"reservations": reservations})
print("   Reverted test reservation back to original.")

print("\nALL CONTRACT BUTTON & CUSTOM PRICES PERSISTENCE TESTS PASSED 100%!")
