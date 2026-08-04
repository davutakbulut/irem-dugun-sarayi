import React, { useState } from 'react';

export default function VirtualTourPage({ navigateTo }) {
  const [activeTour, setActiveTour] = useState('kir-bahcesi');
  const [isTourLoaded, setIsTourLoaded] = useState(false);

  const tours = [
    {
      id: 'kir-bahcesi',
      name: 'Göl Manzaralı Kır Bahçesi',
      embedUrl: 'https://my.matterport.com/show/?m=sample1&play=1',
      cover: 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=1200&q=80',
    },
    {
      id: 'saray-salonu',
      name: 'Saray Balo Salonu',
      embedUrl: 'https://my.matterport.com/show/?m=sample2&play=1',
      cover: 'https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=1200&q=80',
    },
    {
      id: 'safir-salonu',
      name: 'Safir Balo Salonu',
      embedUrl: 'https://my.matterport.com/show/?m=sample3&play=1',
      cover: 'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=1200&q=80',
    },
  ];

  const currentTourData = tours.find((t) => t.id === activeTour);

  return (
    <div className="max-w-7xl mx-auto px-6 sm:px-12 py-12 space-y-10">
      
      {/* HEADER */}
      <div className="text-center space-y-4 max-w-3xl mx-auto">
        <span className="bg-red-500/20 text-red-400 border border-red-500/40 text-xs font-extrabold px-3 py-1 rounded-full inline-flex items-center space-x-1.5">
          <span className="animate-pulse">🔴</span>
          <span>Matterport 3D İnteraktif Teknoloji</span>
        </span>
        <h1 className="text-4xl sm:text-5xl font-heading font-extrabold text-white">
          360° Sanal Tur & Panoramik Gezinti
        </h1>
        <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
          Tesisimizi adeta oradaymış gibi 3 boyutlu adımlarla inceleyin, masaları, sahneyi ve göl manzarasını istediğiniz açıdan gezinin.
        </p>
      </div>

      {/* TOUR SELECTOR TABS */}
      <div className="flex items-center justify-center space-x-3">
        {tours.map((t) => (
          <button
            key={t.id}
            onClick={() => {
              setActiveTour(t.id);
              setIsTourLoaded(false);
            }}
            className={`px-5 py-3 rounded-2xl font-bold text-xs transition cursor-pointer ${
              activeTour === t.id
                ? 'gold-button shadow-xl'
                : 'bg-slate-900 text-slate-300 border border-slate-800 hover:border-amber-500/50'
            }`}
          >
            {t.name}
          </button>
        ))}
      </div>

      {/* 3D VIEWER FRAME / ON-DEMAND CLICK LOAD */}
      <div className="bg-slate-900/90 rounded-3xl border-2 border-amber-500/30 overflow-hidden shadow-2xl relative min-h-[500px] flex items-center justify-center">
        
        {!isTourLoaded ? (
          <div className="relative w-full h-[550px] flex items-center justify-center overflow-hidden group">
            <img
              src={currentTourData.cover}
              alt={currentTourData.name}
              className="w-full h-full object-cover group-hover:scale-105 transition duration-700 opacity-60"
            />
            <div className="absolute inset-0 bg-slate-950/70" />

            <div className="relative z-10 text-center space-y-5 max-w-md px-6">
              <div className="w-20 h-20 rounded-full bg-gradient-to-br from-amber-500 to-amber-600 flex items-center justify-center text-3xl shadow-2xl mx-auto border-2 border-amber-300 animate-bounce">
                🌐
              </div>
              <div className="space-y-2">
                <h3 className="text-2xl font-heading font-extrabold text-white">
                  {currentTourData.name} 3D Turu
                </h3>
                <p className="text-xs text-slate-300">
                  3D dokuları ve görünümü canlı yüklemek için aşağıdaki butona tıklayın.
                </p>
              </div>

              <button
                onClick={() => setIsTourLoaded(true)}
                className="gold-button font-extrabold text-sm px-8 py-4 rounded-2xl shadow-2xl hover:scale-105 transition cursor-pointer w-full"
              >
                360° Sanal Tura Başla →
              </button>
            </div>
          </div>
        ) : (
          <div className="w-full h-[600px] relative bg-slate-950">
            {/* SIMULATED MATTERPORT PANORAMA VIEWER */}
            <iframe
              title={currentTourData.name}
              src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d12089.444390022204!2d30.27!3d40.69!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zNDDCsDQxJzI0LjAiTiAzMMKwMTYnMTIuMCJF!5e0!3m2!1str!2str!4v1620000000000!5m2!1str!2str"
              className="w-full h-full border-0"
              allowFullScreen
              loading="lazy"
            />
            <div className="absolute top-4 right-4 bg-slate-950/80 backdrop-blur-md px-4 py-2 rounded-xl border border-amber-500/40 text-xs font-bold text-amber-400">
              3D Canlı Mod Aktif • Fare İle Döndürün
            </div>
          </div>
        )}

      </div>

    </div>
  );
}
