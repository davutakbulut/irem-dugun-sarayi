import urllib.request

print("1. Verifying index.html source code for nested ThemeIcon tag cleanup ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert 'fallbackEmoji="<ThemeIcon' not in html, "Nested <ThemeIcon> inside fallbackEmoji still exists!"
assert 'fallbackEmoji=\'<ThemeIcon' not in html, "Nested <ThemeIcon> inside fallbackEmoji still exists!"
print("   Source Code Syntax Verification: PASS!")

print("\n2. Testing HTTP GET / ...")
req = urllib.request.Request("http://localhost:8001/")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nALL NESTED THEMEICON SYNTAX TESTS PASSED 100%!")
