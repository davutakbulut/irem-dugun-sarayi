import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = "        </footer>\n\n          {/* FORGOT PASSWORD MODAL */}"
end_marker = "    function HallsPage({ navigateTo }) {"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

print(f"start_idx: {start_idx}, end_idx: {end_idx}")

if start_idx != -1 and end_idx != -1:
    new_code = content[:start_idx + len("        </footer>")] + "\n\n" + content[end_idx:]
    content = new_code
    print("Successfully removed dangling forgot password modal after PublicFooter!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
