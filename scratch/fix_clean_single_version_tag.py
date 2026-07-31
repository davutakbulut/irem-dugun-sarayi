import re
import time
import sys

timestamp = int(time.time())

# Clean index.html and index_prod.html script tag
for fname in ['index.html', 'index_prod.html']:
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Regex replace any src="src/app.compiled.js[^"]*" with clean timestamped version
        content = re.sub(
            r'src="src/app\.compiled\.js[^"]*"',
            f'src="src/app.compiled.js?v={timestamp}"',
            content
        )
        
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Cleaned script tag in {fname} to src/app.compiled.js?v={timestamp}")
    except Exception as e:
        print(f"Error cleaning {fname}:", e)

# Fix build_precompiled.py
with open('scratch/build_precompiled.py', 'r', encoding='utf-8') as f:
    py_code = f.read()

py_code = re.sub(
    r'new_script_tag = \'<script src="src/app\.compiled\.js[^"]*" defer></script>\'',
    "new_script_tag = '<script src=\"src/app.compiled.js?v=' + str(int(time.time())) + '\" defer></script>'",
    py_code
)

if "import time" not in py_code:
    py_code = "import time\n" + py_code

with open('scratch/build_precompiled.py', 'w', encoding='utf-8') as f:
    f.write(py_code)

print("Updated build_precompiled.py with clean dynamic timestamping!")
