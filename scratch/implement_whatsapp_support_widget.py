import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = "    function PublicFooter({ navigateTo }) {"
end_marker = "    function PublicLayout({ children, currentRoute = '/', navigateTo }) {"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_footer_code = """    function PublicFooter({ navigateTo }) {
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

          {/* INTERACTIVE WHATSAPP SUPPORT WIDGET CARD (MATCHING USER REFERENCE IMAGE) */}
          {isWhatsAppWidgetOpen && (
            <div className="fixed bottom-24 right-4 sm:right-6 z-50 w-[calc(100vw-2rem)] sm:w-80 max-w-sm bg-white rounded-3xl shadow-[0_20px_60px_rgba(0,0,0,0.3)] border border-slate-100 overflow-hidden animate-fade-in">
              {/* GREEN HEADER BAR WITH CLOSE BUTTON */}
              <div className="bg-[#25D366] px-5 py-4 flex items-center justify-between text-white">
                <div className="flex items-center space-x-2 font-heading font-extrabold text-base tracking-wide">
                  <span>WhatsApp Destek</span>
                </div>
                <button
                  type="button"
                  onClick={() => setIsWhatsAppWidgetOpen(false)}
                  className="w-7 h-7 rounded-full bg-white/20 hover:bg-white/30 text-white font-bold text-sm flex items-center justify-center transition cursor-pointer"
                  title="Kapat"
                >
                  ✕
                </button>
              </div>

              {/* CARD BODY CONTENT */}
              <div className="p-5 space-y-4 bg-slate-50/50">
                <div className="text-xs sm:text-sm font-bold text-slate-800 text-left">
                  <span className="font-extrabold">Merhaba!</span> Size nasıl yardımcı olabiliriz?
                </div>

                {/* SUPPORT CONTACT 1: DAVUT AKBULUT - HIZLI DESTEK */}
                <a
                  href="https://wa.me/905471440054?text=Merhaba,%20İrem%20Düğün%20Saray%C4%B1%20organizasyon%20hakk%C4%B1nda%20bilgi%20almak%20istiyorum."
                  target="_blank"
                  rel="noreferrer"
                  className="p-3.5 bg-white rounded-2xl border border-slate-200/80 hover:border-[#25D366] shadow-xs hover:shadow-md transition-all duration-300 flex items-center space-x-3.5 group cursor-pointer"
                >
                  <div className="w-11 h-11 rounded-full bg-[#25D366] text-white flex items-center justify-center text-xl shrink-0 group-hover:scale-105 transition-transform shadow-xs">
                    <ThemeIcon icon="chat" className="w-5 h-5 text-white shrink-0" />
                  </div>
                  <div className="flex-1 min-w-0 text-left">
                    <div className="font-extrabold text-xs sm:text-sm text-slate-900 group-hover:text-[#25D366] transition-colors truncate">
                      Davut Akbulut - Hızlı Destek
                    </div>
                    <div className="text-[11px] font-semibold text-slate-500">
                      İletişime Geç
                    </div>
                  </div>
                </a>

                {/* SUPPORT CONTACT 2: REZERVASYON & TEKLİF HATTI */}
                <a
                  href="https://wa.me/905471440054?text=Merhaba,%20düğün%20tarihi%20ve%20fiyat%20teklifi%20almak%20istiyorum."
                  target="_blank"
                  rel="noreferrer"
                  className="p-3.5 bg-white rounded-2xl border border-slate-200/80 hover:border-[#25D366] shadow-xs hover:shadow-md transition-all duration-300 flex items-center space-x-3.5 group cursor-pointer"
                >
                  <div className="w-11 h-11 rounded-full bg-[#25D366] text-white flex items-center justify-center text-xl shrink-0 group-hover:scale-105 transition-transform shadow-xs">
                    <ThemeIcon icon="crown" className="w-5 h-5 text-white shrink-0" />
                  </div>
                  <div className="flex-1 min-w-0 text-left">
                    <div className="font-extrabold text-xs sm:text-sm text-slate-900 group-hover:text-[#25D366] transition-colors truncate">
                      Rezervasyon & Fiyat Teklifi
                    </div>
                    <div className="text-[11px] font-semibold text-slate-500">
                      Canlı İletişim (+90 547 144 00 54)
                    </div>
                  </div>
                </a>
              </div>
            </div>
          )}
        </footer>
      );
    }
"""
    content = content[:start_idx] + new_footer_code + content[end_idx:]
    print("Successfully replaced PublicFooter with interactive WhatsApp pop-up widget!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
