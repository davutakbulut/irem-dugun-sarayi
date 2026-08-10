import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add isInitialLoadDoneRef right before useEffect hooks in App
target_state_section = """      const [tabPermissionsState, setTabPermissionsState] = useState(() => CacheService.get('tab_permissions', DEFAULT_ROLE_TAB_PERMISSIONS));"""

replacement_state_section = """      const [tabPermissionsState, setTabPermissionsState] = useState(() => CacheService.get('tab_permissions', DEFAULT_ROLE_TAB_PERMISSIONS));
      const isInitialLoadDoneRef = useRef(false);"""

if target_state_section in content and "isInitialLoadDoneRef" not in content:
    content = content.replace(target_state_section, replacement_state_section)
    print("1. Added isInitialLoadDoneRef declaration in App component.")

# 2. Update useEffect POST hooks to check isInitialLoadDoneRef.current
old_sync_hooks = """      useEffect(() => {
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

new_sync_hooks = """      useEffect(() => {
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

if old_sync_hooks in content:
    content = content.replace(old_sync_hooks, new_sync_hooks)
    print("2. Added isInitialLoadDoneRef check to all state useEffect hooks.")

# 3. In fetchSystemSettings completion, set isInitialLoadDoneRef.current = true
old_fetch_end = """                  if (data.storedMedia && typeof data.storedMedia === 'object') {"""

new_fetch_end = """                  isInitialLoadDoneRef.current = true;
                  if (data.storedMedia && typeof data.storedMedia === 'object') {"""

if old_fetch_end in content and "isInitialLoadDoneRef.current = true;" not in content:
    content = content.replace(old_fetch_end, new_fetch_end)
    print("3. Set isInitialLoadDoneRef.current = true in fetchSystemSettings success callback.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
