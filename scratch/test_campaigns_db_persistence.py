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

print("1. Verifying index.html source code for campaigns DB persistence ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "Kampanya (" in html and "Veritabanına Başarıyla Kaydedildi" in html, "handleSaveCampaign toast missing!"
assert "Kampanya Veritabanından Silindi" in html, "handleDeleteCampaign toast missing!"
assert "AI Önerisi Veritabanına Kaydedildi" in html, "handleConvertAiToCampaign toast missing!"

print("   Source Code Verification: PASS!")

print("\n2. Checking current GET /api/system-settings campaigns list ...")
data1 = get_settings()
c_list1 = data1.get("campaigns", [])
print(f"   Found {len(c_list1)} campaigns in db_campaigns.json: {[c.get('code') for c in c_list1]}")

assert any(c.get('code') == 'IREM2026' for c in c_list1), "IREM2026 missing from db_campaigns.json!"

print("\n3. Testing POST campaign addition to db_campaigns.json ...")
new_camp = {
    "id": "c-test-99",
    "code": "TESTSEZON26",
    "title": "Test Sezonluk Kampanya",
    "type": "percent",
    "value": 25,
    "description": "Test indirimi"
}

post_settings({"campaigns": [*c_list1, new_camp]})

data2 = get_settings()
c_list2 = data2.get("campaigns", [])
added_c = next((c for c in c_list2 if c.get("id") == "c-test-99"), None)
assert added_c is not None, "Test campaign not found in DB after POST!"
print(f"   Added Campaign DB Record: Code='{added_c['code']}' | Title='{added_c['title']}'")

print("\n4. Cleaning test campaign from db_campaigns.json ...")
clean_c_list = [c for c in c_list2 if c.get("id") != "c-test-99"]
post_settings({"campaigns": clean_c_list})

data3 = get_settings()
c_list3 = data3.get("campaigns", [])
assert not any(c.get("id") == "c-test-99" for c in c_list3)
print("   Cleaned Test Campaign: PASS!")

print("\nALL CAMPAIGNS DATABASE PERSISTENCE TESTS PASSED 100%!")
