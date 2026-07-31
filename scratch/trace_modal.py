import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

script_match = re.search(r'<script type="text/babel">(.*?)</script>', content, re.DOTALL)
code = script_match.group(1)

lines = code.split('\n')

# Let's inspect tokens in lines 2733 to 2785 line by line
stack = []
match_map = {'(': ')', '{': '}', '[': ']'}

for idx in range(2732, 2785):
    line_num = idx + 1
    line = lines[idx]
    
    # Strip strings and comments
    cleaned = ""
    i = 0
    while i < len(line):
        if line[i:i+2] == '//':
            break
        cleaned += line[i]
        i += 1
        
    for col, ch in enumerate(cleaned, 1):
        if ch in '({[':
            stack.append((ch, line_num, col))
            print(f"PUSH '{ch}' at {line_num}:{col} -> stack len {len(stack)}")
        elif ch in ')}]' :
            if stack:
                top_ch, top_line, top_col = stack.pop()
                print(f"POP  '{ch}' at {line_num}:{col} matching '{top_ch}' from {top_line}:{top_col} -> stack len {len(stack)}")
            else:
                print(f"EXTRA '{ch}' at {line_num}:{col}")
