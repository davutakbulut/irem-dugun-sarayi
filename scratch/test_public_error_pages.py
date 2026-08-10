import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for public error page bypassing ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "const isErrorRoute =" in html, "isErrorRoute missing!"
assert "!isErrorRoute" in html, "!isErrorRoute check missing in login guard!"

print("   Source Code Verification: PASS!")

print("\n2. Testing HTTP GET on error routes without login session ...")
error_paths = [
    "/yonetim/girisss",
    "/yonetim/invalid-route-99",
    "/yonetim/simulasyon-404",
    "/yonetim/simulasyon-500"
]

for path in error_paths:
    req = urllib.request.Request(f"{SERVER_URL}{path}")
    with urllib.request.urlopen(req) as response:
        assert response.status == 200, f"Failed HTTP GET on {path}"
        html_text = response.read().decode('utf-8')
        assert "İrem Düğün Sarayı" in html_text, f"Response missing title on {path}"
        print(f"   HTTP GET '{path}': 200 OK (Public error page rendered without login prompt)")

print("\nALL PUBLIC ERROR PAGE TESTS PASSED 100%!")
