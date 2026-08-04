import React, { useState } from 'react';

export default function HallsPage({ navigateTo }) {
  const [selectedCategory, setSelectedCategory] = useState('all');

  const handleNav = (route) => {
    if (navigateTo) navigateTo(route);
    else window.location.href = route;
  };

  const halls = [
    {
      id: 'kir-bahcesi',
      name: 'İrem Göl Kır Bahçesi',
      category: 'outdoor',
      capacity: '1.500 Kişi',
      area: '3.500 m²',
      type: 'Açık Hava & Göl Kır Düğünü',
      img: 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80',
      features: ['Sapanca Göl Manzarası', 'Doğal Çim Zemin', 'Özel Gelin Çıkış Yolu', 'Canlı Müzik Sahnesi', 'Açık Bar & Kokteyl Alanı'],
      description: 'Doğanın büyüleyici atmosferinde, göl esintisi eşliğinde 1.500 kişiye kadar yüksek kapasiteli lüks kır düğünleri.',
    },
    {
      id: 'saray-salonu',
      name: 'İrem Gold Balo Salonu',
      category: 'indoor',
      capacity: '1.000 Kişi',
      area: '2.200 m²',
      type: 'Kolonsuz Luxury Balo Salonu',
      img: 'https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=800&q=80',
      features: ['8 Metre Yüksek Tavan', 'Kristal Avizeler', 'İklimlendirme Altyapısı', 'Dev LED Ekran Sahne', 'Özel VIP Gelin Odası'],
      description: 'Görkemli ve şık tasarımıyla yüksek katılımlı düğün ve kurumsal galalar için mükemmel havalandırma altyapısı.',
    },
    {
      id: 'safir-salonu',
      name: 'İrem Safir Davet Salonu',
      category: 'indoor',
      capacity: '600 Kişi',
      area: '1.400 m²',
      type: 'Modern Butik Balo Salonu',
      img: 'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=800&q=80',
      features: ['Modern Akustik Ses Sistemi', 'Lazer Işık Şovları', 'Özel İkram Barı', 'Asansörlü VIP Giriş', 'Çocuk Oyun Alanı'],
      description: 'Sıcak ve samimi ortam arayan çiftler için özel olarak tasarlanmış modern mimarili balo salonu.',
    },
    {
      id: 'vip-lounge',
      name: 'İrem Panorama Teras & Lounge',
      category: 'vip',
      capacity: '300 Kişi',
      area: '800 m²',
      type: 'Geleneksel & Modern Kına Konsepti',
      img: 'https://images.unsplash.com/photo-1469371670807-013ccf25f16a?auto=format&fit=crop&w=800&q=80',
      features: ['Kına Tahtı & Nedime Alanı', 'VIP Lounge Oturma Düzeni', 'Fotoğraf Çekim Köşesi', 'Özel İkram Büfesi'],
      description: 'Kına geceleri, nişan ve özel aile davetleri için tasarlanmış otantik ve büyüleyici organizasyon salonu.',
    },
  ];

  const filteredHalls = selectedCategory === 'all'
    ? halls
    : halls.filter((h) => h.category === selectedCategory);

  return (
    <div className="bg-[#F5F2ED] min-h-screen text-[#1A1A1A] py-16 px-4 sm:px-8 max-w-7xl mx-auto space-y-12">
      
      {/* PAGE HEADER */}
      <div className="text-center space-y-3 max-w-3xl mx-auto">
        <span className="text-[#C5B37D] font-bold text-xs uppercase tracking-[0.2em]">
          DÜĞÜN MEKANLARIMIZ
        </span>
        <h1 className="font-great-vibes text-5xl sm:text-6xl text-[#1A1A1A] font-normal">
          Balo Salonlarımız & Kır Bahçemiz
        </h1>
        <p className="text-xs sm:text-sm text-[#666666] leading-relaxed">
          Göl manzaralı kır bahçesinden kolonsuz saray mimarisine kadar her ölçekteki davetiniz için kusursuz alanlar sunuyoruz.
        </p>
      </div>

      {/* FILTER BUTTONS */}
      <div className="flex items-center justify-center space-x-3 overflow-x-auto pb-2">
        {[
          { id: 'all', label: 'TÜM ALANLAR' },
          { id: 'outdoor', label: 'AÇIK HAVA & KIR BAHÇESİ' },
          { id: 'indoor', label: 'KAPALI BALO SALONLARI' },
          { id: 'vip', label: 'VIP & KINA SALONU' },
        ].map((btn) => (
          <button
            key={btn.id}
            onClick={() => setSelectedCategory(btn.id)}
            className={`px-6 py-3 rounded-full font-bold text-xs tracking-wider transition cursor-pointer shrink-0 uppercase ${
              selectedCategory === btn.id
                ? 'bg-[#1A1A1A] text-[#F5F2ED] border border-[#C5B37D] shadow-lg'
                : 'bg-white text-[#1A1A1A] border border-[#E6E1D8] hover:border-[#C5B37D]'
            }`}
          >
            {btn.label}
          </button>
        ))}
      </div>

      {/* HALLS GRID */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {filteredHalls.map((hall) => (
          <div
            key={hall.id}
            className="bg-white rounded-2xl border border-[#E6E1D8] shadow-lg overflow-hidden transition duration-300 flex flex-col justify-between"
          >
            <div className="relative h-64 overflow-hidden">
              <img
                src={hall.img}
                alt={hall.name}
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
              <span className="absolute top-4 right-4 bg-[#C5B37D] text-black font-bold text-xs px-4 py-1.5 rounded-full shadow tracking-wider uppercase">
                {hall.capacity}
              </span>
            </div>

            <div className="p-8 space-y-6 flex-1 flex flex-col justify-between">
              <div className="space-y-3">
                <div className="flex justify-between items-center text-xs text-[#C5B37D] font-bold tracking-wider uppercase">
                  <span>{hall.type}</span>
                  <span>{hall.area}</span>
                </div>
                <h3 className="font-serif font-bold text-2xl text-[#1A1A1A]">
                  {hall.name}
                </h3>
                <p className="text-xs text-[#666666] leading-relaxed">
                  {hall.description}
                </p>

                <div className="pt-2 space-y-2">
                  <div className="text-[11px] font-bold text-[#1A1A1A] uppercase tracking-wider">
                    Öne Çıkan Özellikler:
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {hall.features.map((feat, i) => (
                      <span key={i} className="bg-[#F5F2ED] border border-[#E6E1D8] text-[#1A1A1A] text-[10px] font-semibold px-3 py-1 rounded-full">
                        • {feat}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              <div className="pt-4 border-t border-[#E6E1D8] flex items-center justify-between gap-4">
                <button
                  onClick={() => handleNav('/360-tur')}
                  className="bg-[#F5F2ED] border border-[#E6E1D8] text-[#1A1A1A] font-bold text-xs px-5 py-2.5 rounded-full hover:border-[#C5B37D] transition uppercase tracking-wider"
                >
                  360° SANAL TUR
                </button>

                <button
                  onClick={() => handleNav('/iletisim')}
                  className="bg-[#1A1A1A] text-[#F5F2ED] border border-[#C5B37D] font-bold text-xs px-6 py-2.5 rounded-full shadow hover:bg-[#2c2c2c] transition uppercase tracking-wider"
                >
                  TEKLİF AL
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}
