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

  const handleNav = (route) => {
    if (navigateTo) navigateTo(route);
    else window.location.href = route;
  };

  return (
    <div className="bg-[#F5F2ED] text-[#1A1A1A] font-sans -mt-20 overflow-x-hidden">
      
      {/* SECTION 1: SVADBA STYLE HERO WITH AMBIENT VIDEO & OVERLAY */}
      <section className="relative min-h-screen flex flex-col justify-center items-center text-center overflow-hidden pt-20">
        {/* BACKGROUND VIDEO / AMBIENT OVERLAY */}
        <div className="absolute inset-0 w-full h-full z-0">
          <video
            className="w-full h-full object-cover scale-105"
            autoPlay
            muted
            loop
            playsInline
            poster="https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=2000&q=80"
          >
            <source src="https://cdn.creafolks.com/svadba-davet/9e9fee9d-dc11-4bd5-bc7a-4614de2d7e2b.mp4" type="video/mp4" />
          </video>
          <div className="absolute inset-0 bg-black/55" />
        </div>

        {/* HERO CONTENT */}
        <div className="relative z-20 container mx-auto px-4 text-white max-w-4xl space-y-6">
          <h1 className="text-4xl sm:text-6xl md:text-7xl font-bold tracking-widest font-sans uppercase">
            İREM DÜĞÜN SARAYI
          </h1>
          <p className="font-great-vibes text-3xl sm:text-5xl text-[#C5B37D] font-normal leading-relaxed">
            Sapanca Göl Kenarı Masalsı Düğün Mekanları
          </p>

          <div className="pt-6 flex flex-col sm:flex-row items-center justify-center gap-4">
            <button
              onClick={() => handleNav('/salonlar')}
              className="bg-[#C5B37D] hover:bg-[#b09e6a] text-black font-bold text-xs px-8 py-4 rounded-full transition cursor-pointer tracking-widest uppercase shadow-2xl"
            >
              MEKANLARIMIZI KEŞFEDİN
            </button>
            <button
              onClick={() => handleNav('/360-tur')}
              className="bg-white/10 hover:bg-white/20 text-white border border-white/30 backdrop-blur-md font-bold text-xs px-8 py-4 rounded-full transition cursor-pointer tracking-widest uppercase"
            >
              360° SANAL TUR
            </button>
          </div>
        </div>
      </section>

      {/* SECTION 2: SVADBA INTRO TEXT & CENTERED VIDEO */}
      <section className="py-20 px-4 sm:px-8 max-w-7xl mx-auto">
        <div className="bg-[#F5F2ED] rounded-2xl p-6 sm:p-12 border border-[#E6E1D8] shadow-sm">
          <div className="flex flex-col lg:flex-row items-center justify-center gap-8 lg:gap-12">
            
            {/* LEFT TEXT */}
            <div className="flex-1 text-right text-sm leading-relaxed text-[#333333] space-y-4">
              <p>
                Sektöründe lider olma hedefi ile hiçbir fedakârlıktan kaçınılmadan sarf edilen gayretler karşılıksız kalmamış ve herkesin takdirini toplamayı başaran bir mekâna dönüşmüştür.
              </p>
              <p>
                Bugüne kadar binlerce organizasyona ev sahipliği yapan <strong>İREM DÜĞÜN SARAYI</strong>, misafirlerinin teveccühleri ile her geçen gün hizmet kalitesini yükselterek alanında lider konuma yükselmiştir.
              </p>
            </div>

            {/* CENTER VIDEO & TITLE */}
            <div className="flex-[1.4] text-center w-full min-w-[280px]">
              <h2 className="font-great-vibes text-4xl sm:text-6xl text-[#1A1A1A] mb-6 font-normal">
                İrem Düğün Sarayı
              </h2>
              <div className="w-full rounded-2xl overflow-hidden shadow-2xl bg-black border border-[#C5B37D]/30 relative aspect-video">
                <iframe
                  className="w-full h-full"
                  src="https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=0&controls=1"
                  title="İrem Düğün Sarayı Tanıtım Filmi"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                ></iframe>
              </div>
            </div>

            {/* RIGHT TEXT */}
            <div className="flex-1 text-left text-sm leading-relaxed text-[#333333] space-y-4">
              <p>
                Hem mesleki tecrübe hem de profesyonel kadronun bir araya gelmesi bu başarının en önemli sebebi olarak tanımlanabilir.
              </p>
              <p>
                Kendini her geçen gün yenileyen ve düğün salonu sektöründe ilklerin adresi konumuna gelen <strong>İREM DÜĞÜN SARAYI</strong>, göl manzaralı kır bahçesi ve lüks balo salonları ile unutulmaz anılar vaat ediyor.
              </p>
            </div>

          </div>
        </div>
      </section>

      {/* SECTION 3: MASALSI DÜĞÜN MEKANLARI (DARK SECTION) */}
      <section className="bg-[#1A1A1A] text-white py-20 px-4 sm:px-8">
        <div className="max-w-7xl mx-auto space-y-12">
          
          <div className="text-center space-y-3">
            <h2 className="font-great-vibes text-4xl sm:text-6xl text-white font-normal">
              Masalsı Düğün Mekanları
            </h2>
            <p className="text-xs sm:text-sm text-white/60 tracking-wider uppercase">
              Sapanca Gölünün Eşsiz Atmosferinde Hayalinizdeki Davet
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                title: 'İrem Göl Kır Bahçesi',
                desc: 'Sapanca Gölünün yeşilliği içinde yer alan, hem açık hem kapalı alan seçenekleriyle 1500 kişilik kır düğünleri.',
                img: 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80',
                route: '/salonlar',
              },
              {
                title: 'İrem Gold Balo Salonu',
                desc: 'Yüksek tavanlı mimarisi, kristal avizeleri ve 1000 kişilik yemekli kapasitesiyle zarafetin suyla buluştuğu balo mekanı.',
                img: 'https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=800&q=80',
                route: '/salonlar',
              },
              {
                title: 'İrem Safir Davet Salonu',
                desc: 'Doğayla iç içe atmosferi ve modern iklimlendirme altyapısıyla 600 kişilik şık ve ferah organizasyon alanı.',
                img: 'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=800&q=80',
                route: '/salonlar',
              },
              {
                title: 'İrem Panorama Teras',
                desc: 'Göl manzarasına hakim teras alanı, özel kına tahtı ve 300 kişilik VIP davet salonu.',
                img: 'https://images.unsplash.com/photo-1469371670807-013ccf25f16a?auto=format&fit=crop&w=800&q=80',
                route: '/salonlar',
              },
            ].map((hall, idx) => (
              <div
                key={idx}
                onClick={() => handleNav(hall.route)}
                className="group relative overflow-hidden rounded-xl shadow-2xl cursor-pointer h-[500px] border border-white/10 hover:border-[#C5B37D] transition-all duration-500"
              >
                <img
                  src={hall.img}
                  alt={hall.title}
                  className="w-full h-full object-cover group-hover:scale-110 transition duration-700"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-[#1A1A1A] via-[#1A1A1A]/40 to-transparent p-6 flex flex-col justify-end transform transition-transform duration-300">
                  <h3 className="font-great-vibes text-3xl text-white mb-2 group-hover:text-[#C5B37D] transition">
                    {hall.title}
                  </h3>
                  <p className="text-xs text-white/80 line-clamp-3 leading-relaxed">
                    {hall.desc}
                  </p>
                </div>
              </div>
            ))}
          </div>

        </div>
      </section>

      {/* SECTION 4: HIZLI TEKLİF & İLETİŞİM FORMU */}
      <section className="py-20 px-4 sm:px-8 max-w-5xl mx-auto">
        <div className="bg-white rounded-2xl p-8 sm:p-12 border border-[#E6E1D8] shadow-xl space-y-8 text-center">
          
          <div className="space-y-2">
            <span className="text-[#C5B37D] font-bold text-xs uppercase tracking-[0.2em]">
              ÜCRETSİZ DANIŞMANLIK
            </span>
            <h2 className="font-serif text-3xl sm:text-4xl text-[#1A1A1A] font-bold">
              Tarihinizi ve Fiyat Teklifinizi Alın
            </h2>
            <p className="text-xs sm:text-sm text-[#666666] max-w-xl mx-auto">
              Tarihinizi ve tahmini davetli sayınızı iletin, düğün uzmanlarımız size en uygun paket teklifini sunsun.
            </p>
          </div>

          {formSubmitted ? (
            <div className="bg-[#F5F2ED] border border-[#C5B37D] p-8 rounded-xl text-center space-y-3">
              <div className="text-4xl">✨</div>
              <h4 className="text-xl font-serif text-[#1A1A1A] font-bold">Teklif Talebiniz Alındı!</h4>
              <p className="text-xs text-[#666666]">
                Müşteri temsilcimiz en kısa sürede vermiş olduğunuz telefon numarasından sizinle iletişime geçecektir.
              </p>
            </div>
          ) : (
            <form onSubmit={handleQuoteSubmit} className="space-y-4 max-w-3xl mx-auto text-left">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-[#1A1A1A] mb-1">
                    Adınız ve Soyadınız *
                  </label>
                  <input
                    type="text"
                    required
                    placeholder="Ad Soyad"
                    value={quoteForm.name}
                    onChange={(e) => setQuoteForm({ ...quoteForm, name: e.target.value })}
                    className="w-full bg-[#F5F2ED] border border-[#E6E1D8] focus:border-[#C5B37D] text-[#1A1A1A] text-xs px-4 py-3 rounded-lg outline-none transition"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-[#1A1A1A] mb-1">
                    Telefon Numarası *
                  </label>
                  <input
                    type="tel"
                    required
                    placeholder="05XX XXX XX XX"
                    value={quoteForm.phone}
                    onChange={(e) => setQuoteForm({ ...quoteForm, phone: e.target.value })}
                    className="w-full bg-[#F5F2ED] border border-[#E6E1D8] focus:border-[#C5B37D] text-[#1A1A1A] text-xs px-4 py-3 rounded-lg outline-none transition"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-[#1A1A1A] mb-1">
                    Düğün / Etkinlik Tarihi
                  </label>
                  <input
                    type="date"
                    value={quoteForm.eventDate}
                    onChange={(e) => setQuoteForm({ ...quoteForm, eventDate: e.target.value })}
                    className="w-full bg-[#F5F2ED] border border-[#E6E1D8] focus:border-[#C5B37D] text-[#1A1A1A] text-xs px-4 py-3 rounded-lg outline-none transition"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-[#1A1A1A] mb-1">
                    Tahmini Davetli Sayısı
                  </label>
                  <select
                    value={quoteForm.guestCount}
                    onChange={(e) => setQuoteForm({ ...quoteForm, guestCount: e.target.value })}
                    className="w-full bg-[#F5F2ED] border border-[#E6E1D8] focus:border-[#C5B37D] text-[#1A1A1A] text-xs px-4 py-3 rounded-lg outline-none transition"
                  >
                    <option value="100-250">100 - 250 Kişi</option>
                    <option value="250-500">250 - 500 Kişi</option>
                    <option value="500-1000">500 - 1000 Kişi</option>
                    <option value="1000+">1000+ Kişi (Göl Kır Bahçesi)</option>
                  </select>
                </div>
              </div>

              <div className="pt-2 text-center">
                <button
                  type="submit"
                  className="bg-[#1A1A1A] hover:bg-[#2c2c2c] text-[#F5F2ED] border border-[#C5B37D] font-bold text-xs px-10 py-4 rounded-full transition cursor-pointer tracking-widest uppercase shadow-lg"
                >
                  ÜCRETSİZ FİYAT TEKLİFİ GÖNDER
                </button>
              </div>
            </form>
          )}

        </div>
      </section>

    </div>
  );
}
