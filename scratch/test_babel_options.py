import subprocess
import re

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
code = scripts[0]

js = f"""
if (typeof console === 'undefined') {{
    var console = {{ log: function(){{}}, warn: function(){{}}, error: function(){{}} }};
}} else {{
    if (!console.error) console.error = function(){{}};
    if (!console.warn) console.warn = function(){{}};
}}

{babel_js}

var targetCode = {repr(code)};

try {{
    var res = Babel.transform(targetCode, {{ presets: ['react'], compact: true }});
    "COMPACT TRUE SUCCESS! Code length: " + res.code.length;
}} catch (err) {{
    "COMPACT TRUE ERROR: " + err.message + (err.loc ? (" (line " + err.loc.line + ")") : "");
}}
"""

with open('scratch/test_opt.js', 'w', encoding='utf-8') as f:
    f.write(js)

res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_opt.js'], capture_output=True, text=True)
print("COMPACT TRUE RESULT:", res.stdout.strip())
