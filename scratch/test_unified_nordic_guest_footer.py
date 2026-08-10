import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for single unified Nordic Light guest footer ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "FRESH NORDIC LIGHT PUBLIC GUEST FOOTER" not in html, "Duplicate inline footer still present in MediaComponent!"
assert "bg-white/90 dark:bg-slate-900/95" in html, "Dual-theme Nordic Light & Dark background missing!"
assert "Sapanca Göl Kenarı’nın en özel balo salonlarında" in html, "Unified footer description missing!"
assert "Bilgi Al (+90 547 144 00 44)" in html, "CTA button text missing!"

print("   Source Code Verification: PASS (Single unified footer!)")

print("\n2. Testing HTTP GET /medya/RES-2026-3791 ...")
req = urllib.request.Request(f"{SERVER_URL}/medya/RES-2026-3791")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nUNIFIED NORDIC GUEST FOOTER TESTS PASSED 100%!")
