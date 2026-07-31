import subprocess
import re

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
code = scripts[0]
lines = code.split('\n')

def test_insert_div_at(target_line):
    new_lines = lines[:target_line] + ['</div>'] + lines[target_line:]
    test_code = '\n'.join(new_lines)
    
    js = f"""
    if (typeof console === 'undefined') {{ var console = {{ error: function(){{}} }}; }}
    else {{ console.error = function(){{}}; }}
    {babel_js}
    var code = {repr(test_code)};
    var out = "";
    try {{
        var res = Babel.transform(code, {{ presets: ['react'], compact: true }});
        out = "SUCCESS! Output length: " + res.code.length;
    }} catch(e) {{
        out = "ERROR: " + e.message + (e.loc ? (" at line " + e.loc.line) : "");
    }}
    out;
    """
    with open('scratch/test_ins.js', 'w', encoding='utf-8') as f:
        f.write(js)
    res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_ins.js'], capture_output=True, text=True)
    return res.stdout.strip()

for line_n in [1260, 1493, 1596, 1792, 1915, 2110, 2140, 2606]:
    res_str = test_insert_div_at(line_n)
    print(f"Insert </div> at line {line_n}: {res_str[:70]}")
