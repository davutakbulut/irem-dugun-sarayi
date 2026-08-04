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
      title: 'Zeynep & Burak Çiftinin Masalsı Kır Düğünü Klipi',
      category: 'Düğün Hikayesi',
      duration: '04:20',
      embedUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
      poster: 'https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=800&q=80',
    },
    {
      title: 'Görkemli Saray Balo Salonu Işık & Sahne Şovu',
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
    <div className="max-w-7xl mx-auto px-6 sm:px-12 py-12 space-y-12">
      
      {/* HEADER */}
      <div className="text-center space-y-4 max-w-3xl mx-auto">
        <span className="text-amber-500 font-extrabold text-xs uppercase tracking-widest">
          🎬 Medya Galeri & Drone Klipleri
        </span>
        <h1 className="text-4xl sm:text-5xl font-heading font-extrabold text-white">
          4K Video & Fotoğraf Galerimiz
        </h1>
        <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
          Tesisimizde gerçekleşen gerçek organizasyon kliplerini ve drone çekimlerimizi yüksek kalitede izleyin.
        </p>
      </div>

      {/* TABS */}
      <div className="flex justify-center space-x-3">
        <button
          onClick={() => setActiveTab('videos')}
          className={`px-6 py-3 rounded-2xl font-bold text-xs transition cursor-pointer ${
            activeTab === 'videos' ? 'gold-button shadow-xl' : 'bg-slate-900 text-slate-300 border border-slate-800'
          }`}
        >
          🎬 4K Video Klipler
        </button>

        <button
          onClick={() => setActiveTab('photos')}
          className={`px-6 py-3 rounded-2xl font-bold text-xs transition cursor-pointer ${
            activeTab === 'photos' ? 'gold-button shadow-xl' : 'bg-slate-900 text-slate-300 border border-slate-800'
          }`}
        >
          📸 Fotoğraf Galerisi
        </button>
      </div>

      {/* CONTENT */}
      {activeTab === 'videos' ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {videos.map((vid, i) => (
            <div key={i} className="bg-slate-900/90 rounded-3xl border border-slate-800 overflow-hidden shadow-2xl space-y-4 p-4">
              <div className="relative h-48 rounded-2xl overflow-hidden group">
                <img src={vid.poster} alt={vid.title} className="w-full h-full object-cover group-hover:scale-105 transition" />
                <div className="absolute inset-0 bg-slate-950/40 flex items-center justify-center">
                  <div className="w-14 h-14 rounded-full bg-amber-500 text-slate-950 flex items-center justify-center text-xl font-bold shadow-2xl group-hover:scale-110 transition">
                    ▶
                  </div>
                </div>
                <span className="absolute bottom-3 right-3 bg-slate-950/80 text-amber-400 text-[10px] font-bold px-2 py-0.5 rounded">
                  {vid.duration}
                </span>
              </div>
              <div className="space-y-1">
                <span className="text-[10px] font-bold text-amber-400 uppercase">{vid.category}</span>
                <h3 className="font-heading font-extrabold text-sm text-white">{vid.title}</h3>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {photos.map((src, i) => (
            <div key={i} className="h-64 rounded-2xl overflow-hidden border border-slate-800 group shadow-lg">
              <img src={src} alt={`İrem Düğün Sarayı Foto ${i+1}`} className="w-full h-full object-cover group-hover:scale-110 transition duration-500" />
            </div>
          ))}
        </div>
      )}

    </div>
  );
}
