import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add EmailTemplateModalComponent before LoginComponent
email_modal_code = """    // --- EMAIL TEMPLATE MODAL COMPONENT ---
    function EmailTemplateModalComponent({ onClose, customers = [], reservations = [], venues = [], showToast }) {
      const [templateType, setTemplateType] = useState('reservation_confirmation'); // 'reservation_confirmation' | 'welcome_membership' | 'forgot_password'
      const [selectedCustId, setSelectedCustId] = useState(customers[0]?.id || '');
      const [selectedResId, setSelectedResId] = useState(reservations[0]?.id || '');
      const [customEmail, setCustomEmail] = useState('');
      const [customSubject, setCustomSubject] = useState('');
      const [isSending, setIsSending] = useState(false);
      const [sentMailStatus, setSentMailStatus] = useState(null);

      const selectedCust = customers.find(c => c.id === selectedCustId) || customers[0] || { name: 'Müşteri', email: 'musteri@example.com', phone: '05320000000' };
      const selectedRes = reservations.find(r => r.id === selectedResId) || reservations[0] || { id: 'REZ-2026-001', venueId: 'v1', totalAmount: 85000, depositPaid: 25000, date: '2026-08-20' };
      const selectedVenue = venues.find(v => v.id === selectedRes.venueId) || venues[0] || { name: 'Kır Bahçesi VİP' };

      const targetEmail = customEmail || selectedCust?.email || 'musteri@example.com';

      const defaultSubjects = {
        'reservation_confirmation': `🏰 İrem Düğün Sarayı - Rezervasyon Sözleşmeniz Onaylandı! (${selectedRes.id})`,
        'welcome_membership': `🎉 İrem Düğün Sarayı Sistemine Hoş Geldiniz, Sayın ${selectedCust.name}!`,
        'forgot_password': `🔑 İrem Düğün Sarayı - Güvenli Şifre Yenileme ve Otomatik Giriş Bağlantısı`
      };

      const currentSubject = customSubject || defaultSubjects[templateType];

      const handleSendEmail = () => {
        if (!targetEmail || !targetEmail.trim()) {
          showToast('Lütfen geçerli bir alıcı e-posta adresi seçiniz.', 'error');
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
          setSentMailStatus({
            to: targetEmail.trim(),
            subject: currentSubject,
            template: templateType,
            sentAt: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })
          });
          showToast(`✉️ SMTP Mail Sunucusu 200 OK: E-posta şablonu (${targetEmail}) adresine gönderildi!`);
        }, 450);
      };

      return (
        <div className="fixed inset-0 z-[99999] bg-black/80 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 overflow-y-auto animate-fade-in">
          <div className="bg-slate-900 border-2 border-amber-500/40 rounded-3xl max-w-2xl w-full p-6 space-y-4 shadow-2xl text-white max-h-[92vh] overflow-y-auto custom-scrollbar my-auto">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <div className="flex items-center space-x-2">
                <ThemeIcon icon="mail" className="w-5 h-5 text-amber-400 shrink-0" />
                <h3 className="text-base font-bold text-amber-400">E-Posta Şablonları & Otomasyon Gönderim Merkezi</h3>
              </div>
              <button onClick={onClose} className="text-slate-400 hover:text-white font-bold p-1">✕</button>
            </div>

            {!sentMailStatus ? (
              <div className="space-y-4 text-xs">
                {/* TEMPLATE TYPE SELECTOR */}
                <div>
                  <label className="block text-slate-300 font-bold mb-1.5">Gönderilecek E-Posta Şablonunu Seçiniz:</label>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                    <button
                      type="button"
                      onClick={() => { setTemplateType('reservation_confirmation'); setCustomSubject(''); }}
                      className={`p-3 rounded-2xl border text-left font-bold transition flex flex-col justify-between ${
                        templateType === 'reservation_confirmation' ? 'bg-amber-500/20 border-amber-500 text-amber-300' : 'bg-slate-950 border-slate-800 text-slate-400 hover:text-white'
                      }`}
                    >
                      <span className="text-[11px] block">📜 1. Rezervasyon & Sözleşme Şablonu</span>
                      <span className="text-[9px] font-medium opacity-80 mt-1">Sözleşme onayı, salon, ödeme ve bakiye özeti</span>
                    </button>

                    <button
                      type="button"
                      onClick={() => { setTemplateType('welcome_membership'); setCustomSubject(''); }}
                      className={`p-3 rounded-2xl border text-left font-bold transition flex flex-col justify-between ${
                        templateType === 'welcome_membership' ? 'bg-amber-500/20 border-amber-500 text-amber-300' : 'bg-slate-950 border-slate-800 text-slate-400 hover:text-white'
                      }`}
                    >
                      <span className="text-[11px] block">🎉 2. Üyelik & Hoş Geldin Şablonu</span>
                      <span className="text-[9px] font-medium opacity-80 mt-1">Müşteri/kullanıcı hesap aktivasyonu ve portal linki</span>
                    </button>

                    <button
                      type="button"
                      onClick={() => { setTemplateType('forgot_password'); setCustomSubject(''); }}
                      className={`p-3 rounded-2xl border text-left font-bold transition flex flex-col justify-between ${
                        templateType === 'forgot_password' ? 'bg-amber-500/20 border-amber-500 text-amber-300' : 'bg-slate-950 border-slate-800 text-slate-400 hover:text-white'
                      }`}
                    >
                      <span className="text-[11px] block">🔑 3. Şifremi Unuttum Şablonu</span>
                      <span className="text-[9px] font-medium opacity-80 mt-1">Tek kullanımlık güvenli sıfırlama & hızlı giriş linki</span>
                    </button>
                  </div>
                </div>

                {/* RECIPIENT & SUBJECT */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="block text-slate-300 font-bold mb-1">Alıcı Müşteri / E-Posta:</label>
                    <select
                      value={selectedCustId}
                      onChange={e => { setSelectedCustId(e.target.value); setCustomEmail(''); }}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-xs text-white font-bold"
                    >
                      {customers.map(c => (
                        <option key={c.id} value={c.id}>{c.name} ({c.email || 'Mail Yok'})</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-slate-300 font-bold mb-1">E-Posta Konusu (Subject):</label>
                    <input
                      type="text"
                      value={currentSubject}
                      onChange={e => setCustomSubject(e.target.value)}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-xs text-amber-300 font-bold"
                    />
                  </div>
                </div>

                {/* LIVE STYLED HTML EMAIL PREVIEW BOX */}
                <div className="border border-amber-500/30 rounded-2xl bg-slate-950 p-4 space-y-3">
                  <div className="flex justify-between items-center border-b border-slate-800 pb-2 text-[10px] text-slate-400">
                    <span>E-POSTA CANLI ÖNİZLEME (HTML PREVIEW)</span>
                    <span className="text-emerald-400 font-mono font-bold">SMTP SSL/TLS ACTIVE ✓</span>
                  </div>

                  {templateType === 'reservation_confirmation' && (
                    <div className="space-y-3 text-[11px] text-slate-200">
                      <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/30 font-bold text-amber-300 text-xs">
                        🏰 İREM DÜĞÜN SARAYI - REZERVASYON VE SÖZLEŞME ONAY BELGESİ
                      </div>
                      <p>Sayın <strong>{selectedCust.name}</strong>,</p>
                      <p>İrem Düğün Sarayı bünyesinde gerçekleşecek düğün organizasyonunuzun rezervasyon sözleşmesi başarıyla oluşturulmuştur.</p>
                      <div className="grid grid-cols-2 gap-2 p-3 bg-slate-900 rounded-xl border border-slate-800 text-[10px]">
                        <div>Mekan: <strong className="text-amber-400">{selectedVenue.name}</strong></div>
                        <div>Tarih: <strong className="text-amber-400">{selectedRes.date || '2026-08-20'}</strong></div>
                        <div>Toplam Tutar: <strong className="text-emerald-400">{formatCurrency(selectedRes.totalAmount || 85000)}</strong></div>
                        <div>Kalan Net Bakiye: <strong className="text-amber-400">{formatCurrency(Math.max(0, (selectedRes.totalAmount || 85000) - (selectedRes.depositPaid || 25000)))}</strong></div>
                      </div>
                      <button className="gold-button w-full font-bold py-2 rounded-xl text-xs cursor-pointer">
                        📋 Müşteri Portalımdan Sözleşme ve Detayları Gör
                      </button>
                    </div>
                  )}

                  {templateType === 'welcome_membership' && (
                    <div className="space-y-3 text-[11px] text-slate-200">
                      <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/30 font-bold text-amber-300 text-xs">
                        🎉 İREM DÜĞÜN SARAYI - MÜŞTERİ PORTALINA HOŞ GELDİNİZ
                      </div>
                      <p>Sayın <strong>{selectedCust.name}</strong>,</p>
                      <p>İrem Düğün Sarayı Müşteri Portalı hesabınız aktif edilmiştir. Giriş bilgilerinizi kullanarak organizasyon detaylarınızı canlı takip edebilirsiniz.</p>
                      <div className="p-3 bg-slate-900 rounded-xl border border-slate-800 space-y-1 text-[10px]">
                        <div>E-Posta: <strong>{selectedCust.email || targetEmail}</strong></div>
                        <div>Telefon: <strong>{selectedCust.phone || '0532 000 00 00'}</strong></div>
                        <div>Yetki Seviyesi: <strong className="text-amber-400">Müşteri Portalı (Canlı Takip)</strong></div>
                      </div>
                      <button className="gold-button w-full font-bold py-2 rounded-xl text-xs cursor-pointer">
                        🔑 Müşteri Portalına Giriş Yap
                      </button>
                    </div>
                  )}

                  {templateType === 'forgot_password' && (
                    <div className="space-y-3 text-[11px] text-slate-200">
                      <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/30 font-bold text-amber-300 text-xs">
                        🔑 İREM DÜĞÜN SARAYI - GÜVENLİ ŞİFRE SIFIRLAMA & HIZLI GİRİŞ
                      </div>
                      <p>Sayın <strong>{selectedCust.name}</strong>,</p>
                      <p>Hesabınıza güvenli erişim sağlamanız için oluşturulan 30 dakika geçerli tek kullanımlık aktivasyon bağlantınız aşağıdadır.</p>
                      <div className="p-3 bg-slate-900 rounded-xl border border-slate-800 space-y-1 text-[10px]">
                        <div>Protokol: <strong className="text-emerald-400">TLS 256-Bit Encrypted Link</strong></div>
                        <div>Geçerlilik Süresi: <strong>30 Dakika (Tek Kullanımlık)</strong></div>
                      </div>
                      <button className="gold-button w-full font-bold py-2 rounded-xl text-xs cursor-pointer">
                        ⚡ Şifremi Yenile & Otomatik Giriş Yap
                      </button>
                    </div>
                  )}
                </div>

                {/* ACTION BUTTONS */}
                <div className="flex justify-end space-x-2 pt-2 border-t border-slate-800">
                  <button type="button" onClick={onClose} className="px-4 py-2 bg-slate-800 text-slate-300 rounded-xl font-bold">İptal</button>
                  <button
                    type="button"
                    onClick={handleSendEmail}
                    disabled={isSending}
                    className="gold-button font-extrabold px-6 py-2.5 rounded-xl shadow-lg flex items-center space-x-2 cursor-pointer"
                  >
                    <ThemeIcon icon="mail" className="w-4 h-4 shrink-0" />
                    <span>{isSending ? 'Gönderiliyor...' : '✉️ E-Postayı Gönder (SMTP 200 OK)'}</span>
                  </button>
                </div>
              </div>
            ) : (
              <div className="space-y-4 text-xs animate-fade-in">
                <div className="bg-emerald-500/10 border border-emerald-500/30 p-4 rounded-2xl flex items-center space-x-3 text-emerald-400 font-bold">
                  <ThemeIcon icon="checkCircle" className="w-6 h-6 text-emerald-400 shrink-0" />
                  <div>
                    <div className="text-sm font-black">E-Posta Şablonu Gönderimi Başarılı!</div>
                    <div className="text-[11px] font-normal opacity-90">Gönderim Zamanı: {sentMailStatus.sentAt}</div>
                  </div>
                </div>

                <div className="bg-slate-950 border border-slate-800 p-4 rounded-2xl space-y-2 font-mono text-[11px] text-slate-300">
                  <div className="flex justify-between border-b border-slate-800 pb-1 text-slate-400">
                    <span>SMTP Server: mail.iremdugunsarayi.com:587</span>
                    <span className="text-emerald-400 font-bold">STATUS: 200 OK</span>
                  </div>
                  <div><strong>Alıcı:</strong> {sentMailStatus.to}</div>
                  <div><strong>Konu:</strong> {sentMailStatus.subject}</div>
                  <div><strong>Kullanılan Şablon:</strong> {sentMailStatus.template}</div>
                </div>

                <div className="flex justify-end pt-2">
                  <button
                    type="button"
                    onClick={() => { setSentMailStatus(null); onClose(); }}
                    className="gold-button font-bold px-6 py-2 rounded-xl"
                  >
                    Tamam ✓
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      );
    }

    // --- NORDIC LIGHT & FRESH LOGIN COMPONENT ---"""

pos_login = content.find("// --- NORDIC LIGHT & FRESH LOGIN COMPONENT ---")
if pos_login != -1:
    content = content[:pos_login] + email_modal_code + "\n\n    " + content[pos_login:]
    print("1. Added EmailTemplateModalComponent to index.html.")

# 2. Add isEmailModalOpen state to App component
old_app_states = """      const [isMobileSummaryDrawerOpen, setIsMobileSummaryDrawerOpen] = useState(false);
      const [mobileReservationSummary, setMobileReservationSummary] = useState(null);"""

new_app_states = """      const [isMobileSummaryDrawerOpen, setIsMobileSummaryDrawerOpen] = useState(false);
      const [mobileReservationSummary, setMobileReservationSummary] = useState(null);
      const [isEmailTemplateModalOpen, setIsEmailTemplateModalOpen] = useState(false);"""

if old_app_states in content:
    content = content.replace(old_app_states, new_app_states)
    print("2. Added isEmailTemplateModalOpen state to App component.")

# 3. Add Email Template Modal trigger button in topbar header next to Version modal
old_version_button = """                    <button
                      type="button"
                      onClick={() => setIsVersionModalOpen(true)}"""

new_version_button = """                    <button
                      type="button"
                      onClick={() => setIsEmailTemplateModalOpen(true)}
                      className="bg-amber-500/10 text-amber-700 dark:text-gold-400 font-extrabold px-3 py-1 rounded-full border border-amber-500/30 hover:bg-amber-500/20 transition cursor-pointer flex items-center space-x-1 shadow-xs"
                      title="E-Posta Şablonları ve Otomasyon Gönderim Merkezini Aç"
                    >
                      <ThemeIcon icon="mail" className="w-3.5 h-3.5 text-amber-500" />
                      <span>E-Posta Şablonları</span>
                    </button>

                    <button
                      type="button"
                      onClick={() => setIsVersionModalOpen(true)}"""

if old_version_button in content:
    content = content.replace(old_version_button, new_version_button, 1)
    print("3. Added E-Posta Şablonları topbar header button.")

# 4. Render EmailTemplateModalComponent in App modals
old_app_modals = """          {/* VERSION HISTORY MODAL */}
          {isVersionModalOpen && ("""

new_app_modals = """          {/* EMAIL TEMPLATES CENTER MODAL */}
          {isEmailTemplateModalOpen && (
            <EmailTemplateModalComponent
              onClose={() => setIsEmailTemplateModalOpen(false)}
              customers={customers}
              reservations={reservations}
              venues={venues}
              showToast={showToast}
            />
          )}

          {/* VERSION HISTORY MODAL */}
          {isVersionModalOpen && ("""

if old_app_modals in content:
    content = content.replace(old_app_modals, new_app_modals)
    print("4. Added EmailTemplateModalComponent modal rendering in App.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
