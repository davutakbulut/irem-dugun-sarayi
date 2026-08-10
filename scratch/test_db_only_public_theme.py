import urllib.request
import json
import os

SERVER_URL = "http://localhost:8001"

print("1. Verifying db_public_settings.json ...")
db_pub_path = "scratch/db_public_settings.json"
assert os.path.exists(db_pub_path), "db_public_settings.json missing!"

with open(db_pub_path, "r", encoding="utf-8") as f:
    data = json.load(f)

assert data.get("publicTheme") == "dark-gold", f"Expected dark-gold publicTheme in DB, got: {data.get('publicTheme')}"
print("   db_public_settings.json Verification: PASS!")

print("\n2. Verifying index.html source code for pure database public settings ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "setPublicTheme('sapphire-dark')" not in html, "Alternative theme sapphire-dark still present in index.html!"
assert "setPublicTheme('rose-romantic')" not in html, "Alternative theme rose-romantic still present in index.html!"
assert "setPublicTheme('cream-light')" not in html, "Alternative theme cream-light still present in index.html!"
assert "fetchPublicSettingsFromDB" in html, "Database fetch logic missing from index.html!"

print("   Source Code Verification: PASS!")

print("\n3. Testing GET & POST /api/public-settings endpoint ...")
req = urllib.request.Request(f"{SERVER_URL}/api/public-settings")
with urllib.request.urlopen(req) as resp:
    assert resp.status == 200
    res_data = json.loads(resp.read().decode("utf-8"))
    assert res_data.get("publicTheme") == "dark-gold"
    print("   GET /api/public-settings: PASS!")

post_payload = json.dumps({
    "publicTheme": "dark-gold",
    "heroBadgeText": "✨ Sapanca Göl Kenarı Lüks Balo Tesisleri",
    "heroTitle": "Hayalinizdeki Düğün İrem Düğün Sarayı'nda Unutulmaz Oluyor",
    "heroSubtitle": "Canlı veritabanı entegreli saray organizasyonları"
}).encode("utf-8")

post_req = urllib.request.Request(f"{SERVER_URL}/api/public-settings", data=post_payload, headers={"Content-Type": "application/json"}, method="POST")
with urllib.request.urlopen(post_req) as post_resp:
    assert post_resp.status == 200
    print("   POST /api/public-settings: PASS!")

with open(db_pub_path, "r", encoding="utf-8") as f:
    updated_data = json.load(f)
assert updated_data.get("heroBadgeText") == "✨ Sapanca Göl Kenarı Lüks Balo Tesisleri"
print("   Database File Mutation Verification: PASS!")

print("\nPURE DATABASE PUBLIC THEME & SETTINGS TESTS PASSED 100%!")
