import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
code = scripts[0]
lines = code.split('\n')

# Edit Modal is lines 2141 to 2608
edit_modal_lines = lines[2140:2608]
edit_code = '\n'.join(edit_modal_lines)

# Let's inspect all <input...>, <select...>, <textarea...> tags in edit_code
tag_re = re.compile(r'<(input|select|textarea|div|button|span|label|p|h[1-6]|form|table|thead|tbody|tr|th|td)[^>]*?>', re.DOTALL)

stack = []

for idx, line in enumerate(edit_modal_lines):
    line_num = 2141 + idx
    # find tags
    for match in re.finditer(r'</?([a-zA-Z0-9]+)[^>]*?>', line):
        full_tag = match.group(0)
        tag_name = match.group(1)
        
        if full_tag.endswith('/>'):
            continue
            
        if full_tag.startswith('</'):
            if not stack:
                print(f"Edit Modal EXTRA CLOSING </{tag_name}> at line {line_num}: {line.strip()}")
            else:
                top = stack.pop()
                if top['name'] != tag_name:
                    print(f"Edit Modal MISMATCH line {line_num}: closed </{tag_name}>, expected </{top['name']}> (opened at line {top['line']})")
        else:
            stack.append({'name': tag_name, 'line': line_num, 'text': line.strip()})

print(f"\nEdit Modal Stack Size at end: {len(stack)}")
for t in stack:
    print(f"  <{t['name']}> opened at line {t['line']} -> {t['text'][:60]}")
