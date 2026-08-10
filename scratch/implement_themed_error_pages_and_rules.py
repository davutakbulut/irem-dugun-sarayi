import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add the 3 Error Pages Components before PublicLayout
error_pages_code = """
    // =========================================================================
    // WEDDING & EVENT THEMED ERROR PAGES (404 NOT FOUND, 500 SERVER ERROR, 403 FORBIDDEN)
    // =========================================================================
    function NotFoundPage({ navigateTo }) {
      return (
        <div className="min-h-[70vh] bg-[#faf8f5] flex items-center justify-center py-20 px-4">
          <div className="max-w-2xl w-full bg-white rounded-3xl p-8 sm:p-12 shadow-xl border border-amber-100 text-center space-y-6 animate-fade-in">
            <div className="w-20 h-20 mx-auto rounded-full bg-amber-50 border-2 border-amber-200 flex items-center justify-center text-[#B89B5E] text-4xl shadow-inner">
              <ThemeIcon icon="crown" className="w-10 h-10 inline-block shrink-0 text-[#B89B5E]" />
            </div>
            
            <div className="space-y-2">
              <span className="text-xs font-black tracking-widest text-[#B89B5E] uppercase bg-amber-100/60 px-3 py-1 rounded-full border border-amber-200">
                HATA KODU: 404 - SAYFA BULUNAMADI
              </span>
              <h1 className="text-3xl sm:text-4xl font-serif font-extrabold text-slate-900 pt-2">
                Aradığınız Sayfa Bir Düğün Masalı Gibi Kayboldu...
              </h1>
              <p className="text-sm text-slate-600 max-w-lg mx-auto leading-relaxed">
                Ulaşmaya çalıştığınız web adresi silinmiş, taşınmış veya hiç var olmamış olabilir. Hayallerinizdeki düğünü planlamaya kaldığımız yerden devam edebiliriz.
              </p>
            </div>

            <div className="pt-4 flex flex-wrap items-center justify-center gap-4">
              <a
                href="/"
                onClick={(e) => { e.preventDefault(); if (navigateTo) navigateTo('/'); }}
                className="bg-[#B89B5E] hover:bg-[#a3874e] text-white font-extrabold px-7 py-3.5 rounded-full text-xs shadow-lg transition hover:scale-105 cursor-pointer"
              >
                ← Anasayfaya Dön
              </a>
              <a
                href="/salonlar"
                onClick={(e) => { e.preventDefault(); if (navigateTo) navigateTo('/salonlar'); }}
                className="bg-slate-900 hover:bg-slate-800 text-white font-extrabold px-7 py-3.5 rounded-full text-xs shadow-md transition hover:scale-105 cursor-pointer"
              >
                Salonlarımızı İnceleyin
              </a>
              <a
                href="https://wa.me/905471440054"
                target="_blank"
                rel="noreferrer"
                className="bg-[#25D366] hover:bg-[#20bd5a] text-white font-extrabold px-7 py-3.5 rounded-full text-xs shadow-md transition hover:scale-105"
              >
                WhatsApp Canlı Destek
              </a>
            </div>
          </div>
        </div>
      );
    }

    function ServerErrorPage({ navigateTo }) {
      return (
        <div className="min-h-[70vh] bg-[#faf8f5] flex items-center justify-center py-20 px-4">
          <div className="max-w-2xl w-full bg-white rounded-3xl p-8 sm:p-12 shadow-xl border border-amber-100 text-center space-y-6 animate-fade-in">
            <div className="w-20 h-20 mx-auto rounded-full bg-amber-50 border-2 border-amber-200 flex items-center justify-center text-[#B89B5E] text-4xl shadow-inner">
              <ThemeIcon icon="sparkles" className="w-10 h-10 inline-block shrink-0 text-[#B89B5E]" />
            </div>
            
            <div className="space-y-2">
              <span className="text-xs font-black tracking-widest text-[#B89B5E] uppercase bg-amber-100/60 px-3 py-1 rounded-full border border-amber-200">
                HATA KODU: 500 - SUNUCU HATASI
              </span>
              <h1 className="text-3xl sm:text-4xl font-serif font-extrabold text-slate-900 pt-2">
                Orkestramız Kısa Bir Mola Verdi...
              </h1>
              <p className="text-sm text-slate-600 max-w-lg mx-auto leading-relaxed">
                Sunucularımızda anlık bir yoğunluk veya bakım çalışması yaşanıyor. Lütfen sayfayı yenilemeyi deneyin ya da teknik ekibimize bildirin.
              </p>
            </div>

            <div className="pt-4 flex flex-wrap items-center justify-center gap-4">
              <button
                onClick={() => window.location.reload()}
                className="bg-[#B89B5E] hover:bg-[#a3874e] text-white font-extrabold px-7 py-3.5 rounded-full text-xs shadow-lg transition hover:scale-105 cursor-pointer"
              >
                🔄 Sayfayı Yenile
              </button>
              <a
                href="/"
                onClick={(e) => { e.preventDefault(); if (navigateTo) navigateTo('/'); }}
                className="bg-slate-900 hover:bg-slate-800 text-white font-extrabold px-7 py-3.5 rounded-full text-xs shadow-md transition hover:scale-105 cursor-pointer"
              >
                Anasayfaya Dön
              </a>
            </div>
          </div>
        </div>
      );
    }

    function ForbiddenPage({ navigateTo }) {
      return (
        <div className="min-h-[70vh] bg-[#faf8f5] flex items-center justify-center py-20 px-4">
          <div className="max-w-2xl w-full bg-white rounded-3xl p-8 sm:p-12 shadow-xl border border-amber-100 text-center space-y-6 animate-fade-in">
            <div className="w-20 h-20 mx-auto rounded-full bg-amber-50 border-2 border-amber-200 flex items-center justify-center text-[#B89B5E] text-4xl shadow-inner">
              <ThemeIcon icon="lock" className="w-10 h-10 inline-block shrink-0 text-[#B89B5E]" />
            </div>
            
            <div className="space-y-2">
              <span className="text-xs font-black tracking-widest text-[#B89B5E] uppercase bg-amber-100/60 px-3 py-1 rounded-full border border-amber-200">
                HATA KODU: 403 - YETKİSİZ ERİŞİM
              </span>
              <h1 className="text-3xl sm:text-4xl font-serif font-extrabold text-slate-900 pt-2">
                VIP Gelin & Damat Odasına İzinsiz Giriş Engellendi
              </h1>
              <p className="text-sm text-slate-600 max-w-lg mx-auto leading-relaxed">
                Bu özel yönetim ve temsilci alanına erişmek için yetkili hesaba giriş yapmış olmanız gerekmektedir.
              </p>
            </div>

            <div className="pt-4 flex flex-wrap items-center justify-center gap-4">
              <a
                href="/yonetim/giris"
                onClick={(e) => { e.preventDefault(); if (navigateTo) navigateTo('/yonetim/giris'); }}
                className="bg-[#B89B5E] hover:bg-[#a3874e] text-white font-extrabold px-7 py-3.5 rounded-full text-xs shadow-lg transition hover:scale-105 cursor-pointer"
              >
                Tesis Yöneticisi Girişi
              </a>
              <a
                href="/"
                onClick={(e) => { e.preventDefault(); if (navigateTo) navigateTo('/'); }}
                className="bg-slate-900 hover:bg-slate-800 text-white font-extrabold px-7 py-3.5 rounded-full text-xs shadow-md transition hover:scale-105 cursor-pointer"
              >
                Anasayfaya Dön
              </a>
            </div>
          </div>
        </div>
      );
    }
"""

marker = "    // 3. PUBLIC LAYOUT MODULE (ISOLATED NAVBAR & FOOTER BLOCKS)"
marker_idx = content.find(marker)

if marker_idx != -1:
    content = content[:marker_idx] + error_pages_code + "\n" + content[marker_idx:]
    print("Successfully inserted 404, 500, and 403 themed error page components!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
