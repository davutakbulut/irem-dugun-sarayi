import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pass onSaveQuoteRequest & showToast from PublicLayout to PublicNavbar
old_layout = "function PublicLayout({ children, currentRoute = '/', navigateTo }) {"
new_layout = "function PublicLayout({ children, currentRoute = '/', navigateTo, onSaveQuoteRequest, showToast }) {"

old_navbar_in_layout = "<PublicNavbar currentRoute={currentRoute} navigateTo={navigateTo} />"
new_navbar_in_layout = "<PublicNavbar currentRoute={currentRoute} navigateTo={navigateTo} onSaveQuoteRequest={onSaveQuoteRequest} showToast={showToast} />"

old_navbar_def = "function PublicNavbar({ currentRoute = '/', navigateTo }) {"
new_navbar_def = "function PublicNavbar({ currentRoute = '/', navigateTo, onSaveQuoteRequest, showToast }) {"

if old_layout in content:
    content = content.replace(old_layout, new_layout)
if old_navbar_in_layout in content:
    content = content.replace(old_navbar_in_layout, new_navbar_in_layout)
if old_navbar_def in content:
    content = content.replace(old_navbar_def, new_navbar_def)

# Ensure LeadModal inside PublicNavbar receives onSaveQuoteRequest and showToast
old_lead_modal_in_navbar = "<LeadModal isOpen={isLeadModalOpen} onClose={() => setIsLeadModalOpen(false)} />"
new_lead_modal_in_navbar = "<LeadModal isOpen={isLeadModalOpen} onClose={() => setIsLeadModalOpen(false)} onSaveQuoteRequest={onSaveQuoteRequest} showToast={showToast} />"

if old_lead_modal_in_navbar in content:
    content = content.replace(old_lead_modal_in_navbar, new_lead_modal_in_navbar)

# Also ensure PublicLayout in App receives onSaveQuoteRequest={handleSaveQuoteRequest} and showToast={showToast}
old_app_layout = "<PublicLayout currentRoute="
content = content.replace("<PublicLayout currentRoute=", "<PublicLayout onSaveQuoteRequest={handleSaveQuoteRequest} showToast={showToast} currentRoute=")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced PublicLayout & PublicNavbar quote request props!")
