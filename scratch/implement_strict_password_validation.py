import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_auth_code = """          // 1. Search in Users DB
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
          }"""

new_auth_code = """          const enteredPassword = (password || '').trim();

          if (!enteredPassword) {
            showToast('⛔ GİRİŞ BAŞARISIZ: Lütfen şifrenizi giriniz.', 'error');
            return;
          }

          // 1. Search in Users DB
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
          
          // STRICT IDENTITY GUARD: REJECT IF NEITHER USER NOR CUSTOMER IS FOUND IN DATABASE
          if (!matchedUser && !matchedCustomer) {
            showToast('⛔ GİRİŞ BAŞARISIZ: Yazdığınız e-posta adresi veya telefon numarası veritabanımızda kayıtlı değil!', 'error');
            return;
          }

          // STRICT PASSWORD GUARD: VERIFY PASSWORD MATCH AGAINST DB RECORD
          if (matchedUser && matchedUser.password && matchedUser.password !== enteredPassword) {
            showToast('⛔ GİRİŞ BAŞARISIZ: Hatalı şifre girdiniz! Lütfen şifrenizi kontrol ediniz.', 'error');
            return;
          }

          if (matchedCustomer && matchedCustomer.password && matchedCustomer.password !== enteredPassword) {
            showToast('⛔ GİRİŞ BAŞARISIZ: Hatalı şifre girdiniz! Lütfen şifrenizi kontrol ediniz.', 'error');
            return;
          }"""

if old_auth_code in content:
    content = content.replace(old_auth_code, new_auth_code)
    print("1. Successfully implemented strict password validation guard in LoginComponent!")
else:
    print("WARNING: Could not find old_auth_code in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
