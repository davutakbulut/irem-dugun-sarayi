import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add route parsing for standalone public route #/medya/:key in App routing
old_route_parser = "const isPublicGuestRoute = useMemo(() => {"

new_route_parser = """// 1. DEDICATED PUBLIC GUEST ROUTE PARSER (#/medya/:key or #/m/:key)
      const guestMediaKeyMatch = useMemo(() => {
        if (typeof window === 'undefined') return null;
        const hash = window.location.hash || '';
        const match = hash.match(/^#\/(?:medya|m)\/([A-Za-z0-9_-]+)/);
        return match ? match[1] : null;
      }, [activeTab]);

      const isPublicGuestRoute = useMemo(() => {
        if (typeof window === 'undefined') return false;
        const hash = window.location.hash || '';
        return !!guestMediaKeyMatch || hash.includes('mode=guest');
      }, [activeTab, guestMediaKeyMatch]);"""

if old_route_parser in html and "guestMediaKeyMatch" not in html:
    html = html.replace(old_route_parser, new_route_parser)
    print("Added guestMediaKeyMatch route parser to App component!")

# 2. Update Link Copy button in MediaComponent to generate the dedicated standalone URL: #/medya/MEDIA-8X92M1KP
old_copy_link = "const shareUrl = `${window.location.origin}${window.location.pathname}#/medya-yukle?mode=guest&key=${activeMediaKey}`;"
new_copy_link = "const shareUrl = `${window.location.origin}${window.location.pathname}#/medya/${activeMediaKey}`;"

if old_copy_link in html:
    html = html.replace(old_copy_link, new_copy_link)
    print("Updated shareUrl in MediaComponent to generate #/medya/:key!")

# 3. Add standalone public guest top header & footer in App layout
old_guest_top_header = """            {/* PUBLIC GUEST TOP MINIMAL HEADER BAR */}
            {isPublicGuestRoute && (
              <div className="w-full bg-white dark:bg-brand-card border-b border-amber-500/30 p-4 shadow-sm text-center font-heading font-black gold-gradient-text text-lg flex items-center justify-center space-x-2 fixed top-0 left-0 right-0 z-50">
                <ThemeIcon icon="crown" fallbackEmoji="🏰" className="w-6 h-6 text-amber-500 shrink-0" />
                <span>İREM DÜĞÜN SARAYI • DİJİTAL ANI ALBÜMÜ</span>
              </div>
            )}"""

new_guest_top_header = """            {/* DEDICATED STANDALONE PUBLIC GUEST HEADER (ONLY LOGO & BRANDING, NO ADMIN MENUS) */}
            {isPublicGuestRoute && (
              <header className="w-full bg-white/95 dark:bg-brand-card/95 border-b border-amber-500/30 p-4 shadow-md text-center flex items-center justify-center fixed top-0 left-0 right-0 z-50 backdrop-blur-md">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-amber-400 to-amber-600 flex items-center justify-center text-white shadow-lg">
                    <ThemeIcon icon="crown" fallbackEmoji="🏰" className="w-6 h-6 text-white shrink-0" />
                  </div>
                  <div>
                    <h1 className="font-heading font-black text-lg sm:text-xl gold-gradient-text tracking-wide uppercase">
                      İREM DÜĞÜN SARAYI
                    </h1>
                    <p className="text-[10px] font-bold text-slate-500 dark:text-gray-400 tracking-wider">
                      DİJİTAL ANI ALBÜMÜ • ÖZEL MİSAFİR PAYLAŞIM ALANI
                    </p>
                  </div>
                </div>
              </header>
            )}"""

if old_guest_top_header in html:
    html = html.replace(old_guest_top_header, new_guest_top_header)
    print("Updated Guest Top Header to dedicated standalone logo header!")

# 4. Add standalone Guest Footer (No admin links, only guest copyright & promo)
old_guest_footer_cond = "{/* FOOTER */}\n          {!isErrorPage && !isPublicGuestRoute && ("
new_guest_footer_cond = """{/* STANDALONE GUEST FOOTER */}
          {isPublicGuestRoute && (
            <footer className="w-full bg-slate-900 text-slate-400 py-6 px-4 border-t border-amber-500/20 text-center text-xs font-medium space-y-2">
              <div className="flex items-center justify-center space-x-2 font-heading font-bold text-amber-400">
                <ThemeIcon icon="crown" fallbackEmoji="🏰" className="w-4 h-4 text-amber-400 shrink-0" />
                <span>İrem Düğün Sarayı • Dijital Anı Albümü</span>
              </div>
              <p className="text-[11px] text-slate-500 max-w-md mx-auto">
                © 2026 İrem Düğün Sarayı. Tüm hakları saklıdır. Bu bağlantı etkinlik konuklarına özel paylaşım alanıdır.
              </p>
            </footer>
          )}

          {/* ADMIN FOOTER */}
          {!isErrorPage && !isPublicGuestRoute && ("""

if old_guest_footer_cond in html:
    html = html.replace(old_guest_footer_cond, new_guest_footer_cond)
    print("Added Standalone Guest Footer!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with dedicated standalone public guest route (#/medya/:key) successfully!")
