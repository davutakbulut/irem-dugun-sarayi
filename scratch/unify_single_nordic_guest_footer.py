import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove inline footer in MediaComponent
pos1 = content.find("      {/* FRESH NORDIC LIGHT PUBLIC GUEST FOOTER */}")
pos2 = content.find("      {/* LIGHTBOX CAROUSEL MODAL (DEEP BLACK BACKDROP BLUR & ULTRA-HIGH CONTRAST) */}")

if pos1 != -1 and pos2 != -1:
    content = content[:pos1] + content[pos2:]
    print("1. Removed duplicate inline footer inside MediaComponent.")
else:
    print("WARNING: Could not find pos1 or pos2 in index.html!")

# 2. Upgrade GlobalFooterComponent with Unified Nordic Dual-Theme Guest Footer
old_guest_footer_block = """      if (isPublicGuestRoute) {
        return (
          <footer className="w-full bg-slate-900/95 dark:bg-brand-card/95 backdrop-blur-md text-slate-400 py-6 px-4 sm:px-8 border-t border-amber-500/30 text-xs font-medium relative z-40 shadow-lg">
            <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 text-center md:text-left">
              {/* LEFT: BRANDING & COPYRIGHT */}
              <div className="space-y-1">
                <div className="flex items-center justify-center md:justify-start space-x-2 font-heading font-extrabold text-amber-400 text-sm">
                  <ThemeIcon icon="crown" fallbackEmoji="" className="w-4 h-4 text-amber-400 shrink-0" />
                  <span>İrem Düğün Sarayı • Dijital Anı Albümü</span>
                </div>
                <p className="text-[11px] text-slate-400 dark:text-gray-400">
                  © {currentYear} İrem Düğün Sarayı. Tüm hakları saklıdır. Bu sayfa özel etkinlik misafirleri için hazırlanmıştır.
                </p>
              </div>

              {/* RIGHT: PROMOTION AREA FOR GUESTS */}
              <div className="flex flex-col sm:flex-row items-center gap-3 bg-amber-500/10 border border-amber-500/30 p-3 rounded-2xl">
                <div className="text-left space-y-0.5">
                  <div className="font-heading font-bold text-amber-400 text-xs">
                    Kendi Düğün veya Nişanınız İçin Denemek İster Misiniz?
                  </div>
                  <div className="text-[10px] text-slate-300">
                    Davetlilerinizin fotoğraflarını anında tek tıkla toplayın!
                  </div>
                </div>
                <a
                  href="tel:+905471440044"
                  className="px-4 py-2 gold-button text-slate-950 font-black text-xs rounded-xl shadow-md hover:scale-105 transition flex items-center space-x-1.5 shrink-0 cursor-pointer"
                >
                  <ThemeIcon icon="phone" fallbackEmoji="" className="w-3.5 h-3.5 shrink-0 text-slate-950" />
                  <span>Bilgi Al (+90 547 144 00 44)</span>
                </a>
              </div>
            </div>
          </footer>
        );
      }"""

new_guest_footer_block = """      if (isPublicGuestRoute) {
        return (
          <footer className="w-full bg-white/90 dark:bg-slate-900/95 backdrop-blur-md text-slate-700 dark:text-slate-300 py-8 px-4 sm:px-8 border-t border-amber-200/80 dark:border-amber-500/30 text-xs font-medium relative z-40 shadow-lg animate-fade-in">
            <div className="max-w-7xl mx-auto flex flex-col lg:flex-row items-center justify-between gap-6 text-center lg:text-left">
              
              {/* LEFT: BRANDING & SAPANCA LOCATION */}
              <div className="space-y-1.5 max-w-lg">
                <div className="flex items-center justify-center lg:justify-start space-x-2 font-heading font-extrabold text-amber-700 dark:text-amber-400 text-sm tracking-wide">
                  <ThemeIcon icon="crown" className="w-4 h-4 text-amber-600 dark:text-amber-400 shrink-0" />
                  <span>İREM DÜĞÜN SARAYI & BALO TESİSLERİ</span>
                </div>
                <p className="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
                  Sapanca Göl Kenarı’nın en özel balo salonlarında unutulmaz anılar biriktirin. Çektiğiniz tüm fotoğraf ve videolar yüksek çözünürlükle saklanmaktadır.
                </p>
                <div className="flex flex-wrap items-center justify-center lg:justify-start gap-3 text-slate-500 dark:text-slate-400 text-[11px] font-semibold pt-1">
                  <span className="flex items-center space-x-1">
                    <ThemeIcon icon="mapPin" className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />
                    <span>Sapanca Göl Kenarı, Sakarya</span>
                  </span>
                  <span>•</span>
                  <span className="flex items-center space-x-1">
                    <ThemeIcon icon="shieldCheck" className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
                    <span>256-Bit SSL Güvenlik</span>
                  </span>
                </div>
                <div className="text-[10px] text-slate-400 dark:text-slate-500 font-mono pt-1">
                  © {currentYear} İrem Düğün Sarayı Canlı Medya Portalı • Tüm Hakları Saklıdır.
                </div>
              </div>

              {/* RIGHT: PROMOTION AREA FOR GUESTS */}
              <div className="flex flex-col sm:flex-row items-center gap-3.5 bg-amber-50/80 dark:bg-amber-500/10 border border-amber-200/80 dark:border-amber-500/30 p-4 rounded-2xl shadow-xs">
                <div className="text-center sm:text-left space-y-0.5">
                  <div className="font-heading font-bold text-slate-900 dark:text-amber-300 text-xs">
                    Kendi Düğün veya Nişanınız İçin Denemek İster Misiniz?
                  </div>
                  <div className="text-[10px] text-slate-600 dark:text-slate-400 font-medium">
                    Davetlilerinizin fotoğraflarını anında tek tıkla QR kodla toplayın!
                  </div>
                </div>
                <a
                  href="tel:+905471440044"
                  className="px-4 py-2.5 bg-gradient-to-r from-amber-500 via-orange-500 to-amber-600 hover:from-amber-600 hover:to-orange-600 text-white font-extrabold text-xs rounded-xl shadow-md hover:shadow-lg transition flex items-center space-x-1.5 shrink-0 cursor-pointer active:scale-95"
                >
                  <ThemeIcon icon="phone" className="w-3.5 h-3.5 shrink-0" />
                  <span>Bilgi Al (+90 547 144 00 44)</span>
                </a>
              </div>

            </div>
          </footer>
        );
      }"""

if old_guest_footer_block in content:
    content = content.replace(old_guest_footer_block, new_guest_footer_block)
    print("2. Updated GlobalFooterComponent with Unified Nordic Light & Dark Dual-Theme Guest Footer!")
else:
    print("WARNING: Could not find old_guest_footer_block in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
