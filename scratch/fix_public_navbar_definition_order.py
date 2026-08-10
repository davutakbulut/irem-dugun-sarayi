import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check if PublicNavbar function exists
if "function PublicNavbar(" not in content:
    public_navbar_code = """    // 1. PUBLIC NAVBAR MODULE (90VW RIGHT SLIDE-IN GLASS DRAWER WITH FULL DESKTOP SYNCED LINKS & QUICK CONTACT FOOTER)
    function PublicNavbar({ currentRoute = '/', navigateTo, onSaveQuoteRequest, showToast }) {
      const [isScrolled, setIsScrolled] = useState(false);
      const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
      const [isLeadModalOpen, setIsLeadModalOpen] = useState(false);
      const isHomePage = currentRoute === '/' || currentRoute === '' || currentRoute === 'public-home';

      useEffect(() => {
        const handleScroll = () => setIsScrolled(window.scrollY > 40);
        window.addEventListener('scroll', handleScroll, { passive: true });
        handleScroll();
        return () => window.removeEventListener('scroll', handleScroll);
      }, []);

      // Synchronize body scroll locks when mobile drawer opens
      useEffect(() => {
        if (isMobileMenuOpen) {
          document.body.style.overflow = 'hidden';
        } else {
          document.body.style.overflow = '';
        }
        return () => { document.body.style.overflow = ''; };
      }, [isMobileMenuOpen]);

      const navLinks = [
        { label: 'ANA SAYFA', route: '/' },
        { label: 'FİRMA PROFİLİ', route: '/hakkimizda' },
        { label: 'DÜĞÜN MEKANLARIMIZ', route: '/salonlar' },
        { label: '360° SANAL TUR', route: '/360-tur' },
        { label: 'ORGANİZASYONLARIMIZ', route: '/organizasyonlar' },
        { label: 'GALERİ & FOTOĞRAFLAR', route: '/videolar' },
        { label: 'DÜĞÜN REHBERİ & BLOG', route: '/blog' },
        { label: 'MÜŞTERİ VIP PORTALI', route: '/musteri-giris' },
        { label: 'İLETİŞİM & KONUM', route: '/iletisim' }
      ];

      const handleNavClick = (e, route) => {
        if (e) e.preventDefault();
        setIsMobileMenuOpen(false);
        if (navigateTo) navigateTo(route);
        else window.location.href = route;
      };

      const isTransparentMode = isHomePage && !isScrolled;

      return (
        <>
          <header className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ease-in-out ${
            isTransparentMode 
              ? 'bg-transparent border-transparent py-5 text-white drop-shadow-md' 
              : 'bg-white/95 dark:bg-slate-900/95 backdrop-blur-md shadow-md border-b border-amber-100 dark:border-amber-500/20 py-3.5 text-slate-800 dark:text-gray-100'
          }`}>
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between">
              {/* TOP LOGO */}
              <a href="/" onClick={(e) => handleNavClick(e, '/')} className="flex items-center space-x-3 cursor-pointer group">
                <div className={`w-11 h-11 rounded-2xl flex items-center justify-center font-serif font-black text-2xl shadow-md group-hover:scale-105 transition-all duration-300 ${
                  isTransparentMode ? 'bg-white/20 text-white border border-white/30 backdrop-blur-md' : 'bg-gradient-to-br from-[#B89B5E] to-[#ceb992] text-white'
                }`}>
                  <ThemeIcon icon="venue" className="w-5 h-5 inline-block shrink-0" />
                </div>
                <div>
                  <h1 className={`font-serif font-extrabold text-lg sm:text-xl tracking-wider leading-none transition-colors duration-300 ${
                    isTransparentMode ? 'text-white drop-shadow-lg' : 'text-slate-900 dark:text-gray-100'
                  }`}>
                    İREM DÜĞÜN SARAYI
                  </h1>
                  <p className={`text-[9px] font-bold tracking-widest uppercase mt-1 transition-colors duration-300 ${
                    isTransparentMode ? 'text-amber-200/90' : 'text-[#B89B5E] dark:text-gold-400'
                  }`}>
                    Balo & Davet Tesisleri
                  </p>
                </div>
              </a>

              {/* DESKTOP NAV LINKS */}
              <nav className="hidden lg:flex items-center space-x-6">
                {navLinks.slice(0, 6).map(link => {
                  const isActive = currentRoute === link.route;
                  return (
                    <a
                      key={link.route}
                      href={link.route}
                      onClick={(e) => handleNavClick(e, link.route)}
                      className={`text-[11px] font-extrabold transition-all duration-300 cursor-pointer py-1 uppercase tracking-widest ${
                        isTransparentMode
                          ? (isActive ? 'text-amber-300 border-b-2 border-amber-300' : 'text-white/95 hover:text-amber-300 drop-shadow-md')
                          : (isActive ? 'text-[#B89B5E] border-b-2 border-[#B89B5E]' : 'text-slate-700 dark:text-gray-200 hover:text-[#B89B5E]')
                      }`}
                    >
                      {link.label}
                    </a>
                  );
                })}
              </nav>

              {/* RIGHT DESKTOP CTA BUTTONS */}
              <div className="hidden sm:flex items-center space-x-3">
                <a 
                  href="https://wa.me/905471440054" 
                  target="_blank" 
                  rel="noreferrer" 
                  className={`font-bold text-xs px-4 py-2 rounded-full shadow transition-all duration-300 flex items-center space-x-1.5 ${
                    isTransparentMode 
                      ? 'bg-white/20 hover:bg-white/30 backdrop-blur-md border border-white/40 text-white' 
                      : 'bg-[#25D366] hover:bg-[#20bd5a] text-white'
                  }`}
                >
                  <span><ThemeIcon icon="chat" className="w-4 h-4 inline-block shrink-0" /></span>
                  <span>WhatsApp</span>
                </a>
                <button 
                  onClick={() => setIsLeadModalOpen(true)} 
                  className="bg-[#B89B5E] hover:bg-[#a3874e] text-white font-bold text-xs px-5 py-2 rounded-full shadow-lg transition-transform hover:scale-105 cursor-pointer flex items-center space-x-1.5 uppercase tracking-wider"
                >
                  <span><ThemeIcon icon="crown" className="w-4 h-4 inline-block shrink-0" /></span>
                  <span>Teklif Alın</span>
                </button>
              </div>

              {/* MOBILE TOGGLE BUTTON */}
              <div className="flex lg:hidden items-center space-x-2">
                <button onClick={() => setIsLeadModalOpen(true)} className="bg-[#B89B5E] text-white font-bold text-xs px-3.5 py-2 rounded-full shadow cursor-pointer">Teklif Al</button>
                <button 
                  type="button"
                  onClick={() => setIsMobileMenuOpen(true)} 
                  className={`w-10 h-10 rounded-xl font-bold text-lg flex items-center justify-center cursor-pointer transition-colors ${
                    isTransparentMode ? 'bg-white/20 text-white backdrop-blur-md border border-white/30' : 'bg-slate-100 text-slate-800'
                  }`}
                  aria-label="Menüyü Aç"
                >
                  ☰
                </button>
              </div>
            </div>
          </header>

          {/* ANIMATED FULL-HEIGHT 90VW RIGHT SLIDE-IN GLASSMOBILE DRAWER WITH BLUR BACKDROP */}
          {isMobileMenuOpen && (
            <>
              {/* FLUID BLUR BACKDROP OVERLAY */}
              <div 
                className="fixed inset-0 z-[99998] bg-slate-900/60 backdrop-blur-md transition-opacity duration-300"
                onClick={() => setIsMobileMenuOpen(false)}
              />

              {/* 90VW RIGHT SLIDE-IN DRAWER */}
              <div className="fixed inset-y-0 right-0 z-[99999] h-full w-[90vw] max-w-sm sm:max-w-md bg-white/95 dark:bg-slate-900/95 backdrop-blur-2xl shadow-2xl animate-slide-in-right flex flex-col justify-between text-slate-800 dark:text-gray-100 overflow-y-auto border-l border-amber-200/50">
                {/* 1. TOP HEADER AREA (LOGO & CLOSE BUTTON) */}
                <div className="p-5 border-b border-amber-100 dark:border-amber-500/20 flex items-center justify-between bg-gradient-to-r from-amber-50/60 via-white to-transparent dark:from-slate-800/80">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 rounded-2xl bg-[#B89B5E] text-white flex items-center justify-center font-serif font-black text-xl shadow-md">
                      <ThemeIcon icon="venue" className="w-5 h-5 inline-block shrink-0" />
                    </div>
                    <div>
                      <h3 className="font-serif font-extrabold text-base text-slate-900 dark:text-white leading-none">
                        İREM DÜĞÜN SARAYI
                      </h3>
                      <p className="text-[9px] font-bold text-[#B89B5E] tracking-widest uppercase mt-0.5">
                        Balo & Davet Tesisleri
                      </p>
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => setIsMobileMenuOpen(false)}
                    className="w-9 h-9 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-gray-200 font-bold flex items-center justify-center hover:bg-slate-200 transition cursor-pointer text-base"
                    title="Kapat"
                  >
                    ✕
                  </button>
                </div>

                {/* 2. MIDDLE NAVIGATION LINKS (COMPLETE & SYNCHRONIZED WITH DESKTOP) */}
                <div className="p-5 flex-1 space-y-1.5 overflow-y-auto">
                  <div className="text-[10px] font-extrabold text-[#B89B5E] uppercase tracking-widest mb-3 px-2">
                    NAVİGASYON MENÜSÜ
                  </div>
                  {navLinks.map(link => {
                    const isActive = currentRoute === link.route;
                    return (
                      <a
                        key={link.route}
                        href={link.route}
                        onClick={(e) => handleNavClick(e, link.route)}
                        className={`w-full text-left px-4 py-3 rounded-2xl text-xs font-bold flex justify-between items-center transition-all duration-200 ${
                          isActive 
                            ? 'bg-[#B89B5E] text-white shadow-md font-extrabold' 
                            : 'text-slate-700 dark:text-gray-200 hover:bg-amber-50 dark:hover:bg-slate-800/80 hover:text-[#B89B5E]'
                        }`}
                      >
                        <span className="tracking-wide">{link.label}</span>
                        <span className="text-xs opacity-60">→</span>
                      </a>
                    );
                  })}
                </div>

                {/* 3. BOTTOM QUICK CONTACT & TEKLİF AL AREA */}
                <div className="p-5 border-t border-amber-100 dark:border-amber-500/20 bg-slate-50/90 dark:bg-slate-800/60 space-y-3">
                  <div className="text-[10px] font-extrabold text-[#B89B5E] uppercase tracking-widest px-1">
                    HIZLI İLETİŞİM & RANDEVU
                  </div>

                  <div className="grid grid-cols-2 gap-2 text-xs font-bold">
                    <a
                      href="tel:+905471440054"
                      className="p-2.5 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 flex items-center space-x-2 text-slate-800 dark:text-gray-100 shadow-xs hover:border-[#B89B5E] transition"
                    >
                      <ThemeIcon icon="phone" className="w-4 h-4 text-[#B89B5E] shrink-0" />
                      <span className="truncate text-[11px]">+90 547 144 00 54</span>
                    </a>

                    <a
                      href="https://wa.me/905471440054"
                      target="_blank"
                      rel="noreferrer"
                      className="p-2.5 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 flex items-center space-x-2 text-emerald-600 font-bold shadow-xs hover:border-emerald-500 transition"
                    >
                      <ThemeIcon icon="chat" className="w-4 h-4 text-emerald-500 shrink-0" />
                      <span className="text-[11px]">WhatsApp Hat</span>
                    </a>
                  </div>

                  <button
                    type="button"
                    onClick={() => { setIsMobileMenuOpen(false); setIsLeadModalOpen(true); }}
                    className="w-full bg-[#B89B5E] hover:bg-[#a3874e] text-white font-extrabold py-3.5 rounded-full text-xs shadow-lg transition-transform hover:scale-[1.02] active:scale-95 uppercase tracking-wider flex items-center justify-center space-x-2 cursor-pointer"
                  >
                    <span><ThemeIcon icon="crown" className="w-4 h-4 inline-block shrink-0" /></span>
                    <span>ÜCRETSİZ FİYAT TEKLİFİ ALIN</span>
                  </button>
                </div>
              </div>
            </>
          )}

          <LeadModal isOpen={isLeadModalOpen} onClose={() => setIsLeadModalOpen(false)} onSaveQuoteRequest={onSaveQuoteRequest} showToast={showToast} />
        </>
      );
    }
"""
    marker = "    // 3. PUBLIC LAYOUT MODULE (ISOLATED NAVBAR & FOOTER BLOCKS)"
    marker_idx = content.find(marker)
    if marker_idx != -1:
        content = content[:marker_idx] + public_navbar_code + "\n\n" + content[marker_idx:]
        print("Successfully re-inserted PublicNavbar before PublicLayout!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
