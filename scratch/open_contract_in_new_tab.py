import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

old_open = "const printWin = window.open('', '_blank', 'width=900,height=700');"
new_open = "const printWin = window.open('', '_blank');"

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_open in content:
        content = content.replace(old_open, new_open)
        with open(h_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated window.open in {h_file}")
    else:
        print(f"old_open not found in {h_file}")

print("All HTML files updated to open contract in a new tab!")
