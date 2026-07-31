import subprocess
import re

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
code = scripts[0]
lines = code.split('\n')

# ReservationsListComponent lines 1035 to 2612
res_lines = lines[1034:2612]

# Let's test taking lines 0 to N of res_lines, and adding a simple return closing
def test_res_prefix(N):
    head = '\n'.join(res_lines[:N])
    # Try closing common structures if N is inside return ()
    test_code = head + '\n</div>\n</div>\n);}'
    
    js = f"""
    {babel_js}
    var code = {repr(test_code)};
    try {{
        Babel.transform(code, {{ presets: ['react'] }});
        return "OK";
    }} catch(e) {{
        return e.message;
    }}
    """
    with open('scratch/test_prefix.js', 'w', encoding='utf-8') as f:
        f.write(js)
    res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_prefix.js'], capture_output=True, text=True)
    return res.stdout.strip()

# Let's test lines 134 (which is line 1168 return () start) up to 1578
print("Testing prefixes of ReservationsListComponent...")
for n in [200, 400, 600, 700, 750, 760, 770, 780, 800, 1000, 1200, 1400, 1500, 1570]:
    res_status = test_res_prefix(n)
    print(f"Prefix {n} lines (line {1034+n}): {res_status[:60]}")
