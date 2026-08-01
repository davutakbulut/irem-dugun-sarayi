import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix 1: Add system-guide to TAB_PERMISSIONS
old_tab_perm = "      'mind-map': ['admin']\n    };"
new_tab_perm = "      'mind-map': ['admin'],\n      'system-guide': ['admin', 'manager', 'editor', 'staff']\n    };"

if old_tab_perm in html:
    html = html.replace(old_tab_perm, new_tab_perm)
    print("Added system-guide to TAB_PERMISSIONS successfully!")

# Fix 2: Add system-guide to tabPermissionsState initial state
old_perm_state = "return { ...cached, 'mind-map': ['admin'] };"
new_perm_state = "return { ...cached, 'mind-map': ['admin'], 'system-guide': ['admin', 'manager', 'editor', 'staff'] };"

if old_perm_state in html:
    html = html.replace(old_perm_state, new_perm_state)
    print("Added system-guide to tabPermissionsState initial state successfully!")

# Fix 3: Add TAB_TO_SLUG for system-guide
old_tab_slug = "      'mind-map': 'zihin-haritasi',\n      'settings': 'ayarlar'"
new_tab_slug = "      'mind-map': 'zihin-haritasi',\n      'system-guide': 'sistem-kilavuzu',\n      'settings': 'ayarlar'"

if old_tab_slug in html:
    html = html.replace(old_tab_slug, new_tab_slug)
    print("Added TAB_TO_SLUG for system-guide successfully!")

# Fix 4: Add SLUG_TO_TAB mappings for sistem-kilavuzu
old_slug_tab = "      'mindmap': 'mind-map',\n      'ayarlar': 'settings',"
new_slug_tab = "      'mindmap': 'mind-map',\n      'sistem-kilavuzu': 'system-guide',\n      'kilavuz': 'system-guide',\n      'system-guide': 'system-guide',\n      'ayarlar': 'settings',"

if old_slug_tab in html:
    html = html.replace(old_slug_tab, new_slug_tab)
    print("Added SLUG_TO_TAB mappings for sistem-kilavuzu successfully!")

# Fix 5: Render SystemGuidePageComponent inside App main content area
old_app_render = "{activeTab === 'mind-map' && <MindMapComponent navigateTo={handleNavigate} activeRole={activeRole} showToast={showToast} themeColor={themeColor} menuLayout={menuLayout} />}"
new_app_render = "{activeTab === 'mind-map' && <MindMapComponent navigateTo={handleNavigate} activeRole={activeRole} showToast={showToast} themeColor={themeColor} menuLayout={menuLayout} />}\n          {activeTab === 'system-guide' && <SystemGuidePageComponent navigateTo={handleNavigate} activeRole={activeRole} themeColor={themeColor} menuLayout={menuLayout} />}"

if old_app_render in html:
    html = html.replace(old_app_render, new_app_render)
    print("Added SystemGuidePageComponent rendering inside App main content area successfully!")
else:
    print("Could not find old_app_render in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html SystemGuidePageComponent route, permissions, and menu fixes successfully!")
