import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the entity useEffect hooks to allow POSTing empty arrays [] when user deletes all items
old_effects = """      useEffect(() => {
        if (!isInitialLoadDoneRef.current) return;
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
        if (!isInitialLoadDoneRef.current) return;
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
        if (!isInitialLoadDoneRef.current) return;
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
        if (!isInitialLoadDoneRef.current) return;
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
        if (!isInitialLoadDoneRef.current) return;
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
        if (!isInitialLoadDoneRef.current) return;
        CacheService.set('draft_reservations', draftReservations);
        const fetchFn = window.fetchWithRetry || fetch;
        if (fetchFn) {
          fetchFn('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ draftReservations })
          }).catch(() => {});
        }
      }, [draftReservations]);
      useEffect(() => {
        if (!isInitialLoadDoneRef.current) return;
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

new_effects = """      useEffect(() => {
        if (!isInitialLoadDoneRef.current) return;
        CacheService.set('venues', venues);
        const fetchFn = window.fetchWithRetry || fetch;
        if (fetchFn && Array.isArray(venues)) {
          fetchFn('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ venues })
          }).catch(() => {});
        }
      }, [venues]);
      useEffect(() => {
        if (!isInitialLoadDoneRef.current) return;
        CacheService.set('services', services);
        const fetchFn = window.fetchWithRetry || fetch;
        if (fetchFn && Array.isArray(services)) {
          fetchFn('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ services })
          }).catch(() => {});
        }
      }, [services]);
      useEffect(() => {
        if (!isInitialLoadDoneRef.current) return;
        CacheService.set('campaigns', campaigns);
        const fetchFn = window.fetchWithRetry || fetch;
        if (fetchFn && Array.isArray(campaigns)) {
          fetchFn('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ campaigns })
          }).catch(() => {});
        }
      }, [campaigns]);
      useEffect(() => {
        if (!isInitialLoadDoneRef.current) return;
        CacheService.set('customers', customers);
        const fetchFn = window.fetchWithRetry || fetch;
        if (fetchFn && Array.isArray(customers)) {
          fetchFn('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ customers })
          }).catch(() => {});
        }
      }, [customers]);
      useEffect(() => {
        if (!isInitialLoadDoneRef.current) return;
        CacheService.set('reservations', reservations);
        const fetchFn = window.fetchWithRetry || fetch;
        if (fetchFn && Array.isArray(reservations)) {
          fetchFn('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ reservations })
          }).catch(() => {});
        }
      }, [reservations]);
      useEffect(() => {
        if (!isInitialLoadDoneRef.current) return;
        CacheService.set('draft_reservations', draftReservations);
        const fetchFn = window.fetchWithRetry || fetch;
        if (fetchFn && Array.isArray(draftReservations)) {
          fetchFn('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ draftReservations })
          }).catch(() => {});
        }
      }, [draftReservations]);
      useEffect(() => {
        if (!isInitialLoadDoneRef.current) return;
        CacheService.set('users', users);
        const fetchFn = window.fetchWithRetry || fetch;
        if (fetchFn && Array.isArray(users)) {
          fetchFn('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ users })
          }).catch(() => {});
        }
      }, [users]);"""

if old_effects in content:
    content = content.replace(old_effects, new_effects)
    print("Fixed empty array delete bug in useEffect hooks!")
else:
    print("WARNING: Could not find old_effects in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
