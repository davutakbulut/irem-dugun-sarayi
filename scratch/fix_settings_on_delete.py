import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix SettingsComponent signature to include onEditRole and onDeleteRole
old_sig = """    function SettingsComponent({
      activeRole,
      roles,
      tabPermissions,
      onAddRole,
      onToggleTabPermission,"""

new_sig = """    function SettingsComponent({
      activeRole,
      roles,
      tabPermissions,
      onAddRole,
      onEditRole,
      onDeleteRole,
      onToggleTabPermission,"""

if old_sig in html:
    html = html.replace(old_sig, new_sig)
    print("Fixed SettingsComponent parameter signature to include onEditRole and onDeleteRole")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html successfully!")
