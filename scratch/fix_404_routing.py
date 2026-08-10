import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_route_block = """      } else if (pathname.startsWith('/yonetim')) {
        let sub = pathname.replace(/^\/yonetim\/?/, '').split('?')[0].replace(/\/$/, '');
        if (!sub && routePart) sub = routePart.split('?')[0];
        targetTab = SLUG_TO_TAB[sub] || 'dashboard';
        slug = sub || 'dashboard';
      } else {"""

new_route_block = """      } else if (pathname.startsWith('/yonetim')) {
        let sub = pathname.replace(/^\/yonetim\/?/, '').split('?')[0].replace(/\/$/, '');
        if (!sub && routePart) sub = routePart.split('?')[0];
        if (!sub || sub === '') {
          targetTab = 'dashboard';
          slug = 'dashboard';
        } else if (SLUG_TO_TAB[sub]) {
          targetTab = SLUG_TO_TAB[sub];
          slug = sub;
        } else {
          targetTab = 'simulasyon-404';
          slug = '404';
        }
      } else {"""

if old_route_block in content:
    content = content.replace(old_route_block, new_route_block)
    print("1. Successfully updated parseHashRoute to send invalid /yonetim sub-paths to 404!")
else:
    print("WARNING: Could not find old_route_block in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
