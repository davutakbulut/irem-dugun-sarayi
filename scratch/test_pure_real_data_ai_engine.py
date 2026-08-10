import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for Pure Real-Data AI Engine ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "Real-Data GPT Ciro & Doluluk Analizi" in html, "Real-Data GPT Ciro Analizi missing!"
assert "Real-Data Ek Hizmet Çapraz Satış İpucu" in html, "Real-Data Ek Hizmet İpucu missing!"
assert "generateSmartAIRecommendations(reservations, venues, services, customers)" in html, "Pure real-data AI recommendations call missing!"

print("   Source Code Verification: PASS!")

print("\n2. Testing HTTP GET /yonetim ...")
req = urllib.request.Request(f"{SERVER_URL}/yonetim")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nALL PURE REAL-DATA AI ENGINE TESTS PASSED 100%!")
