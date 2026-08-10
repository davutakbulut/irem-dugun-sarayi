import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = "    // 2. PUBLIC FOOTER MODULE (1:1 REPLICA WHATSAPP POPUP SUPPORT WIDGET)"
end_marker = "    // 3. PUBLIC LAYOUT MODULE (ISOLATED NAVBAR & FOOTER BLOCKS)"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

print(f"start_idx: {start_idx}, end_idx: {end_idx}")

if start_idx != -1 and end_idx != -1:
    new_footer_code = """    // 2. PUBLIC FOOTER MODULE (1:1 PIXEL-PERFECT REPLICA WHATSAPP POPUP SUPPORT WIDGET WITH 360 ROTATION)
    function PublicFooter({ navigateTo }) {
      const [isWhatsAppWidgetOpen, setIsWhatsAppWidgetOpen] = useState(false);
      const [isRotated, setIsRotated] = useState(false);

      const toggleWidget = () => {
        setIsRotated(prev => !prev);
        setIsWhatsAppWidgetOpen(prev => !prev);
      };

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
                <button type="button" onClick={toggleWidget} className="w-9 h-9 rounded-full bg-white border border-amber-200 flex items-center justify-center text-[#25D366] hover:bg-[#25D366] hover:text-white transition cursor-pointer"><ThemeIcon icon="chat" className="w-4 h-4 inline-block shrink-0" /></button>
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
              <p className="text-xs text-emerald-600 font-mono font-bold cursor-pointer" onClick={toggleWidget}><ThemeIcon icon="chat" className="w-4 h-4 inline-block shrink-0" /> <span className="hover:underline">WhatsApp: +90 547 144 00 54</span></p>
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

          {/* FLOATING PHONE BUTTON (LEFT) */}
          <a 
            href="tel:+905471440054" 
            className="fixed bottom-6 left-6 z-50 bg-[#B89B5E] hover:bg-[#a3874e] text-white w-14 h-14 sm:w-16 sm:h-16 rounded-full flex items-center justify-center shadow-xl hover:scale-105 transition cursor-pointer border-2 border-white"
            title="Bizi Arayın"
          >
            <ThemeIcon icon="phone" className="w-6 h-6 inline-block shrink-0 text-white" />
          </a>

          {/* FLOATING WHATSAPP CIRCLE TRIGGER BUTTON WITH 360 DEGREE ROTATION ANIMATION */}
          <button 
            type="button"
            onClick={toggleWidget}
            className={`fixed bottom-6 right-6 z-50 bg-[#25D366] hover:bg-[#20bd5a] text-white w-14 h-14 sm:w-16 sm:h-16 rounded-full flex items-center justify-center shadow-[0_10px_30px_rgba(37,211,102,0.45)] cursor-pointer transition-transform duration-500 ease-in-out border-0 outline-none ${
              isRotated ? 'rotate-[360deg] scale-110' : 'hover:scale-105'
            }`}
            title="WhatsApp Destek"
            aria-label="WhatsApp Destek Hattı"
          >
            <svg className="w-8 h-8 text-white fill-current shrink-0" viewBox="0 0 24 24">
              <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/>
            </svg>
          </button>

          {/* INTERACTIVE WHATSAPP SUPPORT WIDGET CARD (1:1 PIXEL-PERFECT REPLICA MATCHING USER IMAGE) */}
          {isWhatsAppWidgetOpen && (
            <div className="fixed bottom-26 right-4 sm:right-6 z-50 w-[calc(100vw-2rem)] sm:w-[330px] max-w-sm bg-white rounded-[24px] shadow-[0_15px_40px_rgba(0,0,0,0.14)] border border-slate-100 overflow-hidden animate-fade-in text-slate-800">
              {/* VIBRANT GREEN TOP HEADER BAR */}
              <div className="bg-[#25D366] px-6 py-4.5 flex items-center justify-between text-white shadow-xs">
                <h3 className="font-sans font-bold text-lg sm:text-[19px] tracking-tight text-white">
                  WhatsApp Destek
                </h3>
                <button
                  type="button"
                  onClick={toggleWidget}
                  className="text-white hover:opacity-80 text-xl font-bold transition cursor-pointer p-0.5 leading-none"
                  title="Kapat"
                  aria-label="Kapat"
                >
                  ✕
                </button>
              </div>

              {/* CARD BODY CONTENT */}
              <div className="p-6 space-y-4 bg-white">
                <p className="text-slate-800 text-[14px] sm:text-[15px] font-sans text-left leading-snug">
                  <span className="font-bold text-slate-900">Merhaba!</span> Size nasıl yardımcı olabiliriz?
                </p>

                {/* NUMBER 1: HIZLI RANDEVU! */}
                <a
                  href="https://wa.me/905471440054?text=Merhaba,%20d%C3%BC%C4%9F%C3%BCn%20ve%20organizasyon%20i%C3%A7in%20h%C4%B1zl%C4%B1%20randevu%20olusturmak%20istiyorum."
                  target="_blank"
                  rel="noreferrer"
                  className="p-4 bg-[#F5F6F8] hover:bg-[#EEF0F3] rounded-[20px] transition-all duration-200 flex items-center space-x-4 group cursor-pointer border border-transparent"
                >
                  <div className="w-14 h-14 rounded-full bg-[#25D366] text-white flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform shadow-xs">
                    <svg className="w-7 h-7 text-white fill-current" viewBox="0 0 24 24">
                      <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/>
                    </svg>
                  </div>
                  <div className="flex-1 min-w-0 text-left">
                    <div className="font-bold text-[16px] text-slate-900 leading-snug">
                      Hızlı Randevu!
                    </div>
                    <div className="text-[13px] font-normal text-slate-500 mt-0.5">
                      İletişime Geç
                    </div>
                  </div>
                </a>

                {/* ITEM 2: BİLGİ AL! */}
                <a
                  href="https://wa.me/905471440054?text=Merhaba,%20d%C3%BC%C4%9F%C3%BCn%20salonlar%C4%B1n%C4%B1z,%20men%C3%BCler%20ve%20fiyatlar%20hakk%C4%B1nda%20bilgi%20almak%20istiyorum."
                  target="_blank"
                  rel="noreferrer"
                  className="p-4 bg-[#F5F6F8] hover:bg-[#EEF0F3] rounded-[20px] transition-all duration-200 flex items-center space-x-4 group cursor-pointer border border-transparent"
                >
                  <div className="w-14 h-14 rounded-full bg-[#25D366] text-white flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform shadow-xs">
                    <svg className="w-7 h-7 text-white fill-current" viewBox="0 0 24 24">
                      <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/>
                    </svg>
                  </div>
                  <div className="flex-1 min-w-0 text-left">
                    <div className="font-bold text-[16px] text-slate-900 leading-snug">
                      Bilgi Al!
                    </div>
                    <div className="text-[13px] font-normal text-slate-500 mt-0.5">
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
"""
    content = content[:start_idx] + new_footer_code + content[end_idx:]
    print("Successfully updated WhatsApp widget to 1:1 pixel perfect replica with 360 animation and circle trigger!")
else:
    print("WARNING: Markers not found!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
