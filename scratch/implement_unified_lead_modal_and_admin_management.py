import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Define INITIAL_QUOTE_REQUESTS
initial_quotes_code = """
    // INITIAL DEMO DATA FOR QUOTE REQUESTS (LEADS)
    const INITIAL_QUOTE_REQUESTS = [
      {
        id: 'QUOTE-2026-001',
        customerName: 'Burak & Selin Demir',
        customerPhone: '+90 532 456 78 90',
        customerEmail: 'burak.demir@gmail.com',
        eventType: 'Düğün',
        preferredVenue: 'Saray Balo Salonu',
        guestCount: 500,
        eventDate: '2026-08-25',
        notes: 'Kır bahçesinde kokteyl karşılama alanı istiyoruz.',
        status: 'beklemede',
        createdAt: '2026-08-10T14:30:00.000Z'
      },
      {
        id: 'QUOTE-2026-002',
        customerName: 'Kaan & Elif Kaya',
        customerPhone: '+90 543 987 65 43',
        customerEmail: 'elif.kaya@hotmail.com',
        eventType: 'Nişan & Söz',
        preferredVenue: 'Safir Salon',
        guestCount: 250,
        eventDate: '2026-09-12',
        notes: 'Canlı müzik ve VIP menü seçenekleri.',
        status: 'teklif_gonderildi',
        createdAt: '2026-08-09T11:15:00.000Z'
      },
      {
        id: 'QUOTE-2026-003',
        customerName: 'Mert Holding Kurumsal',
        customerPhone: '+90 535 111 22 33',
        customerEmail: 'etkinlik@mertholding.com',
        eventType: 'Kurumsal Davet',
        preferredVenue: 'Kır Bahçesi',
        guestCount: 800,
        eventDate: '2026-10-05',
        notes: 'Yıl sonu lansman yemeği ve podyum kurulumu.',
        status: 'arandi',
        createdAt: '2026-08-08T09:45:00.000Z'
      }
    ];
"""

# Insert INITIAL_QUOTE_REQUESTS before INITIAL_USERS
if "const INITIAL_USERS =" in content:
    content = content.replace("const INITIAL_USERS =", initial_quotes_code + "\n    const INITIAL_USERS =")
    print("Added INITIAL_QUOTE_REQUESTS demo data!")

# 2. Redesign LeadModal Component
old_lead_modal = """    // 4-STEP INTERACTIVE LEAD GENERATION MOTOR MODAL (DÜĞÜN.COM ESİNTİSİ)
    function LeadModal({ isOpen, onClose, defaultEventType = 'Düğün' }) {"""

new_lead_modal = """    // 4-STEP UNIFIED INTERACTIVE LEAD GENERATION MOTOR MODAL (CENTERED & WHATSAPP SYNCED)
    function LeadModal({ isOpen, onClose, defaultEventType = 'Düğün', onSaveQuoteRequest, showToast }) {
      const [step, setStep] = useState(1);
      const [formData, setFormData] = useState({
        eventType: defaultEventType,
        preferredVenue: 'Saray Balo Salonu',
        guests: 400,
        date: '',
        name: '',
        phone: '',
        email: '',
        notes: ''
      });
      const [submitted, setSubmitted] = useState(false);

      if (!isOpen) return null;

      const handleNext = () => setStep(prev => Math.min(prev + 1, 4));
      const handlePrev = () => setStep(prev => Math.max(prev - 1, 1));

      const handleSubmit = (e) => {
        e.preventDefault();
        if (!formData.name.trim() || !formData.phone.trim()) {
          if (showToast) showToast('Lütfen Ad Soyad ve Telefon numaranızı giriniz.', 'error');
          return;
        }

        const newLead = {
          id: 'QUOTE-' + Date.now(),
          customerName: formData.name.trim(),
          customerPhone: formData.phone.trim(),
          customerEmail: formData.email.trim(),
          eventType: formData.eventType,
          preferredVenue: formData.preferredVenue,
          guestCount: formData.guests,
          eventDate: formData.date || 'Tarih Esnek',
          notes: formData.notes.trim(),
          status: 'beklemede',
          createdAt: new Date().toISOString()
        };

        // 1. Save locally & to database
        if (onSaveQuoteRequest) {
          onSaveQuoteRequest(newLead);
        } else {
          try {
            const existingLeads = JSON.parse(localStorage.getItem('irem_leads') || '[]');
            existingLeads.unshift(newLead);
            localStorage.setItem('irem_leads', JSON.stringify(existingLeads));
          } catch (err) {}
        }

        // 2. Open WhatsApp Message directly with full details
        const waText = 
`🎉 *İREM DÜĞÜN SARAYI - ÜCRETSİZ FİYAT TEKLİF TALEBİ* 🎉
------------------------------------------------
👤 *Müşteri Adı:* ${formData.name.trim()}
📞 *Telefon:* ${formData.phone.trim()}
✉️ *E-Posta:* ${formData.email.trim() || 'Belirtilmedi'}

💒 *Etkinlik Tipi:* ${formData.eventType}
🏛️ *Tercih Edilen Salon:* ${formData.preferredVenue}
👥 *Davetli Sayısı:* ${formData.guests} Kişi
📅 *Planlanan Tarih:* ${formData.date || 'Tarih Esnek'}
📝 *Notlar:* ${formData.notes.trim() || 'Yok'}
------------------------------------------------
✨ Web sitemiz üzerinden "Ücretsiz Teklif Al" formu ile gönderilmiştir.`;

        const waUrl = `https://wa.me/905471440054?text=${encodeURIComponent(waText)}`;
        window.open(waUrl, '_blank');

        if (showToast) showToast('Fiyat teklif talebiniz başarıyla alındı ve WhatsApp temsilcimize iletildi!');
        setSubmitted(true);
      };

      return (
        <div className="fixed inset-0 z-[99999] bg-black/80 backdrop-blur-md flex items-center justify-center p-4 overflow-y-auto animate-fade-in">
          <div className="bg-[#0f172a] border border-[#c5a059]/40 rounded-3xl max-w-xl w-full p-6 sm:p-8 space-y-6 text-white shadow-2xl relative my-auto">
            <button 
              onClick={onClose} 
              className="absolute top-5 right-5 w-8 h-8 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white flex items-center justify-center text-sm font-bold transition cursor-pointer"
              title="Kapat"
            >
              ✕
            </button>

            {!submitted ? (
              <>
                {/* STEP INDICATOR */}
                <div className="space-y-2">
                  <div className="flex justify-between items-center text-xs font-mono font-bold text-[#e2c07d]">
                    <span><ThemeIcon icon="crown" className="w-4 h-4 inline-block shrink-0" /> ÜCRETSİZ FİYAT TEKLİFİ MOTORU</span>
                    <span>ADIM {step} / 4</span>
                  </div>
                  <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-gradient-to-r from-[#c5a059] to-[#d4af37] transition-all duration-500" style={{ width: `${(step / 4) * 100}%` }} />
                  </div>
                </div>

                <form onSubmit={handleSubmit} className="space-y-6">
                  {/* STEP 1: ETKİNLİK TÜRÜ */}
                  {step === 1 && (
                    <div className="space-y-4 animate-fade-in">
                      <h3 className="text-xl font-serif font-bold text-[#e2c07d] text-center">1. Ne Tür Bir Davet Planlıyorsunuz?</h3>
                      <div className="grid grid-cols-2 gap-3">
                        {['Düğün', 'Nişan & Söz', 'Kına Gecesi', 'Sünnet Düğünü', 'Kır Düğünü', 'Kurumsal Davet'].map(type => (
                          <button
                            key={type}
                            type="button"
                            onClick={() => { setFormData({ ...formData, eventType: type }); handleNext(); }}
                            className={`p-4 rounded-2xl border text-xs font-bold text-left transition-all cursor-pointer flex items-center justify-between ${formData.eventType === type ? 'bg-[#c5a059]/20 border-[#c5a059] text-amber-300 shadow-md' : 'bg-slate-900 border-slate-800 text-slate-300 hover:border-[#c5a059]/40'}`}
                          >
                            <span>{type}</span>
                            <span className="text-[#c5a059]">→</span>
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* STEP 2: TERCİH EDİLEN SALON */}
                  {step === 2 && (
                    <div className="space-y-4 animate-fade-in">
                      <h3 className="text-xl font-serif font-bold text-[#e2c07d] text-center">2. Tercih Ettiğiniz Salon veya Konsept</h3>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        {[
                          { name: 'Saray Balo Salonu', cap: '750 Kişilik VIP Balo' },
                          { name: 'Safir Salon', cap: '500 Kişilik Şık Salon' },
                          { name: 'Kır Bahçesi', cap: '1000+ Kişilik Doğal Açık Hava' },
                          { name: 'Fark Etmez / Öneri İstiyorum', cap: 'Uzman Tavsiyesi' }
                        ].map(v => (
                          <button
                            key={v.name}
                            type="button"
                            onClick={() => { setFormData({ ...formData, preferredVenue: v.name }); handleNext(); }}
                            className={`p-4 rounded-2xl border text-left transition-all cursor-pointer space-y-1 ${formData.preferredVenue === v.name ? 'bg-[#c5a059]/20 border-[#c5a059] text-amber-300 shadow-md' : 'bg-slate-900 border-slate-800 text-slate-300 hover:border-[#c5a059]/40'}`}
                          >
                            <div className="text-xs font-extrabold text-white flex items-center justify-between">
                              <span>{v.name}</span>
                              <span className="text-[#c5a059]">→</span>
                            </div>
                            <div className="text-[10px] text-slate-400 font-medium">{v.cap}</div>
                          </button>
                        ))}
                      </div>
                      <div className="flex justify-between pt-2">
                        <button type="button" onClick={handlePrev} className="px-5 py-2.5 rounded-xl bg-slate-800 text-slate-300 text-xs font-bold cursor-pointer">Geri</button>
                      </div>
                    </div>
                  )}

                  {/* STEP 3: TAHMİNİ DAVETLİ SAYISI & TARİH */}
                  {step === 3 && (
                    <div className="space-y-5 animate-fade-in">
                      <h3 className="text-xl font-serif font-bold text-[#e2c07d] text-center">3. Davetli Sayısı & Planlanan Tarih</h3>
                      <div className="bg-slate-900/90 border border-slate-800 p-5 rounded-2xl space-y-3 text-center">
                        <div className="text-3xl font-mono font-black text-[#e2c07d]">{formData.guests} Davetli</div>
                        <input
                          type="range"
                          min="100"
                          max="1000"
                          step="50"
                          value={formData.guests}
                          onChange={e => setFormData({ ...formData, guests: Number(e.target.value) })}
                          className="w-full accent-[#c5a059] cursor-pointer"
                        />
                        <div className="flex justify-between text-[10px] text-slate-400 font-mono">
                          <span>100 Kişi (VIP Boutique)</span>
                          <span>1000+ Kişi (Kır Bahçesi)</span>
                        </div>
                      </div>

                      <div>
                        <label className="text-xs font-bold text-slate-300 block mb-1.5">Planlanan Etkinlik Tarihi (İsteğe Bağlı)</label>
                        <input
                          type="date"
                          value={formData.date}
                          onChange={e => setFormData({ ...formData, date: e.target.value })}
                          className="w-full bg-slate-900 border border-slate-800 rounded-xl p-3 text-xs text-white font-mono focus:border-[#c5a059] outline-none"
                        />
                      </div>

                      <div className="flex justify-between pt-2">
                        <button type="button" onClick={handlePrev} className="px-5 py-2.5 rounded-xl bg-slate-800 text-slate-300 text-xs font-bold cursor-pointer">Geri</button>
                        <button type="button" onClick={handleNext} className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-[#c5a059] to-[#d4af37] text-slate-950 text-xs font-extrabold cursor-pointer">Devam Et →</button>
                      </div>
                    </div>
                  )}

                  {/* STEP 4: İLETİŞİM BİLGİLERİ */}
                  {step === 4 && (
                    <div className="space-y-4 animate-fade-in">
                      <h3 className="text-xl font-serif font-bold text-[#e2c07d] text-center">4. İletişim Bilgileriniz & Teklif Gönderimi</h3>
                      <div className="space-y-3">
                        <div>
                          <label className="text-xs font-bold text-slate-300 block mb-1">Adınız Soyadınız *</label>
                          <input required type="text" value={formData.name} onChange={e => setFormData({ ...formData, name: e.target.value })} className="w-full bg-slate-900 border border-slate-800 rounded-xl p-3 text-xs text-white focus:border-[#c5a059] outline-none" placeholder="Ahmet & Zeynep Yılmaz" />
                        </div>
                        <div>
                          <label className="text-xs font-bold text-slate-300 block mb-1">Cep Telefonu (WhatsApp Teklif Teyidi İçin) *</label>
                          <input required type="tel" value={formData.phone} onChange={e => setFormData({ ...formData, phone: e.target.value })} className="w-full bg-slate-900 border border-slate-800 rounded-xl p-3 text-xs text-white focus:border-[#c5a059] outline-none" placeholder="+90 547 144 00 54" />
                        </div>
                        <div>
                          <label className="text-xs font-bold text-slate-300 block mb-1">E-Posta Adresi (Opsiyonel)</label>
                          <input type="email" value={formData.email} onChange={e => setFormData({ ...formData, email: e.target.value })} className="w-full bg-slate-900 border border-slate-800 rounded-xl p-3 text-xs text-white focus:border-[#c5a059] outline-none" placeholder="ornek@gmail.com" />
                        </div>
                        <div>
                          <label className="text-xs font-bold text-slate-300 block mb-1">Eklemek İstediğiniz Notlar</label>
                          <textarea rows="2" value={formData.notes} onChange={e => setFormData({ ...formData, notes: e.target.value })} className="w-full bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-white focus:border-[#c5a059] outline-none resize-none" placeholder="Örn: Vejetaryen ikram ve çocuk oyun alanı talebi..." />
                        </div>
                      </div>
                      <div className="flex justify-between pt-2">
                        <button type="button" onClick={handlePrev} className="px-5 py-2.5 rounded-xl bg-slate-800 text-slate-300 text-xs font-bold cursor-pointer">Geri</button>
                        <button type="submit" className="px-8 py-3.5 rounded-xl bg-[#25D366] hover:bg-[#20bd5a] text-white text-xs font-extrabold shadow-xl cursor-pointer flex items-center space-x-2 border border-emerald-400/40">
                          <svg className="w-4 h-4 fill-current shrink-0" viewBox="0 0 24 24">
                            <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/>
                          </svg>
                          <span>Ücretsiz Teklif Al!</span>
                        </button>
                      </div>
                    </div>
                  )}
                </form>
              </>
            ) : (
              <div className="text-center space-y-4 py-6 animate-fade-in">
                <div className="w-16 h-16 rounded-full bg-emerald-500/20 text-emerald-400 text-3xl flex items-center justify-center mx-auto border border-emerald-500/40">✓</div>
                <h3 className="text-2xl font-serif font-bold text-[#e2c07d]">Teklif Talebiniz Başarıyla Kaydedildi!</h3>
                <p className="text-xs text-slate-300 max-w-md mx-auto leading-relaxed">
                  Tebrikler Sayın <strong className="text-white">{formData.name}</strong>. Talebiniz veritabanımıza işlendi ve WhatsApp müşteri temsilcimize iletildi. En kısa sürede sizinle iletişime geçilecektir.
                </p>
                <div className="pt-4">
                  <button onClick={onClose} className="bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs px-6 py-3 rounded-xl cursor-pointer">Pencereyi Kapat</button>
                </div>
              </div>
            )}
          </div>
        </div>
      );
    }"""

if old_lead_modal in content:
    content = content.replace(old_lead_modal, new_lead_modal)
    print("Redesigned LeadModal with screen-centered styling and WhatsApp direct message integration!")

# 3. Define Management QuoteRequestsPageComponent Component
quote_requests_page_code = """
    // MANAGEMENT DASHBOARD: FIYAT TEKLİF TALEPLERİ (LEADS) LISTING PAGE
    function QuoteRequestsPageComponent({ quoteRequests = [], setQuoteRequests, showToast, navigateTo, setRedAlertModalData }) {
      const [filterStatus, setFilterStatus] = useState('all');
      const [searchTerm, setSearchTerm] = useState('');

      const filteredRequests = useMemo(() => {
        return (quoteRequests || []).filter(req => {
          const matchesStatus = filterStatus === 'all' || req.status === filterStatus;
          const searchLower = searchTerm.toLowerCase();
          const matchesSearch = !searchTerm || 
            (req.customerName || '').toLowerCase().includes(searchLower) ||
            (req.customerPhone || '').toLowerCase().includes(searchLower) ||
            (req.eventType || '').toLowerCase().includes(searchLower) ||
            (req.preferredVenue || '').toLowerCase().includes(searchLower);

          return matchesStatus && matchesSearch;
        });
      }, [quoteRequests, filterStatus, searchTerm]);

      const handleUpdateStatus = (reqId, newStatus) => {
        setQuoteRequests(prev => {
          const updated = (prev || []).map(r => r.id === reqId ? { ...r, status: newStatus } : r);
          CacheService.set('quote_requests', updated);
          if (window.fetchWithRetry) {
            window.fetchWithRetry('/api/public-settings', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ quoteRequests: updated })
            }).catch(() => {});
          }
          return updated;
        });
        if (showToast) showToast(`Talep durumu "${newStatus.toUpperCase()}" olarak güncellendi.`);
      };

      const handleDeleteRequest = (reqId, custName) => {
        setRedAlertModalData({
          title: 'TEKLİF TALEBİ SİLİNECEK',
          message: `"${custName}" tarafından oluşturulan fiyat teklif talebini silmek istediğinize emin misiniz?`,
          confirmText: 'Evet, Talebi Sil',
          onConfirm: () => {
            setQuoteRequests(prev => {
              const updated = (prev || []).filter(r => r.id !== reqId);
              CacheService.set('quote_requests', updated);
              if (window.fetchWithRetry) {
                window.fetchWithRetry('/api/public-settings', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ quoteRequests: updated })
                }).catch(() => {});
              }
              return updated;
            });
            if (showToast) showToast('Teklif Talebi Silindi.');
          }
        });
      };

      const handleConvertToReservation = (req) => {
        if (navigateTo) {
          navigateTo('create-reservation', {
            customerName: req.customerName,
            customerPhone: req.customerPhone,
            customerEmail: req.customerEmail,
            eventType: req.eventType,
            venue: req.preferredVenue,
            date: req.eventDate,
            guests: req.guestCount
          });
        }
      };

      const statusBadges = {
        beklemede: { label: 'Beklemede', bg: 'bg-amber-500/10 text-amber-600 border-amber-500/30' },
        arandi: { label: 'Görüşüldü', bg: 'bg-blue-500/10 text-blue-600 border-blue-500/30' },
        teklif_gonderildi: { label: 'Teklif Gönderildi', bg: 'bg-purple-500/10 text-purple-600 border-purple-500/30' },
        onaylandi: { label: 'Onaylandı (Rezervasyon)', bg: 'bg-emerald-500/10 text-emerald-600 border-emerald-500/30' },
        iptal: { label: 'İptal / Olumsuz', bg: 'bg-red-500/10 text-red-600 border-red-500/30' }
      };

      return (
        <div className="space-y-6 animate-fade-in">
          {/* HEADER SUMMARY BAR */}
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white dark:bg-brand-card p-6 rounded-3xl border border-slate-200 dark:border-brand-border/30 shadow-sm">
            <div>
              <div className="flex items-center space-x-2">
                <span className="w-3 h-3 rounded-full bg-amber-500 animate-ping" />
                <h2 className="text-2xl font-serif font-extrabold text-slate-900 dark:text-gold-400">
                  Fiyat Teklif Talepleri (Gelen Leads)
                </h2>
              </div>
              <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">
                Web sitesi ve WhatsApp teklif motorundan gönderilen tüm müşteri adayları veritabanı kaydı.
              </p>
            </div>
            <div className="flex items-center space-x-3">
              <span className="text-xs font-bold text-slate-600 dark:text-gray-300">
                Toplam Talep: <strong className="text-amber-500 text-base">{quoteRequests.length} Adet</strong>
              </span>
            </div>
          </div>

          {/* FILTERS & SEARCH BAR */}
          <div className="flex flex-col sm:flex-row gap-3 justify-between items-center bg-white dark:bg-brand-card p-4 rounded-2xl border border-slate-200 dark:border-brand-border/30 shadow-xs">
            <div className="flex flex-wrap gap-2 w-full sm:w-auto">
              {[
                { id: 'all', label: 'Tüm Talepler' },
                { id: 'beklemede', label: 'Bekleyenler' },
                { id: 'arandi', label: 'Görüşülenler' },
                { id: 'teklif_gonderildi', label: 'Teklif Gönderilenler' },
                { id: 'onaylandi', label: 'Onaylananlar' }
              ].map(f => (
                <button
                  key={f.id}
                  onClick={() => setFilterStatus(f.id)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-bold transition cursor-pointer ${
                    filterStatus === f.id ? 'bg-amber-500 text-slate-950 shadow-sm' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-gray-300 hover:bg-slate-200'
                  }`}
                >
                  {f.label}
                </button>
              ))}
            </div>

            <div className="w-full sm:w-72">
              <input
                type="text"
                value={searchTerm}
                onChange={e => setSearchTerm(e.target.value)}
                placeholder="Müşteri adı, tel veya salon ara..."
                className="w-full bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl px-3.5 py-2 text-xs text-slate-800 dark:text-white focus:border-amber-500 outline-none"
              />
            </div>
          </div>

          {/* DATA TABLE */}
          <div className="bg-white dark:bg-brand-card rounded-3xl border border-slate-200 dark:border-brand-border/30 shadow-sm overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-slate-50 dark:bg-slate-900/60 border-b border-slate-200 dark:border-brand-border/30 text-[11px] font-extrabold text-slate-500 dark:text-gray-400 uppercase tracking-wider">
                    <th className="p-4">Talep No / Tarih</th>
                    <th className="p-4">Müşteri Adı & İletişim</th>
                    <th className="p-4">Etkinlik Tipi & Salon</th>
                    <th className="p-4">Kişi & Tarih</th>
                    <th className="p-4">Durum</th>
                    <th className="p-4 text-right">İşlemler</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-brand-border/20 text-xs">
                  {filteredRequests.length > 0 ? (
                    filteredRequests.map(req => {
                      const st = statusBadges[req.status] || statusBadges.beklemede;
                      const formattedCreatedAt = new Date(req.createdAt).toLocaleDateString('tr-TR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' });

                      return (
                        <tr key={req.id} className="hover:bg-slate-50/80 dark:hover:bg-brand-card/80 transition">
                          <td className="p-4 font-mono font-bold text-amber-600 dark:text-amber-400">
                            <div>{req.id}</div>
                            <div className="text-[10px] text-slate-400 font-normal mt-0.5">{formattedCreatedAt}</div>
                          </td>
                          <td className="p-4">
                            <div className="font-extrabold text-slate-900 dark:text-white">{req.customerName}</div>
                            <div className="text-[11px] text-slate-500 dark:text-gray-400 flex items-center space-x-2 mt-0.5">
                              <a href={`tel:${req.customerPhone}`} className="hover:text-amber-500">{req.customerPhone}</a>
                              {req.customerEmail && <span>• {req.customerEmail}</span>}
                            </div>
                          </td>
                          <td className="p-4">
                            <div className="font-bold text-slate-800 dark:text-gray-200">{req.eventType}</div>
                            <div className="text-[11px] text-amber-600 dark:text-gold-400 font-medium">{req.preferredVenue}</div>
                          </td>
                          <td className="p-4">
                            <div className="font-bold text-slate-800 dark:text-gray-200">{req.guestCount} Davetli</div>
                            <div className="text-[11px] text-slate-400">{req.eventDate}</div>
                          </td>
                          <td className="p-4">
                            <span className={`inline-block px-2.5 py-1 rounded-full text-[10px] font-extrabold border ${st.bg}`}>
                              {st.label}
                            </span>
                          </td>
                          <td className="p-4 text-right">
                            <div className="flex items-center justify-end space-x-2">
                              {/* WHATSAPP ACTION BUTTON */}
                              <a
                                href={`https://wa.me/${(req.customerPhone || '').replace(/[^0-9]/g, '')}`}
                                target="_blank"
                                rel="noreferrer"
                                className="p-2 rounded-xl bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-600 transition"
                                title="WhatsApp Chat Başlat"
                              >
                                💬
                              </a>

                              {/* UPDATE STATUS SELECT */}
                              <select
                                value={req.status}
                                onChange={e => handleUpdateStatus(req.id, e.target.value)}
                                className="bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-white text-[11px] font-bold rounded-xl px-2 py-1.5 outline-none cursor-pointer"
                              >
                                <option value="beklemede">Beklemede</option>
                                <option value="arandi">Görüşüldü</option>
                                <option value="teklif_gonderildi">Teklif Gönderildi</option>
                                <option value="onaylandi">Onaylandı</option>
                                <option value="iptal">İptal</option>
                              </select>

                              {/* CONVERT TO RESERVATION */}
                              <button
                                onClick={() => handleConvertToReservation(req)}
                                className="bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold px-3 py-1.5 rounded-xl text-[11px] transition shadow-xs cursor-pointer"
                                title="Bu talebi rezervasyona dönüştür"
                              >
                                📅 Rezervasyona Dönüştür
                              </button>

                              {/* DELETE */}
                              <button
                                onClick={() => handleDeleteRequest(req.id, req.customerName)}
                                className="p-1.5 text-slate-400 hover:text-red-500 transition cursor-pointer text-sm"
                                title="Talebi Sil"
                              >
                                🗑️
                              </button>
                            </div>
                          </td>
                        </tr>
                      );
                    })
                  ) : (
                    <tr>
                      <td colSpan="6" className="p-8 text-center text-slate-500 dark:text-gray-400 font-medium">
                        Kayıtlı fiyat teklif talebi bulunamadı.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      );
    }
"""

marker = "    // 3. PUBLIC LAYOUT MODULE (ISOLATED NAVBAR & FOOTER BLOCKS)"
marker_idx = content.find(marker)

if marker_idx != -1:
    content = content[:marker_idx] + quote_requests_page_code + "\n" + content[marker_idx:]
    print("Added QuoteRequestsPageComponent management component!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
