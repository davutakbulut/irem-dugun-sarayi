import sys

with open('scratch/build_precompiled.py', 'r', encoding='utf-8') as f:
    py_code = f.read()

old_script_grab = "raw_jsx = scripts[0]"
new_script_grab = "raw_jsx = '\\n\\n'.join(scripts)"

if old_script_grab in py_code:
    py_code = py_code.replace(old_script_grab, new_script_grab)
    print("Updated build_precompiled.py to concatenate ALL babel script blocks!")

with open('scratch/build_precompiled.py', 'w', encoding='utf-8') as f:
    f.write(py_code)

print("Updated build_precompiled.py script successfully!")
