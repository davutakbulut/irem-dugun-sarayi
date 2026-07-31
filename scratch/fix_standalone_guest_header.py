import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace header block in App component to place Standalone Guest Header in the root header slot
old_header_block = """          {/* HEADER */}
          {!isErrorPage && !isPublicGuestRoute && (
            <header role="banner" className="sticky top-0 z-30 bg-white dark:bg-brand-card border-b border-slate-200 dark:border-brand-border/40 shadow-md flex flex-col">"""

new_header_block = """          {/* HEADER */}
          {!isErrorPage && (
            isPublicGuestRoute ? (
              /* DEDICATED STANDALONE PUBLIC GUEST HEADER (ONLY LOGO & BRANDING) */
              <header role="banner" className="sticky top-0 z-50 bg-white/95 dark:bg-brand-card/95 border-b border-amber-500/30 p-4 shadow-md text-center flex items-center justify-center backdrop-blur-md w-full">
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
            ) : (
              <header role="banner" className="sticky top-0 z-30 bg-white dark:bg-brand-card border-b border-slate-200 dark:border-brand-border/40 shadow-md flex flex-col">"""

if old_header_block in html:
    html = html.replace(old_header_block, new_header_block)
    print("Placed Standalone Guest Header into root header slot!")

# Clean up duplicate guest header inside flex container if present
dup_header = """            {/* DEDICATED STANDALONE PUBLIC GUEST HEADER (ONLY LOGO & BRANDING, NO ADMIN MENUS) */}
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

if dup_header in html:
    html = html.replace(dup_header, "")
    print("Removed duplicate guest header inside body flex container!")

# Fix end of admin header closing tag if needed
old_admin_header_end = "            </header>\n          )}"
# Check main tag pt-20
old_main_pt = 'className={`flex-1 p-3 pb-4 sm:p-6 sm:pb-6 lg:p-8 lg:pb-6 min-w-0 w-full max-w-full overflow-x-hidden ${isPublicGuestRoute ? "pt-20" : ""}`}'
new_main_pt = 'className="flex-1 p-3 pb-4 sm:p-6 sm:pb-6 lg:p-8 lg:pb-6 min-w-0 w-full max-w-full overflow-x-hidden"'

if old_main_pt in html:
    html = html.replace(old_main_pt, new_main_pt)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html root Standalone Guest Header successfully!")
