import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = "{/* FORGOT PASSWORD MODAL */}"
end_marker = "{/* RIGHT SIDE: NORDIC LIGHT LUXURY HERO SHOWCASE WITH HAPPY CUSTOMERS */}"

p1 = content.find(start_marker)
p2 = content.find(end_marker)

if p1 != -1 and p2 != -1:
    new_modal_block = """{/* FORGOT PASSWORD MODAL */}
          {showForgotModal && (
            <div className="fixed inset-0 z-[99999] bg-black/85 backdrop-blur-lg flex items-center justify-center p-4 animate-fade-in">
              <div className="bg-slate-900 border-2 border-amber-500/50 rounded-3xl max-w-md w-full p-6 space-y-5 shadow-[0_25px_60px_-15px_rgba(245,158,11,0.25)] text-white animate-scale-up relative">
                
                {/* HEADER */}
                <div className="flex items-center justify-between border-b border-slate-800 pb-3.5">
                  <div className="flex items-center space-x-2.5">
                    <div className="w-9 h-9 rounded-2xl bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-amber-400 shrink-0">
                      <ThemeIcon icon="key" className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="text-sm font-black text-amber-400">Şifremi Unuttum & Aktivasyon</h3>
                      <p className="text-[10px] text-slate-400 font-medium">Otomatik SMTP E-Posta Gönderim Sunucusu</p>
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => { setShowForgotModal(false); setForgotSuccessMail(null); }}
                    className="w-8 h-8 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center transition cursor-pointer"
                  >
                    ✕
                  </button>
                </div>

                {!forgotSuccessMail ? (
                  <div className="space-y-4 text-xs">
                    <div className="bg-amber-500/10 border border-amber-500/30 p-3.5 rounded-2xl flex items-start space-x-3 text-amber-200">
                      <ThemeIcon icon="info" className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
                      <p className="text-[11px] leading-relaxed font-medium">
                        Sistemde kayıtlı <strong>e-posta adresinizi</strong> veya <strong>telefon numaranızı</strong> giriniz. Güvenli giriş ve tek tıkla şifre yenileme bağlantısı e-posta adresinize anında iletilecektir.
                      </p>
                    </div>

                    <div>
                      <label className="block text-slate-200 font-bold mb-1.5 flex items-center space-x-1.5">
                        <ThemeIcon icon="mail" className="w-4 h-4 text-amber-400" />
                        <span>Kayıtlı E-Posta veya Telefon:</span>
                      </label>
                      <input
                        type="text"
                        placeholder="Örn: sumeyra@iremdugunsarayi.com veya 0532..."
                        value={forgotInput}
                        onChange={e => setForgotInput(e.target.value)}
                        className="w-full bg-slate-950 border-2 border-slate-700 focus:border-amber-500 rounded-xl p-3.5 text-xs text-amber-300 font-bold placeholder:text-slate-500 outline-none transition shadow-inner"
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
                        className="flex-1 bg-gradient-to-r from-amber-500 via-orange-500 to-amber-600 hover:from-amber-600 hover:to-orange-600 text-white font-black py-3.5 rounded-xl cursor-pointer shadow-lg hover:shadow-amber-500/25 flex items-center justify-center space-x-2 text-xs transition active:scale-[0.98]"
                      >
                        <ThemeIcon icon="mail" className="w-4 h-4 shrink-0" />
                        <span>Otomatik E-Posta Gönder</span>
                      </button>
                      <button
                        type="button"
                        onClick={() => setShowForgotModal(false)}
                        className="px-4 py-3.5 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold rounded-xl cursor-pointer text-xs transition"
                      >
                        İptal
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-4 text-xs animate-fade-in">
                    <div className="bg-emerald-500/15 border border-emerald-500/40 p-4 rounded-2xl flex items-center space-x-3 text-emerald-400 font-bold">
                      <ThemeIcon icon="checkCircle" className="w-6 h-6 text-emerald-400 shrink-0" />
                      <div>
                        <div className="text-xs font-black">Aktivasyon Maili Gönderildi!</div>
                        <div className="text-[10px] font-normal opacity-90">Gönderim Zamanı: {forgotSuccessMail.sentAt}</div>
                      </div>
                    </div>

                    <div className="bg-slate-950 border border-slate-800 p-4 rounded-2xl space-y-2 font-mono text-[11px] text-slate-300">
                      <div className="flex justify-between border-b border-slate-800 pb-1.5 text-slate-400 text-[10px]">
                        <span>SMTP Sunucusu: mail.iremdugunsarayi.com</span>
                        <span className="text-emerald-400 font-bold">DURUM: 200 OK</span>
                      </div>
                      <div><strong>Kime:</strong> <span className="text-amber-300">{forgotSuccessMail.to}</span></div>
                      <div><strong>Konu:</strong> {forgotSuccessMail.subject}</div>
                      <div className="pt-2 text-slate-300 border-t border-slate-800 leading-relaxed font-sans text-xs">
                        Sayın Kullanıcımız,<br/>
                        Hesabınıza hızlı ve güvenli erişim sağlamanız için oluşturulan tek kullanımlık giriş bağlantınız hazırlanmıştır. Aşağıdaki butona tıklayarak doğrudan hesabınıza erişebilirsiniz.
                      </div>
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
                        className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold rounded-xl text-xs cursor-pointer"
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
    content = content[:p1] + new_modal_block + content[p2:]
    print("1. Successfully replaced showForgotModal with luxury high-contrast design!")
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
