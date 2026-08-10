import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_siteyi_gor_btn = """                  <a
                    href="/"
                    target="_blank"
                    rel="noreferrer"
                    className="bg-slate-900 hover:bg-slate-800 text-amber-400 font-bold text-xs px-3.5 py-2 rounded-xl border border-amber-500/40 shadow-sm flex items-center space-x-1.5 hover:scale-105 transition cursor-pointer"
                    title="Ön Yüz Web Sitesini Yeni Sekmede Aç"
                  >
                    <span className="text-sm"><ThemeIcon icon="location" className="w-4 h-4 inline-block shrink-0" /></span>
                    <span className="hidden sm:inline">Siteyi Gör</span>
                  </a>"""

new_siteyi_gor_btn = """                  <a
                    href="/"
                    target="_blank"
                    rel="noreferrer"
                    className="px-3.5 py-2 rounded-xl bg-amber-50 dark:bg-amber-500/10 border border-amber-300 dark:border-amber-500/40 text-amber-900 dark:text-amber-300 font-extrabold text-xs hover:bg-amber-100 dark:hover:bg-amber-500/20 shadow-xs hover:scale-105 transition flex items-center space-x-1.5 cursor-pointer"
                    title="Ön Yüz Web Sitesini Yeni Sekmede Aç"
                  >
                    <ThemeIcon icon="globe" className="w-4 h-4 text-amber-600 dark:text-amber-400 shrink-0" />
                    <span className="hidden sm:inline font-black tracking-wide">Siteyi Gör ↗</span>
                  </a>"""

if old_siteyi_gor_btn in content:
    content = content.replace(old_siteyi_gor_btn, new_siteyi_gor_btn, 1)
    print("1. Successfully updated 'Siteyi Gör' button with high-contrast Nordic Light & Dark styling!")
else:
    print("WARNING: Could not find old_siteyi_gor_btn in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
