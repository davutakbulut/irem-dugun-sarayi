import os, re

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

old_transactions_block = """      // Unified Ledger
      const allTransactions = useMemo(() => {
        return [...incomeTransactions, ...expenseTransactions].sort((a, b) => new Date(b.date) - new Date(a.date));
      }, [incomeTransactions, expenseTransactions]);"""

new_transactions_block = """      // Unified Ledger (Sorted Newest to Oldest by Transaction Date)
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

old_profitability_block = """      // Filtered Profitability Rows
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

new_profitability_block = """      // Filtered Profitability Rows (Sorted Newest to Oldest by Event Date)
      const filteredProfitabilityRows = useMemo(() => {
        return reservationFinancials
          .filter(rf => {
            if (!searchQuery.trim()) return true;
            const q = searchQuery.toLowerCase();
            const r = rf.reservation;
            return (r.customerName || '').toLowerCase().includes(q) ||
                   (r.id || '').toLowerCase().includes(q) ||
                   (rf.venueName || '').toLowerCase().includes(q);
          })
          .sort((a, b) => {
            const dateA = new Date(a.reservation?.date || a.reservation?.eventDate || 0).getTime();
            const dateB = new Date(b.reservation?.date || b.reservation?.eventDate || 0).getTime();
            return dateB - dateA; // En yeni etkinlik tarihi en üstte
          });
      }, [reservationFinancials, searchQuery]);"""

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_transactions_block in content:
        content = content.replace(old_transactions_block, new_transactions_block)
        print(f"Updated allTransactions sorting in {h_file}")
    else:
        print(f"old_transactions_block not found in {h_file}")

    if old_profitability_block in content:
        content = content.replace(old_profitability_block, new_profitability_block)
        print(f"Updated filteredProfitabilityRows sorting in {h_file}")
    else:
        print(f"old_profitability_block not found in {h_file}")

    # Also update table header to "İşlem Tarihi"
    content = content.replace('<th className="p-3.5">Tarih</th>', '<th className="p-3.5"><ThemeIcon icon="calendar" className="w-3.5 h-3.5 inline mr-1 text-amber-500" />İşlem Tarihi</th>')

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Date sorting successfully updated across all files!")
