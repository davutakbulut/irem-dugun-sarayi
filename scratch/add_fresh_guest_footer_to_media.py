import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

target_marker = """      {/* LIGHTBOX CAROUSEL MODAL (DEEP BLACK BACKDROP BLUR & ULTRA-HIGH CONTRAST) */}"""

fresh_footer_code = """      {/* FRESH NORDIC LIGHT PUBLIC GUEST FOOTER */}
      {isPublicGuestMode && (
        <footer className="w-full mt-12 pt-8 pb-6 border-t border-amber-200/60 dark:border-slate-800 text-center space-y-3 bg-white/70 dark:bg-slate-900/70 backdrop-blur-md rounded-3xl p-6 shadow-xs max-w-4xl mx-auto animate-fade-in">
          <div className="flex items-center justify-center space-x-2 text-amber-600 dark:text-amber-400 font-extrabold text-sm tracking-wide">
            <ThemeIcon icon="crown" className="w-4 h-4 shrink-0" />
            <span>İREM DÜĞÜN SARAYI & BALO TESİSLERİ</span>
          </div>
          <p className="text-xs text-slate-600 dark:text-slate-300 font-medium max-w-md mx-auto leading-relaxed">
            Sapanca Göl Kenarı’nın en özel balo salonlarında unutulmaz anılar biriktirin. Çektiğiniz fotoğraf ve videolar gelin & damat albümünde yüksek çözünürlükle güvenle saklanmaktadır.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-4 text-xs font-semibold text-slate-700 dark:text-slate-200 pt-2">
            <span className="flex items-center space-x-1.5 bg-amber-50 dark:bg-amber-500/10 border border-amber-200/80 dark:border-amber-500/30 px-3 py-1 rounded-full">
              <ThemeIcon icon="mapPin" className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />
              <span>Sapanca Göl Kenarı, Sakarya</span>
            </span>
            <span className="flex items-center space-x-1.5 bg-amber-50 dark:bg-amber-500/10 border border-amber-200/80 dark:border-amber-500/30 px-3 py-1 rounded-full">
              <ThemeIcon icon="phone" className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />
              <span>+90 (264) 582 00 00</span>
            </span>
            <span className="flex items-center space-x-1.5 bg-emerald-50 dark:bg-emerald-500/10 border border-emerald-200/80 dark:border-emerald-500/30 px-3 py-1 rounded-full text-emerald-800 dark:text-emerald-300">
              <ThemeIcon icon="shieldCheck" className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
              <span>256-Bit SSL Korumalı Anı Galeri</span>
            </span>
          </div>
          <div className="text-[10px] text-slate-400 dark:text-slate-500 font-mono pt-2">
            © 2026 İrem Düğün Sarayı Canlı Medya Portalı • Tüm Hakları Saklıdır.
          </div>
        </footer>
      )}

      {/* LIGHTBOX CAROUSEL MODAL (DEEP BLACK BACKDROP BLUR & ULTRA-HIGH CONTRAST) */}"""

if target_marker in content:
    content = content.replace(target_marker, fresh_footer_code)
    print("1. Added Fresh Nordic Light public guest footer to MediaComponent!")
else:
    print("WARNING: Could not find target_marker in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
