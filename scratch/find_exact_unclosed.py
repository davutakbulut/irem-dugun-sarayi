import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
if not scripts:
    print("No script tag found!")
    exit()

code = scripts[0]
lines = code.split('\n')

# Check lines 1034 to 2612 (ReservationsListComponent)
sub_lines = lines[1034:2612]

# Let's count open vs close curly braces { and } line by line inside ReservationsListComponent
open_braces = []
for idx, line in enumerate(sub_lines):
    line_num = 1035 + idx
    # Remove strings
    clean = re.sub(r'".*?"', '""', line)
    clean = re.sub(r"'.*?'", "''", clean)
    clean = re.sub(r'`.*?`', '``', clean) # note: template literals might span multiple lines!
    clean = re.sub(r'//.*', '', clean)
    
    for ch in clean:
        if ch == '{':
            open_braces.append(line_num)
        elif ch == '}':
            if open_braces:
                open_braces.pop()
            else:
                print(f"Extra closing brace '}}' at line {line_num}: {line.strip()}")

print(f"Unclosed braces count: {len(open_braces)}")
for l in open_braces:
    print(f"  Unclosed '{{' at line {l}: {lines[l-1].strip()}")
