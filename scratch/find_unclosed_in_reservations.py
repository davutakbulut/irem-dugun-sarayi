import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
if scripts:
    code = scripts[0]
    lines = code.split('\n')
    
    stack = []
    # inspect lines 1034 to 2612
    for line_idx in range(1034, 2612):
        line = lines[line_idx]
        for col_idx, ch in enumerate(line):
            if ch in '{(':
                stack.append((ch, line_idx + 1, col_idx + 1, line.strip()))
            elif ch in '})':
                if not stack:
                    print(f"Extra closing '{ch}' at line {line_idx+1}:{col_idx+1}")
                else:
                    top_ch, top_line, top_col, top_text = stack[-1]
                    if (ch == '}' and top_ch == '{') or (ch == ')' and top_ch == '('):
                        stack.pop()
                    else:
                        print(f"Mismatch '{ch}' at line {line_idx+1}:{col_idx+1} '{line.strip()[:40]}', expected matching for '{top_ch}' at line {top_line}:{top_col} '{top_text[:40]}'")

    print("\nUnclosed items remaining in stack:", len(stack))
    for item in stack:
        print(f"  Unclosed '{item[0]}' at line {item[1]}:{item[2]} -> {item[3][:60]}")

