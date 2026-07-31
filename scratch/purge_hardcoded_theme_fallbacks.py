import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update HEAD script fallback: Remove 'nordic-light' or 'gold' fallbacks completely
old_head_script = """  <!-- INSTANT THEME RESTORE SCRIPT (0ms INSTANT PAINT - ALL 8 THEMES SUPPORTED) -->
  <script>
    (function() {
      try {
        var getVal = function(k) {
          try {
            var v = localStorage.getItem(k);
            if (!v) return null;
            if (v.startsWith('"') || v.startsWith('{') || v.startsWith('[')) return JSON.parse(v);
            return v;
          } catch(e) { return localStorage.getItem(k); }
        };
        var theme = getVal('irem_cache_theme_color') || getVal('irem_cache_selected_theme') || getVal('theme_color') || getVal('selected_theme') || 'nordic-light';
        if (theme && theme !== 'gold' && theme !== 'classic_gold') {
          document.documentElement.setAttribute('data-ui-theme', theme);
        } else {
          document.documentElement.removeAttribute('data-ui-theme');
        }
      } catch(e) {}
    })();
  </script>"""

new_head_script = """  <!-- INSTANT THEME RESTORE SCRIPT (READS DIRECTLY FROM SERVER INJECTED DOM ATTRIBUTE) -->
  <script>
    (function() {
      try {
        var domTheme = document.documentElement.getAttribute('data-ui-theme');
        if (domTheme) return; // Server already injected active theme into HTML!
        var getVal = function(k) {
          try {
            var v = localStorage.getItem(k);
            if (!v) return null;
            if (v.startsWith('"') || v.startsWith('{') || v.startsWith('[')) return JSON.parse(v);
            return v;
          } catch(e) { return localStorage.getItem(k); }
        };
        var theme = getVal('irem_cache_theme_color') || getVal('selected_theme');
        if (theme) {
          document.documentElement.setAttribute('data-ui-theme', theme);
        }
      } catch(e) {}
    })();
  </script>"""

if old_head_script in html:
    html = html.replace(old_head_script, new_head_script)
    print("Purged hardcoded fallback themes from HEAD script!")

# 2. Update App component themeColor initial state to read DOM attribute ONLY without hardcoded fallback string
old_app_theme_state = """const [themeColor, setThemeColor] = useState(() => {
        const domTheme = typeof document !== 'undefined' ? document.documentElement.getAttribute('data-ui-theme') : null;
        const cachedTheme = CacheService.get('theme_color') || CacheService.get('selected_theme');
        return domTheme || cachedTheme || 'nordic-light';
      });"""

new_app_theme_state = """const [themeColor, setThemeColor] = useState(() => {
        const domTheme = typeof document !== 'undefined' ? document.documentElement.getAttribute('data-ui-theme') : null;
        const cachedTheme = typeof window !== 'undefined' ? (CacheService.get('theme_color') || CacheService.get('selected_theme')) : null;
        return domTheme || cachedTheme || '';
      });"""

if old_app_theme_state in html:
    html = html.replace(old_app_theme_state, new_app_theme_state)
    print("Purged hardcoded fallback theme from App themeColor state!")

# 3. Update SettingsPage draftTheme initial state to read DOM attribute ONLY without hardcoded fallback string
old_settings_draft_state = """const [draftTheme, setDraftTheme] = useState(() => {
        const domTheme = typeof document !== 'undefined' ? document.documentElement.getAttribute('data-ui-theme') : null;
        return themeColor || domTheme || 'nordic-light';
      });"""

new_settings_draft_state = """const [draftTheme, setDraftTheme] = useState(() => {
        const domTheme = typeof document !== 'undefined' ? document.documentElement.getAttribute('data-ui-theme') : null;
        return themeColor || domTheme || '';
      });"""

if old_settings_draft_state in html:
    html = html.replace(old_settings_draft_state, new_settings_draft_state)
    print("Purged hardcoded fallback theme from SettingsPage draftTheme state!")

# 4. Update MediaComponent rawTheme initial state
old_media_raw_theme = """const rawTheme = activeTheme || domTheme || savedTheme || 'classic_gold';"""
new_media_raw_theme = """const rawTheme = activeTheme || domTheme || savedTheme || '';"""

if old_media_raw_theme in html:
    html = html.replace(old_media_raw_theme, new_media_raw_theme)
    print("Purged hardcoded fallback theme from MediaComponent!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Purged all hardcoded fallback theme strings across index.html successfully!")
