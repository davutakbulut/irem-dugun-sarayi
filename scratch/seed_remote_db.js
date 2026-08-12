const mysql = require('mysql2/promise');

(async () => {
  try {
    const conn = await mysql.createConnection({
      host: '213.159.6.158',
      port: 3306,
      user: 'kullaniciadi_irem_dugun_db',
      password: 'Akblt_157',
      database: 'irem_dugun_db'
    });

    console.log('✅ Uzak MariaDB Veritabanına Bağlanıldı (213.159.6.158)');

    // 1. Müşterileri Ekle
    const cust1 = ['cust-9101', 'Ahmet Yılmaz & Selin Kaya', 'ahmet.selin@gmail.com', '0 (532) 412 88 90', 'Göl Mahallesi Sapanca / Sakarya', 'individual', '10293847561', '', 'Sapanca VD', 0, '', ''];
    const cust2 = ['cust-9102', 'Mehmet Demir & Büşra Yıldız', 'mehmet.yildiz@hotmail.com', '0 (544) 987 65 43', 'Serdivan / Sakarya', 'individual', '56473829102', '', 'Adapazarı VD', 0, '', ''];
    const cust3 = ['cust-9103', 'Caner Öztürk & Zeynep Arslan', 'zeynep.caner@outlook.com', '0 (535) 777 44 11', 'Karasu / Sakarya', 'individual', '98765432109', '', 'Karasu VD', 0, '', ''];

    const custQuery = `
      INSERT INTO customers (id, name, email, phone, address, tax_type, tc_no, vkn_no, tax_office, follow_up, follow_up_note, avatar)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      ON DUPLICATE KEY UPDATE name=VALUES(name), phone=VALUES(phone);
    `;

    await conn.query(custQuery, cust1);
    await conn.query(custQuery, cust2);
    await conn.query(custQuery, cust3);
    console.log('✅ 3 Adet Müşteri Kaydı Canlı MariaDB Veritabanına Eklendi!');

    // 2. Rezervasyonları Ekle
    const res1 = [
      'RES-2026-9101', 'v1', 'cust-9101', 'Ahmet Yılmaz & Selin Kaya', 'ahmet.selin@gmail.com', '0 (532) 412 88 90',
      '2026-09-15', '18:30 - 23:30', 500, 120000.00, 120000.00, 'BAHAR2026', 10000.00, 0.00, 110000.00,
      40000.00, 70000.00, 'Kapora Alındı', 0, 'individual', 'VIP Sahne Düzeni, Beyaz Gül & Kristal Avize Konsepti, Canlı Orkestra'
    ];

    const res2 = [
      'RES-2026-9102', 'v1', 'cust-9102', 'Mehmet Demir & Büşra Yıldız', 'mehmet.yildiz@hotmail.com', '0 (544) 987 65 43',
      '2026-10-02', '19:00 - 23:00', 650, 145000.00, 145000.00, '', 0.00, 0.00, 145000.00,
      145000.00, 0.00, 'Ödendi', 1, 'individual', 'Havai Fişek Gösterisi, Özel Işık Şov ve Bebek Bakım Odası Tahsisi'
    ];

    const res3 = [
      'RES-2026-9103', 'v1', 'cust-9103', 'Caner Öztürk & Zeynep Arslan', 'zeynep.caner@outlook.com', '0 (535) 777 44 11',
      '2026-11-20', '18:00 - 22:30', 350, 95000.00, 95000.00, '', 5000.00, 0.00, 90000.00,
      30000.00, 60000.00, 'Kapora Alındı', 0, 'individual', 'Kına Tahtı Kırmızı Konsept, Hint Kınacısı ve Özel Nedime Şov'
    ];

    const resQuery = `
      INSERT INTO reservations (
        id, venue_id, customer_id, customer_name, customer_email, customer_phone,
        event_date, time_slot, guest_count, venue_price, subtotal, campaign_code,
        discount_amount, vat_amount, total_amount, deposit_paid, remaining_balance,
        payment_status, is_invoiced, invoice_type, notes
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      ON DUPLICATE KEY UPDATE customer_name=VALUES(customer_name), total_amount=VALUES(total_amount);
    `;

    await conn.query(resQuery, res1);
    await conn.query(resQuery, res2);
    await conn.query(resQuery, res3);

    console.log('🎉 3 ADET REZERVASYON DOĞRUDAN CANLI UZAK VERİTABANINA YAZILDI!');

    const [rows] = await conn.query('SELECT id, customer_name, event_date, total_amount, payment_status FROM reservations;');
    console.log('📊 VERİTABANINDAKİ GÜNCEL KANIT KAYITLARI:');
    console.table(rows);

    await conn.end();
  } catch (err) {
    console.error('❌ Hata:', err.message);
  }
})();
