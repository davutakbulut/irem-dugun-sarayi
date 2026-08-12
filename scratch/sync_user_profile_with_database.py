import os

files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

# Standard avatar URL for Davut Akbulut / Admin
STANDARD_AVATAR = 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'
OLD_AVATAR = 'https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=200&q=80'

for f_path in files:
    if not os.path.exists(f_path):
        continue
    with open(f_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace hardcoded old avatar in initial state
    content = content.replace(OLD_AVATAR, STANDARD_AVATAR)

    # 2. In fetchSystemSettings -> fetchFn('/api/users'), automatically sync currentUserState with MySQL DB user!
    old_users_fetch = """            // Fetch Users
            fetchFn('/api/users')
              .then(res => res.json())
              .then(data => {
                if (Array.isArray(data)) {
                  lastSyncedUsersRef.current = JSON.stringify(data);
                  setUsers(data);
                }
              })
              .catch(() => {});"""

    new_users_fetch = """            // Fetch Users & Sync Active User Profile from Database
            fetchFn('/api/users')
              .then(res => res.json())
              .then(data => {
                if (Array.isArray(data) && data.length > 0) {
                  lastSyncedUsersRef.current = JSON.stringify(data);
                  setUsers(data);

                  // Auto-sync active user with MySQL Database
                  const activeEmail = (currentUserState?.email || 'dvtakblt@gmail.com').toLowerCase().trim();
                  const activeId = currentUserState?.id;
                  const dbMatch = data.find(u => (activeId && u.id === activeId) || (u.email && u.email.toLowerCase().trim() === activeEmail) || u.role === 'admin');
                  if (dbMatch) {
                    const mergedUser = { ...currentUserState, ...dbMatch };
                    if (JSON.stringify(mergedUser) !== JSON.stringify(currentUserState)) {
                      setCurrentUserState(mergedUser);
                      CacheService.set('current_user', mergedUser);
                    }
                  }
                }
              })
              .catch(() => {});"""

    if old_users_fetch in content:
        content = content.replace(old_users_fetch, new_users_fetch)
        print(f"Successfully updated /api/users sync in {f_path}!")

    with open(f_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Finished updating user profile database sync across all HTML files!")
