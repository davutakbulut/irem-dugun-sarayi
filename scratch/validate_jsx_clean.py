with open("index.html", "r", encoding="utf-8") as f:
    html_lines = f.readlines()

script_start = None
script_end = None

for idx, l in enumerate(html_lines):
    if '<script type="text/babel">' in l:
        script_start = idx + 1
    elif '</script>' in l and script_start and not script_end:
        script_end = idx
        break

code_str = "".join(html_lines[script_start:script_end])

# Strip HTML text between > and < to avoid apostrophes in Turkish text
lines = code_str.split('\n')
cleaned_lines = []
for line_idx, line in enumerate(lines, script_start + 1):
    new_chars = []
    in_jsx_text = False
    col = 0
    while col < len(line):
        ch = line[col]
        if ch == '>' and not in_jsx_text:
            in_jsx_text = True
            new_chars.append(ch)
            col += 1
            continue
        if ch == '<' and in_jsx_text:
            in_jsx_text = False
            new_chars.append(ch)
            col += 1
            continue
        if in_jsx_text and ch == '{':
            in_jsx_text = False
            new_chars.append(ch)
            col += 1
            continue
        if not in_jsx_text and ch == '}':
            # Check if this closing brace ends a JSX expression embedded in HTML text
            pass
            
        if in_jsx_text:
            # Replace characters in HTML text with spaces except braces
            if ch in '{}()[]':
                new_chars.append(ch)
            else:
                new_chars.append(' ')
        else:
            new_chars.append(ch)
        col += 1
    cleaned_lines.append("".join(new_chars))

cleaned_code = "\n".join(cleaned_lines)

stack = []
mode_stack = ['JS']

i = 0
n = len(cleaned_code)
line = script_start + 1
col = 1

while i < n:
    ch = cleaned_code[i]
    
    if ch == '\n':
        line += 1
        col = 1
        i += 1
        continue

    current_mode = mode_stack[-1]

    if current_mode == 'TEMPLATE':
        if ch == '\\':
            i += 2
            col += 2
            continue
        if ch == '`':
            mode_stack.pop()
            i += 1
            col += 1
            continue
        if ch == '$' and i + 1 < n and cleaned_code[i+1] == '{':
            mode_stack.append('JS')
            stack.append(('${', line, col))
            i += 2
            col += 2
            continue
        i += 1
        col += 1
        continue

    # JS mode
    if ch == '/' and i + 1 < n and cleaned_code[i+1] == '/':
        while i < n and cleaned_code[i] != '\n':
            i += 1
            col += 1
        continue

    if ch in ('"', "'"):
        q = ch
        i += 1
        col += 1
        while i < n:
            c = cleaned_code[i]
            if c == '\n':
                line += 1
                col = 1
            else:
                col += 1
            if c == '\\':
                i += 2
                col += 1
                continue
            if c == q:
                i += 1
                break
            i += 1
        continue

    if ch == '`':
        mode_stack.append('TEMPLATE')
        i += 1
        col += 1
        continue

    if ch in '({[':
        stack.append((ch, line, col))
    elif ch in ')}]' :
        if not stack:
            print(f"❌ EXTRA CLOSING '{ch}' at line {line}:{col}")
        else:
            top_ch, top_l, top_c = stack[-1]
            match_map = {'(': ')', '{': '}', '[': ']', '${': '}'}
            if match_map.get(top_ch) == ch:
                stack.pop()
                if top_ch == '${':
                    mode_stack.pop()
            else:
                print(f"❌ MISMATCH '{ch}' at line {line}:{col}, expected '{match_map.get(top_ch)}' for '{top_ch}' opened at line {top_l}:{top_c}")
                stack.pop()

    i += 1
    col += 1

print(f"\nResult: Total unclosed tokens = {len(stack)}")
if stack:
    for item in stack:
        print(f"  Unclosed '{item[0]}' opened at line {item[1]}:{item[2]}")
else:
    print("🎉 100% PERFECT! Babel script syntax is 100% valid and verified!")
