import json
import re
import sys

# 1. Update serve_fast_3g.py do_POST to MERGE incoming JSON with existing db_system_settings.json
with open('scratch/serve_fast_3g.py', 'r', encoding='utf-8') as f:
    py_code = f.read()

old_post_handler = """        if parsed_path.path in ['/api/system-settings', '/api/system-config']:
            try:
                content_len = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_len)
                data = json.loads(body.decode('utf-8'))
                
                db_file = os.path.join(os.path.dirname(__file__), 'db_system_settings.json')
                existing = {}
                if os.path.exists(db_file):
                    try:
                        with open(db_file, 'r', encoding='utf-8') as f:
                            existing = json.load(f)
                    except Exception: pass
                
                existing.update(data)
                
                with open(db_file, 'w', encoding='utf-8') as f:
                    json.dump(existing, f, indent=2)"""

if old_post_handler not in py_code:
    # Rewrite do_POST in serve_fast_3g.py to ensure merging of existing settings
    py_code = re.sub(
        r'if parsed_path\.path in \[\'/api/system-settings\', \'/api/system-config\'\]:.*?(?=self\.send_response)',
        """if parsed_path.path in ['/api/system-settings', '/api/system-config']:
            try:
                content_len = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_len)
                data = json.loads(body.decode('utf-8'))
                
                db_file = os.path.join(os.path.dirname(__file__), 'db_system_settings.json')
                existing = {}
                if os.path.exists(db_file):
                    try:
                        with open(db_file, 'r', encoding='utf-8') as f:
                            existing = json.load(f)
                    except Exception: pass
                
                existing.update(data)
                
                with open(db_file, 'w', encoding='utf-8') as f:
                    json.dump(existing, f, indent=2)
                """,
        py_code,
        flags=re.DOTALL
    )

with open('scratch/serve_fast_3g.py', 'w', encoding='utf-8') as f:
    f.write(py_code)

print("Updated serve_fast_3g.py to merge system settings on POST!")

# 2. Update index.html: Connect handleMenuLayoutChange and Settings page save to send BOTH themeColor and menuLayout to POST /api/system-settings
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace handleMenuLayoutChange in App (lines 5232-5238)
old_menu_change = """      const handleMenuLayoutChange = (newLayout) => {
        setMenuLayout(newLayout);
        try {
          localStorage.setItem('irem_menu_layout', newLayout);
        } catch(e) {}
        showToast(`Menü Düzeni Değiştirildi: ${newLayout === 'horizontal' ? 'Yatay Üst Menü ══' : 'Dikey Sol Menü 📌'}`);
      };"""

new_menu_change = """      const handleMenuLayoutChange = (newLayout) => {
        setMenuLayout(newLayout);
        if (typeof document !== 'undefined') {
          document.documentElement.setAttribute('data-menu-layout', newLayout);
        }
        try {
          localStorage.setItem('irem_menu_layout', newLayout);
          fetch('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ themeColor, menuLayout: newLayout, updatedAt: new Date().toISOString(), updatedBy: 'admin' })
          }).catch(() => {});
        } catch(e) {}
        showToast(`Menü Düzeni Değiştirildi: ${newLayout === 'horizontal' ? 'Yatay Üst Menü ══' : 'Dikey Sol Menü 📌'}`);
      };"""

if old_menu_change in html:
    html = html.replace(old_menu_change, new_menu_change)
    print("Connected handleMenuLayoutChange to POST /api/system-settings!")

# Replace menuLayout initial state in App (line 5226)
old_menu_init = """      const [menuLayout, setMenuLayout] = useState(() => {
        try {
          return localStorage.getItem('irem_menu_layout') || 'vertical';
        } catch(e) { return 'vertical'; }
      });"""

new_menu_init = """      const [menuLayout, setMenuLayout] = useState(() => {
        const domMenu = typeof document !== 'undefined' ? document.documentElement.getAttribute('data-menu-layout') : null;
        try {
          return domMenu || localStorage.getItem('irem_menu_layout') || 'vertical';
        } catch(e) { return domMenu || 'vertical'; }
      });"""

if old_menu_init in html:
    html = html.replace(old_menu_init, new_menu_init)
    print("Connected menuLayout initial state in App to DOM attribute!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html menu and theme combined save successfully!")
