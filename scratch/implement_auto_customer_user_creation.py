import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update onSaveReservation in App component to auto-create 'musteri' role user account in db_users.json
old_onsave = """                      onSaveReservation={(newRes, newCust, refKeyToRemove, isEdit) => {
                        if (newCust) setCustomers(prev => [...prev, newCust]);"""

new_onsave = """                      onSaveReservation={(newRes, newCust, refKeyToRemove, isEdit) => {
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
                        }"""

if old_onsave in content:
    content = content.replace(old_onsave, new_onsave)
    print("1. Added automatic 'musteri' user account creation to onSaveReservation in App component.")
else:
    print("WARNING: Could not find old_onsave exact match in index.html!")

# 2. Update CustomerFormModal onSave in CustomerComponent to auto-create 'musteri' role user account
old_cust_save = """              onSave={(c) => {
                setCustomers(prev => c.id ? prev.map(x => x.id === c.id ? c : x) : [...prev, { ...c, id: 'cust-' + Date.now(), avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80' }]);
                showToast('Müşteri Kartı Başarıyla Kaydedildi!');
                setCustomerModalData(null);
              }}"""

new_cust_save = """              onSave={(c) => {
                const isNew = !c.id;
                const finalCust = c.id ? c : { ...c, id: 'cust-' + Date.now(), avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80' };
                setCustomers(prev => c.id ? prev.map(x => x.id === c.id ? c : x) : [...prev, finalCust]);
                if (isNew) {
                  const newCustUser = {
                    id: 'u-' + finalCust.id,
                    name: finalCust.name || 'Müşteri',
                    email: finalCust.email || `musteri_${Date.now()}@iremdugun.com`,
                    phone: finalCust.phone || '',
                    role: 'musteri',
                    roleName: 'Müşteri',
                    status: 'Aktif',
                    avatar: finalCust.avatar,
                    createdAt: new Date().toISOString()
                  };
                  setUsers(prev => [...(prev || []).filter(u => u.email !== newCustUser.email && u.id !== newCustUser.id), newCustUser]);
                }
                showToast('Müşteri Kartı ve Müşteri Üyeliği Başarıyla Oluşturuldu!');
                setCustomerModalData(null);
              }}"""

if old_cust_save in content:
    content = content.replace(old_cust_save, new_cust_save)
    print("2. Added automatic 'musteri' user account creation to CustomerComponent onSave.")
else:
    print("WARNING: Could not find old_cust_save exact match in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
