import re

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Remove line 4154 (index 4153)
lines_fixed = lines[:4153] + lines[4154:]

start_line = 3349
end_line = 4274 # adjusted after 1 deletion

open_divs = 0
for idx in range(start_line - 1, end_line):
    line_num = idx + 1
    line_str = lines_fixed[idx]
    
    div_opens = len(re.findall(r'<div[\s/>]', line_str))
    div_closes = line_str.count('</div>')
    
    open_divs += (div_opens - div_closes)

print(f"Fixed net open divs at end of component: {open_divs}")
