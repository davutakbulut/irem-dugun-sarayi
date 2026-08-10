import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for empty initial login inputs ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "useState('mustafa@iremdugunsarayi.com');" not in html, "Demo initial email state still present!"
assert "useState('Msytf2026');" not in html, "Demo initial password state still present!"
assert "const [emailInput, setEmailInput] = useState('');" in html, "Empty initial email state missing!"
assert "const [password, setPassword] = useState('');" in html, "Empty initial password state missing!"

print("   Source Code Verification: PASS!")

print("\n2. Testing HTTP GET /yonetim/giris ...")
req = urllib.request.Request(f"{SERVER_URL}/yonetim/giris")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nALL EMPTY LOGIN INPUT TESTS PASSED 100%!")
