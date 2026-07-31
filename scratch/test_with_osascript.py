import subprocess
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract script tag content
scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
if not scripts:
    print("No Babel script found in index.html")
    exit()

code = scripts[0]

# Write js test script
js_test = f"""
var babelCode = {repr(code)};
try {{
    // Test basic syntax validation via Function
    new Function(babelCode);
    console.log("Syntax valid!");
}} catch(e) {{
    console.log("Syntax error: " + e.message);
}}
"""

with open('scratch/test_js.js', 'w', encoding='utf-8') as f:
    f.write(js_test)

res = subprocess.run(['osascript', '-l', 'JavaScript', 'scratch/test_js.js'], capture_output=True, text=True)
print("OSASCRIPT Output:", res.stdout, res.stderr)
