import sys

# Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_badges_container = """              {/* BADGES ROW WITH FLEX-WRAP TO PREVENT HORIZONTAL OVERFLOW */}
              <div className="flex flex-wrap items-center gap-2 max-w-full">"""

new_badges_container = """              {/* BADGES ROW HORIZONTALLY SCROLLABLE ON MOBILE */}
              <div className="w-full flex items-center space-x-2 overflow-x-auto whitespace-nowrap no-scrollbar snap-x snap-mandatory py-1 max-w-full shrink-0">"""

if old_badges_container in html:
    html = html.replace(old_badges_container, new_badges_container)
    # Add shrink-0 whitespace-nowrap snap-start to badges
    html = html.replace(
        '<span className="inline-flex items-center space-x-1.5 bg-slate-100 dark:bg-brand-dark text-slate-800 dark:text-gray-200 text-xs font-bold px-3 py-1 rounded-full border border-slate-200 dark:border-brand-border shrink-0">',
        '<span className="inline-flex items-center space-x-1.5 bg-slate-100 dark:bg-brand-dark text-slate-800 dark:text-gray-200 text-xs font-bold px-3 py-1 rounded-full border border-slate-200 dark:border-brand-border shrink-0 whitespace-nowrap snap-start">'
    )
    html = html.replace(
        'className="px-2.5 py-1 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 text-amber-700 dark:text-gold-400 border border-amber-500/30 text-xs font-mono font-bold inline-flex items-center space-x-1 shrink-0 cursor-pointer transition"',
        'className="px-2.5 py-1 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 text-amber-700 dark:text-gold-400 border border-amber-500/30 text-xs font-mono font-bold inline-flex items-center space-x-1 shrink-0 cursor-pointer transition whitespace-nowrap snap-start"'
    )
    html = html.replace(
        '<span className="px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30 text-xs font-bold inline-flex items-center space-x-1 shrink-0">',
        '<span className="px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30 text-xs font-bold inline-flex items-center space-x-1 shrink-0 whitespace-nowrap snap-start">'
    )
    html = html.replace(
        '<span className="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-brand-dark text-slate-500 text-xs font-semibold inline-flex items-center space-x-1 shrink-0">',
        '<span className="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-brand-dark text-slate-500 text-xs font-semibold inline-flex items-center space-x-1 shrink-0 whitespace-nowrap snap-start">'
    )
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated index.html mobile horizontal scroll badges successfully!")
else:
    print("Could not find old_badges_container in index.html!")

# Update src/pages/CreateReservationPage.jsx
with open('src/pages/CreateReservationPage.jsx', 'r', encoding='utf-8') as f:
    page_jsx = f.read()

if old_badges_container in page_jsx:
    page_jsx = page_jsx.replace(old_badges_container, new_badges_container)
    page_jsx = page_jsx.replace(
        '<span className="inline-flex items-center space-x-1.5 bg-slate-100 dark:bg-brand-dark text-slate-800 dark:text-gray-200 text-xs font-bold px-3 py-1 rounded-full border border-slate-200 dark:border-brand-border shrink-0">',
        '<span className="inline-flex items-center space-x-1.5 bg-slate-100 dark:bg-brand-dark text-slate-800 dark:text-gray-200 text-xs font-bold px-3 py-1 rounded-full border border-slate-200 dark:border-brand-border shrink-0 whitespace-nowrap snap-start">'
    )
    page_jsx = page_jsx.replace(
        'className="px-2.5 py-1 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 text-amber-700 dark:text-gold-400 border border-amber-500/30 text-xs font-mono font-bold inline-flex items-center space-x-1 shrink-0 cursor-pointer transition"',
        'className="px-2.5 py-1 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 text-amber-700 dark:text-gold-400 border border-amber-500/30 text-xs font-mono font-bold inline-flex items-center space-x-1 shrink-0 cursor-pointer transition whitespace-nowrap snap-start"'
    )
    page_jsx = page_jsx.replace(
        '<span className="px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30 text-xs font-bold inline-flex items-center space-x-1 shrink-0">',
        '<span className="px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30 text-xs font-bold inline-flex items-center space-x-1 shrink-0 whitespace-nowrap snap-start">'
    )
    page_jsx = page_jsx.replace(
        '<span className="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-brand-dark text-slate-500 text-xs font-semibold inline-flex items-center space-x-1 shrink-0">',
        '<span className="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-brand-dark text-slate-500 text-xs font-semibold inline-flex items-center space-x-1 shrink-0 whitespace-nowrap snap-start">'
    )
    with open('src/pages/CreateReservationPage.jsx', 'w', encoding='utf-8') as f:
        f.write(page_jsx)
    print("Updated src/pages/CreateReservationPage.jsx mobile horizontal scroll badges successfully!")
