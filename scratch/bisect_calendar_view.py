import subprocess
import re

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('src/pages/ReservationsListPage.jsx', 'r', encoding='utf-8') as f:
    res_jsx = f.read()

lines = res_jsx.split('\n')

# Calendar View is lines 569 to 762
# Let's test removing each sub-section of Calendar View

sub_sections = [
    ("Header & Badge (572-584)", 572, 584),
    ("Toolbar & Dropdowns (585-683)", 585, 683),
    ("7 Column Headers (684-694)", 684, 694),
    ("31 Days Grid (695-761)", 695, 761),
]

def test_cal_sub(start_l, end_l):
    # Keep Table View dummy, replace sub-section in Calendar View
    cal_lines = lines[568:start_l-1] + ['/* removed */'] + lines[end_l:762]
    cal_code = '\n'.join(cal_lines)
    
    test_lines = lines[:465] + ['{viewMode === \'table\' ? (\n<div>Table Dummy</div>\n) : (\n' + cal_code + '\n)}'] + lines[763:]
    test_code = '\n'.join(test_lines)
    
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
    with open('scratch/test_sub.js', 'w', encoding='utf-8') as f:
        f.write(js)
    res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_sub.js'], capture_output=True, text=True)
    return res.stdout.strip()

for name, s, e in sub_sections:
    print(f"Without {name}: {test_cal_sub(s, e)}")
