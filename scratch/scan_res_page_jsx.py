import subprocess
import re

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('src/pages/ReservationsListPage.jsx', 'r', encoding='utf-8') as f:
    res_jsx = f.read()

lines = res_jsx.split('\n')

# Let's test slicing lines 1 to K and adding </div>\n</div>\n</div>... ); }
def test_page_slice(end_line):
    slice_lines = lines[:end_line]
    dummy = '\n'.join(slice_lines) + '\n</div></div></div></div></div></div></div></div></div></div></div></div>\n);\n}'
    
    js = f"""
    if (typeof console === 'undefined') {{ var console = {{ error: function(){{}} }}; }}
    else {{ console.error = function(){{}}; }}
    {babel_js}
    var code = {repr(dummy)};
    var out = "";
    try {{
        var res = Babel.transform(code, {{ presets: ['react'], compact: true }});
        out = "SUCCESS!";
    }} catch(e) {{
        out = "ERROR: " + e.message + (e.loc ? (" at line " + e.loc.line) : "");
    }}
    out;
    """
    with open('scratch/test_sl.js', 'w', encoding='utf-8') as f:
        f.write(js)
    res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_sl.js'], capture_output=True, text=True)
    return res.stdout.strip()

print("Scanning line ranges in ReservationsListPage.jsx...")
for line_n in range(150, 1580, 20):
    res = test_page_slice(line_n)
    if "ERROR" in res:
        print(f"Line {line_n}: {res[:80]}")
