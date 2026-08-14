import os, re

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. ReservationsListComponent filteredReservations
    old_res_sort = """      const filteredReservations = (reservations || []).filter(r => {
        const q = searchQuery.toLowerCase().trim();
        const matchesSearch = !q ||
          (r.customerName || '').toLowerCase().includes(q) ||
          (r.id || '').toLowerCase().includes(q) ||
          (r.customerPhone || '').includes(q);

        const matchesVenue = venueFilter === 'ALL' || r.venueId === venueFilter;
        const matchesStatus = statusFilter === 'ALL' ||
          (statusFilter === 'DRAFT'
            ? (r.status !== 'CONFIRMED' && r.isDraft !== false && (r.status === 'DRAFT' || r.isDraft || r.paymentStatus === 'Taslak' || (r.id && r.id.startsWith('RES-DRAFT-'))))
            : r.paymentStatus === statusFilter);

        let matchesDate = true;
        const rDate = r.eventDate || r.date;
        if (startDateFilter && rDate < startDateFilter) matchesDate = false;
        if (endDateFilter && rDate > endDateFilter) matchesDate = false;

        return matchesSearch && matchesVenue && matchesStatus && matchesDate;
      });"""

    new_res_sort = """      const filteredReservations = (reservations || []).filter(r => {
        const q = searchQuery.toLowerCase().trim();
        const matchesSearch = !q ||
          (r.customerName || '').toLowerCase().includes(q) ||
          (r.id || '').toLowerCase().includes(q) ||
          (r.customerPhone || '').includes(q);

        const matchesVenue = venueFilter === 'ALL' || r.venueId === venueFilter;
        const matchesStatus = statusFilter === 'ALL' ||
          (statusFilter === 'DRAFT'
            ? (r.status !== 'CONFIRMED' && r.isDraft !== false && (r.status === 'DRAFT' || r.isDraft || r.paymentStatus === 'Taslak' || (r.id && r.id.startsWith('RES-DRAFT-'))))
            : r.paymentStatus === statusFilter);

        let matchesDate = true;
        const rDate = r.eventDate || r.date;
        if (startDateFilter && rDate < startDateFilter) matchesDate = false;
        if (endDateFilter && rDate > endDateFilter) matchesDate = false;

        return matchesSearch && matchesVenue && matchesStatus && matchesDate;
      }).sort((a, b) => {
        const getTs = (item) => {
          if (!item) return 0;
          if (item.created_at) {
            const t = new Date(item.created_at).getTime();
            if (!isNaN(t) && t > 0) return t;
          }
          if (item.createdAt) {
            const t = new Date(item.createdAt).getTime();
            if (!isNaN(t) && t > 0) return t;
          }
          if (typeof item.id === 'string') {
            const m = item.id.match(/\\d{10,13}/);
            if (m) {
              const num = Number(m[0]);
              if (num > 1000000000) return num > 100000000000 ? num : num * 1000;
            }
          }
          if (item.date) {
            const t = new Date(item.date).getTime();
            if (!isNaN(t) && t > 0) return t;
          }
          return 0;
        };
        const tsA = getTs(a);
        const tsB = getTs(b);
        if (tsB !== tsA) return tsB - tsA;
        return String(b.id || '').localeCompare(String(a.id || ''));
      });"""

    if old_res_sort in content:
        content = content.replace(old_res_sort, new_res_sort)
        print(f"Updated ReservationsListComponent sort in {h_file}")

    # 2. FinanceComponent filteredProfitabilityRows
    old_prof_sort = """      // Filtered Profitability Rows (Sorted Newest to Oldest by Event Date)
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

    new_prof_sort = """      // Filtered Profitability Rows (Strictly Sorted by System created_at / Creation Timestamp)
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

    if old_prof_sort in content:
        content = content.replace(old_prof_sort, new_prof_sort)
        print(f"Updated FinanceComponent profitability sort in {h_file}")

    # 3. QuoteRequestsPageComponent filteredRequests
    old_quote_sort = """      const filteredRequests = useMemo(() => {
        return (quoteRequests || []).filter(req => {
          const matchesStatus = filterStatus === 'all' || req.status === filterStatus;
          const searchLower = searchTerm.toLowerCase();
          const matchesSearch = !searchTerm || 
            (req.customerName || '').toLowerCase().includes(searchLower) ||
            (req.customerPhone || '').toLowerCase().includes(searchLower) ||
            (req.eventType || '').toLowerCase().includes(searchLower) ||
            (req.preferredVenue || '').toLowerCase().includes(searchLower);

          return matchesStatus && matchesSearch;
        });
      }, [quoteRequests, filterStatus, searchTerm]);"""

    new_quote_sort = """      const filteredRequests = useMemo(() => {
        return (quoteRequests || []).filter(req => {
          const matchesStatus = filterStatus === 'all' || req.status === filterStatus;
          const searchLower = searchTerm.toLowerCase();
          const matchesSearch = !searchTerm || 
            (req.customerName || '').toLowerCase().includes(searchLower) ||
            (req.customerPhone || '').toLowerCase().includes(searchLower) ||
            (req.eventType || '').toLowerCase().includes(searchLower) ||
            (req.preferredVenue || '').toLowerCase().includes(searchLower);

          return matchesStatus && matchesSearch;
        }).sort((a, b) => {
          const tA = new Date(a.created_at || a.createdAt || a.date || 0).getTime();
          const tB = new Date(b.created_at || b.createdAt || b.date || 0).getTime();
          if (tB !== tA) return tB - tA; // En son gelen teklif talebi en üstte
          return String(b.id || '').localeCompare(String(a.id || ''));
        });
      }, [quoteRequests, filterStatus, searchTerm]);"""

    if old_quote_sort in content:
        content = content.replace(old_quote_sort, new_quote_sort)
        print(f"Updated QuoteRequestsPageComponent sort in {h_file}")

    # 4. CustomersComponent filteredCustomers
    old_cust_sort = """      const filteredCustomers = useMemo(() => {
        return customers.filter(c => {
          const matchesTaxType = taxTypeFilter === 'ALL' || c.taxType === taxTypeFilter;
          const matchesSearch = !searchTerm || (
            c.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            c.phone?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            c.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            c.tcNo?.includes(searchTerm) ||
            c.vknNo?.includes(searchTerm)
          );
          return matchesTaxType && matchesSearch;
        });
      }, [customers, taxTypeFilter, searchTerm]);"""

    new_cust_sort = """      const filteredCustomers = useMemo(() => {
        return (customers || []).filter(c => {
          const matchesTaxType = taxTypeFilter === 'ALL' || c.taxType === taxTypeFilter;
          const matchesSearch = !searchTerm || (
            c.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            c.phone?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            c.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            c.tcNo?.includes(searchTerm) ||
            c.vknNo?.includes(searchTerm)
          );
          return matchesTaxType && matchesSearch;
        }).sort((a, b) => {
          const tA = new Date(a.created_at || a.createdAt || 0).getTime();
          const tB = new Date(b.created_at || b.createdAt || 0).getTime();
          if (tB !== tA) return tB - tA; // En son eklenen müşteri en üstte
          return String(b.id || '').localeCompare(String(a.id || ''));
        });
      }, [customers, taxTypeFilter, searchTerm]);"""

    if old_cust_sort in content:
        content = content.replace(old_cust_sort, new_cust_sort)
        print(f"Updated CustomersComponent sort in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

print("All tables successfully updated to sort strictly by created_at!")
