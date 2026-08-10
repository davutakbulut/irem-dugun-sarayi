import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update parseHashRoute to catch unrecognized routeParts on root as public-404
old_parse_hash = """        } else if (routePart === 'musteri-giris') {
          targetTab = 'public-customer-login';
          slug = 'musteri-giris';
        } else {
          targetTab = 'public-home';
          slug = '';
        }"""

new_parse_hash = """        } else if (routePart === 'musteri-giris') {
          targetTab = 'public-customer-login';
          slug = 'musteri-giris';
        } else if (routePart === '404' || routePart === '500' || routePart === '403') {
          targetTab = 'public-' + routePart;
          slug = routePart;
        } else if (routePart && routePart.length > 0) {
          targetTab = 'public-404';
          slug = '404';
        } else {
          targetTab = 'public-home';
          slug = '';
        }"""

if old_parse_hash in content:
    content = content.replace(old_parse_hash, new_parse_hash)
    print("Updated parseHashRoute to route unknown hash routeParts to public-404!")

# 2. Update renderContent in App component to render NotFoundPage, ServerErrorPage & ForbiddenPage inside PublicLayout
old_public_routes_switch = """          {activeTab === 'public-customer-login' && (
            <PublicLayout currentRoute="/musteri-giris" navigateTo={navigateTo}>
              <CustomerLoginPage navigateTo={navigateTo} />
            </PublicLayout>
          )}"""

new_public_routes_switch = """          {activeTab === 'public-customer-login' && (
            <PublicLayout currentRoute="/musteri-giris" navigateTo={navigateTo}>
              <CustomerLoginPage navigateTo={navigateTo} />
            </PublicLayout>
          )}

          {(activeTab === 'public-404' || activeTab === '404' || activeTab === 'simulasyon-404') && (
            <PublicLayout currentRoute="/404" navigateTo={navigateTo}>
              <NotFoundPage navigateTo={navigateTo} />
            </PublicLayout>
          )}

          {(activeTab === 'public-500' || activeTab === '500' || activeTab === 'simulasyon-500') && (
            <PublicLayout currentRoute="/500" navigateTo={navigateTo}>
              <ServerErrorPage navigateTo={navigateTo} />
            </PublicLayout>
          )}

          {(activeTab === 'public-403' || activeTab === '403' || activeTab === 'simulasyon-403') && (
            <PublicLayout currentRoute="/403" navigateTo={navigateTo}>
              <ForbiddenPage navigateTo={navigateTo} />
            </PublicLayout>
          )}"""

if old_public_routes_switch in content:
    content = content.replace(old_public_routes_switch, new_public_routes_switch)
    print("Updated App router to render themed error pages inside PublicLayout!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
