import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_login_matching = """          // 1. Search in Users DB
          const userList = (users && users.length > 0) ? users : (typeof INITIAL_USERS !== 'undefined' ? INITIAL_USERS : []);
          const matchedUser = userList.find(u => 
            (u.email || '').toLowerCase().trim() === valLower || 
            (u.phone && u.phone.replace(/\\D/g, '') === cleanPhoneVal && cleanPhoneVal.length >= 10)
          );

          // 2. Search in Customers DB
          const customerList = (customers && customers.length > 0) ? customers : [];
          const matchedCustomer = customerList.find(c => 
            (c.email || '').toLowerCase().trim() === valLower || 
            (c.phone && c.phone.replace(/\\D/g, '') === cleanPhoneVal && cleanPhoneVal.length >= 10)
          );
          
          let derivedRole = 'admin';
          let displayName = valLower.split('@')[0] || 'Kullanıcı';

          if (matchedUser && matchedUser.role) {
            derivedRole = matchedUser.role;
            displayName = matchedUser.name;
          } else if (matchedCustomer) {
            derivedRole = 'musteri';
            displayName = matchedCustomer.name;
          } else if (valLower.includes('satis')) {
            derivedRole = 'satisci';
            displayName = 'Satış Yöneticisi';
          } else if (valLower.includes('sosyal')) {
            derivedRole = 'sosyal_medyaci';
            displayName = 'Sosyal Medya Sorumlusu';
          } else if (valLower.includes('ahmet') || valLower.includes('musteri') || valLower.includes('example.com') || valLower.includes('canan')) {
            derivedRole = 'musteri';
            displayName = 'Sayın Müşterimiz';
          }

          const user = {
            id: matchedUser?.id || (matchedCustomer ? `u-${matchedCustomer.id}` : `u-${derivedRole}`),
            name: matchedUser?.name || matchedCustomer?.name || displayName,
            email: emailInput || matchedUser?.email || matchedCustomer?.email || 'user@iremdugunsarayi.com',
            phone: phoneInput || matchedUser?.phone || matchedCustomer?.phone || '0532 123 4567',
            role: derivedRole,
            avatar: matchedUser?.avatar || matchedCustomer?.avatar || 'https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=200&q=80'
          };"""

new_login_matching = """          // 1. Search in Users DB
          const userList = (users && users.length > 0) ? users : (typeof INITIAL_USERS !== 'undefined' ? INITIAL_USERS : []);
          const matchedUser = userList.find(u => 
            (u.email || '').toLowerCase().trim() === valLower || 
            (u.phone && u.phone.replace(/\\D/g, '') === cleanPhoneVal && cleanPhoneVal.length >= 10)
          );

          // 2. Search in Customers DB
          const customerList = (customers && customers.length > 0) ? customers : [];
          const matchedCustomer = customerList.find(c => 
            (c.email || '').toLowerCase().trim() === valLower || 
            (c.phone && c.phone.replace(/\\D/g, '') === cleanPhoneVal && cleanPhoneVal.length >= 10)
          );
          
          // STRICT AUTHENTICATION GUARD: REJECT IF NEITHER USER NOR CUSTOMER IS FOUND IN DATABASE
          if (!matchedUser && !matchedCustomer) {
            showToast('⛔ GİRİŞ BAŞARISIZ: Yazdığınız e-posta adresi veya telefon numarası veritabanımızda bulunamadı! Lütfen kaydolun veya bilgilerinizi kontrol ediniz.', 'error');
            return;
          }

          let derivedRole = matchedUser ? (matchedUser.role || 'admin') : 'musteri';
          let displayName = matchedUser ? matchedUser.name : (matchedCustomer ? matchedCustomer.name : 'Müşteri');

          const user = {
            id: matchedUser?.id || `u-${matchedCustomer?.id || Date.now()}`,
            name: displayName,
            email: matchedUser?.email || matchedCustomer?.email || emailInput,
            phone: matchedUser?.phone || matchedCustomer?.phone || phoneInput,
            role: derivedRole,
            avatar: matchedUser?.avatar || matchedCustomer?.avatar || 'https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=200&q=80'
          };"""

if old_login_matching in content:
    content = content.replace(old_login_matching, new_login_matching)
    print("1. Successfully implemented strict database user & customer login verification guard!")
else:
    print("WARNING: Could not find old_login_matching in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
