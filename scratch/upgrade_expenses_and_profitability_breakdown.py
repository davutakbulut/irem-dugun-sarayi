import os, re

# ==========================================
# 1. UPDATE server.js
# ==========================================
with open('server.js', 'r', encoding='utf-8') as f:
    server_code = f.read()

# Update /api/expenses in server.js
old_exp_block = """// -------------------------------------------------------------
// 6. GİDERLER ENDPOINTS (/api/expenses)
// -------------------------------------------------------------
app.get('/api/expenses', async (req, res) => {
  try {
    const activePool = await getPool();
    if (activePool) {
      const [rows] = await activePool.query('SELECT * FROM expenses ORDER BY date DESC, created_at DESC');
      const formatted = (rows || []).map(r => ({
        ...r,
        amount: Number(r.amount || 0),
        date: r.date ? (typeof r.date === 'string' ? r.date.split('T')[0] : (r.date instanceof Date ? `${r.date.getFullYear()}-${String(r.date.getMonth()+1).padStart(2,'0')}-${String(r.date.getDate()).padStart(2,'0')}` : String(r.date).split('T')[0])) : ''
      }));
      return res.json(formatted);
    }
  } catch(e) {
    console.error('MySQL GET /api/expenses error:', e.message);
  }
  res.json(memoryStore.expenses || []);
});

app.post('/api/expenses', async (req, res) => {
  try {
    const item = { id: req.body.id || ('exp-' + Date.now()), ...req.body };
    const cleanDate = item.date || new Date().toISOString().split('T')[0];
    const activePool = await getPool();
    if (activePool) {
      await activePool.query(
        `INSERT INTO expenses (id, title, category, amount, date, description, type)
         VALUES (?, ?, ?, ?, ?, ?, ?)
         ON DUPLICATE KEY UPDATE title=VALUES(title), category=VALUES(category), amount=VALUES(amount), date=VALUES(date), description=VALUES(description), type=VALUES(type)`,
        [item.id, item.title, item.category || 'Genel', Number(item.amount || 0), cleanDate, item.description || '', item.type || 'expense']
      );
      console.log(`💾 Gider [${item.id}] MariaDB Veritabanına Yazıldı: ${item.title} (${item.amount} TL)`);
    }
    
    // Update memoryStore
    memoryStore.expenses = [item, ...(memoryStore.expenses || []).filter(e => e.id !== item.id)];
    res.status(201).json({ success: true, item });
  } catch(e) {
    console.error('MySQL POST /api/expenses error:', e.message);
    res.status(500).json({ error: 'Gider kaydedilemedi', message: e.message });
  }
});"""

new_exp_block = """// -------------------------------------------------------------
// 6. GİDERLER & HARİCİ GELİRLER ENDPOINTS (/api/expenses)
// -------------------------------------------------------------
app.get('/api/expenses', async (req, res) => {
  try {
    const activePool = await getPool();
    if (activePool) {
      const [rows] = await activePool.query('SELECT * FROM expenses ORDER BY date DESC, created_at DESC');
      const formatted = (rows || []).map(r => ({
        ...r,
        amount: Number(r.amount || 0),
        type: (r.type === 'gelir' || r.type === 'income') ? 'gelir' : 'gider',
        date: r.date ? (typeof r.date === 'string' ? r.date.split('T')[0] : (r.date instanceof Date ? `${r.date.getFullYear()}-${String(r.date.getMonth()+1).padStart(2,'0')}-${String(r.date.getDate()).padStart(2,'0')}` : String(r.date).split('T')[0])) : ''
      }));
      return res.json(formatted);
    }
  } catch(e) {
    console.error('MySQL GET /api/expenses error:', e.message);
  }
  res.json(memoryStore.expenses || []);
});

app.post('/api/expenses', async (req, res) => {
  try {
    const raw = req.body || {};
    const item = {
      id: raw.id || (`exp-${Date.now()}`),
      title: (raw.title || 'Kasa Hareketi').trim(),
      category: raw.category || 'Genel Harcama',
      amount: Number(raw.amount || 0),
      date: raw.date || new Date().toISOString().split('T')[0],
      description: raw.description || '',
      type: (raw.type === 'gelir' || raw.type === 'income') ? 'gelir' : 'gider',
      status: raw.status || 'Tamamlandı'
    };

    const activePool = await getPool();
    if (activePool) {
      await activePool.query(
        `INSERT INTO expenses (id, title, category, amount, date, description, type)
         VALUES (?, ?, ?, ?, ?, ?, ?)
         ON DUPLICATE KEY UPDATE 
           title=VALUES(title), category=VALUES(category), amount=VALUES(amount), 
           date=VALUES(date), description=VALUES(description), type=VALUES(type)`,
        [item.id, item.title, item.category, item.amount, item.date, item.description, item.type]
      );
      console.log(`💾 Kasa Hareketi [${item.id}] MariaDB Veritabanına Yazıldı: ${item.title} (${item.type === 'gelir' ? '+' : '-'}${item.amount} TL)`);
    }
    
    // Update memoryStore
    memoryStore.expenses = [item, ...(memoryStore.expenses || []).filter(e => e.id !== item.id)];
    res.status(201).json({ success: true, item });
  } catch(e) {
    console.error('MySQL POST /api/expenses error:', e.message);
    res.status(500).json({ error: 'Kasa hareketi kaydedilemedi', message: e.message });
  }
});"""

if old_exp_block in server_code:
    server_code = server_code.replace(old_exp_block, new_exp_block)
    with open('server.js', 'w', encoding='utf-8') as f:
        f.write(server_code)
    print("Updated /api/expenses in server.js!")
else:
    print("old_exp_block not matched in server.js")


# ==========================================
# 2. UPDATE HTML FILES (FinanceComponent)
# ==========================================
html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the handleAddGeneralTransaction function and make it directly fetch & update state
    old_add_trans = """      // Handle Add General Cash Transaction (Income or Expense)
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
      };"""

    new_add_trans = """      // Handle Add General Cash Transaction (Income or Expense)
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
          description: `Kasa Hareketi (${transType === 'gelir' ? 'Harici Gelir' : 'Harici Gider'})`,
          status: newStatus
        };

        try {
          const fetchFn = window.fetchWithRetry || fetch;
          const resp = await fetchFn('/api/expenses', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newTrans)
          });
          const data = await resp.json();
          if (data.success && data.item) {
            setExpenses(prev => [data.item, ...prev.filter(x => x.id !== data.item.id)]);
          } else {
            setExpenses(prev => [newTrans, ...prev.filter(x => x.id !== newTrans.id)]);
          }
        } catch(err) {
          console.error('Add expense error:', err);
          setExpenses(prev => [newTrans, ...prev.filter(x => x.id !== newTrans.id)]);
        }

        setNewTitle('');
        setNewAmount('');
        setIsModalOpen(false);
      };"""

    if old_add_trans in content:
        content = content.replace(old_add_trans, new_add_trans)
        print(f"Updated handleAddGeneralTransaction in {h_file}")

    # Now let's enrich the expanded row in Profitability Table to display full details (Venue cost, Itemized Selected Services with name & cost, and Custom Expenses with delete action)
    old_expanded_row = """                                {isExpanded && (
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
                                )}"""

    new_expanded_row = """                                {isExpanded && (
                                  <tr className="bg-slate-50/80 dark:bg-brand-dark/70 border-b border-amber-500/20">
                                    <td colSpan="8" className="p-4 sm:p-6 space-y-4">
                                      <div className="flex justify-between items-center pb-2 border-b border-slate-200 dark:border-brand-border">
                                        <div className="flex items-center space-x-2">
                                          <span className="w-2.5 h-2.5 rounded-full bg-amber-500 animate-pulse"></span>
                                          <span className="font-heading font-extrabold text-sm text-slate-900 dark:text-white">
                                            {r.customerName} — Sözleşme & Maliyet Detay Dökümü ({r.id})
                                          </span>
                                        </div>
                                        <button
                                          type="button"
                                          onClick={() => setCustomExpenseModalRes(r)}
                                          className="px-3 py-1.5 gold-button font-bold text-xs rounded-xl shadow cursor-pointer flex items-center space-x-1"
                                        >
                                          <span>+ Bu Düğüne Ek Gider / Harcama Gir</span>
                                        </button>
                                      </div>

                                      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 text-xs">
                                        {/* 1. MEKAN & BALO SALONU MALİYETİ */}
                                        <div className="bg-white dark:bg-brand-card p-4 rounded-2xl border border-slate-200 dark:border-brand-border space-y-2.5 shadow-xs">
                                          <div className="flex justify-between items-center">
                                            <span className="font-bold text-slate-700 dark:text-gray-200 flex items-center space-x-1">
                                              <span>🏰</span><span>Mekan & Salon Maliyeti</span>
                                            </span>
                                            <span className="font-mono font-extrabold text-red-500 dark:text-red-400">{formatCurrency(rf.venueCost)}</span>
                                          </div>
                                          <div className="p-2.5 bg-slate-50 dark:bg-brand-dark rounded-xl text-[11px] space-y-1 text-slate-600 dark:text-gray-300 border border-slate-200/60 dark:border-brand-border/40">
                                            <div className="flex justify-between font-medium">
                                              <span>Salon Adı:</span>
                                              <span className="font-bold text-slate-800 dark:text-gray-100">{rf.venueName}</span>
                                            </div>
                                            <div className="flex justify-between font-medium">
                                              <span>Sözleşme Salon Fiyatı:</span>
                                              <span className="font-bold font-mono">{formatCurrency(r.venuePrice || r.customVenuePrice || 0)}</span>
                                            </div>
                                            <div className="flex justify-between font-medium">
                                              <span>Temel İşletme Maliyeti:</span>
                                              <span className="font-bold font-mono text-red-500">{formatCurrency(rf.venueCost)}</span>
                                            </div>
                                          </div>
                                        </div>

                                        {/* 2. SEÇİLİ EK HİZMETLER VE BİRİM MALİYETLERİ */}
                                        <div className="bg-white dark:bg-brand-card p-4 rounded-2xl border border-slate-200 dark:border-brand-border space-y-2.5 shadow-xs">
                                          <div className="flex justify-between items-center">
                                            <span className="font-bold text-slate-700 dark:text-gray-200 flex items-center space-x-1">
                                              <span>🍽️</span><span>Seçili Ek Hizmetler ({(r.selectedServices || []).length})</span>
                                            </span>
                                            <span className="font-mono font-extrabold text-red-500 dark:text-red-400">{formatCurrency(rf.servicesCost)}</span>
                                          </div>
                                          <div className="space-y-1.5 max-h-36 overflow-y-auto custom-scrollbar">
                                            {(r.selectedServices || []).length === 0 ? (
                                              <div className="text-center py-3 text-slate-400 text-[11px] bg-slate-50 dark:bg-brand-dark rounded-xl border border-dashed border-slate-200 dark:border-brand-border">
                                                Ekstra hizmet seçilmemiş.
                                              </div>
                                            ) : (
                                              (r.selectedServices || []).map((s, idx) => {
                                                const sObj = (services || []).find(srv => srv.id === s.serviceId);
                                                const sName = s.name || sObj?.name || `Hizmet (${s.serviceId})`;
                                                const sQty = Number(s.quantity || 1);
                                                const sCost = s.costPrice !== undefined ? Number(s.costPrice) : (sObj?.costPrice !== undefined ? Number(sObj.costPrice) : Math.round(Number(s.unitPrice || 250) * 0.6));
                                                const totalItemCost = sCost * sQty;
                                                return (
                                                  <div key={idx} className="p-2 bg-slate-50 dark:bg-brand-dark rounded-xl flex justify-between items-center text-[11px] border border-slate-200/60 dark:border-brand-border/40">
                                                    <div>
                                                      <div className="font-bold text-slate-800 dark:text-gray-200">{sName}</div>
                                                      <div className="text-[10px] text-slate-400 font-medium">{sQty} Adet / Kişi × {formatCurrency(sCost)}</div>
                                                    </div>
                                                    <span className="font-mono font-bold text-red-500 dark:text-red-400">{formatCurrency(totalItemCost)}</span>
                                                  </div>
                                                );
                                              })
                                            )}
                                          </div>
                                        </div>

                                        {/* 3. REZERVASYONA ÖZEL EK HARCAMALAR VE YEVMİYELER */}
                                        <div className="bg-white dark:bg-brand-card p-4 rounded-2xl border border-slate-200 dark:border-brand-border space-y-2.5 shadow-xs">
                                          <div className="flex justify-between items-center">
                                            <span className="font-bold text-slate-700 dark:text-gray-200 flex items-center space-x-1">
                                              <span>📑</span><span>Düğüne Özel Giderler ({rf.customExpensesList.length})</span>
                                            </span>
                                            <span className="font-mono font-extrabold text-amber-600 dark:text-gold-400">{formatCurrency(rf.customExpensesTotal)}</span>
                                          </div>
                                          <div className="space-y-1.5 max-h-36 overflow-y-auto custom-scrollbar">
                                            {rf.customExpensesList.length === 0 ? (
                                              <div className="text-center py-3 text-slate-400 text-[11px] bg-slate-50 dark:bg-brand-dark rounded-xl border border-dashed border-slate-200 dark:border-brand-border">
                                                Özel harcama girilmemiş.
                                              </div>
                                            ) : (
                                              rf.customExpensesList.map((exp, idx) => (
                                                <div key={exp.id || idx} className="p-2 bg-slate-50 dark:bg-brand-dark rounded-xl flex justify-between items-center text-[11px] border border-slate-200/60 dark:border-brand-border/40">
                                                  <div>
                                                    <div className="font-bold text-slate-800 dark:text-gray-200">{exp.title}</div>
                                                    <div className="text-[10px] text-slate-400 font-medium">{exp.category} {exp.date ? `• ${formatDate(exp.date)}` : ''}</div>
                                                  </div>
                                                  <div className="flex items-center space-x-2">
                                                    <span className="font-mono font-bold text-amber-600 dark:text-gold-400">{formatCurrency(exp.amount)}</span>
                                                    <button
                                                      type="button"
                                                      onClick={() => handleDeleteCustomExpenseFromRes(exp.id)}
                                                      className="text-red-500 hover:text-red-700 w-4 h-4 rounded bg-red-500/10 hover:bg-red-500/20 flex items-center justify-center text-[10px]"
                                                      title="Gideri Sil"
                                                    >
                                                      ✕
                                                    </button>
                                                  </div>
                                                </div>
                                              ))
                                            )}
                                          </div>
                                        </div>
                                      </div>

                                      {/* BOTTOM CONTRACT PROFIT RECAP BAR */}
                                      <div className="p-3.5 bg-gradient-to-r from-amber-500/10 via-emerald-500/10 to-transparent rounded-2xl border border-amber-500/30 flex flex-col sm:flex-row justify-between items-center gap-3 text-xs">
                                        <div className="flex items-center space-x-4">
                                          <div>
                                            <span className="text-[10px] text-slate-500 block">Sözleşme Cirosu:</span>
                                            <span className="font-mono font-extrabold text-slate-900 dark:text-white text-sm">{formatCurrency(rf.grossIncome)}</span>
                                          </div>
                                          <div className="text-slate-400 font-bold">-</div>
                                          <div>
                                            <span className="text-[10px] text-slate-500 block">Toplam Maliyet:</span>
                                            <span className="font-mono font-extrabold text-red-500 text-sm">{formatCurrency(rf.totalCost)}</span>
                                          </div>
                                          <div className="text-slate-400 font-bold">=</div>
                                          <div>
                                            <span className="text-[10px] text-slate-500 block">Net Kâr:</span>
                                            <span className={`font-mono font-extrabold text-sm ${rf.netProfit >= 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600'}`}>{formatCurrency(rf.netProfit)}</span>
                                          </div>
                                        </div>

                                        <div className="flex items-center space-x-2">
                                          <span className="text-slate-500 text-[11px] font-bold">Kâr Marjı:</span>
                                          <span className={`px-3 py-1 rounded-xl font-extrabold text-xs shadow-xs ${rf.profitMargin >= 35 ? 'bg-emerald-600 text-white' : (rf.profitMargin > 0 ? 'bg-amber-500 text-slate-950' : 'bg-red-600 text-white')}`}>
                                            %{rf.profitMargin}
                                          </span>
                                        </div>
                                      </div>
                                    </td>
                                  </tr>
                                )}"""

    if old_expanded_row in content:
        content = content.replace(old_expanded_row, new_expanded_row)
        print(f"Updated expanded profitability breakdown row in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

print("All files updated successfully with rich contract profitability breakdown!")
