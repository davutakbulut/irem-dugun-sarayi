import React, { useState } from 'react';

export default function VirtualTourPage() {
  const [activeTour, setActiveTour] = useState('kir-bahcesi');
  const [isTourLoaded, setIsTourLoaded] = useState(false);

  const tours = [
    {
      id: 'kir-bahcesi',
      name: 'İrem Göl Kır Bahçesi',
      cover: 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=1200&q=80',
    },
    {
      id: 'saray-salonu',
      name: 'İrem Gold Balo Salonu',
      cover: 'https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=1200&q=80',
    },
    {
      id: 'safir-salonu',
      name: 'İrem Safir Davet Salonu',
      cover: 'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=1200&q=80',
    },
  ];

  const currentTourData = tours.find((t) => t.id === activeTour);

  return (
    <div className="bg-[#F5F2ED] min-h-screen text-[#1A1A1A] py-16 px-4 sm:px-8 max-w-7xl mx-auto space-y-10">
      
      {/* HEADER */}
      <div className="text-center space-y-3 max-w-3xl mx-auto">
        <span className="text-[#C5B37D] font-bold text-xs uppercase tracking-[0.2em]">
          İNTERAKTİF MEKAN İNCELEMESİ
        </span>
        <h1 className="font-great-vibes text-5xl sm:text-6xl text-[#1A1A1A] font-normal">
          360° Sanal Tur & Panoramik Gezinti
        </h1>
        <p className="text-xs sm:text-sm text-[#666666] leading-relaxed">
          Tesisimizi adeta oradaymış gibi 3 boyutlu adımlarla inceleyin, masaları, sahneyi ve göl manzarasını istediğiniz açıdan gezinin.
        </p>
      </div>

      {/* TOUR SELECTOR TABS */}
      <div className="flex items-center justify-center space-x-3 overflow-x-auto pb-2">
        {tours.map((t) => (
          <button
            key={t.id}
            onClick={() => {
              setActiveTour(t.id);
              setIsTourLoaded(false);
            }}
            className={`px-6 py-3 rounded-full font-bold text-xs tracking-wider transition cursor-pointer shrink-0 uppercase ${
              activeTour === t.id
                ? 'bg-[#1A1A1A] text-[#F5F2ED] border border-[#C5B37D] shadow-lg'
                : 'bg-white text-[#1A1A1A] border border-[#E6E1D8] hover:border-[#C5B37D]'
            }`}
          >
            {t.name}
          </button>
        ))}
      </div>

      {/* 3D VIEWER FRAME */}
      <div className="bg-[#1A1A1A] rounded-2xl border border-[#C5B37D]/30 overflow-hidden shadow-2xl relative min-h-[500px] flex items-center justify-center">
        
        {!isTourLoaded ? (
          <div className="relative w-full h-[550px] flex items-center justify-center overflow-hidden group">
            <img
              src={currentTourData.cover}
              alt={currentTourData.name}
              className="w-full h-full object-cover group-hover:scale-105 transition duration-700 opacity-50"
            />
            <div className="absolute inset-0 bg-black/60" />

            <div className="relative z-10 text-center space-y-5 max-w-md px-6 text-white">
              <div className="w-16 h-16 rounded-full bg-[#C5B37D] text-black flex items-center justify-center text-2xl shadow-2xl mx-auto animate-bounce font-serif font-bold">
                360°
              </div>
              <div className="space-y-2">
                <h3 className="text-2xl font-serif font-bold text-white">
                  {currentTourData.name} 3D Turu
                </h3>
                <p className="text-xs text-white/70">
                  Canlı 3D deneyimi ve panoramik görünümü başlatmak için tıklayınız.
                </p>
              </div>

              <button
                onClick={() => setIsTourLoaded(true)}
                className="bg-[#C5B37D] hover:bg-[#b09e6a] text-black font-bold text-xs px-8 py-3.5 rounded-full transition cursor-pointer uppercase tracking-widest w-full shadow-lg"
              >
                SANAL TURU BAŞLAT
              </button>
            </div>
          </div>
        ) : (
          <div className="w-full h-[600px] relative bg-black">
            <iframe
              title={currentTourData.name}
              src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d12089.444390022204!2d30.27!3d40.69!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zNDDCsDQxJzI0LjAiTiAzMMKwMTYnMTIuMCJF!5e0!3m2!1str!2str!4v1620000000000!5m2!1str!2str"
              className="w-full h-full border-0"
              allowFullScreen
              loading="lazy"
            />
            <div className="absolute top-4 right-4 bg-black/80 backdrop-blur-md px-4 py-2 rounded-full border border-[#C5B37D] text-xs font-bold text-[#C5B37D] tracking-wider uppercase">
              3D Canlı Mod • Fare İle Döndürün
            </div>
          </div>
        )}

      </div>

    </div>
  );
}
