import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

handlers_code = """      // Handle Add Payment to Reservation inside modal
      const handleAddPaymentToResInModal = async (e) => {
        e.preventDefault();
        if (!customExpenseModalRes || !newResExpAmount || Number(newResExpAmount) <= 0) return;
        const resId = customExpenseModalRes.id;
        try {
          const fetchFn = window.fetchWithRetry || fetch;
          const resp = await fetchFn(`/api/reservations/${resId}/payments`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              amount: Number(newResExpAmount),
              date: newResPayDate || new Date().toISOString().split('T')[0],
              method: newResPayMethod,
              type: newResPayType,
              note: newResExpTitle.trim() || `${customExpenseModalRes.customerName} - ${newResPayType}`,
              recordedBy: 'Sistem Yöneticisi'
            })
          });
          const data = await resp.json();
          if (data && data.success) {
            setCustomExpenseModalRes(prev => prev ? ({
              ...prev,
              payments: data.payments,
              depositPaid: data.depositPaid,
              remainingBalance: data.remainingBalance,
              paymentStatus: data.paymentStatus
            }) : null);

            if (typeof setReservations === 'function') {
              setReservations(prev => {
                const updated = (prev || []).map(r => {
                  if (r.id === resId) {
                    return {
                      ...r,
                      payments: data.payments,
                      depositPaid: data.depositPaid,
                      remainingBalance: data.remainingBalance,
                      paymentStatus: data.paymentStatus
                    };
                  }
                  return r;
                });
                CacheService.set('reservations', updated);
                return updated;
              });
            }
            if (typeof showToast === 'function') {
              showToast(`${formatCurrency(newResExpAmount)} tahsilat alındı! Kalan: ${formatCurrency(data.remainingBalance)}`);
            }
            setNewResExpAmount('');
            setNewResExpTitle('');
          }
        } catch(err) {
          console.error('Add payment error:', err);
        }
      };

      // Handle Delete Payment from Reservation inside modal
      const handleDeletePaymentFromRes = async (paymentId) => {
        if (!customExpenseModalRes) return;
        const resId = customExpenseModalRes.id;
        try {
          const fetchFn = window.fetchWithRetry || fetch;
          const resp = await fetchFn(`/api/reservations/${resId}/payments/${paymentId}`, { method: 'DELETE' });
          const data = await resp.json();
          if (data && data.success) {
            setCustomExpenseModalRes(prev => prev ? ({
              ...prev,
              payments: data.payments,
              depositPaid: data.depositPaid,
              remainingBalance: data.remainingBalance,
              paymentStatus: data.paymentStatus
            }) : null);

            if (typeof setReservations === 'function') {
              setReservations(prev => {
                const updated = (prev || []).map(r => {
                  if (r.id === resId) {
                    return {
                      ...r,
                      payments: data.payments,
                      depositPaid: data.depositPaid,
                      remainingBalance: data.remainingBalance,
                      paymentStatus: data.paymentStatus
                    };
                  }
                  return r;
                });
                CacheService.set('reservations', updated);
                return updated;
              });
            }
            if (typeof showToast === 'function') {
              showToast('Tahsilat kaydı silindi ve bakiye güncellendi.');
            }
          }
        } catch(err) {
          console.error('Delete payment error:', err);
        }
      };

      const handleDeleteCustomExpenseFromRes = (expId) => {"""

target_anchor = "      const handleDeleteCustomExpenseFromRes = (expId) => {"

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if "const handleAddPaymentToResInModal" not in content and target_anchor in content:
        content = content.replace(target_anchor, handlers_code)
        print(f"Successfully inserted handleAddPaymentToResInModal into {h_file}")
    else:
        print(f"Skipped {h_file}")

    # Ensure button says "+ Gelir / Gider Ekle"
    content = content.replace(
        "<span>+ Gelir / Gider</span>",
        "<span>+ Gelir / Gider Ekle</span>"
    )

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fix completed across all files!")
