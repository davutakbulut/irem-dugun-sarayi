import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update TAB_PERMISSIONS['mind-map'] to ['admin']
html = html.replace(
    "'mind-map': ['admin', 'satisci', 'sosyal_medyaci', 'musteri'],",
    "'mind-map': ['admin'],"
)

# 2. Update tabPermissionsState initialization to enforce 'mind-map': ['admin']
old_state_init = "const [tabPermissionsState, setTabPermissionsState] = useState(() => CacheService.get('tab_permissions', TAB_PERMISSIONS));"
new_state_init = """const [tabPermissionsState, setTabPermissionsState] = useState(() => {
        const cached = CacheService.get('tab_permissions', TAB_PERMISSIONS);
        return { ...cached, 'mind-map': ['admin'] };
      });"""

html = html.replace(old_state_init, new_state_init)

# 3. Remove duplicate mind-map from YÖNETİM & AYARLAR group in sidebar
# In sidebar, YÖNETİM & AYARLAR group has items: [ { id: 'mind-map', ... }, { id: 'users', ... }, { id: 'settings', ... } ]
old_dup_line = "                        { id: 'mind-map', label: 'Zihin Haritası (MindMap)', icon: 'sparkles', fallbackEmoji: '🧠', badge: 'YENİ' },\n                        { id: 'users', label: 'Kullanıcı Yönetimi'"
new_dup_line = "                        { id: 'users', label: 'Kullanıcı Yönetimi'"

if old_dup_line in html:
    html = html.replace(old_dup_line, new_dup_line)
    print("Removed duplicate mind-map from YÖNETİM & AYARLAR in index.html")
else:
    print("Could not find exact duplicate line in index.html, checking alternative...")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html successfully!")
