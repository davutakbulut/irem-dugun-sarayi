import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace residual emojis in user-facing JSX text
remaining_replacements = [
    ("📋", '<ThemeIcon icon="document" className="w-4 h-4 inline-block shrink-0" />'),
    ("💾", '<ThemeIcon icon="check" className="w-4 h-4 inline-block shrink-0" />'),
    ("📖", '<ThemeIcon icon="document" className="w-4 h-4 inline-block shrink-0" />'),
    ("🎴", '<ThemeIcon icon="media" className="w-4 h-4 inline-block shrink-0" />'),
    ("🎬", '<ThemeIcon icon="video" className="w-4 h-4 inline-block shrink-0" />'),
    ("💍", '<ThemeIcon icon="celebrate" className="w-4 h-4 inline-block shrink-0" />'),
    ("🍩", '<ThemeIcon icon="gift" className="w-4 h-4 inline-block shrink-0" />'),
    ("🍇", '<ThemeIcon icon="gift" className="w-4 h-4 inline-block shrink-0" />'),
    ("🥗", '<ThemeIcon icon="gift" className="w-4 h-4 inline-block shrink-0" />'),
    ("🥐", '<ThemeIcon icon="gift" className="w-4 h-4 inline-block shrink-0" />'),
    ("🥩", '<ThemeIcon icon="gift" className="w-4 h-4 inline-block shrink-0" />'),
    ("🎂", '<ThemeIcon icon="gift" className="w-4 h-4 inline-block shrink-0" />'),
    ("🏆", '<ThemeIcon icon="crown" className="w-4 h-4 inline-block shrink-0" />'),
    ("⚜️", '<ThemeIcon icon="crown" className="w-4 h-4 inline-block shrink-0" />'),
    ("⚜", '<ThemeIcon icon="crown" className="w-4 h-4 inline-block shrink-0" />'),
    ("🌊", '<ThemeIcon icon="leaf" className="w-4 h-4 inline-block shrink-0" />'),
    ("🍂", '<ThemeIcon icon="leaf" className="w-4 h-4 inline-block shrink-0" />'),
    ("🏗️", '<ThemeIcon icon="building" className="w-4 h-4 inline-block shrink-0" />'),
    ("💸", '<ThemeIcon icon="money" className="w-4 h-4 inline-block shrink-0" />'),
    ("💖", '<ThemeIcon icon="heart" className="w-4 h-4 inline-block shrink-0" />'),
    ("🔢", '<ThemeIcon icon="ruler" className="w-4 h-4 inline-block shrink-0" />')
]

lines = content.split('\n')
new_lines = []
in_emoji_map = False

for line in lines:
    if "const ThemeConceptEmojis = {" in line:
        in_emoji_map = True
    if in_emoji_map and "};" in line:
        in_emoji_map = False
        new_lines.append(line)
        continue
    if in_emoji_map or "console.log" in line or "console.warn" in line or "console.error" in line:
        new_lines.append(line)
        continue
        
    line_replaced = line
    for emoji, replacement in remaining_replacements:
        if emoji in line_replaced:
            line_replaced = line_replaced.replace(emoji, replacement)
    new_lines.append(line_replaced)

new_content = '\n'.join(new_lines)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Replaced all remaining residual emojis and synced yonetim.html and dist/index.html!")
