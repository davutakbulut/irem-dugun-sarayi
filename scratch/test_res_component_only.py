import subprocess
import re

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
code = scripts[0]
lines = code.split('\n')

# Extract only ReservationsListComponent lines 1035 to 2612
res_code = '\n'.join(lines[1034:2612])

js = f"""
{babel_js}

var targetCode = {repr(res_code)};

try {{
    var res = Babel.transform(targetCode, {{ presets: ['react'] }});
    "ReservationsListComponent Alone SUCCESS! Length: " + res.code.length;
}} catch (err) {{
    "ReservationsListComponent Alone ERROR: " + err.message + (err.loc ? (" (line " + err.loc.line + ")") : "");
}}
"""

with open('scratch/test_res_alone.js', 'w', encoding='utf-8') as f:
    f.write(js)

res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_res_alone.js'], capture_output=True, text=True)
print("RESULT:", res.stdout.strip())
