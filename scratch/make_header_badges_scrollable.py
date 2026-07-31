import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace flex-wrap with horizontal scrolling container in index.html
old_badges_container = '<div className="flex flex-wrap items-center gap-2">'
new_badges_container = '<div className="w-full flex items-center space-x-2 overflow-x-auto whitespace-nowrap custom-scrollbar pb-1.5 shrink-0">'

if old_badges_container in html:
    html = html.replace(old_badges_container, new_badges_container)
    print("Updated badges container in index.html to horizontal scrollable row!")

# Ensure each badge has shrink-0 whitespace-nowrap
html = html.replace(
    'className="inline-flex items-center space-x-1.5 bg-slate-100 dark:bg-brand-dark text-slate-800 dark:text-gray-200 text-xs font-bold px-3 py-1 rounded-full border border-slate-200 dark:border-brand-border"',
    'className="inline-flex items-center space-x-1.5 bg-slate-100 dark:bg-brand-dark text-slate-800 dark:text-gray-200 text-xs font-bold px-3 py-1 rounded-full border border-slate-200 dark:border-brand-border shrink-0 whitespace-nowrap"'
)

html = html.replace(
    'className="px-2.5 py-1 rounded-lg bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20 text-xs font-mono font-bold inline-flex items-center space-x-1"',
    'className="px-2.5 py-1 rounded-lg bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20 text-xs font-mono font-bold inline-flex items-center space-x-1 shrink-0 whitespace-nowrap"'
)

html = html.replace(
    'className="px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20 text-xs font-bold inline-flex items-center space-x-1"',
    'className="px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20 text-xs font-bold inline-flex items-center space-x-1 shrink-0 whitespace-nowrap"'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html badges successfully!")
