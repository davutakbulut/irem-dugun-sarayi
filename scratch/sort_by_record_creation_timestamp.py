import os, re

# ========================================================
# 1. UPGRADE HTML FILES (FinanceComponent & DetailModal)
# ========================================================
html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add getCreationTimestamp and recordTimestamp tracking in FinanceComponent
    old_finance_memo = """      // 2. UNIFIED CASH INFLOWS (Rezervasyon Parçalı Tahsilatları + Harici Gelirler)
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

      // Unified Ledger (Sorted Newest to Oldest by Transaction Date)
      const allTransactions = useMemo(() => {
        return [...incomeTransactions, ...expenseTransactions].sort((a, b) => {
          const dateA = new Date(a.date || 0).getTime();
          const dateB = new Date(b.date || 0).getTime();
          if (dateB !== dateA) {
            return dateB - dateA; // En yeni işlem tarihi en üstte
          }
          return String(b.id || '').localeCompare(String(a.id || ''));
        });
      }, [incomeTransactions, expenseTransactions]);"""

    new_finance_memo = """      // Helper to extract system creation timestamp
      const extractSystemTimestamp = (item) => {
        if (!item) return 0;
        if (item.recordTimestamp && Number(item.recordTimestamp) > 0) return Number(item.recordTimestamp);
        if (item.created_at) {
          const t = new Date(item.created_at).getTime();
          if (!isNaN(t) && t > 0) return t;
        }
        if (item.createdAt) {
          const t = new Date(item.createdAt).getTime();
          if (!isNaN(t) && t > 0) return t;
        }
        if (typeof item.id === 'string') {
          const match = item.id.match(/\\d{10,13}/);
          if (match) {
            const num = Number(match[0]);
            if (num > 1000000000) return num > 100000000000 ? num : num * 1000;
          }
        }
        if (item.date) {
          const t = new Date(item.date).getTime();
          if (!isNaN(t) && t > 0) return t;
        }
        return 0;
      };

      // 2. UNIFIED CASH INFLOWS (Rezervasyon Parçalı Tahsilatları + Harici Gelirler)
      const incomeTransactions = useMemo(() => {
        const list = [];
        // From Reservations (itemized payments)
        (reservations || []).forEach(r => {
          if (Array.isArray(r.payments) && r.payments.length > 0) {
            r.payments.forEach(p => {
              const ts = extractSystemTimestamp(p) || extractSystemTimestamp(r);
              list.push({
                id: p.id || `pay-${r.id}-${Math.random()}`,
                resId: r.id,
                title: `${r.customerName} - ${p.type || 'Tahsilat'} (${p.method || 'Kasa'})`,
                category: 'Rezervasyon Tahsilatı',
                type: 'gelir',
                amount: Number(p.amount || 0),
                date: p.date || r.date || '2026-08-01',
                recordTimestamp: ts,
                status: 'Tahsil Edildi',
                isReservationPayment: true
              });
            });
          } else if (Number(r.depositPaid || 0) > 0) {
            const ts = extractSystemTimestamp(r);
            list.push({
              id: `inc-${r.id}-deposit`,
              resId: r.id,
              title: `${r.customerName} - Kapora / Ödeme`,
              category: 'Rezervasyon Tahsilatı',
              type: 'gelir',
              amount: Number(r.depositPaid || 0),
              date: r.date || '2026-08-01',
              recordTimestamp: ts,
              status: 'Tahsil Edildi',
              isReservationPayment: true
            });
          }
        });

        // From External Incomes in expenses table
        (expenses || []).filter(e => e.type === 'gelir' || e.type === 'income').forEach(e => {
          const ts = extractSystemTimestamp(e);
          list.push({
            id: e.id,
            title: e.title,
            category: e.category || 'Harici Gelir',
            type: 'gelir',
            amount: Number(e.amount || 0),
            date: e.date || '2026-08-01',
            recordTimestamp: ts,
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
          const ts = extractSystemTimestamp(e);
          list.push({
            id: e.id,
            title: e.title,
            category: e.category || 'Genel Gider',
            type: 'gider',
            amount: Number(e.amount || 0),
            date: e.date || '2026-08-01',
            recordTimestamp: ts,
            status: e.status || 'Ödendi',
            isExternal: true
          });
        });

        // Reservation specific custom expenses
        (reservations || []).forEach(r => {
          if (Array.isArray(r.customExpenses)) {
            r.customExpenses.forEach(exp => {
              const ts = extractSystemTimestamp(exp) || extractSystemTimestamp(r);
              list.push({
                id: exp.id || `resexp-${r.id}-${Math.random()}`,
                resId: r.id,
                title: `${r.customerName} - ${exp.title}`,
                category: exp.category || 'Etkinlik Özel Gideri',
                type: 'gider',
                amount: Number(exp.amount || 0),
                date: exp.date || r.date || '2026-08-01',
                recordTimestamp: ts,
                status: 'Ödendi',
                isReservationCustomExpense: true
              });
            });
          }
        });

        return list;
      }, [expenses, reservations]);

      // Unified Ledger (Strictly Sorted by System Action / Creation Timestamp: Newest Action at the Very Top)
      const allTransactions = useMemo(() => {
        return [...incomeTransactions, ...expenseTransactions].sort((a, b) => {
          const tsA = a.recordTimestamp || 0;
          const tsB = b.recordTimestamp || 0;
          if (tsB !== tsA) {
            return tsB - tsA; // Sisteme son eklenen/yapılan işlem daima en üstte
          }
          return String(b.id || '').localeCompare(String(a.id || ''));
        });
      }, [incomeTransactions, expenseTransactions]);"""

    if old_finance_memo in content:
        content = content.replace(old_finance_memo, new_finance_memo)
        print(f"Updated allTransactions sorting by creation timestamp in {h_file}")
    else:
        print(f"old_finance_memo not found in {h_file}")

    # Also ensure handleAddGeneralTransaction attaches explicit recordTimestamp & createdAt
    content = content.replace(
        "amount: Number(newAmount),",
        "amount: Number(newAmount),\n          createdAt: new Date().toISOString(),\n          recordTimestamp: Date.now(),"
    )

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

print("All HTML files updated with strict creation timestamp sorting!")
