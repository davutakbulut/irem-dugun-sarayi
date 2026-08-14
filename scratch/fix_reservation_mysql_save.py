import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

old_on_save_block = """                      onSaveReservation={(newRes, newCust, refKeyToRemove, isEdit) => {
                        if (newCust) {
                          setCustomers(prev => [...prev, newCust]);
                          const newCustUser = {
                            id: 'u-' + (newCust.id || Date.now()),
                            name: newCust.name || 'Müşteri',
                            email: newCust.email || `musteri_${Date.now()}@iremdugun.com`,
                            phone: newCust.phone || '',
                            role: 'musteri',
                            roleName: 'Müşteri',
                            status: 'Aktif',
                            avatar: newCust.avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80',
                            createdAt: new Date().toISOString()
                          };
                          setUsers(prev => [...(prev || []).filter(u => u.email !== newCustUser.email && u.id !== newCustUser.id), newCustUser]);
                        }
                        
                        let targetId = newRes.id;
                        if (!targetId || targetId.startsWith('RES-DRAFT-')) {
                          targetId = `RES-${new Date().getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`;
                        }

                        const finalizedRes = {
                          ...newRes,
                          id: targetId,
                          status: 'CONFIRMED',
                          isDraft: false
                        };

                        setReservations(prev => {
                          const list = prev || [];
                          const cleanRef = refKeyToRemove || newRes.refKey;
                          const existingIdx = list.findIndex(r => r.id === finalizedRes.id || r.id === newRes.id || (cleanRef && r.refKey === cleanRef));
                          let updated;
                          if (existingIdx >= 0) {
                            updated = [...list];
                            updated[existingIdx] = finalizedRes;
                          } else {
                            updated = [finalizedRes, ...list.filter(r => r.id !== finalizedRes.id && r.id !== newRes.id && (!cleanRef || r.refKey !== cleanRef))];
                          }
                          CacheService.set('reservations', updated);
                          if (window.fetchWithRetry) {
                            window.fetchWithRetry('/api/public-settings', {
                              method: 'POST',
                              headers: { 'Content-Type': 'application/json' },
                              body: JSON.stringify({ reservations: updated })
                            }).catch(() => {});
                          }
                          return updated;
                        });

                        showToast(isEdit ? 'Rezervasyon ve Sözleşme Bilgileri Başarıyla Güncellendi!' : 'Yeni Rezervasyon ve Sözleşme Başarıyla Oluşturuldu!');
                        setPrefilledCreateDate(null);
                        navigateTo('reservations');
                      }}"""

new_on_save_block = """                      onSaveReservation={(newRes, newCust, refKeyToRemove, isEdit) => {
                        let targetId = newRes.id;
                        if (!targetId || targetId.startsWith('RES-DRAFT-')) {
                          targetId = `RES-${new Date().getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`;
                        }

                        const finalizedRes = {
                          ...newRes,
                          id: targetId,
                          status: 'CONFIRMED',
                          isDraft: false,
                          paymentStatus: newRes.paymentStatus || 'Bekliyor'
                        };

                        if (newCust) {
                          setCustomers(prev => [...(prev || []).filter(c => c.id !== newCust.id), newCust]);
                          const newCustUser = {
                            id: 'u-' + (newCust.id || Date.now()),
                            name: newCust.name || 'Müşteri',
                            email: newCust.email || `musteri_${Date.now()}@iremdugun.com`,
                            phone: newCust.phone || '',
                            role: 'musteri',
                            roleName: 'Müşteri',
                            status: 'Aktif',
                            avatar: newCust.avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80',
                            createdAt: new Date().toISOString()
                          };
                          setUsers(prev => [...(prev || []).filter(u => u.email !== newCustUser.email && u.id !== newCustUser.id), newCustUser]);
                          if (window.fetchWithRetry) {
                            window.fetchWithRetry('/api/customers', {
                              method: 'POST',
                              headers: { 'Content-Type': 'application/json' },
                              body: JSON.stringify(newCust)
                            }).catch(() => {});
                            window.fetchWithRetry('/api/users', {
                              method: 'POST',
                              headers: { 'Content-Type': 'application/json' },
                              body: JSON.stringify(newCustUser)
                            }).catch(() => {});
                          }
                        }

                        // DIRECT REALTIME MYSQL PERSISTENCE FOR RESERVATION
                        if (window.fetchWithRetry) {
                          window.fetchWithRetry('/api/reservations', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(finalizedRes)
                          }).catch(err => console.error('Reservation MySQL save error:', err));
                        }

                        setReservations(prev => {
                          const list = prev || [];
                          const cleanRef = refKeyToRemove || newRes.refKey;
                          const existingIdx = list.findIndex(r => r.id === finalizedRes.id || r.id === newRes.id || (cleanRef && r.refKey === cleanRef));
                          let updated;
                          if (existingIdx >= 0) {
                            updated = [...list];
                            updated[existingIdx] = finalizedRes;
                          } else {
                            updated = [finalizedRes, ...list.filter(r => r.id !== finalizedRes.id && r.id !== newRes.id && (!cleanRef || r.refKey !== cleanRef))];
                          }
                          return updated;
                        });

                        showToast(isEdit ? 'Rezervasyon ve Sözleşme Bilgileri Veritabanına Kaydedildi!' : 'Yeni Rezervasyon ve Sözleşme Veritabanına Başarıyla Kaydedildi!');
                        setPrefilledCreateDate(null);
                        navigateTo('reservations');
                      }}"""

old_delete_res = """      const handleDeleteReservation = (resId) => {
        setReservations(prev => {
          const updated = prev.filter(r => r.id !== resId);
          try {
            const fetchFn = window.fetchWithRetry || fetch;
            fetchFn('/api/public-settings', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ reservations: updated, updatedAt: new Date().toISOString(), updatedBy: 'admin' })
            }).catch(() => {});
          } catch(e) {}
          return updated;
        });
        showToast(`${resId} sözleşme kodlu rezervasyon veritabanından tamamen silindi.`);
      };"""

new_delete_res = """      const handleDeleteReservation = (resId) => {
        setReservations(prev => {
          const updated = prev.filter(r => r.id !== resId);
          try {
            const fetchFn = window.fetchWithRetry || fetch;
            fetchFn(`/api/reservations/${resId}`, {
              method: 'DELETE'
            }).catch(() => {});
          } catch(e) {}
          return updated;
        });
        showToast(`${resId} sözleşme kodlu rezervasyon veritabanından tamamen silindi.`);
      };"""

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_on_save_block in content:
        content = content.replace(old_on_save_block, new_on_save_block)
        print(f"Updated onSaveReservation MySQL call in {h_file}")

    if old_delete_res in content:
        content = content.replace(old_delete_res, new_delete_res)
        print(f"Updated handleDeleteReservation in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully processed {h_file}!")

print("All HTML files updated to directly persist reservations to MySQL!")
