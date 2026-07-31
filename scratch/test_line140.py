import subprocess

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('src/pages/ReservationsListPage.jsx', 'r', encoding='utf-8') as f:
    res_jsx = f.read()

lines = res_jsx.split('\n')

test_code = '\n'.join(lines[:140]) + '\n</div>\n);\n}'

js = f"""
if (typeof console === 'undefined') {{ var console = {{ error: function(){{}} }}; }}
else {{ console.error = function(){{}}; }}
{babel_js}
var code = {repr(test_code)};
try {{
    var res = Babel.transform(code, {{ presets: ['react'], compact: true }});
    "SUCCESS LINE 140! Length: " + res.code.length;
}} catch(e) {{
    "ERROR LINE 140: " + e.message;
}}
"""

with open('scratch/test_140.js', 'w', encoding='utf-8') as f:
    f.write(js)

res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_140.js'], capture_output=True, text=True)
print("LINE 140 RESULT:", res.stdout.strip())
