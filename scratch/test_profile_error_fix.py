import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for ProfileComponent & UserModalComponent error message fix ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

profile_pos = html.find("function ProfileComponent")
assert profile_pos != -1, "ProfileComponent missing!"

profile_code = html[profile_pos:profile_pos + 4000]
assert "if (errorMessage) setErrorMessage('')" not in profile_code, "errorMessage call still found inside ProfileComponent!"

modal_pos = html.find("function UserModalComponent")
assert modal_pos != -1, "UserModalComponent missing!"

modal_code = html[modal_pos:modal_pos + 2000]
assert "if (errorMessage) setErrorMessage('')" not in modal_code, "errorMessage call still found inside UserModalComponent!"

print("   Source Code Verification: PASS!")

print("\n2. Testing HTTP GET /yonetim/profil ...")
req = urllib.request.Request(f"{SERVER_URL}/yonetim/profil")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nALL PROFILE ERROR FIX TESTS PASSED 100%!")
