import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update App component themeColor useState to synchronously read DOM data-ui-theme attribute on Frame 0
old_app_state = """const [themeColor, setThemeColor] = useState(() => {
        const domTheme = typeof document !== 'undefined' ? document.documentElement.getAttribute('data-ui-theme') : null;
        if (domTheme) return domTheme;
        return CacheService.get('theme_color', 'nordic-light');
      });"""

new_app_state = """const [themeColor, setThemeColor] = useState(() => {
        const domTheme = typeof document !== 'undefined' ? document.documentElement.getAttribute('data-ui-theme') : null;
        const cachedTheme = CacheService.get('theme_color') || CacheService.get('selected_theme');
        return domTheme || cachedTheme || 'nordic-light';
      });"""

if old_app_state in html:
    html = html.replace(old_app_state, new_app_state)
    print("Updated App component themeColor initial state for 0ms zero-flicker paint!")

# 2. Update SettingsPage draftTheme useState to synchronously read DOM data-ui-theme attribute on Frame 0
old_settings_state = "const [draftTheme, setDraftTheme] = useState(themeColor || 'gold');"

new_settings_state = """const [draftTheme, setDraftTheme] = useState(() => {
        const domTheme = typeof document !== 'undefined' ? document.documentElement.getAttribute('data-ui-theme') : null;
        return themeColor || domTheme || 'nordic-light';
      });"""

if old_settings_state in html:
    html = html.replace(old_settings_state, new_settings_state)
    print("Updated SettingsPage draftTheme initial state for 0ms zero-flicker paint!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html zero-flicker theme initialization successfully!")
