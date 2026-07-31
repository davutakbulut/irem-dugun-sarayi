import subprocess
import re

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('src/pages/ReservationsListPage.jsx', 'r', encoding='utf-8') as f:
    res_jsx = f.read()

lines = res_jsx.split('\n')

# Find line numbers of the 4 modals
# Modal 1: Hourly Timeline (selectedDayInspector)
# Modal 2: Preview (selectedResForPreview)
# Modal 3: Delete (deletingRes)
# Modal 4: Edit (editingRes)

def test_without_range(start_l, end_l):
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
    with open('scratch/test_m.js', 'w', encoding='utf-8') as f:
        f.write(js)
    res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_m.js'], capture_output=True, text=True)
    return res.stdout.strip()

print("Modal 1 (Hourly Timeline ~765-885):", test_without_range(765, 885))
print("Modal 2 (Preview ~886-1080):", test_without_range(886, 1080))
print("Modal 3 (Delete ~1081-1110):", test_without_range(1081, 1110))
print("Modal 4 (Edit ~1111-1579):", test_without_range(1111, 1579))

# Test removing ALL 4 MODALS AT ONCE
new_lines_all = lines[:764] + ['</div>\n);\n}']
test_code_all = '\n'.join(new_lines_all)
js_all = f"""
if (typeof console === 'undefined') {{ var console = {{ error: function(){{}} }}; }}
else {{ console.error = function(){{}}; }}
{babel_js}
var code = {repr(test_code_all)};
var out = "";
try {{
    var res = Babel.transform(code, {{ presets: ['react'], compact: true }});
    out = "ALL MODALS REMOVED SUCCESS!";
}} catch(e) {{
    out = "ALL MODALS REMOVED ERROR: " + e.message + (e.loc ? (" at line " + e.loc.line) : "");
}}
out;
"""
with open('scratch/test_m_all.js', 'w', encoding='utf-8') as f:
    f.write(js_all)
res_all = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_m_all.js'], capture_output=True, text=True)
print("ALL 4 MODALS REMOVED RESULT:", res_all.stdout.strip())
