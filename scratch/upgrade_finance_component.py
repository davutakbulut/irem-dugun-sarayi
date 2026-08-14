import os, re

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

new_finance_component_code = """    // --- COMPREHENSIVE FINANCE & CASHFLOW COMPONENT WITH MULTI-INCOME/EXPENSE & MONTHLY REPORTING ---
    function FinanceComponent({ financialStats, reservations = [], venues = [], services = [], expenses = [], setExpenses = () => {}, onUpdateReservation }) {
      const [expandedResIds, setExpandedResIds] = useState({});
      const toggleExpandRes = (resId) => {
        setExpandedResIds(prev => ({
          ...prev,
          [resId]: !prev[resId]
        }));
      };

      const [activeSubTab, setActiveSubTab] = useState('profitability'); // 'profitability' | 'kasa' | 'monthly'
      const [filterTab, setFilterTab] = useState('all'); // 'all' | 'income' | 'expense'
      const [searchQuery, setSearchQuery] = useState('');
      const [isModalOpen, setIsModalOpen] = useState(false);
      
      // Selected Reservation for Custom Expense Modal
      const [customExpenseModalRes, setCustomExpenseModalRes] = useState(null);
      const [newResExpTitle, setNewResExpTitle] = useState('');
      const [newResExpAmount, setNewResExpAmount] = useState('');
      const [newResExpCategory, setNewResExpCategory] = useState('Personel & Yevmiye');

      const [currentPage, setCurrentPage] = useState(1);
      const [pageSize, setPageSize] = useState(10);

      // Selected Month for Monthly Cashflow Report
      const [selectedReportMonth, setSelectedReportMonth] = useState('2026-08');

      useEffect(() => {
        setCurrentPage(1);
      }, [filterTab, searchQuery, activeSubTab, selectedReportMonth]);

      // General Cashflow Transaction Modal State (Income vs Expense)
      const [transType, setTransType] = useState('gider'); // 'gelir' | 'gider'
      const [newTitle, setNewTitle] = useState('');
      const [newCategory, setNewCategory] = useState('Faturalar & Enerji');
      const [newAmount, setNewAmount] = useState('');
      const [newDate, setNewDate] = useState(new Date().toISOString().split('T')[0]);
      const [newStatus, setNewStatus] = useState('Tamamlandı');

      // Update default category when transType changes
      useEffect(() => {
        if (transType === 'gelir') {
          setNewCategory('Dış Çekim & Plato');
        } else {
          setNewCategory('Faturalar & Enerji');
        }
      }, [transType]);

      // 1. RESERVATION ITEMIZED FINANCIAL & PROFITABILITY CALCULATION
      const reservationFinancials = useMemo(() => {
        return (reservations || []).map(r => {
          const vObj = (venues || []).find(v => v.id === r.venueId);
          const venueCost = r.venueCost !== undefined ? Number(r.venueCost) : Number(vObj?.costPrice || Math.round((r.venuePrice || 60000) * 0.55));

          const servicesCost = (r.selectedServices || []).reduce((sum, s) => {
            const sObj = (services || []).find(srv => srv.id === s.serviceId);
            const uCost = s.costPrice !== undefined ? Number(s.costPrice) : (sObj?.costPrice !== undefined ? Number(sObj.costPrice) : Math.round(Number(s.unitPrice || 250) * 0.6));
            return sum + (uCost * Number(s.quantity || 1));
          }, 0);

          const customExpensesList = r.customExpenses || [];
          const customExpensesTotal = customExpensesList.reduce((sum, exp) => sum + Number(exp.amount || 0), 0);

          const grossIncome = Number(r.totalAmount || 0);
          const totalCost = Math.round(venueCost + servicesCost + customExpensesTotal);
          const netProfit = Math.round(grossIncome - totalCost);
          const profitMargin = grossIncome > 0 ? ((netProfit / grossIncome) * 100).toFixed(1) : '0.0';

          return {
            reservation: r,
            venueName: vObj?.name || r.venueName || r.venueId,
            grossIncome,
            venueCost,
            servicesCost,
            customExpensesList,
            customExpensesTotal,
            totalCost,
            netProfit,
            profitMargin: Number(profitMargin)
          };
        });
      }, [reservations, venues, services]);

      // Global Summary Totals for Contracts
      const totalGrossRevenue = useMemo(() => {
        return reservationFinancials.reduce((sum, rf) => sum + rf.grossIncome, 0);
      }, [reservationFinancials]);

      const totalCalculatedCosts = useMemo(() => {
        return reservationFinancials.reduce((sum, rf) => sum + rf.totalCost, 0);
      }, [reservationFinancials]);

      const totalNetProfit = totalGrossRevenue - totalCalculatedCosts;
      const avgProfitMargin = totalGrossRevenue > 0 ? ((totalNetProfit / totalGrossRevenue) * 100).toFixed(1) : '0.0';

      // 2. UNIFIED CASH INFLOWS (Rezervasyon Parçalı Tahsilatları + Harici Gelirler)
      const incomeTransactions = useMemo(() => {
        const list = [];
        // From Reservations (itemized payments)
        (reservations || []).forEach(r => {
          if (Array.isArray(r.payments) && r.payments.length > 0) {
            r.payments.forEach(p => {
              list.push({
                id: p.id || `pay-${r.id}-${Math.random()}`,
                resId: r.id,
                title: `${r.customerName} - ${p.type || 'Tahsilat'} (${p.method || 'Kasa'})`,
                category: 'Rezervasyon Tahsilatı',
                type: 'gelir',
                amount: Number(p.amount || 0),
                date: p.date || r.date || '2026-08-01',
                status: 'Tahsil Edildi',
                isReservationPayment: true
              });
            });
          } else if (Number(r.depositPaid || 0) > 0) {
            list.push({
              id: `inc-${r.id}-deposit`,
              resId: r.id,
              title: `${r.customerName} - Kapora / Ödeme`,
              category: 'Rezervasyon Tahsilatı',
              type: 'gelir',
              amount: Number(r.depositPaid || 0),
              date: r.date || '2026-08-01',
              status: 'Tahsil Edildi',
              isReservationPayment: true
            });
          }
        });

        // From External Incomes in expenses table
        (expenses || []).filter(e => e.type === 'gelir' || e.type === 'income').forEach(e => {
          list.push({
            id: e.id,
            title: e.title,
            category: e.category || 'Harici Gelir',
            type: 'gelir',
            amount: Number(e.amount || 0),
            date: e.date || '2026-08-01',
            status: 'Tahsil Edildi',
            isExternal: true
          });
        });

        return list;
      }, [reservations, expenses]);

      // 3. UNIFIED CASH OUTFLOWS (Harici Giderler + Rezervasyon Özel Harcamaları)
      const expenseTransactions = useMemo(() => {
        const list = [];
        // External general expenses
        (expenses || []).filter(e => e.type !== 'gelir' && e.type !== 'income').forEach(e => {
          list.push({
            id: e.id,
            title: e.title,
            category: e.category || 'Genel Gider',
            type: 'gider',
            amount: Number(e.amount || 0),
            date: e.date || '2026-08-01',
            status: e.status || 'Ödendi',
            isExternal: true
          });
        });

        // Reservation specific custom expenses
        (reservations || []).forEach(r => {
          if (Array.isArray(r.customExpenses)) {
            r.customExpenses.forEach(exp => {
              list.push({
                id: exp.id || `resexp-${r.id}-${Math.random()}`,
                resId: r.id,
                title: `${r.customerName} - ${exp.title}`,
                category: exp.category || 'Etkinlik Özel Gideri',
                type: 'gider',
                amount: Number(exp.amount || 0),
                date: exp.date || r.date || '2026-08-01',
                status: 'Ödendi',
                isReservationCustomExpense: true
              });
            });
          }
        });

        return list;
      }, [expenses, reservations]);

      // Unified Ledger
      const allTransactions = useMemo(() => {
        return [...incomeTransactions, ...expenseTransactions].sort((a, b) => new Date(b.date) - new Date(a.date));
      }, [incomeTransactions, expenseTransactions]);

      // Totals
      const totalCashInflow = useMemo(() => incomeTransactions.reduce((sum, t) => sum + t.amount, 0), [incomeTransactions]);
      const totalCashOutflow = useMemo(() => expenseTransactions.reduce((sum, t) => sum + t.amount, 0), [expenseTransactions]);
      const netCashBalance = totalCashInflow - totalCashOutflow;

      // Filtered Transactions
      const filteredTransactions = useMemo(() => {
        return allTransactions.filter(t => {
          if (filterTab === 'income' && t.type !== 'gelir') return false;
          if (filterTab === 'expense' && t.type !== 'gider') return false;

          if (searchQuery.trim()) {
            const q = searchQuery.toLowerCase();
            const matchTitle = (t.title || '').toLowerCase().includes(q);
            const matchCategory = (t.category || '').toLowerCase().includes(q);
            const matchAmount = String(t.amount).includes(q);
            if (!matchTitle && !matchCategory && !matchAmount) return false;
          }
          return true;
        });
      }, [allTransactions, filterTab, searchQuery]);

      // 4. MONTHLY REPORT DATA AGGREGATION
      const monthlyReportData = useMemo(() => {
        const monthPrefix = selectedReportMonth; // e.g. '2026-08'
        const monthInflows = incomeTransactions.filter(t => (t.date || '').startsWith(monthPrefix));
        const monthOutflows = expenseTransactions.filter(t => (t.date || '').startsWith(monthPrefix));

        const sumInflow = monthInflows.reduce((sum, t) => sum + t.amount, 0);
        const sumOutflow = monthOutflows.reduce((sum, t) => sum + t.amount, 0);
        const netDiff = sumInflow - sumOutflow;

        // Group expenses by category
        const categoryMap = {};
        monthOutflows.forEach(t => {
          const cat = t.category || 'Diğer';
          categoryMap[cat] = (categoryMap[cat] || 0) + t.amount;
        });

        // Group incomes by category
        const incomeCategoryMap = {};
        monthInflows.forEach(t => {
          const cat = t.category || 'Diğer';
          incomeCategoryMap[cat] = (incomeCategoryMap[cat] || 0) + t.amount;
        });

        const monthEventsCount = (reservations || []).filter(r => (r.date || r.eventDate || '').startsWith(monthPrefix)).length;

        return {
          monthInflows,
          monthOutflows,
          sumInflow,
          sumOutflow,
          netDiff,
          categoryMap,
          incomeCategoryMap,
          monthEventsCount
        };
      }, [incomeTransactions, expenseTransactions, selectedReportMonth, reservations]);

      // Handle Add General Cash Transaction (Income or Expense)
      const handleAddGeneralTransaction = async (e) => {
        e.preventDefault();
        if (!newTitle.trim() || !newAmount) return;

        const newTrans = {
          id: `trans-${Date.now()}`,
          title: newTitle.trim(),
          category: newCategory,
          type: transType, // 'gelir' or 'gider'
          amount: Number(newAmount),
          date: newDate || new Date().toISOString().split('T')[0],
          description: `Kasa Hareketi (${transType === 'gelir' ? 'Gelir' : 'Gider'})`,
          status: newStatus
        };

        setExpenses(prev => {
          const updated = [newTrans, ...prev.filter(x => x.id !== newTrans.id)];
          try {
            const fetchFn = window.fetchWithRetry || fetch;
            fetchFn('/api/expenses', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(newTrans)
            }).catch(() => {});
          } catch(err) {}
          return updated;
        });

        setNewTitle('');
        setNewAmount('');
        setIsModalOpen(false);
      };

      const handleDeleteGeneralExpense = (expId) => {
        if (!confirm('Bu kasa hareketini silmek istediğinize emin misiniz?')) return;
        setExpenses(prev => {
          const updated = prev.filter(e => e.id !== expId);
          try {
            const fetchFn = window.fetchWithRetry || fetch;
            fetchFn(`/api/expenses/${expId}`, {
              method: 'DELETE'
            }).catch(() => {});
          } catch(err) {}
          return updated;
        });
      };

      // Add Custom Expense to Reservation
      const handleAddCustomExpenseToRes = (e) => {
        e.preventDefault();
        if (!customExpenseModalRes || !newResExpTitle.trim() || !newResExpAmount) return;

        const existingExpenses = customExpenseModalRes.customExpenses || [];
        const newExpItem = {
          id: `res-exp-${Date.now()}`,
          title: newResExpTitle.trim(),
          amount: Number(newResExpAmount),
          category: newResExpCategory,
          date: new Date().toISOString().split('T')[0]
        };

        const updatedCustomExpenses = [newExpItem, ...existingExpenses];
        const updatedReservation = { ...customExpenseModalRes, customExpenses: updatedCustomExpenses };

        if (onUpdateReservation) {
          onUpdateReservation(updatedReservation);
        }

        setCustomExpenseModalRes(updatedReservation);
        setNewResExpTitle('');
        setNewResExpAmount('');
      };

      const handleDeleteCustomExpenseFromRes = (expId) => {
        if (!customExpenseModalRes) return;
        const updatedCustomExpenses = (customExpenseModalRes.customExpenses || []).filter(e => e.id !== expId);
        const updatedReservation = { ...customExpenseModalRes, customExpenses: updatedCustomExpenses };

        if (onUpdateReservation) {
          onUpdateReservation(updatedReservation);
        }
        setCustomExpenseModalRes(updatedReservation);
      };

      return (
        <div className="space-y-6 animate-fade-in pb-12">
          
          {/* HEADER & MAIN TAB SWITCHER */}
          <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex flex-col md:flex-row justify-between items-start md:items-center gap-4 shadow-sm">
            <div>
              <h2 className="text-2xl font-heading font-extrabold gold-gradient-text flex items-center space-x-2">
                <span><ThemeIcon icon="money" className="w-5 h-5 inline-block shrink-0" /></span>
                <span>Finans Yönetimi & Kasa Nakit Akışı</span>
              </h2>
              <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">
                Sözleşme kârlılığı, parçalı tahsilatlar, harici gelir/giderler ve ay bazlı kasa nakit raporu.
              </p>
            </div>

            <div className="flex items-center space-x-2 w-full md:w-auto flex-wrap gap-2">
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
            </div>
          </div>

          {/* 3 TOP KPI CARDS */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="glass-panel p-5 rounded-3xl border border-emerald-500/30 bg-emerald-500/5 space-y-1 shadow-sm">
              <div className="flex justify-between items-center text-xs font-bold text-slate-500 dark:text-gray-400">
                <span>{activeSubTab === 'profitability' ? 'Toplam Ciro (Sözleşmeler)' : 'Fiili Kasa Girişi (+)'}</span>
                <span className="text-emerald-500 text-lg font-bold">↗</span>
              </div>
              <div className="text-2xl font-mono font-extrabold text-emerald-600 dark:text-emerald-400">
                {formatCurrency(activeSubTab === 'profitability' ? totalGrossRevenue : totalCashInflow)}
              </div>
              <div className="text-[11px] text-slate-400 font-medium">
                {activeSubTab === 'profitability' ? `${reservations.length} Adet Rezervasyon` : `${incomeTransactions.length} Adet Gelir / Tahsilat`}
              </div>
            </div>

            <div className="glass-panel p-5 rounded-3xl border border-red-500/30 bg-red-500/5 space-y-1 shadow-sm">
              <div className="flex justify-between items-center text-xs font-bold text-slate-500 dark:text-gray-400">
                <span>{activeSubTab === 'profitability' ? 'Toplam Maliyet (Etkinlikler)' : 'Fiili Kasa Çıkışı (-)'}</span>
                <span className="text-red-500 text-lg font-bold">↘</span>
              </div>
              <div className="text-2xl font-mono font-extrabold text-red-600 dark:text-red-400">
                {formatCurrency(activeSubTab === 'profitability' ? totalCalculatedCosts : totalCashOutflow)}
              </div>
              <div className="text-[11px] text-slate-400 font-medium">
                {activeSubTab === 'profitability' ? 'Salon + Hizmet + Özel Giderler' : `${expenseTransactions.length} Adet Gider Kalemi`}
              </div>
            </div>

            <div className="glass-panel p-5 rounded-3xl border border-amber-500/40 bg-amber-500/5 space-y-1 shadow-sm">
              <div className="flex justify-between items-center text-xs font-bold text-slate-500 dark:text-gray-400">
                <span>{activeSubTab === 'profitability' ? 'Net Kâr (Kâr Marjı %' + avgProfitMargin + ')' : 'Net Kasa Dengesi (+/-)'}</span>
                <span className="text-amber-500 text-lg font-bold">★</span>
              </div>
              <div className={`text-2xl font-mono font-extrabold ${(activeSubTab === 'profitability' ? totalNetProfit : netCashBalance) >= 0 ? 'text-emerald-600 dark:text-gold-400' : 'text-red-600'}`}>
                {formatCurrency(activeSubTab === 'profitability' ? totalNetProfit : netCashBalance)}
              </div>
              <div className="text-[11px] text-slate-400 font-medium">
                {activeSubTab === 'profitability' ? 'Sözleşme Bazlı Net Kârlılık' : 'Kasada Kalan Net Nakit'}
              </div>
            </div>
          </div>

          {/* TAB 1: SÖZLEŞME BAZLI KÂRLILIK VE DETAY DÖKÜMÜ */}
          {activeSubTab === 'profitability' && (
            <div className="space-y-4">
              <div className="glass-panel p-4 rounded-3xl flex justify-between items-center gap-4 border border-slate-200 dark:border-brand-border">
                <div className="relative w-full md:w-80">
                  <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"><ThemeIcon icon="search" className="w-4 h-4 inline-block shrink-0" /></span>
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={e => setSearchQuery(e.target.value)}
                    placeholder="Müşteri, salon veya sözleşme ara..."
                    className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl pl-9 pr-4 py-2 text-xs font-bold text-slate-800 dark:text-gray-100 placeholder:text-slate-400 focus:outline-none focus:border-amber-500"
                  />
                </div>
              </div>

              <div className="glass-panel rounded-3xl border border-slate-200 dark:border-brand-border overflow-hidden shadow-sm">
                <div className="overflow-x-auto custom-scrollbar">
                  <table className="w-full text-left text-xs border-collapse">
                    <thead>
                      <tr className="bg-slate-100/80 dark:bg-brand-card/80 border-b border-slate-200 dark:border-brand-border text-slate-600 dark:text-gray-300 font-bold uppercase tracking-wider">
                        <th className="p-3.5">Sözleşme & Müşteri</th>
                        <th className="p-3.5">Etkinlik Tarihi</th>
                        <th className="p-3.5 text-right">Ciro (Gelir)</th>
                        <th className="p-3.5 text-right">Maliyet</th>
                        <th className="p-3.5 text-right">Özel Gider</th>
                        <th className="p-3.5 text-right">Net Kâr</th>
                        <th className="p-3.5 text-center">Kâr %</th>
                        <th className="p-3.5 text-center">İşlem</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 dark:divide-brand-border/40 font-medium">
                      {filteredProfitabilityRows.length === 0 ? (
                        <tr>
                          <td colSpan="8" className="text-center py-8 text-slate-400 font-bold">
                            Kayıtlı rezervasyon finansmanı bulunamadı.
                          </td>
                        </tr>
                      ) : (
                        filteredProfitabilityRows
                          .slice((currentPage - 1) * pageSize, currentPage * pageSize)
                          .map(rf => {
                            const r = rf.reservation;
                            const isExpanded = !!expandedResIds[r.id];
                            return (
                              <React.Fragment key={r.id}>
                                <tr className="hover:bg-slate-50/60 dark:hover:bg-brand-card/50 transition">
                                  <td className="p-3.5">
                                    <div className="font-bold text-slate-800 dark:text-gray-100">{r.customerName}</div>
                                    <div className="text-[10px] text-slate-400 font-mono">{r.id} • {rf.venueName}</div>
                                  </td>
                                  <td className="p-3.5 whitespace-nowrap font-mono text-slate-600 dark:text-gray-300">
                                    {formatDate(r.date || r.eventDate)}
                                  </td>
                                  <td className="p-3.5 text-right font-mono font-bold text-slate-800 dark:text-gray-100">
                                    {formatCurrency(rf.grossIncome)}
                                  </td>
                                  <td className="p-3.5 text-right font-mono text-red-500 dark:text-red-400 font-bold">
                                    {formatCurrency(rf.venueCost + rf.servicesCost)}
                                  </td>
                                  <td className="p-3.5 text-right font-mono font-bold">
                                    {rf.customExpensesTotal > 0 ? (
                                      <button
                                        type="button"
                                        onClick={() => setCustomExpenseModalRes(r)}
                                        className="text-amber-600 dark:text-gold-400 hover:underline cursor-pointer flex items-center justify-end space-x-1 ml-auto"
                                        title="Ek giderleri yönet"
                                      >
                                        <span>{formatCurrency(rf.customExpensesTotal)}</span>
                                        <span className="text-[9px] font-extrabold bg-amber-500/10 px-1 rounded">({rf.customExpensesList.length})</span>
                                      </button>
                                    ) : (
                                      <button
                                        type="button"
                                        onClick={() => setCustomExpenseModalRes(r)}
                                        className="text-[10px] text-slate-400 hover:text-amber-500 hover:underline cursor-pointer"
                                      >
                                        + Gider Ekle
                                      </button>
                                    )}
                                  </td>
                                  <td className={`p-3.5 text-right font-mono font-extrabold ${rf.netProfit >= 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600'}`}>
                                    {formatCurrency(rf.netProfit)}
                                  </td>
                                  <td className="p-3.5 text-center whitespace-nowrap">
                                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-extrabold ${rf.profitMargin >= 35 ? 'bg-emerald-500/10 text-emerald-600' : (rf.profitMargin > 0 ? 'bg-amber-500/10 text-amber-600' : 'bg-red-500/10 text-red-600')}`}>
                                      %{rf.profitMargin}
                                    </span>
                                  </td>
                                  <td className="p-3.5 text-center whitespace-nowrap">
                                    <div className="flex items-center justify-center space-x-1.5">
                                      <button
                                        type="button"
                                        onClick={() => toggleExpandRes(r.id)}
                                        className="px-2 py-1 bg-slate-100 dark:bg-brand-dark hover:bg-slate-200 text-slate-600 dark:text-gray-300 rounded-lg text-[10px] font-bold transition cursor-pointer"
                                      >
                                        {isExpanded ? '▲ Kapat' : '▼ Detay'}
                                      </button>
                                      <button
                                        type="button"
                                        onClick={() => setCustomExpenseModalRes(r)}
                                        className="px-2 py-1 bg-amber-500/10 hover:bg-amber-500 text-amber-700 hover:text-white rounded-lg text-[10px] font-bold transition cursor-pointer border border-amber-500/30"
                                      >
                                        + Ek Gider
                                      </button>
                                    </div>
                                  </td>
                                </tr>

                                {isExpanded && (
                                  <tr className="bg-slate-50/80 dark:bg-brand-dark/50">
                                    <td colSpan="8" className="p-4">
                                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
                                        <div className="p-3 bg-white dark:bg-brand-card rounded-xl border border-slate-200 dark:border-brand-border space-y-1">
                                          <span className="text-[10px] font-bold text-slate-400 uppercase">Mekan Maliyeti</span>
                                          <div className="font-mono font-bold text-slate-800 dark:text-gray-200">{formatCurrency(rf.venueCost)}</div>
                                        </div>
                                        <div className="p-3 bg-white dark:bg-brand-card rounded-xl border border-slate-200 dark:border-brand-border space-y-1">
                                          <span className="text-[10px] font-bold text-slate-400 uppercase">Ek Hizmetler Maliyeti</span>
                                          <div className="font-mono font-bold text-slate-800 dark:text-gray-200">{formatCurrency(rf.servicesCost)}</div>
                                        </div>
                                        <div className="p-3 bg-white dark:bg-brand-card rounded-xl border border-slate-200 dark:border-brand-border space-y-1">
                                          <span className="text-[10px] font-bold text-slate-400 uppercase">Özel Harcamalar & Yevmiyeler</span>
                                          <div className="font-mono font-bold text-amber-600 dark:text-gold-400">{formatCurrency(rf.customExpensesTotal)}</div>
                                        </div>
                                      </div>
                                    </td>
                                  </tr>
                                )}
                              </React.Fragment>
                            );
                          })
                      )}
                    </tbody>
                  </table>
                </div>

                <Pagination
                  currentPage={currentPage}
                  totalItems={filteredProfitabilityRows.length}
                  pageSize={pageSize}
                  onPageChange={setCurrentPage}
                  onPageSizeChange={setPageSize}
                />
              </div>
            </div>
          )}

          {/* TAB 2: KASA VE HARCAMA AKIŞI */}
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
              </div>

              <div className="glass-panel rounded-3xl border border-slate-200 dark:border-brand-border overflow-hidden shadow-sm">
                <div className="overflow-x-auto custom-scrollbar">
                  <table className="w-full text-left text-xs border-collapse">
                    <thead>
                      <tr className="bg-slate-100/80 dark:bg-brand-card/80 border-b border-slate-200 dark:border-brand-border text-slate-600 dark:text-gray-300 font-bold uppercase tracking-wider">
                        <th className="p-3.5">Tarih</th>
                        <th className="p-3.5">Açıklama & Hareket</th>
                        <th className="p-3.5">Kategori</th>
                        <th className="p-3.5 text-center">Tür</th>
                        <th className="p-3.5 text-right">Tutar</th>
                        <th className="p-3.5 text-center">Durum</th>
                        <th className="p-3.5 text-center">İşlem</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 dark:divide-brand-border/40 font-medium">
                      {filteredTransactions.length === 0 ? (
                        <tr>
                          <td colSpan="7" className="text-center py-8 text-slate-400 font-bold">
                            Kasa hareketi bulunamadı.
                          </td>
                        </tr>
                      ) : (
                        filteredTransactions
                          .slice((currentPage - 1) * pageSize, currentPage * pageSize)
                          .map(t => (
                          <tr key={t.id} className="hover:bg-slate-50/60 dark:hover:bg-brand-card/50 transition">
                            <td className="p-3.5 whitespace-nowrap font-mono text-slate-600 dark:text-gray-400">{formatDate(t.date)}</td>
                            <td className="p-3.5 font-bold text-slate-800 dark:text-gray-100">
                              <div>{t.title}</div>
                              {t.resId && <span className="text-[10px] text-amber-600 dark:text-gold-400 font-mono">{t.resId}</span>}
                            </td>
                            <td className="p-3.5">
                              <span className="bg-slate-100 dark:bg-brand-dark px-2.5 py-1 rounded-lg text-[10px] font-bold text-slate-600 dark:text-gray-300 border border-slate-200 dark:border-brand-border">
                                {t.category}
                              </span>
                            </td>
                            <td className="p-3.5 text-center whitespace-nowrap">
                              {t.type === 'gelir' ? (
                                <span className="bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20 font-bold text-[10px] px-2.5 py-1 rounded-full">
                                  + Gelir
                                </span>
                              ) : (
                                <span className="bg-red-500/10 text-red-600 dark:text-red-400 border border-red-500/20 font-bold text-[10px] px-2.5 py-1 rounded-full">
                                  - Gider
                                </span>
                              )}
                            </td>
                            <td className={`p-3.5 text-right font-bold text-sm whitespace-nowrap ${t.type === 'gelir' ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400'}`}>
                              {t.type === 'gelir' ? '+' : '-'}{formatCurrency(t.amount)}
                            </td>
                            <td className="p-3.5 text-center whitespace-nowrap">
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-600 dark:text-emerald-400">
                                {t.status}
                              </span>
                            </td>
                            <td className="p-3.5 text-center whitespace-nowrap">
                              {t.isExternal ? (
                                <button
                                  type="button"
                                  onClick={() => handleDeleteGeneralExpense(t.id)}
                                  className="px-2 py-1 bg-red-500/10 hover:bg-red-500 text-red-600 hover:text-white rounded-lg text-[10px] font-bold transition cursor-pointer border border-red-500/20"
                                  title="Bu kasa hareketini sil"
                                >
                                  🗑️ Sil
                                </button>
                              ) : (
                                <span className="text-[10px] text-slate-400 font-mono" title="Rezervasyon üzerinden yönetilir">Sözleşmeli</span>
                              )}
                            </td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>

                <Pagination
                  currentPage={currentPage}
                  totalItems={filteredTransactions.length}
                  pageSize={pageSize}
                  onPageChange={setCurrentPage}
                  onPageSizeChange={setPageSize}
                />
              </div>
            </div>
          )}

          {/* TAB 3: AYLIK NAKİT AKIŞI VE KASA RAPORU */}
          {activeSubTab === 'monthly' && (
            <div className="space-y-6">
              {/* MONTH PICKER & QUICK STATS */}
              <div className="glass-panel p-5 rounded-3xl border border-slate-200 dark:border-brand-border flex flex-col sm:flex-row justify-between items-center gap-4">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 rounded-xl bg-amber-500/10 text-amber-600 font-bold flex items-center justify-center text-lg">
                    <ThemeIcon icon="calendar" className="w-5 h-5 shrink-0" />
                  </div>
                  <div>
                    <h3 className="font-extrabold text-base text-slate-800 dark:text-gray-100">Raporlanacak Ayı Seçin</h3>
                    <p className="text-xs text-slate-400">Kasaya fiilen giren ve çıkan nakit hareketleri</p>
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <select
                    value={selectedReportMonth}
                    onChange={e => setSelectedReportMonth(e.target.value)}
                    className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-xl px-4 py-2 text-xs font-bold text-slate-800 dark:text-gray-100 cursor-pointer shadow-xs focus:outline-none"
                  >
                    <option value="2026-05">Mayıs 2026</option>
                    <option value="2026-06">Haziran 2026</option>
                    <option value="2026-07">Temmuz 2026</option>
                    <option value="2026-08">Ağustos 2026</option>
                    <option value="2026-09">Eylül 2026</option>
                    <option value="2026-10">Ekim 2026</option>
                    <option value="2026-11">Kasım 2026</option>
                    <option value="2026-12">Aralık 2026</option>
                  </select>
                </div>
              </div>

              {/* MONTHLY KPI 4-GRID */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="glass-panel p-5 rounded-3xl border border-emerald-500/30 bg-emerald-500/5 space-y-1">
                  <span className="text-[11px] font-bold text-slate-500 uppercase">Bu Ay Kasa Girişi (+)</span>
                  <div className="text-2xl font-mono font-extrabold text-emerald-600 dark:text-emerald-400">
                    {formatCurrency(monthlyReportData.sumInflow)}
                  </div>
                  <div className="text-[10px] text-slate-400">{monthlyReportData.monthInflows.length} Adet Tahsilat / Gelir</div>
                </div>

                <div className="glass-panel p-5 rounded-3xl border border-red-500/30 bg-red-500/5 space-y-1">
                  <span className="text-[11px] font-bold text-slate-500 uppercase">Bu Ay Kasa Çıkışı (-)</span>
                  <div className="text-2xl font-mono font-extrabold text-red-600 dark:text-red-400">
                    {formatCurrency(monthlyReportData.sumOutflow)}
                  </div>
                  <div className="text-[10px] text-slate-400">{monthlyReportData.monthOutflows.length} Adet Gider / Harcama</div>
                </div>

                <div className="glass-panel p-5 rounded-3xl border border-amber-500/40 bg-amber-500/5 space-y-1">
                  <span className="text-[11px] font-bold text-slate-500 uppercase">Net Kasa Farkı (+ / -)</span>
                  <div className={`text-2xl font-mono font-extrabold ${monthlyReportData.netDiff >= 0 ? 'text-emerald-600 dark:text-gold-400' : 'text-red-600'}`}>
                    {formatCurrency(monthlyReportData.netDiff)}
                  </div>
                  <div className="text-[10px] text-slate-400">Seçili Ayın Net Kasa Biyesi</div>
                </div>

                <div className="glass-panel p-5 rounded-3xl border border-slate-200 dark:border-brand-border space-y-1">
                  <span className="text-[11px] font-bold text-slate-500 uppercase">Bu Ayki Düğün / Etkinlik</span>
                  <div className="text-2xl font-mono font-extrabold text-slate-800 dark:text-gray-100">
                    {monthlyReportData.monthEventsCount} Adet
                  </div>
                  <div className="text-[10px] text-slate-400">Bu ay salonlarda icra edilen</div>
                </div>
              </div>

              {/* MONTHLY EXPENSES CATEGORY BREAKDOWN CARDS */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border space-y-4">
                  <h4 className="font-extrabold text-sm text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                    <span className="text-red-500">↘</span>
                    <span>Seçili Ay Gider Dağılımı (Kategori Bazlı)</span>
                  </h4>
                  <div className="space-y-2.5">
                    {Object.keys(monthlyReportData.categoryMap).length === 0 ? (
                      <div className="text-center py-6 text-slate-400 text-xs font-medium">Bu ay için henüz gider kaydı bulunmuyor.</div>
                    ) : (
                      Object.entries(monthlyReportData.categoryMap).map(([cat, amt]) => {
                        const pct = monthlyReportData.sumOutflow > 0 ? Math.round((amt / monthlyReportData.sumOutflow) * 100) : 0;
                        return (
                          <div key={cat} className="space-y-1">
                            <div className="flex justify-between items-center text-xs font-bold">
                              <span className="text-slate-700 dark:text-gray-300">{cat}</span>
                              <span className="font-mono text-red-500">{formatCurrency(amt)} (%{pct})</span>
                            </div>
                            <div className="w-full h-1.5 bg-slate-100 dark:bg-brand-dark rounded-full overflow-hidden">
                              <div className="h-full bg-red-500 rounded-full" style={{ width: `${pct}%` }}></div>
                            </div>
                          </div>
                        );
                      })
                    )}
                  </div>
                </div>

                <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border space-y-4">
                  <h4 className="font-extrabold text-sm text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                    <span className="text-emerald-500">↗</span>
                    <span>Seçili Ay Gelir Dağılımı (Kategori Bazlı)</span>
                  </h4>
                  <div className="space-y-2.5">
                    {Object.keys(monthlyReportData.incomeCategoryMap).length === 0 ? (
                      <div className="text-center py-6 text-slate-400 text-xs font-medium">Bu ay için henüz tahsilat kaydı bulunmuyor.</div>
                    ) : (
                      Object.entries(monthlyReportData.incomeCategoryMap).map(([cat, amt]) => {
                        const pct = monthlyReportData.sumInflow > 0 ? Math.round((amt / monthlyReportData.sumInflow) * 100) : 0;
                        return (
                          <div key={cat} className="space-y-1">
                            <div className="flex justify-between items-center text-xs font-bold">
                              <span className="text-slate-700 dark:text-gray-300">{cat}</span>
                              <span className="font-mono text-emerald-600 dark:text-emerald-400">{formatCurrency(amt)} (%{pct})</span>
                            </div>
                            <div className="w-full h-1.5 bg-slate-100 dark:bg-brand-dark rounded-full overflow-hidden">
                              <div className="h-full bg-emerald-500 rounded-full" style={{ width: `${pct}%` }}></div>
                            </div>
                          </div>
                        );
                      })
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* DEDICATED RESERVATION CUSTOM EXPENSE MANAGEMENT MODAL */}
          {customExpenseModalRes && (
            <div className="fixed inset-0 z-[99999] bg-black/80 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in">
              <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-lg w-full p-6 space-y-4 shadow-2xl max-h-[90vh] overflow-y-auto custom-scrollbar my-auto">
                <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border">
                  <div>
                    <span className="text-[10px] font-mono font-extrabold text-amber-600 dark:text-gold-400 uppercase tracking-wider">Rezervasyona Özel Harcama Yönetimi</span>
                    <h3 className="text-lg font-heading font-extrabold text-slate-900 dark:text-white">
                      <ThemeIcon icon="document" className="w-4 h-4 inline-block shrink-0" /> {customExpenseModalRes.id} - {customExpenseModalRes.customerName}
                    </h3>
                  </div>
                  <button onClick={() => setCustomExpenseModalRes(null)} className="w-8 h-8 rounded-full bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-300 font-bold flex items-center justify-center hover:bg-slate-200">✕</button>
                </div>

                {/* ADD NEW EXPENSE FORM */}
                <form onSubmit={handleAddCustomExpenseToRes} className="p-4 bg-amber-500/10 rounded-2xl border border-amber-500/30 space-y-3 text-xs">
                  <span className="font-extrabold block text-slate-800 dark:text-gray-100 flex items-center space-x-1">
                    <span><ThemeIcon icon="plus" className="w-4 h-4 inline-block shrink-0" /> Yeni Ek Gider Kalemi Ekle:</span>
                  </span>

                  <div className="space-y-2">
                    <input
                      type="text"
                      placeholder="Gider Açıklaması (Örn: Ekstra Orkestra, Garson Mesai, Sürpriz Volkan)"
                      value={newResExpTitle}
                      onChange={e => setNewResExpTitle(e.target.value)}
                      required
                      className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-xs text-slate-800 dark:text-gray-100 font-medium"
                    />

                    <div className="grid grid-cols-2 gap-2">
                      <div>
                        <select
                          value={newResExpCategory}
                          onChange={e => setNewResExpCategory(e.target.value)}
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-xs text-slate-800 dark:text-gray-100 font-bold"
                        >
                          <option value="Personel & Yevmiye">Personel & Yevmiye</option>
                          <option value="Dekorasyon & Çiçek">Dekorasyon & Çiçek</option>
                          <option value="Ses, Sahne & Sanatçı">Ses, Sahne & Sanatçı</option>
                          <option value="Mutfak & İkram">Mutfak & İkram</option>
                          <option value="Fotoğraf & Video Ekstra">Fotoğraf & Video Ekstra</option>
                          <option value="Diğer Özel Harcama">Diğer Özel Harcama</option>
                        </select>
                      </div>
                      <div>
                        <input
                          type="number"
                          placeholder="Tutar (TL)"
                          value={newResExpAmount}
                          onChange={e => setNewResExpAmount(e.target.value)}
                          required
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-xs font-mono font-bold text-slate-800 dark:text-gray-100"
                        />
                      </div>
                    </div>

                    <button
                      type="submit"
                      className="w-full gold-button font-bold py-2 rounded-xl text-xs shadow-sm hover:scale-[1.01] transition"
                    >
                      + Bu Rezervasyona Gideri Ekle
                    </button>
                  </div>
                </form>

                {/* CURRENT CUSTOM EXPENSES LIST */}
                <div className="space-y-2">
                  <span className="font-extrabold text-xs block text-slate-700 dark:text-gray-300">
                    Kayıtlı Özel Ek Giderler ({(customExpenseModalRes.customExpenses || []).length}):
                  </span>
                  {(!customExpenseModalRes.customExpenses || customExpenseModalRes.customExpenses.length === 0) ? (
                    <div className="text-center py-4 text-slate-400 text-xs border border-dashed rounded-xl border-slate-200 dark:border-brand-border">
                      Bu rezervasyona ait özel ek harcama girilmemiş.
                    </div>
                  ) : (
                    <div className="space-y-1.5 max-h-48 overflow-y-auto custom-scrollbar">
                      {customExpenseModalRes.customExpenses.map(exp => (
                        <div key={exp.id} className="flex justify-between items-center p-2.5 bg-slate-50 dark:bg-brand-dark rounded-xl border border-slate-200 dark:border-brand-border text-xs">
                          <div>
                            <div className="font-bold text-slate-800 dark:text-gray-200">{exp.title}</div>
                            <div className="text-[10px] text-slate-400">{exp.category}</div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <span className="font-mono font-bold text-red-500">{formatCurrency(exp.amount)}</span>
                            <button
                              type="button"
                              onClick={() => handleDeleteCustomExpenseFromRes(exp.id)}
                              className="text-red-500 hover:text-red-700 w-5 h-5 flex items-center justify-center rounded bg-red-500/10 hover:bg-red-500/20 text-xs"
                            >
                              ✕
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                <div className="pt-3 border-t border-slate-200 dark:border-brand-border flex justify-end">
                  <button
                    type="button"
                    onClick={() => setCustomExpenseModalRes(null)}
                    className="px-5 py-2 bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 rounded-xl font-bold text-xs cursor-pointer"
                  >
                    Kapat
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* GENERAL CASHFLOW TRANSACTION MODAL (GELİR / GİDER SEÇİMLİ) */}
          {isModalOpen && (
            <div className="fixed inset-0 z-[99999] bg-black/80 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in">
              <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-md w-full p-6 space-y-4 shadow-2xl">
                <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border">
                  <h3 className="text-lg font-bold text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                    <span><ThemeIcon icon="money" className="w-5 h-5 inline-block shrink-0" /></span>
                    <span>Yeni Kasa Hareketi Ekle</span>
                  </h3>
                  <button onClick={() => setIsModalOpen(false)} className="text-slate-400 hover:text-white font-bold cursor-pointer">✕</button>
                </div>

                {/* TYPE SWITCHER: GELİR (+) vs GİDER (-) */}
                <div className="grid grid-cols-2 gap-2 p-1 bg-slate-100 dark:bg-brand-dark rounded-2xl border border-slate-200 dark:border-brand-border">
                  <button
                    type="button"
                    onClick={() => setTransType('gelir')}
                    className={`py-2 rounded-xl text-xs font-extrabold transition cursor-pointer flex items-center justify-center space-x-1.5 ${
                      transType === 'gelir' ? 'bg-emerald-600 text-white shadow-md' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900'
                    }`}
                  >
                    <span>+ Harici Gelir (+)</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => setTransType('gider')}
                    className={`py-2 rounded-xl text-xs font-extrabold transition cursor-pointer flex items-center justify-center space-x-1.5 ${
                      transType === 'gider' ? 'bg-red-600 text-white shadow-md' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900'
                    }`}
                  >
                    <span>- Harici Gider (-)</span>
                  </button>
                </div>

                <form onSubmit={handleAddGeneralTransaction} className="space-y-3 text-xs">
                  <div>
                    <label className="font-bold block mb-1">Harcama / Gelir Açıklaması:</label>
                    <input
                      type="text"
                      value={newTitle}
                      onChange={e => setNewTitle(e.target.value)}
                      placeholder={transType === 'gelir' ? 'Örn: Dış Fotoğraf Çekim Alanı Kiralama' : 'Örn: Temmuz Ayı Elektrik Faturası Ödemesi'}
                      required
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                    />
                  </div>

                  <div>
                    <label className="font-bold block mb-1">Kategori:</label>
                    <select
                      value={newCategory}
                      onChange={e => setNewCategory(e.target.value)}
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                    >
                      {transType === 'gelir' ? (
                        <>
                          <option value="Dış Çekim & Plato">📷 Dış Çekim & Plato Kiralama Geliri</option>
                          <option value="Kafeterya & Mutfak Satışı">☕ Kafeterya & Mutfak Günlük Satış</option>
                          <option value="Ses & Işık Kiralama">🔊 Ses & Işık Ekipman Dış Kiralama</option>
                          <option value="Sponsorluk & Reklam">🏷️ Sponsorluk & Reklam Geliri</option>
                          <option value="Ekipman & Hurda Satışı">📦 Eski Ekipman / Hurda Satış Geliri</option>
                          <option value="Muhtelif Gelir">💵 Diğer Muhtelif Kasa Geliri</option>
                        </>
                      ) : (
                        <>
                          <option value="Faturalar & Enerji">💡 Faturalar & Enerji (Elektrik, Su, Doğalgaz, Fiber İnternet)</option>
                          <option value="Yemek & Mutfak & İkram">🍽️ Yemek & Mutfak & İkram Alımları</option>
                          <option value="Keyfi & Temsil Ağırlama">☕ Keyfi & Temsil Ağırlama (Kahve, Yemek vb.)</option>
                          <option value="Personel & Yevmiye">👥 Personel Maaş, Yevmiye & SGK</option>
                          <option value="Dekorasyon & Çiçek">🌸 Dekorasyon, Çiçek & Sahne Süsleme</option>
                          <option value="Ekipman & Bakım">🔊 Ekipman, Ses, Işık & Bakım Onarım</option>
                          <option value="Ofis & Kırtasiye & Sarf">📑 Ofis, Kırtasiye & Sarf Malzeme</option>
                          <option value="Vergi & Muhasebe">⚖️ Vergi, Harç & Muhasebe Ödemeleri</option>
                          <option value="Genel Harcama">📦 Diğer Genel İşletme Giderleri</option>
                        </>
                      )}
                    </select>
                  </div>

                  <div className="grid grid-cols-2 gap-2.5">
                    <div>
                      <label className="font-bold block mb-1">Tutar (TL):</label>
                      <input
                        type="number"
                        value={newAmount}
                        onChange={e => setNewAmount(e.target.value)}
                        placeholder="0"
                        required
                        className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                      />
                    </div>
                    <div>
                      <label className="font-bold block mb-1">İşlem Tarihi:</label>
                      <input
                        type="date"
                        value={newDate}
                        onChange={e => setNewDate(e.target.value)}
                        required
                        className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                      />
                    </div>
                  </div>

                  <div className="pt-2 flex justify-end space-x-2 border-t border-slate-200 dark:border-brand-border">
                    <button
                      type="button"
                      onClick={() => setIsModalOpen(false)}
                      className="px-4 py-2 bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 rounded-xl font-bold cursor-pointer"
                    >
                      İptal
                    </button>
                    <button
                      type="submit"
                      className={`font-bold px-5 py-2 rounded-xl text-white shadow cursor-pointer ${transType === 'gelir' ? 'bg-emerald-600 hover:bg-emerald-500' : 'bg-red-600 hover:bg-red-500'}`}
                    >
                      {transType === 'gelir' ? '+ Geliri Kaydet' : '- Gideri Kaydet'}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          )}
        </div>
      );
    }"""

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    finance_pattern = re.compile(r'// --- FINANCE COMPONENT WITH RESERVATION PROFITABILITY & CUSTOM EXPENSE AUDIT ---[\s\S]*?function FinanceComponent[\s\S]*?^    }', re.MULTILINE)
    if finance_pattern.search(content):
        content = finance_pattern.sub(new_finance_component_code, content)
        print(f"Replaced FinanceComponent in {h_file}")
    else:
        print(f"FinanceComponent pattern not found in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Finance component successfully upgraded across all files!")
