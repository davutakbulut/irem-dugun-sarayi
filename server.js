/**
 * İREM DÜĞÜN SARAYI & ORGANİZASYON PLATFORMU
 * Express.js + MySQL REST API Sunucusu (server.js)
 */

const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// MySQL Bağlantı Havuzu (Pool Configuration)
const pool = mysql.createPool({
  host: process.env.DB_HOST || 'localhost',
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || '',
  database: process.env.DB_NAME || 'irem_dugun_db',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

// API Durum Kontrolü
app.get('/api/health', async (req, res) => {
  try {
    const [rows] = await pool.query('SELECT 1 + 1 AS result');
    res.json({ status: 'OK', database: 'Connected', time: new Date() });
  } catch (err) {
    res.status(500).json({ status: 'ERROR', message: 'MySQL bağlantı hatası', error: err.message });
  }
});

// 1. DÜĞÜN SALONLARI ENDPOINTS
app.get('/api/venues', async (req, res) => {
  try {
    const [venues] = await pool.query('SELECT * FROM venues ORDER BY created_at DESC');
    res.json(venues.map(v => ({
      ...v,
      features: typeof v.features_json === 'string' ? JSON.parse(v.features_json) : (v.features_json || []),
      images: typeof v.images_json === 'string' ? JSON.parse(v.images_json) : (v.images_json || [])
    })));
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/venues', async (req, res) => {
  try {
    const { name, category, capacity, price, deposit, location, description, features, images } = req.body;
    const id = 'v-' + Date.now();
    await pool.query(
      'INSERT INTO venues (id, name, category, capacity, price, deposit, location, description, features_json, images_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
      [id, name, category, capacity, price, deposit, location, description, JSON.stringify(features || []), JSON.stringify(images || [])]
    );
    res.status(201).json({ id, message: 'Düğün salonu başarıyla kaydedildi!' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 2. EK HİZMETLER ENDPOINTS
app.get('/api/services', async (req, res) => {
  try {
    const [services] = await pool.query('SELECT * FROM services ORDER BY created_at DESC');
    res.json(services);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 3. REZERVASYONLAR VE ÇAKIŞMA KONTROLÜ
app.get('/api/reservations', async (req, res) => {
  try {
    const [reservations] = await pool.query('SELECT * FROM reservations ORDER BY event_date DESC');
    res.json(reservations);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/reservations', async (req, res) => {
  try {
    const { venueId, customerId, customerName, customerEmail, customerPhone, eventDate, timeSlot, guestCount, venuePrice, subtotal, campaignCode, discountAmount, vatAmount, totalAmount, depositPaid, remainingBalance, paymentStatus, isInvoiceNeeded, invoiceType } = req.body;

    // Çakışma Kontrolü (Collision Check Algorithm)
    const [existing] = await pool.query(
      'SELECT id FROM reservations WHERE venue_id = ? AND event_date = ? AND time_slot = ?',
      [venueId, eventDate, timeSlot]
    );

    if (existing.length > 0) {
      return res.status(409).json({ error: 'ÇAKIŞMA TESPİT EDİLDİ: Bu salon belirtilen tarih ve zaman diliminde doludur!' });
    }

    const id = `RES-${new Date().getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`;
    await pool.query(
      'INSERT INTO reservations (id, venue_id, customer_id, customer_name, customer_email, customer_phone, event_date, time_slot, guest_count, venue_price, subtotal, campaign_code, discount_amount, vat_amount, total_amount, deposit_paid, remaining_balance, payment_status, is_invoiced, invoice_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
      [id, venueId, customerId, customerName, customerEmail, customerPhone, eventDate, timeSlot, guestCount, venuePrice, subtotal, campaignCode, discountAmount, vatAmount, totalAmount, depositPaid, remainingBalance, paymentStatus, isInvoiceNeeded, invoiceType]
    );

    res.status(201).json({ id, message: 'Rezervasyon MySQL veritabanına başarıyla kaydedildi!' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Statik Dosya Servis Etme
app.use(express.static(path.join(__dirname, './')));

app.listen(PORT, () => {
  console.log(`🏰 İrem Düğün Sarayı MySQL API Sunucusu http://localhost:${PORT} portunda çalışıyor.`);
});
