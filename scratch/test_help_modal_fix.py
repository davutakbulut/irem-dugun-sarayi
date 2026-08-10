import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for showHelpModal state declaration ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "const [showHelpModal, setShowHelpModal] = useState(false);" in html, "showHelpModal state declaration missing!"

print("   Source Code Verification: PASS!")

print("\n2. Testing HTTP GET /giris ...")
req = urllib.request.Request(f"{SERVER_URL}/giris")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nALL HELP MODAL FIX TESTS PASSED 100%!")
