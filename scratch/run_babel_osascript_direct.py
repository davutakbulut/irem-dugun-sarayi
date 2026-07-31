import subprocess
import re

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
if not scripts:
    print("No Babel script found in index.html")
    exit()

target_code = scripts[0]

js_code = f"""
if (typeof console === 'undefined') {{ var console = {{ error: function(){{}} }}; }}
else {{ console.error = function(){{}}; }}

{babel_js}

var targetCode = {repr(target_code)};

try {{
    var res = Babel.transform(targetCode, {{ presets: ['react'], compact: true }});
    console.log("SUCCESS: Transformed code length is " + res.code.length);
}} catch (err) {{
    console.log("BABEL ERROR MESSAGE: " + err.message);
    if (err.loc) {{
        console.log("BABEL ERROR LOC: line " + err.loc.line + ", column " + err.loc.column);
    }}
}}
"""

with open('scratch/run_babel_test.js', 'w', encoding='utf-8') as f:
    f.write(js_code)

print("Executing Babel standalone via JavaScriptCore (osascript)...")
res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/run_babel_test.js'], capture_output=True, text=True)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
