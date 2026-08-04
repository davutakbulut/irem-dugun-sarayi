import React, { useState, useEffect } from 'react';

export default function PublicNavbar({ currentRoute = '/', navigateTo }) {
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
    { label: 'ANA SAYFA', route: '/' },
    { label: 'FİRMA PROFİLİ', route: '/hakkimizda' },
    { label: 'DÜĞÜN MEKANLARIMIZ', route: '/salonlar' },
    { label: 'ORGANİZASYONLARIMIZ', route: '/organizasyonlar' },
    { label: '360° SANAL TUR', route: '/360-tur' },
    { label: 'VİDEOLAR', route: '/videolar' },
    { label: 'BLOG', route: '/blog' },
    { label: 'İLETİŞİM', route: '/iletisim' },
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
          ? 'bg-[#F5F2ED]/95 backdrop-blur-md border-b border-[#E6E1D8] py-3 shadow-md text-[#1A1A1A]'
          : 'bg-gradient-to-b from-black/80 via-black/40 to-transparent py-5 text-white'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between">
        {/* LOGO & BRAND */}
        <div
          onClick={() => handleNavClick('/')}
          className="flex items-center space-x-3 cursor-pointer group"
        >
          <div className="w-10 h-10 rounded-full border border-[#C5B37D] bg-black/40 flex items-center justify-center text-[#C5B37D] font-serif text-xl shrink-0 group-hover:scale-105 transition duration-300">
            👑
          </div>
          <div>
            <h1 className={`font-serif tracking-widest text-lg sm:text-xl font-bold uppercase transition-colors ${
              isScrolled ? 'text-[#1A1A1A]' : 'text-white'
            }`}>
              İREM DÜĞÜN SARAYI
            </h1>
            <p className="text-[10px] font-medium tracking-[0.25em] text-[#C5B37D] uppercase">
              Balo & Davet Tesisleri
            </p>
          </div>
        </div>

        {/* DESKTOP NAVIGATION LINKS */}
        <nav className="hidden lg:flex items-center space-x-1 xl:space-x-3">
          {navLinks.map((link) => {
            const isActive = currentRoute === link.route;
            return (
              <button
                key={link.route}
                onClick={() => handleNavClick(link.route)}
                className={`px-3 py-2 text-xs font-semibold tracking-wider transition-all duration-200 cursor-pointer ${
                  isActive
                    ? 'text-[#C5B37D] border-b-2 border-[#C5B37D]'
                    : isScrolled
                    ? 'text-[#1A1A1A] hover:text-[#C5B37D]'
                    : 'text-white/90 hover:text-[#C5B37D]'
                }`}
              >
                {link.label}
              </button>
            );
          })}
        </nav>

        {/* RIGHT CTA BUTTON */}
        <div className="hidden sm:flex items-center space-x-3">
          <button
            onClick={() => handleNavClick('/iletisim')}
            className="bg-[#1A1A1A] hover:bg-[#2c2c2c] text-[#F5F2ED] border border-[#C5B37D] text-xs font-bold tracking-widest px-5 py-2.5 rounded-full transition cursor-pointer hover:shadow-lg uppercase"
          >
            FİYAT TEKLİFİ AL
          </button>
        </div>

        {/* MOBILE HAMBURGER BUTTON */}
        <div className="flex lg:hidden items-center">
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className={`w-10 h-10 rounded-md flex items-center justify-center font-bold text-xl ${
              isScrolled ? 'text-[#1A1A1A]' : 'text-white'
            }`}
          >
            {isMobileMenuOpen ? '✕' : '☰'}
          </button>
        </div>
      </div>

      {/* MOBILE MENU DRAWER */}
      {isMobileMenuOpen && (
        <div className="lg:hidden bg-[#F5F2ED] border-b border-[#E6E1D8] px-4 pt-4 pb-6 space-y-3 mt-3 animate-fade-in text-[#1A1A1A] shadow-2xl">
          <div className="flex flex-col space-y-2">
            {navLinks.map((link) => (
              <button
                key={link.route}
                onClick={() => handleNavClick(link.route)}
                className={`w-full text-left px-4 py-3 text-xs font-bold tracking-wider rounded-lg border-b border-[#E6E1D8]/50 ${
                  currentRoute === link.route
                    ? 'bg-[#C5B37D] text-white'
                    : 'hover:bg-[#E6E1D8]/50 text-[#1A1A1A]'
                }`}
              >
                {link.label}
              </button>
            ))}
          </div>

          <div className="pt-3">
            <button
              onClick={() => handleNavClick('/iletisim')}
              className="w-full bg-[#1A1A1A] text-[#F5F2ED] border border-[#C5B37D] font-bold text-xs py-3 rounded-full uppercase tracking-widest"
            >
              FİYAT TEKLİFİ AL
            </button>
          </div>
        </div>
      )}
    </header>
  );
}
