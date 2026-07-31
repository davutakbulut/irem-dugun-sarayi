import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update SLUG_TO_TAB to include 'medya' -> 'media' and 'm' -> 'media'
old_slug_map = "const SLUG_TO_TAB = {"
new_slug_map = """const SLUG_TO_TAB = {
      'medya': 'media',
      'm': 'media',"""

if old_slug_map in html and "'medya': 'media'" not in html:
    html = html.replace(old_slug_map, new_slug_map)
    print("Added 'medya' and 'm' to SLUG_TO_TAB map!")

# 2. Update hashToTab to recognize #/medya/:key and #/m/:key routes
old_hash_to_tab = "const tab = (slug === 'anasayfa' ? 'dashboard' : (SLUG_TO_TAB[slug] || 'simulasyon-404'));"
new_hash_to_tab = """let targetTab = 'simulasyon-404';
      if (slug === 'anasayfa') {
        targetTab = 'dashboard';
      } else if (cleanHash.startsWith('medya/') || cleanHash.startsWith('m/')) {
        targetTab = 'media';
      } else {
        targetTab = SLUG_TO_TAB[slug] || 'simulasyon-404';
      }
      const tab = targetTab;"""

if old_hash_to_tab in html:
    html = html.replace(old_hash_to_tab, new_hash_to_tab)
    print("Updated hashToTab to match #/medya/:key and #/m/:key routes!")

# 3. Update RBAC guard in App component to BYPASS permission check when isPublicGuestRoute is true
old_rbac_guard = ") : !(activeRole === 'admin' || (tabPermissionsState[activeTab] || tabPermissionsState[activeTab.split('-')[0]] || ['admin']).includes(activeRole)) ? ("
new_rbac_guard = ") : (!isPublicGuestRoute && !(activeRole === 'admin' || (tabPermissionsState[activeTab] || tabPermissionsState[activeTab.split('-')[0]] || ['admin']).includes(activeRole))) ? ("

if old_rbac_guard in html:
    html = html.replace(old_rbac_guard, new_rbac_guard)
    print("Bypassed RBAC permission check for isPublicGuestRoute in App component!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html incognito 404 fix successfully!")
