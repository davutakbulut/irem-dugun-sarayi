import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', content, re.DOTALL)

for idx, script in enumerate(scripts, 1):
    lines = script.split('\n')
    stack = []
    in_str = None
    escaped = False
    
    for line_num, line in enumerate(lines, 1):
        i = 0
        while i < len(line):
            ch = line[i]
            if not in_str and line[i:i+2] == '//':
                break
            if not in_str:
                if ch in ('"', "'", '`'):
                    in_str = ch
                elif ch in ('{', '(', '['):
                    stack.append((ch, line_num, i+1, line.strip()))
                elif ch in ('}', ')', ']'):
                    if not stack:
                        print(f"ERROR: Extra closing '{ch}' at line {line_num}:{i+1} -> {line.strip()}")
                    else:
                        top, t_line, t_col, t_code = stack.pop()
                        expected = {'{': '}', '(': ')', '[': ']'}[top]
                        if ch != expected:
                            print(f"MISMATCH at L{line_num}:{i+1} '{ch}' vs expected '{expected}' for '{top}' opened at L{t_line}:{t_col} ({t_code})")
                            print("\nCURRENT UNMATCHED STACK (Last 10):")
                            for item, l_num, c_num, code in stack[-10:]:
                                print(f"  L{l_num}:{c_num} '{item}' -> {code[:70]}")
                            break
            else:
                if ch == '\\' and not escaped:
                    escaped = True
                elif ch == in_str and not escaped:
                    in_str = None
                else:
                    escaped = False
            i += 1
