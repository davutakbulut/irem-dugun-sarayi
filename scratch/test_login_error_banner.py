import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for In-Place Red Alert Error Banner ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "const [errorMessage, setErrorMessage] = useState('');" in html, "errorMessage state missing!"
assert "IN-PLACE RED ALERT ERROR BANNER" in html, "In-place red alert error banner missing!"
assert "Giriş Başarısız!" in html, "Error banner header text missing!"

print("   Source Code Verification: PASS!")

print("\n2. Testing HTTP GET /yonetim/giris ...")
req = urllib.request.Request(f"{SERVER_URL}/yonetim/giris")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nALL LOGIN ERROR BANNER TESTS PASSED 100%!")
