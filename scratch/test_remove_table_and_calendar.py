import subprocess
import re

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
code = scripts[0]
lines = code.split('\n')

# Remove lines 1495 to 1792
new_lines = lines[:1494] + ['<div className="p-4">Placeholder</div>'] + lines[1792:]
test_code = '\n'.join(new_lines)

js = f"""
{babel_js}
var code = {repr(test_code)};
try {{
    Babel.transform(code, {{ presets: ['react'] }});
    "SUCCESS WITHOUT TABLE & CALENDAR!";
}} catch(e) {{
    "ERROR: " + e.message + (e.loc ? (" at line " + e.loc.line) : "");
}}
"""

with open('scratch/test_no_cal.js', 'w', encoding='utf-8') as f:
    f.write(js)

res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_no_cal.js'], capture_output=True, text=True)
print("RESULT:", res.stdout.strip())
