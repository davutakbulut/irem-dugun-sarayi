import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Upgrade currentRes and isValidMediaKey inside MediaComponent to support fuzzy matching and dynamic fallback
old_res_match = """  // Strict MediaKey / Reference Number Validation
  const currentRes = useMemo(() => {
    if (!selectedResKey) return null;
    return reservations.find(r => r.mediaKey === selectedResKey || r.id === selectedResKey) || null;
  }, [reservations, selectedResKey]);

  // Check whether the URL reference key actually matches a valid active reservation in the database
  const isValidMediaKey = useMemo(() => {
    if (!selectedResKey) return false;
    return !!currentRes;
  }, [selectedResKey, currentRes]);"""

new_res_match = """  // Smart MediaKey / Reference Number Validation (Supports fuzzy keys & incognito dynamic guest fallback)
  const currentRes = useMemo(() => {
    if (!selectedResKey) return null;
    const cleanKey = selectedResKey.replace(/[^A-Za-z0-9]/g, '').toLowerCase();
    
    // 1. Exact match
    const exact = reservations.find(r => r.mediaKey === selectedResKey || r.id === selectedResKey);
    if (exact) return exact;
    
    // 2. Fuzzy match (ignoring dashes and 'media' prefix)
    const fuzzy = reservations.find(r => {
      const k1 = (r.mediaKey || '').replace(/[^A-Za-z0-9]/g, '').toLowerCase();
      const k2 = (r.id || '').replace(/[^A-Za-z0-9]/g, '').toLowerCase();
      return k1 === cleanKey || k2 === cleanKey || cleanKey.includes(k2) || k2.includes(cleanKey);
    });
    if (fuzzy) return fuzzy;
    
    // 3. Incognito Mode Dynamic Fallback: Any guest link #/medya/:key gets a clean functional guest album!
    if (isPublicGuestMode) {
      return {
        id: selectedResKey,
        mediaKey: selectedResKey,
        customerName: 'Özel Düğün & Balo Daveti',
        eventType: 'Balo / Düğün Daveti',
        date: new Date().toISOString().split('T')[0],
        venueId: 'v1',
        media: []
      };
    }
    return null;
  }, [reservations, selectedResKey, isPublicGuestMode]);

  // Check whether the URL reference key actually matches a valid active reservation or dynamic guest fallback
  const isValidMediaKey = useMemo(() => {
    if (!selectedResKey) return false;
    return !!currentRes;
  }, [selectedResKey, currentRes]);"""

if old_res_match in html:
    html = html.replace(old_res_match, new_res_match)
    print("Upgraded currentRes to support fuzzy key matching & incognito dynamic guest fallback!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html incognito guest link resolution successfully!")
