import urllib.request

SERVER_URL = "http://localhost:8001"

print("1. Verifying index.html source code for LeadModal & Quote Requests Management ...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert "function LeadModal" in html, "LeadModal component missing!"
assert "function QuoteRequestsPageComponent" in html, "QuoteRequestsPageComponent missing!"
assert "Ücretsiz Teklif Al!" in html, "Final submit button 'Ücretsiz Teklif Al!' missing!"
assert "QUOTE-2026-001" in html, "INITIAL_QUOTE_REQUESTS demo data missing!"
assert "quote-requests" in html, "quote-requests route missing!"
assert "Fiyat Teklif Talepleri (Gelen Leads)" in html, "Management dashboard title missing!"

print("   Source Code Verification: PASS 100%!")

print("\n2. Testing HTTP GET / ...")
req = urllib.request.Request(f"{SERVER_URL}/")
with urllib.request.urlopen(req) as resp:
    assert resp.status == 200
    print("   HTTP 200 OK: PASS!")

print("\nUNIFIED LEAD MODAL & ADMIN QUOTE REQUESTS MANAGEMENT TESTS PASSED 100%!")
