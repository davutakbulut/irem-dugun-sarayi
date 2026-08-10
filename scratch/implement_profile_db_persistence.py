import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Include password in ProfileComponent onSaveProfile payload if password is typed
old_profile_save = """        onSaveProfile({
          name,
          email,
          phone,
          avatar,
          role: selectedRole
        });"""

new_profile_save = """        const profilePayload = {
          name,
          email,
          phone,
          avatar,
          role: selectedRole
        };
        if (password && password.trim()) {
          profilePayload.password = password.trim();
        }
        onSaveProfile(profilePayload);"""

if old_profile_save in content:
    content = content.replace(old_profile_save, new_profile_save)
    print("1. Updated ProfileComponent handleSave payload.")

# 2. Update onSaveProfile callback in App component to persist to users DB (db_users.json)
old_onsave_profile = """                  {activeTab === 'profile' && (
                    <ProfileComponent
                      currentUser={currentUserState}
                      activeRole={activeRole}
                      onSaveProfile={(updated) => {
                        setCurrentUserState(prev => ({ ...prev, ...updated }));
                        showToast(`Profil Bilgileri (${updated.name}) Başarıyla Güncellendi!`);
                      }}
                      showToast={showToast}
                      onRoleChange={(newRole) => {
                        setActiveRole(newRole);
                        showToast(`Rol Değiştirildi: ${rolesState[newRole] || newRole}`);
                      }}
                    />
                  )}"""

new_onsave_profile = """                  {activeTab === 'profile' && (
                    <ProfileComponent
                      currentUser={currentUserState}
                      activeRole={activeRole}
                      onSaveProfile={(updated) => {
                        const updatedUserObj = { ...(currentUserState || {}), ...updated };
                        if (!updated.password && currentUserState?.password) {
                          updatedUserObj.password = currentUserState.password;
                        }
                        setCurrentUserState(updatedUserObj);
                        setSessionUser(updatedUserObj);
                        CacheService.set('session_user', updatedUserObj);
                        CacheService.set('current_user', updatedUserObj);

                        setUsers(prev => {
                          const list = prev || [];
                          const targetId = updatedUserObj.id || currentUserState?.id;
                          const targetEmail = (updatedUserObj.email || '').toLowerCase().trim();
                          const idx = list.findIndex(u => u.id === targetId || (u.email && u.email.toLowerCase().trim() === targetEmail));
                          let newUsers;
                          if (idx >= 0) {
                            newUsers = [...list];
                            newUsers[idx] = { ...newUsers[idx], ...updatedUserObj };
                          } else {
                            newUsers = [...list, updatedUserObj];
                          }
                          CacheService.set('users', newUsers);
                          if (window.fetchWithRetry) {
                            window.fetchWithRetry('/api/system-settings', {
                              method: 'POST',
                              headers: { 'Content-Type': 'application/json' },
                              body: JSON.stringify({ users: newUsers })
                            }).catch(() => {});
                          }
                          return newUsers;
                        });

                        showToast(`Profil Bilgileri (${updated.name}) Veritabanına Başarıyla Kaydedildi!`);
                      }}
                      showToast={showToast}
                      onRoleChange={(newRole) => {
                        setActiveRole(newRole);
                        showToast(`Rol Değiştirildi: ${rolesState[newRole] || newRole}`);
                      }}
                    />
                  )}"""

if old_onsave_profile in content:
    content = content.replace(old_onsave_profile, new_onsave_profile)
    print("2. Updated App component onSaveProfile callback with database persistence.")
else:
    print("WARNING: Could not find old_onsave_profile in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
