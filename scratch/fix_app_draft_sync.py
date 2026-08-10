import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_use_effects = """      useEffect(() => {
        CacheService.set('venues', venues);
        if (window.fetchWithRetry && venues && venues.length > 0) {
          window.fetchWithRetry('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ venues })
          }).catch(() => {});
        }
      }, [venues]);
      useEffect(() => {
        CacheService.set('services', services);
        if (window.fetchWithRetry && services && services.length > 0) {
          window.fetchWithRetry('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ services })
          }).catch(() => {});
        }
      }, [services]);
      useEffect(() => {
        CacheService.set('campaigns', campaigns);
        if (window.fetchWithRetry && campaigns && campaigns.length > 0) {
          window.fetchWithRetry('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ campaigns })
          }).catch(() => {});
        }
      }, [campaigns]);
      useEffect(() => {
        CacheService.set('customers', customers);
        if (window.fetchWithRetry && customers && customers.length > 0) {
          window.fetchWithRetry('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ customers })
          }).catch(() => {});
        }
      }, [customers]);
      useEffect(() => {
        CacheService.set('reservations', reservations);
        if (window.fetchWithRetry && reservations && reservations.length > 0) {
          window.fetchWithRetry('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ reservations })
          }).catch(() => {});
        }
      }, [reservations]);
      useEffect(() => {
        CacheService.set('draft_reservations', draftReservations);
        window.fetchWithRetry('/api/system-settings', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ draftReservations })
        }).catch(() => {});
      }, [draftReservations]);
      useEffect(() => {
        CacheService.set('users', users);
        if (window.fetchWithRetry && users && users.length > 0) {
          window.fetchWithRetry('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ users })
          }).catch(() => {});
        }
      }, [users]);"""

new_use_effects = """      useEffect(() => {
        CacheService.set('venues', venues);
        const fetchFn = window.fetchWithRetry || fetch;
        if (fetchFn && venues && venues.length > 0) {
          fetchFn('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ venues })
          }).catch(() => {});
        }
      }, [venues]);
      useEffect(() => {
        CacheService.set('services', services);
        const fetchFn = window.fetchWithRetry || fetch;
        if (fetchFn && services && services.length > 0) {
          fetchFn('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ services })
          }).catch(() => {});
        }
      }, [services]);
      useEffect(() => {
        CacheService.set('campaigns', campaigns);
        const fetchFn = window.fetchWithRetry || fetch;
        if (fetchFn && campaigns && campaigns.length > 0) {
          fetchFn('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ campaigns })
          }).catch(() => {});
        }
      }, [campaigns]);
      useEffect(() => {
        CacheService.set('customers', customers);
        const fetchFn = window.fetchWithRetry || fetch;
        if (fetchFn && customers && customers.length > 0) {
          fetchFn('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ customers })
          }).catch(() => {});
        }
      }, [customers]);
      useEffect(() => {
        CacheService.set('reservations', reservations);
        const fetchFn = window.fetchWithRetry || fetch;
        if (fetchFn && reservations && reservations.length > 0) {
          fetchFn('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ reservations })
          }).catch(() => {});
        }
      }, [reservations]);
      useEffect(() => {
        CacheService.set('draft_reservations', draftReservations);
        const fetchFn = window.fetchWithRetry || fetch;
        if (fetchFn && draftReservations) {
          fetchFn('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ draftReservations })
          }).catch(() => {});
        }
      }, [draftReservations]);
      useEffect(() => {
        CacheService.set('users', users);
        const fetchFn = window.fetchWithRetry || fetch;
        if (fetchFn && users && users.length > 0) {
          fetchFn('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ users })
          }).catch(() => {});
        }
      }, [users]);"""

if old_use_effects in content:
    content = content.replace(old_use_effects, new_use_effects)
    print("Replaced useEffect state synchronizers with fail-safe fetchFn!")
else:
    print("WARNING: Could not find exact old_use_effects string in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
