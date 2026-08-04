import React from 'react';

export default function AboutUsPage() {
  return (
    <div className="bg-[#F5F2ED] min-h-screen text-[#1A1A1A] py-16 px-4 sm:px-8 max-w-7xl mx-auto space-y-16">
      
      {/* HEADER */}
      <div className="text-center space-y-3 max-w-3xl mx-auto">
        <span className="text-[#C5B37D] font-bold text-xs uppercase tracking-[0.2em]">
          FİRMA PROFİLİ & HİKAYEMİZ
        </span>
        <h1 className="font-great-vibes text-5xl sm:text-6xl text-[#1A1A1A] font-normal">
          İrem Düğün Sarayı & Balo Tesisleri
        </h1>
        <p className="text-xs sm:text-sm text-[#666666] leading-relaxed">
          15 yılı aşkın tecrübemizle, Sapanca Göl kenarında binlerce çiftin en mutlu gününe şahitlik ediyoruz.
        </p>
      </div>

      {/* STORY & MISSION */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
        <div className="space-y-6 text-[#333333] text-xs sm:text-sm leading-relaxed">
          <h2 className="font-serif font-bold text-3xl text-[#1A1A1A]">
            Doğanın Kalbinde Lüks ve İhtişam
          </h2>
          <p>
            Sektöründe lider olma hedefi ile hiçbir fedakârlıktan kaçınılmadan sarf edilen gayretler karşılıksız kalmamış ve herkesin takdirini toplamayı başaran bir mekâna dönüşmüştür.
          </p>
          <p>
            İrem Düğün Sarayı, Sapanca Gölünün eşsiz manzarasına karşı kurulmuş 3.500 m² açık kır bahçesi ve 3 farklı kapalı balo salonuyla bölgenin en prestijli organizasyon kompleksidir.
          </p>

          <div className="pt-4 grid grid-cols-2 gap-4">
            <div className="bg-white border border-[#E6E1D8] p-5 rounded-xl text-center shadow-md">
              <div className="text-2xl font-serif font-bold text-[#1A1A1A]">15+ Yıl</div>
              <div className="text-[11px] text-[#666666] uppercase tracking-wider font-semibold">Sektörel Deneyim</div>
            </div>
            <div className="bg-white border border-[#E6E1D8] p-5 rounded-xl text-center shadow-md">
              <div className="text-2xl font-serif font-bold text-[#1A1A1A]">ISO 22000</div>
              <div className="text-[11px] text-[#666666] uppercase tracking-wider font-semibold">Gıda Güvenliği Belgeli</div>
            </div>
          </div>
        </div>

        <div className="h-96 rounded-2xl overflow-hidden shadow-2xl border border-[#C5B37D]/30">
          <img
            src="https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=1000&q=80"
            alt="Firma Profili"
            className="w-full h-full object-cover"
          />
        </div>
      </div>

    </div>
  );
}
