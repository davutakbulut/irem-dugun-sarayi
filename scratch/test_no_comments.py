import subprocess
import re

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('src/pages/ReservationsListPage.jsx', 'r', encoding='utf-8') as f:
    res_jsx = f.read()

# Strip all JSX comments {/* ... */}
no_comments = re.sub(r'\{/\*.*?\*/\}', '', res_jsx, flags=re.DOTALL)

js = f"""
if (typeof console === 'undefined') {{ var console = {{ error: function(){{}} }}; }}
else {{ console.error = function(){{}}; }}
{babel_js}
var code = {repr(no_comments)};
var out = "";
try {{
    var res = Babel.transform(code, {{ presets: ['react'], compact: true }});
    out = "NO COMMENTS SUCCESS! Length: " + res.code.length;
}} catch(e) {{
    out = "NO COMMENTS ERROR: " + e.message + (e.loc ? (" at line " + e.loc.line) : "");
}}
out;
"""

with open('scratch/test_nocomm.js', 'w', encoding='utf-8') as f:
    f.write(js)

res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_nocomm.js'], capture_output=True, text=True)
print("NO COMMENTS RESULT:", res.stdout.strip())
