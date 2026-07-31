import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update App component mount effect to IMMEDIATELY apply database theme to DOM data-ui-theme
old_app_mount = """      useEffect(() => {
        try {
          fetch('/api/system-settings')
            .then(res => res.json())
            .then(data => {
              if (data && data.themeColor && data.themeColor !== themeColor) {
                setThemeColor(data.themeColor);
              }
            }).catch(() => {});
        } catch(e) {}
      }, []);"""

new_app_mount = """      useEffect(() => {
        try {
          fetch('/api/system-settings')
            .then(res => res.json())
            .then(data => {
              if (data && data.themeColor) {
                setThemeColor(data.themeColor);
                if (data.themeColor !== 'gold' && data.themeColor !== 'classic_gold') {
                  document.documentElement.setAttribute('data-ui-theme', data.themeColor);
                } else {
                  document.documentElement.removeAttribute('data-ui-theme');
                }
              }
            }).catch(() => {});
        } catch(e) {}
      }, []);"""

if old_app_mount in html:
    html = html.replace(old_app_mount, new_app_mount)
    print("Fixed App component mount effect to force DOM attribute sync with DB!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html DOM/DB theme sync fix successfully!")
