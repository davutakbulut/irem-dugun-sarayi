import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix the top script that cleans localStorage so it NEVER touches session_user or current_user
    old_top_clean = """    try {
      if (typeof localStorage !== 'undefined') {
        const preserveKeys = ['session_user', 'current_user', 'auth_token'];
        Object.keys(localStorage).forEach(k => {
          if (!preserveKeys.includes(k) && !k.startsWith('auth')) {
            localStorage.removeItem(k);
          }
        });
      }
    } catch(e){}"""

    new_top_clean = """    try {
      if (typeof localStorage !== 'undefined') {
        Object.keys(localStorage).forEach(k => {
          if (!k.includes('session_user') && !k.includes('current_user') && !k.startsWith('auth')) {
            localStorage.removeItem(k);
          }
        });
      }
    } catch(e){}"""

    if old_top_clean in content:
        content = content.replace(old_top_clean, new_top_clean)
        print(f"Protected session keys in top boot script in {h_file}")

    # 2. Add getInitialSessionUser helper before App
    session_helper = """    function getInitialSessionUser() {
      if (typeof localStorage === 'undefined') return null;
      try {
        const raw = localStorage.getItem('irem_session_user') || localStorage.getItem('irem_cache_session_user') || localStorage.getItem('session_user');
        if (raw) {
          const parsed = JSON.parse(raw);
          if (parsed && parsed.name) return parsed;
        }
      } catch(e){}
      return null;
    }
"""

    if "function getInitialSessionUser()" not in content:
        content = content.replace("function App() {", session_helper + "\n    function App() {")
        print(f"Added getInitialSessionUser in {h_file}")

    # 3. Update sessionUser state initialization in App
    old_session_init = "const [sessionUser, setSessionUser] = useState(() => CacheService.get('session_user', null));"
    new_session_init = "const [sessionUser, setSessionUser] = useState(getInitialSessionUser);"

    if old_session_init in content:
        content = content.replace(old_session_init, new_session_init)
        print(f"Updated sessionUser init in {h_file}")

    # 4. Synchronize session storage on login and logout
    old_set_session_login = """              setSessionUser(userObj);
              CacheService.set('session_user', userObj);
              setCurrentUserState(userObj);
              CacheService.set('current_user', userObj);"""

    new_set_session_login = """              setSessionUser(userObj);
              try {
                localStorage.setItem('irem_session_user', JSON.stringify(userObj));
                localStorage.setItem('irem_cache_session_user', JSON.stringify(userObj));
              } catch(e){}
              CacheService.set('session_user', userObj);
              setCurrentUserState(userObj);
              CacheService.set('current_user', userObj);"""

    if old_set_session_login in content:
        content = content.replace(old_set_session_login, new_set_session_login)
        print(f"Updated login session persistence in {h_file}")

    old_logout_block = """      const handleLogout = useCallback(() => {
        setSessionUser(null);
        CacheService.set('session_user', null);"""

    new_logout_block = """      const handleLogout = useCallback(() => {
        setSessionUser(null);
        try {
          localStorage.removeItem('irem_session_user');
          localStorage.removeItem('irem_cache_session_user');
          localStorage.removeItem('session_user');
          sessionStorage.clear();
        } catch(e){}
        CacheService.set('session_user', null);"""

    if old_logout_block in content:
        content = content.replace(old_logout_block, new_logout_block)
        print(f"Updated logout session purge in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully processed {h_file}!")

print("All persistent auth session fixes applied successfully!")
