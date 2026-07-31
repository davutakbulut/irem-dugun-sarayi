import subprocess
import re

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('src/pages/ReservationsListPage.jsx', 'r', encoding='utf-8') as f:
    res_jsx = f.read()

lines = res_jsx.split('\n')

def test_page_prefix_flexible(end_line):
    prefix_code = '\n'.join(lines[:end_line])
    
    # Try 1 to 12 closing </div>s
    for depth in range(1, 12):
        dummy_closings = '\n'.join(['</div>'] * depth) + '\n);\n}'
        test_code = prefix_code + '\n' + dummy_closings
        js = f"""
        if (typeof console === 'undefined') {{ var console = {{ error: function(){{}} }}; }}
        else {{ console.error = function(){{}}; }}
        {babel_js}
        var code = {repr(test_code)};
        try {{
            Babel.transform(code, {{ presets: ['react'], compact: true }});
            return true;
        }} catch(e) {{
            // continue
        }}
        """
        with open('scratch/test_flex.js', 'w', encoding='utf-8') as f:
            f.write(js)
        res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_flex.js'], capture_output=True, text=True)
        if "true" in res.stdout:
            return True
    return False

print("Testing flexible line prefixes from 140 to 1580...")
last_good = 138
for l in range(140, 1580, 5):
    ok = test_page_prefix_flexible(l)
    if ok:
        last_good = l
    else:
        print(f"FAILED AT LINE {l} (Last good line: {last_good})")
        break

print(f"\nLast good prefix line: {last_good}")
for i in range(max(0, last_good-3), min(len(lines), last_good+15)):
    print(f"{i+1}: {lines[i]}")
