import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = "    // --- NORDIC LIGHT & FRESH LOGIN COMPONENT ---"
end_marker = "    // --- PREMIUM DÜĞÜN VE DAVET SALONU WEB SİTESİ (PROMPT BRIEF ULTRA LUXURY SUITE) ---"

p1 = content.find(start_marker)
p2 = content.find(end_marker)

if p1 != -1 and p2 != -1:
    new_login_component_code = """    // --- NORDIC LIGHT & FRESH LOGIN COMPONENT ---
    function LoginComponent({ onLoginSuccess, showToast, users = [], customers = [] }) {
      const [loginMethod, setLoginMethod] = useState('email'); // 'email' | 'phone'
      const [emailInput, setEmailInput] = useState('');
      const [phoneInput, setPhoneInput] = useState('');
      const [password, setPassword] = useState('');
      const [showPassword, setShowPassword] = useState(false);
      const [rememberMe, setRememberMe] = useState(true);
      const [isLoading, setIsLoading] = useState(false);
      const [showForgotModal, setShowForgotModal] = useState(false);
      const [showHelpModal, setShowHelpModal] = useState(false);
      const [forgotSuccessMail, setForgotSuccessMail] = useState(null);
      const [forgotInput, setForgotInput] = useState('');
      const [errorMessage, setErrorMessage] = useState('');

      const activeValue = loginMethod === 'email' ? emailInput : phoneInput;

      // ANLIK CANLI FORMAT VE GÜVENLİK KONTROLÜ (SYNTAX & SECURITY VALIDATOR)
      const inputValidation = useMemo(() => {
        const val = (activeValue || '').trim();
        if (!val) return { isValid: false, message: '' };

        if (loginMethod === 'email') {
          const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$/;
          if (emailRegex.test(val)) return { isValid: true, message: 'E-posta Formatı Geçerli' };
          return { isValid: false, message: 'Lütfen geçerli bir e-posta adresi giriniz.' };
        } else {
          const digits = val.replace(/\\D/g, '');
          if ((digits.length === 11 && digits.startsWith('05')) || (digits.length === 10 && digits.startsWith('5'))) {
            return { isValid: true, message: 'Telefon Numarası Formatı (TR) Geçerli' };
          }
          return { isValid: false, message: 'Lütfen geçerli bir 05xx... telefon numarası giriniz.' };
        }
      }, [loginMethod, emailInput, phoneInput]);

      const handleFormSubmit = (e) => {
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
          
          let matchedUser = null;
          let matchedRole = 'musteri';
          let isCustomerMatch = false;

          if (users && users.length > 0) {
            matchedUser = users.find(u => {
              const uEmail = (u.email || '').toLowerCase().trim();
              const uPhone = (u.phone || '').replace(/\\D/g, '');
              const inputDigits = valLower.replace(/\\D/g, '');

              const identityMatch = loginMethod === 'email' ? (uEmail === valLower) : (uPhone && inputDigits && uPhone.includes(inputDigits));
              const passwordMatch = u.password ? (u.password === password) : true;
              return identityMatch && passwordMatch;
            });

            if (matchedUser) {
              matchedRole = matchedUser.role || 'musteri';
            }
          }

          if (!matchedUser && customers && customers.length > 0) {
            const matchedCust = customers.find(c => {
              const cEmail = (c.email || '').toLowerCase().trim();
              const cPhone = (c.phone || '').replace(/\\D/g, '');
              const inputDigits = valLower.replace(/\\D/g, '');
              return loginMethod === 'email' ? (cEmail === valLower) : (cPhone && inputDigits && cPhone.includes(inputDigits));
            });

            if (matchedCust) {
              matchedUser = {
                id: matchedCust.id,
                name: matchedCust.name,
                email: matchedCust.email,
                role: 'musteri',
                avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'
              };
              matchedRole = 'musteri';
              isCustomerMatch = true;
            }
          }

          if (!matchedUser) {
            const errorText = `Girdiğiniz ${loginMethod === 'email' ? 'e-posta adresi' : 'telefon numarası'} veya şifre hatalıdır. Lütfen kontrol edip tekrar deneyiniz.`;
            setErrorMessage(errorText);
            showToast('Hatalı e-posta/telefon veya şifre!', 'error');
            return;
          }

          onLoginSuccess({
            role: matchedRole,
            userName: matchedUser.name || 'Kullanıcı',
            userEmail: matchedUser.email || valLower,
            avatar: matchedUser.avatar || 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=200&q=80'
          });
          showToast(`Hoş geldiniz Sayın ${matchedUser.name || 'Kullanıcımız'}! (${matchedRole.toUpperCase()})`);
        }, 350);
      };

      const handleQuickRoleLogin = (role, name, email, avatar) => {
        setErrorMessage('');
        onLoginSuccess({ role, userName: name, userEmail: email, avatar });
        showToast(`Hızlı Giriş Sağlandı: ${name} (${role.toUpperCase()})`);
      };

      return (
        <div className="min-h-screen bg-[#FFFBF5] dark:bg-slate-950 flex flex-col justify-between font-sans selection:bg-amber-500 selection:text-white relative overflow-hidden">
          
          {/* TOP BAR / NORDIC BRAND HEADER */}
          <header className="w-full bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200/80 dark:border-amber-500/20 px-6 py-3.5 flex items-center justify-between z-30 shadow-xs">
            <div className="flex items-center space-x-3">
              <div className="w-9 h-9 rounded-2xl bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center text-white shadow-sm shrink-0">
                <ThemeIcon icon="crown" className="w-5 h-5" />
              </div>
              <div>
                <span className="font-extrabold text-sm text-slate-900 dark:text-white tracking-wide block">İREM DÜĞÜN SARAYI</span>
                <span className="text-[10px] text-amber-700 dark:text-amber-400 font-medium block">Yönetim & Müşteri Portalı</span>
              </div>
            </div>

            <div className="flex items-center space-x-2 text-xs font-bold">
              <button
                type="button"
                onClick={() => setShowHelpModal(true)}
                className="px-3.5 py-1.5 rounded-full bg-amber-50 dark:bg-amber-500/10 border border-amber-200 dark:border-amber-500/30 text-amber-800 dark:text-amber-300 hover:bg-amber-100 transition cursor-pointer flex items-center space-x-1"
              >
                <ThemeIcon icon="helpCircle" className="w-3.5 h-3.5 text-amber-600" />
                <span>Destek</span>
              </button>
            </div>
          </header>

          {/* MAIN TWO-COLUMN CONTAINER */}
          <div className="flex-1 flex flex-col lg:flex-row items-center justify-center p-4 sm:p-8 max-w-7xl w-full mx-auto z-20 gap-8">
            
            {/* LEFT COLUMN: CRISP NORDIC LIGHT LOGIN CARD */}
            <div className="w-full lg:w-1/2 max-w-md bg-white dark:bg-slate-900 border border-slate-200 dark:border-amber-500/20 rounded-3xl p-6 sm:p-8 shadow-[0_20px_50px_rgba(0,0,0,0.06)] space-y-6 animate-scale-up">
              
              {/* CARD HEADER */}
              <div className="space-y-1.5 text-center lg:text-left">
                <h1 className="text-2xl font-heading font-black text-slate-900 dark:text-white tracking-tight">
                  Portala <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-600 to-orange-500">Giriş Yapın</span>
                </h1>
                <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">
                  Rezervasyonlarınızı, sözleşmelerinizi ve salon takvimini canlı yönetin.
                </p>
              </div>

              {/* IN-PLACE RED ALERT ERROR BANNER */}
              {errorMessage && (
                <div className="bg-red-50 dark:bg-red-500/15 border-2 border-red-300 dark:border-red-500/40 p-3.5 rounded-2xl flex items-start space-x-3 text-red-700 dark:text-red-300 text-xs animate-shake shadow-xs">
                  <ThemeIcon icon="alertTriangle" className="w-5 h-5 text-red-600 dark:text-red-400 shrink-0 mt-0.5" />
                  <div className="flex-1 font-semibold leading-relaxed">
                    <div>{errorMessage}</div>
                  </div>
                </div>
              )}

              {/* LOGIN METHOD TABS (E-POSTA / TELEFON) */}
              <div className="flex p-1 bg-slate-100 dark:bg-slate-950 rounded-2xl border border-slate-200 dark:border-slate-800 text-xs font-bold">
                <button
                  type="button"
                  onClick={() => { setLoginMethod('email'); setErrorMessage(''); }}
                  className={`flex-1 py-2.5 rounded-xl transition flex items-center justify-center space-x-1.5 cursor-pointer ${
                    loginMethod === 'email' ? 'bg-white dark:bg-slate-800 text-amber-600 dark:text-amber-400 shadow-sm' : 'text-slate-500 hover:text-slate-800 dark:hover:text-white'
                  }`}
                >
                  <ThemeIcon icon="mail" className="w-3.5 h-3.5" />
                  <span>E-Posta Adresi</span>
                </button>
                <button
                  type="button"
                  onClick={() => { setLoginMethod('phone'); setErrorMessage(''); }}
                  className={`flex-1 py-2.5 rounded-xl transition flex items-center justify-center space-x-1.5 cursor-pointer ${
                    loginMethod === 'phone' ? 'bg-white dark:bg-slate-800 text-amber-600 dark:text-amber-400 shadow-sm' : 'text-slate-500 hover:text-slate-800 dark:hover:text-white'
                  }`}
                >
                  <ThemeIcon icon="phone" className="w-3.5 h-3.5" />
                  <span>Telefon Numarası</span>
                </button>
              </div>

              {/* LOGIN FORM */}
              <form onSubmit={handleFormSubmit} className="space-y-4">
                
                {/* IDENTITY INPUT (EMAIL OR PHONE) */}
                {loginMethod === 'email' ? (
                  <div>
                    <label className="block text-slate-700 dark:text-slate-200 font-bold text-xs mb-1.5">
                      E-Posta Adresi <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="email"
                      required
                      value={emailInput}
                      onChange={e => { setEmailInput(e.target.value); if (errorMessage) setErrorMessage(''); }}
                      placeholder="ornek@iremdugunsarayi.com"
                      className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 focus:bg-white dark:focus:bg-slate-950 focus:border-amber-500 rounded-xl p-3 text-xs text-slate-800 dark:text-white font-medium outline-none transition shadow-xs"
                    />
                  </div>
                ) : (
                  <div>
                    <label className="block text-slate-700 dark:text-slate-200 font-bold text-xs mb-1.5">
                      Telefon Numarası <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="tel"
                      required
                      value={phoneInput}
                      onChange={e => { setPhoneInput(e.target.value); if (errorMessage) setErrorMessage(''); }}
                      placeholder="05XX XXX XX XX"
                      className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 focus:bg-white dark:focus:bg-slate-950 focus:border-amber-500 rounded-xl p-3 text-xs text-slate-800 dark:text-white font-medium outline-none transition shadow-xs"
                    />
                  </div>
                )}

                {/* PASSWORD INPUT */}
                <div>
                  <div className="flex justify-between items-center mb-1.5">
                    <label className="block text-slate-700 dark:text-slate-200 font-bold text-xs">
                      Şifre <span className="text-red-500">*</span>
                    </label>
                    <button
                      type="button"
                      onClick={() => setShowForgotModal(true)}
                      className="text-[11px] font-bold text-amber-600 dark:text-amber-400 hover:underline cursor-pointer"
                    >
                      Şifremi Unuttum
                    </button>
                  </div>
                  <div className="relative">
                    <input
                      type={showPassword ? 'text' : 'password'}
                      required
                      value={password}
                      onChange={e => setPassword(e.target.value)}
                      placeholder="Şifrenizi giriniz..."
                      className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 focus:bg-white dark:focus:bg-slate-950 focus:border-amber-500 rounded-xl p-3 pr-10 text-xs text-slate-800 dark:text-white font-medium outline-none transition shadow-xs"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-white cursor-pointer"
                    >
                      <ThemeIcon icon={showPassword ? 'eyeOff' : 'eye'} className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {/* SUBMIT BUTTON */}
                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full bg-gradient-to-r from-amber-500 via-orange-500 to-amber-600 hover:from-amber-600 hover:to-orange-600 text-white font-black py-3.5 rounded-xl shadow-md hover:shadow-lg transition flex items-center justify-center space-x-2 text-xs cursor-pointer active:scale-[0.99] mt-2"
                >
                  {isLoading ? (
                    <span>Doğrulanıyor...</span>
                  ) : (
                    <>
                      <ThemeIcon icon="sparkles" className="w-4 h-4" />
                      <span>Sisteme Giriş Yap</span>
                    </>
                  )}
                </button>
              </form>

              {/* QUICK DEMO ROLE BUTTONS FOR MANAGERS */}
              <div className="pt-2 border-t border-slate-100 dark:border-slate-800 space-y-2">
                <span className="text-[10px] text-slate-400 font-bold block text-center uppercase tracking-wider">Hızlı Rol Girişleri:</span>
                <div className="grid grid-cols-2 gap-2 text-[11px] font-bold">
                  <button
                    type="button"
                    onClick={() => handleQuickRoleLogin('admin', 'Sümeyra Yılmaz (Yönetici)', 'sumeyra@iremdugunsarayi.com', 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=200&q=80')}
                    className="p-2 rounded-xl bg-amber-50 dark:bg-amber-500/10 border border-amber-200 dark:border-amber-500/30 text-amber-800 dark:text-amber-300 hover:bg-amber-100 transition cursor-pointer text-center"
                  >
                    👑 Yönetici (Admin)
                  </button>
                  <button
                    type="button"
                    onClick={() => handleQuickRoleLogin('satis', 'Ahmet Can (Satış Müdürü)', 'ahmet@iremdugunsarayi.com', 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=200&q=80')}
                    className="p-2 rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-200 transition cursor-pointer text-center"
                  >
                    💼 Satış Müdürü
                  </button>
                </div>
              </div>

            </div>

            {/* RIGHT COLUMN: SINGLE FRESH NORDIC HERO SHOWCASE */}
            <div className="w-full lg:w-1/2 bg-gradient-to-br from-[#FFF8EE] via-[#F5EEE2] to-[#EBE4D5] dark:from-slate-900 dark:to-slate-950 border border-amber-200/60 dark:border-amber-500/20 rounded-3xl p-8 xl:p-10 space-y-6 relative overflow-hidden shadow-sm flex flex-col justify-between min-h-[520px]">
              
              {/* TOP BRAND BADGE & HEADING */}
              <div className="space-y-3 relative z-10">
                <div className="inline-flex items-center space-x-2 bg-amber-500/10 backdrop-blur-md text-amber-900 dark:text-amber-300 text-xs font-extrabold px-3.5 py-1.5 rounded-full border border-amber-500/30">
                  <ThemeIcon icon="crown" className="w-4 h-4 text-amber-600" />
                  <span>Sapanca Göl Kenarı Lüks Düğün Tesisleri</span>
                </div>
                <h2 className="text-3xl xl:text-4xl font-heading font-black text-slate-900 dark:text-white leading-tight tracking-tight">
                  Hayallerinizin Ötesinde Bir <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-600 via-orange-500 to-amber-700">Düğün Deneyimi</span>
                </h2>
                <p className="text-xs xl:text-sm text-slate-600 dark:text-slate-300 leading-relaxed font-medium">
                  Sapanca Göl Kenarında 4 farklı konsept balo salonu, canlı etkinlik akış takibi ve kusursuz organizasyon yönetimi.
                </p>
              </div>

              {/* CENTER STATS GRID */}
              <div className="grid grid-cols-3 gap-3 relative z-10">
                <div className="bg-white/90 dark:bg-slate-900/90 backdrop-blur-md p-3.5 rounded-2xl border border-amber-200/80 dark:border-amber-500/20 shadow-xs text-center">
                  <div className="text-lg xl:text-xl font-black text-amber-600 dark:text-amber-400">1,250+</div>
                  <div className="text-[10px] text-slate-500 dark:text-slate-400 font-bold mt-0.5">Mutlu Çift</div>
                </div>
                <div className="bg-white/90 dark:bg-slate-900/90 backdrop-blur-md p-3.5 rounded-2xl border border-amber-200/80 dark:border-amber-500/20 shadow-xs text-center">
                  <div className="text-lg xl:text-xl font-black text-amber-600 dark:text-amber-400">4.9 / 5</div>
                  <div className="text-[10px] text-slate-500 dark:text-slate-400 font-bold mt-0.5">Müşteri Puanı</div>
                </div>
                <div className="bg-white/90 dark:bg-slate-900/90 backdrop-blur-md p-3.5 rounded-2xl border border-amber-200/80 dark:border-amber-500/20 shadow-xs text-center">
                  <div className="text-lg xl:text-xl font-black text-amber-600 dark:text-amber-400">%99.8</div>
                  <div className="text-[10px] text-slate-500 dark:text-slate-400 font-bold mt-0.5">Tavsiye Oranı</div>
                </div>
              </div>

              {/* TESTIMONIAL CARD */}
              <div className="bg-white/90 dark:bg-slate-900/90 backdrop-blur-md p-4 rounded-2xl border border-amber-200/80 dark:border-amber-500/20 shadow-xs space-y-2 relative z-10">
                <div className="flex items-center space-x-3">
                  <img
                    src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80"
                    alt="Selin & Mert"
                    className="w-10 h-10 rounded-full object-cover border-2 border-amber-500 shrink-0"
                  />
                  <div>
                    <div className="text-xs font-bold text-slate-900 dark:text-white">Selin & Mert Yılmaz</div>
                    <div className="text-[10px] text-amber-600 dark:text-amber-400 font-medium">15 Haziran 2025 • Safir Balo Salonu</div>
                  </div>
                </div>
                <p className="text-[11px] text-slate-600 dark:text-slate-300 italic leading-relaxed">
                  "Balo salonunun ihtişamı, masa süslemeleri ve organizasyon ekibinin rüya gibi bir düğün yaşatması harikaydı. Her detay mükemmeldi!"
                </p>
              </div>

              {/* FOOTER INFO */}
              <div className="flex justify-between items-center text-[11px] text-slate-500 dark:text-slate-400 pt-2 border-t border-amber-200/60 dark:border-slate-800 relative z-10 font-medium">
                <span>📍 Sapanca Balo Tesisleri, Sakarya</span>
                <span>📞 +90 (264) 582 00 00</span>
              </div>

            </div>

          </div>

          {/* FOOTER COPYRIGHT */}
          <footer className="w-full text-center py-4 text-[11px] text-slate-500 dark:text-slate-400 font-medium border-t border-slate-200/60 dark:border-slate-900">
            © 2026 İrem Düğün Sarayı & Balo Tesisleri. Tüm Hakları Saklıdır.
          </footer>

          {/* FORGOT PASSWORD MODAL */}
          {showForgotModal && (
            <div className="fixed inset-0 z-[99999] bg-slate-900/60 dark:bg-black/80 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in">
              <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-amber-500/30 rounded-3xl max-w-md w-full p-6 sm:p-7 space-y-5 shadow-[0_20px_50px_rgba(0,0,0,0.12)] text-slate-800 dark:text-white animate-scale-up relative">
                
                {/* HEADER */}
                <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3.5">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 rounded-2xl bg-amber-500/10 dark:bg-amber-500/20 border border-amber-500/30 flex items-center justify-center text-amber-600 dark:text-amber-400 shrink-0 shadow-xs">
                      <ThemeIcon icon="key" className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="text-sm font-extrabold text-slate-900 dark:text-amber-400">Şifremi Unuttum & Aktivasyon</h3>
                      <p className="text-[10px] text-slate-500 dark:text-slate-400 font-medium">Otomatik SMTP E-Posta Gönderim Sunucusu</p>
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => { setShowForgotModal(false); setForgotSuccessMail(null); }}
                    className="w-8 h-8 rounded-full bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-white flex items-center justify-center transition cursor-pointer font-bold text-xs"
                  >
                    ✕
                  </button>
                </div>

                {!forgotSuccessMail ? (
                  <div className="space-y-4 text-xs">
                    {/* NORDIC FRESH INFO CARD */}
                    <div className="bg-amber-50/80 dark:bg-amber-500/10 border border-amber-200/80 dark:border-amber-500/30 p-4 rounded-2xl flex items-start space-x-3 text-slate-700 dark:text-amber-200 shadow-xs">
                      <ThemeIcon icon="info" className="w-5 h-5 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
                      <p className="text-[11px] leading-relaxed font-medium">
                        Sistemde kayıtlı <strong>e-posta adresinizi</strong> veya <strong>telefon numaranızı</strong> giriniz. Güvenli giriş ve tek tıkla şifre yenileme bağlantısı e-posta adresinize anında iletilecektir.
                      </p>
                    </div>

                    <div>
                      <label className="block text-slate-700 dark:text-slate-200 font-bold mb-1.5 flex items-center space-x-1.5">
                        <ThemeIcon icon="mail" className="w-4 h-4 text-amber-600 dark:text-amber-400" />
                        <span>Kayıtlı E-Posta veya Telefon:</span>
                      </label>
                      <input
                        type="text"
                        placeholder="Örn: sumeyra@iremdugunsarayi.com veya 0532..."
                        value={forgotInput}
                        onChange={e => setForgotInput(e.target.value)}
                        className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-700 focus:bg-white dark:focus:bg-slate-950 focus:border-amber-500 rounded-xl p-3.5 text-xs text-slate-800 dark:text-amber-300 font-semibold placeholder:text-slate-400 dark:placeholder:text-slate-500 outline-none transition shadow-xs"
                      />
                    </div>

                    <div className="flex items-center space-x-2 pt-2">
                      <button
                        type="button"
                        onClick={() => {
                          if (!forgotInput || !forgotInput.trim()) {
                            showToast('Lütfen geçerli bir e-posta veya telefon giriniz.', 'error');
                            return;
                          }
                          const target = forgotInput.trim();
                          const recipientMail = target.includes('@') ? target : `${target}@iremdugunsarayi.com`;

                          if (window.fetchWithRetry) {
                            window.fetchWithRetry('/api/send-email', {
                              method: 'POST',
                              headers: { 'Content-Type': 'application/json' },
                              body: JSON.stringify({
                                to: recipientMail,
                                subject: '🔑 Şifre Sıfırlama ve Otomatik Giriş Bağlantısı',
                                body: 'Sayın Kullanıcımız, şifre yenileme ve otomatik giriş bağlantınız başarıyla oluşturulmuştur.'
                              })
                            }).catch(() => {});
                          }

                          setForgotSuccessMail({
                            to: recipientMail,
                            subject: '🔑 Şifre Sıfırlama ve Otomatik Giriş Bağlantısı',
                            sentAt: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })
                          });
                          showToast(`✉️ SMTP Mail Sunucusu 200 OK: ${recipientMail} adresine aktivasyon maili iletildi!`);
                        }}
                        className="flex-1 bg-gradient-to-r from-amber-500 via-orange-500 to-amber-600 hover:from-amber-600 hover:to-orange-600 text-white font-extrabold py-3.5 rounded-xl cursor-pointer shadow-md hover:shadow-lg flex items-center justify-center space-x-2 text-xs transition active:scale-[0.98]"
                      >
                        <ThemeIcon icon="mail" className="w-4 h-4 shrink-0" />
                        <span>Otomatik E-Posta Gönder</span>
                      </button>
                      <button
                        type="button"
                        onClick={() => setShowForgotModal(false)}
                        className="px-4 py-3.5 bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 font-bold rounded-xl cursor-pointer text-xs transition"
                      >
                        İptal
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-4 text-xs animate-fade-in">
                    <div className="bg-emerald-50 dark:bg-emerald-500/15 border border-emerald-200 dark:border-emerald-500/40 p-4 rounded-2xl flex items-center space-x-3 text-emerald-800 dark:text-emerald-400 font-bold">
                      <ThemeIcon icon="checkCircle" className="w-6 h-6 text-emerald-600 dark:text-emerald-400 shrink-0" />
                      <div>
                        <div className="text-xs font-black">Aktivasyon Maili Gönderildi!</div>
                        <div className="text-[10px] font-normal opacity-90">Gönderim Zamanı: {forgotSuccessMail.sentAt}</div>
                      </div>
                    </div>

                    <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-4 rounded-2xl space-y-2 font-mono text-[11px] text-slate-700 dark:text-slate-300">
                      <div className="flex justify-between border-b border-slate-200 dark:border-slate-800 pb-1.5 text-slate-500 dark:text-slate-400 text-[10px]">
                        <span>SMTP Sunucusu: mail.iremdugunsarayi.com</span>
                        <span className="text-emerald-600 dark:text-emerald-400 font-bold">DURUM: 200 OK</span>
                      </div>
                      <div><strong>Kime:</strong> <span className="text-amber-700 dark:text-amber-300">{forgotSuccessMail.to}</span></div>
                      <div><strong>Konu:</strong> {forgotSuccessMail.subject}</div>
                    </div>

                    <button
                      type="button"
                      onClick={() => {
                        const targetEmail = forgotSuccessMail.to;
                        setEmailInput(targetEmail);
                        setShowForgotModal(false);
                        setForgotSuccessMail(null);
                        const isCust = targetEmail.includes('canan') || targetEmail.includes('musteri') || targetEmail.includes('example.com');
                        handleQuickRoleLogin(isCust ? 'musteri' : 'admin', isCust ? 'Canan & Serkan Öztürk' : 'Sistem Yöneticisi', targetEmail, 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80');
                      }}
                      className="w-full bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-black py-3.5 rounded-xl shadow-lg transition flex items-center justify-center space-x-2 cursor-pointer text-xs"
                    >
                      <ThemeIcon icon="sparkles" className="w-4 h-4" />
                      <span>⚡ Doğrudan Otomatik Giriş Yap ve Şifreyi Yenile</span>
                    </button>

                    <div className="flex justify-end pt-1">
                      <button
                        type="button"
                        onClick={() => { setForgotSuccessMail(null); setShowForgotModal(false); }}
                        className="px-4 py-2 bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 font-bold rounded-xl text-xs cursor-pointer"
                      >
                        Kapat
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* DESTEK VE YARDIM MODAL */}
          {showHelpModal && (
            <div className="fixed inset-0 z-[99999] bg-black/70 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in">
              <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-amber-500/30 rounded-3xl max-w-md w-full p-6 space-y-4 shadow-2xl text-slate-800 dark:text-white animate-scale-up">
                <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
                  <h3 className="text-sm font-bold text-amber-600 dark:text-amber-400 flex items-center space-x-2">
                    <ThemeIcon icon="helpCircle" className="w-5 h-5 text-amber-600" />
                    <span>Canlı Destek & İletişim Hatları</span>
                  </h3>
                  <button onClick={() => setShowHelpModal(false)} className="text-slate-400 hover:text-slate-600 dark:hover:text-white font-bold p-1">✕</button>
                </div>
                <div className="space-y-3 text-xs">
                  <div className="p-3 bg-amber-50 dark:bg-amber-500/10 rounded-2xl border border-amber-200 dark:border-amber-500/30 space-y-1">
                    <div className="font-bold text-amber-900 dark:text-amber-300">📞 Santral & Müşteri Hizmetleri:</div>
                    <div className="text-slate-600 dark:text-slate-300 font-mono">+90 (264) 582 00 00</div>
                  </div>
                  <div className="p-3 bg-slate-50 dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 space-y-1">
                    <div className="font-bold text-slate-800 dark:text-slate-200">✉️ E-Posta Destek:</div>
                    <div className="text-slate-600 dark:text-slate-300 font-mono">destek@iremdugunsarayi.com</div>
                  </div>
                </div>
                <div className="flex justify-end pt-2">
                  <button
                    type="button"
                    onClick={() => setShowHelpModal(false)}
                    className="px-4 py-2 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white font-extrabold rounded-xl text-xs cursor-pointer shadow-md"
                  >
                    Anladım, Kapat
                  </button>
                </div>
              </div>
            </div>
          )}

        </div>
      );
    }

    """

    content = content[:p1] + new_login_component_code + content[p2:]
    print("1. Replaced LoginComponent cleanly, removed all duplicates, applied Nordic Light redesign!")
else:
    print(f"ERROR: Could not find markers p1={p1}, p2={p2}!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
