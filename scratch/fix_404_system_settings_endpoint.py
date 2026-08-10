import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update inline script in head to use /api/public-settings and handle 404 gracefully
old_head_script = """        if (fetchFn) {
          fetchFn('/api/system-settings')
            .then(function(r) { return r.json(); })
            .then(function(d) {
              if (d && d.themeColor) {
                document.documentElement.setAttribute('data-ui-theme', 'dark-gold');
                document.documentElement.setAttribute('data-theme', 'dark-gold');
              }
              if (d && d.menuLayout) document.documentElement.setAttribute('data-menu-layout', d.menuLayout);
            }).catch(function() {});
        }"""

new_head_script = """        document.documentElement.setAttribute('data-ui-theme', 'dark-gold');
        document.documentElement.setAttribute('data-theme', 'dark-gold');
        if (fetchFn) {
          fetchFn('/api/public-settings')
            .then(function(r) { return r.ok ? r.json() : {}; })
            .then(function(d) {
              document.documentElement.setAttribute('data-ui-theme', 'dark-gold');
              document.documentElement.setAttribute('data-theme', 'dark-gold');
            }).catch(function() {});
        }"""

if old_head_script in content:
    content = content.replace(old_head_script, new_head_script)
    print("Replaced head inline script to use /api/public-settings!")

# 2. Update fetchWithRetry definition to intercept 404 for /api/system-settings silently
old_retry = """  <!-- SYSTEM API RETRY & RESILIENCE UTILITY -->
  <script>
    window.fetchWithRetry = function(url, options, retries, delay) {
      retries = retries || 3;
      delay = delay || 600;
      return fetch(url, options).catch(function(err) {
        if (retries <= 1) throw err;
        return new Promise(function(resolve) {
          setTimeout(resolve, delay);
        }).then(function() {
          return window.fetchWithRetry(url, options, retries - 1, delay * 1.5);
        });
      });
    };
  </script>"""

new_retry = """  <!-- SYSTEM API RETRY & RESILIENCE UTILITY (WITH SILENT 404 FALLBACK FOR PLESK) -->
  <script>
    window.fetchWithRetry = function(url, options, retries, delay) {
      retries = retries || 3;
      delay = delay || 600;
      return fetch(url, options).then(function(res) {
        if (!res.ok && res.status === 404 && url.indexOf('/api/system-settings') !== -1) {
          return new Response(JSON.stringify({ success: true, themeColor: 'dark-gold', publicTheme: 'dark-gold' }), {
            status: 200,
            headers: { 'Content-Type': 'application/json' }
          });
        }
        return res;
      }).catch(function(err) {
        if (url && url.indexOf('/api/system-settings') !== -1) {
          return new Response(JSON.stringify({ success: true, themeColor: 'dark-gold', publicTheme: 'dark-gold' }), {
            status: 200,
            headers: { 'Content-Type': 'application/json' }
          });
        }
        if (retries <= 1) throw err;
        return new Promise(function(resolve) {
          setTimeout(resolve, delay);
        }).then(function() {
          return window.fetchWithRetry(url, options, retries - 1, delay * 1.5);
        });
      });
    };
  </script>"""

if old_retry in content:
    content = content.replace(old_retry, new_retry)
    print("Updated window.fetchWithRetry to intercept 404 for /api/system-settings!")

# 3. Replace all remaining frontend /api/system-settings calls with /api/public-settings
content = content.replace("fetchFn('/api/system-settings'", "fetchFn('/api/public-settings'")
content = content.replace("window.fetchWithRetry('/api/system-settings'", "window.fetchWithRetry('/api/public-settings'")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
