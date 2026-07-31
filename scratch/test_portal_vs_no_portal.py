import subprocess
import re

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('src/pages/ReservationsListPage.jsx', 'r', encoding='utf-8') as f:
    res_jsx = f.read()

# Replace createPortal( ... , document.body ) with simple ( ... )
# Let's test if createPortal syntax is causing Babel standalone issue in React preset
no_portal = res_jsx.replace('createPortal(', '(')
no_portal = no_portal.replace(',\n            document.body\n          )', ')')
no_portal = no_portal.replace(', document.body)', ')')

js = f"""
if (typeof console === 'undefined') {{ var console = {{ error: function(){{}} }}; }}
else {{ console.error = function(){{}}; }}
{babel_js}
var code = {repr(no_portal)};
var out = "";
try {{
    var res = Babel.transform(code, {{ presets: ['react'], compact: true }});
    out = "NO PORTAL SUCCESS! Length: " + res.code.length;
}} catch(e) {{
    out = "NO PORTAL ERROR: " + e.message + (e.loc ? (" at line " + e.loc.line) : "");
}}
out;
"""

with open('scratch/test_noportal.js', 'w', encoding='utf-8') as f:
    f.write(js)

res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_noportal.js'], capture_output=True, text=True)
print("NO PORTAL RESULT:", res.stdout.strip())
