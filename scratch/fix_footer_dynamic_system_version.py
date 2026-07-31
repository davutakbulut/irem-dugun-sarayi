import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix 1: Update GlobalFooterComponent hardcoded v1.4.0 to dynamic {systemVersion || 'v1.4.56'}
old_footer_span = "<span>Canlı Sistem v1.4.0 (Sürüm Notları 📋)</span>"
new_footer_span = "<span>Canlı Sistem ({systemVersion || 'v1.4.56'}) (Sürüm Notları 📋)</span>"

if old_footer_span in html:
    html = html.replace(old_footer_span, new_footer_span)
    print("Updated GlobalFooterComponent button text to render dynamic systemVersion!")

# Fix 2: Update VersionHistoryModalComponent active version indicator from v1.4.0 (Canlı) to dynamic {systemVersion || 'v1.4.56'} (Canlı)
old_modal_span = 'Mevcut Aktif Sürüm: <strong className="text-emerald-700 dark:text-emerald-400 font-extrabold">v1.4.0 (Canlı)</strong>'
new_modal_span = 'Mevcut Aktif Sürüm: <strong className="text-emerald-700 dark:text-emerald-400 font-extrabold">{systemVersion || "v1.4.56"} (Canlı)</strong>'

if old_modal_span in html:
    html = html.replace(old_modal_span, new_modal_span)
    print("Updated VersionHistoryModalComponent active version text to render dynamic systemVersion!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html footer and modal dynamic systemVersion fix successfully!")
