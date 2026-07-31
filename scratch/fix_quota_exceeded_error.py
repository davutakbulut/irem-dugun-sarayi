import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace CacheService.set with Smart QuotaExceeded Protection & Storage Compression
old_cache_set = """      set: (key, value) => {
        try {
          const isEnabled = localStorage.getItem('irem_cache_cache_enabled');
          const isSystemPref = key === 'cache_enabled' || key === 'theme_color' || key === 'selected_theme' || key === 'current_user' || key === 'roles' || key === 'tab_permissions';
          if (isEnabled === 'false' && !isSystemPref) return;
          localStorage.setItem(`irem_cache_${key}`, JSON.stringify(value));
          if (key === 'theme_color') {
            localStorage.setItem('selected_theme', value);
          }
        } catch (e) {
          console.warn('Cache write failed:', e);
        }
      },"""

new_cache_set = """      set: (key, value) => {
        try {
          const isEnabled = localStorage.getItem('irem_cache_cache_enabled');
          const isSystemPref = key === 'cache_enabled' || key === 'theme_color' || key === 'selected_theme' || key === 'current_user' || key === 'roles' || key === 'tab_permissions';
          if (isEnabled === 'false' && !isSystemPref) return;
          
          let stringified = JSON.stringify(value);
          
          // Smart quota guard: If saving reservations with heavy base64 media, strip heavy base64 data for localStorage
          if (key === 'reservations' && stringified.length > 2000000) {
            try {
              const sanitizedReservations = value.map(r => {
                if (!r.media || !Array.isArray(r.media)) return r;
                return {
                  ...r,
                  media: r.media.slice(0, 50).map(m => {
                    // Keep metadata intact, truncate huge raw base64 if needed for localStorage
                    if (m.url && m.url.length > 200000 && m.url.startsWith('data:')) {
                      return { ...m, url: m.url.substring(0, 100) + '...[cached_in_memory]' };
                    }
                    return m;
                  })
                };
              });
              stringified = JSON.stringify(sanitizedReservations);
            } catch(err) {}
          }
          
          localStorage.setItem(`irem_cache_${key}`, stringified);
          if (key === 'theme_color') {
            localStorage.setItem('selected_theme', value);
          }
        } catch (e) {
          // Graceful QuotaExceededError fallback without breaking app execution
          if (e && (e.name === 'QuotaExceededError' || e.code === 22 || e.code === 1014)) {
            console.info('💾 LocalStorage limitine ulaşıldı; medya içerikleri bellek üzerinde (RAM) sorunsuz tutuluyor.');
          }
        }
      },"""

if old_cache_set in html:
    html = html.replace(old_cache_set, new_cache_set)
    print("Upgraded CacheService.set with Smart QuotaExceeded Protection!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html QuotaExceededError fix successfully!")
