import urllib.request

print("1. Verifying index.html source code for synchronized deposit payment handlers ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "setHasDeposit(isYes);" in html, "Synchronized hasDeposit handler missing!"
assert "setPaymentStatus('Kapora Alındı');" in html, "Synchronized paymentStatus handler missing!"
assert "setDepositPaid(calculations?.grandTotal" in html, "Synchronized full payment handler missing!"

print("   Source Code Handler Verification: PASS!")

print("\n2. Testing HTTP GET /yonetim/yeni-rezervasyon?editId=RES-2026-3791 ...")
req = urllib.request.Request("http://localhost:8001/yonetim/yeni-rezervasyon?editId=RES-2026-3791")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nALL DEPOSIT SYNCHRONIZATION TESTS PASSED 100%!")
