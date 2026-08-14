import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update currentUserState initialization to use sessionUser or null (no hardcoded Davut fallback)
    old_current_user_init = """      const [currentUserState, setCurrentUserState] = useState(() => CacheService.get('current_user', {
        id: 'u_davut',
        name: 'Davut Akbulut',
        email: 'dvtakblt@gmail.com',
        phone: '+90 537 882 68 58',
        role: 'admin',
        avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'
      }));"""

    new_current_user_init = """      const [currentUserState, setCurrentUserState] = useState(getInitialSessionUser);"""

    if old_current_user_init in content:
        content = content.replace(old_current_user_init, new_current_user_init)
        print(f"Purged hardcoded default user state in {h_file}")

    # 2. Fix activeRole definition so it doesn't default to admin when logged out
    old_active_role = "const activeRole = (sessionUser?.role || currentUserState?.role || 'admin');"
    new_active_role = "const activeRole = sessionUser?.role || currentUserState?.role || 'guest';"

    if old_active_role in content:
        content = content.replace(old_active_role, new_active_role)
        print(f"Fixed activeRole default to guest in {h_file}")

    # 3. Fix auto-sync in fetch(/api/users) - NEVER auto-login when logged out
    old_user_sync_block = """                  // Strict Auto-sync for active logged-in user ONLY (no arbitrary role fallbacks)
                  const loggedInEmail = (sessionUser?.email || currentUserState?.email || 'dvtakblt@gmail.com').toLowerCase().trim();
                  const loggedInId = sessionUser?.id || currentUserState?.id;
                  const dbMatch = data.find(u => (loggedInId && u.id === loggedInId) || (loggedInEmail && u.email && u.email.toLowerCase().trim() === loggedInEmail));
                  if (dbMatch) {
                    const mergedUser = { ...(sessionUser || currentUserState || {}), ...dbMatch };
                    setCurrentUserState(mergedUser);
                    setSessionUser(mergedUser);
                    CacheService.set('current_user', mergedUser);
                    CacheService.set('session_user', mergedUser);
                  }"""

    new_user_sync_block = """                  // Sync profile ONLY if a user is legitimately logged in
                  if (sessionUser && (sessionUser.id || sessionUser.email)) {
                    const loggedInEmail = (sessionUser.email || '').toLowerCase().trim();
                    const loggedInId = sessionUser.id;
                    const dbMatch = data.find(u => (loggedInId && u.id === loggedInId) || (loggedInEmail && u.email && u.email.toLowerCase().trim() === loggedInEmail));
                    if (dbMatch) {
                      const mergedUser = { ...sessionUser, ...dbMatch };
                      setCurrentUserState(mergedUser);
                      setSessionUser(mergedUser);
                      try {
                        localStorage.setItem('irem_session_user', JSON.stringify(mergedUser));
                        localStorage.setItem('irem_cache_session_user', JSON.stringify(mergedUser));
                      } catch(e){}
                    }
                  }"""

    if old_user_sync_block in content:
        content = content.replace(old_user_sync_block, new_user_sync_block)
        print(f"Fixed user sync block in {h_file}")

    # 4. Update handleLogout to completely clean all user references
    old_logout = """      const handleLogout = useCallback(() => {
        setSessionUser(null);
        try {
          localStorage.removeItem('irem_session_user');
          localStorage.removeItem('irem_cache_session_user');
          localStorage.removeItem('session_user');
          sessionStorage.clear();
        } catch(e){}
        CacheService.set('session_user', null);
        setActiveTabState('login');
        if (typeof window !== 'undefined' && window.history && window.history.pushState) {
          window.history.pushState({}, '', '/yonetim/giris');
        }
        showToast('Güvenli Şekilde Oturum Kapatıldı');
      }, []);"""

    new_logout = """      const handleLogout = useCallback(() => {
        setSessionUser(null);
        setCurrentUserState(null);
        try {
          localStorage.removeItem('irem_session_user');
          localStorage.removeItem('irem_cache_session_user');
          localStorage.removeItem('session_user');
          localStorage.removeItem('current_user');
          localStorage.removeItem('irem_cache_current_user');
          sessionStorage.clear();
        } catch(e){}
        if (typeof CacheService !== 'undefined') {
          CacheService.set('session_user', null);
          CacheService.set('current_user', null);
        }
        setActiveTabState('login');
        if (typeof window !== 'undefined' && window.history && window.history.pushState) {
          window.history.pushState({}, '', '/yonetim/giris');
        }
        showToast('Güvenli Şekilde Oturum Kapatıldı');
      }, []);"""

    if old_logout in content:
        content = content.replace(old_logout, new_logout)
        print(f"Updated handleLogout in {h_file}")

    # 5. Ensure management route strictly checks sessionUser
    old_mgmt_route_check = """      // 3. LOGIN REQUIRED FOR MANAGEMENT ROUTES (WHEN UNAUTHENTICATED & NOT GUEST MEDIA)
      if (isManagementRoute && !sessionUser && !isMediaRoute && !isErrorRoute) {"""

    new_mgmt_route_check = """      // 3. LOGIN REQUIRED FOR MANAGEMENT ROUTES (WHEN UNAUTHENTICATED & NOT GUEST MEDIA)
      if ((isManagementRoute || pathname.startsWith('/yonetim')) && !sessionUser && !isMediaRoute && !isErrorRoute) {"""

    if old_mgmt_route_check in content:
        content = content.replace(old_mgmt_route_check, new_mgmt_route_check)
        print(f"Strengthened management route gatekeeper in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully processed {h_file}!")

print("All authentication lifecycle and RBAC fixes applied successfully!")
