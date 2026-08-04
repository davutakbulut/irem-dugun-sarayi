import React, { useState } from 'react';

export default function HallsPage({ navigateTo }) {
  const [selectedCategory, setSelectedCategory] = useState('all');

  const halls = [
    {
      id: 'kir-bahcesi',
      name: 'Göl Manzaralı Kır Bahçesi',
      category: 'outdoor',
      capacity: '1.500 Kişi',
      area: '3.500 m²',
      type: 'Açık Hava & Kır Düğünü',
      img: 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80',
      features: ['Sapanca Göl Manzarası', 'Doğal Çim Zemin', 'Özel Gelin Çıkış Yolu', 'Canlı Müzik Sahnesi', 'Açık Bar & Kokteyl Alanı'],
      description: 'Doğanın büyüleyici atmosferinde, göl esintisi eşliğinde 1.500 kişiye kadar yüksek kapasiteli lüks kır düğünleri.',
    },
    {
      id: 'saray-salonu',
      name: 'Saray Balo Salonu',
      category: 'indoor',
      capacity: '1.000 Kişi',
      area: '2.200 m²',
      type: 'Kolonsuz Luxury Balo Salonu',
      img: 'https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=800&q=80',
      features: ['8 Metre Yüksek Tavan', 'Swarovski Avizeler', 'İklimlendirme & Havalandırma', 'Dev LED Ekran Sahne', 'Özel VİP Gelin Odası'],
      description: 'Görkemli ve şık tasarımıyla yüksek katılımlı düğün ve kurumsal galalar için mükemmel havalandırma altyapısı.',
    },
    {
      id: 'safir-salonu',
      name: 'Safir Balo Salonu',
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
      name: 'VIP Lounge & Kına Salonu',
      category: 'vip',
      capacity: '300 Kişi',
      area: '800 m²',
      type: 'Geleneksel & Modern Kına Konsepti',
      img: 'https://images.unsplash.com/photo-1469371670807-013ccf25f16a?auto=format&fit=crop&w=800&q=80',
      features: ['Kına Tahtı & Nedime Alanı', 'Özel Işık Topları', 'VIP Lounge Oturma Düzeni', 'Fotoğraf Çekim Köşesi', 'Özel İkram Büfesi'],
      description: 'Kına geceleri, nişan ve özel aile davetleri için tasarlanmış otantik ve büyüleyici organizasyon salonu.',
    },
  ];

  const filteredHalls = selectedCategory === 'all'
    ? halls
    : halls.filter((h) => h.category === selectedCategory);

  return (
    <div className="max-w-7xl mx-auto px-6 sm:px-12 py-12 space-y-12">
      
      {/* PAGE HEADER */}
      <div className="text-center space-y-4 max-w-3xl mx-auto">
        <span className="text-amber-500 font-extrabold text-xs uppercase tracking-widest">
          🏛️ Balo & Davet Alanlarımız
        </span>
        <h1 className="text-4xl sm:text-5xl font-heading font-extrabold text-white">
          Balo Salonlarımız & Kır Bahçemiz
        </h1>
        <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
          Göl manzaralı kır bahçesinden kolonsuz saray mimarisine kadar her ölçekteki davetiniz için kusursuz alanlar sunuyoruz.
        </p>
      </div>

      {/* FILTER BUTTONS */}
      <div className="flex items-center justify-center space-x-2 overflow-x-auto pb-2">
        {[
          { id: 'all', label: 'Tüm Alanlar' },
          { id: 'outdoor', label: 'Açık Hava & Kır Bahçesi' },
          { id: 'indoor', label: 'Kapalı Balo Salonları' },
          { id: 'vip', label: 'VIP & Kına Salonu' },
        ].map((btn) => (
          <button
            key={btn.id}
            onClick={() => setSelectedCategory(btn.id)}
            className={`px-5 py-2.5 rounded-xl font-bold text-xs transition cursor-pointer shrink-0 ${
              selectedCategory === btn.id
                ? 'gold-button shadow-lg'
                : 'bg-slate-900 text-slate-300 border border-slate-800 hover:border-amber-500/50'
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
            className="bg-slate-900/90 rounded-3xl border border-slate-800 hover:border-amber-500/50 overflow-hidden shadow-2xl transition duration-300 flex flex-col justify-between"
          >
            <div className="relative h-64 overflow-hidden">
              <img
                src={hall.img}
                alt={hall.name}
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent to-transparent" />
              <span className="absolute top-4 right-4 bg-amber-500 text-slate-950 font-black text-xs px-3 py-1 rounded-full shadow">
                {hall.capacity}
              </span>
            </div>

            <div className="p-8 space-y-6 flex-1 flex flex-col justify-between">
              <div className="space-y-3">
                <div className="flex justify-between items-center text-xs text-amber-400 font-bold">
                  <span>{hall.type}</span>
                  <span>{hall.area}</span>
                </div>
                <h3 className="font-heading font-extrabold text-2xl text-white">
                  {hall.name}
                </h3>
                <p className="text-xs text-slate-300 leading-relaxed">
                  {hall.description}
                </p>

                <div className="pt-2 space-y-1.5">
                  <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                    Öne Çıkan Özellikler:
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {hall.features.map((feat, i) => (
                      <span key={i} className="bg-slate-950 border border-slate-800 text-amber-300 text-[10px] font-bold px-2.5 py-1 rounded-lg">
                        ✓ {feat}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              <div className="pt-4 border-t border-slate-800 flex items-center justify-between gap-4">
                <button
                  onClick={() => navigateTo && navigateTo('/360-tur')}
                  className="bg-slate-950 border border-amber-500/30 text-amber-400 font-bold text-xs px-4 py-2.5 rounded-xl hover:bg-slate-800 transition"
                >
                  360° Sanal Tur 🌐
                </button>

                <button
                  onClick={() => navigateTo && navigateTo('/iletisim')}
                  className="gold-button font-extrabold text-xs px-5 py-2.5 rounded-xl shadow"
                >
                  Fiyat Al →
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}
