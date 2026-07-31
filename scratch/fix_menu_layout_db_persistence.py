import json
import sys

# 1. Update scratch/db_system_settings.json to include menuLayout
db_path = 'scratch/db_system_settings.json'
try:
    with open(db_path, 'r', encoding='utf-8') as f:
        db_data = json.load(f)
except Exception:
    db_data = {}

db_data['menuLayout'] = db_data.get('menuLayout', 'vertical')

with open(db_path, 'w', encoding='utf-8') as f:
    json.dump(db_data, f, indent=2)

print("Updated db_system_settings.json with menuLayout property!")

# 2. Update index.html menuLayout state and toggle handler to sync with POST /api/system-settings
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_menu_state = """        const saved = localStorage.getItem('irem_menu_layout');
        return saved || 'vertical';"""

new_menu_state = """        const domMenu = typeof document !== 'undefined' ? document.documentElement.getAttribute('data-menu-layout') : null;
        const saved = typeof window !== 'undefined' ? localStorage.getItem('irem_menu_layout') : null;
        return domMenu || saved || 'vertical';"""

if old_menu_state in html:
    html = html.replace(old_menu_state, new_menu_state)
    print("Updated menuLayout initial state to read DOM attribute first!")

old_menu_toggle = """        localStorage.setItem('irem_menu_layout', newLayout);
        setMenuLayout(newLayout);"""

new_menu_toggle = """        localStorage.setItem('irem_menu_layout', newLayout);
        setMenuLayout(newLayout);
        if (typeof document !== 'undefined') {
          document.documentElement.setAttribute('data-menu-layout', newLayout);
        }
        try {
          fetch('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ menuLayout: newLayout, updatedAt: new Date().toISOString(), updatedBy: 'admin' })
          }).catch(() => {});
        } catch(e) {}"""

if old_menu_toggle in html:
    html = html.replace(old_menu_toggle, new_menu_toggle)
    print("Updated menuLayout toggle handler to POST menuLayout to /api/system-settings backend DB!")

# Update App mount effect to sync menuLayout from /api/system-settings
old_system_fetch = """              if (data && data.themeColor) {
                setThemeColor(data.themeColor);
                if (data.themeColor !== 'gold' && data.themeColor !== 'classic_gold') {
                  document.documentElement.setAttribute('data-ui-theme', data.themeColor);
                } else {
                  document.documentElement.removeAttribute('data-ui-theme');
                }
              }"""

new_system_fetch = """              if (data) {
                if (data.themeColor) {
                  setThemeColor(data.themeColor);
                  if (data.themeColor !== 'gold' && data.themeColor !== 'classic_gold') {
                    document.documentElement.setAttribute('data-ui-theme', data.themeColor);
                  } else {
                    document.documentElement.removeAttribute('data-ui-theme');
                  }
                }
                if (data.menuLayout) {
                  setMenuLayout(data.menuLayout);
                  if (typeof document !== 'undefined') {
                    document.documentElement.setAttribute('data-menu-layout', data.menuLayout);
                  }
                }
              }"""

if old_system_fetch in html:
    html = html.replace(old_system_fetch, new_system_fetch)
    print("Updated App mount system settings fetch to sync menuLayout!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html menu layout server DB persistence successfully!")
