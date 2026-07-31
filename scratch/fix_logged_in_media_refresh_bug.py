import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update isPublicGuestRoute in App component to strictly match standalone public routes (#/medya/ or #/m/ or mode=guest)
old_app_guest_route = """      const isPublicGuestRoute = useMemo(() => {
        if (typeof window === 'undefined') return false;
        const hash = window.location.hash || '';
        return hash.includes('medya/') || hash.includes('m/') || hash.includes('key=') || hash.includes('mode=guest');
      }, [activeTab]);"""

new_app_guest_route = """      // STRICT PUBLIC GUEST ROUTE DETECTOR:
      // Public guest mode is enforced ONLY for standalone guest URLs (#/medya/:key or #/m/:key or ?mode=guest).
      // Internal staff navigation (#/medya-yukle?key=...) preserves full Admin/Customer layout on page refresh!
      const isPublicGuestRoute = useMemo(() => {
        if (typeof window === 'undefined') return false;
        const hash = window.location.hash || '';
        const isStandaloneGuestUrl = /^#\/(?:medya|m)\//.test(hash) || hash.includes('mode=guest');
        return isStandaloneGuestUrl;
      }, [activeTab]);"""

if old_app_guest_route in html:
    html = html.replace(old_app_guest_route, new_app_guest_route)
    print("Updated App isPublicGuestRoute to strictly match standalone guest routes!")

# 2. Update isPublicGuestMode in MediaComponent to match
old_media_guest_mode = """  // STRICT GUEST MODE: Whenever key= or mode=guest is in URL hash, enforce Guest View
  const isPublicGuestMode = useMemo(() => {
    if (typeof window === 'undefined') return false;
    const hash = window.location.hash || '';
    return hash.includes('key=') || hash.includes('mode=guest');
  }, []);"""

new_media_guest_mode = """  // STRICT GUEST MODE: Active ONLY on standalone guest links (#/medya/:key or ?mode=guest)
  const isPublicGuestMode = useMemo(() => {
    if (typeof window === 'undefined') return false;
    const hash = window.location.hash || '';
    return /^#\/(?:medya|m)\//.test(hash) || hash.includes('mode=guest');
  }, []);"""

if old_media_guest_mode in html:
    html = html.replace(old_media_guest_mode, new_media_guest_mode)
    print("Updated MediaComponent isPublicGuestMode to match standalone guest routes!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html logged-in media refresh fix successfully!")
