import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = "    function PublicHeroBlock({ onOpenLeadModal }) {"
end_marker = "    function PublicWelcomeBlock({ navigateTo }) {"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

print(f"start_idx: {start_idx}, end_idx: {end_idx}")

if start_idx != -1 and end_idx != -1:
    new_hero_code = """    function PublicHeroBlock({ onOpenLeadModal }) {
      return (
        <section id="section-hero" className="w-full relative min-h-screen">
          <div className="relative w-full h-screen min-h-[100vh] overflow-hidden flex items-center justify-center">
            <video
              autoPlay
              loop
              muted
              playsInline
              className="absolute inset-0 w-full h-full object-cover scale-105 pointer-events-none"
              src="https://cdn.creafolks.com/svadba-davet/9e9fee9d-dc11-4bd5-bc7a-4614de2d7e2b.mp4"
            />
            <div className="absolute inset-0 bg-gradient-to-b from-black/65 via-black/45 to-black/75 backdrop-blur-[0.5px]" />

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

              <div className="pt-6 flex flex-wrap justify-center items-center gap-4">
                <button 
                  onClick={onOpenLeadModal} 
                  className="bg-[#B89B5E] hover:bg-[#a3874e] text-white font-extrabold px-8 py-4 rounded-full text-xs shadow-2xl transition-all duration-300 hover:scale-105 flex items-center space-x-2.5 cursor-pointer uppercase tracking-wider border border-amber-300/30"
                >
                  <span><ThemeIcon icon="crown" className="w-4 h-4 inline-block shrink-0" /></span>
                  <span>ÜCRETSİZ FİYAT TEKLİFİ ALIN</span>
                </button>

                {/* VIBRANT CORPORATE GREEN WHATSAPP BUTTON (#25D366) */}
                <a 
                  href="https://wa.me/905471440054?text=Merhaba,%20d%C3%BC%C4%9F%C3%BCn%20ve%20organizasyon%20detaylar%C4%B1%20hakk%C4%B1nda%20bilgi%20almak%20istiyorum." 
                  target="_blank" 
                  rel="noreferrer" 
                  className="bg-[#25D366] hover:bg-[#20bd5a] text-white font-extrabold px-8 py-4 rounded-full text-xs shadow-[0_10px_25px_rgba(37,211,102,0.45)] transition-all duration-300 hover:scale-105 flex items-center space-x-3 uppercase tracking-wider border border-emerald-400/40 cursor-pointer"
                >
                  <svg className="w-5 h-5 text-white fill-current shrink-0" viewBox="0 0 24 24">
                    <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/>
                  </svg>
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
        </section>
      );
    }
"""
    content = content[:start_idx] + new_hero_code + content[end_idx:]
    print("Successfully redesigned Hero WhatsApp button with vibrant #25D366 background!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
