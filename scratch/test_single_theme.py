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

def get_html():
    req = urllib.request.Request(f"{SERVER_URL}/yonetim")
    with urllib.request.urlopen(req) as response:
        return response.read().decode('utf-8')

print("1. Testing GET /api/system-settings ...")
data = get_settings()
print("   Current DB themeColor:", data.get("themeColor"))

print("\n2. Updating themeColor to 'apple' via POST /api/system-settings ...")
res_post = post_settings({"themeColor": "apple"})
print("   POST response:", res_post)

print("\n3. Verifying GET /api/system-settings after update ...")
data2 = get_settings()
print("   Updated DB themeColor:", data2.get("themeColor"))
assert data2.get("themeColor") == "apple", "Theme update failed!"

print("\n4. Verifying 0ms HTML injection from server ...")
html_str = get_html()
assert 'data-ui-theme="apple"' in html_str, "Server HTML injection failed!"
print("   HTML injection contains data-ui-theme=\"apple\": PASS!")

print("\n5. Restoring themeColor to 'nordic-light' ...")
post_settings({"themeColor": "nordic-light"})
data3 = get_settings()
print("   Restored DB themeColor:", data3.get("themeColor"))

print("\nALL SINGLE GLOBAL THEME TESTS PASSED 100% SUCCESS!")
