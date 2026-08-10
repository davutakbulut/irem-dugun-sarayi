import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for mobile scroll indicator centering ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "left-0 right-0 z-20" in html, "Full width absolute positioning missing!"
assert "flex flex-col items-center justify-center text-center" in html, "Flex center alignment missing!"
assert "tracking-[0.25em]" in html, "Tracking letter-spacing missing!"

print("   Source Code Verification: PASS 100%!")

print("\n2. Testing HTTP GET / ...")
req = urllib.request.Request(f"{SERVER_URL}/")
with urllib.request.urlopen(req) as resp:
    assert resp.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nMOBILE SCROLL INDICATOR CENTERING TESTS PASSED 100%!")
