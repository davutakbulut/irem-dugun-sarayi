import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update PublicNavbar to render fixed dynamic header with white transparent overlay when not scrolled
old_public_navbar = """    function PublicNavbar({ currentRoute = '/', navigateTo }) {
      const [isScrolled, setIsScrolled] = useState(false);
      const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
      const [isLeadModalOpen, setIsLeadModalOpen] = useState(false);

      useEffect(() => {
        const handleScroll = () => setIsScrolled(window.scrollY > 40);
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
      }, []);

      const navLinks = [
        { label: 'ANASAYFA', route: '/' },
        { label: 'SALONLARIMIZ', route: '/salonlar' },
        { label: '360° SANAL TUR', route: '/360-tur' },
        { label: 'ORGANİZASYONLAR', route: '/organizasyonlar' },
        { label: 'MEDYA & VİDEOLAR', route: '/videolar' },
        { label: 'BLOG', route: '/blog' },
        { label: 'HAKKIMIZDA', route: '/hakkimizda' },
        { label: 'İLETİŞİM', route: '/iletisim' }
      ];

      const handleNavClick = (e, route) => {
        if (e) e.preventDefault();
        setIsMobileMenuOpen(false);
        if (navigateTo) navigateTo(route);
        else window.location.href = route;
      };

      return (
        <>
          {/* TOP MINI INFO BAR (EZODAVET TOP ANNOUNCEMENT BAR) */}
          <div className="bg-[#FAF6F0] border-b border-amber-200/60 text-slate-700 text-[11px] py-2 px-4 hidden sm:block">
            <div className="max-w-7xl mx-auto flex justify-between items-center font-medium">
              <div className="flex items-center space-x-6">
                <span><ThemeIcon icon="location" className="w-4 h-4 inline-block shrink-0" /> Sapanca Göl Kenarı Caddesi No:42 Sakarya</span>
                <span><ThemeIcon icon="phone" className="w-4 h-4 inline-block shrink-0" /> <a href="tel:+905471440054" className="hover:text-[#B89B5E] font-bold">+90 547 144 00 54</a></span>
                <span><ThemeIcon icon="chat" className="w-4 h-4 inline-block shrink-0" /> <a href="https://wa.me/905471440054" target="_blank" rel="noreferrer" className="text-emerald-600 font-bold hover:underline">WhatsApp: +90 547 144 00 54</a></span>
              </div>
              <div className="flex items-center space-x-4 text-[#B89B5E] font-bold">
                <span><ThemeIcon icon="crown" className="w-4 h-4 inline-block shrink-0" /> Sakarya'nın En Çok Tercih Edilen Balo & Davet Tesisleri</span>
              </div>
            </div>
          </div>

          <header className={`sticky top-0 z-40 transition-all duration-300 ${isScrolled ? 'bg-white/95 backdrop-blur-md shadow-md border-b border-amber-100 py-3' : 'bg-white border-b border-slate-100 py-4'}`}>
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between">
              {/* EZO DAVET STYLE LOGO */}
              <a href="/" onClick={(e) => handleNavClick(e, '/')} className="flex items-center space-x-3 cursor-pointer group">
                <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-[#B89B5E] to-[#ceb992] flex items-center justify-center text-white font-serif font-black text-2xl shadow-md group-hover:scale-105 transition-transform"><ThemeIcon icon="venue" className="w-4 h-4 inline-block shrink-0" /></div>
                <div>
                  <h1 className="font-serif font-bold text-lg sm:text-xl text-slate-900 tracking-wide leading-none">İREM DÜĞÜN SARAYI</h1>
                  <p className="text-[9px] font-bold text-[#B89B5E] tracking-widest uppercase mt-1">Balo & Davet Tesisleri</p>
                </div>
              </a>

              {/* CENTER NAV LINKS */}
              <nav className="hidden lg:flex items-center space-x-6">
                {navLinks.map(link => (
                  <a
                    key={link.route}
                    href={link.route}
                    onClick={(e) => handleNavClick(e, link.route)}
                    className={`text-xs font-bold transition-colors cursor-pointer py-1 ${currentRoute === link.route ? 'text-[#B89B5E] border-b-2 border-[#B89B5E]' : 'text-slate-700 hover:text-[#B89B5E]'}`}
                  >
                    {link.label}
                  </a>
                ))}
              </nav>

              {/* RIGHT CTA BUTTONS */}
              <div className="hidden sm:flex items-center space-x-3">
                <a href="https://wa.me/905471440054" target="_blank" rel="noreferrer" className="bg-[#25D366] hover:bg-[#20bd5a] text-white font-bold text-xs px-4 py-2.5 rounded-full shadow transition flex items-center space-x-1.5">
                  <span><ThemeIcon icon="chat" className="w-4 h-4 inline-block shrink-0" /></span><span>WhatsApp</span>
                </a>
                <button onClick={() => setIsLeadModalOpen(true)} className="bg-[#B89B5E] hover:bg-[#a3874e] text-white font-bold text-xs px-5 py-2.5 rounded-full shadow transition cursor-pointer flex items-center space-x-1.5">
                  <span><ThemeIcon icon="crown" className="w-4 h-4 inline-block shrink-0" /></span><span>Teklif Alın</span>
                </button>
              </div>

              {/* MOBILE TOGGLE */}
              <div className="flex lg:hidden items-center space-x-2">
                <button onClick={() => setIsLeadModalOpen(true)} className="bg-[#B89B5E] text-white font-bold text-xs px-3.5 py-2 rounded-full shadow">Teklif Al</button>
                <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="w-10 h-10 rounded-xl bg-slate-100 text-slate-800 font-bold text-lg flex items-center justify-center cursor-pointer">
                  {isMobileMenuOpen ? '✕' : '☰'}
                </button>
              </div>
            </div>

            {/* MOBILE DRAWER */}
            {isMobileMenuOpen && (
              <div className="lg:hidden bg-white border-b border-slate-200 p-6 space-y-3 shadow-xl animate-fade-in">
                {navLinks.map(link => (
                  <a key={link.route} href={link.route} onClick={(e) => handleNavClick(e, link.route)} className={`w-full text-left px-4 py-3 rounded-xl text-xs font-bold flex justify-between items-center ${currentRoute === link.route ? 'bg-[#faf8f5] text-[#B89B5E]' : 'text-slate-700 hover:bg-slate-50'}`}>
                    <span>{link.label}</span>
                  </a>
                ))}
                <div className="pt-4 border-t border-slate-100 flex flex-col gap-2">
                  <a href="https://wa.me/905471440054" target="_blank" rel="noreferrer" className="bg-[#25D366] text-white font-bold py-3 text-xs rounded-full w-full text-center"><ThemeIcon icon="chat" className="w-4 h-4 inline-block shrink-0" /> WhatsApp İletişim</a>
                  <button onClick={() => { setIsMobileMenuOpen(false); setIsLeadModalOpen(true); }} className="bg-[#B89B5E] text-white font-bold py-3 text-xs rounded-full w-full text-center"><ThemeIcon icon="crown" className="w-4 h-4 inline-block shrink-0" /> Ücretsiz Fiyat Teklifi Al</button>
                </div>
              </div>
            )}
          </header>

          <LeadModal isOpen={isLeadModalOpen} onClose={() => setIsLeadModalOpen(false)} />
        </>
      );
    }"""

new_public_navbar = """    function PublicNavbar({ currentRoute = '/', navigateTo }) {
      const [isScrolled, setIsScrolled] = useState(false);
      const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
      const [isLeadModalOpen, setIsLeadModalOpen] = useState(false);
      const isHomePage = currentRoute === '/';

      useEffect(() => {
        const handleScroll = () => setIsScrolled(window.scrollY > 50);
        window.addEventListener('scroll', handleScroll, { passive: true });
        handleScroll();
        return () => window.removeEventListener('scroll', handleScroll);
      }, []);

      const navLinks = [
        { label: 'ANASAYFA', route: '/' },
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
              {/* EZO & SVADBA STYLE LOGO */}
              <a href="/" onClick={(e) => handleNavClick(e, '/')} className="flex items-center space-x-3 cursor-pointer group">
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center font-serif font-black text-2xl shadow-md group-hover:scale-105 transition-all duration-300 ${
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
                    isTransparentMode ? 'text-amber-300/90' : 'text-[#B89B5E] dark:text-gold-400'
                  }`}>
                    Balo & Davet Tesisleri
                  </p>
                </div>
              </a>

              {/* CENTER NAV LINKS */}
              <nav className="hidden lg:flex items-center space-x-7">
                {navLinks.map(link => {
                  const isActive = currentRoute === link.route;
                  return (
                    <a
                      key={link.route}
                      href={link.route}
                      onClick={(e) => handleNavClick(e, link.route)}
                      className={`text-xs font-extrabold transition-all duration-300 cursor-pointer py-1 uppercase tracking-wider ${
                        isTransparentMode
                          ? (isActive ? 'text-amber-300 border-b-2 border-amber-300' : 'text-white hover:text-amber-300 drop-shadow-md')
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
                  className={`font-bold text-xs px-4 py-2.5 rounded-full shadow transition-all duration-300 flex items-center space-x-1.5 ${
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
                  className="bg-[#B89B5E] hover:bg-[#a3874e] text-white font-bold text-xs px-5 py-2.5 rounded-full shadow-lg transition-transform hover:scale-105 cursor-pointer flex items-center space-x-1.5"
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
    }"""

if old_public_navbar in content:
    content = content.replace(old_public_navbar, new_public_navbar, 1)
    print("1. Replaced PublicNavbar with dynamic transparent/scrolled transition!")
else:
    print("WARNING: Could not find old_public_navbar in index.html!")

# 2. Update HomePage to start with full-screen video background
old_home_page = """    function HomePage({ navigateTo }) {
      const [isLeadModalOpen, setIsLeadModalOpen] = useState(false);

      return (
        <div className="space-y-24 pb-20 bg-white">
          {/* 1. HERO BANNER BÖLÜMÜ (EZODAVET SINEMATİK BEYAZ & ALTIN BANNER) */}
          <div className="relative bg-gradient-to-b from-[#faf8f5] via-[#fcfbf9] to-white py-20 sm:py-28 px-4 text-center border-b border-amber-100/60 overflow-hidden">
            <div className="max-w-4xl mx-auto space-y-6 relative z-10">
              <div className="w-16 h-16 mx-auto rounded-full bg-[#B89B5E]/10 border border-[#B89B5E]/30 flex items-center justify-center text-2xl text-[#B89B5E] shadow-sm"><ThemeIcon icon="crown" className="w-4 h-4 inline-block shrink-0" /></div>
              <div className="text-xs font-bold text-[#B89B5E] tracking-widest uppercase bg-[#B89B5E]/10 inline-block px-4 py-1.5 rounded-full">
                İrem Düğün Sarayı • Sakarya Sapanca
              </div>
              <h1 className="text-4xl sm:text-6xl font-serif font-extrabold text-slate-900 tracking-tight leading-tight">
                Sakarya Balo & Davet Salonu
              </h1>
              <p className="text-slate-600 max-w-2xl mx-auto text-sm sm:text-base leading-relaxed font-normal">
                Özel günlerinizde ayrıcalıklı ve kaliteli salonlarımız ile organizasyonlarınızı gerçekleştiriyoruz. Düğün, kına, sünnet ve tüm özel davetlerinizi özenle yönetiyoruz.
              </p>
              <div className="pt-4 flex flex-wrap justify-center gap-4">
                <a href="https://wa.me/905471440054" target="_blank" rel="noreferrer" className="bg-[#25D366] hover:bg-[#20bd5a] text-white font-bold px-8 py-3.5 rounded-full text-xs shadow-md transition cursor-pointer flex items-center space-x-2">
                  <span><ThemeIcon icon="chat" className="w-4 h-4 inline-block shrink-0" /></span><span>WhatsApp İletişim</span>
                </a>
                <button onClick={() => setIsLeadModalOpen(true)} className="bg-[#B89B5E] hover:bg-[#a3874e] text-white font-bold px-8 py-3.5 rounded-full text-xs shadow-md transition cursor-pointer flex items-center space-x-2">
                  <span><ThemeIcon icon="crown" className="w-4 h-4 inline-block shrink-0" /></span><span>Ücretsiz Fiyat Teklifi Al</span>
                </button>
              </div>
            </div>

            {/* FOTO GALERİ SHOWCASE GRID (EZODAVET 5'Lİ FOTO GRID) */}
            <div className="max-w-6xl mx-auto mt-14 grid grid-cols-2 md:grid-cols-5 gap-4 px-4">
              <img src="https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=500&q=80" alt="İrem Düğün Sarayı" className="w-full h-44 object-cover rounded-2xl shadow-md border-2 border-white hover:scale-105 transition duration-300" />
              <img src="https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=500&q=80" alt="İrem Düğün Sarayı" className="w-full h-44 object-cover rounded-2xl shadow-md border-2 border-white hover:scale-105 transition duration-300" />
              <img src="https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&w=500&q=80" alt="İrem Düğün Sarayı" className="w-full h-44 object-cover rounded-2xl shadow-sm border-2 border-white hover:scale-105 transition duration-300" />
              <img src="https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?auto=format&fit=crop&w=500&q=80" alt="İrem Düğün Sarayı" className="w-full h-44 object-cover rounded-2xl shadow-sm border-2 border-white hover:scale-105 transition duration-300" />
              <img src="https://images.unsplash.com/photo-1520854221256-17451cc331bf?auto=format&fit=crop&w=500&q=80" alt="İrem Düğün Sarayı" className="w-full h-44 object-cover rounded-2xl shadow-sm border-2 border-white hover:scale-105 transition duration-300" />
            </div>
          </div>"""

new_home_page = """    function HomePage({ navigateTo }) {
      const [isLeadModalOpen, setIsLeadModalOpen] = useState(false);

      return (
        <div className="space-y-24 pb-20 bg-white">
          {/* 1. FULLSCREEN VIDEO HERO HERO BÖLÜMÜ (SVADBA DAVET BİREBİR TAM EKRAN VİDEO ARKA PLAN) */}
          <div className="relative w-full h-screen min-h-[100vh] overflow-hidden flex items-center justify-center">
            <video
              autoPlay
              loop
              muted
              playsInline
              className="absolute inset-0 w-full h-full object-cover scale-105 pointer-events-none"
              src="https://cdn.creafolks.com/svadba-davet/9e9fee9d-dc11-4bd5-bc7a-4614de2d7e2b.mp4"
            />
            {/* Soft Dark Vignette Overlay for Crisp White Text Contrast */}
            <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-black/40 to-black/70 backdrop-blur-[0.5px]" />

            {/* Centered Hero Content */}
            <div className="relative z-10 text-center text-white px-4 max-w-4xl space-y-6 animate-fade-in">
              <div className="w-14 h-14 sm:w-16 sm:h-16 mx-auto rounded-full bg-white/10 backdrop-blur-md border border-white/30 flex items-center justify-center text-2xl text-amber-300 shadow-2xl animate-pulse">
                <ThemeIcon icon="crown" className="w-7 h-7 sm:w-8 sm:h-8 text-amber-300 shrink-0" />
              </div>

              <div className="space-y-3">
                <h1 className="text-3xl sm:text-6xl md:text-7xl font-serif font-extrabold tracking-widest uppercase text-white drop-shadow-[0_10px_35px_rgba(0,0,0,0.8)]">
                  İREM DÜĞÜN SARAYI
                </h1>
                <p className="text-base sm:text-2xl md:text-3xl font-serif italic text-amber-200/95 font-light tracking-wide drop-shadow-md">
                  Türkiye'nin & Sakarya'nın Düğün Mekanları
                </p>
              </div>

              <p className="text-xs sm:text-base text-slate-200/90 max-w-2xl mx-auto leading-relaxed font-medium drop-shadow-sm hidden sm:block">
                Sapanca Göl kıyısında 4 farklı saray konseptli balo salonumuz ve kır bahçemiz ile hayallerinizdeki düğünü taçlandırıyoruz.
              </p>

              <div className="pt-6 flex flex-wrap justify-center gap-4">
                <button 
                  onClick={() => setIsLeadModalOpen(true)} 
                  className="bg-[#B89B5E] hover:bg-[#a3874e] text-white font-extrabold px-8 py-4 rounded-full text-xs shadow-2xl transition-all duration-300 hover:scale-105 flex items-center space-x-2.5 cursor-pointer uppercase tracking-wider"
                >
                  <span><ThemeIcon icon="crown" className="w-4 h-4 inline-block shrink-0" /></span>
                  <span>ÜCRETSİZ FİYAT TEKLİFİ ALIN</span>
                </button>
                <a 
                  href="https://wa.me/905471440054" 
                  target="_blank" 
                  rel="noreferrer" 
                  className="bg-white/20 hover:bg-white/30 text-white backdrop-blur-md border border-white/40 font-extrabold px-8 py-4 rounded-full text-xs shadow-xl transition-all duration-300 hover:scale-105 flex items-center space-x-2.5 uppercase tracking-wider"
                >
                  <span><ThemeIcon icon="chat" className="w-4 h-4 inline-block shrink-0 text-emerald-400" /></span>
                  <span>WHATSAPP İLETİŞİM</span>
                </a>
              </div>
            </div>

            {/* Scroll Down Indicator */}
            <div 
              onClick={() => window.scrollTo({ top: window.innerHeight - 70, behavior: 'smooth' })}
              className="absolute bottom-8 left-1/2 -translate-x-1/2 z-10 text-white/80 animate-bounce flex flex-col items-center cursor-pointer group"
            >
              <span className="text-[10px] font-extrabold tracking-widest uppercase mb-1 group-hover:text-amber-300 transition-colors">AŞAĞI KAYDIRIN</span>
              <span className="text-2xl">↓</span>
            </div>
          </div>"""

if old_home_page in content:
    content = content.replace(old_home_page, new_home_page, 1)
    print("2. Replaced HomePage top hero section with full-screen video background!")
else:
    print("WARNING: Could not find old_home_page in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
