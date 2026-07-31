import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update App component initial state for themeColor so it checks DOM attribute first and defaults to 'nordic-light' instead of 'gold'
old_app_state = "const [themeColor, setThemeColor] = useState(() => CacheService.get('theme_color', 'gold'));"

new_app_state = """const [themeColor, setThemeColor] = useState(() => {
        const domTheme = typeof document !== 'undefined' ? document.documentElement.getAttribute('data-ui-theme') : null;
        if (domTheme) return domTheme;
        return CacheService.get('theme_color', 'nordic-light');
      });"""

if old_app_state in html:
    html = html.replace(old_app_state, new_app_state)
    print("Fixed App component themeColor initial state to read DOM attribute and default to nordic-light!")

# 2. Update initial HEAD script fallback from gold to nordic-light if no cache exists
old_head_script_fallback = "var theme = getVal('irem_cache_theme_color') || getVal('irem_cache_selected_theme') || getVal('theme_color') || getVal('selected_theme');"
new_head_script_fallback = "var theme = getVal('irem_cache_theme_color') || getVal('irem_cache_selected_theme') || getVal('theme_color') || getVal('selected_theme') || 'nordic-light';"

if old_head_script_fallback in html:
    html = html.replace(old_head_script_fallback, new_head_script_fallback)
    print("Fixed Head script theme fallback to nordic-light!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html cleared history theme race condition fix successfully!")
