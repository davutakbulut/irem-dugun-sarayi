import subprocess
import re

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('src/pages/ReservationsListPage.jsx', 'r', encoding='utf-8') as f:
    res_jsx = f.read()

lines = res_jsx.split('\n')

# Test 1: Keep Table View, replace Calendar View with dummy
lines_table_only = lines[:568] + ['<div>Calendar Dummy</div>\n          )}'] + lines[763:]
code_table_only = '\n'.join(lines_table_only)

# Test 2: Keep Calendar View, replace Table View with dummy
lines_cal_only = lines[:465] + ['{viewMode === \'table\' ? (\n<div>Table Dummy</div>\n) : (\n'] + lines[569:]
code_cal_only = '\n'.join(lines_cal_only)

def test_code_str(code):
    js = f"""
    if (typeof console === 'undefined') {{ var console = {{ error: function(){{}} }}; }}
    else {{ console.error = function(){{}}; }}
    {babel_js}
    var code = {repr(code)};
    var out = "";
    try {{
        var res = Babel.transform(code, {{ presets: ['react'], compact: true }});
        out = "SUCCESS!";
    }} catch(e) {{
        out = "ERROR: " + e.message + (e.loc ? (" at line " + e.loc.line) : "");
    }}
    out;
    """
    with open('scratch/test_tc.js', 'w', encoding='utf-8') as f:
        f.write(js)
    res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_tc.js'], capture_output=True, text=True)
    return res.stdout.strip()

print("TEST 1 (Table View Only, Calendar Dummy):", test_code_str(code_table_only))
print("TEST 2 (Calendar View Only, Table Dummy):", test_code_str(code_cal_only))
