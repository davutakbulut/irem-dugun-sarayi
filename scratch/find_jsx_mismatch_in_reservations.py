import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
if scripts:
    code = scripts[0]
    lines = code.split('\n')
    
    # Extract line 1034 to 2612
    sub_code = '\n'.join(lines[1034:2612])
    
    # Tag matcher
    tag_regex = re.compile(r'</?([A-Za-z0-9\._]+)[^>]*?>')
    
    stack = []
    for line_idx in range(1034, 2612):
        line = lines[line_idx]
        # Ignore comments
        clean_line = re.sub(r'\{/\*.*?\*/\}', '', line)
        for match in tag_regex.finditer(clean_line):
            full_tag = match.group(0)
            tag_name = match.group(1)
            
            if full_tag.endswith('/>') or full_tag.startswith('<?'):
                continue # self closing
            
            if full_tag.startswith('</'):
                # Closing tag
                if not stack:
                    print(f"Extra closing tag </{tag_name}> at line {line_idx+1}")
                else:
                    top = stack.pop()
                    if top['name'] != tag_name:
                        print(f"Tag mismatch at line {line_idx+1}: closed </{tag_name}>, expected </{top['name']}> (opened at line {top['line']})")
            else:
                # Opening tag
                stack.append({'name': tag_name, 'line': line_idx+1, 'text': line.strip()})

    print(f"\nUnclosed JSX tags: {len(stack)}")
    for item in stack:
        print(f"  <{item['name']}> opened at line {item['line']} -> {item['text'][:60]}")

