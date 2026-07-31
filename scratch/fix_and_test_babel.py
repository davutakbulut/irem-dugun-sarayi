import subprocess
import re

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
code = scripts[0]

# Let's test removing line 2610 (</div> right before );)
lines = code.split('\n')
print("Line 2609:", lines[2608])
print("Line 2610:", lines[2609])
print("Line 2611:", lines[2610])
print("Line 2612:", lines[2611])

# Try removing line 2610
mod_lines = lines[:2609] + lines[2610:]
mod_code = '\n'.join(mod_lines)

js = f"""
if (typeof console === 'undefined') {{
    var console = {{ log: function(){{}}, warn: function(){{}}, error: function(){{}} }};
}} else {{
    if (!console.error) console.error = function(){{}};
    if (!console.warn) console.warn = function(){{}};
}}

{babel_js}

var targetCode = {repr(mod_code)};

try {{
    var res = Babel.transform(targetCode, {{ presets: ['react'], compact: true }});
    "SUCCESS WITHOUT LINE 2610! Length: " + res.code.length;
}} catch(e) {{
    "ERROR WITHOUT LINE 2610: " + e.message + (e.loc ? (" at line " + e.loc.line) : "");
}}
"""

with open('scratch/test_fix1.js', 'w', encoding='utf-8') as f:
    f.write(js)

res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_fix1.js'], capture_output=True, text=True)
print("TEST WITHOUT LINE 2610 RESULT:", res.stdout.strip())
