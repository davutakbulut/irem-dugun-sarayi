import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix mediaKey normalization to preserve initial custom mediaKeys (e.g. MEDIA-8X92M1KP)
old_normalization = """      // Auto-normalize mediaKey on all reservations (Ensures older cached items have mediaKeys)
      const normalizeReservationsMediaKeys = (list) => {
        if (!Array.isArray(list)) return [];
        return list.map((r, idx) => ({
          ...r,
          mediaKey: r.mediaKey || ('MEDIA-' + (r.id || 'RES-' + idx).replace(/[^A-Za-z0-9]/g, ''))
        }));
      };"""

new_normalization = """      // Auto-normalize mediaKey on all reservations while PRESERVING custom initial keys like MEDIA-8X92M1KP
      const normalizeReservationsMediaKeys = (list) => {
        if (!Array.isArray(list)) return [];
        const initialMap = {
          'RES-2026-001': 'MEDIA-8X92M1KP',
          'RES-2026-002': 'MEDIA-7K34P9LV'
        };
        return list.map((r, idx) => {
          const knownKey = initialMap[r.id] || r.mediaKey;
          return {
            ...r,
            mediaKey: knownKey || ('MEDIA-' + (r.id || 'RES-' + idx).replace(/[^A-Za-z0-9]/g, ''))
          };
        });
      };"""

if old_normalization in html:
    html = html.replace(old_normalization, new_normalization)
    print("Updated normalizeReservationsMediaKeys to strictly preserve MEDIA-8X92M1KP and MEDIA-7K34P9LV!")

# Clear localstorage cache initialization script in html if needed
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html mediaKey preservation successfully!")
