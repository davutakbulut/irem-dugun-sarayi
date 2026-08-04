import React, { useState, useEffect } from 'react';

export default function PublicNavbar({ currentRoute = '/', navigateTo, themeMode, onToggleTheme }) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 20) {
        setIsScrolled(true);
      } else {
        setIsScrolled(false);
      }
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navLinks = [
    { label: 'Anasayfa', route: '/' },
    { label: 'Salonlarımız', route: '/salonlar' },
    { label: '360° Sanal Tur', route: '/360-tur', isNew: true },
    { label: 'Organizasyonlar', route: '/organizasyonlar' },
    { label: 'Videolar', route: '/videolar' },
    { label: 'Düğün Rehberi', route: '/blog' },
    { label: 'Hakkımızda', route: '/hakkimizda' },
    { label: 'İletişim', route: '/iletisim' },
  ];

  const handleNavClick = (route) => {
    setIsMobileMenuOpen(false);
    if (navigateTo) {
      navigateTo(route);
    } else {
      window.location.href = route;
    }
  };

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled
          ? themeMode === 'dark'
            ? 'bg-slate-950/90 backdrop-blur-md border-b border-amber-500/20 py-3 shadow-xl'
            : 'bg-white/90 backdrop-blur-md border-b border-amber-500/20 py-3 shadow-md'
          : 'bg-gradient-to-b from-slate-950/80 via-slate-950/40 to-transparent py-5'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between">
        {/* LOGO & BRAND */}
        <div
          onClick={() => handleNavClick('/')}
          className="flex items-center space-x-3 cursor-pointer group"
        >
          <div className="w-11 h-11 rounded-2xl bg-gradient-to-br from-amber-500 via-orange-500 to-amber-600 flex items-center justify-center text-white font-extrabold text-xl shadow-lg border border-amber-400/40 shrink-0 group-hover:scale-105 transition duration-300">
            🏰
          </div>
          <div>
            <h1 className="font-heading font-extrabold text-lg sm:text-xl text-white tracking-wide leading-tight gold-gradient-text">
              İREM DÜĞÜN SARAYI
            </h1>
            <p className="text-[10px] font-bold text-amber-400 tracking-widest uppercase flex items-center space-x-1">
              <span>👑</span>
              <span>Balo & Organizasyon Tesisleri</span>
            </p>
          </div>
        </div>

        {/* DESKTOP NAVIGATION LINKS */}
        <nav className="hidden lg:flex items-center space-x-1 xl:space-x-2">
          {navLinks.map((link) => {
            const isActive = currentRoute === link.route;
            return (
              <button
                key={link.route}
                onClick={() => handleNavClick(link.route)}
                className={`px-3.5 py-2 rounded-xl text-xs font-bold transition-all duration-200 cursor-pointer flex items-center space-x-1.5 ${
                  isActive
                    ? 'bg-gradient-to-r from-amber-500 to-amber-600 text-white shadow-md'
                    : isScrolled && themeMode === 'light'
                    ? 'text-slate-700 hover:text-amber-600 hover:bg-amber-500/10'
                    : 'text-slate-200 hover:text-amber-400 hover:bg-white/10'
                }`}
              >
                <span>{link.label}</span>
                {link.isNew && (
                  <span className="bg-gradient-to-r from-red-500 to-amber-500 text-white text-[9px] font-black px-1.5 py-0.5 rounded-md animate-pulse">
                    360°
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        {/* RIGHT ACTION BUTTONS */}
        <div className="hidden sm:flex items-center space-x-3">
          {/* THEME TOGGLE BUTTON */}
          <button
            onClick={onToggleTheme}
            className="w-10 h-10 rounded-xl bg-white/10 hover:bg-white/20 text-amber-400 flex items-center justify-center transition cursor-pointer border border-amber-500/30"
            title={themeMode === 'dark' ? 'Gündüz Moduna Geç' : 'Gece Moduna Geç'}
          >
            {themeMode === 'dark' ? '☀️' : '🌙'}
          </button>

          {/* QUICK QUOTE CTA BUTTON */}
          <button
            onClick={() => handleNavClick('/iletisim')}
            className="gold-button font-extrabold text-xs px-4 py-2.5 rounded-xl shadow-lg flex items-center space-x-2 hover:scale-105 transition cursor-pointer"
          >
            <span>Teklif Alın</span>
            <span>→</span>
          </button>

          {/* VIP CLIENT PORTAL LOGIN */}
          <button
            onClick={() => handleNavClick('/musteri-giris')}
            className="bg-slate-800/80 hover:bg-slate-800 text-amber-400 font-bold text-xs px-3.5 py-2.5 rounded-xl border border-amber-500/30 flex items-center space-x-1.5 transition cursor-pointer"
            title="Sözleşmeli Müşteri Portalı Girişi"
          >
            <span>🔑</span>
            <span>Müşteri Portalı</span>
          </button>
        </div>

        {/* MOBILE HAMBURGER BUTTON */}
        <div className="flex sm:hidden items-center space-x-2">
          <button
            onClick={onToggleTheme}
            className="w-9 h-9 rounded-xl bg-white/10 text-amber-400 flex items-center justify-center"
          >
            {themeMode === 'dark' ? '☀️' : '🌙'}
          </button>

          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="w-10 h-10 rounded-xl bg-amber-500 text-white flex items-center justify-center font-bold text-xl shadow"
          >
            {isMobileMenuOpen ? '✕' : '☰'}
          </button>
        </div>
      </div>

      {/* MOBILE MENU DRAWER */}
      {isMobileMenuOpen && (
        <div className="lg:hidden bg-slate-950/95 backdrop-blur-xl border-b border-amber-500/30 px-4 pt-4 pb-6 space-y-3 mt-3 animate-fade-in text-white shadow-2xl">
          <div className="grid grid-cols-1 gap-1.5">
            {navLinks.map((link) => (
              <button
                key={link.route}
                onClick={() => handleNavClick(link.route)}
                className={`w-full text-left px-4 py-3 rounded-xl font-bold text-sm flex items-center justify-between ${
                  currentRoute === link.route
                    ? 'bg-amber-500 text-white'
                    : 'hover:bg-white/10 text-slate-200'
                }`}
              >
                <span>{link.label}</span>
                {link.isNew && (
                  <span className="bg-red-500 text-white text-[10px] font-black px-2 py-0.5 rounded-full">
                    360° Canlı Tur
                  </span>
                )}
              </button>
            ))}
          </div>

          <div className="pt-3 border-t border-slate-800 grid grid-cols-2 gap-2">
            <button
              onClick={() => handleNavClick('/iletisim')}
              className="gold-button font-extrabold text-xs py-3 rounded-xl shadow text-center"
            >
              Hızlı Teklif Al
            </button>
            <button
              onClick={() => handleNavClick('/musteri-giris')}
              className="bg-slate-800 text-amber-400 font-bold text-xs py-3 rounded-xl border border-amber-500/40 text-center"
            >
              Müşteri Portalı 🔑
            </button>
          </div>
        </div>
      )}
    </header>
  );
}
