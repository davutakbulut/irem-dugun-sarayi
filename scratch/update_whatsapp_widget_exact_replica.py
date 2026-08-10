import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = "          {/* INTERACTIVE WHATSAPP SUPPORT WIDGET CARD */}"
end_marker = "        </footer>"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

print(f"start_idx: {start_idx}, end_idx: {end_idx}")

if start_idx != -1 and end_idx != -1:
    exact_whatsapp_widget_code = """          {/* INTERACTIVE WHATSAPP SUPPORT WIDGET CARD (EXACT REPLICA MATCHING REFERENCE IMAGE) */}
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
"""
    content = content[:start_idx] + exact_whatsapp_widget_code + content[end_idx:]
    print("Successfully updated WhatsApp widget to 1:1 exact image replica!")
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
