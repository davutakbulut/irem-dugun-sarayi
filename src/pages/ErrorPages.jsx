import React, { useState, useEffect } from 'react';

// 1. 404 NOT FOUND PAGE
export function Page404({ onNavigate }) {
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <div className="min-h-[80vh] flex flex-col items-center justify-center p-6 text-center animate-fade-in">
      <div className="relative mb-6">
        <div className="absolute inset-0 bg-amber-500/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="relative w-28 h-28 sm:w-36 sm:h-36 rounded-3xl bg-gradient-to-br from-amber-500/20 via-slate-800 to-amber-900/40 border border-amber-500/40 flex items-center justify-center text-5xl sm:text-6xl font-heading font-extrabold text-gold-400 shadow-2xl">
          404
        </div>
      </div>

      <span className="bg-amber-500/20 text-amber-800 dark:text-gold-400 font-mono font-bold text-xs px-3 py-1 rounded-full border border-amber-500/30 uppercase tracking-widest mb-3">
        HTTP 404 — Sayfa Bulunamadı
      </span>

      <h1 className="text-2xl sm:text-4xl font-heading font-extrabold text-slate-900 dark:text-white max-w-xl leading-tight mb-3">
        Aradığınız Sayfa Bulunamadı veya Taşınmış Olabilir
      </h1>

      <p className="text-xs sm:text-sm text-slate-600 dark:text-gray-400 max-w-md mb-8 leading-relaxed">
        Girmeye çalıştığınız sayfa adresi değiştirilmiş, silinmiş veya geçici olarak servis dışı kalmış olabilir. Lütfen adresi kontrol edin veya aşağıdaki hızlı bağlantıları kullanın.
      </p>

      {/* QUICK SEARCH */}
      <div className="w-full max-w-md mb-8">
        <div className="relative">
          <input
            type="text"
            placeholder="🔍 Sistemde hızlı arama yapın (Örn: Rezervasyonlar, Müşteri...)"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-white dark:bg-brand-dark border border-slate-300 dark:border-brand-border rounded-2xl py-3 pl-4 pr-12 text-xs font-medium text-slate-800 dark:text-gray-200 shadow-lg focus:outline-none focus:ring-2 focus:ring-amber-500"
          />
          {searchQuery && (
            <button
              onClick={() => onNavigate && onNavigate('reservations')}
              className="absolute right-2 top-2 bottom-2 bg-amber-600 text-white text-xs font-bold px-3 rounded-xl hover:bg-amber-500 transition"
            >
              Ara
            </button>
          )}
        </div>
      </div>

      {/* NAVIGATION SHORTCUTS */}
      <div className="flex flex-wrap justify-center gap-3 text-xs font-bold">
        <button
          onClick={() => onNavigate && onNavigate('dashboard')}
          className="gold-button px-5 py-3 rounded-2xl shadow-lg flex items-center space-x-2"
        >
          <span>🏠</span>
          <span>Ana Panele Dön</span>
        </button>

        <button
          onClick={() => onNavigate && onNavigate('reservations')}
          className="px-5 py-3 rounded-2xl bg-white dark:bg-brand-card text-slate-800 dark:text-gray-200 border border-slate-200 dark:border-brand-border hover:border-amber-500/40 shadow-sm flex items-center space-x-2 transition"
        >
          <span>📅</span>
          <span>Rezervasyonlarım & Takvim</span>
        </button>

        <button
          onClick={() => onNavigate && onNavigate('create-reservation')}
          className="px-5 py-3 rounded-2xl bg-white dark:bg-brand-card text-slate-800 dark:text-gray-200 border border-slate-200 dark:border-brand-border hover:border-amber-500/40 shadow-sm flex items-center space-x-2 transition"
        >
          <span>➕</span>
          <span>Yeni Rezervasyon</span>
        </button>
      </div>
    </div>
  );
}

// 2. 301 PERMANENT REDIRECT PAGE
export function Page301({ targetRoute = 'reservations', targetName = 'Rezervasyonlar & Takvim Yönetimi', onNavigate }) {
  const [countdown, setCountdown] = useState(5);

  useEffect(() => {
    const timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          if (onNavigate) onNavigate(targetRoute);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [targetRoute, onNavigate]);

  return (
    <div className="min-h-[80vh] flex flex-col items-center justify-center p-6 text-center animate-fade-in">
      <div className="w-24 h-24 rounded-3xl bg-amber-500/10 border border-amber-500/30 text-amber-600 dark:text-gold-400 flex items-center justify-center text-4xl font-extrabold mb-6 shadow-xl">
        🔄
      </div>

      <span className="bg-amber-500/20 text-amber-800 dark:text-gold-400 font-mono font-bold text-xs px-3 py-1 rounded-full border border-amber-500/30 uppercase tracking-widest mb-3">
        HTTP 301 — Kalıcı Yönlendirme (Moved Permanently)
      </span>

      <h1 className="text-2xl sm:text-3xl font-heading font-extrabold text-slate-900 dark:text-white max-w-xl mb-3">
        Bu Sayfa Yeni Adresine Taşındı
      </h1>

      <p className="text-xs sm:text-sm text-slate-600 dark:text-gray-400 max-w-md mb-6 leading-relaxed">
        Erişmeye çalıştığınız içerik yeni güncellenen konuma taşınmıştır. Sistem sizi otomatik olarak yönlendiriyor.
      </p>

      {/* REDIRECT BADGE */}
      <div className="bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border p-4 rounded-2xl shadow-md max-w-sm w-full mb-6 text-xs font-bold space-y-2">
        <div className="flex justify-between items-center text-slate-400">
          <span>Eski Konum:</span>
          <span className="font-mono text-red-500 line-through">/#/old-route</span>
        </div>
        <div className="flex justify-between items-center text-emerald-600 dark:text-emerald-400">
          <span>Yeni Konum:</span>
          <span className="font-mono">{targetName}</span>
        </div>
      </div>

      {/* COUNTDOWN & ACTION */}
      <div className="flex items-center space-x-4 text-xs">
        <div className="bg-amber-500/10 text-amber-800 dark:text-gold-400 font-mono font-extrabold px-4 py-2.5 rounded-xl border border-amber-500/30">
          ⏳ {countdown} saniye içinde yönlendiriliyorsunuz...
        </div>

        <button
          onClick={() => onNavigate && onNavigate(targetRoute)}
          className="gold-button px-5 py-2.5 rounded-xl font-bold shadow-md"
        >
          Hemen Git ➔
        </button>
      </div>
    </div>
  );
}

// 3. 403 FORBIDDEN PAGE
export function Page403({ requiredRole = 'Yönetici (Admin)', onNavigate }) {
  return (
    <div className="min-h-[80vh] flex flex-col items-center justify-center p-6 text-center animate-fade-in">
      <div className="w-24 h-24 rounded-3xl bg-red-500/10 border border-red-500/30 text-red-600 dark:text-red-400 flex items-center justify-center text-4xl font-extrabold mb-6 shadow-xl">
        🛡️
      </div>

      <span className="bg-red-500/20 text-red-700 dark:text-red-400 font-mono font-bold text-xs px-3 py-1 rounded-full border border-red-500/30 uppercase tracking-widest mb-3">
        HTTP 403 — Yetkisiz Erişim Denemesi
      </span>

      <h1 className="text-2xl sm:text-3xl font-heading font-extrabold text-slate-900 dark:text-white max-w-xl mb-3">
        Bu Sayfaya Erişim Yetkiniz Bulunmuyor
      </h1>

      <p className="text-xs sm:text-sm text-slate-600 dark:text-gray-400 max-w-md mb-6 leading-relaxed">
        Bu modüldeki işlem ve verileri görüntülemek için <strong className="text-slate-900 dark:text-white">{requiredRole}</strong> rol yetkisine sahip olmanız gerekmektedir.
      </p>

      {/* ACTION BUTTONS */}
      <div className="flex flex-wrap justify-center gap-3 text-xs font-bold">
        <button
          onClick={() => onNavigate && onNavigate('dashboard')}
          className="px-5 py-3 rounded-2xl bg-slate-800 text-white hover:bg-slate-700 shadow-md flex items-center space-x-2 transition"
        >
          <span>🏠</span>
          <span>Ana Panele Dön</span>
        </button>

        <button
          onClick={() => alert('Yetki yükseltme talebiniz sistem yöneticisine iletildi!')}
          className="px-5 py-3 rounded-2xl bg-amber-500/20 text-amber-800 dark:text-gold-400 border border-amber-500/40 hover:bg-amber-500/30 shadow-sm flex items-center space-x-2 transition"
        >
          <span>🔑</span>
          <span>Yöneticiden Yetki İste</span>
        </button>
      </div>
    </div>
  );
}

// 4. 500 INTERNAL SERVER ERROR PAGE
export function Page500({ errorDetails = 'Bilinmeyen bir işlem hatası meydana geldi.', onNavigate }) {
  const [showStack, setShowStack] = useState(false);

  return (
    <div className="min-h-[80vh] flex flex-col items-center justify-center p-6 text-center animate-fade-in">
      <div className="w-24 h-24 rounded-3xl bg-red-500/10 border border-red-500/30 text-red-600 dark:text-red-400 flex items-center justify-center text-4xl font-extrabold mb-6 shadow-xl">
        💥
      </div>

      <span className="bg-red-500/20 text-red-700 dark:text-red-400 font-mono font-bold text-xs px-3 py-1 rounded-full border border-red-500/30 uppercase tracking-widest mb-3">
        HTTP 500 — Sunucu & Sistem Hatası
      </span>

      <h1 className="text-2xl sm:text-3xl font-heading font-extrabold text-slate-900 dark:text-white max-w-xl mb-3">
        Beklenmeyen Bir Hata Oluştu
      </h1>

      <p className="text-xs sm:text-sm text-slate-600 dark:text-gray-400 max-w-md mb-6 leading-relaxed">
        Sistem otomatik hata günlüğüne kaydetti. Sayfayı yenileyerek veya önbelleği temizleyerek tekrar deneyebilirsiniz.
      </p>

      {/* ERROR DETAILS ACCORDION */}
      <div className="w-full max-w-lg mb-6 text-left">
        <button
          onClick={() => setShowStack(!showStack)}
          className="w-full p-3 bg-slate-100 dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl text-xs font-bold text-slate-700 dark:text-gray-300 flex justify-between items-center"
        >
          <span>🛠️ Teknik Hata Detayı</span>
          <span>{showStack ? '▲' : '▼'}</span>
        </button>

        {showStack && (
          <div className="p-3 bg-slate-950 text-red-400 font-mono text-[11px] rounded-b-xl border border-t-0 border-slate-800 space-y-1 overflow-x-auto">
            <div>[ERROR 500]: {errorDetails}</div>
            <div>[TIMESTAMP]: {new Date().toISOString()}</div>
            <div>[USER AGENT]: {navigator.userAgent}</div>
          </div>
        )}
      </div>

      {/* ACTION BUTTONS */}
      <div className="flex flex-wrap justify-center gap-3 text-xs font-bold">
        <button
          onClick={() => window.location.reload()}
          className="gold-button px-5 py-3 rounded-2xl shadow-md flex items-center space-x-2"
        >
          <span>↺</span>
          <span>Sistemi Yeniden Başlat & Yenile</span>
        </button>

        <button
          onClick={() => onNavigate && onNavigate('dashboard')}
          className="px-5 py-3 rounded-2xl bg-white dark:bg-brand-card text-slate-800 dark:text-gray-200 border border-slate-200 dark:border-brand-border hover:border-amber-500/40 shadow-sm flex items-center space-x-2 transition"
        >
          <span>🏠</span>
          <span>Ana Panele Dön</span>
        </button>
      </div>
    </div>
  );
}
