import subprocess
import re

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('src/pages/ReservationsListPage.jsx', 'r', encoding='utf-8') as f:
    res_jsx = f.read()

res_lines = [l for l in res_jsx.split('\n') if not l.strip().startswith('import ')]
clean_res_code = '\n'.join(res_lines)

js = f"""
if (typeof console === 'undefined') {{ var console = {{ error: function(){{}} }}; }}
else {{ console.error = function(){{}}; }}
{babel_js}
var code = {repr(clean_res_code)};
var out = "";
try {{
    var res = Babel.transform(code, {{ presets: ['react'], compact: true }});
    out = "RESERVATIONS LIST PAGE ALONE SUCCESS! Length: " + res.code.length;
}} catch(e) {{
    out = "RESERVATIONS LIST PAGE ALONE ERROR: " + e.message + (e.loc ? (" at line " + e.loc.line) : "");
}}
out;
"""

with open('scratch/test_page_alone.js', 'w', encoding='utf-8') as f:
    f.write(js)

res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_page_alone.js'], capture_output=True, text=True)
print("PAGE ALONE RESULT:", res.stdout.strip())
