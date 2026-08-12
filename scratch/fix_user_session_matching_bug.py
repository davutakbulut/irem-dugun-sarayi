import os

files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for f_path in files:
    if not os.path.exists(f_path):
        continue
    with open(f_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace dangerous dbMatch logic in fetchUsers
    old_db_match = """                  // Auto-sync active user with MySQL Database
                  const activeEmail = (currentUserState?.email || 'dvtakblt@gmail.com').toLowerCase().trim();
                  const activeId = currentUserState?.id;
                  const dbMatch = data.find(u => (activeId && u.id === activeId) || (u.email && u.email.toLowerCase().trim() === activeEmail) || u.role === 'admin');
                  if (dbMatch) {
                    const mergedUser = { ...currentUserState, ...dbMatch };
                    if (JSON.stringify(mergedUser) !== JSON.stringify(currentUserState)) {
                      setCurrentUserState(mergedUser);
                      CacheService.set('current_user', mergedUser);
                    }
                  }"""

    new_db_match = """                  // Strict Auto-sync for active logged-in user ONLY (no arbitrary role fallbacks)
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

    if old_db_match in content:
        content = content.replace(old_db_match, new_db_match)
        print(f"Successfully fixed dbMatch in {f_path}!")
    else:
        print(f"old_db_match not found in {f_path}!")

    # 2. Fix initial currentUserState default if it contained Mustafa Beyazyüz
    old_init_user = """      const [currentUserState, setCurrentUserState] = useState(() => CacheService.get('current_user', {
        id: 'u0',
        name: 'Mustafa Beyazyüz',
        email: 'mustafa@iremdugunsarayi.com',
        phone: '+90 547 144 00 54',
        role: 'admin',
        avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'
      }));"""

    new_init_user = """      const [currentUserState, setCurrentUserState] = useState(() => CacheService.get('current_user', {
        id: 'u_davut',
        name: 'Davut Akbulut',
        email: 'dvtakblt@gmail.com',
        phone: '+90 537 882 68 58',
        role: 'admin',
        avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'
      }));"""

    if old_init_user in content:
        content = content.replace(old_init_user, new_init_user)
        print(f"Successfully fixed default currentUserState in {f_path}!")

    with open(f_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Finished fixing session user matching bug across all HTML files!")
