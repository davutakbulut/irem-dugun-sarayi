import os, re

files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for f_path in files:
    if not os.path.exists(f_path):
        continue
    with open(f_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove calls to setActiveRole
    content = content.replace("setActiveRole(sessionUser.role);", "// activeRole is derived from sessionUser.role")
    content = content.replace("setActiveRole(userObj.role || 'admin');", "// activeRole is derived from userObj.role")
    content = content.replace("setActiveRole(newRole);", "// activeRole is derived from session user")
    content = content.replace("setActiveRole,", "")
    content = content.replace("setActiveRole", "null")

    with open(f_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully cleaned up setActiveRole calls from {f_path}!")

print("Cleanup of setActiveRole completed!")
