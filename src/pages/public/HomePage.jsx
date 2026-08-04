import React, { useState } from 'react';

export default function HomePage({ navigateTo }) {
  const [quoteForm, setQuoteForm] = useState({
    name: '',
    phone: '',
    eventDate: '',
    guestCount: '250-500',
    eventType: 'Düğün / Balo',
    message: '',
  });

  const [formSubmitted, setFormSubmitted] = useState(false);

  const handleQuoteSubmit = (e) => {
    e.preventDefault();
    setFormSubmitted(true);
    setTimeout(() => {
      setFormSubmitted(false);
      setQuoteForm({
        name: '',
        phone: '',
        eventDate: '',
        guestCount: '250-500',
        eventType: 'Düğün / Balo',
        message: '',
      });
    }, 4000);
  };

  return (
    <div className="space-y-24 pb-16">
      
      {/* SECTION 1: FULL-SCREEN HERO SHOWCASE */}
      <section className="relative min-h-[90vh] flex items-center justify-center overflow-hidden -mt-20 pt-20">
        {/* HERO BACKGROUND VIDEO / IMAGE */}
        <div className="absolute inset-0 z-0">
          <img
            src="https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=2000&q=80"
            alt="İrem Düğün Sarayı Balo Tesisleri"
            className="w-full h-full object-cover object-center transform scale-105 animate-pulse duration-[10000ms]"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/75 to-slate-950/60" />
        </div>

        {/* HERO CONTENT CONTAINER */}
        <div className="relative z-10 max-w-7xl mx-auto px-6 sm:px-12 py-16 grid grid-cols-1 lg:grid-cols-12 gap-12 items-center w-full">
          
          {/* LEFT HERO TEXT */}
          <div className="lg:col-span-7 space-y-6 text-center lg:text-left text-white">
            <div className="inline-flex items-center space-x-2 bg-amber-500/10 border border-amber-500/30 text-amber-300 px-4 py-2 rounded-full text-xs font-extrabold shadow-inner">
              <span>👑</span>
              <span>Sapanca Göl Kenarında Lüks Düğün & Balo Deneyimi</span>
            </div>

            <h1 className="text-4xl sm:text-6xl font-heading font-extrabold tracking-tight leading-tight">
              Hayallerinizin Ötesinde Bir <br className="hidden sm:block" />
              <span className="bg-gradient-to-r from-amber-400 via-orange-400 to-amber-500 bg-clip-text text-transparent">
                Masalsı Düğün Daveti
              </span>
            </h1>

            <p className="text-sm sm:text-base text-slate-300 leading-relaxed max-w-2xl font-medium mx-auto lg:mx-0">
              4 farklı konsept balo salonu, kır bahçesi, VIP ikram servisi ve yüksek kapasiteli organizasyon imkanları. Hayatınızın en özel gecesini kusursuz detaylarla tasarlıyoruz.
            </p>

            <div className="pt-4 flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4">
              <button
                onClick={() => navigateTo && navigateTo('/salonlar')}
                className="gold-button font-extrabold text-sm px-8 py-4 rounded-2xl shadow-2xl hover:scale-105 transition cursor-pointer flex items-center space-x-2 w-full sm:w-auto justify-center"
              >
                <span>Salonlarımızı Keşfedin</span>
                <span>→</span>
              </button>

              <button
                onClick={() => navigateTo && navigateTo('/360-tur')}
                className="bg-slate-900/90 hover:bg-slate-800 text-amber-400 font-bold text-sm px-7 py-4 rounded-2xl border border-amber-500/40 backdrop-blur-md transition cursor-pointer flex items-center space-x-2.5 w-full sm:w-auto justify-center"
              >
                <span className="animate-pulse text-red-500">🔴</span>
                <span>360° Sanal Turu Başlat</span>
              </button>
            </div>

            {/* TRUST BADGES */}
            <div className="pt-8 border-t border-slate-800/80 grid grid-cols-3 gap-4 max-w-lg mx-auto lg:mx-0 text-center">
              <div>
                <div className="text-2xl font-black text-amber-400">1500+</div>
                <div className="text-[11px] text-slate-400 font-medium">Mutlu Çift</div>
              </div>
              <div>
                <div className="text-2xl font-black text-amber-400">4 Konsept</div>
                <div className="text-[11px] text-slate-400 font-medium">Balo Salonu</div>
              </div>
              <div>
                <div className="text-2xl font-black text-amber-400">%100</div>
                <div className="text-[11px] text-slate-400 font-medium">Memnuniyet</div>
              </div>
            </div>
          </div>

          {/* RIGHT QUICK QUOTE FORM CARD */}
          <div className="lg:col-span-5">
            <div className="bg-slate-900/95 backdrop-blur-2xl p-8 rounded-3xl border-2 border-amber-500/30 shadow-2xl text-white space-y-6">
              
              <div className="space-y-1">
                <span className="text-amber-400 text-xs font-bold uppercase tracking-wider">
                  ⚡ Hızlı Fiyat ve Tarih Sorgulama
                </span>
                <h3 className="text-2xl font-heading font-extrabold text-white">
                  Düğün Unvanı & Tarih Alın
                </h3>
                <p className="text-xs text-slate-400">
                  Tarihinizi ve kişi sayınızı seçin, organizasyon ekibimiz 15 dakikada size özel fiyat teklifini hazırlasın.
                </p>
              </div>

              {formSubmitted ? (
                <div className="bg-emerald-500/10 border border-emerald-500/40 p-6 rounded-2xl text-center space-y-3 animate-fade-in">
                  <div className="text-4xl">✅</div>
                  <h4 className="text-lg font-bold text-emerald-400">Teklif Talebiniz Alındı!</h4>
                  <p className="text-xs text-slate-300">
                    Müşteri temsilcimiz vermiş olduğunuz telefon numarası üzerinden en kısa sürede size ulaşacaktır.
                  </p>
                </div>
              ) : (
                <form onSubmit={handleQuoteSubmit} className="space-y-4">
                  <div>
                    <label className="block text-[11px] font-bold text-slate-300 mb-1">
                      Adınız ve Soyadınız *
                    </label>
                    <input
                      type="text"
                      required
                      placeholder="Örn: Ayşe Yılmaz"
                      value={quoteForm.name}
                      onChange={(e) => setQuoteForm({ ...quoteForm, name: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 focus:border-amber-500 text-white text-xs px-4 py-3 rounded-xl outline-none transition"
                    />
                  </div>

                  <div>
                    <label className="block text-[11px] font-bold text-slate-300 mb-1">
                      Telefon Numarası *
                    </label>
                    <input
                      type="tel"
                      required
                      placeholder="Örn: 0532 000 00 00"
                      value={quoteForm.phone}
                      onChange={(e) => setQuoteForm({ ...quoteForm, phone: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 focus:border-amber-500 text-white text-xs px-4 py-3 rounded-xl outline-none transition"
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-[11px] font-bold text-slate-300 mb-1">
                        Düğün / Etkinlik Tarihi
                      </label>
                      <input
                        type="date"
                        value={quoteForm.eventDate}
                        onChange={(e) => setQuoteForm({ ...quoteForm, eventDate: e.target.value })}
                        className="w-full bg-slate-950 border border-slate-800 focus:border-amber-500 text-white text-xs px-3 py-3 rounded-xl outline-none transition"
                      />
                    </div>

                    <div>
                      <label className="block text-[11px] font-bold text-slate-300 mb-1">
                        Tahmini Kişi Sayısı
                      </label>
                      <select
                        value={quoteForm.guestCount}
                        onChange={(e) => setQuoteForm({ ...quoteForm, guestCount: e.target.value })}
                        className="w-full bg-slate-950 border border-slate-800 focus:border-amber-500 text-white text-xs px-3 py-3 rounded-xl outline-none transition"
                      >
                        <option value="100-250">100 - 250 Kişi</option>
                        <option value="250-500">250 - 500 Kişi</option>
                        <option value="500-1000">500 - 1000 Kişi</option>
                        <option value="1000+">1000+ Kişi (Kır Bahçesi)</option>
                      </select>
                    </div>
                  </div>

                  <button
                    type="submit"
                    className="w-full gold-button font-extrabold text-sm py-4 rounded-xl shadow-xl hover:scale-[1.02] transition cursor-pointer"
                  >
                    Ücretsiz Özel Teklif Al →
                  </button>
                </form>
              )}

            </div>
          </div>

        </div>
      </section>

      {/* SECTION 2: FEATURED HALLS SHOWCASE */}
      <section className="max-w-7xl mx-auto px-6 sm:px-12 space-y-12">
        <div className="text-center space-y-3 max-w-3xl mx-auto">
          <span className="text-amber-500 font-extrabold text-xs uppercase tracking-widest">
            👑 Konsept Salonlarımız
          </span>
          <h2 className="text-3xl sm:text-4xl font-heading font-extrabold">
            Eşsiz Mimarisiyle 4 Farklı Balo Alanı
          </h2>
          <p className="text-xs sm:text-sm text-slate-400 leading-relaxed">
            İster açık havada göl manzaralı kır düğünü, ister yüksek tavanlı saray ihtişamı.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[
            {
              title: 'Göl Manzaralı Kır Bahçesi',
              capacity: '1.500 Kişi',
              type: 'Açık Hava & Kır Düğünü',
              img: 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=600&q=80',
              badge: 'AÇIK ALAN',
            },
            {
              title: 'Saray Balo Salonu',
              capacity: '1.000 Kişi',
              type: 'Yüksek Tavan & Kolonsuz',
              img: 'https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=600&q=80',
              badge: 'KAPALI LUXURY',
            },
            {
              title: 'Safir Balo Salonu',
              capacity: '600 Kişi',
              type: 'Modern Işık & Ses Sistemi',
              img: 'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=600&q=80',
              badge: 'BUTİK DAVET',
            },
            {
              title: 'VIP Lounge & Kına Salonu',
              capacity: '300 Kişi',
              type: 'Özel Taht & Nedime Alanı',
              img: 'https://images.unsplash.com/photo-1469371670807-013ccf25f16a?auto=format&fit=crop&w=600&q=80',
              badge: 'KINA & NİŞAN',
            },
          ].map((hall, idx) => (
            <div
              key={idx}
              onClick={() => navigateTo && navigateTo('/salonlar')}
              className="bg-slate-900/90 rounded-3xl border border-slate-800 hover:border-amber-500/60 overflow-hidden transition-all duration-300 hover:scale-[1.03] shadow-xl cursor-pointer group flex flex-col justify-between"
            >
              <div className="relative h-48 overflow-hidden">
                <img
                  src={hall.img}
                  alt={hall.title}
                  className="w-full h-full object-cover group-hover:scale-110 transition duration-500"
                />
                <span className="absolute top-3 right-3 bg-amber-500 text-slate-950 font-black text-[10px] px-2.5 py-1 rounded-full shadow">
                  {hall.badge}
                </span>
              </div>

              <div className="p-6 space-y-3 flex-1 flex flex-col justify-between">
                <div className="space-y-1">
                  <h3 className="font-heading font-extrabold text-lg text-white group-hover:text-amber-400 transition">
                    {hall.title}
                  </h3>
                  <p className="text-xs text-slate-400">{hall.type}</p>
                </div>

                <div className="pt-3 border-t border-slate-800 flex justify-between items-center text-xs text-amber-400 font-bold">
                  <span>Kapasite: {hall.capacity}</span>
                  <span>İncele →</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* SECTION 3: 360 DEGREE VIRTUAL TOUR BANNER */}
      <section className="max-w-7xl mx-auto px-6 sm:px-12">
        <div className="bg-gradient-to-r from-slate-900 via-slate-950 to-slate-900 p-8 sm:p-12 rounded-3xl border-2 border-amber-500/40 shadow-2xl relative overflow-hidden flex flex-col md:flex-row items-center justify-between gap-8">
          <div className="space-y-4 max-w-xl text-center md:text-left">
            <span className="bg-red-500/20 text-red-400 border border-red-500/40 text-xs font-extrabold px-3 py-1 rounded-full inline-flex items-center space-x-1.5">
              <span className="animate-pulse">🔴</span>
              <span>İnteraktif 3D Deneyim</span>
            </span>
            <h2 className="text-2xl sm:text-4xl font-heading font-extrabold text-white">
              Tesisimizi 360° Sanal Tur İle Evinizden Gezin
            </h2>
            <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
              Matterport 3D teknolojisi ile kır bahçemizi, gelin odalarını ve balo salonlarını detaylarıyla canlı olarak keşfedin.
            </p>
          </div>

          <button
            onClick={() => navigateTo && navigateTo('/360-tur')}
            className="gold-button font-extrabold text-sm px-8 py-4 rounded-2xl shadow-xl hover:scale-105 transition cursor-pointer shrink-0"
          >
            360° Sanal Tura Başla 🌐
          </button>
        </div>
      </section>

    </div>
  );
}
