import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for Nordic Light fresh modal design ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "bg-white dark:bg-slate-900 border border-slate-200" in html, "Fresh Nordic white card container missing!"
assert "bg-amber-50/80 dark:bg-amber-500/10" in html, "Fresh Nordic warm info card missing!"
assert "bg-slate-50 dark:bg-slate-950 border border-slate-200" in html, "Fresh Nordic input field missing!"

print("   Source Code Verification: PASS!")

print("\n2. Testing HTTP GET /yonetim/giris ...")
req = urllib.request.Request(f"{SERVER_URL}/yonetim/giris")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nNORDIC LIGHT FRESH FORGOT PASSWORD MODAL TESTS PASSED 100%!")
