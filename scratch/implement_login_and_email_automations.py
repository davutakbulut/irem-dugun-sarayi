import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update LoginComponent call in App component to pass customers={customers} and route 'musteri' role to customer portal
old_login_call = """          <LoginComponent
            users={users}
            showToast={showToast}
            onLoginSuccess={(userObj) => {
              let returnUrl = null;
              let returnTab = null;
              try {
                returnUrl = sessionStorage.getItem('login_return_url');
                returnTab = sessionStorage.getItem('login_return_tab');
                sessionStorage.removeItem('login_return_url');
                sessionStorage.removeItem('login_return_tab');
              } catch(e){}

              let targetTab = returnTab || 'dashboard';
              if (targetTab === 'login') targetTab = 'dashboard';
              
              let targetPath = returnUrl || (TAB_TO_PATH[targetTab] || '/yonetim');
              if (targetPath === '/giris' || targetPath === '/login') {
                targetPath = '/yonetim';
              }"""

new_login_call = """          <LoginComponent
            users={users}
            customers={customers}
            showToast={showToast}
            onLoginSuccess={(userObj) => {
              let returnUrl = null;
              let returnTab = null;
              try {
                returnUrl = sessionStorage.getItem('login_return_url');
                returnTab = sessionStorage.getItem('login_return_tab');
                sessionStorage.removeItem('login_return_url');
                sessionStorage.removeItem('login_return_tab');
              } catch(e){}

              const isCustomerRole = userObj.role === 'musteri';
              let targetTab = returnTab || (isCustomerRole ? 'musteri-portali' : 'dashboard');
              if (targetTab === 'login') targetTab = isCustomerRole ? 'musteri-portali' : 'dashboard';
              
              let targetPath = returnUrl || (TAB_TO_PATH[targetTab] || (isCustomerRole ? '/yonetim/musteri-portali' : '/yonetim'));
              if (targetPath === '/giris' || targetPath === '/login') {
                targetPath = isCustomerRole ? '/yonetim/musteri-portali' : '/yonetim';
              }"""

if old_login_call in content:
    content = content.replace(old_login_call, new_login_call)
    print("1. Updated LoginComponent call in App component with customers prop & customer portal routing.")

# 2. Update LoginComponent definition & submit handler to support user & customer logins and email automations
old_login_comp = """    function LoginComponent({ onLoginSuccess, showToast, users = [] }) {
      const [loginMethod, setLoginMethod] = useState('email'); // 'email' | 'phone'
      const [emailInput, setEmailInput] = useState('mustafa@iremdugunsarayi.com');
      const [phoneInput, setPhoneInput] = useState('0532 123 4567');
      const [password, setPassword] = useState('Msytf2026');
      const [showPassword, setShowPassword] = useState(false);
      const [rememberMe, setRememberMe] = useState(true);
      const [isLoading, setIsLoading] = useState(false);
      const [showForgotModal, setShowForgotModal] = useState(false);
      const [showHelpModal, setShowHelpModal] = useState(false);
      const [forgotInput, setForgotInput] = useState('');"""

new_login_comp = """    function LoginComponent({ onLoginSuccess, showToast, users = [], customers = [] }) {
      const [loginMethod, setLoginMethod] = useState('email'); // 'email' | 'phone'
      const [emailInput, setEmailInput] = useState('mustafa@iremdugunsarayi.com');
      const [phoneInput, setPhoneInput] = useState('0532 123 4567');
      const [password, setPassword] = useState('Msytf2026');
      const [showPassword, setShowPassword] = useState(false);
      const [rememberMe, setRememberMe] = useState(true);
      const [isLoading, setIsLoading] = useState(false);
      const [showForgotModal, setShowForgotModal] = useState(false);
      const [forgotSuccessMail, setForgotSuccessMail] = useState(null);
      const [forgotInput, setForgotInput] = useState('');"""

if old_login_comp in content:
    content = content.replace(old_login_comp, new_login_comp)
    print("2. Updated LoginComponent definition with customers prop.")

# 3. Update handleFormSubmit in LoginComponent to perform smart user & customer matching
old_form_submit = """          const emailLower = (emailInput || '').toLowerCase().trim();
          const userList = (users && users.length > 0) ? users : (typeof INITIAL_USERS !== 'undefined' ? INITIAL_USERS : []);
          const matchedUser = userList.find(u => (u.email || '').toLowerCase() === emailLower);
          
          let derivedRole = 'admin';
          if (matchedUser && matchedUser.role) {
            derivedRole = matchedUser.role;
          } else if (emailLower.includes('satis')) {
            derivedRole = 'satisci';
          } else if (emailLower.includes('sosyal')) {
            derivedRole = 'sosyal_medyaci';
          } else if (emailLower.includes('ahmet') || emailLower.includes('musteri') || emailLower.includes('example.com')) {
            derivedRole = 'musteri';
          }

          const user = {
            id: matchedUser?.id || `u-${derivedRole}`,
            name: matchedUser?.name || (emailInput.split('@')[0] || 'Kullanıcı'),
            email: emailInput || 'user@iremdugunsarayi.com',
            phone: phoneInput || '0532 123 4567',
            role: derivedRole,
            avatar: matchedUser?.avatar || 'https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=200&q=80'
          };
          onLoginSuccess(user);"""

new_form_submit = """          const valLower = (activeValue || '').toLowerCase().trim();
          const cleanPhoneVal = (phoneInput || '').replace(/\\D/g, '');

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
          };

          const roleLabels = { 'admin': 'Sistem Yöneticisi', 'satisci': 'Satış Müdürü', 'sosyal_medyaci': 'Sosyal Medya Sorumlusu', 'musteri': 'Müşteri Portalı' };
          showToast(`Hoş geldiniz, ${user.name}! (${roleLabels[user.role] || 'Giriş Başarılı'})`);
          onLoginSuccess(user);"""

if old_form_submit in content:
    content = content.replace(old_form_submit, new_form_submit)
    print("3. Updated handleFormSubmit with smart user & customer matching logic.")

# 4. Add Quick Demo Role Login Buttons to LoginComponent
old_submit_btn = """                <button
                  type="submit"
                  disabled={isLoading}
                  aria-label="Sisteme Giriş Yap"
                  className="w-full bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-extrabold py-3.5 min-h-[48px] rounded-xl text-sm shadow-md hover:shadow-lg transition transform active:scale-[0.99] flex items-center justify-center space-x-2 mt-3 cursor-pointer"
                >
                  {isLoading ? (
                    <>
                      <ThemeIcon icon="refresh" fallbackEmoji="" className="w-4 h-4 animate-spin shrink-0" />
                      <span>Doğrulanıyor...</span>
                    </>
                  ) : (
                    <>
                      <ThemeIcon icon="sparkles" fallbackEmoji="" className="w-4 h-4 shrink-0" />
                      <span>Giriş Yap</span>
                    </>
                  )}
                </button>"""

new_submit_btn = """                <button
                  type="submit"
                  disabled={isLoading}
                  aria-label="Sisteme Giriş Yap"
                  className="w-full bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-extrabold py-3.5 min-h-[48px] rounded-xl text-sm shadow-md hover:shadow-lg transition transform active:scale-[0.99] flex items-center justify-center space-x-2 mt-3 cursor-pointer"
                >
                  {isLoading ? (
                    <>
                      <ThemeIcon icon="refresh" fallbackEmoji="" className="w-4 h-4 animate-spin shrink-0" />
                      <span>Doğrulanıyor...</span>
                    </>
                  ) : (
                    <>
                      <ThemeIcon icon="sparkles" fallbackEmoji="" className="w-4 h-4 shrink-0" />
                      <span>Giriş Yap</span>
                    </>
                  )}
                </button>

                {/* QUICK ROLE DEMO LOGIN PRESET BUTTONS */}
                <div className="pt-4 border-t border-slate-200 dark:border-brand-border/60 space-y-2">
                  <div className="text-[11px] font-bold text-slate-500 dark:text-gray-400 flex items-center space-x-1">
                    <ThemeIcon icon="sparkles" className="w-3.5 h-3.5 text-amber-500 inline shrink-0" />
                    <span>Hızlı Canlı Rol Seçimi & Demo Girişleri:</span>
                  </div>
                  <div className="grid grid-cols-2 gap-2 text-[11px] font-bold">
                    <button
                      type="button"
                      onClick={() => { setEmailInput('mustafa@iremdugunsarayi.com'); setPassword('Msytf2026'); handleDemoLogin('admin', 'Mustafa Beyazyüz', 'mustafa@iremdugunsarayi.com', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'); }}
                      className="p-2 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 text-amber-900 dark:text-gold-300 border border-amber-500/30 transition text-left flex items-center space-x-1.5"
                    >
                      <span className="text-amber-500">👑</span>
                      <div className="truncate">
                        <span className="block font-extrabold truncate">Yönetici (Admin)</span>
                        <span className="text-[9px] opacity-75 block truncate">mustafa@...</span>
                      </div>
                    </button>

                    <button
                      type="button"
                      onClick={() => { setEmailInput('satis@iremdugunsarayi.com'); setPassword('Satis2026'); handleDemoLogin('satisci', 'Canan Güneş', 'satis@iremdugunsarayi.com', 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80'); }}
                      className="p-2 rounded-xl bg-blue-500/10 hover:bg-blue-500/20 text-blue-900 dark:text-blue-300 border border-blue-500/30 transition text-left flex items-center space-x-1.5"
                    >
                      <span className="text-blue-500">💼</span>
                      <div className="truncate">
                        <span className="block font-extrabold truncate">Satış Müdürü</span>
                        <span className="text-[9px] opacity-75 block truncate">satis@...</span>
                      </div>
                    </button>

                    <button
                      type="button"
                      onClick={() => { setEmailInput('sosyal@iremdugunsarayi.com'); setPassword('Sosyal2026'); handleDemoLogin('sosyal_medyaci', 'Murat Arslan', 'sosyal@iremdugunsarayi.com', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80'); }}
                      className="p-2 rounded-xl bg-purple-500/10 hover:bg-purple-500/20 text-purple-900 dark:text-purple-300 border border-purple-500/30 transition text-left flex items-center space-x-1.5"
                    >
                      <span className="text-purple-500">📸</span>
                      <div className="truncate">
                        <span className="block font-extrabold truncate">Sosyal Medya</span>
                        <span className="text-[9px] opacity-75 block truncate">sosyal@...</span>
                      </div>
                    </button>

                    <button
                      type="button"
                      onClick={() => { setEmailInput('canan.ozturk@example.com'); setPassword('Musteri2026'); handleDemoLogin('musteri', 'Canan & Serkan Öztürk', 'canan.ozturk@example.com', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'); }}
                      className="p-2 rounded-xl bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-900 dark:text-emerald-300 border border-emerald-500/30 transition text-left flex items-center space-x-1.5"
                    >
                      <span className="text-emerald-500">👤</span>
                      <div className="truncate">
                        <span className="block font-extrabold truncate">Müşteri Portalı</span>
                        <span className="text-[9px] opacity-75 block truncate">canan.ozturk@...</span>
                      </div>
                    </button>
                  </div>
                </div>"""

if old_submit_btn in content:
    content = content.replace(old_submit_btn, new_submit_btn)
    print("4. Added quick role demo login preset buttons to LoginComponent.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
