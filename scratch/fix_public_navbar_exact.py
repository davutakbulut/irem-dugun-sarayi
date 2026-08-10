import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace PublicNavbar completely
start_marker = "    function PublicNavbar({ currentRoute = '/', navigateTo }) {"
end_marker = "    function PublicFooter({ navigateTo }) {"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_navbar_code = """    function PublicNavbar({ currentRoute = '/', navigateTo }) {
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

      const navLinks = [
        { label: 'ANA SAYFA', route: '/' },
        { label: 'FİRMA PROFİLİ', route: '/hakkimizda' },
        { label: 'DÜĞÜN MEKANLARIMIZ', route: '/salonlar' },
        { label: 'ORGANİZASYONLARIMIZ', route: '/organizasyonlar' },
        { label: 'BLOG', route: '/blog' },
        { label: 'İLETİŞİM', route: '/iletisim' }
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
              {/* EZO & SVADBA STYLE ELEGANT OVAL LOGO */}
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

              {/* CENTER NAV LINKS (EXACT MATCH FOR SVADBA REFERENCE) */}
              <nav className="hidden lg:flex items-center space-x-7">
                {navLinks.map(link => {
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

              {/* RIGHT CTA BUTTONS */}
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

              {/* MOBILE TOGGLE */}
              <div className="flex lg:hidden items-center space-x-2">
                <button onClick={() => setIsLeadModalOpen(true)} className="bg-[#B89B5E] text-white font-bold text-xs px-3.5 py-2 rounded-full shadow">Teklif Al</button>
                <button 
                  onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} 
                  className={`w-10 h-10 rounded-xl font-bold text-lg flex items-center justify-center cursor-pointer transition-colors ${
                    isTransparentMode ? 'bg-white/20 text-white backdrop-blur-md border border-white/30' : 'bg-slate-100 text-slate-800'
                  }`}
                >
                  {isMobileMenuOpen ? '✕' : '☰'}
                </button>
              </div>
            </div>

            {/* MOBILE DRAWER */}
            {isMobileMenuOpen && (
              <div className="lg:hidden bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-amber-500/20 p-6 space-y-3 shadow-xl animate-fade-in text-slate-800 dark:text-gray-100">
                {navLinks.map(link => (
                  <a key={link.route} href={link.route} onClick={(e) => handleNavClick(e, link.route)} className={`w-full text-left px-4 py-3 rounded-xl text-xs font-bold flex justify-between items-center ${currentRoute === link.route ? 'bg-[#faf8f5] dark:bg-amber-500/10 text-[#B89B5E]' : 'text-slate-700 dark:text-gray-200 hover:bg-slate-50 dark:hover:bg-slate-800'}`}>
                    <span>{link.label}</span>
                  </a>
                ))}
                <div className="pt-4 border-t border-slate-100 dark:border-slate-800 flex flex-col gap-2">
                  <a href="https://wa.me/905471440054" target="_blank" rel="noreferrer" className="bg-[#25D366] text-white font-bold py-3 text-xs rounded-full w-full text-center"><ThemeIcon icon="chat" className="w-4 h-4 inline-block shrink-0" /> WhatsApp İletişim</a>
                  <button onClick={() => { setIsMobileMenuOpen(false); setIsLeadModalOpen(true); }} className="bg-[#B89B5E] text-white font-bold py-3 text-xs rounded-full w-full text-center"><ThemeIcon icon="crown" className="w-4 h-4 inline-block shrink-0" /> Ücretsiz Fiyat Teklifi Al</button>
                </div>
              </div>
            )}
          </header>

          <LeadModal isOpen={isLeadModalOpen} onClose={() => setIsLeadModalOpen(false)} />
        </>
      );
    }

"""
    content = content[:start_idx] + new_navbar_code + content[end_idx:]
    print("Successfully replaced PublicNavbar component!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
