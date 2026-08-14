import os, re

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean the top header so "+ Kasa Hareketi Ekle" is removed from the top header group
    old_header_buttons = """            <div className="flex items-center space-x-2 w-full md:w-auto flex-wrap gap-2">
              <div className="flex bg-slate-100 dark:bg-brand-dark p-1 rounded-2xl border border-slate-200 dark:border-brand-border">
                <button
                  onClick={() => setActiveSubTab('profitability')}
                  className={`px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 cursor-pointer ${
                    activeSubTab === 'profitability'
                      ? 'bg-amber-500 text-slate-950 shadow-md font-extrabold'
                      : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-white'
                  }`}
                >
                  <span><ThemeIcon icon="chart" className="w-4 h-4 inline-block shrink-0" /></span>
                  <span>Sözleşme Kârlılığı</span>
                </button>
                <button
                  onClick={() => setActiveSubTab('kasa')}
                  className={`px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 cursor-pointer ${
                    activeSubTab === 'kasa'
                      ? 'bg-amber-500 text-slate-950 shadow-md font-extrabold'
                      : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-white'
                  }`}
                >
                  <span><ThemeIcon icon="card" className="w-4 h-4 inline-block shrink-0" /></span>
                  <span>Kasa & Harcama Akışı</span>
                </button>
                <button
                  onClick={() => setActiveSubTab('monthly')}
                  className={`px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 cursor-pointer ${
                    activeSubTab === 'monthly'
                      ? 'bg-amber-500 text-slate-950 shadow-md font-extrabold'
                      : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-white'
                  }`}
                >
                  <span><ThemeIcon icon="calendar" className="w-4 h-4 inline-block shrink-0" /></span>
                  <span>Aylık Nakit Raporu</span>
                </button>
              </div>

              {activeSubTab === 'kasa' && (
                <button
                  onClick={() => {
                    setTransType('gider');
                    setIsModalOpen(true);
                  }}
                  className="px-4 py-2 gold-button font-extrabold text-xs rounded-xl shadow cursor-pointer flex items-center space-x-1.5"
                >
                  <span>+ Kasa Hareketi Ekle</span>
                </button>
              )}
            </div>"""

    new_header_buttons = """            <div className="flex items-center space-x-2 w-full md:w-auto">
              <div className="flex bg-slate-100 dark:bg-brand-dark p-1 rounded-2xl border border-slate-200 dark:border-brand-border w-full sm:w-auto justify-between sm:justify-start">
                <button
                  onClick={() => setActiveSubTab('profitability')}
                  className={`px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 cursor-pointer ${
                    activeSubTab === 'profitability'
                      ? 'bg-amber-500 text-slate-950 shadow-md font-extrabold'
                      : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-white'
                  }`}
                >
                  <span><ThemeIcon icon="chart" className="w-4 h-4 inline-block shrink-0" /></span>
                  <span>Sözleşme Kârlılığı</span>
                </button>
                <button
                  onClick={() => setActiveSubTab('kasa')}
                  className={`px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 cursor-pointer ${
                    activeSubTab === 'kasa'
                      ? 'bg-amber-500 text-slate-950 shadow-md font-extrabold'
                      : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-white'
                  }`}
                >
                  <span><ThemeIcon icon="card" className="w-4 h-4 inline-block shrink-0" /></span>
                  <span>Kasa & Harcama Akışı</span>
                </button>
                <button
                  onClick={() => setActiveSubTab('monthly')}
                  className={`px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 cursor-pointer ${
                    activeSubTab === 'monthly'
                      ? 'bg-amber-500 text-slate-950 shadow-md font-extrabold'
                      : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-white'
                  }`}
                >
                  <span><ThemeIcon icon="calendar" className="w-4 h-4 inline-block shrink-0" /></span>
                  <span>Aylık Nakit Raporu</span>
                </button>
              </div>
            </div>"""

    if old_header_buttons in content:
        content = content.replace(old_header_buttons, new_header_buttons)
        print(f"Cleaned header in {h_file}")

    # 2. Place the "+ Kasa Hareketi Ekle" button cleanly inside the Kasa Tab Toolbar
    old_kasa_toolbar = """          {/* TAB 2: KASA VE HARCAMA AKIŞI */}
          {activeSubTab === 'kasa' && (
            <div className="space-y-4">
              <div className="glass-panel p-4 rounded-3xl flex flex-col md:flex-row justify-between items-center gap-4 border border-slate-200 dark:border-brand-border">
                <div className="flex bg-slate-100 dark:bg-brand-card p-1 rounded-2xl border border-slate-200 dark:border-brand-border/60 w-full md:w-auto">
                  <button
                    onClick={() => setFilterTab('all')}
                    className={`px-4 py-2 text-xs font-bold rounded-xl transition flex-1 md:flex-none cursor-pointer ${
                      filterTab === 'all' ? 'bg-amber-500 text-slate-950 shadow' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-white'
                    }`}
                  >
                    Tümü ({allTransactions.length})
                  </button>
                  <button
                    onClick={() => setFilterTab('income')}
                    className={`px-4 py-2 text-xs font-bold rounded-xl transition flex-1 md:flex-none cursor-pointer ${
                      filterTab === 'income' ? 'bg-emerald-600 text-white shadow' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-white'
                    }`}
                  >
                    Gelirler (+) ({incomeTransactions.length})
                  </button>
                  <button
                    onClick={() => setFilterTab('expense')}
                    className={`px-4 py-2 text-xs font-bold rounded-xl transition flex-1 md:flex-none cursor-pointer ${
                      filterTab === 'expense' ? 'bg-red-600 text-white shadow' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-white'
                    }`}
                  >
                    Giderler (-) ({expenseTransactions.length})
                  </button>
                </div>

                <div className="relative w-full md:w-80">
                  <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"><ThemeIcon icon="search" className="w-4 h-4 inline-block shrink-0" /></span>
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={e => setSearchQuery(e.target.value)}
                    placeholder="Kasa hareketlerinde ara..."
                    className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl pl-9 pr-4 py-2 text-xs font-bold text-slate-800 dark:text-gray-100 placeholder:text-slate-400 focus:outline-none focus:border-amber-500"
                  />
                </div>
              </div>"""

    new_kasa_toolbar = """          {/* TAB 2: KASA VE HARCAMA AKIŞI */}
          {activeSubTab === 'kasa' && (
            <div className="space-y-4">
              <div className="glass-panel p-4 rounded-3xl flex flex-col lg:flex-row justify-between items-stretch lg:items-center gap-3 border border-slate-200 dark:border-brand-border shadow-sm">
                <div className="flex bg-slate-100 dark:bg-brand-card p-1 rounded-2xl border border-slate-200 dark:border-brand-border/60 w-full lg:w-auto">
                  <button
                    onClick={() => setFilterTab('all')}
                    className={`px-4 py-2 text-xs font-bold rounded-xl transition flex-1 lg:flex-none cursor-pointer ${
                      filterTab === 'all' ? 'bg-amber-500 text-slate-950 shadow font-extrabold' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-white'
                    }`}
                  >
                    Tümü ({allTransactions.length})
                  </button>
                  <button
                    onClick={() => setFilterTab('income')}
                    className={`px-4 py-2 text-xs font-bold rounded-xl transition flex-1 lg:flex-none cursor-pointer ${
                      filterTab === 'income' ? 'bg-emerald-600 text-white shadow font-extrabold' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-white'
                    }`}
                  >
                    Gelirler (+) ({incomeTransactions.length})
                  </button>
                  <button
                    onClick={() => setFilterTab('expense')}
                    className={`px-4 py-2 text-xs font-bold rounded-xl transition flex-1 lg:flex-none cursor-pointer ${
                      filterTab === 'expense' ? 'bg-red-600 text-white shadow font-extrabold' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-white'
                    }`}
                  >
                    Giderler (-) ({expenseTransactions.length})
                  </button>
                </div>

                <div className="flex items-center space-x-2.5 w-full lg:w-auto">
                  <div className="relative flex-1 lg:w-72">
                    <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"><ThemeIcon icon="search" className="w-4 h-4 inline-block shrink-0" /></span>
                    <input
                      type="text"
                      value={searchQuery}
                      onChange={e => setSearchQuery(e.target.value)}
                      placeholder="Kasa hareketlerinde ara..."
                      className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl pl-9 pr-4 py-2 text-xs font-bold text-slate-800 dark:text-gray-100 placeholder:text-slate-400 focus:outline-none focus:border-amber-500"
                    />
                  </div>
                  <button
                    onClick={() => {
                      setTransType('gider');
                      setIsModalOpen(true);
                    }}
                    className="px-4 py-2 gold-button font-extrabold text-xs rounded-xl shadow cursor-pointer flex items-center space-x-1.5 shrink-0 hover:scale-[1.02] transition"
                  >
                    <span>+ Kasa Hareketi Ekle</span>
                  </button>
                </div>
              </div>"""

    if old_kasa_toolbar in content:
        content = content.replace(old_kasa_toolbar, new_kasa_toolbar)
        print(f"Updated kasa toolbar in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Kasa button and toolbar successfully upgraded across all files!")
