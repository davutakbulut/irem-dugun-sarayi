import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add isPublicGuestRoute state check at the top of App component
old_app_start = "      const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);"
new_app_start = """      const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

      // Check if current route is a Public Guest Link (e.g. #/medya-yukle?key=MEDIA-8X92M1KP or ?mode=guest)
      const isPublicGuestRoute = useMemo(() => {
        if (typeof window === 'undefined') return false;
        const hash = window.location.hash || '';
        return hash.includes('key=') || hash.includes('mode=guest');
      }, [activeTab]);"""

if old_app_start in html and "isPublicGuestRoute =" not in html:
    html = html.replace(old_app_start, new_app_start)
    print("Added isPublicGuestRoute check to App component!")

# Hide Admin Header when isPublicGuestRoute is true
old_header_cond = "{!isErrorPage && ("
new_header_cond = "{!isErrorPage && !isPublicGuestRoute && ("
if old_header_cond in html:
    html = html.replace(old_header_cond, new_header_cond)
    print("Isolated Header from Public Guest Mode!")

# Hide Admin Sidebar Navigation when isPublicGuestRoute is true
old_sidebar_cond = "{!isErrorPage && ("
new_sidebar_cond = "{!isErrorPage && !isPublicGuestRoute && ("

# Find line for aside navigation wrapper
old_aside_block = """          {/* MAIN BODY CONTAINER WITH ASIDE NAVIGATION & PAGE CONTENT */}
          <div className="flex-1 flex w-full max-w-full">
            {/* ASIDE SIDEBAR NAVIGATION */}
            {!isErrorPage && ("""

new_aside_block = """          {/* MAIN BODY CONTAINER WITH ASIDE NAVIGATION & PAGE CONTENT */}
          <div className="flex-1 flex w-full max-w-full">
            {/* PUBLIC GUEST TOP MINIMAL HEADER BAR */}
            {isPublicGuestRoute && (
              <div className="w-full bg-white dark:bg-brand-card border-b border-amber-500/30 p-4 shadow-sm text-center font-heading font-black gold-gradient-text text-lg flex items-center justify-center space-x-2 fixed top-0 left-0 right-0 z-50">
                <ThemeIcon icon="crown" fallbackEmoji="🏰" className="w-6 h-6 text-amber-500 shrink-0" />
                <span>İREM DÜĞÜN SARAYI • DİJİTAL ANI ALBÜMÜ</span>
              </div>
            )}

            {/* ASIDE SIDEBAR NAVIGATION */}
            {!isErrorPage && !isPublicGuestRoute && ("""

if old_aside_block in html:
    html = html.replace(old_aside_block, new_aside_block)
    print("Isolated Sidebar Navigation and added minimal guest top logo bar!")

# Add top padding when isPublicGuestRoute is true so content doesn't get covered by fixed guest header
old_main_tag = '<main role="main" className="flex-1 p-3 pb-4 sm:p-6 sm:pb-6 lg:p-8 lg:pb-6 min-w-0 w-full max-w-full overflow-x-hidden">'
new_main_tag = '<main role="main" className={`flex-1 p-3 pb-4 sm:p-6 sm:pb-6 lg:p-8 lg:pb-6 min-w-0 w-full max-w-full overflow-x-hidden ${isPublicGuestRoute ? "pt-20" : ""}`}'

if old_main_tag in html:
    html = html.replace(old_main_tag, new_main_tag)
    print("Added pt-20 to main layout for Public Guest Mode!")

# Hide Admin Footer when isPublicGuestRoute is true
old_footer_tag = "{/* FOOTER */}\n          {!isErrorPage && ("
new_footer_tag = "{/* FOOTER */}\n          {!isErrorPage && !isPublicGuestRoute && ("

if old_footer_tag in html:
    html = html.replace(old_footer_tag, new_footer_tag)
    print("Isolated Footer from Public Guest Mode!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html layout isolation for Public Guest Mode successfully!")
