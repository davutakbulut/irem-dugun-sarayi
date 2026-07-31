import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
code = scripts[0]
lines = code.split('\n')

sub = lines[1034:2612]

# Accurate JSX tag stack
tag_stack = []

tag_re = re.compile(r'<(/)?([A-Za-z0-9\._]+)([^>]*?)(/)?>')

for idx, line in enumerate(sub):
    line_num = 1035 + idx
    # Remove comments
    clean = re.sub(r'\{/\*.*?\*/\}', '', line)
    clean = re.sub(r'//.*', '', clean)
    
    for match in tag_re.finditer(clean):
        is_closing = bool(match.group(1))
        tag_name = match.group(2)
        is_self_closing = bool(match.group(4))
        
        if is_self_closing:
            continue
            
        if is_closing:
            if tag_stack:
                last_tag = tag_stack.pop()
                if last_tag['name'] != tag_name:
                    print(f"TAG MISMATCH line {line_num}: closed </{tag_name}>, but top of stack was <{last_tag['name']}> (opened at line {last_tag['line']})")
            else:
                print(f"EXTRA CLOSING TAG </{tag_name}> at line {line_num}: {line.strip()}")
        else:
            tag_stack.append({'name': tag_name, 'line': line_num, 'text': line.strip()})

print(f"\nUnclosed JSX tags remaining at end of component: {len(tag_stack)}")
for t in tag_stack:
    print(f"  <{t['name']}> opened at line {t['line']} -> {t['text'][:60]}")
