import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_sub_footer = """            <div className="flex items-center space-x-4 font-semibold text-[11px]">
              <button onClick={() => onNavigate('settings-appearance')} className="hover:text-amber-600 dark:hover:text-gold-400 transition">Görünüm Ayarları</button>
              <span>•</span>
              <button onClick={onOpenVersionModal} className="hover:text-amber-600 dark:hover:text-gold-400 transition font-bold text-amber-600 dark:text-gold-400">📋 Sistem Sürüm Geçmişi ({systemVersion || 'v1.4.48'})</button>
              <span>•</span>
              <button onClick={() => showToast('🛡️ Gizlilik ve Güvenlik Sözleşmesi Onaylıdır')} className="hover:text-amber-600 dark:hover:text-gold-400 transition">Gizlilik Politikası</button>
            </div>"""

new_sub_footer = """            <div className="flex items-center space-x-4 font-semibold text-[11px]">
              <button onClick={() => onNavigate('settings-appearance')} className="hover:text-amber-600 dark:hover:text-gold-400 transition">Görünüm Ayarları</button>
              <span>•</span>
              <button onClick={() => showToast('🛡️ Gizlilik ve Güvenlik Sözleşmesi Onaylıdır')} className="hover:text-amber-600 dark:hover:text-gold-400 transition">Gizlilik Politikası</button>
            </div>"""

if old_sub_footer in html:
    html = html.replace(old_sub_footer, new_sub_footer)
    print("Removed duplicate sub-footer version history link from index.html successfully!")
else:
    print("Could not find old_sub_footer in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html duplicate version link cleanup successfully!")
