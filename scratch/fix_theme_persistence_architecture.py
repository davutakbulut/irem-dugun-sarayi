import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update HEAD script (lines 48-67) to support all themes and both storage keys
old_head_script = """  <!-- INSTANT THEME RESTORE SCRIPT (0ms INSTANT PAINT) -->
  <script>
    (function() {
      try {
        var raw = localStorage.getItem('irem_cache_theme_color') || localStorage.getItem('irem_cache_selected_theme') || localStorage.getItem('selected_theme');
        if (raw) {
          var theme = JSON.parse(raw);
          if (theme === 'elite-luxury' || theme === 'obsidian') {
            document.documentElement.setAttribute('data-ui-theme', 'elite-luxury');
          } else if (theme === 'nordic-light') {
            document.documentElement.setAttribute('data-ui-theme', 'nordic-light');
          } else if (theme === 'apple' || theme === 'apple-light') {
            document.documentElement.setAttribute('data-ui-theme', 'apple');
          } else if (theme === 'sapphire-minimal' || theme === 'sapphire_clean' || theme === 'sapphire') {
            document.documentElement.setAttribute('data-ui-theme', 'sapphire-minimal');
          } else if (theme === 'emerald-royal' || theme === 'emerald_royal' || theme === 'emerald') {
            document.documentElement.setAttribute('data-ui-theme', 'emerald-royal');
          } else {
            document.documentElement.removeAttribute('data-ui-theme');
          }
        }
      } catch(e) {}
    })();
  </script>"""

new_head_script = """  <!-- INSTANT THEME RESTORE SCRIPT (0ms INSTANT PAINT - ALL 8 THEMES SUPPORTED) -->
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
        var theme = getVal('irem_cache_theme_color') || getVal('irem_cache_selected_theme') || getVal('theme_color') || getVal('selected_theme');
        if (theme && theme !== 'gold' && theme !== 'classic_gold') {
          document.documentElement.setAttribute('data-ui-theme', theme);
        } else {
          document.documentElement.removeAttribute('data-ui-theme');
        }
      } catch(e) {}
    })();
  </script>"""

if "INSTANT THEME RESTORE SCRIPT" in html:
    # Find beginning and end of head theme script
    start_idx = html.find("<!-- INSTANT THEME RESTORE SCRIPT")
    end_idx = html.find("</script>", start_idx) + 9
    html = html[:start_idx] + new_head_script + html[end_idx:]
    print("Updated HEAD Theme Restore script!")

# 2. Update App component useEffect (lines 4901-4914) to support ALL themes and sync both keys
old_app_effect = """      useEffect(() => {
        CacheService.set('theme_color', themeColor);
        if (themeColor === 'elite-luxury' || themeColor === 'obsidian') {
          document.documentElement.setAttribute('data-ui-theme', 'elite-luxury');
        } else if (themeColor === 'nordic-light') {
          document.documentElement.setAttribute('data-ui-theme', 'nordic-light');
        } else if (themeColor === 'sapphire-minimal' || themeColor === 'sapphire_clean' || themeColor === 'sapphire') {
          document.documentElement.setAttribute('data-ui-theme', 'sapphire-minimal');
        } else if (themeColor === 'emerald-royal' || themeColor === 'emerald_royal' || themeColor === 'emerald') {
          document.documentElement.setAttribute('data-ui-theme', 'emerald-royal');
        } else {
          document.documentElement.removeAttribute('data-ui-theme');
        }
      }, [themeColor]);"""

new_app_effect = """      useEffect(() => {
        CacheService.set('theme_color', themeColor);
        CacheService.set('selected_theme', themeColor);
        if (themeColor && themeColor !== 'gold' && themeColor !== 'classic_gold') {
          document.documentElement.setAttribute('data-ui-theme', themeColor);
        } else {
          document.documentElement.removeAttribute('data-ui-theme');
        }
      }, [themeColor]);"""

if old_app_effect in html:
    html = html.replace(old_app_effect, new_app_effect)
    print("Updated App component theme useEffect!")

# 3. Update MediaComponent theme initialization (around line 1618-1630) to sync HTML data-ui-theme
old_media_theme = """      const domTheme = typeof document !== 'undefined' ? document.documentElement.getAttribute('data-ui-theme') : null;
      const rawTheme = activeTheme || domTheme || (typeof window !== 'undefined' ? (localStorage.getItem('selected_theme') || localStorage.getItem('irem_cache_theme_color')) : 'classic_gold') || 'classic_gold';"""

new_media_theme = """      const domTheme = typeof document !== 'undefined' ? document.documentElement.getAttribute('data-ui-theme') : null;
      const savedTheme = typeof window !== 'undefined' ? (CacheService.get('theme_color') || CacheService.get('selected_theme') || localStorage.getItem('irem_cache_theme_color') || localStorage.getItem('selected_theme')) : null;
      const rawTheme = activeTheme || domTheme || savedTheme || 'classic_gold';

      useEffect(() => {
        if (rawTheme && rawTheme !== 'gold' && rawTheme !== 'classic_gold') {
          document.documentElement.setAttribute('data-ui-theme', rawTheme);
        }
      }, [rawTheme]);"""

if old_media_theme in html:
    html = html.replace(old_media_theme, new_media_theme)
    print("Updated MediaComponent theme useEffect!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html theme persistence architecture successfully!")
