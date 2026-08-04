import React from 'react';

export default function OrganizationsPage({ navigateTo }) {
  const handleNav = (route) => {
    if (navigateTo) navigateTo(route);
    else window.location.href = route;
  };

  const orgs = [
    {
      id: 'dugun',
      title: 'Lüks Düğün & Balo Organizasyonları',
      subtitle: 'Hayallerinizin Ötesinde Bir Başlangıç',
      img: 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80',
      features: ['Yemekli & Kokteyl Menü Seçenekleri', 'Gelin & Damat VIP Hazırlık Süiti', 'Orkestra & Ses/Işık Düzeni', 'Düğün Pastası & Şampanya Şovu', 'Anı Defteri & Karşılama Kokteyli'],
      desc: 'Sapanca Göl kenarında rüya gibi bir düğün. Uzman organizasyon kadromuz ve kişiselleştirilebilir menü konseptlerimizle mükemmellik.',
    },
    {
      id: 'kina',
      title: 'Geleneksel & Modern Kına Gecesi',
      subtitle: 'Otantik Konsept ve Nedime Şovları',
      img: 'https://images.unsplash.com/photo-1469371670807-013ccf25f16a?auto=format&fit=crop&w=800&q=80',
      features: ['Kına Tahtı & Şark Köşesi', 'Profesyonel Nedime Dans Ekibi', 'Kına Yakma Seremonisi & Testi Kırma', 'Zenne / Oryantal Performansı', 'Lokum & Şerbet İkram Büfesi'],
      desc: 'Geleneklerimizi modern detaylarla harmanlayan, unutulmaz ve eğlence dolu kına organizasyonları.',
    },
    {
      id: 'nisan',
      title: 'Söz & Nişan Davetleri',
      subtitle: 'Zarif ve Şık Aile Kutlamaları',
      img: 'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=800&q=80',
      features: ['Özel Nişan Masası Tasarımı', 'Yüzük Tepsisi & Makas Masası', 'Butik İkram & Tatlı Tepsileri', 'Canlı Müzik Duo / Trio Enstrümantal', 'Özel Fotoğraf Çekim Alanı'],
      desc: 'Evliliğe atılan ilk adımda ailelerinizin ve sevdiklerinizin ağırlanacağı şık ve elit nişan törenleri.',
    },
    {
      id: 'kurumsal',
      title: 'Kurumsal Gala & Lansman Etkinlikleri',
      subtitle: 'Prestijli Şirket Toplantıları',
      img: 'https://images.unsplash.com/photo-1511578314322-379afb476865?auto=format&fit=crop&w=800&q=80',
      features: ['Yüksek Çözünürlüklü LED Ekranlar', 'Simültane Çeviri Kabinleri', 'Kürsü & Telsiz Mikrofon Sistemleri', 'Gala Yemeği & Networking Barı', 'Geniş Otopark & Vale Hizmeti'],
      desc: 'Şirket yıllık toplantıları, ürün lansmanları ve ödül törenleri için yüksek teknolojili kurumsal davet ortamı.',
    },
  ];

  return (
    <div className="bg-[#F5F2ED] min-h-screen text-[#1A1A1A] py-16 px-4 sm:px-8 max-w-7xl mx-auto space-y-12">
      
      {/* HEADER */}
      <div className="text-center space-y-3 max-w-3xl mx-auto">
        <span className="text-[#C5B37D] font-bold text-xs uppercase tracking-[0.2em]">
          ORGANİZASYON KONSEPTLERİMİZ
        </span>
        <h1 className="font-great-vibes text-5xl sm:text-6xl text-[#1A1A1A] font-normal">
          Her Konsept İçin Özel Tasarlanmış Davetler
        </h1>
        <p className="text-xs sm:text-sm text-[#666666] leading-relaxed">
          Düğünden kınaya, kurumsal galalardan nişan törenlerine kadar her detay profesyonel ekibimiz tarafından kusursuz planlanır.
        </p>
      </div>

      {/* ORGANIZATIONS LIST */}
      <div className="space-y-12">
        {orgs.map((org, index) => (
          <div
            key={org.id}
            className={`bg-white rounded-2xl border border-[#E6E1D8] p-8 sm:p-12 shadow-xl flex flex-col lg:flex-row items-center gap-10 ${
              index % 2 === 1 ? 'lg:flex-row-reverse' : ''
            }`}
          >
            <div className="w-full lg:w-1/2 h-80 rounded-xl overflow-hidden shadow-lg relative group">
              <img
                src={org.img}
                alt={org.title}
                className="w-full h-full object-cover group-hover:scale-105 transition duration-700"
              />
            </div>

            <div className="w-full lg:w-1/2 space-y-6">
              <div className="space-y-2">
                <span className="text-xs font-bold text-[#C5B37D] uppercase tracking-widest">
                  {org.subtitle}
                </span>
                <h3 className="font-serif font-bold text-2xl sm:text-3xl text-[#1A1A1A]">
                  {org.title}
                </h3>
                <p className="text-xs sm:text-sm text-[#666666] leading-relaxed">
                  {org.desc}
                </p>
              </div>

              <div className="space-y-2">
                <div className="text-xs font-bold text-[#1A1A1A] uppercase tracking-wider">
                  Paket İçeriğine Dahil Hizmetler:
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {org.features.map((f, i) => (
                    <div key={i} className="flex items-center space-x-2 text-xs text-[#333333]">
                      <span className="text-[#C5B37D] font-bold">•</span>
                      <span>{f}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="pt-2">
                <button
                  onClick={() => handleNav('/iletisim')}
                  className="bg-[#1A1A1A] hover:bg-[#2c2c2c] text-[#F5F2ED] border border-[#C5B37D] font-bold text-xs px-8 py-3.5 rounded-full transition cursor-pointer tracking-widest uppercase shadow-md"
                >
                  FİYAT TEKLİFİ AL
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}
