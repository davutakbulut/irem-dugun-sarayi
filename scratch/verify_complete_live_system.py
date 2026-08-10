import urllib.request
import json
import os
import re

SERVER_URL = "http://localhost:8001"

print("1. Testing GET /api/system-settings for all database entities ...")
req = urllib.request.Request(f"{SERVER_URL}/api/system-settings")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    data = json.loads(response.read().decode())

entities = ["venues", "services", "campaigns", "customers", "reservations", "expenses", "users"]
for entity in entities:
    count = len(data.get(entity, []))
    print(f"   - Database entity '{entity}': {count} live items loaded from server DB.")
    assert count > 0, f"Entity {entity} is empty!"

print("\n2. Checking physical JSON database files on disk ...")
for entity in entities:
    filepath = os.path.join("scratch", f"db_{entity}.json")
    assert os.path.exists(filepath), f"File {filepath} missing!"
    with open(filepath, "r", encoding="utf-8") as f:
        items = json.load(f)
        assert len(items) > 0, f"Disk file {filepath} is empty!"

print("   Physical DB File Check: ALL PASS!")

print("\n3. Testing HTTP 200 OK across all primary routes ...")
routes = [
    "/",
    "/yonetim/dugun-salonlari",
    "/yonetim/yeni-rezervasyon",
    "/yonetim/rezervasyonlar",
    "/yonetim/finans",
    "/yonetim/musteriler",
    "/yonetim/kullanicilar",
    "/giris"
]

for route in routes:
    r = urllib.request.Request(f"{SERVER_URL}{route}")
    with urllib.request.urlopen(r) as resp:
        assert resp.status == 200, f"Route {route} returned status {resp.status}"
        print(f"   Route '{route}': 200 OK")

print("\nALL LIVE PRODUCTION SYSTEM AUDIT TESTS PASSED 100%!")
