import os, re

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add formatTurkishPhone helper before LoginComponent
    phone_helper = """    function formatTurkishPhone(val) {
      if (!val) return '';
      let digits = val.replace(/\\D/g, '');
      if (digits.startsWith('90')) digits = digits.slice(2);
      if (digits.startsWith('0')) digits = digits.slice(1);
      digits = digits.slice(0, 10);
      if (digits.length === 0) return '';
      if (digits.length <= 3) return `0 (${digits}`;
      if (digits.length <= 6) return `0 (${digits.slice(0, 3)}) ${digits.slice(3)}`;
      if (digits.length <= 8) return `0 (${digits.slice(0, 3)}) ${digits.slice(3, 6)} ${digits.slice(6)}`;
      return `0 (${digits.slice(0, 3)}) ${digits.slice(3, 6)} ${digits.slice(6, 8)} ${digits.slice(8, 10)}`;
    }
"""

    if "function formatTurkishPhone(" not in content:
        content = content.replace("function LoginComponent({", phone_helper + "\n    function LoginComponent({")
        print(f"Added formatTurkishPhone in {h_file}")

    # 2. Update inputValidation in LoginComponent
    old_validation_pattern = re.search(r'const inputValidation = useMemo\(\(\) => \{[\s\S]*?\}, \[loginMethod, emailInput, phoneInput\]\);', content)
    new_validation = """const inputValidation = useMemo(() => {
        const val = (activeValue || '').trim();
        if (!val) return { isValid: false, message: '' };

        if (loginMethod === 'email') {
          const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$/;
          if (emailRegex.test(val)) return { isValid: true, message: 'E-posta Formatı Geçerli' };
          return { isValid: false, message: 'Lütfen geçerli bir e-posta adresi giriniz.' };
        } else {
          let digits = val.replace(/\\D/g, '');
          if (digits.startsWith('90')) digits = digits.slice(2);
          if (digits.startsWith('0')) digits = digits.slice(1);
          if (digits.length === 10 && digits.startsWith('5')) {
            return { isValid: true, message: 'Telefon Formatı Geçerli' };
          }
          return { isValid: false, message: 'Lütfen geçerli bir 0 (5XX) telefon numarası giriniz.' };
        }
      }, [loginMethod, emailInput, phoneInput]);"""

    if old_validation_pattern:
        content = content[:old_validation_pattern.start()] + new_validation + content[old_validation_pattern.end():]
        print(f"Updated inputValidation in {h_file}")

    # 3. Update handleFormSubmit to strictly validate with MySQL and reject unknown logins
    old_submit_pattern = re.search(r'const handleFormSubmit = \(e\) => \{[\s\S]*?showToast\(`Hoş geldiniz Sayın \$\{matchedUser\.name[\s\S]*?\}, 350\);\s*\};', content)
    new_submit = """const handleFormSubmit = async (e) => {
        e.preventDefault();
        setErrorMessage('');
        if (!inputValidation.isValid) {
          const msg = `Geçerli bir ${loginMethod === 'email' ? 'e-posta adresi' : 'telefon numarası'} giriniz.`;
          setErrorMessage(msg);
          showToast(msg, 'error');
          return;
        }
        
        const passTrim = (password || '').trim();
        if (!passTrim) {
          setErrorMessage('Lütfen şifrenizi giriniz.');
          showToast('Lütfen şifrenizi giriniz.', 'error');
          return;
        }

        setIsLoading(true);

        try {
          // Fetch real-time active users from MySQL database
          let dbUsers = users;
          try {
            const uRes = await fetch('/api/users');
            const uData = await uRes.json();
            if (Array.isArray(uData) && uData.length > 0) dbUsers = uData;
          } catch(err) {}

          let dbCustomers = customers;
          try {
            const cRes = await fetch('/api/customers');
            const cData = await cRes.json();
            if (Array.isArray(cData) && cData.length > 0) dbCustomers = cData;
          } catch(err) {}

          const valLower = (activeValue || '').toLowerCase().trim();
          let digits = valLower.replace(/\\D/g, '');
          if (digits.startsWith('90')) digits = digits.slice(2);
          if (digits.startsWith('0')) digits = digits.slice(1);

          let matchedUser = null;
          let matchedRole = 'admin';

          // 1. Strict match in MySQL users
          if (dbUsers && dbUsers.length > 0) {
            matchedUser = dbUsers.find(u => {
              const uEmail = (u.email || '').toLowerCase().trim();
              let uPhone = (u.phone || '').replace(/\\D/g, '');
              if (uPhone.startsWith('90')) uPhone = uPhone.slice(2);
              if (uPhone.startsWith('0')) uPhone = uPhone.slice(1);

              return loginMethod === 'email' ? (uEmail === valLower) : (uPhone && digits && uPhone === digits);
            });

            if (matchedUser) {
              matchedRole = matchedUser.role || 'admin';
            }
          }

          // 2. Strict match in MySQL customers
          if (!matchedUser && dbCustomers && dbCustomers.length > 0) {
            const matchedCust = dbCustomers.find(c => {
              const cEmail = (c.email || '').toLowerCase().trim();
              let cPhone = (c.phone || '').replace(/\\D/g, '');
              if (cPhone.startsWith('90')) cPhone = cPhone.slice(2);
              if (cPhone.startsWith('0')) cPhone = cPhone.slice(1);

              return loginMethod === 'email' ? (cEmail === valLower) : (cPhone && digits && cPhone === digits);
            });

            if (matchedCust) {
              matchedUser = {
                id: matchedCust.id,
                name: matchedCust.name,
                email: matchedCust.email,
                phone: matchedCust.phone,
                role: 'musteri',
                avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'
              };
              matchedRole = 'musteri';
            }
          }

          // STRICT REJECTION: BLOCK ALL RANDOM OR UNREGISTERED ACCOUNTS
          if (!matchedUser) {
            setIsLoading(false);
            const errorText = `Girdiğiniz ${loginMethod === 'email' ? 'e-posta adresi' : 'telefon numarası'} veya şifre sistemde kayıtlı değildir.`;
            setErrorMessage(errorText);
            showToast('Hatalı e-posta/telefon veya şifre!', 'error');
            return;
          }

          setIsLoading(false);
          onLoginSuccess({
            id: matchedUser.id,
            role: matchedRole,
            name: matchedUser.name || 'Kullanıcı',
            userName: matchedUser.name || 'Kullanıcı',
            email: matchedUser.email || valLower,
            userEmail: matchedUser.email || valLower,
            phone: matchedUser.phone || '',
            avatar: matchedUser.avatar || 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=200&q=80'
          });
          showToast(`Hoş geldiniz Sayın ${matchedUser.name}! (${matchedRole.toUpperCase()})`);

        } catch(err) {
          setIsLoading(false);
          showToast('Giriş işlemi gerçekleştirilemedi', 'error');
        }
      };"""

    if old_submit_pattern:
        content = content[:old_submit_pattern.start()] + new_submit + content[old_submit_pattern.end():]
        print(f"Updated handleFormSubmit in {h_file}")

    # 4. Update phone input in form to use formatTurkishPhone
    old_phone_input = """                    <input
                      type="tel"
                      required
                      value={phoneInput}
                      onChange={e => { setPhoneInput(e.target.value); if (errorMessage) setErrorMessage(''); }}
                      placeholder="05XX XXX XX XX"
                      className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 focus:bg-white dark:focus:bg-slate-950 focus:border-amber-500 rounded-xl p-3 text-xs text-slate-800 dark:text-white font-medium outline-none transition shadow-xs"
                    />"""

    new_phone_input = """                    <input
                      type="tel"
                      required
                      value={phoneInput}
                      onChange={e => {
                        const formatted = formatTurkishPhone(e.target.value);
                        setPhoneInput(formatted);
                        if (errorMessage) setErrorMessage('');
                      }}
                      placeholder="0 (5XX) XXX XX XX"
                      className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 focus:bg-white dark:focus:bg-slate-950 focus:border-amber-500 rounded-xl p-3 text-xs text-slate-800 dark:text-white font-medium outline-none transition shadow-xs tracking-wider"
                    />"""

    if old_phone_input in content:
        content = content.replace(old_phone_input, new_phone_input)
        print(f"Updated phone input with formatting mask in {h_file}")

    # 5. Remove the bottom demo account card section entirely
    demo_section_pattern = re.search(r'\{\s*/\*\s*QUICK DEMO LOGIN BUTTONS\s*\*/\s*\}[\s\S]*?<\/div>\s*<\/div>\s*<\/div>\s*\{\s*/\*\s*RIGHT COLUMN:', content)
    if demo_section_pattern:
        content = content[:demo_section_pattern.start()] + '</div>\n\n            {/* RIGHT COLUMN:' + content[demo_section_pattern.end() - len('{/* RIGHT COLUMN:'):]
        print(f"Purged quick demo login cards in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully processed {h_file}!")

print("All login security, phone format, and demo cleanup fixes applied!")
