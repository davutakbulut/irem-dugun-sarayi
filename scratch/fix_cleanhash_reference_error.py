with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

bad_hash_check = "} else if (cleanHash.startsWith('medya/') || cleanHash.startsWith('m/')) {"
good_hash_check = "} else if (slug.startsWith('medya/') || slug.startsWith('m/')) {"

if bad_hash_check in html:
    html = html.replace(bad_hash_check, good_hash_check)
    print("Fixed cleanHash ReferenceError typo in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
