import subprocess
import re

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('src/pages/ReservationsListPage.jsx', 'r', encoding='utf-8') as f:
    res_jsx = f.read()

lines = res_jsx.split('\n')

# Main page content is line 140 to 764
def test_main_prefix(end_line):
    # Take lines 0 to end_line, and close with </div>\n);\n}
    test_code = '\n'.join(lines[:end_line]) + '\n</div></div></div></div></div>\n);\n}'
    
    js = f"""
    if (typeof console === 'undefined') {{ var console = {{ error: function(){{}} }}; }}
    else {{ console.error = function(){{}}; }}
    {babel_js}
    var code = {repr(test_code)};
    var out = "";
    try {{
        var res = Babel.transform(code, {{ presets: ['react'], compact: true }});
        out = "SUCCESS!";
    }} catch(e) {{
        out = "ERROR: " + e.message + (e.loc ? (" at line " + e.loc.line) : "");
    }}
    out;
    """
    with open('scratch/test_main.js', 'w', encoding='utf-8') as f:
        f.write(js)
    res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_main.js'], capture_output=True, text=True)
    return res.stdout.strip()

print("Testing line by line prefixes between line 140 and 764...")
for l in range(145, 765, 20):
    res = test_main_prefix(l)
    print(f"Prefix up to line {l}: {res[:70]}")
