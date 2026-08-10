import urllib.request

print("1. Verifying index.html source code for Babel syntax error resolution ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert 'placeholder="<ThemeIcon' not in html, "Invalid placeholder syntax still present in index.html!"
print("   Babel Syntax Check: PASS!")

print("\n2. Testing HTTP GET / ...")
req = urllib.request.Request("http://localhost:8001/")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nALL SYNTAX ERROR DIAGNOSTIC TESTS PASSED 100%!")
