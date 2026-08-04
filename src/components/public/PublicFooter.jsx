import React from 'react';

export default function PublicFooter({ navigateTo }) {
  const handleNav = (route) => {
    if (navigateTo) navigateTo(route);
    else window.location.href = route;
  };

  return (
    <footer className="bg-slate-950 text-slate-300 font-sans border-t border-amber-500/20 relative overflow-hidden">
      {/* GLOW DECORATIONS */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-amber-500/5 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-orange-500/5 rounded-full blur-3xl pointer-events-none" />

      {/* TOP NEWSLETTER BAR */}
      <div className="border-b border-slate-800/80 py-10 px-6 sm:px-12 max-w-7xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
          <div className="space-y-2">
            <span className="text-amber-400 font-bold text-xs uppercase tracking-widest flex items-center space-x-1.5">
              <span>👑</span>
              <span>Düğün & Organizasyon İpuçları</span>
            </span>
            <h3 className="text-2xl sm:text-3xl font-heading font-extrabold text-white">
              Özel Fırsat ve Trend Rehberimizden Haberdar Olun
            </h3>
            <p className="text-xs text-slate-400">
              Yeni sezon kampanya indirimleri ve düğün hazırlık takvimini e-posta adresinize gönderelim.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-3">
            <input
              type="email"
              placeholder="E-posta adresinizi giriniz..."
              className="bg-slate-900 border border-slate-700 focus:border-amber-500 text-white text-xs px-4 py-3.5 rounded-xl flex-1 outline-none transition"
            />
            <button
              onClick={() => alert('Bülten kaydınız başarıyla alındı!')}
              className="gold-button font-extrabold text-xs px-6 py-3.5 rounded-xl shadow-lg shrink-0 cursor-pointer"
            >
              Abone Ol →
            </button>
          </div>
        </div>
      </div>

      {/* MAIN FOOTER LINKS GRID */}
      <div className="max-w-7xl mx-auto px-6 sm:px-12 py-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-10">
        
        {/* COL 1: BRAND & ABOUT */}
        <div className="lg:col-span-2 space-y-5">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-amber-500 to-amber-600 flex items-center justify-center text-white text-2xl shadow-lg border border-amber-400/40 shrink-0">
              🏰
            </div>
            <div>
              <h2 className="font-heading font-extrabold text-xl text-white gold-gradient-text">
                İREM DÜĞÜN SARAYI
              </h2>
              <p className="text-xs font-bold text-amber-400">Balo & Organizasyon Tesisleri</p>
            </div>
          </div>

          <p className="text-xs text-slate-400 leading-relaxed max-w-md">
            Sapanca Göl kenarında, doğanın kalbinde 4 farklı konsept balo salonu, açık hava kır bahçesi ve VIP hizmet anlayışıyla unutulmaz davetler tasarlıyoruz.
          </p>

          <div className="flex items-center space-x-3 pt-2">
            {['facebook', 'instagram', 'youtube', 'whatsapp'].map((social) => (
              <a
                key={social}
                href="#"
                onClick={(e) => { e.preventDefault(); alert(`İrem Düğün Sarayı ${social.toUpperCase()} sayfasına yönlendiriliyorsunuz.`); }}
                className="w-9 h-9 rounded-xl bg-slate-900 border border-slate-800 hover:border-amber-500 text-slate-300 hover:text-amber-400 flex items-center justify-center transition"
              >
                {social === 'facebook' && '📘'}
                {social === 'instagram' && '📸'}
                {social === 'youtube' && '🎬'}
                {social === 'whatsapp' && '💬'}
              </a>
            ))}
          </div>
        </div>

        {/* COL 2: HIZLI MENÜ */}
        <div className="space-y-4">
          <h4 className="font-heading font-extrabold text-sm text-white uppercase tracking-wider border-b border-amber-500/30 pb-2">
            Hızlı Gezinti
          </h4>
          <ul className="space-y-2.5 text-xs font-medium">
            {[
              { label: 'Anasayfa', route: '/' },
              { label: 'Salonlarımız', route: '/salonlar' },
              { label: '360° Sanal Tur', route: '/360-tur' },
              { label: 'Organizasyonlar', route: '/organizasyonlar' },
              { label: 'Videolar & Galeri', route: '/videolar' },
              { label: 'Düğün Rehberi Blog', route: '/blog' },
            ].map((item) => (
              <li key={item.route}>
                <button
                  onClick={() => handleNav(item.route)}
                  className="hover:text-amber-400 transition flex items-center space-x-1.5 text-left"
                >
                  <span className="text-amber-500 text-[10px]">▸</span>
                  <span>{item.label}</span>
                </button>
              </li>
            ))}
          </ul>
        </div>

        {/* COL 3: SALONLARIMIZ */}
        <div className="space-y-4">
          <h4 className="font-heading font-extrabold text-sm text-white uppercase tracking-wider border-b border-amber-500/30 pb-2">
            Balo Salonları
          </h4>
          <ul className="space-y-2.5 text-xs font-medium">
            {[
              'Göl Manzaralı Kır Bahçesi (1500 Kişi)',
              'Saray Balo Salonu (1000 Kişi)',
              'Safir Balo Salonu (600 Kişi)',
              'VIP Lounge & Kına Salonu',
              'Gelin Hazırlık Süiti',
              'Özel Otopark & Vale Hizmeti',
            ].map((name) => (
              <li key={name} className="flex items-center space-x-1.5">
                <span className="text-amber-500 text-[10px]">✨</span>
                <span>{name}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* COL 4: İLETİŞİM & KONUM */}
        <div className="space-y-4">
          <h4 className="font-heading font-extrabold text-sm text-white uppercase tracking-wider border-b border-amber-500/30 pb-2">
            İletişim & Konum
          </h4>
          <div className="space-y-3 text-xs">
            <div className="flex items-start space-x-2.5">
              <span className="text-amber-400 text-sm">📍</span>
              <span className="text-slate-300">
                Sapanca Göl Caddesi No:42, Sakarya / Türkiye
              </span>
            </div>

            <div className="flex items-center space-x-2.5">
              <span className="text-amber-400 text-sm">📞</span>
              <a href="tel:+902645820000" className="hover:text-amber-400 font-bold transition">
                +90 (264) 582 00 00
              </a>
            </div>

            <div className="flex items-center space-x-2.5">
              <span className="text-amber-400 text-sm">💬</span>
              <a href="https://wa.me/905320000000" target="_blank" rel="noreferrer" className="text-emerald-400 font-bold hover:underline">
                WhatsApp Canlı Destek
              </a>
            </div>

            <div className="flex items-center space-x-2.5">
              <span className="text-amber-400 text-sm">✉️</span>
              <a href="mailto:info@iremdugunsarayi.com" className="hover:text-amber-400 transition">
                info@iremdugunsarayi.com
              </a>
            </div>
          </div>
        </div>

      </div>

      {/* BOTTOM COPYRIGHT & PORTAL ENTRANCE */}
      <div className="border-t border-slate-900 bg-slate-950 py-6 px-6 sm:px-12 text-xs text-slate-500 flex flex-col sm:flex-row justify-between items-center gap-4 max-w-7xl mx-auto">
        <div>
          © 2026 İrem Düğün Sarayı & Balo Tesisleri. Tüm Hakları Saklıdır.
        </div>

        <div className="flex items-center space-x-4">
          <button onClick={() => handleNav('/musteri-giris')} className="hover:text-amber-400 transition">
            Müşteri VIP Portalı
          </button>
          <span>•</span>
          <button onClick={() => handleNav('/yonetim')} className="hover:text-amber-400 transition">
            Yönetim Girişi
          </button>
        </div>
      </div>
    </footer>
  );
}
