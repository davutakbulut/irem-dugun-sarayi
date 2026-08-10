import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = "    // ISOLATED BLOCK ERROR BOUNDARY (SINGLE BLOCK FAULT ISOLATION)"
end_marker = "    function HallsPage({ navigateTo }) {"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

print(f"start_idx: {start_idx}, end_idx: {end_idx}")

if start_idx != -1 and end_idx != -1:
    clean_code = """    // ISOLATED BLOCK ERROR BOUNDARY (SINGLE BLOCK FAULT ISOLATION)
    class BlockErrorBoundary extends React.Component {
      constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
      }
      static getDerivedStateFromError(error) {
        return { hasError: true, error };
      }
      componentDidCatch(error, errorInfo) {
        console.warn(`[PublicBlock:${this.props.blockName || 'Block'}] Error isolated:`, error, errorInfo);
      }
      render() {
        if (this.state.hasError) {
          return this.props.fallback || (
            <div className="w-full p-4 my-2 rounded-2xl bg-amber-500/5 border border-amber-500/20 text-center text-xs text-slate-500">
              <span>⚠️ {this.props.blockName || 'Bu Modül'} geçici olarak gösterilemiyor.</span>
            </div>
          );
        }
        return this.props.children;
      }
    }

    // 1. PUBLIC NAVBAR MODULE
    function PublicNavbar({ currentRoute = '/', navigateTo }) {
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
              {/* LOGO */}
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

              {/* CENTER NAV LINKS */}
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

    // 2. PUBLIC FOOTER MODULE (1:1 REPLICA WHATSAPP POPUP SUPPORT WIDGET)
    function PublicFooter({ navigateTo }) {
      const [isWhatsAppWidgetOpen, setIsWhatsAppWidgetOpen] = useState(false);

      const handleFooterClick = (e, route) => {
        if (e) e.preventDefault();
        if (navigateTo) navigateTo(route);
        else window.location.href = route;
      };

      return (
        <footer className="bg-[#faf8f5] border-t border-amber-200/60 text-slate-600 text-xs pt-16 pb-12 px-4 relative overflow-hidden">
          <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-10 pb-12 border-b border-amber-200/40">
            <div className="space-y-4 md:col-span-1">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 rounded-xl bg-[#B89B5E] flex items-center justify-center text-white font-serif font-black text-xl shadow"><ThemeIcon icon="venue" className="w-4 h-4 inline-block shrink-0" /></div>
                <h3 className="text-slate-900 font-serif font-bold text-lg">İrem Düğün Sarayı</h3>
              </div>
              <p className="text-xs text-slate-500 leading-relaxed">Sapanca Gölünün kıyısında 4 farklı balo salonu, kır bahçesi ve VIP organizasyon hizmetleri ile en özel gününüzü taçlandırıyoruz.</p>
              <div className="flex space-x-3 text-base">
                <a href="https://instagram.com" target="_blank" rel="noreferrer" className="w-9 h-9 rounded-full bg-white border border-amber-200 flex items-center justify-center text-[#B89B5E] hover:bg-[#B89B5E] hover:text-white transition"><ThemeIcon icon="camera" className="w-4 h-4 inline-block shrink-0" /></a>
                <a href="https://facebook.com" target="_blank" rel="noreferrer" className="w-9 h-9 rounded-full bg-white border border-amber-200 flex items-center justify-center text-[#B89B5E] hover:bg-[#B89B5E] hover:text-white transition"><ThemeIcon icon="user" className="w-4 h-4 inline-block shrink-0" /></a>
                <a href="https://youtube.com" target="_blank" rel="noreferrer" className="w-9 h-9 rounded-full bg-white border border-amber-200 flex items-center justify-center text-[#B89B5E] hover:bg-[#B89B5E] hover:text-white transition"><ThemeIcon icon="video" className="w-4 h-4 inline-block shrink-0" /></a>
                <button type="button" onClick={() => setIsWhatsAppWidgetOpen(prev => !prev)} className="w-9 h-9 rounded-full bg-white border border-amber-200 flex items-center justify-center text-[#25D366] hover:bg-[#25D366] hover:text-white transition cursor-pointer"><ThemeIcon icon="chat" className="w-4 h-4 inline-block shrink-0" /></button>
              </div>
            </div>

            <div className="space-y-3">
              <h4 className="text-slate-900 font-bold text-sm tracking-wider uppercase border-l-2 border-[#B89B5E] pl-2">Hızlı Menü</h4>
              <ul className="space-y-2 text-slate-600 text-xs">
                <li><a href="/" className="hover:text-[#B89B5E] transition" onClick={(e) => handleFooterClick(e, '/')}>Anasayfa</a></li>
                <li><a href="/salonlar" className="hover:text-[#B89B5E] transition" onClick={(e) => handleFooterClick(e, '/salonlar')}>Salonlarımız</a></li>
                <li><a href="/360-tur" className="hover:text-[#B89B5E] transition" onClick={(e) => handleFooterClick(e, '/360-tur')}>360° Sanal Tur</a></li>
                <li><a href="/organizasyonlar" className="hover:text-[#B89B5E] transition" onClick={(e) => handleFooterClick(e, '/organizasyonlar')}>Organizasyon Paketleri</a></li>
                <li><a href="/videolar" className="hover:text-[#B89B5E] transition" onClick={(e) => handleFooterClick(e, '/videolar')}>Galeri & Fotoğraflar</a></li>
              </ul>
            </div>

            <div className="space-y-3">
              <h4 className="text-slate-900 font-bold text-sm tracking-wider uppercase border-l-2 border-[#B89B5E] pl-2">Düğün Rehberi</h4>
              <ul className="space-y-2 text-slate-600 text-xs">
                <li><a href="/blog" className="hover:text-[#B89B5E] transition" onClick={(e) => handleFooterClick(e, '/blog')}>Düğün Tarihi Seçim İpuçları</a></li>
                <li><a href="/blog" className="hover:text-[#B89B5E] transition" onClick={(e) => handleFooterClick(e, '/blog')}>Gelinlik & Damatlık Rehberi</a></li>
                <li><a href="/hakkimizda" className="hover:text-[#B89B5E] transition" onClick={(e) => handleFooterClick(e, '/hakkimizda')}>Hakkımızda & Kalite Belgelerimiz</a></li>
                <li><a href="/musteri-giris" className="hover:text-[#B89B5E] transition" onClick={(e) => handleFooterClick(e, '/musteri-giris')}>Müşteri VIP Portalı</a></li>
              </ul>
            </div>

            <div className="space-y-3">
              <h4 className="text-slate-900 font-bold text-sm tracking-wider uppercase border-l-2 border-[#B89B5E] pl-2">İletişim & Konum</h4>
              <p className="text-xs text-slate-700 leading-relaxed"><ThemeIcon icon="location" className="w-4 h-4 inline-block shrink-0" /> Sapanca Göl Kenarı Caddesi No:42 Sakarya / Turkey</p>
              <p className="text-xs text-[#B89B5E] font-mono font-bold"><ThemeIcon icon="phone" className="w-4 h-4 inline-block shrink-0" /> <a href="tel:+905471440054" className="hover:underline">+90 547 144 00 54</a></p>
              <p className="text-xs text-emerald-600 font-mono font-bold cursor-pointer" onClick={() => setIsWhatsAppWidgetOpen(prev => !prev)}><ThemeIcon icon="chat" className="w-4 h-4 inline-block shrink-0" /> <span className="hover:underline">WhatsApp: +90 547 144 00 54</span></p>
              <p className="text-xs text-slate-700 font-mono font-bold"><ThemeIcon icon="email" className="w-4 h-4 inline-block shrink-0" /> <a href="mailto:irem.wedding@gmail.com" className="hover:underline">irem.wedding@gmail.com</a></p>
              <p className="text-[11px] text-slate-500">Çalışma Saatleri: 09:00 - 23:00 (Haftanın 7 Günü)</p>
            </div>
          </div>

          <div className="max-w-7xl mx-auto pt-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px] text-slate-500">
            <div>© 2026 İrem Düğün Sarayı & Balo Tesisleri. Tüm Hakları Saklıdır.</div>
            <div className="flex space-x-4">
              <a href="/yonetim" className="hover:underline cursor-pointer">Tesis Yöneticisi Girişi <ThemeIcon icon="lock" className="w-4 h-4 inline-block shrink-0" /></a>
            </div>
          </div>

          {/* FLOATING ACTION BUTTONS */}
          <a 
            href="tel:+905471440054" 
            className="fixed bottom-6 left-6 z-50 bg-[#B89B5E] hover:bg-[#a3874e] text-white w-14 h-14 rounded-full flex items-center justify-center shadow-2xl hover:scale-105 transition cursor-pointer border-2 border-white"
            title="Bizi Arayın"
          >
            <ThemeIcon icon="phone" className="w-5 h-5 inline-block shrink-0 text-white" />
          </a>

          {/* FLOATING WHATSAPP TRIGGER BUTTON */}
          <button 
            type="button"
            onClick={() => setIsWhatsAppWidgetOpen(prev => !prev)}
            className="fixed bottom-6 right-6 z-50 bg-[#25D366] hover:bg-[#20bd5a] text-white w-14 h-14 rounded-full flex items-center justify-center shadow-2xl hover:scale-110 transition-transform cursor-pointer border-2 border-white"
            title="WhatsApp Destek"
            aria-label="WhatsApp Destek Hattı"
          >
            <ThemeIcon icon="chat" className="w-7 h-7 inline-block shrink-0 text-white" />
          </button>

          {/* INTERACTIVE WHATSAPP SUPPORT WIDGET CARD (EXACT REPLICA MATCHING REFERENCE IMAGE) */}
          {isWhatsAppWidgetOpen && (
            <div className="fixed bottom-24 right-4 sm:right-6 z-50 w-[calc(100vw-2rem)] sm:w-[340px] max-w-sm bg-white rounded-[24px] shadow-[0_20px_50px_rgba(0,0,0,0.18)] border border-slate-100/80 overflow-hidden animate-fade-in text-slate-800">
              {/* VIBRANT GREEN TOP HEADER BAR */}
              <div className="bg-[#25D366] px-5 py-4 flex items-center justify-between text-white shadow-xs">
                <h3 className="font-heading font-extrabold text-lg sm:text-xl tracking-tight text-white">
                  WhatsApp Destek
                </h3>
                <button
                  type="button"
                  onClick={() => setIsWhatsAppWidgetOpen(false)}
                  className="text-white hover:opacity-80 text-xl font-bold transition cursor-pointer p-1 leading-none"
                  title="Kapat"
                  aria-label="Kapat"
                >
                  ✕
                </button>
              </div>

              {/* CARD BODY CONTENT */}
              <div className="p-5 space-y-4 bg-white">
                <p className="text-sm sm:text-[15px] text-slate-700 font-medium text-left leading-snug">
                  <span className="font-bold text-slate-900">Merhaba!</span> Size nasıl yardımcı olabiliriz?
                </p>

                {/* NUMBER 1: HIZLI RANDEVU! */}
                <a
                  href="https://wa.me/905471440054?text=Merhaba,%20d%C3%BC%C4%9F%C3%BCn%20ve%20organizasyon%20i%C3%A7in%20h%C4%B1zl%C4%B1%20randevu%20olusturmak%20istiyorum."
                  target="_blank"
                  rel="noreferrer"
                  className="p-3.5 sm:p-4 bg-[#F8F9FA] hover:bg-[#F0F2F5] rounded-[20px] transition-all duration-200 flex items-center space-x-4 group cursor-pointer border border-transparent hover:border-slate-200"
                >
                  <div className="w-12 h-12 sm:w-13 sm:h-13 rounded-full bg-[#25D366] text-white flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform shadow-xs">
                    <svg className="w-6 h-6 sm:w-7 sm:h-7 text-white fill-current" viewBox="0 0 24 24">
                      <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/>
                    </svg>
                  </div>
                  <div className="flex-1 min-w-0 text-left">
                    <div className="font-extrabold text-base sm:text-lg text-slate-900 group-hover:text-[#25D366] transition-colors leading-tight">
                      Hızlı Randevu!
                    </div>
                    <div className="text-xs font-semibold text-slate-500 mt-0.5">
                      İletişime Geç
                    </div>
                  </div>
                </a>

                {/* NUMBER 2: BİLGİ AL! */}
                <a
                  href="https://wa.me/905471440054?text=Merhaba,%20d%C3%BC%C4%9F%C3%BCn%20salonlar%C4%B1n%C4%B1z,%20men%C3%BCler%20ve%20fiyatlar%20hakk%C4%B1nda%20bilgi%20almak%20istiyorum."
                  target="_blank"
                  rel="noreferrer"
                  className="p-3.5 sm:p-4 bg-[#F8F9FA] hover:bg-[#F0F2F5] rounded-[20px] transition-all duration-200 flex items-center space-x-4 group cursor-pointer border border-transparent hover:border-slate-200"
                >
                  <div className="w-12 h-12 sm:w-13 sm:h-13 rounded-full bg-[#25D366] text-white flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform shadow-xs">
                    <svg className="w-6 h-6 sm:w-7 sm:h-7 text-white fill-current" viewBox="0 0 24 24">
                      <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/>
                    </svg>
                  </div>
                  <div className="flex-1 min-w-0 text-left">
                    <div className="font-extrabold text-base sm:text-lg text-slate-900 group-hover:text-[#25D366] transition-colors leading-tight">
                      Bilgi Al!
                    </div>
                    <div className="text-xs font-semibold text-slate-500 mt-0.5">
                      İletişime Geç
                    </div>
                  </div>
                </a>
              </div>
            </div>
          )}
        </footer>
      );
    }

    // 3. PUBLIC LAYOUT MODULE (ISOLATED NAVBAR & FOOTER BLOCKS)
    function PublicLayout({ children, currentRoute = '/', navigateTo }) {
      return (
        <div className="min-h-screen bg-white text-slate-800 font-sans relative flex flex-col justify-between overflow-x-hidden">
          <BlockErrorBoundary blockName="Üst Navigasyon (Header)">
            <PublicNavbar currentRoute={currentRoute} navigateTo={navigateTo} />
          </BlockErrorBoundary>

          <main className="flex-1 w-full">
            {children}
          </main>

          <BlockErrorBoundary blockName="Alt Footer & WhatsApp Destek">
            <PublicFooter navigateTo={navigateTo} />
          </BlockErrorBoundary>
        </div>
      );
    }

    // 4. MODULAR PAGE BLOCKS (INDEPENDENT FAULT ISOLATED PUBLIC SECTIONS)
    function PublicHeroBlock({ onOpenLeadModal }) {
      return (
        <div className="relative w-full h-screen min-h-[100vh] overflow-hidden flex items-center justify-center">
          <video
            autoPlay
            loop
            muted
            playsInline
            className="absolute inset-0 w-full h-full object-cover scale-105 pointer-events-none"
            src="https://cdn.creafolks.com/svadba-davet/9e9fee9d-dc11-4bd5-bc7a-4614de2d7e2b.mp4"
          />
          <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-black/40 to-black/70 backdrop-blur-[0.5px]" />

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
                onClick={onOpenLeadModal} 
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

          <div 
            onClick={() => window.scrollTo({ top: window.innerHeight - 70, behavior: 'smooth' })}
            className="absolute bottom-8 sm:bottom-10 left-0 right-0 z-20 text-white/90 animate-bounce flex flex-col items-center justify-center text-center cursor-pointer group pointer-events-auto mx-auto w-full px-4"
          >
            <span className="text-[10px] sm:text-xs font-black tracking-[0.25em] uppercase mb-1 group-hover:text-amber-300 transition-colors text-center w-full block drop-shadow-md">AŞAĞI KAYDIRIN</span>
            <span className="text-2xl font-bold leading-none drop-shadow-md">↓</span>
          </div>
        </div>
      );
    }

    function PublicWelcomeBlock({ navigateTo }) {
      return (
        <div className="max-w-7xl mx-auto px-4 grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          <div className="relative rounded-3xl overflow-hidden shadow-2xl border-4 border-amber-100">
            <img src="https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80" alt="İrem Düğün Sarayı" className="w-full h-[420px] object-cover" />
          </div>
          <div className="space-y-6">
            <span className="text-xs font-bold text-[#B89B5E] tracking-widest uppercase border-b-2 border-[#B89B5E] pb-1">İrem Düğün Sarayı Sakarya</span>
            <h2 className="text-3xl sm:text-4xl font-serif font-extrabold text-slate-900 leading-snug">İrem Düğün Sarayı’na Hoşgeldiniz...</h2>
            <p className="text-slate-600 text-sm leading-relaxed">
              İrem Düğün Sarayı, Sapanca Gölünün kıyısında konumlanan; şıklığı, konforu ve profesyonel hizmet anlayışını bir araya getiren seçkin bir davet ve organizasyon merkezidir. En özel anlarınızı unutulmaz kılmak için tasarlanan mekanımız, tamamı göl manzarasına sahip üç farklı salon seçeneği ile her davete eşsiz bir atmosfer sunar.
            </p>
            <p className="text-slate-600 text-sm leading-relaxed">
              Düğün, nişan, kına gecesi, sünnet, özel kutlamalar ve kurumsal davetler için farklı konsept alternatifleri sunan İrem Düğün Sarayı; otel konseptinden kır düğününe kadar uzanan geniş organizasyon yelpazesiyle hayallerinizi gerçeğe dönüştürür.
            </p>
            <div className="pt-2">
              <a href="/salonlar" onClick={(e) => { e.preventDefault(); if (navigateTo) navigateTo('/salonlar'); }} className="inline-block bg-[#B89B5E] hover:bg-[#a3874e] text-white font-bold px-8 py-3.5 rounded-full text-xs shadow-md transition">
                Salonlarımızı İnceleyin →
              </a>
            </div>
          </div>
        </div>
      );
    }

    function PublicServicesBlock() {
      const services = [
        { title: 'Düğün Salonu', desc: 'Hayalinizdeki düğün için şık, konforlu ve özenle tasarlanmış salonlarımızı keşfedebilirsiniz.' },
        { title: 'Nişan Organizasyonu', desc: 'Nişan organizasyonlarınız için zarif detaylarla hazırlanmış özel salonlarımızı inceleyebilirsiniz.' },
        { title: 'Sünnet Düğünü', desc: 'Sünnet düğünleri için ferah, modern ve ailelere uygun salon seçeneklerimizi keşfedebilirsiniz.' },
        { title: 'Kır Düğünü', desc: 'Doğayla iç içe, romantik ve unutulmaz kır düğünleri için özel alanlarımızı inceleyebilirsiniz.' },
        { title: 'Dönemsel Organizasyonlar', desc: 'Özel günler ve sezonluk organizasyonlar için profesyonelce hazırlanmış salonlarımızı keşfedebilirsiniz.' },
        { title: 'Mezuniyet Kutlaması', desc: 'Mezuniyet gecelerinizi unutulmaz kılacak geniş ve özenle hazırlanmış salonlarımızı inceleyebilirsiniz.' },
        { title: 'Kurumsal Organizasyon', desc: 'Toplantı, davet ve kurumsal etkinlikler için prestijli ve fonksiyonel salonlarımızı inceleyebilirsiniz.' },
      ];

      return (
        <div className="bg-[#faf8f5] py-20 px-4 border-y border-amber-200/50">
          <div className="max-w-7xl mx-auto space-y-12">
            <div className="text-center space-y-3">
              <span className="text-xs font-bold text-[#B89B5E] tracking-widest uppercase">Ayrıcalıklı Konseptler</span>
              <h2 className="text-3xl font-serif font-extrabold text-slate-900">Organizasyon Hizmetlerimiz</h2>
              <p className="text-xs text-slate-500 max-w-xl mx-auto">Her davet türüne özel olarak dizayn edilmiş lüks salon ve organizasyon seçenekleri.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {services.map((item, idx) => (
                <div key={idx} className="bg-white p-8 rounded-3xl border border-amber-100 shadow-sm hover:shadow-xl transition-all duration-300 text-center space-y-4 hover:-translate-y-1">
                  <div className="w-14 h-14 mx-auto rounded-full bg-[#faf8f5] border border-amber-200 flex items-center justify-center text-[#B89B5E] text-2xl shadow-inner"><ThemeIcon icon="crown" className="w-4 h-4 inline-block shrink-0" /></div>
                  <h3 className="font-serif font-bold text-xl text-slate-900">{item.title}</h3>
                  <p className="text-xs text-slate-600 leading-relaxed">{item.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      );
    }

    function PublicHallsBlock({ navigateTo, onOpenLeadModal }) {
      const halls = [
        { name: 'Saray Balo', cap: '750 Kişi', desc: 'Geniş salonu ve göz alıcı dekorasyonuyla Saray Balo, lüks ve estetiği bir arada sunar. Özel günlerinizi prestijli ve şık bir atmosferde gerçekleştirmenizi sağlar.', img: 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=600&q=80' },
        { name: 'Safir Salon', cap: '500 Kişi', desc: 'Modern mimarisi ve şık tasarımıyla Safir Salon, zarif davetler için özel olarak hazırlanmıştır. Konforlu yapısı ve manzarasıyla kusursuz bir düğün deneyimi sunar.', img: 'https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=600&q=80' },
        { name: 'Kır Bahçesi', cap: '1000+ Kişi', desc: 'Göl manzarası ve ferah alanlarıyla Kır Bahçesi, açık hava konseptini şıklıkla buluşturur. Doğayla iç içe, keyifli ve unutulmaz davetler için ideal bir mekândır.', img: 'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&w=600&q=80' },
      ];

      return (
        <div className="max-w-7xl mx-auto px-4 space-y-12">
          <div className="text-center space-y-3">
            <span className="text-xs font-bold text-[#B89B5E] tracking-widest uppercase">İrem Düğün Sarayı</span>
            <h2 className="text-3xl sm:text-5xl font-serif font-extrabold text-slate-900">Sakarya Düğün Salonları</h2>
            <p className="text-xs text-slate-500 max-w-xl mx-auto">Sapanca Gölünün kıyısında kolonsuz yüksek tavan ferahlığıyla tasarlanmış balo salonlarımız.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {halls.map((hall, idx) => (
              <div key={idx} className="bg-white rounded-3xl overflow-hidden border border-amber-100 shadow-md hover:shadow-2xl transition duration-300 space-y-5 p-6 flex flex-col justify-between">
                <div className="space-y-4">
                  <div className="relative h-60 rounded-2xl overflow-hidden shadow-sm">
                    <img src={hall.img} alt={hall.name} className="w-full h-full object-cover" />
                    <div className="absolute top-3 right-3 bg-white/95 backdrop-blur-md text-[#B89B5E] font-bold text-xs px-3.5 py-1.5 rounded-full shadow border border-amber-200">
                      <ThemeIcon icon="users" className="w-4 h-4 inline-block shrink-0" /> {hall.cap}
                    </div>
                  </div>
                  <h3 className="font-serif font-bold text-2xl text-slate-900">{hall.name}</h3>
                  <p className="text-xs text-slate-600 leading-relaxed">{hall.desc}</p>
                </div>

                <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
                  <a href="/360-tur" onClick={(e) => { e.preventDefault(); if (navigateTo) navigateTo('/360-tur'); }} className="text-xs font-bold text-[#B89B5E] hover:underline flex items-center space-x-1">
                    <span><ThemeIcon icon="location" className="w-4 h-4 inline-block shrink-0" /></span><span>360° İnceleyin</span>
                  </a>
                  <button onClick={onOpenLeadModal} className="bg-[#B89B5E] hover:bg-[#a3874e] text-white px-5 py-2.5 rounded-full text-xs font-bold shadow transition cursor-pointer">
                    Teklif Alın
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      );
    }

    function PublicMenusBlock() {
      return (
        <div className="bg-[#faf8f5] py-16 px-4 border-y border-amber-200/50">
          <div className="max-w-7xl mx-auto space-y-10">
            <div className="text-center space-y-2">
              <span className="text-xs font-bold text-[#B89B5E] tracking-widest uppercase">Zengin Davet İkramları</span>
              <h2 className="text-3xl font-serif font-extrabold text-slate-900">Menülerimiz & VIP Lezzetler</h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="bg-white p-6 rounded-3xl border border-amber-100 shadow-sm space-y-3">
                <div className="text-[#B89B5E] font-bold text-sm flex items-center space-x-2">
                  <span><ThemeIcon icon="gift" className="w-4 h-4 inline-block shrink-0" /></span><span>Ordövr Tabağı</span>
                </div>
                <p className="text-xs text-slate-600 leading-relaxed">Zengin Türk ordövr tabağı, dana füme et şöleni, ezme, humus ve gurme peynir çeşitleri.</p>
              </div>
              <div className="bg-white p-6 rounded-3xl border border-amber-100 shadow-sm space-y-3">
                <div className="text-[#B89B5E] font-bold text-sm flex items-center space-x-2">
                  <span><ThemeIcon icon="gift" className="w-4 h-4 inline-block shrink-0" /></span><span>Ara Sıcaklar</span>
                </div>
                <p className="text-xs text-slate-600 leading-relaxed">Sıcak Paçanga böreği, fıstıklı içli köfte ve sebzeli krep ikramları.</p>
              </div>
              <div className="bg-white p-6 rounded-3xl border border-amber-100 shadow-sm space-y-3">
                <div className="text-[#B89B5E] font-bold text-sm flex items-center space-x-2">
                  <span><ThemeIcon icon="gift" className="w-4 h-4 inline-block shrink-0" /></span><span>Ana Yemek</span>
                </div>
                <p className="text-xs text-slate-600 leading-relaxed">Ağır ateşte pişmiş Kuzu Tandır veya Özel Soslu Dana Antrikot, iç pilav ile.</p>
              </div>
              <div className="bg-white p-6 rounded-3xl border border-amber-100 shadow-sm space-y-3">
                <div className="text-[#B89B5E] font-bold text-sm flex items-center space-x-2">
                  <span><ThemeIcon icon="gift" className="w-4 h-4 inline-block shrink-0" /></span><span>Düğün Pastası</span>
                </div>
                <p className="text-xs text-slate-600 leading-relaxed">5 Katlı şov düğün pastası, mevsim meyveleri tabağı ve meşrubat servisi.</p>
              </div>
            </div>
          </div>
        </div>
      );
    }

    function PublicTestimonialsBlock() {
      return (
        <div className="max-w-7xl mx-auto px-4 space-y-10">
          <div className="text-center space-y-2">
            <div className="text-amber-500 text-sm font-bold"><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /> (643 Doğrulanmış Değerlendirme)</div>
            <h2 className="text-3xl font-serif font-extrabold text-slate-900">Müşteri Yorumları</h2>
            <p className="text-xs text-slate-500">Google ve Düğün.com üzerinden gelen gerçek çift deneyimleri.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white border border-amber-100 p-8 rounded-3xl space-y-4 shadow-sm hover:shadow-md transition">
              <div className="flex items-center space-x-1 text-amber-500 text-sm"><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /></div>
              <p className="text-xs text-slate-600 leading-relaxed font-serif italic">"Sapanca göl kenarındaki Saray Balo salonunda 600 kişilik düğünümüz gerçekleşti. Yemek kalitesi ve garson ilgisi harikaydı!"</p>
              <div className="flex items-center justify-between pt-3 border-t border-slate-100 text-[11px]">
                <span className="font-bold text-slate-900">Ahmet & Zeynep Y.</span>
                <span className="text-emerald-600 font-bold">Google Doğrulanmış</span>
              </div>
            </div>

            <div className="bg-white border border-amber-100 p-8 rounded-3xl space-y-4 shadow-sm hover:shadow-md transition">
              <div className="flex items-center space-x-1 text-amber-500 text-sm"><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /></div>
              <p className="text-xs text-slate-600 leading-relaxed font-serif italic">"Kır bahçesindeki nişan organizasyonumuz masal gibiydi. Işıklandırma ve ses sistemleri son teknolojiydi. Emeği geçen herkese teşekkürler."</p>
              <div className="flex items-center justify-between pt-3 border-t border-slate-100 text-[11px]">
                <span className="font-bold text-slate-900">Burak & Selin K.</span>
                <span className="text-emerald-600 font-bold">Düğün.com Doğrulanmış</span>
              </div>
            </div>

            <div className="bg-white border border-amber-100 p-8 rounded-3xl space-y-4 shadow-sm hover:shadow-md transition">
              <div className="flex items-center space-x-1 text-amber-500 text-sm"><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /></div>
              <p className="text-xs text-slate-600 leading-relaxed font-serif italic">"Safir Salon'da yapılan sünnet organizasyonumuzda organizasyon koordinatörünün planlaması sayesinde sıfır aksamayla harika bir gece geçirdik."</p>
              <div className="flex items-center justify-between pt-3 border-t border-slate-100 text-[11px]">
                <span className="font-bold text-slate-900">Murat & Elif D.</span>
                <span className="text-emerald-600 font-bold">Google Doğrulanmış</span>
              </div>
            </div>
          </div>
        </div>
      );
    }

    // 5. MAIN HOMEPAGE ASSEMBLY WITH ISOLATED MODULAR BLOCKS
    function HomePage({ navigateTo }) {
      const [isLeadModalOpen, setIsLeadModalOpen] = useState(false);

      return (
        <div className="space-y-24 pb-20 bg-white">
          <BlockErrorBoundary blockName="Video Hero Header">
            <PublicHeroBlock onOpenLeadModal={() => setIsLeadModalOpen(true)} />
          </BlockErrorBoundary>

          <BlockErrorBoundary blockName="Hoşgeldiniz Alanı">
            <PublicWelcomeBlock navigateTo={navigateTo} />
          </BlockErrorBoundary>

          <BlockErrorBoundary blockName="Organizasyon Hizmetleri">
            <PublicServicesBlock />
          </BlockErrorBoundary>

          <BlockErrorBoundary blockName="Salonlarımız">
            <PublicHallsBlock navigateTo={navigateTo} onOpenLeadModal={() => setIsLeadModalOpen(true)} />
          </BlockErrorBoundary>

          <BlockErrorBoundary blockName="Catering & VIP Menüler">
            <PublicMenusBlock />
          </BlockErrorBoundary>

          <BlockErrorBoundary blockName="Müşteri Yorumları">
            <PublicTestimonialsBlock />
          </BlockErrorBoundary>

          <LeadModal isOpen={isLeadModalOpen} onClose={() => setIsLeadModalOpen(false)} />
        </div>
      );
    }

"""
    content = content[:start_idx] + clean_code + content[end_idx:]
    print("Successfully replaced all public components cleanly!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
