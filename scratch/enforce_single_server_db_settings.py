import json
import sys

# 1. Ensure db_system_settings.json has both themeColor and menuLayout
db_path = 'scratch/db_system_settings.json'
try:
    with open(db_path, 'r', encoding='utf-8') as f:
        db_data = json.load(f)
except Exception:
    db_data = {}

db_data['themeColor'] = db_data.get('themeColor', 'nordic-light')
db_data['menuLayout'] = db_data.get('menuLayout', 'vertical')

with open(db_path, 'w', encoding='utf-8') as f:
    json.dump(db_data, f, indent=2)

print("Verified db_system_settings.json with themeColor and menuLayout!")

# 2. Refactor index.html: Remove all localStorage fallbacks for menuLayout & themeColor
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace menuLayout state initialization in App
old_menu_init = """const [menuLayout, setMenuLayout] = useState(() => {
        const domMenu = typeof document !== 'undefined' ? document.documentElement.getAttribute('data-menu-layout') : null;
        const saved = typeof window !== 'undefined' ? localStorage.getItem('irem_menu_layout') : null;
        return domMenu || saved || 'vertical';
      });"""

new_menu_init = """const [menuLayout, setMenuLayout] = useState(() => {
        return (typeof document !== 'undefined' && document.documentElement.getAttribute('data-menu-layout')) || 'vertical';
      });"""

if old_menu_init in html:
    html = html.replace(old_menu_init, new_menu_init)
    print("Cleaned menuLayout state initialization in App!")

# Replace toggleMenuLayout function to send POST /api/system-settings directly
old_toggle_menu = """      const toggleMenuLayout = (forcedLayout) => {
        const newLayout = forcedLayout || (menuLayout === 'vertical' ? 'horizontal' : 'vertical');
        localStorage.setItem('irem_menu_layout', newLayout);
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
        } catch(e) {}
      };"""

new_toggle_menu = """      const toggleMenuLayout = (forcedLayout) => {
        const newLayout = forcedLayout || (menuLayout === 'vertical' ? 'horizontal' : 'vertical');
        setMenuLayout(newLayout);
        if (typeof document !== 'undefined') {
          document.documentElement.setAttribute('data-menu-layout', newLayout);
        }
        try {
          fetch('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ menuLayout: newLayout, updatedAt: new Date().toISOString(), updatedBy: 'admin' })
          }).then(r => r.json()).then(data => {
            if (data.status === 'ok') {
              console.log('✅ Menu Layout updated in server DB:', newLayout);
            }
          }).catch(() => {});
        } catch(e) {}
      };"""

if old_toggle_menu in html:
    html = html.replace(old_toggle_menu, new_toggle_menu)
    print("Cleaned toggleMenuLayout to rely strictly on server DB!")

# Update HEAD Instant Restore Script in index.html to read DOM attributes ONLY
old_head = """  <!-- INSTANT THEME RESTORE SCRIPT (READS DIRECTLY FROM SERVER INJECTED DOM ATTRIBUTE) -->
  <script>
    (function() {
      try {
        var domTheme = document.documentElement.getAttribute('data-ui-theme');
        if (domTheme) return; // Server already injected active theme into HTML!
        var getVal = function(k) {
          try {
            var v = localStorage.getItem(k);
            if (!v) return null;
            if (v.startsWith('"') || v.startsWith('{') || v.startsWith('[')) return JSON.parse(v);
            return v;
          } catch(e) { return localStorage.getItem(k); }
        };
        var theme = getVal('irem_cache_theme_color') || getVal('selected_theme');
        if (theme) {
          document.documentElement.setAttribute('data-ui-theme', theme);
        }
      } catch(e) {}
    })();
  </script>"""

new_head = """  <!-- INSTANT SYSTEM SETTINGS RESTORE SCRIPT (100% SERVER DB DOM INJECTED) -->
  <script>
    (function() {
      try {
        // Synchronously check server-injected DOM attributes on HTML element
        var domTheme = document.documentElement.getAttribute('data-ui-theme');
        var domMenu = document.documentElement.getAttribute('data-menu-layout');
        if (!domTheme || !domMenu) {
          fetch('/api/system-settings')
            .then(function(r) { return r.json(); })
            .then(function(d) {
              if (d.themeColor && !domTheme) document.documentElement.setAttribute('data-ui-theme', d.themeColor);
              if (d.menuLayout && !domMenu) document.documentElement.setAttribute('data-menu-layout', d.menuLayout);
            }).catch(function() {});
        }
      } catch(e) {}
    })();
  </script>"""

if old_head in html:
    html = html.replace(old_head, new_head)
    print("Updated HEAD Instant Restore script for 100% server DB enforcement!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html single server DB settings architecture successfully!")
