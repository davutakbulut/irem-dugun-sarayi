import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for /yonetim/giris route configuration ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "'login': '/yonetim/giris'" in html, "TAB_TO_PATH['login'] is not /yonetim/giris!"
assert "'yonetim/giris': 'login'" in html, "PATH_TO_TAB['yonetim/giris'] missing!"
assert "/yonetim/giris" in html, "/yonetim/giris route missing!"

print("   Source Code Route Verification: PASS!")

print("\n2. Testing HTTP GET on all login URL variations ...")
login_urls = [
    "/yonetim/giris",
    "/yonetim/login",
    "/giris",
    "/login"
]

for path in login_urls:
    req = urllib.request.Request(f"{SERVER_URL}{path}")
    with urllib.request.urlopen(req) as response:
        assert response.status == 200, f"Failed HTTP GET on {path}"
        print(f"   HTTP GET '{path}': 200 OK")

print("\nALL YÖNETİM GİRİŞ ROUTE TESTS PASSED 100%!")
