import React, { useState } from 'react';

export default function VideosPage() {
  const [activeTab, setActiveTab] = useState('videos');

  const videos = [
    {
      title: 'İrem Düğün Sarayı 4K Drone Tanıtım Filmi',
      category: 'Drone Çekimi',
      duration: '03:45',
      embedUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
      poster: 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80',
    },
    {
      title: 'Masalsı Göl Kır Düğünü Hikayesi',
      category: 'Düğün Hikayesi',
      duration: '04:20',
      embedUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
      poster: 'https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=800&q=80',
    },
    {
      title: 'Görkemli Gold Balo Salonu Işık & Sahne Şovu',
      category: 'Işık & Sahne',
      duration: '02:15',
      embedUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
      poster: 'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=800&q=80',
    },
  ];

  const photos = [
    'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80',
    'https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=800&q=80',
    'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=800&q=80',
    'https://images.unsplash.com/photo-1469371670807-013ccf25f16a?auto=format&fit=crop&w=800&q=80',
    'https://images.unsplash.com/photo-1511578314322-379afb476865?auto=format&fit=crop&w=800&q=80',
    'https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?auto=format&fit=crop&w=800&q=80',
  ];

  return (
    <div className="bg-[#F5F2ED] min-h-screen text-[#1A1A1A] py-16 px-4 sm:px-8 max-w-7xl mx-auto space-y-12">
      
      {/* HEADER */}
      <div className="text-center space-y-3 max-w-3xl mx-auto">
        <span className="text-[#C5B37D] font-bold text-xs uppercase tracking-[0.2em]">
          MEDYA & GALERİ
        </span>
        <h1 className="font-great-vibes text-5xl sm:text-6xl text-[#1A1A1A] font-normal">
          4K Video & Fotoğraf Galerimiz
        </h1>
        <p className="text-xs sm:text-sm text-[#666666] leading-relaxed">
          Tesisimizde gerçekleşen gerçek organizasyon kliplerini ve drone çekimlerimizi yüksek kalitede izleyin.
        </p>
      </div>

      {/* TABS */}
      <div className="flex justify-center space-x-3">
        <button
          onClick={() => setActiveTab('videos')}
          className={`px-8 py-3 rounded-full font-bold text-xs tracking-wider transition cursor-pointer uppercase ${
            activeTab === 'videos'
              ? 'bg-[#1A1A1A] text-[#F5F2ED] border border-[#C5B37D] shadow-lg'
              : 'bg-white text-[#1A1A1A] border border-[#E6E1D8] hover:border-[#C5B37D]'
          }`}
        >
          4K VİDEO KLİPLER
        </button>

        <button
          onClick={() => setActiveTab('photos')}
          className={`px-8 py-3 rounded-full font-bold text-xs tracking-wider transition cursor-pointer uppercase ${
            activeTab === 'photos'
              ? 'bg-[#1A1A1A] text-[#F5F2ED] border border-[#C5B37D] shadow-lg'
              : 'bg-white text-[#1A1A1A] border border-[#E6E1D8] hover:border-[#C5B37D]'
          }`}
        >
          FOTOĞRAF GALERİSİ
        </button>
      </div>

      {/* CONTENT */}
      {activeTab === 'videos' ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {videos.map((vid, i) => (
            <div key={i} className="bg-white rounded-2xl border border-[#E6E1D8] overflow-hidden shadow-lg space-y-4 p-4">
              <div className="relative h-52 rounded-xl overflow-hidden group cursor-pointer">
                <img src={vid.poster} alt={vid.title} className="w-full h-full object-cover group-hover:scale-105 transition duration-500" />
                <div className="absolute inset-0 bg-black/40 flex items-center justify-center">
                  <div className="w-14 h-14 rounded-full bg-[#C5B37D] text-black flex items-center justify-center text-xl font-bold shadow-2xl group-hover:scale-110 transition">
                    ▶
                  </div>
                </div>
                <span className="absolute bottom-3 right-3 bg-black/80 text-[#C5B37D] text-[10px] font-bold px-2.5 py-1 rounded-full uppercase tracking-wider">
                  {vid.duration}
                </span>
              </div>
              <div className="space-y-1">
                <span className="text-[10px] font-bold text-[#C5B37D] uppercase tracking-widest">{vid.category}</span>
                <h3 className="font-serif font-bold text-base text-[#1A1A1A]">{vid.title}</h3>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
          {photos.map((src, i) => (
            <div key={i} className="h-64 rounded-xl overflow-hidden border border-[#E6E1D8] group shadow-md">
              <img src={src} alt={`İrem Düğün Sarayı Foto ${i+1}`} className="w-full h-full object-cover group-hover:scale-110 transition duration-700" />
            </div>
          ))}
        </div>
      )}

    </div>
  );
}
