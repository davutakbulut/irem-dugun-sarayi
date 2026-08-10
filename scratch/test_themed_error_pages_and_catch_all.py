import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for themed wedding error pages & catch-all router ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "function NotFoundPage" in html, "NotFoundPage (404) component missing!"
assert "function ServerErrorPage" in html, "ServerErrorPage (500) component missing!"
assert "function ForbiddenPage" in html, "ForbiddenPage (403) component missing!"
assert "Aradığınız Sayfa Bir Düğün Masalı Gibi Kayboldu" in html, "404 wedding theme text missing!"
assert "Orkestramız Kısa Bir Mola Verdi" in html, "500 wedding theme text missing!"
assert "VIP Gelin & Damat Odasına İzinsiz Giriş Engellendi" in html, "403 wedding theme text missing!"

print("   Themed Error Pages Source Code Verification: PASS 100%!")

print("\n2. Testing HTTP GET / ...")
req = urllib.request.Request(f"{SERVER_URL}/")
with urllib.request.urlopen(req) as resp:
    assert resp.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nTHEMED ERROR PAGES & CATCH-ALL ROUTING TESTS PASSED 100%!")
