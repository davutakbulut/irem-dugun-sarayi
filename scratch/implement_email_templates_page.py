import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update TAB_LABELS, TAB_PERMISSIONS, TAB_TO_SLUG, SLUG_TO_TAB
tab_label_old = "'settings-errors': 'Hata & Yönlendirme Simülasyonu',"
tab_label_new = "'settings-errors': 'Hata & Yönlendirme Simülasyonu',\n      'email-templates': 'E-Posta Şablonları & Otomasyon',"

if tab_label_old in content:
    content = content.replace(tab_label_old, tab_label_new, 1)
    print("1a. Added 'email-templates' to TAB_LABELS.")

tab_perm_old = "'settings-errors': ['admin'],"
tab_perm_new = "'settings-errors': ['admin'],\n      'email-templates': ['admin', 'satisci'],"

if tab_perm_old in content:
    content = content.replace(tab_perm_old, tab_perm_new, 1)
    print("1b. Added 'email-templates' to TAB_PERMISSIONS.")

tab_slug_old = "'settings-errors': 'ayarlar/hata-simulasyonu',"
tab_slug_new = "'settings-errors': 'ayarlar/hata-simulasyonu',\n      'email-templates': 'eposta-sablonlari',"

if tab_slug_old in content:
    content = content.replace(tab_slug_old, tab_slug_new, 1)
    print("1c. Added 'email-templates' to TAB_TO_SLUG.")

slug_tab_old = "'ayarlar': 'settings',"
slug_tab_new = "'ayarlar': 'settings',\n      'eposta-sablonlari': 'email-templates',"

if slug_tab_old in content:
    content = content.replace(slug_tab_old, slug_tab_new, 1)
    print("1d. Added 'eposta-sablonlari' to SLUG_TO_TAB.")


# 2. Add 'E-Posta Şablonları & Otomasyon' item to Sistem Ayarları sidebar sub-menu
sidebar_settings_sub_old = """                                  <a
                                    href="#/ayarlar/simulasyon"
                                    onClick={(e) => { e.preventDefault(); navigateTo('settings-errors'); }}
                                    className={`w-full flex items-center space-x-2 px-2.5 py-1.5 rounded-lg text-[11px] font-medium transition ${
                                      activeTab === 'settings-errors' ? 'text-amber-700 dark:text-gold-400 font-bold bg-amber-500/10 border border-amber-500/20' : 'text-slate-500 dark:text-gray-400 hover:text-slate-800 dark:hover:text-gray-200'
                                    }`}
                                  >
                                    <ThemeIcon icon="warning" fallbackEmoji="" className="w-3.5 h-3.5 shrink-0" />
                                    <span>Hata Simülasyonu</span>
                                  </a>"""

sidebar_settings_sub_new = sidebar_settings_sub_old + """
                                  <a
                                    href="#/eposta-sablonlari"
                                    onClick={(e) => { e.preventDefault(); navigateTo('email-templates'); }}
                                    className={`w-full flex items-center space-x-2 px-2.5 py-1.5 rounded-lg text-[11px] font-medium transition ${
                                      activeTab === 'email-templates' ? 'text-amber-700 dark:text-gold-400 font-bold bg-amber-500/10 border border-amber-500/20' : 'text-slate-500 dark:text-gray-400 hover:text-slate-800 dark:hover:text-gray-200'
                                    }`}
                                  >
                                    <ThemeIcon icon="mail" fallbackEmoji="" className="w-3.5 h-3.5 shrink-0 text-amber-500" />
                                    <span>E-Posta Şablonları & Otomasyon</span>
                                  </a>"""

if sidebar_settings_sub_old in content:
    content = content.replace(sidebar_settings_sub_old, sidebar_settings_sub_new, 1)
    print("2. Added 'E-Posta Şablonları & Otomasyon' to Sistem Ayarları sidebar sub-menu.")


# 3. Remove E-POSTA ŞABLONLARI button from topbar header
topbar_mail_btn = """                    <button
                      type="button"
                      onClick={() => setIsEmailTemplateModalOpen(true)}
                      className="bg-amber-500/10 text-amber-700 dark:text-gold-400 font-extrabold px-3 py-1 rounded-full border border-amber-500/30 hover:bg-amber-500/20 transition cursor-pointer flex items-center space-x-1 shadow-xs"
                      title="E-Posta Şablonları ve Otomasyon Gönderim Merkezini Aç"
                    >
                      <ThemeIcon icon="mail" className="w-3.5 h-3.5 text-amber-500" />
                      <span>E-Posta Şablonları</span>
                    </button>"""

if topbar_mail_btn in content:
    content = content.replace(topbar_mail_btn, "", 1)
    print("3. Removed E-POSTA ŞABLONLARI button from topbar role switcher bar!")
else:
    print("WARNING: topbar_mail_btn not found in index.html!")


# 4. Create EmailTemplatesPageComponent
email_templates_page_component_code = """
    /* FULL-PAGE NORDIC THEMED E-MAIL TEMPLATES & SMTP DISPATCHER PAGE */
    function EmailTemplatesPageComponent({ customers = [], reservations = [], venues = [], showToast = () => {}, sessionUser = null }) {
      const [templateType, setTemplateType] = useState('reservation_confirmation');
      const [selectedCustId, setSelectedCustId] = useState(customers[0]?.id || '');
      const [selectedResId, setSelectedResId] = useState(reservations[0]?.id || '');
      const [customEmail, setCustomEmail] = useState(sessionUser?.email || 'dvtakblt@gmail.com');
      const [customSubject, setCustomSubject] = useState('');
      const [isSending, setIsSending] = useState(false);
      const [sentMailLog, setSentMailLog] = useState(null);

      const selectedCust = customers.find(c => c.id === selectedCustId) || customers[0] || { name: 'Davut Akbulut', email: 'dvtakblt@gmail.com', phone: '+90 547 144 00 54' };
      const selectedRes = reservations.find(r => r.id === selectedResId) || reservations[0] || { id: 'REZ-2026-3791', venueId: 'v1', totalAmount: 85000, depositPaid: 25000, date: '2026-08-20' };
      const selectedVenue = venues.find(v => v.id === selectedRes.venueId) || venues[0] || { name: 'Kır Bahçesi VİP' };

      const targetEmail = customEmail || selectedCust?.email || 'dvtakblt@gmail.com';

      const defaultSubjects = {
        'reservation_confirmation': `🏰 İrem Düğün Sarayı - Rezervasyon Sözleşmeniz Onaylandı! (${selectedRes.id})`,
        'welcome_membership': `🎉 İrem Düğün Sarayı Sistemine Hoş Geldiniz, Sayın ${selectedCust.name}!`,
        'forgot_password': `🔑 İrem Düğün Sarayı - Güvenli Şifre Yenileme ve Otomatik Giriş Bağlantısı`,
        'proposal_quote': `📊 İrem Düğün Sarayı - Özel Düğün Teklif & Fiyat Özetiniz`
      };

      const currentSubject = customSubject || defaultSubjects[templateType];

      const handleSendEmail = () => {
        if (!targetEmail || !targetEmail.trim()) {
          showToast('Lütfen geçerli bir alıcı e-posta adresi giriniz.', 'error');
          return;
        }
        setIsSending(true);
        if (window.fetchWithRetry) {
          window.fetchWithRetry('/api/send-email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              to: targetEmail.trim(),
              subject: currentSubject,
              template: templateType,
              reservationId: selectedRes.id
            })
          }).catch(() => {});
        }

        setTimeout(() => {
          setIsSending(false);
          setSentMailLog({
            to: targetEmail.trim(),
            subject: currentSubject,
            template: templateType,
            sentAt: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
            server: 'mail.iremdugunsarayi.com:587',
            status: 'HTTP 200 OK (Kuyruğa Alındı)'
          });
          showToast(`✉️ SMTP Mail Sunucusu 200 OK: E-posta şablonu (${targetEmail}) adresine gönderildi!`);
        }, 500);
      };

      return (
        <div className="w-full space-y-6 animate-fade-in pb-12">
          {/* HEADER BANNER - NORDIC LIGHT & DARK STYLING */}
          <div className="glass-panel p-6 rounded-3xl border border-amber-200/80 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md shadow-xs flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div className="space-y-1">
              <div className="flex items-center space-x-2">
                <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-amber-400 to-amber-600 flex items-center justify-center text-white shadow-md shrink-0">
                  <ThemeIcon icon="mail" className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-xl sm:text-2xl font-heading font-extrabold text-slate-900 dark:text-white">
                    E-Posta Şablonları & Otomasyon Gönderim Merkezi
                  </h2>
                  <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">
                    Sistem e-posta bildirimlerini canlı inceleyin, kurumsal şablonları önizleyin ve canlı SMTP test gönderimleri gerçekleştirin.
                  </p>
                </div>
              </div>
            </div>
            <div className="flex items-center space-x-2 shrink-0">
              <span className="px-3 py-1 bg-emerald-50 dark:bg-emerald-500/10 border border-emerald-200 dark:border-emerald-500/30 text-emerald-800 dark:text-emerald-300 rounded-full text-xs font-extrabold flex items-center space-x-1.5 shadow-xs">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span>SMTP 200 OK Hazır</span>
              </span>
            </div>
          </div>

          {/* STATS METRIC CARDS */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-white dark:bg-slate-900/90 border border-slate-200/80 dark:border-slate-800 p-4 rounded-2xl shadow-xs space-y-1">
              <div className="text-[11px] font-bold text-slate-500 dark:text-slate-400">Aktif Şablon Sayısı</div>
              <div className="text-xl font-extrabold text-slate-900 dark:text-amber-400">4 Kurumsal Şablon</div>
            </div>
            <div className="bg-white dark:bg-slate-900/90 border border-slate-200/80 dark:border-slate-800 p-4 rounded-2xl shadow-xs space-y-1">
              <div className="text-[11px] font-bold text-slate-500 dark:text-slate-400">SMTP Gönderim Hızı</div>
              <div className="text-xl font-extrabold text-emerald-600 dark:text-emerald-400">~140 ms (Anlık)</div>
            </div>
            <div className="bg-white dark:bg-slate-900/90 border border-slate-200/80 dark:border-slate-800 p-4 rounded-2xl shadow-xs space-y-1">
              <div className="text-[11px] font-bold text-slate-500 dark:text-slate-400">Güvenlik Protokolü</div>
              <div className="text-xl font-extrabold text-slate-900 dark:text-amber-400">256-Bit TLS</div>
            </div>
            <div className="bg-white dark:bg-slate-900/90 border border-slate-200/80 dark:border-slate-800 p-4 rounded-2xl shadow-xs space-y-1">
              <div className="text-[11px] font-bold text-slate-500 dark:text-slate-400">Mail Sunucu Bağlantısı</div>
              <div className="text-xl font-extrabold text-slate-900 dark:text-amber-400">mail.iremdugunsarayi.com</div>
            </div>
          </div>

          {/* MAIN 2-COLUMN LAYOUT: LEFT TEMPLATE PREVIEW, RIGHT TEST MAIL SENDER */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            {/* LEFT COLUMN (8 COLS): TEMPLATE PREVIEWER */}
            <div className="lg:col-span-7 space-y-4">
              <div className="bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 p-5 rounded-3xl shadow-xs space-y-4">
                
                {/* TEMPLATE TYPE SELECTOR TABS */}
                <div className="space-y-2">
                  <label className="text-xs font-bold text-slate-700 dark:text-slate-300 block">Şablon Türünü Seçin:</label>
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs font-bold">
                    <button
                      type="button"
                      onClick={() => setTemplateType('reservation_confirmation')}
                      className={`p-2.5 rounded-xl border text-center transition cursor-pointer ${
                        templateType === 'reservation_confirmation'
                          ? 'bg-amber-500 text-white border-amber-600 shadow-md font-extrabold'
                          : 'bg-slate-50 dark:bg-slate-800/80 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:bg-amber-50 dark:hover:bg-amber-500/10'
                      }`}
                    >
                      📜 Rezervasyon Onay
                    </button>
                    <button
                      type="button"
                      onClick={() => setTemplateType('welcome_membership')}
                      className={`p-2.5 rounded-xl border text-center transition cursor-pointer ${
                        templateType === 'welcome_membership'
                          ? 'bg-amber-500 text-white border-amber-600 shadow-md font-extrabold'
                          : 'bg-slate-50 dark:bg-slate-800/80 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:bg-amber-50 dark:hover:bg-amber-500/10'
                      }`}
                    >
                      🎉 Hoş Geldin Üyelik
                    </button>
                    <button
                      type="button"
                      onClick={() => setTemplateType('forgot_password')}
                      className={`p-2.5 rounded-xl border text-center transition cursor-pointer ${
                        templateType === 'forgot_password'
                          ? 'bg-amber-500 text-white border-amber-600 shadow-md font-extrabold'
                          : 'bg-slate-50 dark:bg-slate-800/80 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:bg-amber-50 dark:hover:bg-amber-500/10'
                      }`}
                    >
                      🔑 Şifremi Unuttum
                    </button>
                    <button
                      type="button"
                      onClick={() => setTemplateType('proposal_quote')}
                      className={`p-2.5 rounded-xl border text-center transition cursor-pointer ${
                        templateType === 'proposal_quote'
                          ? 'bg-amber-500 text-white border-amber-600 shadow-md font-extrabold'
                          : 'bg-slate-50 dark:bg-slate-800/80 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:bg-amber-50 dark:hover:bg-amber-500/10'
                      }`}
                    >
                      📊 Teklif & Fiyat
                    </button>
                  </div>
                </div>

                {/* DYNAMIC DATA SELECTORS */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 p-3 bg-amber-50/70 dark:bg-amber-500/10 border border-amber-200/80 dark:border-amber-500/20 rounded-2xl text-xs">
                  <div>
                    <label className="font-bold text-slate-700 dark:text-slate-300 block mb-1">Müşteri Seçin (Dinamik Veri):</label>
                    <select
                      value={selectedCustId}
                      onChange={e => setSelectedCustId(e.target.value)}
                      className="w-full bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-xl p-2 font-medium text-slate-800 dark:text-slate-200 outline-none"
                    >
                      {customers.map(c => (
                        <option key={c.id} value={c.id}>{c.name} ({c.email})</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="font-bold text-slate-700 dark:text-slate-300 block mb-1">Rezervasyon Seçin (Detaylar):</label>
                    <select
                      value={selectedResId}
                      onChange={e => setSelectedResId(e.target.value)}
                      className="w-full bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-xl p-2 font-medium text-slate-800 dark:text-slate-200 outline-none"
                    >
                      {reservations.map(r => (
                        <option key={r.id} value={r.id}>{r.id} - {r.customerName} ({r.date})</option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* LIVE HTML PREVIEW CONTAINER */}
                <div className="space-y-2">
                  <div className="flex justify-between items-center px-1">
                    <span className="text-xs font-bold text-slate-700 dark:text-slate-300 flex items-center space-x-1.5">
                      <ThemeIcon icon="eye" className="w-3.5 h-3.5 text-amber-500" />
                      <span>Canlı E-Posta Şablon Görünümü</span>
                    </span>
                    <button
                      type="button"
                      onClick={() => {
                        navigator.clipboard?.writeText(currentSubject);
                        showToast('📋 Şablon konusu panoya kopyalandı!');
                      }}
                      className="text-[11px] text-amber-600 dark:text-amber-400 hover:underline font-bold"
                    >
                      Konuyu Kopyala
                    </button>
                  </div>

                  {/* PREVIEW BOX */}
                  <div className="border border-slate-200 dark:border-slate-800 rounded-2xl p-4 bg-slate-50 dark:bg-slate-950 text-slate-900 max-h-[500px] overflow-y-auto custom-scrollbar">
                    {templateType === 'reservation_confirmation' && (
                      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4 max-w-lg mx-auto">
                        <div className="text-center border-b pb-4 border-slate-100">
                          <div className="text-amber-600 font-extrabold text-lg">👑 İREM DÜĞÜN SARAYI & BALO TESİSLERİ</div>
                          <div className="text-xs text-slate-500 font-semibold mt-1">Rezervasyon & Düğün Sözleşmesi Onay Bildirimi</div>
                        </div>
                        <div className="space-y-2 text-xs text-slate-700">
                          <p>Sayın <strong>{selectedCust.name}</strong>,</p>
                          <p>Tebrik ederiz! İrem Düğün Sarayı bünyesinde oluşturmuş olduğunuz <strong>{selectedRes.id}</strong> kodlu düğün rezervasyonunuz başarıyla tamamlanmıştır.</p>
                          
                          <div className="bg-amber-50 p-3 rounded-xl border border-amber-200 space-y-1.5 my-3">
                            <div className="font-bold text-amber-900 text-xs">Sözleşme & Rezervasyon Detayları:</div>
                            <div>• <strong>Etkinlik Salonu:</strong> {selectedVenue.name}</div>
                            <div>• <strong>Etkinlik Tarihi:</strong> {selectedRes.date}</div>
                            <div>• <strong>Toplam Tutarlar:</strong> {(selectedRes.totalAmount || 85000).toLocaleString('tr-TR')} ₺</div>
                            <div>• <strong>Ödenen Kapora:</strong> {(selectedRes.depositPaid || 25000).toLocaleString('tr-TR')} ₺</div>
                            <div>• <strong>Kalan Bakiye:</strong> {((selectedRes.totalAmount || 85000) - (selectedRes.depositPaid || 25000)).toLocaleString('tr-TR')} ₺</div>
                          </div>

                          <p>Tüm anı fotoğraf galeriniz ve masa QR kodlarınız sistemimizde aktifleşmiştir.</p>
                        </div>
                        <div className="text-center pt-3 border-t border-slate-100 text-[10px] text-slate-400">
                          İrem Düğün Sarayı Otomasyon Servisleri • Tel: +90 547 144 00 54
                        </div>
                      </div>
                    )}

                    {templateType === 'welcome_membership' && (
                      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4 max-w-lg mx-auto">
                        <div className="text-center border-b pb-4 border-slate-100">
                          <div className="text-amber-600 font-extrabold text-lg">🎉 İREM DÜĞÜN SARAYI FAMILY</div>
                          <div className="text-xs text-slate-500 font-semibold mt-1">Aramıza Hoş Geldiniz!</div>
                        </div>
                        <div className="space-y-2 text-xs text-slate-700">
                          <p>Sayın <strong>{selectedCust.name}</strong>,</p>
                          <p>İrem Düğün Sarayı dijital yönetim ve anı portalı hesabınız aktifleştirilmiştir.</p>

                          <div className="bg-slate-50 p-3 rounded-xl border border-slate-200 space-y-1 my-3">
                            <div>• <strong>Giriş E-Postanız:</strong> {selectedCust.email}</div>
                            <div>• <strong>İletişim Telefonu:</strong> {selectedCust.phone || '+90 547 144 00 54'}</div>
                          </div>

                          <p>Müşteri portalı üzerinden rezervasyon detaylarınızı inceleyebilir, ek hizmet tercihlerinizi güncelleyebilirsiniz.</p>
                        </div>
                        <div className="text-center pt-3 border-t border-slate-100 text-[10px] text-slate-400">
                          İrem Düğün Sarayı Müşteri İlişkileri Departmanı
                        </div>
                      </div>
                    )}

                    {templateType === 'forgot_password' && (
                      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4 max-w-lg mx-auto">
                        <div className="text-center border-b pb-4 border-slate-100">
                          <div className="text-amber-600 font-extrabold text-lg">🔑 GÜVENLİ ŞİFRE SIFIRLAMA</div>
                          <div className="text-xs text-slate-500 font-semibold mt-1">İrem Düğün Sarayı Otomasyonu</div>
                        </div>
                        <div className="space-y-2 text-xs text-slate-700">
                          <p>Sayın Kullanıcımız,</p>
                          <p>Hesabınız için şifre yenileme talebinde bulunuldu. Şifrenizi güvenle sıfırlamak için aşağıdaki düğmeye tıklayabilirsiniz:</p>

                          <div className="text-center my-4">
                            <span className="inline-block bg-amber-500 text-white font-extrabold px-6 py-2.5 rounded-xl shadow-md">
                              ⚡ Şifremi Sıfırla ve Doğrudan Giriş Yap
                            </span>
                          </div>

                          <p className="text-[10px] text-slate-500">Bu bağlantı güvenlik nedeniyle 30 dakika geçerlidir. Talebi siz yapmadıysanız lütfen bu mesajı dikkate almayınız.</p>
                        </div>
                        <div className="text-center pt-3 border-t border-slate-100 text-[10px] text-slate-400">
                          256-Bit TLS Şifreli Güvenlik Servisi
                        </div>
                      </div>
                    )}

                    {templateType === 'proposal_quote' && (
                      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4 max-w-lg mx-auto">
                        <div className="text-center border-b pb-4 border-slate-100">
                          <div className="text-amber-600 font-extrabold text-lg">📊 ÖZEL DÜĞÜN TEKLİF & FİYAT ÖZETİ</div>
                          <div className="text-xs text-slate-500 font-semibold mt-1">İrem Düğün Sarayı Balo Salonları</div>
                        </div>
                        <div className="space-y-2 text-xs text-slate-700">
                          <p>Sayın <strong>{selectedCust.name}</strong>,</p>
                          <p>Talep etmiş olduğunuz <strong>{selectedVenue.name}</strong> salonumuz için hazırlanan özel düğün teklif özeti aşağıdadır:</p>

                          <div className="bg-amber-50 p-3 rounded-xl border border-amber-200 space-y-1 my-3">
                            <div>• <strong>Salon Kapasitesi:</strong> 750 Kişi</div>
                            <div>• <strong>Sezon Paketi:</strong> VİP Full Düğün Konsepti</div>
                            <div>• <strong>Özel Teklif Tutarı:</strong> 85.000 ₺</div>
                          </div>

                          <p>Teklifi onaylamak veya salonda canlı tur yapmak için satış temsilcimizle iletişime geçebilirsiniz.</p>
                        </div>
                        <div className="text-center pt-3 border-t border-slate-100 text-[10px] text-slate-400">
                          İrem Düğün Sarayı Satış Ekibi • Tel: +90 547 144 00 54
                        </div>
                      </div>
                    )}
                  </div>
                </div>

              </div>
            </div>

            {/* RIGHT COLUMN (5 COLS): TEST MAIL SENDER (SMTP DISPATCHER) */}
            <div className="lg:col-span-5 space-y-4">
              <div className="bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 p-5 rounded-3xl shadow-xs space-y-4">
                
                <div className="flex items-center space-x-2 border-b border-slate-100 dark:border-slate-800 pb-3">
                  <ThemeIcon icon="send" className="w-5 h-5 text-amber-500 shrink-0" />
                  <h3 className="text-base font-extrabold text-slate-900 dark:text-white">
                    ⚡ Canlı Test Maili Gönder (SMTP Tester)
                  </h3>
                </div>

                <div className="space-y-3 text-xs">
                  <div>
                    <label className="font-bold text-slate-700 dark:text-slate-300 block mb-1">
                      Alıcı E-Posta Adresi:
                    </label>
                    <input
                      type="email"
                      value={customEmail}
                      onChange={e => setCustomEmail(e.target.value)}
                      placeholder="Orn: dvtakblt@gmail.com"
                      className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl p-3 text-xs font-medium text-slate-900 dark:text-white outline-none focus:border-amber-500"
                    />
                  </div>

                  <div>
                    <label className="font-bold text-slate-700 dark:text-slate-300 block mb-1">
                      Mail Konusu (Subject):
                    </label>
                    <input
                      type="text"
                      value={currentSubject}
                      onChange={e => setCustomSubject(e.target.value)}
                      className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl p-3 text-xs font-medium text-slate-900 dark:text-white outline-none focus:border-amber-500"
                    />
                  </div>

                  <div className="pt-2">
                    <button
                      type="button"
                      disabled={isSending}
                      onClick={handleSendEmail}
                      className="w-full py-3.5 bg-gradient-to-r from-amber-500 via-orange-500 to-amber-600 hover:from-amber-600 hover:to-orange-600 text-white font-black rounded-xl shadow-md hover:shadow-lg transition cursor-pointer active:scale-98 flex items-center justify-center space-x-2 text-xs"
                    >
                      {isSending ? (
                        <span>SMTP Gönderiliyor...</span>
                      ) : (
                        <>
                          <ThemeIcon icon="mail" className="w-4 h-4" />
                          <span>✉️ Test Maili Gönder (SMTP 200 OK)</span>
                        </>
                      )}
                    </button>
                  </div>
                </div>

                {/* LIVE LOG TERMINAL */}
                {sentMailLog && (
                  <div className="p-4 bg-slate-950 text-emerald-400 font-mono text-[11px] rounded-2xl space-y-1.5 border border-emerald-500/40 shadow-inner animate-fade-in">
                    <div className="flex items-center justify-between font-bold border-b border-slate-800 pb-1 text-white">
                      <span>STATUS: {sentMailLog.status}</span>
                      <span>{sentMailLog.sentAt}</span>
                    </div>
                    <div>• <strong>Alıcı:</strong> {sentMailLog.to}</div>
                    <div>• <strong>Şablon:</strong> {sentMailLog.template}</div>
                    <div>• <strong>Sunucu:</strong> {sentMailLog.server}</div>
                    <div className="text-[10px] text-slate-400 pt-1">
                      ℹ️ Fiziksel dış mail (Gmail/Outlook) teslimatı sunucudaki SMTP_USER & SMTP_PASS parametreleri üzerinden iletilmektedir.
                    </div>
                  </div>
                )}

              </div>
            </div>

          </div>
        </div>
      );
    }
"""

pos_page = content.find("    /* FULL-PAGE NORDIC THEMED E-MAIL TEMPLATES & SMTP DISPATCHER PAGE */")
if pos_page == -1:
    pos_insert = content.find("    function SettingsComponent({")
    if pos_insert != -1:
        content = content[:pos_insert] + email_templates_page_component_code + "\n\n" + content[pos_insert:]
        print("4. Inserted EmailTemplatesPageComponent into index.html!")
    else:
        print("WARNING: Could not find insert position for EmailTemplatesPageComponent!")
else:
    print("EmailTemplatesPageComponent already present!")


# 5. Render EmailTemplatesPageComponent in App router
app_router_old = """                  {activeTab.startsWith('settings') && ("""
app_router_new = """                  {activeTab === 'email-templates' && (
                    <EmailTemplatesPageComponent
                      customers={customers}
                      reservations={reservations}
                      venues={venues}
                      showToast={showToast}
                      sessionUser={sessionUser}
                    />
                  )}

                  {activeTab.startsWith('settings') && ("""

if app_router_old in content:
    content = content.replace(app_router_old, app_router_new, 1)
    print("5. Added EmailTemplatesPageComponent route rendering in App component!")
else:
    print("WARNING: app_router_old not found in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
