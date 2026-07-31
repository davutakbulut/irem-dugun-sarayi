import subprocess
import re

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('src/pages/ReservationsListPage.jsx', 'r', encoding='utf-8') as f:
    res_jsx = f.read()

lines = res_jsx.split('\n')

# Let's find all conditional blocks in return () like {draftReservations.length > 0 && ( ... )}
# Let's test replacing each conditional block with a simple dummy node <div>Dummy</div>

conditional_ranges = [
    ("Draft Panel (145-220)", 145, 220, "<div>Draft Dummy</div>"),
    ("Filter Open (226-448)", 226, 448, "<div>Filter Dummy</div>"),
    ("Table or Calendar (466-762)", 466, 762, "<div>Table Calendar Dummy</div>"),
    ("Hourly Timeline Modal (765-885)", 765, 885, "<div>Timeline Dummy</div>"),
    ("Preview Modal (886-1080)", 886, 1080, "<div>Preview Dummy</div>"),
    ("Delete Modal (1081-1110)", 1081, 1110, "<div>Delete Dummy</div>"),
    ("Edit Modal (1111-1579)", 1111, 1579, "<div>Edit Dummy</div>"),
]

def test_replace_range(start_l, end_l, dummy_text):
    new_lines = lines[:start_l-1] + [dummy_text] + lines[end_l:]
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
    with open('scratch/test_cond.js', 'w', encoding='utf-8') as f:
        f.write(js)
    res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_cond.js'], capture_output=True, text=True)
    return res.stdout.strip()

print("Testing replacement of each conditional block with clean dummy <div>...")
for name, s, e, dummy in conditional_ranges:
    res = test_replace_range(s, e, dummy)
    print(f"Replaced {name}: {res[:80]}")
