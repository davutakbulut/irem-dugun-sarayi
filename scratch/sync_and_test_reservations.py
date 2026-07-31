import subprocess
import re

with open('src/pages/ReservationsListPage.jsx', 'r', encoding='utf-8') as f:
    res_jsx = f.read()

# Strip import statements
res_lines = [l for l in res_jsx.split('\n') if not l.strip().startswith('import ')]
clean_res_code = '\n'.join(res_lines)

# Convert export function ReservationsListPage to function ReservationsListComponent
clean_res_code = clean_res_code.replace('export function ReservationsListPage(', 'function ReservationsListComponent(')
clean_res_code = clean_res_code.replace('export function ReservationsListPage', 'function ReservationsListComponent')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
code = scripts[0]
lines = code.split('\n')

# Replace lines 1035 to 2612 (ReservationsListComponent) with clean_res_code
new_lines = lines[:1034] + [clean_res_code] + lines[2612:]
test_code = '\n'.join(new_lines)

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

js = f"""
if (typeof console === 'undefined') {{ var console = {{ error: function(){{}} }}; }}
else {{ console.error = function(){{}}; }}
{babel_js}
var code = {repr(test_code)};
var out = "";
try {{
    var res = Babel.transform(code, {{ presets: ['react'], compact: true }});
    out = "SYNC SUCCESS! Total transformed length: " + res.code.length;
}} catch(e) {{
    out = "SYNC ERROR: " + e.message + (e.loc ? (" at line " + e.loc.line) : "");
}}
out;
"""

with open('scratch/test_sync.js', 'w', encoding='utf-8') as f:
    f.write(js)

res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_sync.js'], capture_output=True, text=True)
print("SYNC TEST RESULT:", res.stdout.strip())

if "SYNC SUCCESS" in res.stdout:
    # Update index.html for real!
    p_start = html.find('// --- RESERVATIONS LIST COMPONENT ---')
    p_end = html.find('// --- USERS COMPONENT ---')
    if p_start != -1 and p_end != -1:
        new_html = html[:p_start] + '// --- RESERVATIONS LIST COMPONENT ---\n' + clean_res_code + '\n\n' + html[p_end:]
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(new_html)
        print("Updated index.html on disk successfully!")
