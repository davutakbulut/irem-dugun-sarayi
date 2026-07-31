import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Clean up checkTheme if misplaced inside printWin.document.write
bad_snippet = """  <!-- THEME DIAGNOSTIC CONSOLE TOOL: Type checkTheme() in browser F12 console -->
  <script>
    window.checkTheme = function() {
      console.log('🔍 SYSTEM THEME DIAGNOSTIC REPORT:');
      console.log('----------------------------------------');
      var domTheme = document.documentElement.getAttribute('data-ui-theme') || 'classic_gold (default)';
      var localTheme = localStorage.getItem('irem_cache_theme_color') || localStorage.getItem('selected_theme') || 'None';
      console.log('1. HTML DOM Attribute (data-ui-theme):', domTheme);
      console.log('2. LocalStorage Cache:', localTheme);
      
      fetch('/api/system-settings')
        .then(r => r.json())
        .then(data => {
          console.log('3. Server Backend DB Theme (/api/system-settings):', data.themeColor || 'Unknown');
          console.log('----------------------------------------');
          if (data.themeColor === domTheme || (domTheme === 'classic_gold (default)' && data.themeColor === 'gold')) {
            console.log('✅ RESULT: THEME IS 100% MATCHED AND PERSISTENT IN BACKEND DB!');
          } else {
            console.warn('⚠️ WARNING: DOM theme does not match Backend DB theme.');
          }
        }).catch(err => console.error('❌ Failed to fetch backend DB theme:', err));
    };
  </script>"""

if bad_snippet in html:
    html = html.replace(bad_snippet, "")
    print("Removed misplaced checkTheme snippet from index.html!")

# Clean checkTheme script to be inserted right after INSTANT THEME RESTORE SCRIPT inside <head>
clean_check_theme = """
  <!-- THEME DIAGNOSTIC CONSOLE TOOL: Type checkTheme() in browser F12 console -->
  <script>
    window.checkTheme = function() {
      console.log('🔍 SYSTEM THEME DIAGNOSTIC REPORT:');
      console.log('----------------------------------------');
      var domTheme = document.documentElement.getAttribute('data-ui-theme') || 'classic_gold (default)';
      var localTheme = localStorage.getItem('irem_cache_theme_color') || localStorage.getItem('selected_theme') || 'None';
      console.log('1. HTML DOM Attribute (data-ui-theme):', domTheme);
      console.log('2. LocalStorage Cache:', localTheme);
      
      fetch('/api/system-settings')
        .then(function(r) { return r.json(); })
        .then(function(data) {
          console.log('3. Server Backend DB Theme (/api/system-settings):', data.themeColor || 'Unknown');
          console.log('----------------------------------------');
          if (data.themeColor === domTheme || (domTheme === 'classic_gold (default)' && data.themeColor === 'gold')) {
            console.log('✅ RESULT: THEME IS 100% MATCHED AND PERSISTENT IN BACKEND DB!');
          } else {
            console.warn('⚠️ WARNING: DOM theme (' + domTheme + ') does not match Backend DB theme (' + data.themeColor + ').');
          }
        }).catch(function(err) { console.error('❌ Failed to fetch backend DB theme:', err); });
    };
  </script>"""

anchor = "<!-- INSTANT THEME RESTORE SCRIPT"
if anchor in html and "window.checkTheme" not in html:
    # Insert right after INSTANT THEME RESTORE SCRIPT block
    end_of_restore = html.find("</script>", html.find(anchor)) + 9
    html = html[:end_of_restore] + "\n" + clean_check_theme + html[end_of_restore:]
    print("Inserted clean checkTheme script into <head> in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html checkTheme location fix successfully!")
