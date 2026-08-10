import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_guard = """      // 1. ROUTE CLASSIFICATION & DOMAIN GUARD
      const pathname = typeof window !== 'undefined' ? (window.location.pathname || '/').toLowerCase() : '/';
      const isMediaRoute = pathname.startsWith('/medya') || pathname.startsWith('/m/') || activeTab === 'media';
      const isManagementRoute = pathname.startsWith('/yonetim') || pathname === '/giris' || pathname === '/login';
      const isPublicMarketingRoute = !isManagementRoute && !isMediaRoute;"""

new_guard = """      // 1. ROUTE CLASSIFICATION & DOMAIN GUARD
      const pathname = typeof window !== 'undefined' ? (window.location.pathname || '/').toLowerCase() : '/';
      const isErrorRoute = activeTab === 'simulasyon-404' || activeTab === '404' || activeTab === 'simulasyon-301' || activeTab === '301' || activeTab === 'simulasyon-403' || activeTab === '403' || activeTab === 'simulasyon-500' || activeTab === '500';
      const isMediaRoute = pathname.startsWith('/medya') || pathname.startsWith('/m/') || activeTab === 'media';
      const isManagementRoute = (pathname.startsWith('/yonetim') || pathname === '/giris' || pathname === '/login') && !isErrorRoute;
      const isPublicMarketingRoute = !isManagementRoute && !isMediaRoute && !isErrorRoute;"""

if old_guard in content:
    content = content.replace(old_guard, new_guard)
    print("1. Updated route classification to classify error routes as public/bypassed.")
else:
    print("WARNING: Could not find old_guard in index.html!")

old_login_guard = "if (isManagementRoute && !sessionUser && !isMediaRoute) {"
new_login_guard = "if (isManagementRoute && !sessionUser && !isMediaRoute && !isErrorRoute) {"

if old_login_guard in content:
    content = content.replace(old_login_guard, new_login_guard)
    print("2. Updated management login guard to skip error routes.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
