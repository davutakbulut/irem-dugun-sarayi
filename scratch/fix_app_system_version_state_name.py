import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_code = "systemVersion={systemVersionState || systemSettings?.systemVersion || 'v1.4.59'}"
new_code = "systemVersion={systemVersion || systemSettings?.systemVersion || 'v1.4.60'}"

if old_code in html:
    html = html.replace(old_code, new_code)
    print("Fixed systemVersionState to systemVersion in index.html successfully!")
else:
    print("Could not find old_code in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html systemVersion variable name fix successfully!")
