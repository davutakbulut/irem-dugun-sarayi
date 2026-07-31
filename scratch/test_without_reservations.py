import subprocess
import re

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
code = scripts[0]
lines = code.split('\n')

# Replace lines 1035 to 2612 (ReservationsListComponent) with simple dummy
dummy = """
function ReservationsListComponent() {
  return <div>Reservations Dummy</div>;
}
"""

new_lines = lines[:1034] + [dummy] + lines[2612:]
test_code = '\n'.join(new_lines)

js = f"""
if (typeof console === 'undefined') {{ var console = {{ error: function(){{}} }}; }}
else {{ console.error = function(){{}}; }}
{babel_js}
var code = {repr(test_code)};
var out = "";
try {{
    var res = Babel.transform(code, {{ presets: ['react'], compact: true }});
    out = "SUCCESS WITHOUT RESERVATIONS COMPONENT! Length: " + res.code.length;
}} catch(e) {{
    out = "ERROR: " + e.message + (e.loc ? (" at line " + e.loc.line) : "");
}}
out;
"""

with open('scratch/test_no_res.js', 'w', encoding='utf-8') as f:
    f.write(js)

res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_no_res.js'], capture_output=True, text=True)
print("WITHOUT RESERVATIONS RESULT:", res.stdout.strip())
