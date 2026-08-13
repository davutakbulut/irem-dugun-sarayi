import os

# 1. FIX server.js POST Fallback Middleware
with open('server.js', 'r', encoding='utf-8') as f:
    server_code = f.read()

old_middleware = """// POST Fallback Middleware for DELETE actions (Prevents 403 Forbidden on Plesk / IIS / ModSecurity WAF)
app.use((req, res, next) => {
  if (req.method === 'POST') {
    const overrideMethod = req.headers['x-http-method-override'] || req.headers['x-method-override'];
    if (overrideMethod === 'DELETE') {
      req.method = 'DELETE';
    } else if (req.url.includes('/delete/')) {
      req.url = req.url.replace('/delete/', '/');
      req.method = 'DELETE';
    } else if (req.url.endsWith('-delete')) {
      req.url = req.url.replace(/-delete$/, '');
      req.method = 'DELETE';
    }
  }
  next();
});"""

new_middleware = """// POST Fallback Middleware for DELETE actions (Prevents 403 Forbidden on Plesk / IIS / ModSecurity WAF)
app.use((req, res, next) => {
  if (req.method === 'POST') {
    const overrideMethod = req.headers['x-http-method-override'] || req.headers['x-method-override'];
    if (overrideMethod === 'DELETE') {
      req.method = 'DELETE';
    }
  }
  next();
});"""

if old_middleware in server_code:
    server_code = server_code.replace(old_middleware, new_middleware)

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(server_code)

print("Successfully updated server.js middleware!")

# 2. UPDATE Google Fonts URL in HTML files
html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

old_fonts_url = 'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400;1,600&display=swap'
new_fonts_url = 'https://fonts.googleapis.com/css2?family=Outfit:wght@300..800&family=Plus+Jakarta+Sans:ital,wght@0,300..800;1,400;1,600&display=swap'

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_fonts_url in content:
        content = content.replace(old_fonts_url, new_fonts_url)
        with open(h_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully updated Google Fonts URL in {h_file}!")

print("All fixes applied successfully!")
