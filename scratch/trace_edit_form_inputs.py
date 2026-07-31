import re

with open('src/pages/ReservationsListPage.jsx', 'r', encoding='utf-8') as f:
    res_jsx = f.read()

lines = res_jsx.split('\n')

# Edit form starts at line 1111 (editingRes && editForm && createPortal)
edit_lines = lines[1110:1580]

stack = []

for idx, line in enumerate(edit_lines):
    line_num = 1111 + idx
    # find tags
    clean = re.sub(r'\{/\*.*?\*/\}', '', line)
    clean = re.sub(r'//.*', '', clean)
    
    # match tags
    tag_re = re.compile(r'</?([a-zA-Z0-9]+)[^>]*?>')
    for m in tag_re.finditer(clean):
        full_tag = m.group(0)
        tag_name = m.group(1)
        
        if full_tag.endswith('/>'):
            continue
            
        if full_tag.startswith('</'):
            if not stack:
                print(f"Edit Form EXTRA CLOSING </{tag_name}> at line {line_num}: {line.strip()}")
            else:
                top = stack.pop()
                if top['name'] != tag_name:
                    print(f"Edit Form MISMATCH at line {line_num}: closed </{tag_name}>, expected </{top['name']}> (opened at line {top['line']})")
        else:
            stack.append({'name': tag_name, 'line': line_num, 'text': line.strip()})

print(f"\nEdit Form Unclosed Tags: {len(stack)}")
for t in stack:
    print(f"  <{t['name']}> opened at line {t['line']} -> {t['text'][:60]}")
