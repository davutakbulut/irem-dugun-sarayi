import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update GlobalFooterComponent to accept isPublicGuestRoute and render standalone promo footer on guest links
old_footer_func = "function GlobalFooterComponent({ onNavigate, activeRole, campaigns = [], showToast, onOpenVersionModal }) {"
new_footer_func = "function GlobalFooterComponent({ onNavigate, activeRole, campaigns = [], showToast, onOpenVersionModal, isPublicGuestRoute }) {"

if old_footer_func in html:
    html = html.replace(old_footer_func, new_footer_func)
    print("Updated GlobalFooterComponent parameter signature!")

# 2. Add isPublicGuestRoute conditionally inside GlobalFooterComponent
old_footer_return = """      return (
        <footer className="w-full m-0 mt-0 border-t border-slate-200 dark:border-brand-border/60 glass-panel rounded-none px-4 sm:px-8 py-8 space-y-8 animate-fade-in relative overflow-hidden">"""

new_footer_return = """      if (isPublicGuestRoute) {
        return (
          <footer className="w-full bg-slate-900/95 dark:bg-brand-card/95 backdrop-blur-md text-slate-400 py-6 px-4 sm:px-8 border-t border-amber-500/30 text-xs font-medium relative z-40 shadow-lg">
            <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 text-center md:text-left">
              {/* LEFT: BRANDING & COPYRIGHT */}
              <div className="space-y-1">
                <div className="flex items-center justify-center md:justify-start space-x-2 font-heading font-extrabold text-amber-400 text-sm">
                  <ThemeIcon icon="crown" fallbackEmoji="🏰" className="w-4 h-4 text-amber-400 shrink-0" />
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
                  href="tel:+905321112233"
                  className="px-4 py-2 gold-button text-slate-950 font-black text-xs rounded-xl shadow-md hover:scale-105 transition flex items-center space-x-1.5 shrink-0 cursor-pointer"
                >
                  <ThemeIcon icon="phone" fallbackEmoji="📞" className="w-3.5 h-3.5 shrink-0 text-slate-950" />
                  <span>Bilgi Al (+90 532 111 2233)</span>
                </a>
              </div>
            </div>
          </footer>
        );
      }

      return (
        <footer className="w-full m-0 mt-0 border-t border-slate-200 dark:border-brand-border/60 glass-panel rounded-none px-4 sm:px-8 py-8 space-y-8 animate-fade-in relative overflow-hidden">"""

if old_footer_return in html and "if (isPublicGuestRoute)" not in html:
    html = html.replace(old_footer_return, new_footer_return)
    print("Added Standalone Guest Footer Promo rendering inside GlobalFooterComponent!")

# 3. Pass isPublicGuestRoute prop to GlobalFooterComponent in App layout
old_footer_call = """          {/* SYSTEM GLOBAL FOOTER COMPONENT (FLUSH TO EDGES - 0 MARGIN & 0 PADDING WRAPPER) */}
          <div className="w-full m-0 p-0">
            <GlobalFooterComponent
              onNavigate={navigateTo}
              activeRole={activeRole}
              campaigns={campaigns}
              showToast={showToast}
              onOpenVersionModal={() => setIsVersionModalOpen(true)}
            />
          </div>"""

new_footer_call = """          {/* SYSTEM GLOBAL FOOTER COMPONENT (FLUSH TO EDGES - 0 MARGIN & 0 PADDING WRAPPER) */}
          <div className="w-full m-0 p-0">
            <GlobalFooterComponent
              onNavigate={navigateTo}
              activeRole={activeRole}
              campaigns={campaigns}
              showToast={showToast}
              onOpenVersionModal={() => setIsVersionModalOpen(true)}
              isPublicGuestRoute={isPublicGuestRoute}
            />
          </div>"""

if old_footer_call in html:
    html = html.replace(old_footer_call, new_footer_call)
    print("Passed isPublicGuestRoute prop to GlobalFooterComponent!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html guest page redesign successfully!")
