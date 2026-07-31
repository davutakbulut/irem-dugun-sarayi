import subprocess
import re

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
code = scripts[0]
lines = code.split('\n')

def test_full_script_with_replacement(start_line, end_line):
    new_lines = lines[:start_line-1] + ['/* removed */'] + lines[end_line:]
    test_code = '\n'.join(new_lines)
    
    js = f"""
    {babel_js}
    var code = {repr(test_code)};
    var output = "";
    try {{
        Babel.transform(code, {{ presets: ['react'] }});
        output = "SUCCESS!";
    }} catch(e) {{
        output = "ERROR: " + e.message + (e.loc ? (" at line " + e.loc.line) : "");
    }}
    output;
    """
    with open('scratch/test_sect.js', 'w', encoding='utf-8') as f:
        f.write(js)
    res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_sect.js'], capture_output=True, text=True)
    return res.stdout.strip()

sections = [
    ("Draft Panel (1180-1260)", 1180, 1260),
    ("Filters Panel (1261-1493)", 1261, 1493),
    ("Table View (1495-1596)", 1495, 1596),
    ("Monthly Calendar View (1597-1792)", 1597, 1792),
    ("Hourly Timeline Modal (1793-1915)", 1793, 1915),
    ("Preview Modal (1916-2110)", 1916, 2110),
    ("Delete Confirm Modal (2111-2140)", 2111, 2140),
    ("Edit Modal (2141-2608)", 2141, 2608),
]

print("Testing removal of each section from index.html script...")
for name, start_l, end_l in sections:
    res = test_full_script_with_replacement(start_l, end_l)
    print(f"Without {name}: {res[:80]}")
