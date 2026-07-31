import time
import re
import subprocess

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
if not scripts:
    print("No Babel script found in index.html")
    exit()

raw_jsx = '\n\n'.join(scripts)

js_code = f"""
if (typeof console === 'undefined') {{ var console = {{ error: function(){{}}, log: function(){{}} }}; }}

{open('scratch/babel.min.js', 'r', encoding='utf-8').read()}

var targetCode = {repr(raw_jsx)};

try {{
    var res = Babel.transform(targetCode, {{ presets: ['react'], compact: true }});
    res.code;
}} catch (err) {{
    "BABEL BUILD ERROR: " + err.message;
}}
"""

with open('scratch/compile_step.js', 'w', encoding='utf-8') as f:
    f.write(js_code)

print("Pre-compiling JSX via Babel standalone...")
res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/compile_step.js'], capture_output=True, text=True)

compiled_js = res.stdout.strip() or res.stderr.strip()

if not compiled_js or "BABEL BUILD ERROR" in compiled_js or len(compiled_js) < 100000:
    print("Build failed or returned small output!")
    print("Output len:", len(compiled_js))
    print("Start:", compiled_js[:300])
    exit(1)

print(f"Pre-compilation SUCCESS! Compiled JS length: {len(compiled_js)} bytes")

# Save precompiled js to assets/app.compiled.js
with open('src/app.compiled.js', 'w', encoding='utf-8') as f:
    f.write(compiled_js)

# Create index_prod.html
prod_html = html

# Remove babel.min.js script tag
prod_html = prod_html.replace('<script src="https://cdn.jsdelivr.net/npm/@babel/standalone@7.23.2/babel.min.js"></script>', '')

# Replace <script type="text/babel">...</script> with <script src="src/app.compiled.js" defer></script>
old_tag_pattern = r'<script type="text/babel">.*?</script>'
new_script_tag = '<script src="src/app.compiled.js?v=' + str(int(time.time())) + '" defer></script>'

prod_html = re.sub(old_tag_pattern, new_script_tag, prod_html, flags=re.DOTALL)

with open('index_prod.html', 'w', encoding='utf-8') as f:
    f.write(prod_html)

print("Saved pre-compiled index_prod.html and src/app.compiled.js successfully!")
