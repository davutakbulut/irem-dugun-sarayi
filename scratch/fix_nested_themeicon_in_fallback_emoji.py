import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all occurrences of fallbackEmoji="<ThemeIcon..." or fallbackEmoji='<ThemeIcon...' with fallbackEmoji=""
fixed_content = re.sub(r'fallbackEmoji=["\']<ThemeIcon[^>]*/>["\']', 'fallbackEmoji=""', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("Cleaned up all nested <ThemeIcon> tags inside fallbackEmoji attributes!")
