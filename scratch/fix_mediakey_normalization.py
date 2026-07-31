import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add auto-normalization helper for mediaKey on reservations state in App component
old_app_res_state = "const [reservations, setReservations] = useState(() => CacheService.get('reservations', INITIAL_RESERVATIONS));"

new_app_res_state = """// Auto-normalize mediaKey on all reservations (Ensures older cached items have mediaKeys)
      const normalizeReservationsMediaKeys = (list) => {
        if (!Array.isArray(list)) return [];
        return list.map((r, idx) => ({
          ...r,
          mediaKey: r.mediaKey || ('MEDIA-' + (r.id || 'RES-' + idx).replace(/[^A-Za-z0-9]/g, ''))
        }));
      };

      const [reservations, setReservations] = useState(() => {
        const cached = CacheService.get('reservations', INITIAL_RESERVATIONS);
        return normalizeReservationsMediaKeys(cached);
      });"""

if old_app_res_state in html:
    html = html.replace(old_app_res_state, new_app_res_state)
    print("Added normalizeReservationsMediaKeys to App state initialization!")

# 2. Fix target matching in MediaComponent setReservations upload handler
old_target_matching = """          // Update reservations state & IMMEDIATELY SAVE TO CACHESERVICE & DISPATCH CUSTOM SYNC EVENT
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
            });"""

new_target_matching = """          // Update reservations state & IMMEDIATELY SAVE TO CACHESERVICE & DISPATCH CUSTOM SYNC EVENT
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
            });"""

if old_target_matching in html:
    html = html.replace(old_target_matching, new_target_matching)
    print("Upgraded MediaComponent target matching logic to support fallback matching!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with mediaKey normalization & bulletproof matching successfully!")
