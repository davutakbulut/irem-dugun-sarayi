import subprocess
import re

with open('src/pages/ReservationsListPage.jsx', 'r', encoding='utf-8') as f:
    res_jsx = f.read()

lines = res_jsx.split('\n')

# Table view is lines 466 to 568
table_lines = lines[465:568]

stack = []
tag_re = re.compile(r'</?([a-zA-Z0-9]+)[^>]*?>')

for idx, line in enumerate(table_lines):
    line_num = 466 + idx
    clean = re.sub(r'\{/\*.*?\*/\}', '', line)
    clean = re.sub(r'//.*', '', clean)
    
    for match in tag_re.finditer(clean):
        full_tag = match.group(0)
        tag_name = match.group(1)
        
        if full_tag.endswith('/>'):
            continue
            
        if full_tag.startswith('</'):
            if not stack:
                print(f"Table View EXTRA CLOSING </{tag_name}> at line {line_num}: {line.strip()}")
            else:
                top = stack.pop()
                if top['name'] != tag_name:
                    print(f"Table View MISMATCH line {line_num}: closed </{tag_name}>, expected </{top['name']}> (opened at line {top['line']})")
        else:
            stack.append({'name': tag_name, 'line': line_num, 'text': line.strip()})

print(f"\nTable View Stack size at end: {len(stack)}")
for t in stack:
    print(f"  <{t['name']}> opened at line {t['line']} -> {t['text'][:60]}")
