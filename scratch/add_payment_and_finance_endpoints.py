with open('server.js', 'r', encoding='utf-8') as f:
    code = f.read()

target_anchor = "app.delete('/api/reservations/:id',"

new_payment_endpoints = """// -------------------------------------------------------------
// 5.5 REZERVASYON PARÇALI TAHSİLAT & ÖDEME HAREKETLERİ ENDPOINTS
// -------------------------------------------------------------
app.post('/api/reservations/:id/payments', async (req, res) => {
  try {
    const { id } = req.params;
    const { amount, date, method, type, note, receiptNo, recordedBy } = req.body;
    const activePool = await getPool();
    if (!activePool) return res.status(500).json({ error: 'Database connection not available' });

    const [rows] = await activePool.query('SELECT * FROM reservations WHERE id = ?', [id]);
    if (!rows || rows.length === 0) return res.status(404).json({ error: 'Rezervasyon bulunamadı' });

    const raw = rows[0];
    let detailsObj = {};
    if (raw.details_json) {
      try { detailsObj = typeof raw.details_json === 'string' ? JSON.parse(raw.details_json) : raw.details_json; } catch(e){}
    }

    const currentPayments = Array.isArray(detailsObj.payments) ? detailsObj.payments : [];
    const newPayment = {
      id: `pay-${Date.now()}-${Math.random().toString(36).substr(2, 4)}`,
      amount: Number(amount || 0),
      date: date || new Date().toISOString().split('T')[0],
      method: method || 'Banka Havalesi & EFT',
      type: type || 'Kısmi Ara Ödeme',
      note: note || '',
      receiptNo: receiptNo || '',
      recordedBy: recordedBy || 'Sistem Yöneticisi',
      createdAt: new Date().toISOString()
    };

    const updatedPayments = [newPayment, ...currentPayments];
    const totalPaid = updatedPayments.reduce((sum, p) => sum + Number(p.amount || 0), 0);
    const totalAmount = Number(raw.total_amount || detailsObj.totalAmount || 0);
    const remainingBalance = Math.max(0, totalAmount - totalPaid);

    let paymentStatus = 'Ödeme Alınmadı';
    if (totalPaid >= totalAmount && totalAmount > 0) {
      paymentStatus = 'Tamamı Ödendi';
    } else if (totalPaid > 0) {
      paymentStatus = totalPaid === Number(amount) && (type === 'Kapora' || type === 'İlk Kapora') ? 'Kapora Alındı' : 'Kısmi Ödeme Alındı';
    }

    detailsObj.payments = updatedPayments;
    detailsObj.depositPaid = totalPaid;
    detailsObj.remainingBalance = remainingBalance;
    detailsObj.paymentStatus = paymentStatus;

    await activePool.query(
      `UPDATE reservations 
       SET deposit_paid = ?, remaining_balance = ?, payment_status = ?, details_json = ? 
       WHERE id = ?`,
      [totalPaid, remainingBalance, paymentStatus, JSON.stringify(detailsObj), id]
    );

    console.log(`💳 Rezervasyon [${id}] İçin Tahsilat Eklendi: ${newPayment.amount} TL (${newPayment.type})`);

    // Memory Store update
    const memIdx = memoryStore.reservations.findIndex(r => r.id === id);
    if (memIdx >= 0) {
      memoryStore.reservations[memIdx] = {
        ...memoryStore.reservations[memIdx],
        payments: updatedPayments,
        depositPaid: totalPaid,
        remainingBalance: remainingBalance,
        paymentStatus: paymentStatus
      };
    }

    return res.status(201).json({
      success: true,
      payment: newPayment,
      payments: updatedPayments,
      depositPaid: totalPaid,
      remainingBalance: remainingBalance,
      paymentStatus: paymentStatus
    });
  } catch(e) {
    console.error('MySQL POST /api/reservations/:id/payments error:', e.message);
    return res.status(500).json({ error: 'Tahsilat kaydedilemedi', message: e.message });
  }
});

app.delete('/api/reservations/:id/payments/:paymentId', async (req, res) => {
  try {
    const { id, paymentId } = req.params;
    const activePool = await getPool();
    if (!activePool) return res.status(500).json({ error: 'Database connection not available' });

    const [rows] = await activePool.query('SELECT * FROM reservations WHERE id = ?', [id]);
    if (!rows || rows.length === 0) return res.status(404).json({ error: 'Rezervasyon bulunamadı' });

    const raw = rows[0];
    let detailsObj = {};
    if (raw.details_json) {
      try { detailsObj = typeof raw.details_json === 'string' ? JSON.parse(raw.details_json) : raw.details_json; } catch(e){}
    }

    const currentPayments = Array.isArray(detailsObj.payments) ? detailsObj.payments : [];
    const updatedPayments = currentPayments.filter(p => p.id !== paymentId);
    const totalPaid = updatedPayments.reduce((sum, p) => sum + Number(p.amount || 0), 0);
    const totalAmount = Number(raw.total_amount || detailsObj.totalAmount || 0);
    const remainingBalance = Math.max(0, totalAmount - totalPaid);

    let paymentStatus = 'Ödeme Alınmadı';
    if (totalPaid >= totalAmount && totalAmount > 0) {
      paymentStatus = 'Tamamı Ödendi';
    } else if (totalPaid > 0) {
      paymentStatus = 'Kısmi Ödeme Alındı';
    }

    detailsObj.payments = updatedPayments;
    detailsObj.depositPaid = totalPaid;
    detailsObj.remainingBalance = remainingBalance;
    detailsObj.paymentStatus = paymentStatus;

    await activePool.query(
      `UPDATE reservations 
       SET deposit_paid = ?, remaining_balance = ?, payment_status = ?, details_json = ? 
       WHERE id = ?`,
      [totalPaid, remainingBalance, paymentStatus, JSON.stringify(detailsObj), id]
    );

    console.log(`🗑️ Rezervasyon [${id}] İçin Tahsilat Silindi: ${paymentId}`);

    // Memory Store update
    const memIdx = memoryStore.reservations.findIndex(r => r.id === id);
    if (memIdx >= 0) {
      memoryStore.reservations[memIdx] = {
        ...memoryStore.reservations[memIdx],
        payments: updatedPayments,
        depositPaid: totalPaid,
        remainingBalance: remainingBalance,
        paymentStatus: paymentStatus
      };
    }

    return res.json({
      success: true,
      deletedPaymentId: paymentId,
      payments: updatedPayments,
      depositPaid: totalPaid,
      remainingBalance: remainingBalance,
      paymentStatus: paymentStatus
    });
  } catch(e) {
    console.error('MySQL DELETE payment error:', e.message);
    return res.status(500).json({ error: 'Tahsilat silinemedi', message: e.message });
  }
});

"""

if target_anchor in code:
    code = code.replace(target_anchor, new_payment_endpoints + target_anchor)
    with open('server.js', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Added reservation payment endpoints to server.js!")
else:
    print("target_anchor not found in server.js")
