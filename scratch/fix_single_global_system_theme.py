import os
import re

print("Starting Single Global System Theme Architecture Fix...")

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update <head> inline script: Purge local theme keys and DO NOT read theme from LocalStorage
old_inline_script = """    (function() {
      try {
        ['irem_cache_reservations', 'irem_cache_draft_reservations', 'irem_cache_services', 'irem_cache_venues', 'irem_cache_customers', 'irem_cache_campaigns', 'irem_cache_theme_color', 'irem_cache_selected_theme', 'irem_cache_menu_layout', 'selected_theme', 'theme_color', 'menu_layout'].forEach(function(k) {
          try { localStorage.removeItem(k); } catch(e){}
        });
        var cachedTheme = localStorage.getItem('irem_cache_theme_color') || localStorage.getItem('selected_theme') || localStorage.getItem('theme_color');
        var cachedMenu = localStorage.getItem('irem_cache_menu_layout') || localStorage.getItem('menu_layout');
        if (cachedTheme) {
          document.documentElement.setAttribute('data-ui-theme', cachedTheme);
        }
        if (cachedMenu) {
          document.documentElement.setAttribute('data-menu-layout', cachedMenu);
        }
        if (window.fetchWithRetry) {
          window.fetchWithRetry('/api/system-settings')
            .then(function(r) { return r.json(); })
            .then(function(d) {
              if (d && d.themeColor) document.documentElement.setAttribute('data-ui-theme', d.themeColor);
              if (d && d.menuLayout) document.documentElement.setAttribute('data-menu-layout', d.menuLayout);
            }).catch(function());
        }
      } catch(e) {}
    })();"""

new_inline_script = """    (function() {
      try {
        ['irem_cache_theme_color', 'irem_cache_selected_theme', 'selected_theme', 'theme_color', 'theme', 'irem_cache_menu_layout', 'menu_layout'].forEach(function(k) {
          try { localStorage.removeItem(k); } catch(e){}
        });
        var cachedMenu = localStorage.getItem('irem_cache_menu_layout') || localStorage.getItem('menu_layout');
        if (cachedMenu) {
          document.documentElement.setAttribute('data-menu-layout', cachedMenu);
        }
        var fetchFn = window.fetchWithRetry || window.fetch;
        if (fetchFn) {
          fetchFn('/api/system-settings')
            .then(function(r) { return r.json(); })
            .then(function(d) {
              if (d && d.themeColor) {
                document.documentElement.setAttribute('data-ui-theme', d.themeColor);
                document.documentElement.setAttribute('data-theme', d.themeColor);
              }
              if (d && d.menuLayout) document.documentElement.setAttribute('data-menu-layout', d.menuLayout);
            }).catch(function() {});
        }
      } catch(e) {}
    })();"""

if old_inline_script in content:
    content = content.replace(old_inline_script, new_inline_script)
    print("1. Replaced <head> inline script for single global theme hydration!")
else:
    print("WARNING: Could not find exact old_inline_script snippet!")

# 2. Fix ThemeIcon: Remove local storage reading and DOM mutation side-effect
old_theme_icon = """    function ThemeIcon({ icon, fallbackEmoji, activeTheme, className = "w-4 h-4" }) {
      const domTheme = typeof document !== 'undefined' ? document.documentElement.getAttribute('data-ui-theme') : null;
      const savedTheme = typeof window !== 'undefined' ? (CacheService.get('theme_color') || CacheService.get('selected_theme') || localStorage.getItem('irem_cache_theme_color') || localStorage.getItem('selected_theme')) : null;
      const rawTheme = activeTheme || domTheme || savedTheme || '';

      useEffect(() => {
        if (rawTheme && rawTheme !== 'gold' && rawTheme !== 'classic_gold') {
          document.documentElement.setAttribute('data-ui-theme', rawTheme);
        }
      }, [rawTheme]);"""

new_theme_icon = """    function ThemeIcon({ icon, fallbackEmoji, activeTheme, className = "w-4 h-4" }) {
      const domTheme = typeof document !== 'undefined' ? document.documentElement.getAttribute('data-ui-theme') : null;
      const rawTheme = activeTheme || domTheme || 'gold';"""

if old_theme_icon in content:
    content = content.replace(old_theme_icon, new_theme_icon)
    print("2. Fixed ThemeIcon to remove localStorage theme override and side-effect!")
else:
    print("WARNING: Could not find exact old_theme_icon snippet!")

# 3. Fix App themeColor state initialization
old_app_theme_init = """      const [themeColor, setThemeColor] = useState(() => {
        const domTheme = typeof document !== 'undefined' ? document.documentElement.getAttribute('data-ui-theme') : null;
        const cachedTheme = typeof window !== 'undefined' ? (CacheService.get('theme_color') || CacheService.get('selected_theme')) : null;
        return domTheme || cachedTheme || '';
      });"""

new_app_theme_init = """      const [themeColor, setThemeColor] = useState(() => {
        return (typeof document !== 'undefined' && document.documentElement.getAttribute('data-ui-theme')) || 'gold';
      });"""

if old_app_theme_init in content:
    content = content.replace(old_app_theme_init, new_app_theme_init)
    print("3. Fixed App themeColor state initialization to rely strictly on server DOM attribute!")
else:
    print("WARNING: Could not find exact old_app_theme_init snippet!")

# 4. Fix App themeColor useEffect (remove CacheService.set)
old_app_theme_effect = """      useEffect(() => {
        CacheService.set('theme_color', themeColor);
        CacheService.set('selected_theme', themeColor);
        if (themeColor && themeColor !== 'gold' && themeColor !== 'classic_gold') {
          document.documentElement.setAttribute('data-ui-theme', themeColor);
        } else {
          document.documentElement.removeAttribute('data-ui-theme');
        }
      }, [themeColor]);"""

new_app_theme_effect = """      useEffect(() => {
        if (themeColor && themeColor !== 'gold' && themeColor !== 'classic_gold') {
          document.documentElement.setAttribute('data-ui-theme', themeColor);
          document.documentElement.setAttribute('data-theme', themeColor);
        } else {
          document.documentElement.removeAttribute('data-ui-theme');
          document.documentElement.removeAttribute('data-theme');
        }
      }, [themeColor]);"""

if old_app_theme_effect in content:
    content = content.replace(old_app_theme_effect, new_app_theme_effect)
    print("4. Fixed App themeColor useEffect to update DOM without polluting LocalStorage!")
else:
    print("WARNING: Could not find exact old_app_theme_effect snippet!")

# 5. Fix handleClearCache
old_handle_clear_cache = """      const handleClearCache = () => {
        try {
          const sysKeys = ['theme_color', 'selected_theme', 'cache_enabled', 'current_user', 'roles', 'tab_permissions'];
          Object.keys(localStorage).forEach(key => {
            if (key.startsWith('irem_cache_')) {
              const subKey = key.replace('irem_cache_', '');
              if (!sysKeys.includes(subKey)) {
                localStorage.removeItem(key);
              }
            }
          });
          // Ensure active theme remains active on HTML root attribute
          CacheService.set('theme_color', themeColor);
        } catch (e) {}
      };"""

new_handle_clear_cache = """      const handleClearCache = () => {
        try {
          ['irem_cache_theme_color', 'irem_cache_selected_theme', 'selected_theme', 'theme_color'].forEach(function(k) {
            try { localStorage.removeItem(k); } catch(e){}
          });
          const sysKeys = ['cache_enabled', 'current_user', 'roles', 'tab_permissions'];
          Object.keys(localStorage).forEach(key => {
            if (key.startsWith('irem_cache_')) {
              const subKey = key.replace('irem_cache_', '');
              if (!sysKeys.includes(subKey)) {
                localStorage.removeItem(key);
              }
            }
          });
        } catch (e) {}
      };"""

if old_handle_clear_cache in content:
    content = content.replace(old_handle_clear_cache, new_handle_clear_cache)
    print("5. Fixed handleClearCache to clean up any legacy local theme keys!")
else:
    print("WARNING: Could not find exact old_handle_clear_cache snippet!")

# Save modified index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated index.html successfully!")

# Copy index.html to yonetim.html and dist/index.html
with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Copied to yonetim.html!")

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Copied to dist/index.html!")

print("Single Global System Theme Architecture applied & synced 100%!")
