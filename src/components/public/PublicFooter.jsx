import React from 'react';

export default function PublicFooter({ navigateTo }) {
  const handleNav = (route) => {
    if (navigateTo) navigateTo(route);
    else window.location.href = route;
  };

  return (
    <footer className="bg-[#1A1A1A] text-white font-sans border-t border-[#C5B37D]/30 relative overflow-hidden">
      {/* TOP NEWSLETTER BAR */}
      <div className="border-b border-white/10 py-12 px-6 sm:px-12 max-w-7xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
          <div className="space-y-2">
            <span className="text-[#C5B37D] font-semibold text-xs uppercase tracking-[0.2em] block">
              DÜĞÜN & ORGANİZASYON İPUÇLARI
            </span>
            <h3 className="text-2xl sm:text-3xl font-serif font-normal text-white">
              Özel Fırsat ve Trend Rehberimizden Haberdar Olun
            </h3>
            <p className="text-xs text-white/60">
              Yeni sezon kampanya indirimleri ve düğün hazırlık rehberini e-posta adresinize gönderelim.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-3">
            <input
              type="email"
              placeholder="E-posta adresinizi giriniz..."
              className="bg-white/5 border border-white/20 focus:border-[#C5B37D] text-white text-xs px-4 py-3.5 rounded-full flex-1 outline-none transition"
            />
            <button
              onClick={() => alert('Bülten kaydınız başarıyla alındı!')}
              className="bg-[#C5B37D] hover:bg-[#b09e6a] text-black font-bold text-xs px-8 py-3.5 rounded-full transition cursor-pointer uppercase tracking-widest shrink-0"
            >
              ABONE OL
            </button>
          </div>
        </div>
      </div>

      {/* MAIN FOOTER LINKS GRID */}
      <div className="max-w-7xl mx-auto px-6 sm:px-12 py-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12">
        
        {/* COL 1: BRAND & ABOUT */}
        <div className="space-y-5">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-full border border-[#C5B37D] bg-black/40 flex items-center justify-center text-[#C5B37D] font-serif text-xl shrink-0">
              👑
            </div>
            <div>
              <h2 className="font-serif tracking-widest text-lg font-bold text-white uppercase">
                İREM DÜĞÜN SARAYI
              </h2>
              <p className="text-[10px] font-medium text-[#C5B37D] tracking-widest uppercase">
                Balo & Organizasyon Tesisleri
              </p>
            </div>
          </div>

          <p className="text-xs text-white/70 leading-relaxed">
            Sapanca Göl kenarında, doğanın kalbinde 4 farklı konsept balo salonu, açık hava kır bahçesi ve VIP hizmet anlayışıyla hayalinizdeki organizasyonları gerçeğe dönüştürüyoruz.
          </p>

          <div className="flex items-center space-x-3 pt-2">
            {['Instagram', 'Facebook', 'WhatsApp'].map((social) => (
              <a
                key={social}
                href="#"
                onClick={(e) => { e.preventDefault(); alert(`İrem Düğün Sarayı ${social} sayfasına yönlendiriliyorsunuz.`); }}
                className="px-3 py-1.5 rounded-full bg-white/5 border border-white/10 hover:border-[#C5B37D] text-[11px] text-white/80 hover:text-[#C5B37D] transition"
              >
                {social}
              </a>
            ))}
          </div>
        </div>

        {/* COL 2: HIZLI MENÜ */}
        <div className="space-y-4">
          <h4 className="font-serif text-sm text-[#C5B37D] uppercase tracking-widest border-b border-white/10 pb-2">
            Hızlı Gezinti
          </h4>
          <ul className="space-y-2 text-xs font-medium text-white/80">
            {[
              { label: 'ANA SAYFA', route: '/' },
              { label: 'FİRMA PROFİLİ', route: '/hakkimizda' },
              { label: 'DÜĞÜN MEKANLARIMIZ', route: '/salonlar' },
              { label: 'ORGANİZASYONLARIMIZ', route: '/organizasyonlar' },
              { label: '360° SANAL TUR', route: '/360-tur' },
              { label: 'VİDEOLAR', route: '/videolar' },
              { label: 'BLOG', route: '/blog' },
              { label: 'İLETİŞİM', route: '/iletisim' },
            ].map((item) => (
              <li key={item.route}>
                <button
                  onClick={() => handleNav(item.route)}
                  className="hover:text-[#C5B37D] transition text-left"
                >
                  {item.label}
                </button>
              </li>
            ))}
          </ul>
        </div>

        {/* COL 3: SALONLARIMIZ */}
        <div className="space-y-4">
          <h4 className="font-serif text-sm text-[#C5B37D] uppercase tracking-widest border-b border-white/10 pb-2">
            Düğün Mekanlarımız
          </h4>
          <ul className="space-y-2.5 text-xs text-white/80">
            {[
              'İrem Göl Kır Bahçesi (1500 Kişi)',
              'İrem Gold Balo Salonu (1000 Kişi)',
              'İrem Safir Davet Salonu (600 Kişi)',
              'İrem Panorama Teras & Lounge',
              'Gelin Hazırlık Süiti & VIP Salon',
              'Özel Otopark & Vale Hizmeti',
            ].map((name) => (
              <li key={name} className="flex items-center space-x-2">
                <span className="text-[#C5B37D]">•</span>
                <span>{name}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* COL 4: İLETİŞİM & KONUM */}
        <div className="space-y-4">
          <h4 className="font-serif text-sm text-[#C5B37D] uppercase tracking-widest border-b border-white/10 pb-2">
            İletişim & Konum
          </h4>
          <div className="space-y-3 text-xs text-white/80">
            <div>
              <p className="font-semibold text-white">Adres:</p>
              <p className="text-white/70">Sapanca Göl Caddesi No:10, Sakarya / Türkiye</p>
            </div>

            <div>
              <p className="font-semibold text-white">Telefon:</p>
              <a href="tel:+905321112233" className="hover:text-[#C5B37D] font-bold text-white transition">
                +90 532 111 2233
              </a>
            </div>

            <div>
              <p className="font-semibold text-white">E-Posta:</p>
              <a href="mailto:info@iremdugunsarayi.com" className="hover:text-[#C5B37D] transition">
                info@iremdugunsarayi.com
              </a>
            </div>
          </div>
        </div>

      </div>

      {/* BOTTOM COPYRIGHT */}
      <div className="border-t border-white/10 bg-[#121212] py-6 px-6 sm:px-12 text-xs text-white/50 text-center max-w-7xl mx-auto">
        © 2026 İrem Düğün Sarayı & Balo Tesisleri. Tüm Hakları Saklıdır.
      </div>
    </footer>
  );
}
