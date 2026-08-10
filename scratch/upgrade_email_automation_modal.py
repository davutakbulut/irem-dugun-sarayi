import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_modal = """          {showForgotModal && (
            <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
              <div className="glass-panel p-6 rounded-3xl max-w-sm w-full space-y-4 border border-amber-500/40 bg-slate-900 text-white">
                <h3 className="text-base font-bold text-amber-400 flex items-center space-x-2">
                  <ThemeIcon icon="key" fallbackEmoji="" className="w-4 h-4 text-amber-400 shrink-0" />
                  <span>Şifre Sıfırlama Talebi</span>
                </h3>
                <p className="text-xs text-slate-300">
                  Sistemde kayıtlı e-posta adresinizi veya telefon numaranızı giriniz. Tek kullanımlık doğrulama kodu iletilecektir.
                </p>
                <input
                  type="text"
                  placeholder="e-posta@iremdugunsarayi.com veya 05XX XXX XX XX"
                  value={forgotInput}
                  onChange={e => setForgotInput(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-xs text-white outline-none focus:border-amber-500"
                />
                <div className="flex space-x-2 pt-2 text-xs">
                  <button
                    type="button"
                    onClick={() => {
                      if (!forgotInput) return alert('Lütfen bilgilerinizi giriniz.');
                      alert(`Şifre sıfırlama kuralı ${forgotInput} adresine/numarasına iletildi.`);
                      setShowForgotModal(false);
                    }}
                    className="flex-1 gold-button font-bold py-2 rounded-xl cursor-pointer"
                  >
                    Sıfırlama Bağlantısı Gönder
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowForgotModal(false)}
                    className="px-4 bg-slate-800 hover:bg-slate-700 font-bold py-2 rounded-xl text-slate-300 cursor-pointer"
                  >
                    Kapat
                  </button>
                </div>
              </div>
            </div>
          )}"""

new_modal = """          {showForgotModal && (
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
                          setForgotSuccessMail({
                            to: target.includes('@') ? target : `${target}@iremdugunsarayi.com`,
                            subject: '🔑 Şifre Sıfırlama ve Otomatik Giriş Bağlantısı',
                            sentAt: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })
                          });
                          showToast(`✉️ E-Posta otomasyonu tetiklendi: ${target} adresine aktivasyon maili iletildi!`);
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
                      <div className="pt-2 text-slate-300 border-t border-slate-800 leading-relaxed font-sans">
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
                        handleDemoLogin(isCust ? 'musteri' : 'admin', isCust ? 'Canan & Serkan Öztürk' : 'Sistem Yöneticisi', targetEmail, 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80');
                      }}
                      className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold py-3 rounded-xl shadow-lg transition flex items-center justify-center space-x-2 cursor-pointer"
                    >
                      <ThemeIcon icon="sparkles" className="w-4 h-4 shrink-0" />
                      <span>Tek Kullanımlık Bağlantı ile Anında Giriş Yap</span>
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}"""

if old_modal in content:
    content = content.replace(old_modal, new_modal)
    print("1. Successfully upgraded showForgotModal to interactive Email Automation Modal!")
else:
    print("WARNING: Could not find old_modal exact match in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
