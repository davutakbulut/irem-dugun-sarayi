import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
code = scripts[0]
lines = code.split('\n')

# Lines 1034 to 2612 (ReservationsListComponent)
sub = lines[1034:2612]

# Let's track brace stack with exact line and position
stack = []

for idx, line in enumerate(sub):
    line_num = 1035 + idx
    # Remove string literals and comments
    clean = line
    # Remove single line comments
    clean = re.sub(r'//.*', '', clean)
    # Remove JSX comments {/* ... */}
    clean = re.sub(r'\{/\*.*?\*/\}', '', clean)
    
    # Simple character scanner
    in_str = None
    for col, ch in enumerate(clean):
        if in_str:
            if ch == in_str and (col == 0 or clean[col-1] != '\\'):
                in_str = None
        else:
            if ch in ('"', "'", '`'):
                in_str = ch
            elif ch == '{':
                stack.append((line_num, col+1, line.strip()))
            elif ch == '}':
                if stack:
                    stack.pop()
                else:
                    print(f"EXTRA '}}' at line {line_num}:{col+1} -> {line.strip()}")

print(f"Stack size at end of ReservationsListComponent: {len(stack)}")
for line_num, col, text in stack:
    print(f"  Unclosed '{{' at line {line_num}:{col} -> {text[:60]}")
