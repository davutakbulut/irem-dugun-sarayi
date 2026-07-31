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

stack = []
mode_stack = ['JS']

i = 0
n = len(code_str)
line = script_start + 1
col = 1

while i < n:
    ch = code_str[i]
    
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
        if ch == '$' and i + 1 < n and code_str[i+1] == '{':
            mode_stack.append('JS')
            stack.append(('${', line, col))
            if line >= 3558 and line <= 3610:
                print(f"[{line}:{col}] PUSH '${{' -> stack: {[x[0] for x in stack]}")
            i += 2
            col += 2
            continue
        i += 1
        col += 1
        continue

    # JS mode
    if ch == '/' and i + 1 < n and code_str[i+1] == '/':
        while i < n and code_str[i] != '\n':
            i += 1
            col += 1
        continue

    if ch == '/' and i + 1 < n and code_str[i+1] == '*':
        i += 2
        col += 2
        while i + 1 < n and not (code_str[i] == '*' and code_str[i+1] == '/'):
            if code_str[i] == '\n':
                line += 1
                col = 1
            else:
                col += 1
            i += 1
        i += 2
        col += 2
        continue

    if ch in ('"', "'"):
        q = ch
        i += 1
        col += 1
        while i < n:
            c = code_str[i]
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
        if line >= 3558 and line <= 3610:
            print(f"[{line}:{col}] PUSH '{ch}' -> stack: {[x[0] for x in stack]}")
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
                if line >= 3558 and line <= 3610:
                    print(f"[{line}:{col}] POP '{ch}' (matched {top_ch} from {top_l}:{top_c}) -> stack: {[x[0] for x in stack]}")
            else:
                print(f"❌ MISMATCH '{ch}' at line {line}:{col}, expected '{match_map.get(top_ch)}' for '{top_ch}' opened at line {top_l}:{top_c}")
                stack.pop()

    i += 1
    col += 1
