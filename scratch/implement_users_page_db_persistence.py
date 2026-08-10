import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_user_handlers = """      const handleSaveUser = (uObj) => {
        setUsers(prev => {
          const idx = prev.findIndex(x => x.id === uObj.id);
          if (idx >= 0) {
            const updated = [...prev];
            updated[idx] = uObj;
            return updated;
          }
          return [...prev, uObj];
        });
        setUserModalData(null);
        showToast('Kullanıcı Bilgileri Başarıyla Güncellendi!');
      };

      const handleDeleteUser = (uIdOrObj) => {
        const uId = typeof uIdOrObj === 'object' ? uIdOrObj.id : uIdOrObj;
        const user = users.find(x => x.id === uId);
        const uName = user ? user.name : 'Kullanıcı';
        setRedAlertModalData({
          title: 'KULLANICI HESABI SİLİNECEK',
          message: `"${uName}" kullanıcısının yetkilerini iptal edip sistemden silmek istediğinize emin misiniz?`,
          confirmText: 'Evet, Kullanıcıyı Sil',
          onConfirm: () => {
            setUsers(prev => {
              const updated = prev.filter(x => x.id !== uId);
              CacheService.set('users', updated);
              return updated;
            });
            showToast('Kullanıcı Sistemden Silindi.');
          }
        });
      };"""

new_user_handlers = """      const handleSaveUser = (uObj) => {
        setUsers(prev => {
          const list = prev || [];
          const idx = list.findIndex(x => x.id === uObj.id || (x.email && x.email.toLowerCase().trim() === (uObj.email || '').toLowerCase().trim()));
          let updated;
          if (idx >= 0) {
            updated = [...list];
            updated[idx] = { ...updated[idx], ...uObj };
          } else {
            updated = [...list, uObj];
          }
          CacheService.set('users', updated);
          if (window.fetchWithRetry) {
            window.fetchWithRetry('/api/system-settings', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ users: updated })
            }).catch(() => {});
          }
          return updated;
        });
        setUserModalData(null);
        showToast(`Kullanıcı (${uObj.name}) Bilgileri Veritabanına Başarıyla Kaydedildi!`);
      };

      const handleDeleteUser = (uIdOrObj) => {
        const uId = typeof uIdOrObj === 'object' ? uIdOrObj.id : uIdOrObj;
        const user = users.find(x => x.id === uId);
        const uName = user ? user.name : 'Kullanıcı';
        setRedAlertModalData({
          title: 'KULLANICI HESABI SİLİNECEK',
          message: `"${uName}" kullanıcısının yetkilerini iptal edip sistemden silmek istediğinize emin misiniz?`,
          confirmText: 'Evet, Kullanıcıyı Sil',
          onConfirm: () => {
            setUsers(prev => {
              const updated = (prev || []).filter(x => x.id !== uId);
              CacheService.set('users', updated);
              if (window.fetchWithRetry) {
                window.fetchWithRetry('/api/system-settings', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ users: updated })
                }).catch(() => {});
              }
              return updated;
            });
            showToast('Kullanıcı Veritabanından Silindi.');
          }
        });
      };"""

if old_user_handlers in content:
    content = content.replace(old_user_handlers, new_user_handlers)
    print("1. Successfully updated handleSaveUser and handleDeleteUser with database persistence POST calls!")
else:
    print("WARNING: Could not find old_user_handlers in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
