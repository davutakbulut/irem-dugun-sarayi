import subprocess

with open('scratch/babel.min.js', 'r', encoding='utf-8') as f:
    babel_js = f.read()

with open('src/pages/ReservationsListPage.jsx', 'r', encoding='utf-8') as f:
    res_jsx = f.read()

lines = res_jsx.split('\n')

def test_line_count(N):
    prefix = '\n'.join(lines[:N])
    
    # We will try appending 1..15 closing divs
    for num_divs in range(1, 15):
        dummy = prefix + '\n' + '\n'.join(['</div>'] * num_divs) + '\n);\n}'
        js = f"""
        if (typeof console === 'undefined') {{ var console = {{ error: function(){{}} }}; }}
        else {{ console.error = function(){{}}; }}
        {babel_js}
        var code = {repr(dummy)};
        try {{
            Babel.transform(code, {{ presets: ['react'], compact: true }});
            return "SUCCESS";
        }} catch(e) {{
            // continue
        }}
        """
        with open('scratch/test_step.js', 'w', encoding='utf-8') as f:
            f.write(js)
        res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_step.js'], capture_output=True, text=True)
        if "SUCCESS" in res.stdout:
            return "SUCCESS"
    return "FAIL"

last_good = 140
for n in range(141, 1580):
    status = test_line_count(n)
    if status == "SUCCESS":
        last_good = n
    else:
        print(f"FAILED AT LINE {n}! (Last good line: {last_good})")
        print(f"Line {n}: {lines[n-1]}")
        break

print(f"\nLines around failure:")
for i in range(max(0, last_good-2), min(len(lines), last_good+8)):
    print(f"{i+1}: {lines[i]}")
