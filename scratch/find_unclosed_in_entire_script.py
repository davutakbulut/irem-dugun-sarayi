import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
if not scripts:
    print("No script tag found!")
    exit()

code = scripts[0]
lines = code.split('\n')

open_braces = []

for idx, line in enumerate(lines):
    line_num = idx + 1
    # Strip comments
    clean = re.sub(r'//.*', '', line)
    
    # Process characters carefully, ignoring strings inside "" or ''
    in_single = False
    in_double = False
    in_template = False
    
    i = 0
    while i < len(clean):
        ch = clean[i]
        
        if ch == "'" and not in_double and not in_template:
            in_single = not in_single
        elif ch == '"' and not in_single and not in_template:
            in_double = not in_double
        elif ch == '`' and not in_single and not in_double:
            in_template = not in_template
        elif not in_single and not in_double and not in_template:
            if ch == '{':
                open_braces.append((line_num, line.strip()))
            elif ch == '}':
                if open_braces:
                    open_braces.pop()
                else:
                    print(f"Extra closing brace '}}' at line {line_num}: {line.strip()}")
        i += 1

print(f"\nUnclosed braces count in ENTIRE script: {len(open_braces)}")
for line_num, text in open_braces:
    print(f"  Line {line_num}: {text[:70]}")
