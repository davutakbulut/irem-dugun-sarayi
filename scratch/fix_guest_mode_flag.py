import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Refine isPublicGuestMode in MediaComponent to strictly check mode=guest
old_media_guest_mode = """  // Public guest mode is active ONLY if accessed via key parameter from outside without staff navigation
  const [isPublicGuestMode, setIsPublicGuestMode] = useState(() => {
    if (typeof window === 'undefined') return false;
    const hash = window.location.hash || '';
    return hash.includes('key=MEDIA-') || hash.includes('mode=guest');
  });"""

new_media_guest_mode = """  // Public guest mode is active ONLY if accessed via explicit guest URL (mode=guest)
  const [isPublicGuestMode, setIsPublicGuestMode] = useState(() => {
    if (typeof window === 'undefined') return false;
    const hash = window.location.hash || '';
    return hash.includes('mode=guest');
  });"""

if old_media_guest_mode in html:
    html = html.replace(old_media_guest_mode, new_media_guest_mode)
    print("Updated MediaComponent isPublicGuestMode to check mode=guest!")

# 2. Refine isPublicGuestRoute in App component to strictly check mode=guest
old_app_guest_route = """      // Check if current route is a Public Guest Link (e.g. #/medya-yukle?key=MEDIA-8X92M1KP or ?mode=guest)
      const isPublicGuestRoute = useMemo(() => {
        if (typeof window === 'undefined') return false;
        const hash = window.location.hash || '';
        return hash.includes('key=') || hash.includes('mode=guest');
      }, [activeTab]);"""

new_app_guest_route = """      // Check if current route is a Public Guest Link (Only when mode=guest parameter is present)
      const isPublicGuestRoute = useMemo(() => {
        if (typeof window === 'undefined') return false;
        const hash = window.location.hash || '';
        return hash.includes('mode=guest');
      }, [activeTab]);"""

if old_app_guest_route in html:
    html = html.replace(old_app_guest_route, new_app_guest_route)
    print("Updated App isPublicGuestRoute to check mode=guest!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html guest mode flags successfully!")
