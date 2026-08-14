import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

old_aside = '<aside aria-label="Ana Gezinti Menüsü" className="w-64 glass-panel p-4 hidden lg:flex flex-col justify-between border-r border-slate-200 dark:border-brand-border/40 shrink-0 sticky top-24 h-[calc(100vh-100px)] overflow-hidden">'
new_aside = '<aside aria-label="Ana Gezinti Menüsü" className="w-64 bg-white/95 dark:bg-brand-card/95 p-4 hidden lg:flex flex-col justify-between border-r border-t-0 border-slate-200 dark:border-brand-border/40 shrink-0 sticky top-16 h-[calc(100vh-4rem)] overflow-hidden">'

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_aside in content:
        content = content.replace(old_aside, new_aside)
        with open(h_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed header-sidebar gap in {h_file}")
    else:
        print(f"old_aside not found in {h_file}")

print("Header-sidebar gap fix applied to all HTML files!")
