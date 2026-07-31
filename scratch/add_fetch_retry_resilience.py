import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add fetchWithRetry utility to index.html to seamlessly retry /api/system-settings requests during server restarts
retry_util = """
  <!-- SYSTEM API RETRY & RESILIENCE UTILITY -->
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
  </script>
"""

if 'window.fetchWithRetry' not in html:
    anchor = "</head>"
    idx = html.find(anchor)
    if idx != -1:
        html = html[:idx] + retry_util + "\n" + html[idx:]
        print("Added fetchWithRetry utility to <head> in index.html!")

# Update /api/system-settings fetch calls in index.html to use fetchWithRetry
html = html.replace("fetch('/api/system-settings'", "window.fetchWithRetry('/api/system-settings'")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with API Resilience & Auto-Retry mechanism successfully!")
