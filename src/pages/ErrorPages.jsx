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

      <span className="bg-amber-500/20 text-amber-800 dark:text-gold-400 font-mono font-bold text-xs px-3.5 py-1 rounded-full border border-amber-500/30 uppercase tracking-widest mb-3">
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
            placeholder="Sistemde hızlı arama yapın (Örn: Rezervasyonlar, Müşteri...)"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-white dark:bg-brand-dark border border-slate-300 dark:border-brand-border rounded-2xl py-3 pl-4 pr-12 text-xs font-medium text-slate-800 dark:text-gray-200 shadow-lg focus:outline-none focus:ring-2 focus:ring-amber-500"
          />
          {searchQuery && (
            <button
              onClick={() => onNavigate && onNavigate('reservations')}
              className="absolute right-2 top-2 bottom-2 bg-amber-600 text-white text-xs font-bold px-3 rounded-xl hover:bg-amber-500 transition inline-flex items-center space-x-1"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
              <span>Ara</span>
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
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
          </svg>
          <span>Ana Panele Dön</span>
        </button>

        <button
          onClick={() => onNavigate && onNavigate('reservations')}
          className="px-5 py-3 rounded-2xl bg-white dark:bg-brand-card text-slate-800 dark:text-gray-200 border border-slate-200 dark:border-brand-border hover:border-amber-500/40 shadow-sm flex items-center space-x-2 transition"
        >
          <svg className="w-4 h-4 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
          </svg>
          <span>Rezervasyonlarım & Takvim</span>
        </button>

        <button
          onClick={() => onNavigate && onNavigate('create-reservation')}
          className="px-5 py-3 rounded-2xl bg-white dark:bg-brand-card text-slate-800 dark:text-gray-200 border border-slate-200 dark:border-brand-border hover:border-amber-500/40 shadow-sm flex items-center space-x-2 transition"
        >
          <svg className="w-4 h-4 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4"></path>
          </svg>
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
      <div className="w-24 h-24 rounded-3xl bg-blue-500/10 border border-blue-500/30 text-blue-600 dark:text-blue-400 flex items-center justify-center mb-6 shadow-xl">
        <svg className="w-12 h-12 animate-spin" style={{ animationDuration: '3s' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
        </svg>
      </div>

      <span className="bg-blue-500/20 text-blue-700 dark:text-blue-400 font-mono font-bold text-xs px-3.5 py-1 rounded-full border border-blue-500/30 uppercase tracking-widest mb-3">
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
        <div className="bg-blue-500/10 text-blue-700 dark:text-blue-400 font-mono font-extrabold px-4 py-2.5 rounded-xl border border-blue-500/30 flex items-center space-x-1.5">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <span>{countdown} saniye içinde yönlendiriliyorsunuz...</span>
        </div>

        <button
          onClick={() => onNavigate && onNavigate(targetRoute)}
          className="gold-button px-5 py-2.5 rounded-xl font-bold shadow-md inline-flex items-center space-x-1"
        >
          <span>Hemen Git</span>
          <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
          </svg>
        </button>
      </div>
    </div>
  );
}

// 3. 403 FORBIDDEN PAGE
export function Page403({ requiredRole = 'Yönetici (Admin)', onNavigate }) {
  return (
    <div className="min-h-[80vh] flex flex-col items-center justify-center p-6 text-center animate-fade-in">
      <div className="w-24 h-24 rounded-3xl bg-red-500/10 border border-red-500/30 text-red-600 dark:text-red-400 flex items-center justify-center mb-6 shadow-xl">
        <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
        </svg>
      </div>

      <span className="bg-red-500/20 text-red-700 dark:text-red-400 font-mono font-bold text-xs px-3.5 py-1 rounded-full border border-red-500/30 uppercase tracking-widest mb-3">
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
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
          </svg>
          <span>Ana Panele Dön</span>
        </button>

        <button
          onClick={() => alert('Yetki yükseltme talebiniz sistem yöneticisine iletildi!')}
          className="px-5 py-3 rounded-2xl bg-amber-500/20 text-amber-800 dark:text-gold-400 border border-amber-500/40 hover:bg-amber-500/30 shadow-sm flex items-center space-x-2 transition"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"></path>
          </svg>
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
      <div className="w-24 h-24 rounded-3xl bg-purple-500/10 border border-purple-500/30 text-purple-600 dark:text-purple-400 flex items-center justify-center mb-6 shadow-xl">
        <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
        </svg>
      </div>

      <span className="bg-purple-500/20 text-purple-700 dark:text-purple-400 font-mono font-bold text-xs px-3.5 py-1 rounded-full border border-purple-500/30 uppercase tracking-widest mb-3">
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
          <span className="flex items-center space-x-1.5">
            <svg className="w-4 h-4 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
            </svg>
            <span>Teknik Hata Detayı</span>
          </span>
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
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          <span>Sistemi Yeniden Başlat & Yenile</span>
        </button>

        <button
          onClick={() => onNavigate && onNavigate('dashboard')}
          className="px-5 py-3 rounded-2xl bg-white dark:bg-brand-card text-slate-800 dark:text-gray-200 border border-slate-200 dark:border-brand-border hover:border-amber-500/40 shadow-sm flex items-center space-x-2 transition"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
          </svg>
          <span>Ana Panele Dön</span>
        </button>
      </div>
    </div>
  );
}
