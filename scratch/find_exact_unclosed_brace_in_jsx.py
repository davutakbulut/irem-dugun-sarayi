import re

with open('src/pages/ReservationsListPage.jsx', 'r', encoding='utf-8') as f:
    res_jsx = f.read()

# Remove comments
clean_code = re.sub(r'\{/\*.*?\*/\}', '', res_jsx, flags=re.DOTALL)
clean_code = re.sub(r'//.*', '', clean_code)

lines = clean_code.split('\n')

stack = []

for idx, line in enumerate(lines):
    line_num = idx + 1
    
    # scan characters
    i = 0
    in_s = False
    in_d = False
    in_t = False
    
    while i < len(line):
        ch = line[i]
        
        if ch == "'" and not in_d and not in_t:
            in_s = not in_s
        elif ch == '"' and not in_s and not in_t:
            in_d = not in_d
        elif ch == '`' and not in_s and not in_d:
            in_t = not in_t
        elif not in_s and not in_d and not in_t:
            if ch == '{':
                stack.append((line_num, i+1, line.strip()))
            elif ch == '}':
                if stack:
                    stack.pop()
                else:
                    print(f"Extra '}}' at line {line_num}:{i+1} -> {line.strip()}")
        i += 1

print(f"\nUnclosed {{ count at end of file: {len(stack)}")
for line_num, col, text in stack:
    print(f"  Line {line_num}:{col} -> {text[:70]}")
