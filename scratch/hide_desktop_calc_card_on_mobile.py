import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

old_str = '<div className="glass-panel p-5 sm:p-6 rounded-3xl space-y-4 shadow-xl border-2 border-amber-500/40 dark:border-amber-500/30 bg-white/95 dark:bg-brand-card/95 backdrop-blur-md">'
new_str = '<div className="hidden lg:block glass-panel p-5 sm:p-6 rounded-3xl space-y-4 shadow-xl border-2 border-amber-500/40 dark:border-amber-500/30 bg-white/95 dark:bg-brand-card/95 backdrop-blur-md">'

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_str in content:
        content = content.replace(old_str, new_str)
        with open(h_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully hidden on mobile in {h_file}!")
    else:
        print(f"old_str not found in {h_file}")

print("All HTML files updated!")
