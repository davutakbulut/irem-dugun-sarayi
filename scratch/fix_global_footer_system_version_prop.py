import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update GlobalFooterComponent signature to accept systemVersion prop
old_footer_sig = "function GlobalFooterComponent({ onNavigate, activeRole, campaigns = [], showToast, onOpenVersionModal, isPublicGuestRoute }) {"
new_footer_sig = "function GlobalFooterComponent({ onNavigate, activeRole, campaigns = [], showToast, onOpenVersionModal, isPublicGuestRoute, systemVersion }) {"

if old_footer_sig in html:
    html = html.replace(old_footer_sig, new_footer_sig)
    print("Updated GlobalFooterComponent signature to accept systemVersion prop!")

# 2. Update GlobalFooterComponent invocation in App component to pass systemVersion
old_footer_render = "<GlobalFooterComponent onNavigate={navigateTo} activeRole={activeRole} campaigns={campaigns} showToast={showToast} onOpenVersionModal={() => setIsVersionModalOpen(true)} isPublicGuestRoute={isPublicGuestRoute} />"
new_footer_render = "<GlobalFooterComponent onNavigate={navigateTo} activeRole={activeRole} campaigns={campaigns} showToast={showToast} onOpenVersionModal={() => setIsVersionModalOpen(true)} isPublicGuestRoute={isPublicGuestRoute} systemVersion={systemVersion} />"

if old_footer_render in html:
    html = html.replace(old_footer_render, new_footer_render)
    print("Passed systemVersion prop to GlobalFooterComponent in App component!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html GlobalFooterComponent systemVersion prop fix successfully!")
