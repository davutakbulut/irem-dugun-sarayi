import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = "    function LeadModal({ isOpen, onClose, defaultEventType = 'Düğün', onSaveQuoteRequest, showToast }) {"
end_marker = "    function PublicFooter({ navigateTo }) {"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

print(f"start_idx: {start_idx}, end_idx: {end_idx}")

if start_idx != -1 and end_idx != -1:
    new_lead_modal_code = """    function LeadModal({ isOpen, onClose, defaultEventType = 'Düğün', onSaveQuoteRequest, showToast }) {
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

      // Lock body scrolling when modal is open to ensure viewport centering
      useEffect(() => {
        if (isOpen) {
          document.body.style.overflow = 'hidden';
        } else {
          document.body.style.overflow = '';
        }
        return () => { document.body.style.overflow = ''; };
      }, [isOpen]);

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

      const modalJSX = (
        <div 
          className="fixed inset-0 top-0 left-0 w-screen h-screen z-[999999] bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 sm:p-6 overflow-y-auto animate-fade-in"
          onClick={(e) => {
            if (e.target === e.currentTarget) onClose();
          }}
        >
          {/* ELEGANT LIGHT LUXURY CARD IN HARMONY WITH PUBLIC SITE THEME */}
          <div className="bg-white border border-amber-200/80 rounded-3xl max-w-xl w-full p-6 sm:p-8 space-y-6 text-slate-800 shadow-[0_25px_60px_rgba(0,0,0,0.22)] relative my-auto max-h-[90vh] overflow-y-auto custom-scrollbar">
            <button 
              onClick={onClose} 
              className="absolute top-5 right-5 w-8 h-8 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-500 hover:text-slate-900 flex items-center justify-center text-sm font-bold transition cursor-pointer z-10 shadow-xs"
              title="Kapat"
            >
              ✕
            </button>

            {!submitted ? (
              <>
                {/* STEP INDICATOR */}
                <div className="space-y-2">
                  <div className="flex justify-between items-center text-xs font-mono font-bold text-[#B89B5E]">
                    <span className="flex items-center space-x-1.5">
                      <ThemeIcon icon="crown" className="w-4 h-4 text-[#B89B5E] inline-block shrink-0" />
                      <span>ÜCRETSİZ FİYAT TEKLİFİ MOTORU</span>
                    </span>
                    <span className="text-slate-400">ADIM {step} / 4</span>
                  </div>
                  <div className="w-full h-1.5 bg-amber-100/60 rounded-full overflow-hidden">
                    <div className="h-full bg-gradient-to-r from-[#B89B5E] to-[#ceb992] transition-all duration-500 rounded-full" style={{ width: `${(step / 4) * 100}%` }} />
                  </div>
                </div>

                <form onSubmit={handleSubmit} className="space-y-6 pt-1">
                  {/* STEP 1: ETKİNLİK TÜRÜ */}
                  {step === 1 && (
                    <div className="space-y-4 animate-fade-in">
                      <h3 className="text-xl sm:text-2xl font-serif font-extrabold text-slate-900 text-center">1. Ne Tür Bir Davet Planlıyorsunuz?</h3>
                      <div className="grid grid-cols-2 gap-3">
                        {['Düğün', 'Nişan & Söz', 'Kına Gecesi', 'Sünnet Düğünü', 'Kır Düğünü', 'Kurumsal Davet'].map(type => (
                          <button
                            key={type}
                            type="button"
                            onClick={() => { setFormData({ ...formData, eventType: type }); handleNext(); }}
                            className={`p-4 rounded-2xl border text-xs font-extrabold text-left transition-all cursor-pointer flex items-center justify-between ${
                              formData.eventType === type 
                                ? 'bg-amber-50/90 border-2 border-[#B89B5E] text-[#B89B5E] shadow-sm' 
                                : 'bg-slate-50 border-slate-200 text-slate-700 hover:border-[#B89B5E]/60 hover:bg-amber-50/30'
                            }`}
                          >
                            <span>{type}</span>
                            <span className="text-[#B89B5E] font-bold">→</span>
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* STEP 2: TERCİH EDİLEN SALON */}
                  {step === 2 && (
                    <div className="space-y-4 animate-fade-in">
                      <h3 className="text-xl sm:text-2xl font-serif font-extrabold text-slate-900 text-center">2. Tercih Ettiğiniz Salon veya Konsept</h3>
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
                            className={`p-4 rounded-2xl border text-left transition-all cursor-pointer space-y-1 ${
                              formData.preferredVenue === v.name 
                                ? 'bg-amber-50/90 border-2 border-[#B89B5E] text-slate-900 shadow-sm' 
                                : 'bg-slate-50 border-slate-200 text-slate-700 hover:border-[#B89B5E]/60 hover:bg-amber-50/30'
                            }`}
                          >
                            <div className="text-xs font-extrabold text-slate-900 flex items-center justify-between">
                              <span>{v.name}</span>
                              <span className="text-[#B89B5E] font-bold">→</span>
                            </div>
                            <div className="text-[10px] text-slate-500 font-medium">{v.cap}</div>
                          </button>
                        ))}
                      </div>
                      <div className="flex justify-between pt-2">
                        <button type="button" onClick={handlePrev} className="px-5 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold cursor-pointer transition">Geri</button>
                      </div>
                    </div>
                  )}

                  {/* STEP 3: TAHMİNİ DAVETLİ SAYISI & TARİH */}
                  {step === 3 && (
                    <div className="space-y-5 animate-fade-in">
                      <h3 className="text-xl sm:text-2xl font-serif font-extrabold text-slate-900 text-center">3. Davetli Sayısı & Planlanan Tarih</h3>
                      <div className="bg-amber-50/70 border border-amber-200/80 p-5 rounded-2xl space-y-3 text-center">
                        <div className="text-3xl sm:text-4xl font-serif font-black text-[#B89B5E]">{formData.guests} Davetli</div>
                        <input
                          type="range"
                          min="100"
                          max="1000"
                          step="50"
                          value={formData.guests}
                          onChange={e => setFormData({ ...formData, guests: Number(e.target.value) })}
                          className="w-full accent-[#B89B5E] cursor-pointer"
                        />
                        <div className="flex justify-between text-[10px] text-slate-500 font-mono">
                          <span>100 Kişi (VIP Boutique)</span>
                          <span>1000+ Kişi (Kır Bahçesi)</span>
                        </div>
                      </div>

                      <div>
                        <label className="text-xs font-bold text-slate-700 block mb-1.5">Planlanan Etkinlik Tarihi (İsteğe Bağlı)</label>
                        <input
                          type="date"
                          value={formData.date}
                          onChange={e => setFormData({ ...formData, date: e.target.value })}
                          className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs text-slate-900 font-medium focus:border-[#B89B5E] focus:bg-white outline-none transition"
                        />
                      </div>

                      <div className="flex justify-between pt-2">
                        <button type="button" onClick={handlePrev} className="px-5 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold cursor-pointer transition">Geri</button>
                        <button type="button" onClick={handleNext} className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-[#B89B5E] to-[#ceb992] text-white text-xs font-extrabold shadow-md cursor-pointer transition hover:scale-105">Devam Et →</button>
                      </div>
                    </div>
                  )}

                  {/* STEP 4: İLETİŞİM BİLGİLERİ */}
                  {step === 4 && (
                    <div className="space-y-4 animate-fade-in">
                      <h3 className="text-xl sm:text-2xl font-serif font-extrabold text-slate-900 text-center">4. İletişim Bilgileriniz & Teklif Gönderimi</h3>
                      <div className="space-y-3">
                        <div>
                          <label className="text-xs font-bold text-slate-700 block mb-1">Adınız Soyadınız *</label>
                          <input required type="text" value={formData.name} onChange={e => setFormData({ ...formData, name: e.target.value })} className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs text-slate-900 focus:border-[#B89B5E] focus:bg-white outline-none transition placeholder:text-slate-400" placeholder="Ahmet & Zeynep Yılmaz" />
                        </div>
                        <div>
                          <label className="text-xs font-bold text-slate-700 block mb-1">Cep Telefonu (WhatsApp Teklif Teyidi İçin) *</label>
                          <input required type="tel" value={formData.phone} onChange={e => setFormData({ ...formData, phone: e.target.value })} className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs text-slate-900 focus:border-[#B89B5E] focus:bg-white outline-none transition placeholder:text-slate-400" placeholder="+90 547 144 00 54" />
                        </div>
                        <div>
                          <label className="text-xs font-bold text-slate-300 block mb-1 text-slate-700">E-Posta Adresi (Opsiyonel)</label>
                          <input type="email" value={formData.email} onChange={e => setFormData({ ...formData, email: e.target.value })} className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs text-slate-900 focus:border-[#B89B5E] focus:bg-white outline-none transition placeholder:text-slate-400" placeholder="ornek@gmail.com" />
                        </div>
                        <div>
                          <label className="text-xs font-bold text-slate-700 block mb-1">Eklemek İstediğiniz Notlar</label>
                          <textarea rows="2" value={formData.notes} onChange={e => setFormData({ ...formData, notes: e.target.value })} className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-xs text-slate-900 focus:border-[#B89B5E] focus:bg-white outline-none resize-none transition placeholder:text-slate-400" placeholder="Örn: Vejetaryen ikram ve çocuk oyun alanı talebi..." />
                        </div>
                      </div>
                      <div className="flex justify-between pt-2">
                        <button type="button" onClick={handlePrev} className="px-5 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold cursor-pointer transition">Geri</button>
                        <button type="submit" className="px-8 py-3.5 rounded-full bg-[#25D366] hover:bg-[#20bd5a] text-white text-xs font-extrabold shadow-lg transition-all duration-300 hover:scale-105 cursor-pointer flex items-center space-x-2.5 uppercase tracking-wider border border-emerald-400/30">
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
                <div className="w-16 h-16 rounded-full bg-emerald-100 text-emerald-600 text-3xl flex items-center justify-center mx-auto border border-emerald-200 shadow-inner">✓</div>
                <h3 className="text-2xl font-serif font-extrabold text-slate-900">Teklif Talebiniz Başarıyla Kaydedildi!</h3>
                <p className="text-xs text-slate-600 max-w-md mx-auto leading-relaxed font-medium">
                  Tebrikler Sayın <strong className="text-slate-900">{formData.name}</strong>. Talebiniz veritabanımıza işlendi ve WhatsApp müşteri temsilcimize iletildi. En kısa sürede sizinle iletişime geçilecektir.
                </p>
                <div className="pt-4">
                  <button onClick={onClose} className="bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs px-7 py-3 rounded-full shadow-md cursor-pointer transition">Pencereyi Kapat</button>
                </div>
              </div>
            )}
          </div>
        </div>
      );

      if (typeof document !== 'undefined' && document.body && window.ReactDOM && window.ReactDOM.createPortal) {
        return window.ReactDOM.createPortal(modalJSX, document.body);
      }
      return modalJSX;
    }
"""
    content = content[:start_idx] + new_lead_modal_code + content[end_idx:]
    print("Successfully redesigned LeadModal to clean light luxury theme matching site design!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
