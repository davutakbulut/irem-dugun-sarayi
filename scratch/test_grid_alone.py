import subprocess
import re

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('src/pages/ReservationsListPage.jsx', 'r', encoding='utf-8') as f:
    res_jsx = f.read()

lines = res_jsx.split('\n')

# Test A: Calendar View WITHOUT 31 Days Grid (lines 695 to 761 replaced with <div>Grid Dummy</div>)
grid_dummy_cal = lines[568:695] + ['<div>Grid Dummy</div>\n</div>\n)}'] + lines[763:]
code_no_grid = '\n'.join(lines[:465] + ['{viewMode === \'table\' ? (\n<div>Table Dummy</div>\n) : (\n'] + grid_dummy_cal)

# Test B: Calendar View WITH ONLY 31 Days Grid (Header/Toolbar replaced with dummy)
only_grid_cal = ['<div className="space-y-4">\n<div>Header Dummy</div>\n'] + lines[695:762]
code_only_grid = '\n'.join(lines[:465] + ['{viewMode === \'table\' ? (\n<div>Table Dummy</div>\n) : (\n'] + only_grid_cal + lines[763:])

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
    with open('scratch/test_g.js', 'w', encoding='utf-8') as f:
        f.write(js)
    res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_g.js'], capture_output=True, text=True)
    return res.stdout.strip()

print("TEST A (NO 31-Days Grid):", test_code_str(code_no_grid))
print("TEST B (ONLY 31-Days Grid):", test_code_str(code_only_grid))
