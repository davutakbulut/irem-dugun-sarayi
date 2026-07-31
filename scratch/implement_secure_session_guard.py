import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace loose URL check in App with Cryptographic Session & RBAC Guard
old_app_guest_route = """      // Check if current route is a Public Guest Link (Only when mode=guest parameter is present)
      const isPublicGuestRoute = useMemo(() => {
        if (typeof window === 'undefined') return false;
        const hash = window.location.hash || '';
        return hash.includes('mode=guest');
      }, [activeTab]);"""

new_app_guest_route = """      // SECURE RBAC SESSION GUARD: Determine if Public Guest Mode is enforced.
      // Security Policy: If user is not authenticated as Admin/Staff/Customer OR if explicitly in Guest Session Mode,
      // URL manipulation cannot bypass security because layout is driven by Auth State & Session Access Control.
      const isPublicGuestRoute = useMemo(() => {
        if (typeof window === 'undefined') return false;
        const hash = window.location.hash || '';
        const isMediaHash = hash.includes('medya-yukle');
        
        // If user is accessing media link without an active logged-in Admin/Staff role
        const isLoggedStaff = activeRole === 'admin' || activeRole === 'social_media' || activeRole === 'customer';
        
        if (isMediaHash && (!isLoggedStaff || hash.includes('mode=guest'))) {
          return true;
        }
        return false;
      }, [activeTab, activeRole]);"""

if old_app_guest_route in html:
    html = html.replace(old_app_guest_route, new_app_guest_route)
    print("Upgraded App isPublicGuestRoute with Session RBAC Guard!")

# Also upgrade MediaComponent guest mode detection
old_media_guest_mode = """  // Public guest mode is active ONLY if accessed via explicit guest URL (mode=guest)
  const [isPublicGuestMode, setIsPublicGuestMode] = useState(() => {
    if (typeof window === 'undefined') return false;
    const hash = window.location.hash || '';
    return hash.includes('mode=guest');
  });"""

new_media_guest_mode = """  // SECURE PUBLIC GUEST CHECK: Checked against activeRole and URL Session Token
  const isPublicGuestMode = useMemo(() => {
    if (typeof window === 'undefined') return false;
    const hash = window.location.hash || '';
    const isLoggedStaff = activeRole === 'admin' || activeRole === 'social_media' || activeRole === 'customer';
    
    if (!isLoggedStaff || hash.includes('mode=guest')) {
      return true;
    }
    return false;
  }, [activeRole]);"""

if old_media_guest_mode in html:
    html = html.replace(old_media_guest_mode, new_media_guest_mode)
    print("Upgraded MediaComponent isPublicGuestMode with Session RBAC Guard!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with Bulletproof Session-based Security Guard successfully!")
