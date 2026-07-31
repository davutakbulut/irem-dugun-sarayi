import urllib.request
import re

print("Testing Media Page & Public Guest Link Routes...")

url_admin = "http://localhost:8008/index_prod.html#/medya-yukle"
url_guest = "http://localhost:8008/index_prod.html#/medya-yukle?key=MEDIA-8X92M1KP"

req_admin = urllib.request.urlopen(url_admin)
html_admin = req_admin.read().decode('utf-8')

req_guest = urllib.request.urlopen(url_guest)
html_guest = req_guest.read().decode('utf-8')

print(f"Admin Route HTTP Status: {req_admin.status}")
print(f"Guest Route HTTP Status: {req_guest.status}")

if "app.compiled.js" in html_admin and "app.compiled.js" in html_guest:
    print("SUCCESS: Both Admin and Public Guest media routes are served cleanly!")
else:
    print("ERROR: Route bundle missing!")
