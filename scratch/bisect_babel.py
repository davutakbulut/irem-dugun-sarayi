import subprocess
import re

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
code = scripts[0]
lines = code.split('\n')

# ReservationsListComponent is from line 1035 (idx 1034) to line 2612 (idx 2611)
# Let's test compiling small chunks or building fake component endings
# For example, line 1034 to line K + closing tags

res_head = '\n'.join(lines[1034:1168]) # Component setup up to return (

print("Head lines count:", 1168 - 1034)

# Let's test ending the component at different line numbers N between 1168 and 2608
def test_slice(end_line):
    chunk = '\n'.join(lines[1034:end_line])
    # Add dummy closing tags to try to close return ( and function
    dummy_code = chunk + '\n</div>\n</div>\n</div>\n</div>\n</div>\n</div>\n</div>\n</div>\n);}'
    
    js = f"""
    {babel_js}
    var code = {repr(dummy_code)};
    try {{
        Babel.transform(code, {{ presets: ['react'] }});
        return "OK";
    }} catch(e) {{
        return e.message;
    }}
    """
    with open('scratch/test_tmp.js', 'w', encoding='utf-8') as f:
        f.write(js)
    res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_tmp.js'], capture_output=True, text=True)
    return res.stdout.strip()

# Let's bisect line by line or step by 50 lines
for line_num in range(1170, 2610, 50):
    err = test_slice(line_num)
    print(f"Line {line_num}: {err[:80]}")
