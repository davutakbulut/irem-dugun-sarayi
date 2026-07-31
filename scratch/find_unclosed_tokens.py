import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

script_match = re.search(r'<script type="text/babel">(.*?)</script>', content, re.DOTALL)
if not script_match:
    print("No babel script found")
    exit(1)

code = script_match.group(1)

# We want to parse code and ignore strings ('...', "...", `...`), single-line comments //..., and multi-line comments /*...*/
stack = []
i = 0
n = len(code)

line = 1
col = 1

while i < n:
    ch = code[i]
    
    # Handle newline tracking
    if ch == '\n':
        line += 1
        col = 1
        i += 1
        continue
    
    # Handle single line comment
    if ch == '/' and i + 1 < n and code[i+1] == '/':
        while i < n and code[i] != '\n':
            i += 1
        continue

    # Handle multi-line comment
    if ch == '/' and i + 1 < n and code[i+1] == '*':
        i += 2
        while i + 1 < n and not (code[i] == '*' and code[i+1] == '/'):
            if code[i] == '\n':
                line += 1
                col = 1
            i += 1
        i += 2
        continue

    # Handle strings ('', "", ``)
    if ch in ('"', "'", '`'):
        quote = ch
        start_line, start_col = line, col
        i += 1
        col += 1
        while i < n:
            c = code[i]
            if c == '\n':
                line += 1
                col = 1
            else:
                col += 1
            
            if c == '\\':
                i += 2
                col += 1
                continue
            if c == quote:
                i += 1
                break
            i += 1
        continue

    # Check brackets
    if ch in '({[':
        stack.append((ch, line, col))
    elif ch in ')}]' :
        if not stack:
            print(f"EXTRA CLOSING '{ch}' at line {line}:{col}")
        else:
            top_ch, top_line, top_col = stack[-1]
            match_map = {'(': ')', '{': '}', '[': ']'}
            if match_map[top_ch] == ch:
                stack.pop()
            else:
                print(f"MISMATCHED '{ch}' at line {line}:{col}, expected '{match_map[top_ch]}' for '{top_ch}' opened at line {top_line}:{top_col}")
                stack.pop()

    i += 1
    col += 1

print(f"\nRemaining unclosed items on stack: {len(stack)}")
for item in stack:
    print(f"  Unclosed '{item[0]}' opened at line {item[1]}:{item[2]}")
