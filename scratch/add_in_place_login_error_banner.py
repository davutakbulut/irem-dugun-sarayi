import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add errorMessage state to LoginComponent
old_states = """      const [showForgotModal, setShowForgotModal] = useState(false);
      const [showHelpModal, setShowHelpModal] = useState(false);
      const [forgotSuccessMail, setForgotSuccessMail] = useState(null);
      const [forgotInput, setForgotInput] = useState('');"""

new_states = """      const [showForgotModal, setShowForgotModal] = useState(false);
      const [showHelpModal, setShowHelpModal] = useState(false);
      const [forgotSuccessMail, setForgotSuccessMail] = useState(null);
      const [forgotInput, setForgotInput] = useState('');
      const [errorMessage, setErrorMessage] = useState('');"""

if old_states in content:
    content = content.replace(old_states, new_states)
    print("1. Added errorMessage state to LoginComponent.")

# 2. Update handleFormSubmit validations to setErrorMessage
old_submit_logic = """      const handleFormSubmit = (e) => {
        e.preventDefault();
        if (!inputValidation.isValid) {
          showToast(`Lütfen geçerli bir ${loginMethod === 'email' ? 'e-posta adresi' : 'telefon numarası'} giriniz.`, 'error');
          return;
        }
        setIsLoading(true);
        setTimeout(() => {
          setIsLoading(false);
          const valLower = (activeValue || '').toLowerCase().trim();
          const cleanPhoneVal = (phoneInput || '').replace(/\D/g, '');

          const enteredPassword = (password || '').trim();

          if (!enteredPassword) {
            showToast('⛔ GİRİŞ BAŞARISIZ: Lütfen şifrenizi giriniz.', 'error');
            return;
          }

          // 1. Search in Users DB
          const userList = (users && users.length > 0) ? users : (typeof INITIAL_USERS !== 'undefined' ? INITIAL_USERS : []);
          const matchedUser = userList.find(u => 
            (u.email || '').toLowerCase().trim() === valLower || 
            (u.phone && u.phone.replace(/\D/g, '') === cleanPhoneVal && cleanPhoneVal.length >= 10)
          );

          // 2. Search in Customers DB
          const customerList = (customers && customers.length > 0) ? customers : [];
          const matchedCustomer = customerList.find(c => 
            (c.email || '').toLowerCase().trim() === valLower || 
            (c.phone && c.phone.replace(/\D/g, '') === cleanPhoneVal && cleanPhoneVal.length >= 10)
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

new_submit_logic = """      const handleFormSubmit = (e) => {
        e.preventDefault();
        setErrorMessage('');
        if (!inputValidation.isValid) {
          const msg = `Geçerli bir ${loginMethod === 'email' ? 'e-posta adresi' : 'telefon numarası'} giriniz.`;
          setErrorMessage(msg);
          showToast(msg, 'error');
          return;
        }
        setIsLoading(true);
        setTimeout(() => {
          setIsLoading(false);
          const valLower = (activeValue || '').toLowerCase().trim();
          const cleanPhoneVal = (phoneInput || '').replace(/\D/g, '');
          const enteredPassword = (password || '').trim();

          if (!enteredPassword) {
            setErrorMessage('Lütfen şifrenizi giriniz.');
            showToast('⛔ GİRİŞ BAŞARISIZ: Lütfen şifrenizi giriniz.', 'error');
            return;
          }

          // 1. Search in Users DB
          const userList = (users && users.length > 0) ? users : (typeof INITIAL_USERS !== 'undefined' ? INITIAL_USERS : []);
          const matchedUser = userList.find(u => 
            (u.email || '').toLowerCase().trim() === valLower || 
            (u.phone && u.phone.replace(/\D/g, '') === cleanPhoneVal && cleanPhoneVal.length >= 10)
          );

          // 2. Search in Customers DB
          const customerList = (customers && customers.length > 0) ? customers : [];
          const matchedCustomer = customerList.find(c => 
            (c.email || '').toLowerCase().trim() === valLower || 
            (c.phone && c.phone.replace(/\D/g, '') === cleanPhoneVal && cleanPhoneVal.length >= 10)
          );
          
          // STRICT IDENTITY GUARD: REJECT IF NEITHER USER NOR CUSTOMER IS FOUND IN DATABASE
          if (!matchedUser && !matchedCustomer) {
            const err = 'Yazdığınız e-posta adresi veya telefon numarası veritabanımızda bulunamadı!';
            setErrorMessage(err);
            showToast(`⛔ GİRİŞ BAŞARISIZ: ${err}`, 'error');
            return;
          }

          // STRICT PASSWORD GUARD: VERIFY PASSWORD MATCH AGAINST DB RECORD
          if (matchedUser && matchedUser.password && matchedUser.password !== enteredPassword) {
            const err = 'Girilen şifre hatalı! Lütfen şifrenizi kontrol ediniz.';
            setErrorMessage(err);
            showToast(`⛔ GİRİŞ BAŞARISIZ: ${err}`, 'error');
            return;
          }

          if (matchedCustomer && matchedCustomer.password && matchedCustomer.password !== enteredPassword) {
            const err = 'Girilen şifre hatalı! Lütfen şifrenizi kontrol ediniz.';
            setErrorMessage(err);
            showToast(`⛔ GİRİŞ BAŞARISIZ: ${err}`, 'error');
            return;
          }"""

if old_submit_logic in content:
    content = content.replace(old_submit_logic, new_submit_logic)
    print("2. Updated handleFormSubmit to set errorMessage state.")

# 3. Add Red Alert Error Banner inside login form
old_form_start = """              {/* FORM */}
              <form onSubmit={handleFormSubmit} className="space-y-4 text-xs pt-1">"""

new_form_start = """              {/* FORM */}
              <form onSubmit={handleFormSubmit} className="space-y-4 text-xs pt-1">
                
                {/* IN-PLACE RED ALERT ERROR BANNER */}
                {errorMessage && (
                  <div className="bg-red-500/10 border-2 border-red-500/60 p-3.5 rounded-2xl flex items-center space-x-3 text-red-700 dark:text-red-300 text-xs font-bold shadow-md animate-bounce-subtle mb-4">
                    <div className="w-8 h-8 rounded-xl bg-red-500/20 flex items-center justify-center shrink-0">
                      <ThemeIcon icon="warning" className="w-5 h-5 text-red-500 shrink-0" />
                    </div>
                    <div className="flex-1">
                      <span className="block font-black text-red-800 dark:text-red-200">Giriş Başarısız!</span>
                      <span className="font-medium text-[11px] opacity-90">{errorMessage}</span>
                    </div>
                    <button type="button" onClick={() => setErrorMessage('')} className="text-red-400 hover:text-red-600 p-1">
                      <ThemeIcon icon="x" className="w-4 h-4 shrink-0" />
                    </button>
                  </div>
                )}"""

if old_form_start in content:
    content = content.replace(old_form_start, new_form_start)
    print("3. Added In-Place Red Alert Error Banner to login form.")

# 4. Clear errorMessage on input onChange
content = content.replace("onChange={e => setEmailInput(e.target.value)}", "onChange={e => { setEmailInput(e.target.value); if (errorMessage) setErrorMessage(''); }}")
content = content.replace("onChange={e => setPhoneInput(e.target.value)}", "onChange={e => { setPhoneInput(e.target.value); if (errorMessage) setErrorMessage(''); }}")
content = content.replace("onChange={e => setPassword(e.target.value)}", "onChange={e => { setPassword(e.target.value); if (errorMessage) setErrorMessage(''); }}")

print("4. Updated input onChange handlers to clear errorMessage.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
