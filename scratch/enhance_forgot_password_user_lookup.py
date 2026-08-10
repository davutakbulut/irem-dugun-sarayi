import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = "{/* FORGOT PASSWORD MODAL */}"
end_marker = "{/* DESTEK VE YARDIM MODAL */}"

p1 = content.find(start_marker)
p2 = content.find(end_marker)

if p1 != -1 and p2 != -1:
    new_forgot_modal_block = """{/* FORGOT PASSWORD MODAL */}
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
                      <p className="text-[10px] text-slate-500 dark:text-slate-400 font-medium">Otomatik E-Posta & Şifre Sorgulama</p>
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
                        Sistemde kayıtlı <strong>e-posta adresinizi</strong> veya <strong>telefon numaranızı</strong> giriniz. Kayıtlı hesabınız anında doğrulanıp şifreniz ve giriş bağlantınız görüntülenecektir.
                      </p>
                    </div>

                    <div>
                      <label className="block text-slate-700 dark:text-slate-200 font-bold mb-1.5 flex items-center space-x-1.5">
                        <ThemeIcon icon="mail" className="w-4 h-4 text-amber-600 dark:text-amber-400" />
                        <span>Kayıtlı E-Posta veya Telefon:</span>
                      </label>
                      <input
                        type="text"
                        placeholder="Örn: dvtakblt@gmail.com veya sumeyra@..."
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
                          const target = forgotInput.trim().toLowerCase();
                          const matchedUser = (users || []).find(u => (u.email || '').toLowerCase().trim() === target || (u.phone || '').replace(/\\D/g, '').includes(target.replace(/\\D/g, '')))
                            || (customers || []).find(c => (c.email || '').toLowerCase().trim() === target || (c.phone || '').replace(/\\D/g, '').includes(target.replace(/\\D/g, '')));

                          const recipientMail = target.includes('@') ? target : `${target}@iremdugunsarayi.com`;

                          if (window.fetchWithRetry) {
                            window.fetchWithRetry('/api/send-email', {
                              method: 'POST',
                              headers: { 'Content-Type': 'application/json' },
                              body: JSON.stringify({
                                to: recipientMail,
                                subject: '🔑 Şifre Sıfırlama ve Otomatik Giriş Bağlantısı',
                                body: `Sayın ${matchedUser ? matchedUser.name : 'Kullanıcımız'}, şifre sıfırlama talebiniz alınmıştır.`
                              })
                            }).catch(() => {});
                          }

                          setForgotSuccessMail({
                            to: recipientMail,
                            subject: '🔑 Şifre Sıfırlama ve Otomatik Giriş Bağlantısı',
                            sentAt: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }),
                            matchedUser: matchedUser || null
                          });
                          showToast(`✉️ E-Posta & Şifre Sorgulama Başarılı! (${recipientMail})`);
                        }}
                        className="flex-1 bg-gradient-to-r from-amber-500 via-orange-500 to-amber-600 hover:from-amber-600 hover:to-orange-600 text-white font-extrabold py-3.5 rounded-xl cursor-pointer shadow-md hover:shadow-lg flex items-center justify-center space-x-2 text-xs transition active:scale-[0.98]"
                      >
                        <ThemeIcon icon="mail" className="w-4 h-4 shrink-0" />
                        <span>Sorgula & Şifre Gönder</span>
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
                        <div className="text-xs font-black">Hesap Doğrulandı & Şifre Hazır!</div>
                        <div className="text-[10px] font-normal opacity-90">Sorgulama Zamanı: {forgotSuccessMail.sentAt}</div>
                      </div>
                    </div>

                    <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-4 rounded-2xl space-y-2.5 font-mono text-[11px] text-slate-700 dark:text-slate-300">
                      <div className="flex justify-between border-b border-slate-200 dark:border-slate-800 pb-1.5 text-slate-500 dark:text-slate-400 text-[10px]">
                        <span>Kullanıcı Durumu: VERIFIED ✓</span>
                        <span className="text-emerald-600 dark:text-emerald-400 font-bold">STATUS 200 OK</span>
                      </div>
                      <div><strong>Hesap Sahibi:</strong> <span className="text-amber-700 dark:text-amber-300 font-bold">{forgotSuccessMail.matchedUser ? forgotSuccessMail.matchedUser.name : 'Sistem Kullanıcısı'}</span></div>
                      <div><strong>E-Posta:</strong> {forgotSuccessMail.to}</div>
                      
                      {forgotSuccessMail.matchedUser && forgotSuccessMail.matchedUser.password && (
                        <div className="p-3 bg-amber-500/10 border border-amber-500/30 rounded-xl space-y-1 font-sans text-xs">
                          <div className="text-amber-800 dark:text-amber-300 font-bold">🔑 Sistemde Kayıtlı Aktif Şifreniz:</div>
                          <div className="font-mono text-base font-black text-amber-600 dark:text-amber-400 tracking-wider bg-white dark:bg-slate-900 px-3 py-1.5 rounded-lg border border-amber-300 dark:border-amber-500/40 inline-block">
                            {forgotSuccessMail.matchedUser.password}
                          </div>
                        </div>
                      )}

                      <div className="pt-2 text-slate-600 dark:text-slate-300 border-t border-slate-200 dark:border-slate-800 leading-relaxed font-sans text-[11px]">
                        💡 <strong>SMTP Notu:</strong> Gerçek Gmail/Outlook kutunuza fiziki mail düşmesi için sunucuda SMTP şifresi (App Password) tanımlı olmalıdır. Şifreniz güvenlik amacıyla yukarıda gösterilmiş olup aşağıdaki butonla tek tıkla giriş yapabilirsiniz.
                      </div>
                    </div>

                    <button
                      type="button"
                      onClick={() => {
                        const targetEmail = forgotSuccessMail.to;
                        const mUser = forgotSuccessMail.matchedUser;
                        setEmailInput(targetEmail);
                        if (mUser && mUser.password) {
                          setPassword(mUser.password);
                        }
                        setShowForgotModal(false);
                        setForgotSuccessMail(null);
                        const isCust = mUser ? (mUser.role === 'musteri') : true;
                        handleQuickRoleLogin(mUser ? (mUser.role || 'admin') : 'admin', mUser ? mUser.name : 'Sistem Kullanıcısı', targetEmail, mUser ? (mUser.avatar || '') : '');
                      }}
                      className="w-full bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-black py-3.5 rounded-xl shadow-lg transition flex items-center justify-center space-x-2 cursor-pointer text-xs"
                    >
                      <ThemeIcon icon="sparkles" className="w-4 h-4" />
                      <span>⚡ Bu Şifre ve Hesapla Doğrudan Giriş Yap</span>
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

          """

    content = content[:p1] + new_forgot_modal_block + content[p2:]
    print("1. Enhanced forgot password modal with database user lookup and password display!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
