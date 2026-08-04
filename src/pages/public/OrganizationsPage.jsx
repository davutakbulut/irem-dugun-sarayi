import React from 'react';

export default function OrganizationsPage({ navigateTo }) {
  const orgs = [
    {
      id: 'dugun',
      title: 'Lüks Düğün & Balo Organizasyonları',
      subtitle: 'Hayallerinizin Ötesinde Bir Başlangıç',
      icon: '👑',
      img: 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80',
      features: ['Yemekli & Kokteyl Menü Seçenekleri', 'Gelin & Damat VIP Hazırlık Süiti', 'Orkestra & Ses/Işık Düzeni', 'Düğün Pastası & Şampanya Şovu', 'Anı Defteri & Karşılama Kokteyli'],
      desc: 'Sapanca Göl kenarında rüya gibi bir düğün. Uzman organizasyon kadromuz ve kişiselleştirilebilir menü konseptlerimizle mükemmellik.',
    },
    {
      id: 'kina',
      title: 'Geleneksel & Modern Kına Gecesi',
      subtitle: 'Otantik Konsept ve Nedime Şovları',
      icon: '💃',
      img: 'https://images.unsplash.com/photo-1469371670807-013ccf25f16a?auto=format&fit=crop&w=800&q=80',
      features: ['Kına Tahtı & Şark Köşesi', 'Profesyonel Nedime Dans Ekibi', 'Kına Yakma Seremonisi & Testi Kırma', 'Zenne / Oryantal Performansı', 'Lokum & Serbet İkram Büfesi'],
      description: 'Geleneklerimizi modern detaylarla harmanlayan, unutulmaz ve eğlence dolu kına organizasyonları.',
    },
    {
      id: 'nisan',
      title: 'Söz & Nişan Davetleri',
      subtitle: 'Zarif ve Şık Aile Kutlamaları',
      icon: '💍',
      img: 'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=800&q=80',
      features: ['Özel Nişan Masası Tasarımı', 'Yüzük Tepsisi & Makas Masası', 'Butik İkram & Tatlı Tepsileri', 'Canlı Müzik Duo / Trio Enstrümantal', 'Özel Fotoğraf Çekim Alanı'],
      description: 'Evliliğe atılan ilk adımda ailelerinizin ve sevdiklerinizin ağırlanacağı şık ve elit nişan törenleri.',
    },
    {
      id: 'kurumsal',
      title: 'Kurumsal Gala & Lansman Etkinlikleri',
      subtitle: 'Prestijli Şirket Toplantıları',
      icon: '💼',
      img: 'https://images.unsplash.com/photo-1511578314322-379afb476865?auto=format&fit=crop&w=800&q=80',
      features: ['Yüksek Çözünürlüklü LED Ekranlar', 'Simültane Çeviri Kabinleri', 'Kürsü & Telsiz Mikrofon Sistemleri', 'Gala Yemeği & Networking Barı', 'Geniş Otopark & Vale Hizmeti'],
      description: 'Şirket yıllık toplantıları, ürün lansmanları ve ödül törenleri için yüksek teknolojili kurumsal davet ortamı.',
    },
  ];

  return (
    <div className="max-w-7xl mx-auto px-6 sm:px-12 py-12 space-y-12">
      
      {/* HEADER */}
      <div className="text-center space-y-4 max-w-3xl mx-auto">
        <span className="text-amber-500 font-extrabold text-xs uppercase tracking-widest">
          🎉 Etkinlik & Organizasyon Hizmetlerimiz
        </span>
        <h1 className="text-4xl sm:text-5xl font-heading font-extrabold text-white">
          Her Konsept İçin Özel Tasarlanmış Davetler
        </h1>
        <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
          Düğünden kınaya, kurumsal galalardan sünnet törenlerine kadar her detay profesyonel ekibimiz tarafından planlanır.
        </p>
      </div>

      {/* ORGANIZATIONS LIST */}
      <div className="space-y-12">
        {orgs.map((org, index) => (
          <div
            key={org.id}
            className={`bg-slate-900/90 rounded-3xl border border-slate-800 p-8 sm:p-12 shadow-2xl flex flex-col lg:flex-row items-center gap-10 ${
              index % 2 === 1 ? 'lg:flex-row-reverse' : ''
            }`}
          >
            <div className="w-full lg:w-1/2 h-80 rounded-2xl overflow-hidden shadow-xl relative group">
              <img
                src={org.img}
                alt={org.title}
                className="w-full h-full object-cover group-hover:scale-105 transition duration-500"
              />
              <div className="absolute top-4 left-4 bg-slate-950/80 backdrop-blur-md px-3.5 py-1.5 rounded-full text-lg shadow border border-amber-500/30">
                {org.icon}
              </div>
            </div>

            <div className="w-full lg:w-1/2 space-y-6">
              <div className="space-y-2">
                <span className="text-xs font-bold text-amber-400 uppercase tracking-widest">
                  {org.subtitle}
                </span>
                <h3 className="text-2xl sm:text-3xl font-heading font-extrabold text-white">
                  {org.title}
                </h3>
                <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                  {org.desc || org.description}
                </p>
              </div>

              <div className="space-y-2">
                <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                  Paket İçeriğine Dahil Hizmetler:
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {org.features.map((f, i) => (
                    <div key={i} className="flex items-center space-x-2 text-xs text-slate-200">
                      <span className="text-amber-500 font-bold">✓</span>
                      <span>{f}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="pt-4 flex items-center space-x-4">
                <button
                  onClick={() => navigateTo && navigateTo('/iletisim')}
                  className="gold-button font-extrabold text-xs px-6 py-3 rounded-xl shadow-lg"
                >
                  Paket Detayları & Fiyat Al →
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}
