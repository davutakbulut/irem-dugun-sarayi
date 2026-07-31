import urllib.request
import json
import re

def run_test(target_theme):
    print(f"\n--- TESTING CHANGE TO: '{target_theme}' ---")
    post_payload = json.dumps({"themeColor": target_theme, "updatedAt": "2026-08-01T01:44:00Z"}).encode('utf-8')
    post_req = urllib.request.Request('http://127.0.0.1:8008/api/system-settings', data=post_payload, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
    
    post_resp = urllib.request.urlopen(post_req)
    print(f"1. Admin Saved Theme '{target_theme}' -> Server DB Response: {post_resp.status}")
    
    # Simulate browser history clearing
    fresh_req = urllib.request.Request('http://127.0.0.1:8008/', headers={'User-Agent': 'Mozilla/5.0'})
    html_content = urllib.request.urlopen(fresh_req).read().decode('utf-8')
    
    match = re.search(r'data-ui-theme="([^"]+)"', html_content)
    served_theme = match.group(1) if match else "DEFAULT / UNSET"
    print(f"2. Cleared Browser History -> Server Served HTML Attribute: data-ui-theme=\"{served_theme}\"")
    
    if served_theme == target_theme:
        print(f"✅ VERIFIED PERFECT: '{target_theme}' is 100% persistent in backend DB and served on initial paint!")
    else:
        print(f"❌ MISMATCH: expected '{target_theme}', got '{served_theme}'")

run_test("nordic-light")
run_test("emerald-royal")
run_test("nordic-light")
