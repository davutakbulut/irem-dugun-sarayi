import subprocess
import re

babel_js_path = '/Users/davutakbulut/.gemini/antigravity/brain/f60111cc-5bec-4b99-8da2-93a0a75c00b9/.system_generated/steps/10029/content.md'

with open(babel_js_path, 'r', encoding='utf-8') as f:
    babel_lib = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
if not scripts:
    print("No script tag found!")
    exit()

code = scripts[0]

# Build osascript JavaScript file
js_runner = f"""
{babel_lib}

var targetCode = {repr(code)};

try {{
    var result = Babel.transform(targetCode, {{ presets: ['react'] }});
    console.log("Babel Transform SUCCESS! Output length: " + result.code.length);
}} catch (e) {{
    console.log("Babel Transform ERROR: " + e.message);
    if (e.loc) {{
        console.log("Error Location: line " + e.loc.line + ", column " + e.loc.column);
    }}
}}
"""

with open('scratch/test_babel_exec.js', 'w', encoding='utf-8') as f:
    f.write(js_runner)

print("Running osascript test with real Babel standalone...")
res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_babel_exec.js'], capture_output=True, text=True)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
