import urllib.request
import json

SERVER_URL = "http://localhost:8001"

def get_settings():
    req = urllib.request.Request(f"{SERVER_URL}/api/system-settings")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

print("1. Checking database services count from /api/system-settings ...")
data = get_settings()
services = data.get("services", [])

print(f"   Database Services count: {len(services)}")
assert len(services) == 9, f"Expected 9 services in DB, found {len(services)}"

print("\n2. Verifying HTML VenueModalComponent binding ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "allServices={services}" in html, "allServices={services} prop missing from VenueModalComponent!"
assert "defaultServicesList = [...(allServices || [])]" in html, "defaultServicesList dynamic database binding missing!"

print("   VenueModalComponent receives 100% database services: PASS!")
print("\nALL VENUE MODAL DATABASE SERVICES TESTS PASSED 100%!")
