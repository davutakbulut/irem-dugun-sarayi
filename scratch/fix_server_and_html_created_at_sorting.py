import os, re

# ========================================================
# 1. UPGRADE server.js GET /api/reservations to include created_at
# ========================================================
with open('server.js', 'r', encoding='utf-8') as f:
    server_code = f.read()

target_in_server = """          status: r.status === 'DRAFT' ? 'CONFIRMED' : (r.status || 'CONFIRMED'),
          isDraft: false"""

replacement_in_server = """          created_at: r.created_at || detailsObj.created_at || detailsObj.createdAt || '',
          createdAt: r.created_at || detailsObj.createdAt || detailsObj.created_at || '',
          status: r.status === 'DRAFT' ? 'CONFIRMED' : (r.status || 'CONFIRMED'),
          isDraft: false"""

if target_in_server in server_code and "created_at: r.created_at" not in server_code:
    server_code = server_code.replace(target_in_server, replacement_in_server)
    with open('server.js', 'w', encoding='utf-8') as f:
        f.write(server_code)
    print("Updated server.js GET /api/reservations to explicitly output created_at and createdAt!")
else:
    print("server.js already updated or target not found")


# ========================================================
# 2. UPGRADE HTML FILES
# ========================================================
html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

old_rf_return = """          return {
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
          };"""

new_rf_return = """          return {
            reservation: r,
            created_at: r.created_at || r.createdAt || '',
            createdAt: r.createdAt || r.created_at || '',
            venueName: vObj?.name || r.venueName || r.venueId,
            grossIncome,
            venueCost,
            servicesCost,
            customExpensesList,
            customExpensesTotal,
            totalCost,
            netProfit,
            profitMargin: Number(profitMargin)
          };"""

old_prof_sort_block = """      // Filtered Profitability Rows (Strictly Sorted by System created_at / Creation Timestamp)
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
            const tsA = extractSystemTimestamp(a.reservation);
            const tsB = extractSystemTimestamp(b.reservation);
            if (tsB !== tsA) return tsB - tsA; // Sisteme en son eklenen rezervasyon en üstte
            return String(b.reservation?.id || '').localeCompare(String(a.reservation?.id || ''));
          });
      }, [reservationFinancials, searchQuery]);"""

new_prof_sort_block = """      // Filtered Profitability Rows (Strictly Sorted by System created_at / Creation Timestamp: Newest First)
      const filteredProfitabilityRows = useMemo(() => {
        const getTs = (obj) => {
          const r = obj.reservation || obj;
          if (!r) return 0;
          if (r.created_at) {
            const t = new Date(r.created_at).getTime();
            if (!isNaN(t) && t > 0) return t;
          }
          if (r.createdAt) {
            const t = new Date(r.createdAt).getTime();
            if (!isNaN(t) && t > 0) return t;
          }
          if (typeof r.id === 'string') {
            const m = r.id.match(/\\d{10,13}/);
            if (m) {
              const num = Number(m[0]);
              if (num > 1000000000) return num > 100000000000 ? num : num * 1000;
            }
          }
          return 0;
        };

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
            const tsA = getTs(a);
            const tsB = getTs(b);
            if (tsB !== tsA) return tsB - tsA; // En son sisteme kaydedilen rezervasyon sözleşmesi en üstte
            return String(b.reservation?.id || '').localeCompare(String(a.reservation?.id || ''));
          });
      }, [reservationFinancials, searchQuery]);"""

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_rf_return in content:
        content = content.replace(old_rf_return, new_rf_return)
        print(f"Updated reservationFinancials return in {h_file}")

    if old_prof_sort_block in content:
        content = content.replace(old_prof_sort_block, new_prof_sort_block)
        print(f"Updated filteredProfitabilityRows sorting in {h_file}")
    else:
        print(f"old_prof_sort_block not found in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

print("All files updated successfully with robust created_at contract sorting!")
