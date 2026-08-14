import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

target_block = """      // Filtered Transactions
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
      }, [allTransactions, filterTab, searchQuery]);"""

replacement_block = """      // Filtered Transactions
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

      // Filtered Profitability Rows
      const filteredProfitabilityRows = useMemo(() => {
        return reservationFinancials.filter(rf => {
          if (!searchQuery.trim()) return true;
          const q = searchQuery.toLowerCase();
          const r = rf.reservation;
          return (r.customerName || '').toLowerCase().includes(q) ||
                 (r.id || '').toLowerCase().includes(q) ||
                 (rf.venueName || '').toLowerCase().includes(q);
        });
      }, [reservationFinancials, searchQuery]);"""

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if target_block in content:
        content = content.replace(target_block, replacement_block)
        with open(h_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added filteredProfitabilityRows in {h_file}")
    else:
        print(f"target_block not found in {h_file}")

print("All files updated successfully!")
