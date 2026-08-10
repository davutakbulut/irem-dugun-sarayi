import urllib.request
import re

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for phone number standardization ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "547 144 00 44" not in html, "Old phone number 547 144 00 44 still present in index.html!"
assert "(264) 582 00 00" not in html, "Old phone number (264) 582 00 00 still present in index.html!"
assert "547 144 00 54" in html, "New phone number +90 547 144 00 54 missing in index.html!"
assert "905471440054" in html, "New WhatsApp number 905471440054 missing in index.html!"

print("   Source Code Verification: PASS (All phone numbers standardized to +90 547 144 00 54!)")

print("\n2. Verifying backend API /api/public-settings phone number ...")
req = urllib.request.Request(f"{SERVER_URL}/api/public-settings")
with urllib.request.urlopen(req) as response:
    data = response.read().decode('utf-8')
    assert "547 144 00 54" in data or "905471440054" in data, "Backend public settings phone number not updated!"
    print("   Backend API Phone Verification: PASS!")

print("\nALL PHONE NUMBERS STANDARDIZATION TESTS PASSED 100%!")
