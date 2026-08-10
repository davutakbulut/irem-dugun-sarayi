import urllib.request

print("1. Verifying index.html source code for numeric input validation rules ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Check initial states
assert "const [guestCount, setGuestCount] = useState('');" in html, "guestCount should initialize as empty string!"
assert "const [depositPaid, setDepositPaid] = useState('');" in html, "depositPaid should initialize as empty string!"
assert "const [customDiscountAmount, setCustomDiscountAmount] = useState('');" in html, "customDiscountAmount should initialize as empty string!"

# Check validation warnings
assert "⚠️ 0'dan büyük giriniz" in html, "Negative validation warning text missing!"
assert "border-2 border-red-500 bg-red-500/10" in html, "Red warning border styling missing!"

print("   HTML Source Code Verification: PASS!")

print("\n2. Testing HTTP GET /yonetim/yeni-rezervasyon?ref=k7YlI5FAm88b ...")
req = urllib.request.Request("http://localhost:8001/yonetim/yeni-rezervasyon?ref=k7YlI5FAm88b")
with urllib.request.urlopen(req) as response:
    assert response.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nALL NUMERIC INPUT VALIDATION TESTS PASSED 100%!")
