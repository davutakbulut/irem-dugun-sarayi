import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the real-time sync useEffect and save logic in MediaComponent

old_sync_effect = """  // REAL-TIME SYNC ACROSS TABS / ADMIN PANEL
  useEffect(() => {
    const handleStorageChange = (e) => {
      if (e.key === 'irem_cache_reservations' || e.key === 'reservations') {
        try {
          const freshReservations = JSON.parse(e.newValue);
          if (Array.isArray(freshReservations)) {
            setReservations(freshReservations);
          }
        } catch(err){}
      }
    };
    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [setReservations]);"""

new_sync_effect = """  // REAL-TIME INSTANT SYNC ACROSS TABS AND SAME WINDOW (POLLING + BROADCAST + STORAGE EVENT)
  useEffect(() => {
    const syncFromCache = () => {
      try {
        const raw = localStorage.getItem('irem_cache_reservations');
        if (raw) {
          const parsed = JSON.parse(raw);
          if (Array.isArray(parsed) && parsed.length > 0) {
            setReservations(prev => {
              // Only update state if JSON strings differ to avoid infinite re-render loop
              if (JSON.stringify(prev) !== raw) {
                return parsed;
              }
              return prev;
            });
          }
        }
      } catch(e){}
    };

    const handleStorageChange = (e) => {
      if (!e.key || e.key === 'irem_cache_reservations' || e.key === 'reservations') {
        syncFromCache();
      }
    };

    const handleCustomSync = (e) => {
      if (e.detail && Array.isArray(e.detail)) {
        setReservations(e.detail);
      } else {
        syncFromCache();
      }
    };

    window.addEventListener('storage', handleStorageChange);
    window.addEventListener('irem_media_sync', handleCustomSync);

    // Fast 1-second polling fallback so guest uploads appear on Admin panel in under 1 second without page refresh
    const pollTimer = setInterval(syncFromCache, 1000);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
      window.removeEventListener('irem_media_sync', handleCustomSync);
      clearInterval(pollTimer);
    };
  }, [setReservations]);"""

if old_sync_effect in html:
    html = html.replace(old_sync_effect, new_sync_effect)
    print("Replaced real-time sync effect with Fast Polling + Custom Event + Storage Event sync!")

# Now replace the upload save code in reader.onload
old_save_code = """          // Update reservations state & IMMEDIATELY SAVE TO CACHESERVICE (PERSISTENCE FIX)
          setReservations(prev => {
            const updated = prev.map(r => {
              if (r.mediaKey === activeMediaKey || r.id === currentRes?.id) {
                return {
                  ...r,
                  mediaFiles: [newMediaObj, ...(r.mediaFiles || [])]
                };
              }
              return r;
            });

            // Save to CacheService and trigger LocalStorage event for real-time admin sync
            try {
              if (typeof CacheService !== 'undefined') {
                CacheService.set('reservations', updated);
              } else {
                localStorage.setItem('irem_cache_reservations', JSON.stringify(updated));
              }
            } catch(e){}

            return updated;
          });"""

new_save_code = """          // Update reservations state & IMMEDIATELY SAVE TO CACHESERVICE & DISPATCH CUSTOM SYNC EVENT
          setReservations(prev => {
            const targetResKey = activeMediaKey || currentRes?.mediaKey || currentRes?.id;
            const updated = prev.map(r => {
              if (r.mediaKey === targetResKey || r.id === targetResKey || r.mediaKey === selectedResKey || r.id === selectedResKey) {
                const existingList = r.mediaFiles || [];
                return {
                  ...r,
                  mediaFiles: [newMediaObj, ...existingList]
                };
              }
              return r;
            });

            // Save to CacheService & LocalStorage
            try {
              const jsonStr = JSON.stringify(updated);
              localStorage.setItem('irem_cache_reservations', jsonStr);
              if (typeof CacheService !== 'undefined') {
                CacheService.set('reservations', updated);
              }
              // Dispatch instant custom sync event for all active components in same tab/window
              window.dispatchEvent(new CustomEvent('irem_media_sync', { detail: updated }));
            } catch(e){}

            return updated;
          });"""

if old_save_code in html:
    html = html.replace(old_save_code, new_save_code)
    print("Replaced upload save code with guaranteed targetResKey matching & instant CustomEvent dispatch!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated real-time instant media sync successfully!")
