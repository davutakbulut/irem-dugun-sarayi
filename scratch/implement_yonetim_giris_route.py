import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update PATH_TO_TAB mappings to support 'yonetim/giris'
old_path_to_tab = """      'giris': 'login',
      'login': 'login'"""

new_path_to_tab = """      'giris': 'login',
      'login': 'login',
      'yonetim/giris': 'login',
      'yonetim/login': 'login'"""

if old_path_to_tab in content:
    content = content.replace(old_path_to_tab, new_path_to_tab)
    print("1. Updated PATH_TO_TAB mappings for /yonetim/giris.")

# 2. Update TAB_TO_PATH mapping for 'login' -> '/yonetim/giris'
old_tab_to_path = "'login': '/giris',"
new_tab_to_path = "'login': '/yonetim/giris',"

if old_tab_to_path in content:
    content = content.replace(old_tab_to_path, new_tab_to_path)
    print("2. Updated TAB_TO_PATH for login -> /yonetim/giris.")

# 3. Update handleLogout & navigateTo cleanPath
old_logout = "window.history.pushState({}, '', '/giris');"
new_logout = "window.history.pushState({}, '', '/yonetim/giris');"

if old_logout in content:
    content = content.replace(old_logout, new_logout)
    print("3. Updated handleLogout to pushState /yonetim/giris.")

old_nav_clean = "if (tab === 'login') cleanPath = '/giris';"
new_nav_clean = "if (tab === 'login') cleanPath = '/yonetim/giris';"

if old_nav_clean in content:
    content = content.replace(old_nav_clean, new_nav_clean)
    print("4. Updated navigateTo cleanPath to /yonetim/giris.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
