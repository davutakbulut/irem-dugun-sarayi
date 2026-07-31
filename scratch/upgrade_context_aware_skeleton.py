import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Replace PageSkeletonLoader component definition in index.html
old_skeleton_pattern = r'function PageSkeletonLoader\(\{ title = "Sayfa Yükleniyor\.\.\." \}\) \{[\s\S]*?\n    \}'

new_skeleton_code = """function PageSkeletonLoader({ tab = 'dashboard', title = "Sayfa Yükleniyor..." }) {
      const isTablePage = ['reservations', 'finance', 'customers', 'users'].includes(tab);
      const isCardPage = ['venues', 'services', 'campaigns', 'media'].includes(tab);
      const isCalendarPage = tab === 'calendar';
      const isFormPage = tab === 'create-reservation';

      return (
        <div className="w-full space-y-6 animate-fade-in pb-12">
          {/* HEADER BANNER SKELETON */}
          <div className="glass-panel p-6 rounded-3xl space-y-3 border border-amber-500/20 relative overflow-hidden">
            <div className="h-4 w-32 rounded-full skeleton-shimmer" />
            <div className="h-7 w-64 rounded-xl skeleton-shimmer" />
            <div className="h-3 w-80 sm:w-96 rounded-lg skeleton-shimmer" />
          </div>

          {/* LAYOUT 1: TABLE PAGES (Reservations, Finance, Customers, Users) */}
          {isTablePage && (
            <div className="space-y-4">
              <div className="glass-panel p-4 rounded-2xl flex flex-col sm:flex-row gap-3 justify-between items-center border border-slate-200 dark:border-brand-border/40">
                <div className="h-10 w-full sm:w-72 rounded-xl skeleton-shimmer" />
                <div className="flex space-x-2 w-full sm:w-auto">
                  <div className="h-10 w-28 rounded-xl skeleton-shimmer" />
                  <div className="h-10 w-28 rounded-xl skeleton-shimmer" />
                </div>
              </div>
              <div className="glass-panel p-4 rounded-3xl space-y-2.5 border border-slate-200 dark:border-brand-border/40">
                <div className="h-10 w-full rounded-xl skeleton-shimmer" />
                {[...Array(6)].map((_, i) => (
                  <div key={i} className="h-14 w-full rounded-2xl skeleton-shimmer border border-slate-100 dark:border-brand-border/20" />
                ))}
              </div>
            </div>
          )}

          {/* LAYOUT 2: CALENDAR PAGE */}
          {isCalendarPage && (
            <div className="glass-panel p-6 rounded-3xl space-y-4 border border-slate-200 dark:border-brand-border/40">
              <div className="flex justify-between items-center pb-3 border-b border-slate-200 dark:border-brand-border/40">
                <div className="h-9 w-32 rounded-xl skeleton-shimmer" />
                <div className="h-8 w-44 rounded-xl skeleton-shimmer" />
                <div className="h-9 w-32 rounded-xl skeleton-shimmer" />
              </div>
              <div className="grid grid-cols-7 gap-2 text-center">
                {[...Array(7)].map((_, i) => (
                  <div key={i} className="h-8 rounded-lg skeleton-shimmer" />
                ))}
              </div>
              <div className="grid grid-cols-7 gap-2">
                {[...Array(35)].map((_, i) => (
                  <div key={i} className="h-20 sm:h-24 rounded-2xl skeleton-shimmer border border-slate-100 dark:border-brand-border/20" />
                ))}
              </div>
            </div>
          )}

          {/* LAYOUT 3: CARDS PAGES (Venues, Services, Campaigns, Media) */}
          {isCardPage && (
            <div className="space-y-4">
              <div className="glass-panel p-4 rounded-2xl flex justify-between items-center border border-slate-200 dark:border-brand-border/40">
                <div className="h-10 w-full sm:w-64 rounded-xl skeleton-shimmer" />
                <div className="h-10 w-36 rounded-xl skeleton-shimmer" />
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {[...Array(8)].map((_, i) => (
                  <div key={i} className="glass-panel p-4 rounded-3xl space-y-3 border border-slate-200 dark:border-brand-border">
                    <div className="h-40 rounded-2xl skeleton-shimmer" />
                    <div className="h-5 w-3/4 rounded-lg skeleton-shimmer" />
                    <div className="h-3 w-1/2 rounded-lg skeleton-shimmer" />
                    <div className="flex justify-between items-center pt-2">
                      <div className="h-4 w-20 rounded-lg skeleton-shimmer" />
                      <div className="h-7 w-20 rounded-xl skeleton-shimmer" />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* LAYOUT 4: FORM PAGE (Create Reservation) */}
          {isFormPage && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 glass-panel p-6 rounded-3xl space-y-6 border border-slate-200 dark:border-brand-border/40">
                <div className="h-8 w-48 rounded-xl skeleton-shimmer" />
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {[...Array(6)].map((_, i) => (
                    <div key={i} className="h-14 rounded-2xl skeleton-shimmer" />
                  ))}
                </div>
                <div className="h-32 rounded-2xl skeleton-shimmer" />
              </div>
              <div className="glass-panel p-6 rounded-3xl space-y-4 border border-amber-500/20">
                <div className="h-6 w-36 rounded-lg skeleton-shimmer" />
                <div className="h-48 rounded-2xl skeleton-shimmer" />
                <div className="h-12 rounded-xl skeleton-shimmer" />
              </div>
            </div>
          )}

          {/* LAYOUT 5: DASHBOARD & REPORTS (Default Grid + KPI Cards) */}
          {(!isTablePage && !isCardPage && !isCalendarPage && !isFormPage) && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {[...Array(4)].map((_, i) => (
                  <div key={i} className="glass-panel p-4 rounded-3xl space-y-3 border border-slate-200 dark:border-brand-border/40">
                    <div className="flex justify-between items-center">
                      <div className="h-3 w-24 rounded skeleton-shimmer" />
                      <div className="h-8 w-8 rounded-xl skeleton-shimmer" />
                    </div>
                    <div className="h-7 w-36 rounded-lg skeleton-shimmer" />
                    <div className="h-3 w-20 rounded skeleton-shimmer" />
                  </div>
                ))}
              </div>
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 glass-panel p-6 rounded-3xl space-y-4 border border-slate-200 dark:border-brand-border/40">
                  <div className="h-6 w-40 rounded-lg skeleton-shimmer" />
                  <div className="h-64 rounded-2xl skeleton-shimmer" />
                </div>
                <div className="glass-panel p-6 rounded-3xl space-y-4 border border-slate-200 dark:border-brand-border/40">
                  <div className="h-6 w-32 rounded-lg skeleton-shimmer" />
                  <div className="h-64 rounded-2xl skeleton-shimmer" />
                </div>
              </div>
            </div>
          )}
        </div>
      );
    }"""

if re.search(old_skeleton_pattern, html):
    html = re.sub(old_skeleton_pattern, new_skeleton_code, html)
    print("Upgraded PageSkeletonLoader to Context-Aware Skeleton Loader!")

# 2. Update PageSkeletonLoader call site to pass activeTab as 'tab' prop
old_call_site = '<PageSkeletonLoader title={TAB_LABELS[activeTab] || activeTab} />'
new_call_site = '<PageSkeletonLoader tab={activeTab} title={TAB_LABELS[activeTab] || activeTab} />'

if old_call_site in html:
    html = html.replace(old_call_site, new_call_site)
    print("Updated PageSkeletonLoader call site to pass activeTab prop!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html successfully!")
