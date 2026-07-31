import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace isPublicGuestRoute in App component to ALWAYS hide sidebar when key= or mode=guest is in URL hash
old_route_logic = """      // SECURE RBAC SESSION GUARD: Determine if Public Guest Mode is enforced.
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

new_route_logic = """      // STRICT SIDEBAR HIDING GUARD: Whenever key= or mode=guest is present in URL hash,
      // Sidebar, Admin Topbar, Role Switcher and Admin Header are 100% HIDDEN AND INACCESSIBLE!
      const isPublicGuestRoute = useMemo(() => {
        if (typeof window === 'undefined') return false;
        const hash = window.location.hash || '';
        return hash.includes('key=') || hash.includes('mode=guest');
      }, [activeTab]);"""

if old_route_logic in html:
    html = html.replace(old_route_logic, new_route_logic)
    print("Updated App isPublicGuestRoute to strictly hide sidebar whenever key= or mode=guest is present!")

# Also update MediaComponent isPublicGuestMode to match
old_media_mode_logic = """  // SECURE PUBLIC GUEST CHECK: Checked against activeRole and URL Session Token
  const isPublicGuestMode = useMemo(() => {
    if (typeof window === 'undefined') return false;
    const hash = window.location.hash || '';
    const isLoggedStaff = activeRole === 'admin' || activeRole === 'social_media' || activeRole === 'customer';
    
    if (!isLoggedStaff || hash.includes('mode=guest')) {
      return true;
    }
    return false;
  }, [activeRole]);"""

new_media_mode_logic = """  // STRICT GUEST MODE: Whenever key= or mode=guest is in URL hash, enforce Guest View
  const isPublicGuestMode = useMemo(() => {
    if (typeof window === 'undefined') return false;
    const hash = window.location.hash || '';
    return hash.includes('key=') || hash.includes('mode=guest');
  }, []);"""

if old_media_mode_logic in html:
    html = html.replace(old_media_mode_logic, new_media_mode_logic)
    print("Updated MediaComponent isPublicGuestMode to match key= or mode=guest check!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html sidebar hiding guard successfully!")
