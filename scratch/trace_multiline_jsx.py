import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
code = scripts[0]
lines = code.split('\n')

sub_code = '\n'.join(lines[1034:2612])

# Clean out strings and JS comments, but preserve line breaks
def clean_jsx(text):
    # Strip comments
    text = re.sub(r'\{/\*.*?\*/\}', '', text, flags=re.DOTALL)
    text = re.sub(r'//.*', '', text)
    return text

cleaned = clean_jsx(sub_code)

# Find JSX tags
# Match <tag...>, </tag>, or <tag.../>
tag_pattern = re.compile(r'</?([A-Za-z0-9\._]+)(?:[^>"\']|"[^"]*"|\'[^\']*\')*?>')

stack = []

for match in tag_pattern.finditer(cleaned):
    tag = match.group(0)
    name = match.group(1)
    
    # Calculate line number
    pos = match.start()
    line_num = 1035 + cleaned[:pos].count('\n')
    
    if tag.endswith('/>') or tag.startswith('<?'):
        continue
        
    if tag.startswith('</'):
        if not stack:
            print(f"EXTRA CLOSING </{name}> at line {line_num}")
        else:
            top = stack.pop()
            if top['name'] != name:
                print(f"MISMATCH at line {line_num}: closed </{name}>, expected </{top['name']}> (opened at line {top['line']})")
    else:
        stack.append({'name': name, 'line': line_num, 'text': tag[:40]})

print(f"\nUnclosed multiline tags: {len(stack)}")
for t in stack:
    print(f"  <{t['name']}> opened at line {t['line']} -> {t['text']}")
