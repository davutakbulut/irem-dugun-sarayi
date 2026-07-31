import subprocess
import re

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('src/pages/ReservationsListPage.jsx', 'r', encoding='utf-8') as f:
    res_jsx = f.read()

lines = res_jsx.split('\n')

# Let's test removing each top-level block inside return () in ReservationsListPage.jsx
# return ( starts at line 140
# 1. Draft Panel (lines 145 to 220)
# 2. Filters Panel (lines 221 to 450)
# 3. Table / Calendar switcher (lines 451 to 760)
# 4. Hourly Timeline Modal (lines 761 to 885)
# 5. Preview Modal (lines 886 to 1080)
# 6. Delete Confirm Modal (lines 1081 to 1110)
# 7. Edit Modal (lines 1111 to 1575)

def test_remove_lines(start_l, end_l):
    new_lines = lines[:start_l-1] + ['/* removed */'] + lines[end_l:]
    test_code = '\n'.join(new_lines)
    
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
    with open('scratch/test_bisect_page.js', 'w', encoding='utf-8') as f:
        f.write(js)
    res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_bisect_page.js'], capture_output=True, text=True)
    return res.stdout.strip()

blocks = [
    ("Draft Panel (145-220)", 145, 220),
    ("Filters Panel (221-450)", 221, 450),
    ("Table & Calendar View (451-760)", 451, 760),
    ("Hourly Timeline Modal (761-885)", 761, 885),
    ("Preview Modal (886-1080)", 886, 1080),
    ("Delete Confirm Modal (1081-1110)", 1081, 1110),
    ("Edit Modal (1111-1575)", 1111, 1575),
]

for name, s, e in blocks:
    res = test_remove_lines(s, e)
    print(f"Without {name}: {res[:80]}")
