import subprocess
import re

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('src/pages/ReservationsListPage.jsx', 'r', encoding='utf-8') as f:
    res_jsx = f.read()

lines = res_jsx.split('\n')

# Insert </div> after line 760 (index 760)
fixed_lines = lines[:761] + ['              </div>'] + lines[761:]
fixed_code = '\n'.join(fixed_lines)

js = f"""
if (typeof console === 'undefined') {{ var console = {{ error: function(){{}} }}; }}
else {{ console.error = function(){{}}; }}
{babel_js}
var code = {repr(fixed_code)};
var out = "";
try {{
    var res = Babel.transform(code, {{ presets: ['react'], compact: true }});
    out = "FIX SUCCESS! Total output length: " + res.code.length;
}} catch(e) {{
    out = "FIX ERROR: " + e.message + (e.loc ? (" at line " + e.loc.line) : "");
}}
out;
"""

with open('scratch/test_fix_div.js', 'w', encoding='utf-8') as f:
    f.write(js)

res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_fix_div.js'], capture_output=True, text=True)
print("TEST FIX RESULT:", res.stdout.strip())
