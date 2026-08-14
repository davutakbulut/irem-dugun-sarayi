import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

old_cb = """                onUpdatePayment={(id, dep, stat) => {
                  setReservations(prev => prev.map(r => r.id === id ? { ...r, depositPaid: dep, remainingBalance: Math.max(0, r.totalAmount - dep), paymentStatus: stat } : r));
                  showToast('Ödeme & Sözleşme Güncellendi!');
                  setSelectedResForDetail(null);
                }}"""

new_cb = """                onUpdatePayment={(id, dep, stat, updatedPayments) => {
                  setReservations(prev => prev.map(r => r.id === id ? {
                    ...r,
                    depositPaid: dep,
                    remainingBalance: Math.max(0, (r.totalAmount || 0) - dep),
                    paymentStatus: stat,
                    payments: updatedPayments || r.payments
                  } : r));
                  showToast('Ödeme & Tahsilat Hareketi Güncellendi!');
                }}"""

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_cb in content:
        content = content.replace(old_cb, new_cb)
        with open(h_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated onUpdatePayment in {h_file}")
    else:
        print(f"old_cb not found in {h_file}")

print("All files updated with enhanced onUpdatePayment callback!")
