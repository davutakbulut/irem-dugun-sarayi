import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
code = scripts[0]
lines = code.split('\n')

portal_lines = lines[2142:2608] # Line 2143 to 2608

div_stack = []

for idx, line in enumerate(portal_lines):
    line_num = 2143 + idx
    # find <div> and </div>
    # clean comments
    clean = re.sub(r'\{/\*.*?\*/\}', '', line)
    clean = re.sub(r'//.*', '', clean)
    
    # scan for <div and </div
    for m in re.finditer(r'</?div[^>]*?>', clean):
        tag = m.group(0)
        if tag.endswith('/>'):
            continue
        if tag.startswith('</'):
            if div_stack:
                div_stack.pop()
            else:
                print(f"EXTRA </div> at line {line_num}: {line.strip()}")
        else:
            div_stack.append((line_num, line.strip()))

print(f"\nUnclosed <div> tags in portal: {len(div_stack)}")
for l, t in div_stack:
    print(f"  Line {l}: {t[:60]}")
