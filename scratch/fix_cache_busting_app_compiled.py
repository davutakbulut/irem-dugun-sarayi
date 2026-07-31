import time
import sys

timestamp = int(time.time())

# 1. Update index.html and index_prod.html to load src/app.compiled.js?v={timestamp}
for fname in ['index.html', 'index_prod.html']:
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace src/app.compiled.js with timestamped version
        content = content.replace('src/app.compiled.js', f'src/app.compiled.js?v={timestamp}')
        
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {fname} with cache-busting script tag v={timestamp}!")
    except Exception as e:
        print(f"Could not update {fname}:", e)

# 2. Update build_precompiled.py to output timestamped script tag in index_prod.html
with open('scratch/build_precompiled.py', 'r', encoding='utf-8') as f:
    py_code = f.read()

old_script_tag = "new_script_tag = '<script src=\"src/app.compiled.js\" defer></script>'"
new_script_tag = f"new_script_tag = '<script src=\"src/app.compiled.js?v={timestamp}\" defer></script>'"

if old_script_tag in py_code:
    py_code = py_code.replace(old_script_tag, new_script_tag)
    print("Updated build_precompiled.py script tag with cache-busting version!")

with open('scratch/build_precompiled.py', 'w', encoding='utf-8') as f:
    f.write(py_code)

print("Cache-busting script update completed successfully!")
