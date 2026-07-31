import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace selectReservation and add browser Back/Forward navigation listener in MediaComponent
old_select_res = """  // Sync selectedResKey with browser URL Hash dynamically without full reload
  const selectReservation = (key) => {
    setSelectedResKey(key);
    if (typeof window !== 'undefined') {
      if (key) {
        const prefix = isPublicGuestMode ? 'mode=guest&key=' : 'key=';
        window.history.replaceState(null, '', `#/medya-yukle?${prefix}${key}`);
      } else {
        window.history.replaceState(null, '', `#/medya-yukle`);
      }
    }
  };"""

new_select_res = """  // Sync selectedResKey with browser URL Hash (Pushes new history entry so Back button returns to #/medya-yukle cards list)
  const selectReservation = (key) => {
    setSelectedResKey(key);
    if (typeof window !== 'undefined') {
      if (key) {
        const prefix = isPublicGuestMode ? 'mode=guest&key=' : 'key=';
        window.location.hash = `#/medya-yukle?${prefix}${key}`;
      } else {
        window.location.hash = `#/medya-yukle`;
      }
    }
  };

  // Listen for browser Back / Forward button clicks (popstate & hashchange)
  useEffect(() => {
    const handleUrlHashSync = () => {
      const freshUrlKey = getUrlKey();
      setSelectedResKey(freshUrlKey || null);
    };
    window.addEventListener('hashchange', handleUrlHashSync);
    window.addEventListener('popstate', handleUrlHashSync);
    return () => {
      window.removeEventListener('hashchange', handleUrlHashSync);
      window.removeEventListener('popstate', handleUrlHashSync);
    };
  }, []);"""

if old_select_res in html:
    html = html.replace(old_select_res, new_select_res)
    print("Replaced replaceState with location.hash & added popstate/hashchange Back button listener!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html browser back button navigation successfully!")
