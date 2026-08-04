import React, { useState, useEffect } from 'react';
import PublicNavbar from './PublicNavbar';
import PublicFooter from './PublicFooter';

export default function PublicLayout({ children, currentRoute = '/', navigateTo }) {
  const [themeMode, setThemeMode] = useState(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('irem_public_theme') || 'dark';
    }
    return 'dark';
  });

  useEffect(() => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('irem_public_theme', themeMode);
    }
  }, [themeMode]);

  const handleToggleTheme = () => {
    setThemeMode((prev) => (prev === 'dark' ? 'light' : 'dark'));
  };

  return (
    <div
      className={`min-h-screen font-sans transition-colors duration-300 relative flex flex-col justify-between overflow-x-hidden ${
        themeMode === 'dark'
          ? 'bg-slate-950 text-slate-100'
          : 'bg-slate-50 text-slate-900'
      }`}
    >
      {/* TOP NAVIGATION BAR */}
      <PublicNavbar
        currentRoute={currentRoute}
        navigateTo={navigateTo}
        themeMode={themeMode}
        onToggleTheme={handleToggleTheme}
      />

      {/* MAIN PUBLIC PAGE CONTENT */}
      <main className="flex-1 w-full pt-20">
        {children}
      </main>

      {/* FLOATING WHATSAPP BUTTON */}
      <a
        href="https://wa.me/905320000000?text=Merhaba,%20İrem%20Düğün%20Sarayı%20hakkında%20bilgi%20ve%20teklif%20almak%20istiyorum."
        target="_blank"
        rel="noreferrer"
        className="fixed bottom-6 right-6 z-50 bg-emerald-500 hover:bg-emerald-600 text-white w-14 h-14 rounded-full flex items-center justify-center shadow-2xl hover:scale-110 transition duration-300 group"
        title="WhatsApp Hızlı İletişim Hattı"
      >
        <span className="text-2xl group-hover:rotate-12 transition transform">💬</span>
        <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full border-2 border-white animate-ping" />
      </a>

      {/* FOOTER */}
      <PublicFooter navigateTo={navigateTo} />
    </div>
  );
}
