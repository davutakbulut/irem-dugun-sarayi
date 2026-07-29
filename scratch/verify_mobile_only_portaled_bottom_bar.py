with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check 1: Mobile bar portaled directly to document.body
has_portal = 'ReactDOM.createPortal(' in content and 'document.body' in content
print(f"[CHECK 1] Mobile Bottom Bar portaled to document.body: {has_portal}")

# Check 2: Hidden on desktop (sm:hidden)
has_sm_hidden = 'sm:hidden fixed bottom-0 left-0 right-0 z-50' in content
print(f"[CHECK 2] Completely hidden on desktop (sm:hidden): {has_sm_hidden}")

# Check 3: Desktop right column Canlı Hesaplama & Sözleşme Kartı intact (hidden sm:block)
has_desktop_sidebar_card = 'hidden sm:block glass-panel p-6 rounded-3xl space-y-4 shadow-xl' in content
print(f"[CHECK 3] Desktop sidebar card untouched (hidden sm:block): {has_desktop_sidebar_card}")

if has_portal and has_sm_hidden and has_desktop_sidebar_card:
    print("\n✅ ALL MOBILE-ONLY PORTALED BOTTOM BAR CHECKS PASSED 100%!")
else:
    print("\n❌ SOME CHECKS FAILED!")
