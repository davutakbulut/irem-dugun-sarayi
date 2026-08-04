import React from 'react';

export default function AboutUsPage() {
  return (
    <div className="max-w-7xl mx-auto px-6 sm:px-12 py-12 space-y-16">
      
      {/* HEADER */}
      <div className="text-center space-y-4 max-w-3xl mx-auto">
        <span className="text-amber-500 font-extrabold text-xs uppercase tracking-widest">
          ℹ️ Kurumsal Vizyonumuz & Hikayemiz
        </span>
        <h1 className="text-4xl sm:text-5xl font-heading font-extrabold text-white">
          İrem Düğün Sarayı & Balo Tesisleri
        </h1>
        <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
          15 yılı aşkın tecrübemizle, Sapanca Göl kenarında binlerce çiftin en mutlu gününe şahitlik ediyoruz.
        </p>
      </div>

      {/* STORY & MISSION */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
        <div className="space-y-5 text-slate-300 text-xs sm:text-sm leading-relaxed">
          <h2 className="text-2xl sm:text-3xl font-heading font-extrabold text-white">
            Doğanın Kalbinde Lüks ve İhtişam
          </h2>
          <p>
            İrem Düğün Sarayı, Sapanca Gölünün eşsiz manzarasına karşı kurulmuş 3.500 m² açık kır bahçesi ve 3 farklı kapalı balo salonuyla bölgenin en prestijli organizasyon kompleksidir.
          </p>
          <p>
            Alanında uzman şeflerimiz tarafından hazırlanan zengin ikram menüleri, son teknoloji iklimlendirme ve ışık şovlarımızla her daveti bir sanat eserine dönüştürüyoruz.
          </p>

          <div className="pt-2 grid grid-cols-2 gap-4">
            <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl">
              <div className="text-xl font-bold text-amber-400">15+ Yıl</div>
              <div className="text-[11px] text-slate-400">Sektörel Deneyim</div>
            </div>
            <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl">
              <div className="text-xl font-bold text-amber-400">ISO 22000</div>
              <div className="text-[11px] text-slate-400">Gıda Güvenliği Belgeli</div>
            </div>
          </div>
        </div>

        <div className="h-96 rounded-3xl overflow-hidden shadow-2xl border border-amber-500/30">
          <img
            src="https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=1000&q=80"
            alt="Hakkımızda"
            className="w-full h-full object-cover"
          />
        </div>
      </div>

    </div>
  );
}
