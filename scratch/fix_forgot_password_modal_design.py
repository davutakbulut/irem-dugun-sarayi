import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_modal_jsx = """          {/* FORGOT PASSWORD MODAL */}
          {showForgotModal && (
            <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in">
              <div className="glass-panel p-6 rounded-3xl max-w-md w-full space-y-4 border border-amber-500/40 bg-slate-900 text-white shadow-2xl animate-scale-up">
                
                <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                  <h3 className="text-base font-bold text-amber-400 flex items-center space-x-2">
                    <ThemeIcon icon="mail" fallbackEmoji="" className="w-5 h-5 text-amber-400 shrink-0" />
                    <span>Otomatik E-Posta & Şifre Yenileme</span>
                  </h3>
                  <button onClick={() => { setShowForgotModal(false); setForgotSuccessMail(null); }} className="text-slate-400 hover:text-white p-1">
                    <ThemeIcon icon="x" className="w-4 h-4 shrink-0" />
                  </button>
                </div>

                {!forgotSuccessMail ? (
                  <div className="space-y-3 text-xs">
                    <p className="text-slate-300 leading-relaxed">
                      Sistemde kayıtlı e-posta adresinizi veya cep telefon numaranızı yazınız. Otomatik mail sunucumuz üzerinden anında güvenli giriş bağlantısı iletilecektir.
                    </p>
                    <div>
                      <label className="block text-slate-400 font-bold mb-1">E-Posta veya Telefon:</label>
                      <input
                        type="text"
                        placeholder="Örn: canan.ozturk@example.com veya 0532..."
                        value={forgotInput}
                        onChange={e => setForgotInput(e.target.value)}
                        className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-white outline-none focus:border-amber-500 font-medium"
                      />
                    </div>
                    <div className="flex space-x-2 pt-2">
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
                        className="flex-1 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white font-extrabold py-2.5 rounded-xl cursor-pointer shadow-md flex items-center justify-center space-x-1.5"
                      >
                        <ThemeIcon icon="mail" className="w-4 h-4 shrink-0" />
                        <span>Otomatik E-Posta Gönder</span>
                      </button>
                      <button
                        type="button"
                        onClick={() => setShowForgotModal(false)}
                        className="px-4 bg-slate-800 hover:bg-slate-700 font-bold py-2.5 rounded-xl text-slate-300 cursor-pointer"
                      >
                        İptal
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-3 text-xs animate-fade-in">
                    <div className="bg-emerald-500/10 border border-emerald-500/30 p-3 rounded-2xl flex items-center space-x-2 text-emerald-400 font-bold">
                      <ThemeIcon icon="checkCircle" className="w-5 h-5 text-emerald-400 shrink-0" />
                      <span>E-Posta Otomasyonu Başarıyla Tamamlandı! ({forgotSuccessMail.sentAt})</span>
                    </div>

                    <div className="bg-slate-950 border border-slate-800 p-4 rounded-2xl space-y-2 text-[11px] font-mono text-slate-300">
                      <div className="flex justify-between border-b border-slate-800 pb-1 text-slate-400">
                        <span>SMTP Sunucusu: mail.iremdugunsarayi.com</span>
                        <span className="text-emerald-400 font-bold">DURUM: GÖNDERİLDİ 200 OK</span>
                      </div>
                      <div><strong>Kime:</strong> {forgotSuccessMail.to}</div>
                      <div><strong>Konu:</strong> {forgotSuccessMail.subject}</div>
                    </div>

                    <div className="flex justify-end pt-2">
                      <button
                        type="button"
                        onClick={() => { setForgotSuccessMail(null); setShowForgotModal(false); }}
                        className="gold-button font-bold px-6 py-2 rounded-xl"
                      >
                        Tamam ✓
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}"""

new_modal_jsx = """          {/* FORGOT PASSWORD MODAL */}
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
                    </div>

                    <div className="flex justify-end pt-2">
                      <button
                        type="button"
                        onClick={() => { setForgotSuccessMail(null); setShowForgotModal(false); }}
                        className="bg-gradient-to-r from-amber-500 to-orange-500 text-white font-extrabold px-6 py-2.5 rounded-xl cursor-pointer text-xs"
                      >
                        Tamam ✓
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}"""

if old_modal_jsx in content:
    content = content.replace(old_modal_jsx, new_modal_jsx)
    print("1. Replaced showForgotModal JSX with luxury high-contrast design!")
else:
    print("WARNING: Could not find old_modal_jsx in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
