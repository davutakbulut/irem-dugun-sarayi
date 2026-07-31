import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

script_match = re.search(r'<script type="text/babel">(.*?)</script>', content, re.DOTALL)
if not script_match:
    print("No babel script found")
    exit(1)

code = script_match.group(1)

# Full lexer / parser for JS + JSX brackets
stack = []
i = 0
n = len(code)

line = 1
col = 1

def advance():
    global i, line, col
    if i < n:
        if code[i] == '\n':
            line += 1
            col = 1
        else:
            col += 1
        i += 1

in_template_expr_stack = [] # tracks nested ${ } inside template literals

while i < n:
    ch = code[i]
    
    # 1. Single line comment
    if ch == '/' and i + 1 < n and code[i+1] == '/':
        while i < n and code[i] != '\n':
            advance()
        continue
        
    # 2. Multi line comment
    if ch == '/' and i + 1 < n and code[i+1] == '*':
        advance()
        advance()
        while i + 1 < n and not (code[i] == '*' and code[i+1] == '/'):
            advance()
        advance()
        advance()
        continue
        
    # 3. Single or Double quoted strings
    if ch in ('"', "'"):
        quote = ch
        start_l, start_c = line, col
        advance()
        while i < n:
            c = code[i]
            if c == '\\':
                advance()
                advance()
                continue
            if c == quote:
                advance()
                break
            advance()
        continue

    # 4. Template literals `...`
    if ch == '`':
        start_l, start_c = line, col
        advance()
        while i < n:
            c = code[i]
            if c == '\\':
                advance()
                advance()
                continue
            if c == '`':
                advance()
                break
            if c == '$' and i + 1 < n and code[i+1] == '{':
                # entering template expression
                advance() # consume $
                advance() # consume {
                stack.append(('${', line, col))
                break
            advance()
        continue

    # Brackets
    if ch in '({[':
        stack.append((ch, line, col))
        advance()
    elif ch in ')}]' :
        if not stack:
            print(f"❌ EXTRA CLOSING '{ch}' at line {line}:{col}")
            advance()
        else:
            top_ch, top_l, top_c = stack[-1]
            match_map = {'(': ')', '{': '}', '[': ']', '${': '}'}
            expected = match_map.get(top_ch)
            if expected == ch:
                stack.pop()
                advance()
            else:
                print(f"❌ MISMATCHED '{ch}' at line {line}:{col}, expected '{expected}' for '{top_ch}' opened at line {top_l}:{top_c}")
                stack.pop()
    else:
        advance()

print("\n--- STACK ANALYSIS COMPLETE ---")
print(f"Unclosed items remaining on stack: {len(stack)}")
for item in stack:
    print(f"  Unclosed '{item[0]}' opened at line {item[1]}:{item[2]}")
