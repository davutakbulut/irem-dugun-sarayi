import re
import html.parser

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

script_match = re.search(r'<script type="text/babel">(.*?)</script>', content, re.DOTALL)
code = script_match.group(1)

# Simple JSX tag balancer
# Remove JS string contents first
lines = code.split('\n')
clean_lines = []
for l in lines:
    # remove // comments
    comment_idx = l.find('//')
    if comment_idx != -1:
        # Check if // is inside string
        quote_cnt = l[:comment_idx].count('"') + l[:comment_idx].count("'") + l[:comment_idx].count('`')
        if quote_cnt % 2 == 0:
            l = l[:comment_idx]
    clean_lines.append(l)

clean_code = "\n".join(clean_lines)

# Find JSX tags: <tag ...>, </tag>, <tag ... />
tag_pattern = re.compile(r'</?([A-Za-z0-9.]+)(?:[^>"\']|"[^"]*"|\'[^\']*\')*/?>')

tag_stack = []
for line_num, line in enumerate(clean_lines, 1):
    for match in tag_pattern.finditer(line):
        full_tag = match.group(0)
        tag_name = match.group(1)
        
        # Ignore self closing
        if full_tag.endswith('/>') or tag_name in ('img', 'input', 'br', 'hr', 'meta', 'link'):
            continue
            
        if full_tag.startswith('</'):
            if not tag_stack:
                print(f"ERROR: Extra closing tag </{tag_name}> at line {line_num}")
            else:
                top_tag, top_line = tag_stack.pop()
                if top_tag != tag_name:
                    print(f"ERROR: Mismatched tag </{tag_name}> at line {line_num}, expected </{top_tag}> opened at line {top_line}")
        else:
            tag_stack.append((tag_name, line_num))

if tag_stack:
    print(f"ERROR: {len(tag_stack)} unclosed JSX tags at end:")
    for tag_name, line_num in tag_stack[-10:]:
        print(f"  <{tag_name}> opened at line {line_num}")
else:
    print("✅ PERFECT JSX TAG MATCHING!")
