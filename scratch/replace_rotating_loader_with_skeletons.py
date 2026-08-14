import os, re

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update ReservationsPageComponent: replace blocking ReservationIconsRotatingLoader with in-table skeleton rows
    old_res_loading_block = """          {/* VIEW SWITCHER: TABLE OR MASTER CALENDAR */}
          {isListLoading ? (
            <div className="glass-panel p-8 rounded-3xl border border-amber-500/30 shadow-md my-4 flex items-center justify-center">
              <ReservationIconsRotatingLoader message="Rezervasyon Kayıtları Listeleniyor ve İşleniyor..." />
            </div>
          ) : viewMode === 'table' ? ("""

    new_res_loading_block = """          {/* VIEW SWITCHER: TABLE OR MASTER CALENDAR */}
          {viewMode === 'table' ? ("""

    content = content.replace(old_res_loading_block, new_res_loading_block)

    # In table body of ReservationsPageComponent, inject skeleton rows if isListLoading
    old_tbody_res = """                  <tbody className="divide-y divide-slate-100 dark:divide-brand-border/40">
                    {filteredReservations"""

    new_tbody_res = """                  <tbody className="divide-y divide-slate-100 dark:divide-brand-border/40">
                    {isListLoading ? (
                      [...Array(6)].map((_, i) => (
                        <tr key={i} className="animate-pulse">
                          <td className="py-3.5 px-3"><div className="h-4 w-6 rounded skeleton-shimmer mx-auto" /></td>
                          <td className="py-3.5 px-3"><div className="h-4 w-24 rounded skeleton-shimmer" /></td>
                          <td className="py-3.5 px-3"><div className="h-4 w-36 rounded skeleton-shimmer" /></td>
                          <td className="py-3.5 px-3"><div className="h-4 w-28 rounded skeleton-shimmer" /></td>
                          <td className="py-3.5 px-3"><div className="h-4 w-24 rounded skeleton-shimmer" /></td>
                          <td className="py-3.5 px-3"><div className="h-4 w-14 rounded skeleton-shimmer" /></td>
                          <td className="py-3.5 px-3"><div className="h-4 w-20 rounded skeleton-shimmer" /></td>
                          <td className="py-3.5 px-3"><div className="h-4 w-20 rounded skeleton-shimmer" /></td>
                          <td className="py-3.5 px-3"><div className="h-6 w-24 rounded-full skeleton-shimmer" /></td>
                          <td className="py-3.5 px-3 text-right"><div className="h-7 w-20 rounded-xl skeleton-shimmer ml-auto" /></td>
                        </tr>
                      ))
                    ) : filteredReservations"""

    content = content.replace(old_tbody_res, new_tbody_res)

    # 2. Update CustomersPageComponent: replace blocking ReservationIconsRotatingLoader with card/table skeletons
    old_cust_loading_block = """          {/* CONTENT: GRID MODE vs TABLE MODE */}
          {isListLoading ? (
            <div className="glass-panel p-8 rounded-3xl border border-amber-500/30 shadow-md my-4 flex items-center justify-center">
              <ReservationIconsRotatingLoader message="Müşteri Kayıtları Yükleniyor ve Filtreleniyor..." />
            </div>
          ) : filteredCustomers.length === 0 ? ("""

    new_cust_loading_block = """          {/* CONTENT: GRID MODE vs TABLE MODE */}
          {isListLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-pulse">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="glass-panel p-5 rounded-2xl flex items-start space-x-4 shadow-sm border border-slate-200 dark:border-brand-border/40">
                  <div className="w-14 h-14 rounded-2xl skeleton-shimmer shrink-0" />
                  <div className="flex-1 space-y-2">
                    <div className="h-4 w-36 rounded skeleton-shimmer" />
                    <div className="h-3 w-48 rounded skeleton-shimmer" />
                    <div className="h-3 w-28 rounded skeleton-shimmer" />
                  </div>
                </div>
              ))}
            </div>
          ) : filteredCustomers.length === 0 ? ("""

    content = content.replace(old_cust_loading_block, new_cust_loading_block)

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Replaced blocking loaders with fast skeleton shimmers in {h_file}!")

print("All files updated successfully!")
