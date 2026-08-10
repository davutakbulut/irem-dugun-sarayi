import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update HomePage signature and LeadModal call inside HomePage
old_homepage = "function HomePage({ navigateTo }) {"
new_homepage = "function HomePage({ navigateTo, onSaveQuoteRequest, showToast }) {"

if old_homepage in content:
    content = content.replace(old_homepage, new_homepage)

old_homepage_lead = "<LeadModal isOpen={isLeadModalOpen} onClose={() => setIsLeadModalOpen(false)} onSaveQuoteRequest={handleSaveQuoteRequest} showToast={showToast} />"
new_homepage_lead = "<LeadModal isOpen={isLeadModalOpen} onClose={() => setIsLeadModalOpen(false)} onSaveQuoteRequest={onSaveQuoteRequest} showToast={showToast} />"

if old_homepage_lead in content:
    content = content.replace(old_homepage_lead, new_homepage_lead)

# 2. Update PublicNavbar LeadModal call
old_navbar_lead = "<LeadModal isOpen={isLeadModalOpen} onClose={() => setIsLeadModalOpen(false)} onSaveQuoteRequest={handleSaveQuoteRequest} showToast={showToast} />"
new_navbar_lead = "<LeadModal isOpen={isLeadModalOpen} onClose={() => setIsLeadModalOpen(false)} onSaveQuoteRequest={onSaveQuoteRequest} showToast={showToast} />"

if old_navbar_lead in content:
    content = content.replace(old_navbar_lead, new_navbar_lead)

# 3. Update all secondary public page wrappers (HallsPage, OrganizationsPage, VideosPage, BlogPage, AboutUsPage)
page_wrappers = [
    ("function HallsPage({ navigateTo }) {", "function HallsPage({ navigateTo, onSaveQuoteRequest, showToast }) {"),
    ("return <HomePage navigateTo={navigateTo} />;", "return <HomePage navigateTo={navigateTo} onSaveQuoteRequest={onSaveQuoteRequest} showToast={showToast} />;"),
    ("function OrganizationsPage({ navigateTo }) { return <HomePage navigateTo={navigateTo} />; }", "function OrganizationsPage({ navigateTo, onSaveQuoteRequest, showToast }) { return <HomePage navigateTo={navigateTo} onSaveQuoteRequest={onSaveQuoteRequest} showToast={showToast} />; }"),
    ("function VideosPage({ navigateTo }) { return <HomePage navigateTo={navigateTo} />; }", "function VideosPage({ navigateTo, onSaveQuoteRequest, showToast }) { return <HomePage navigateTo={navigateTo} onSaveQuoteRequest={onSaveQuoteRequest} showToast={showToast} />; }"),
    ("function BlogPage({ navigateTo }) { return <HomePage navigateTo={navigateTo} />; }", "function BlogPage({ navigateTo, onSaveQuoteRequest, showToast }) { return <HomePage navigateTo={navigateTo} onSaveQuoteRequest={onSaveQuoteRequest} showToast={showToast} />; }"),
    ("function AboutUsPage({ navigateTo }) { return <HomePage navigateTo={navigateTo} />; }", "function AboutUsPage({ navigateTo, onSaveQuoteRequest, showToast }) { return <HomePage navigateTo={navigateTo} onSaveQuoteRequest={onSaveQuoteRequest} showToast={showToast} />; }"),
    ("function VirtualTourPage({ navigateTo }) { return <HomePage navigateTo={navigateTo} />; }", "function VirtualTourPage({ navigateTo, onSaveQuoteRequest, showToast }) { return <HomePage navigateTo={navigateTo} onSaveQuoteRequest={onSaveQuoteRequest} showToast={showToast} />; }"),
    ("function ContactPage({ navigateTo }) { return <HomePage navigateTo={navigateTo} />; }", "function ContactPage({ navigateTo, onSaveQuoteRequest, showToast }) { return <HomePage navigateTo={navigateTo} onSaveQuoteRequest={onSaveQuoteRequest} showToast={showToast} />; }")
]

for old_str, new_str in page_wrappers:
    if old_str in content:
        content = content.replace(old_str, new_str)

# 4. In App component, ensure HomePage/HallsPage/etc. receive onSaveQuoteRequest={handleSaveQuoteRequest} and showToast={showToast}
old_app_homepage_render = "<HomePage navigateTo={navigateTo} />"
new_app_homepage_render = "<HomePage navigateTo={navigateTo} onSaveQuoteRequest={handleSaveQuoteRequest} showToast={showToast} />"

if old_app_homepage_render in content:
    content = content.replace(old_app_homepage_render, new_app_homepage_render)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed ReferenceError: handleSaveQuoteRequest is not defined across all components!")
