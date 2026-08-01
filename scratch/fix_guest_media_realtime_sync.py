import re

# 1. Update serve_fast_3g.py to persist uploaded guest media into db_system_settings.json
with open('scratch/serve_fast_3g.py', 'r', encoding='utf-8') as f:
    server_code = f.read()

old_upload_handler = """        # 2. API: Media Upload POST
        if parsed_path.path == '/api/upload-media':
            try:
                content_len = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_len)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status":"ok","message":"File upload received successfully"}')
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"error":"Upload failed"}')
                return"""

new_upload_handler = """        # 2. API: Media Upload POST
        if parsed_path.path == '/api/upload-media':
            try:
                content_len = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_len)
                data = json.loads(body.decode('utf-8'))
                
                db_file = os.path.join(os.path.dirname(__file__), 'db_system_settings.json')
                existing = {}
                if os.path.exists(db_file):
                    try:
                        with open(db_file, 'r', encoding='utf-8') as f:
                            existing = json.load(f)
                    except Exception: pass
                
                if 'reservations' in data and isinstance(data['reservations'], list):
                    existing['reservations'] = data['reservations']
                elif 'resId' in data and 'mediaObj' in data:
                    res_id = data['resId']
                    media_obj = data['mediaObj']
                    res_list = existing.get('reservations', [])
                    found = False
                    for r in res_list:
                        if r.get('id') == res_id or r.get('mediaKey') == res_id:
                            if 'mediaFiles' not in r: r['mediaFiles'] = []
                            r['mediaFiles'].insert(0, media_obj)
                            found = True
                            break
                    if not found:
                        res_list.insert(0, {
                            "id": res_id,
                            "mediaKey": res_id,
                            "customerName": "Özel Düğün & Balo Daveti",
                            "eventType": "Balo / Düğün Daveti",
                            "date": "2026-08-01",
                            "venueId": "v1",
                            "mediaFiles": [media_obj]
                        })
                    existing['reservations'] = res_list
                
                with open(db_file, 'w', encoding='utf-8') as f:
                    json.dump(existing, f, indent=2)
                    
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status":"ok","message":"Media uploaded and saved to backend DB"}')
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(f'{{"error":"Upload failed: {str(e)}"}}'.encode('utf-8'))
                return"""

if old_upload_handler in server_code:
    server_code = server_code.replace(old_upload_handler, new_upload_handler)
    with open('scratch/serve_fast_3g.py', 'w', encoding='utf-8') as f:
        f.write(server_code)
    print("Updated serve_fast_3g.py POST /api/upload-media handler successfully!")
else:
    print("Warning: Could not find old_upload_handler in serve_fast_3g.py!")

# 2. Update index.html App component to process data.reservations from /api/system-settings
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_app_fetch = """            if (data.themeColor) {"""
new_app_fetch = """            if (data.reservations && Array.isArray(data.reservations) && data.reservations.length > 0) {
              setReservations(prev => {
                if (JSON.stringify(prev) !== JSON.stringify(data.reservations)) {
                  return data.reservations;
                }
                return prev;
              });
            }
            if (data.themeColor) {"""

if old_app_fetch in html:
    html = html.replace(old_app_fetch, new_app_fetch, 1)

# 3. Update MediaComponent real-time sync & guest reservation creation logic
old_media_sync_block = """  // REAL-TIME INSTANT SYNC ACROSS TABS AND SAME WINDOW (POLLING + BROADCAST + STORAGE EVENT)
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

new_media_sync_block = """  // REAL-TIME INSTANT SYNC ACROSS TABS, BROWSERS AND INCOGNITO WINDOWS (BACKEND API + POLLING + LOCALSTORAGE)
  useEffect(() => {
    const syncFromBackendAndCache = () => {
      // 1. Fetch live reservations from backend server DB
      if (typeof window !== 'undefined' && window.fetchWithRetry) {
        window.fetchWithRetry('/api/system-settings')
          .then(res => res.json())
          .then(data => {
            if (data && Array.isArray(data.reservations) && data.reservations.length > 0) {
              setReservations(prev => {
                if (JSON.stringify(prev) !== JSON.stringify(data.reservations)) {
                  try { localStorage.setItem('irem_cache_reservations', JSON.stringify(data.reservations)); } catch(e){}
                  return data.reservations;
                }
                return prev;
              });
            }
          })
          .catch(() => {
            // Fallback to localStorage
            try {
              const raw = localStorage.getItem('irem_cache_reservations');
              if (raw) {
                const parsed = JSON.parse(raw);
                if (Array.isArray(parsed) && parsed.length > 0) {
                  setReservations(prev => JSON.stringify(prev) !== raw ? parsed : prev);
                }
              }
            } catch(e){}
          });
      }
    };

    const handleStorageChange = (e) => {
      if (!e.key || e.key === 'irem_cache_reservations' || e.key === 'reservations') {
        syncFromBackendAndCache();
      }
    };

    const handleCustomSync = (e) => {
      if (e.detail && Array.isArray(e.detail)) {
        setReservations(e.detail);
      } else {
        syncFromBackendAndCache();
      }
    };

    window.addEventListener('storage', handleStorageChange);
    window.addEventListener('irem_media_sync', handleCustomSync);

    // Initial sync
    syncFromBackendAndCache();

    // 1-Second Fast Polling for instant updates across devices / windows without page refresh
    const pollTimer = setInterval(syncFromBackendAndCache, 1000);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
      window.removeEventListener('irem_media_sync', handleCustomSync);
      clearInterval(pollTimer);
    };
  }, [setReservations]);"""

if old_media_sync_block in html:
    html = html.replace(old_media_sync_block, new_media_sync_block)
    print("Updated MediaComponent real-time sync block successfully!")
else:
    print("Warning: Could not find old_media_sync_block in index.html!")

# 4. Update setReservations upload callback inside MediaComponent to dynamically push targetResKey if missing
old_upload_save_block = """          // Update reservations state & IMMEDIATELY SAVE TO CACHESERVICE & DISPATCH CUSTOM SYNC EVENT
          setReservations(prev => {
            const targetResKey = activeMediaKey || currentRes?.mediaKey || currentRes?.id;
            const targetResId = currentRes?.id;

            const updated = prev.map((r, idx) => {
              const isMatch = (r.mediaKey && r.mediaKey === targetResKey) ||
                              (r.id && r.id === targetResKey) ||
                              (targetResId && r.id === targetResId) ||
                              (selectedResKey && (r.mediaKey === selectedResKey || r.id === selectedResKey)) ||
                              (prev.length === 1 || idx === 0 && !selectedResKey);

              if (isMatch) {
                const existingList = r.mediaFiles || [];
                return {
                  ...r,
                  mediaKey: r.mediaKey || targetResKey || 'MEDIA-8X92M1KP',
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

new_upload_save_block = """          // Update reservations state & IMMEDIATELY PERSIST TO SERVER DB, CACHESERVICE, LOCALSTORAGE & DISPATCH SYNC EVENT
          setReservations(prev => {
            const targetResKey = activeMediaKey || currentRes?.mediaKey || currentRes?.id || selectedResKey || 'MEDIA-8X92M1KP';
            const targetResId = currentRes?.id;
            const cleanKey = targetResKey.replace(/[^A-Za-z0-9]/g, '').toLowerCase();

            let found = false;
            const updated = prev.map((r, idx) => {
              const k1 = (r.mediaKey || '').replace(/[^A-Za-z0-9]/g, '').toLowerCase();
              const k2 = (r.id || '').replace(/[^A-Za-z0-9]/g, '').toLowerCase();
              const isMatch = k1 === cleanKey || k2 === cleanKey ||
                              (r.mediaKey && r.mediaKey === targetResKey) ||
                              (r.id && r.id === targetResKey) ||
                              (targetResId && r.id === targetResId) ||
                              (selectedResKey && (r.mediaKey === selectedResKey || r.id === selectedResKey));

              if (isMatch) {
                found = true;
                const existingList = r.mediaFiles || [];
                return {
                  ...r,
                  mediaKey: r.mediaKey || targetResKey,
                  mediaFiles: [newMediaObj, ...existingList]
                };
              }
              return r;
            });

            if (!found) {
              updated.unshift({
                id: targetResKey,
                mediaKey: targetResKey,
                customerName: 'Özel Düğün & Balo Daveti',
                eventType: 'Balo / Düğün Daveti',
                date: new Date().toISOString().split('T')[0],
                venueId: 'v1',
                mediaFiles: [newMediaObj]
              });
            }

            // Persist to Server DB via API, LocalStorage, and dispatch Custom Event
            try {
              const jsonStr = JSON.stringify(updated);
              localStorage.setItem('irem_cache_reservations', jsonStr);
              if (typeof CacheService !== 'undefined') {
                CacheService.set('reservations', updated);
              }

              fetch('/api/upload-media', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  resId: targetResKey,
                  mediaObj: newMediaObj,
                  reservations: updated
                })
              }).catch(e => console.warn('POST /api/upload-media error:', e));

              window.dispatchEvent(new CustomEvent('irem_media_sync', { detail: updated }));
            } catch(e){}

            return updated;
          });"""

if old_upload_save_block in html:
    html = html.replace(old_upload_save_block, new_upload_save_block)
    print("Updated MediaComponent upload save block successfully!")
else:
    print("Warning: Could not find old_upload_save_block in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Synchronized guest media upload and real-time backend sync successfully!")
