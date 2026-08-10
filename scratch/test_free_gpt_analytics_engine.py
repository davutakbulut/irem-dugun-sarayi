import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for Free GPT Analytics Engine integration ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "generateSmartAITips" in html, "generateSmartAITips function missing!"
assert "Free GPT-4o Analytics Engine Bağlı ✓" in html, "Free GPT engine badge missing!"
assert "Yapay Zeka Analizini Yenile" in html, "Refresh AI analysis button missing!"

print("   Source Code Verification: PASS!")

print("\n2. Testing HTTP GET /yonetim ...")
req = urllib.request.Request(f"{SERVER_URL}/yonetim")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nALL FREE GPT ANALYTICS ENGINE TESTS PASSED 100%!")
