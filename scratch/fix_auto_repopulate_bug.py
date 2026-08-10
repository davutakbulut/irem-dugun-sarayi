import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the fallback logic in fetchSystemSettings
old_fetch_logic = """                  if (data.reservations !== undefined && Array.isArray(data.reservations)) {
                    setReservations(prev => {
                      if (JSON.stringify(prev) !== JSON.stringify(data.reservations)) {
                        return data.reservations;
                      }
                      return prev;
                    });
                  } else {
                    const initRes = (typeof INITIAL_RESERVATIONS !== 'undefined' && Array.isArray(INITIAL_RESERVATIONS)) ? INITIAL_RESERVATIONS : [];
                    setReservations(initRes);
                    try {
                      const fetchFn = window.fetchWithRetry || fetch;
                      fetchFn('/api/system-settings', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ reservations: initRes, updatedAt: new Date().toISOString(), updatedBy: 'system' })
                      }).catch(() => {});
                    } catch(e) {}
                  }"""

new_fetch_logic = """                  if (data.reservations !== undefined && Array.isArray(data.reservations)) {
                    setReservations(prev => {
                      if (JSON.stringify(prev) !== JSON.stringify(data.reservations)) {
                        return data.reservations;
                      }
                      return prev;
                    });
                  } else {
                    setReservations([]);
                  }"""

if old_fetch_logic in content:
    content = content.replace(old_fetch_logic, new_fetch_logic)
    print("1. Removed automatic INITIAL_RESERVATIONS repopulate fallback in fetchSystemSettings!")
else:
    print("WARNING: Could not find old_fetch_logic in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
