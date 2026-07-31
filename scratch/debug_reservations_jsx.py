import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
if scripts:
    code = scripts[0]
    lines = code.split('\n')
    
    # Lines 1034 to 2612
    res_lines = lines[1034:2612]
    
    tag_stack = []
    
    # Simple JSX Tag Parser
    for idx, line in enumerate(res_lines):
        line_num = 1035 + idx
        # Strip comments
        clean = re.sub(r'\{/\*.*?\*/\}', '', line)
        clean = re.sub(r'//.*', '', clean)
        
        # Find tags
        matches = re.finditer(r'</?([a-zA-Z0-9\.\-_]+)[^>]*?>', clean)
        for m in matches:
            tag_str = m.group(0)
            tag_name = m.group(1)
            
            if tag_str.endswith('/>') or tag_str.startswith('<?'):
                continue
                
            if tag_str.startswith('</'):
                if not tag_stack:
                    print(f"Extra closing tag </{tag_name}> at line {line_num}")
                else:
                    last_tag = tag_stack.pop()
                    if last_tag['name'] != tag_name:
                        print(f"MISMATCH at line {line_num}: closed </{tag_name}>, expected </{last_tag['name']}> (opened at line {last_tag['line']})")
            else:
                tag_stack.append({'name': tag_name, 'line': line_num, 'text': line.strip()})

    print(f"\nTotal unclosed tags: {len(tag_stack)}")
    for t in tag_stack:
        print(f"  <{t['name']}> opened at line {t['line']} -> {t['text'][:60]}")

