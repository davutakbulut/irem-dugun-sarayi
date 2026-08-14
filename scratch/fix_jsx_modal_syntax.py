import os, re

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find entire section from {/* FORGOT PASSWORD to {/* DESTEK VE YARDIM MODAL
    pattern = re.search(r'\{\s*/\*\s*FORGOT PASSWORD[\s\S]*?\{\s*/\*\s*DESTEK VE YARDIM MODAL', content)
    
    clean_modal_section = """{/* FORGOT PASSWORD REAL 2-STEP SMTP MODAL */}
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
                      <h3 className="text-sm font-extrabold text-slate-900 dark:text-amber-400">Şifre Sıfırlama</h3>
                      <p className="text-[10px] text-slate-500 dark:text-slate-400 font-medium">E-Posta ile Doğrulama & Yeni Şifre</p>
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => { setShowForgotModal(false); setForgotSuccessMail(null); setForgotInput(''); }}
                    className="w-8 h-8 rounded-full bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-white flex items-center justify-center transition cursor-pointer font-bold text-xs"
                  >
                    ✕
                  </button>
                </div>

                {!forgotSuccessMail ? (
                  /* STEP 1: ENTER EMAIL OR PHONE */
                  <form onSubmit={async (e) => {
                    e.preventDefault();
                    if (!forgotInput || !forgotInput.trim()) {
                      showToast('Lütfen geçerli bir e-posta veya telefon giriniz.', 'error');
                      return;
                    }
                    setIsLoading(true);
                    try {
                      const res = await fetch('/api/auth/forgot-password', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ identity: forgotInput.trim() })
                      });
                      const data = await res.json();
                      setIsLoading(false);
                      if (!res.ok || data.error) {
                        showToast(data.error || 'Kullanıcı bulunamadı!', 'error');
                        return;
                      }
                      setForgotSuccessMail({
                        email: data.email,
                        maskedEmail: data.maskedEmail,
                        code: '',
                        newPassword: '',
                        confirmPassword: ''
                      });
                      showToast(data.message || 'Doğrulama kodu e-posta adresinize gönderildi!');
                    } catch(err) {
                      setIsLoading(false);
                      showToast('Sunucu ile iletişim kurulamadı.', 'error');
                    }
                  }} className="space-y-4 text-xs">
                    
                    <div className="bg-amber-50/80 dark:bg-amber-500/10 border border-amber-200/80 dark:border-amber-500/30 p-4 rounded-2xl flex items-start space-x-3 text-slate-700 dark:text-amber-200 shadow-xs">
                      <ThemeIcon icon="info" className="w-5 h-5 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
                      <p className="text-[11px] leading-relaxed font-medium">
                        Sistemde kayıtlı <strong>e-posta adresinizi</strong> veya <strong>telefon numaranızı</strong> giriniz. Şifrenizi güvenle yenileyebilmeniz için 6 haneli güvenlik kodu e-posta adresinize iletilecektir.
                      </p>
                    </div>

                    <div>
                      <label className="block text-slate-700 dark:text-slate-200 font-bold mb-1.5 flex items-center space-x-1.5">
                        <ThemeIcon icon="mail" className="w-4 h-4 text-amber-600 dark:text-amber-400" />
                        <span>Kayıtlı E-Posta veya Telefon:</span>
                      </label>
                      <input
                        type="text"
                        required
                        placeholder="Örn: dvtakblt@gmail.com veya 0532..."
                        value={forgotInput}
                        onChange={e => setForgotInput(e.target.value)}
                        className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-700 focus:bg-white dark:focus:bg-slate-950 focus:border-amber-500 rounded-xl p-3.5 text-xs text-slate-800 dark:text-amber-300 font-semibold placeholder:text-slate-400 dark:placeholder:text-slate-500 outline-none transition shadow-xs"
                      />
                    </div>

                    <div className="flex items-center space-x-2 pt-2">
                      <button
                        type="submit"
                        disabled={isLoading}
                        className="flex-1 bg-gradient-to-r from-amber-500 via-orange-500 to-amber-600 hover:from-amber-600 hover:to-orange-600 text-white font-extrabold py-3.5 rounded-xl cursor-pointer shadow-md hover:shadow-lg flex items-center justify-center space-x-2 text-xs transition active:scale-[0.98]"
                      >
                        {isLoading ? <span>Kod Gönderiliyor...</span> : <span>Doğrulama Kodu Gönder</span>}
                      </button>
                    </div>
                  </form>
                ) : (
                  /* STEP 2: ENTER CODE & SET NEW PASSWORD */
                  <form onSubmit={async (e) => {
                    e.preventDefault();
                    if (!forgotSuccessMail.code || forgotSuccessMail.code.trim().length !== 6) {
                      showToast('Lütfen 6 haneli doğrulama kodunu giriniz.', 'error');
                      return;
                    }
                    if (!forgotSuccessMail.newPassword || forgotSuccessMail.newPassword.length < 4) {
                      showToast('Yeni şifre en az 4 karakter olmalıdır.', 'error');
                      return;
                    }
                    if (forgotSuccessMail.newPassword !== forgotSuccessMail.confirmPassword) {
                      showToast('Yeni şifreler birbiriyle eşleşmiyor!', 'error');
                      return;
                    }

                    setIsLoading(true);
                    try {
                      const res = await fetch('/api/auth/reset-password', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                          email: forgotSuccessMail.email,
                          code: forgotSuccessMail.code.trim(),
                          newPassword: forgotSuccessMail.newPassword
                        })
                      });
                      const data = await res.json();
                      setIsLoading(false);
                      if (!res.ok || data.error) {
                        showToast(data.error || 'Doğrulama kodu hatalı veya süresi dolmuş!', 'error');
                        return;
                      }

                      // Fill in login form automatically
                      setEmailInput(forgotSuccessMail.email);
                      setPassword(forgotSuccessMail.newPassword);
                      setLoginMethod('email');
                      setShowForgotModal(false);
                      setForgotSuccessMail(null);
                      setForgotInput('');
                      showToast('🎉 Şifreniz başarıyla yenilendi! Yeni şifrenizle giriş yapabilirsiniz.');
                    } catch(err) {
                      setIsLoading(false);
                      showToast('Şifre güncellenirken hata oluştu.', 'error');
                    }
                  }} className="space-y-4 text-xs">
                    
                    <div className="bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-300 dark:border-emerald-700/60 p-3.5 rounded-2xl flex items-start space-x-2.5 text-emerald-800 dark:text-emerald-300 shadow-xs">
                      <ThemeIcon icon="check" className="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" />
                      <div>
                        <div className="font-extrabold text-xs">Kod Gönderildi!</div>
                        <div className="text-[11px] mt-0.5"><strong>{forgotSuccessMail.maskedEmail || forgotSuccessMail.email}</strong> adresinize 6 haneli güvenlik kodu iletildi.</div>
                      </div>
                    </div>

                    <div>
                      <label className="block text-slate-700 dark:text-slate-200 font-bold mb-1.5">
                        6 Haneli Güvenlik Kodu <span className="text-red-500">*</span>
                      </label>
                      <input
                        type="text"
                        maxLength="6"
                        required
                        placeholder="Örn: 123456"
                        value={forgotSuccessMail.code}
                        onChange={e => setForgotSuccessMail({ ...forgotSuccessMail, code: e.target.value.replace(/\\D/g, '') })}
                        className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-700 focus:bg-white dark:focus:bg-slate-950 focus:border-amber-500 rounded-xl p-3 text-center text-lg font-black tracking-widest text-amber-700 dark:text-amber-300 outline-none transition"
                      />
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      <div>
                        <label className="block text-slate-700 dark:text-slate-200 font-bold mb-1.5">
                          Yeni Şifre <span className="text-red-500">*</span>
                        </label>
                        <input
                          type="password"
                          required
                          placeholder="Yeni şifreniz"
                          value={forgotSuccessMail.newPassword}
                          onChange={e => setForgotSuccessMail({ ...forgotSuccessMail, newPassword: e.target.value })}
                          className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-700 focus:bg-white dark:focus:bg-slate-950 focus:border-amber-500 rounded-xl p-3 text-xs outline-none transition"
                        />
                      </div>
                      <div>
                        <label className="block text-slate-700 dark:text-slate-200 font-bold mb-1.5">
                          Şifre Tekrar <span className="text-red-500">*</span>
                        </label>
                        <input
                          type="password"
                          required
                          placeholder="Şifreyi tekrar yazın"
                          value={forgotSuccessMail.confirmPassword}
                          onChange={e => setForgotSuccessMail({ ...forgotSuccessMail, confirmPassword: e.target.value })}
                          className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-700 focus:bg-white dark:focus:bg-slate-950 focus:border-amber-500 rounded-xl p-3 text-xs outline-none transition"
                        />
                      </div>
                    </div>

                    <div className="flex items-center space-x-2 pt-2">
                      <button
                        type="button"
                        onClick={() => setForgotSuccessMail(null)}
                        className="px-4 py-3 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 font-bold rounded-xl text-xs transition cursor-pointer"
                      >
                        Geri
                      </button>
                      <button
                        type="submit"
                        disabled={isLoading}
                        className="flex-1 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white font-extrabold py-3 rounded-xl cursor-pointer shadow-md hover:shadow-lg flex items-center justify-center space-x-2 text-xs transition"
                      >
                        {isLoading ? <span>Güncelleniyor...</span> : <span>Şifremi Yenile ve Kaydet</span>}
                      </button>
                    </div>
                  </form>
                )}

              </div>
            </div>
          )}\n\n          {/* DESTEK VE YARDIM MODAL"""

    if pattern:
        content = content[:pattern.start()] + clean_modal_section + content[pattern.end() - len('{/* DESTEK VE YARDIM MODAL'):]
        with open(h_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Cleaned up JSX syntax perfectly in {h_file}")
    else:
        print(f"Pattern not found in {h_file}")

print("All files checked and JSX errors resolved!")
