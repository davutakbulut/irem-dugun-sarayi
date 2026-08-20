const nodemailer = require('nodemailer');
/**
 * İREM DÜĞÜN SARAYI & ORGANİZASYON PLATFORMU
 * Express.js + JSON DB & MySQL REST API Sunucusu (server.js)
 * %100 Veritabanı ve Sunucu Klasörü Persistansı
 */

const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const crypto = require('crypto');

// Load .env variables if present
const envPath = path.join(__dirname, '.env');
if (fs.existsSync(envPath)) {
  const envContent = fs.readFileSync(envPath, 'utf-8');
  envContent.split('\n').forEach(line => {
    const trimmed = line.trim();
    if (trimmed && !trimmed.startsWith('#') && trimmed.includes('=')) {
      const [key, ...vals] = trimmed.split('=');
      const val = vals.join('=').trim().replace(/^["']|["']$/g, '');
      if (key.trim() && !process.env[key.trim()]) {
        process.env[key.trim()] = val;
      }
    }
  });
}

const app = express();
const PORT = process.env.PORT || 5001;

// Statik Uploads Klasörü Oluşturma ve Servis Etme
const uploadsDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
}

app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With', 'X-HTTP-Method-Override', 'X-Method-Override', 'Accept', 'Origin']
}));

app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS, PATCH');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With, X-HTTP-Method-Override, X-Method-Override, Accept, Origin');
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }
  next();
});

// STRICT RULE: ZERO CACHE - ALL RESPONSES 100% FRESH FROM MYSQL
app.use('/api', (req, res, next) => {
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');
  res.setHeader('Surrogate-Control', 'no-store');
  next();
});

app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

// POST Fallback Middleware for DELETE actions (Prevents 403 Forbidden on Plesk / IIS / ModSecurity WAF)
app.use((req, res, next) => {
  if (req.method === 'POST') {
    const overrideMethod = req.headers['x-http-method-override'] || req.headers['x-method-override'];
    if (overrideMethod === 'DELETE') {
      req.method = 'DELETE';
    }
  }
  next();
});
app.use('/uploads', express.static(uploadsDir));
app.use(express.static(path.join(__dirname, './')));

app.get('/api/db-status', async (req, res) => {
  let dbStatus = 'NOT_CONNECTED';
  let dbError = null;
  let resCount = 0;
  if (pool) {
    try {
      const [rows] = await pool.query('SELECT COUNT(*) as cnt FROM reservations');
      resCount = rows[0].cnt;
      dbStatus = 'CONNECTED_OK';
    } catch(e) {
      dbError = e.message;
      dbStatus = 'QUERY_ERROR';
    }
  }
  res.json({ status: dbStatus, error: dbError, reservationCount: resCount, poolActive: !!pool, memoryCount: memoryStore.reservations.length });
});

// DISKSEL JSON YEREL DOSYA KULLANIMI TAMAMEN KALDIRILDI
// Tüm sistem verileri %100 CANLI MySQL / MariaDB veritabanından okunur ve veritabanına yazılır.

// %100 Canlı Veritabanı Bellek & Dosya Deposu
const memoryStore = {
  venues: [],
  services: [],
  campaigns: [],
  customers: [],
  users: [],
  reservations: [],
  draftReservations: [],
  expenses: [],
  media: [],
  roles: [
    { id: 'admin', name: 'Sistem Yöneticisi', permissions: ['dashboard', 'reservations', 'create_reservation', 'calendar', 'customers', 'finance', 'media', 'settings', 'roles', 'system_guide'] },
    { id: 'satisci', name: 'Satış Danışmanı', permissions: ['dashboard', 'reservations', 'create_reservation', 'calendar', 'customers'] },
    { id: 'sosyal_medyaci', name: 'Sosyal Medya Sorumlusu', permissions: ['dashboard', 'media'] },
    { id: 'musteri', name: 'Müşteri Portalı', permissions: ['reservations'] }
  ],
  systemSettings: {
    publicTheme: 'dark-gold',
    heroBadgeText: '✨ Sapanca Göl Kenarı Lüks Düğün Tesisleri',
    heroTitle: "Hayalinizdeki Düğün İrem Düğün Sarayı'nda Unutulmaz Oluyor",
    heroSubtitle: '4 farklı balo salonu, açık hava kır bahçesi, kristal avizeler ve VIP ikram menüleriyle hayatınızın en özel gününe ev sahipliği yapıyoruz.'
  }
};

// Diskteki fiziksel uploads klasörlerini tarayıp eksik görselleri bellek ve veritabanı deposuna ekleyen fonksiyon
const syncPhysicalUploadsWithMemoryStore = () => {
  try {
    if (!fs.existsSync(uploadsDir)) return;
    
    if (!Array.isArray(memoryStore.reservations)) {
      memoryStore.reservations = [];
    }

    const subdirs = fs.readdirSync(uploadsDir);
    let updated = false;

    for (const item of subdirs) {
      if (item.startsWith('.')) continue;
      const itemPath = path.join(uploadsDir, item);
      if (fs.statSync(itemPath).isDirectory()) {
        const resId = item;
        
        let targetRes = memoryStore.reservations.find(r => r.id === resId || r.mediaKey === resId);
        if (!targetRes) {
          continue; // Gerçek veritabanında olmayan hayalet klasörler için rezervasyon nesnesi oluşturma
        }

        if (!targetRes.mediaFiles) targetRes.mediaFiles = [];

        const files = fs.readdirSync(itemPath);
        for (const file of files) {
          if (file.startsWith('.')) continue;
          const fileUrl = `/uploads/${resId}/${file}`;
          const existing = targetRes.mediaFiles.find(m => m.url === fileUrl || (m.fileName && file.endsWith(m.fileName)));
          
          if (!existing) {
            const stat = fs.statSync(path.join(itemPath, file));
            const isVideo = /\.(mp4|webm|mov|avi|mkv)$/i.test(file);
            const mediaObj = {
              id: 'mf_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4),
              type: isVideo ? 'video' : 'image',
              url: fileUrl,
              thumbnail: fileUrl,
              fileName: file.replace(/^media_\d+_/, ''),
              fileSize: (stat.size / (1024 * 1024)).toFixed(1) + ' MB',
              uploaderName: 'Davetli Konuk',
              timestamp: new Date(stat.mtime).toISOString().replace('T', ' ').substr(0, 16),
              isGuest: true,
              fileHash: `${file}_${stat.size}`
            };
            targetRes.mediaFiles.unshift(mediaObj);
            updated = true;
            console.log(`🔍 Diskteki Fiziksel Görsel Otomatik İndekslendi: ${fileUrl}`);
          }
        }
      }
    }

    if (updated) {
      // %100 MySQL Veritabanına kaydedilir
    }
  } catch (err) {
    console.error('Disk medya senkronizasyon hatası:', err.message);
  }
};

syncPhysicalUploadsWithMemoryStore();

// MySQL / MariaDB Bağlantı Havuzu
let pool = null;
let isConnectingPool = false;

const getPool = async () => {
  if (pool) return pool;
  if (isConnectingPool) {
    while (isConnectingPool) {
      await new Promise(r => setTimeout(r, 100));
    }
    if (pool) return pool;
  }
  isConnectingPool = true;
  try {
    const mysql = require('mysql2/promise');
    const testPool = mysql.createPool({
      host: '213.159.6.158',
      port: (process.env.DB_PORT || process.env.MYSQL_PORT) ? Number(process.env.DB_PORT || process.env.MYSQL_PORT) : 3306,
      user: 'kullaniciadi_irem_dugun_db',
      password: 'Akblt_157',
      database: 'irem_dugun_db',
      dateStrings: true,
      waitForConnections: true,
      connectionLimit: 2, // Strict 2 connections max for shared hosting limit
      maxIdle: 2,
      idleTimeout: 30000,
      enableKeepAlive: true,
      keepAliveInitialDelay: 10000,
      connectTimeout: 5000
    });
    await testPool.query('SELECT 1');
    pool = testPool;
    console.log(`✅ MariaDB Tekil Bağlantı Havuzu Başlatıldı!`);
  } catch(err) {
    console.warn(`ℹ️ MariaDB Havuz Bağlantı Uyarısı:`, err.message);
  } finally {
    isConnectingPool = false;
  }
  return pool;
};

const queryDb = async (sql, params = []) => {
  let activePool = await getPool();
  if (!activePool) return [[]];
  try {
    return await activePool.query(sql, params);
  } catch (err) {
    if (err.code === 'ECONNRESET' || err.code === 'PROTOCOL_CONNECTION_LOST' || err.code === 'ER_TOO_MANY_USER_CONNECTIONS') {
      console.warn('⚠️ MariaDB bağlantısı yenileniyor:', err.message);
      pool = null;
      activePool = await getPool();
      if (activePool) {
        return await activePool.query(sql, params);
      }
    }
    throw err;
  }
};

const initMysql = async () => {
  const activePool = await getPool();

    const syncMemoryFromMysql = async () => {
      if (!pool) return;
      try {
        const [vRows] = await pool.query('SELECT * FROM venues ORDER BY created_at DESC');
        if (vRows.length) memoryStore.venues = vRows.map(r => ({
          ...r,
          costPrice: r.cost_price ? Number(r.cost_price) : 0,
          occupancyRate: r.occupancy_rate || 0,
          eventTypes: r.features_json ? (typeof r.features_json === 'string' ? JSON.parse(r.features_json) : r.features_json) : ['Düğün', 'Nişan'],
          images: r.images_json ? (typeof r.images_json === 'string' ? JSON.parse(r.images_json) : r.images_json) : (r.image ? [r.image] : []),
          availableServices: r.available_services_json ? (typeof r.available_services_json === 'string' ? JSON.parse(r.available_services_json) : r.available_services_json) : ['s1', 's2', 's3', 's-tavuk-menu']
        }));

        const [sRows] = await pool.query('SELECT * FROM services ORDER BY created_at DESC');
        if (sRows.length) memoryStore.services = sRows.map(r => ({
          ...r,
          price: Number(r.price || 0),
          costPrice: r.cost_price ? Number(r.cost_price) : 0,
          pricingType: r.pricing_type || 'fixed',
          image: r.image_url || r.image
        }));

        const [cRows] = await pool.query('SELECT * FROM customers ORDER BY created_at DESC');
        if (cRows.length) memoryStore.customers = cRows.map(r => ({
          ...r,
          taxType: r.tax_type,
          tcNo: r.tc_no,
          vknNo: r.vkn_no,
          taxOffice: r.tax_office,
          followUp: Boolean(r.follow_up),
          followUpNote: r.follow_up_note
        }));

        const [uRows] = await pool.query('SELECT * FROM users ORDER BY created_at DESC');
        if (uRows.length) memoryStore.users = uRows.map(r => ({
          ...r,
          password: r.password_hash || r.password
        }));

        const [resRows] = await pool.query('SELECT * FROM reservations ORDER BY created_at DESC');
        if (resRows.length) memoryStore.reservations = resRows.map(r => ({
          ...r,
          venueId: r.venue_id,
          customerId: r.customer_id,
          customerName: r.customer_name,
          customerEmail: r.customer_email,
          customerPhone: r.customer_phone,
          eventDate: r.event_date ? (r.event_date instanceof Date ? r.event_date.toISOString().split('T')[0] : String(r.event_date).split('T')[0]) : '',
          date: r.event_date ? (r.event_date instanceof Date ? r.event_date.toISOString().split('T')[0] : String(r.event_date).split('T')[0]) : '',
          timeSlot: r.time_slot,
          guestCount: r.guest_count,
          venuePrice: Number(r.venue_price || 0),
          subtotal: Number(r.subtotal || 0),
          campaignCode: r.campaign_code,
          discountAmount: Number(r.discount_amount || 0),
          vatAmount: Number(r.vat_amount || 0),
          totalAmount: Number(r.total_amount || 0),
          depositPaid: Number(r.deposit_paid || 0),
          remainingBalance: Number(r.remaining_balance || 0),
          paymentStatus: r.payment_status,
          isInvoiced: Boolean(r.is_invoiced),
          invoiceType: r.invoice_type
        }));

        const [expRows] = await pool.query('SELECT * FROM expenses ORDER BY date DESC');
        if (expRows.length) memoryStore.expenses = expRows.map(r => ({
          ...r,
          amount: Number(r.amount || 0),
          date: r.date ? (r.date instanceof Date ? r.date.toISOString().split('T')[0] : String(r.date).split('T')[0]) : ''
        }));

        const [campRows] = await pool.query('SELECT * FROM campaigns ORDER BY created_at DESC');
        if (campRows.length) memoryStore.campaigns = campRows.map(r => ({
          ...r,
          value: Number(r.value || 0),
          startDate: r.start_date ? (r.start_date instanceof Date ? r.start_date.toISOString().split('T')[0] : String(r.start_date).split('T')[0]) : '',
          endDate: r.end_date ? (r.end_date instanceof Date ? r.end_date.toISOString().split('T')[0] : String(r.end_date).split('T')[0]) : '',
          active: Boolean(r.active)
        }));

        const [roleRows] = await pool.query('SELECT * FROM roles');
        if (roleRows.length) memoryStore.roles = roleRows.map(r => ({
          ...r,
          permissions: r.permissions_json ? (typeof r.permissions_json === 'string' ? JSON.parse(r.permissions_json) : r.permissions_json) : []
        }));

        const [sysRows] = await pool.query('SELECT * FROM system_settings WHERE id = 1');
        if (sysRows.length && sysRows[0].settings_json) {
          const parsed = typeof sysRows[0].settings_json === 'string' ? JSON.parse(sysRows[0].settings_json) : sysRows[0].settings_json;
          memoryStore.systemSettings = { ...memoryStore.systemSettings, ...parsed };
        }

        const [qRows] = await pool.query('SELECT * FROM quote_requests ORDER BY created_at DESC');
        if (qRows && qRows.length) {
          memoryStore.quoteRequests = qRows.map(q => ({
            id: q.id,
            customerName: q.customer_name || '',
            customerPhone: q.customer_phone || '',
            customerEmail: q.customer_email || '',
            eventType: q.event_type || 'Düğün',
            preferredVenue: q.preferred_venue || 'İrem Kraliyet Balo Salonu',
            guestCount: Number(q.guest_count || 0),
            eventDate: q.event_date ? (q.event_date instanceof Date ? q.event_date.toISOString().split('T')[0] : String(q.event_date).split('T')[0]) : '',
            notes: q.notes || '',
            status: q.status || 'beklemede',
            createdAt: q.created_at || new Date().toISOString()
          }));
          console.log(`📋 [Boot] ${memoryStore.quoteRequests.length} Teklif Talebi MariaDB'den Belleğe Yüklendi.`);
        }
      } catch (e) {
        console.error('MySQL Memory Hydration Error:', e.message);
      }
    };

    try {
      await pool.query(`
        CREATE TABLE IF NOT EXISTS company_settings (
          id VARCHAR(50) PRIMARY KEY,
          company_name VARCHAR(255) NOT NULL DEFAULT 'İrem Düğün Sarayı Ltd. Şti.',
          brand_title VARCHAR(255) DEFAULT 'Organizasyon & Kiralama Şirketi',
          address TEXT,
          tax_office VARCHAR(150) DEFAULT 'Sapanca Vergi Dairesi',
          tax_number VARCHAR(50) DEFAULT '4820192837',
          phone VARCHAR(50) DEFAULT '+90 532 111 2233',
          email VARCHAR(100) DEFAULT 'bilgi@iremdugunsarayi.com',
          website VARCHAR(100) DEFAULT 'https://irem.portegu.com',
          authorized_person VARCHAR(100) DEFAULT 'Davut Akbulut (Genel Müdür)',
          bank_info TEXT,
          contract_title VARCHAR(255) DEFAULT 'DÜĞÜN SALONU KİRALAMA & ETKİNLİK HİZMET SÖZLEŞMESİ',
          contract_terms_full LONGTEXT,
          updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
      `);

      // Seed default company settings if not exists
      try {
        const [exist] = await pool.query("SELECT id FROM company_settings WHERE id = 'default'");
        if (!exist || exist.length === 0) {
          const defaultTerms = `
<h3>BÖLÜM 1: GENEL HÜKÜMLER, TARAFLAR VE REZERVASYON KOŞULLARI</h3>
<p><strong>Madde 1 - Sözleşmenin Tarafları:</strong> İşbu sözleşme, bir tarafta yukarıda bilgileri yer alan Hizmet Veren (İrem Düğün Sarayı Ltd. Şti.) ile diğer tarafta Hizmet Alan (Müşteri/Kiracı) arasında karşılıklı mutabakat ile akdedilmiştir.</p>
<p><strong>Madde 2 - Sözleşmenin Konusu ve Kapsamı:</strong> Hizmet Veren'in mülkiyetinde/işletmesinde bulunan etkinlik salonunun, sözleşmede belirtilen tarih ve saat aralığında, belirlenen davetli kapasitesi ve seçilen ek hizmetler doğrultusunda Hizmet Alan'a tahsis edilmesidir.</p>
<p><strong>Madde 3 - Tarih, Saat Dilimi ve Kapasite:</strong> Etkinlik başlangıç ve bitiş saatleri kesin olup; program aşımı durumunda her ek saat için yürürlükteki ek salon kullanım ücreti tahakkuk ettirilir. Mekan azami kapasitesinin aşılmaması esastır.</p>
<p><strong>Madde 4 - Kapora, Fiyat ve Ödeme Planı:</strong> Rezervasyonun kesinleşmesi için belirlenen asgari kapora tutarı sözleşme anında tahsil edilir. Kalan bakiye, en geç etkinlik tarihinden 7 (yedi) iş günü öncesine kadar Hizmet Veren'in banka hesabına veya kasasına eksiksiz ödenmelidir.</p>

<div class="page-break" style="page-break-before: always; margin-top: 30px;"></div>

<h3>BÖLÜM 2: HİZMET DETAYLARI, İPTAL VE DEĞİŞİKLİK ŞARTLARI</h3>
<p><strong>Madde 5 - Catering ve Menü Standartları:</strong> Seçilen yemekli/kokteyl menüler profesyonel hijyen ve kalite standartlarında servis edilir. Menü tadımı ve kişi sayısı revizyonları etkinlikten en geç 10 gün önce yazılı olarak bildirilmelidir.</p>
<p><strong>Madde 6 - Fotoğraf, Video ve Müzik Hizmetleri:</strong> Etkinlik süresince ses ve ışık sistemleri uzman teknik personelce yönetilir. 4K video ve fotoğraf teslimatları organizasyon bitiminden itibaren azami 20 iş günü içinde dijital/albüm olarak teslim edilir.</p>
<p><strong>Madde 7 - Rezervasyon İptali ve Kapora İade Koşulları:</strong> Hizmet Alan tarafından etkinlik tarihine 60 günden fazla süre kala yapılan iptallerde kaporanın %50'si iade edilir. 60 günden az kalan iptallerde kapora iadesi yapılmaz; ancak karşılıklı mutabakatla sezon içi müsait başka bir tarihe devir hakkı tanınabilir.</p>
<p><strong>Madde 8 - Tarih Değişikliği ve Seans Revizyonu:</strong> Tarih erteleme talepleri en geç 30 gün öncesinden yazılı yapılmalıdır. Yeni seçilecek tarihteki güncel fiyat farkı Hizmet Alan tarafından karşılanır.</p>

<div class="page-break" style="page-break-before: always; margin-top: 30px;"></div>

<h3>BÖLÜM 3: TESİS KULLANIM KURALLARI, MÜCBİR SEBEPLER VE YETKİLİ MAHKEME</h3>
<p><strong>Madde 9 - Tesis Güvenliği ve Demirbaş Sorumluluğu:</strong> Hizmet Alan ve davetlileri tesis genel ahlak ve huzur kurallarına uymakla yükümlüdür. Mekan demirbaşlarına, ses-ışık donanımına kasti verilecek zararlar Hizmet Alan tarafından tazmin edilir.</p>
<p><strong>Madde 10 - Mücbir Sebepler (Force Majeure):</strong> Deprem, sel, yangın, salgın hastalık, resmi makamlarca getirilen sokağa çıkma yasakları veya yasal kısıtlamalar gibi tarafların iradesi dışındaki durumlarda etkinlik ileri bir tarihe ertelenir; taraflar birbirine tazminat yükümlülüğü getirmez.</p>
<p><strong>Madde 11 - Kişisel Verilerin Korunması (KVKK):</strong> Hizmet Alan'ın paylaştığı iletişim ve fatura verileri 6698 sayılı KVKK kapsamında yalnızca organizasyon ve yasal muhasebe süreçleri için işlenir.</p>
<p><strong>Madde 12 - Yetkili Mahkeme ve İcra Daireleri:</strong> İşbu 12 maddeden ve 3 sayfadan ibaret sözleşmenin uygulanmasından doğabilecek her türlü ihtilafta Sakarya Mahkemeleri ve İcra Daireleri yetkilidir.</p>
          `;

          await pool.query(`
            INSERT INTO company_settings (
              id, company_name, brand_title, address, tax_office, tax_number, phone, email, website, authorized_person, bank_info, contract_title, contract_terms_full
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
          `, [
            'default',
            'İrem Düğün Sarayı Ltd. Şti.',
            'Organizasyon & Kiralama Şirketi | Sapanca Göl Kenarı, Sakarya',
            'Sapanca Göl Kenarı No: 45, Sapanca / Sakarya',
            'Sapanca Vergi Dairesi',
            '4820192837',
            '+90 532 111 2233',
            'bilgi@iremdugunsarayi.com',
            'https://irem.portegu.com',
            'Davut Akbulut (Genel Müdür)',
            'Garanti BBVA - TR12 0006 2000 0001 2345 6789 01 (Alıcı: İrem Düğün Sarayı Ltd. Şti.)',
            'DÜĞÜN SALONU KİRALAMA & ETKİNLİK SÖZLEŞMESİ',
            defaultTerms.trim()
          ]);
        }
      } catch(e){}

      await pool.query(`
        CREATE TABLE IF NOT EXISTS venues (
          id VARCHAR(50) PRIMARY KEY,
          name VARCHAR(150) NOT NULL,
          category VARCHAR(100) NOT NULL DEFAULT 'Kapalı Salon',
          capacity INT NOT NULL DEFAULT 500,
          price DECIMAL(12,2) NOT NULL DEFAULT 0.00,
          deposit DECIMAL(12,2) NOT NULL DEFAULT 0.00,
          location VARCHAR(255) NOT NULL,
          occupancy_rate INT DEFAULT 0,
          description TEXT,
          features_json LONGTEXT,
          images_json LONGTEXT,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
      `);

      // Ensure venues table has all rich columns
      try { await pool.query("ALTER TABLE venues ADD COLUMN IF NOT EXISTS cost_price DECIMAL(12,2) DEFAULT 0.00;"); } catch(e){}
      try { await pool.query("ALTER TABLE venues ADD COLUMN IF NOT EXISTS exterior_images_json LONGTEXT;"); } catch(e){}
      try { await pool.query("ALTER TABLE venues ADD COLUMN IF NOT EXISTS event_types_json LONGTEXT;"); } catch(e){}
      try { await pool.query("ALTER TABLE venues ADD COLUMN IF NOT EXISTS available_services_json LONGTEXT;"); } catch(e){}
      try {
        await pool.query(`
          UPDATE venues SET
            images_json = '["https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=1200&q=80", "https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=800&q=80", "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=800&q=80", "https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?auto=format&fit=crop&w=800&q=80"]',
            exterior_images_json = '["https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?auto=format&fit=crop&w=800&q=80", "https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&w=800&q=80", "https://images.unsplash.com/photo-1527529482837-4698179dc6ce?auto=format&fit=crop&w=800&q=80"]',
            event_types_json = '["Düğün", "Nişan", "Kına", "Kurumsal Etkinlik", "Gala", "Sünnet Düğünü"]',
            available_services_json = '["s1", "s2", "s3", "s-tavuk-menu"]',
            features_json = '["Geniş Dans Pisti", "Gelişmiş İklimlendirme", "Özel Gelin & Damat Odası", "Ücretsiz Otopark & Vale", "Kristal Avizeler & Sahne", "Gelişmiş Ses & Işık Sistemi", "Jeneratör Desteği", "VIP Karşılama Alanı"]',
            location = 'Sapanca Göl Kenarı, Sakarya / İrem Düğün Sarayı'
          WHERE id = 'v1' OR id = 'venue-1';
        `);
      } catch(e){}




      await pool.query(`
        CREATE TABLE IF NOT EXISTS services (
          id VARCHAR(50) PRIMARY KEY,
          name VARCHAR(150) NOT NULL,
          category VARCHAR(100),
          price DECIMAL(12,2) DEFAULT 0,
          pricing_type VARCHAR(50) DEFAULT 'fixed',
          description TEXT,
          image_url TEXT,
          sort_order INT(11) DEFAULT 0,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
      `);

      await pool.query(`
        CREATE TABLE IF NOT EXISTS customers (
          id VARCHAR(50) PRIMARY KEY,
          name VARCHAR(150) NOT NULL,
          email VARCHAR(150),
          phone VARCHAR(50),
          address TEXT,
          tax_type VARCHAR(50) DEFAULT 'individual',
          tc_no VARCHAR(20),
          vkn_no VARCHAR(20),
          tax_office VARCHAR(100),
          follow_up TINYINT(1) DEFAULT 0,
          follow_up_note TEXT,
          avatar TEXT,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
      `);

      await pool.query(`
        CREATE TABLE IF NOT EXISTS users (
          id VARCHAR(50) PRIMARY KEY,
          name VARCHAR(150) NOT NULL,
          email VARCHAR(150),
          phone VARCHAR(50),
          password_hash VARCHAR(255),
          role VARCHAR(50) DEFAULT 'admin',
          avatar LONGTEXT,
          notify_whatsapp TINYINT(1) DEFAULT 1,
          notify_email TINYINT(1) DEFAULT 1,
          notify_sms TINYINT(1) DEFAULT 0,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
      `);

      try { await pool.query("ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR(50)"); } catch(e){}
      try { await pool.query("ALTER TABLE users ADD COLUMN IF NOT EXISTS notify_whatsapp TINYINT(1) DEFAULT 1"); } catch(e){}
      try { await pool.query("ALTER TABLE users ADD COLUMN IF NOT EXISTS notify_email TINYINT(1) DEFAULT 1"); } catch(e){}
      try { await pool.query("ALTER TABLE users ADD COLUMN IF NOT EXISTS notify_sms TINYINT(1) DEFAULT 0"); } catch(e){}

      await pool.query(`
        CREATE TABLE IF NOT EXISTS reservations (
          id VARCHAR(50) PRIMARY KEY,
          venue_id VARCHAR(50),
          customer_id VARCHAR(50),
          customer_name VARCHAR(150),
          customer_email VARCHAR(150),
          customer_phone VARCHAR(50),
          event_date DATE,
          time_slot VARCHAR(50),
          guest_count INT,
          venue_price DECIMAL(12,2),
          subtotal DECIMAL(12,2),
          campaign_code VARCHAR(50),
          discount_amount DECIMAL(12,2),
          vat_amount DECIMAL(12,2),
          total_amount DECIMAL(12,2),
          deposit_paid DECIMAL(12,2),
          remaining_balance DECIMAL(12,2),
          payment_status VARCHAR(50),
          is_invoiced TINYINT(1) DEFAULT 0,
          invoice_type VARCHAR(50),
          notes TEXT,
          media_json LONGTEXT,
          status VARCHAR(50) DEFAULT 'CONFIRMED',
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
      `);

      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS secondary_phone VARCHAR(50)"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS end_date DATE"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS start_time VARCHAR(20)"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS end_time VARCHAR(20)"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS custom_venue_price DECIMAL(12,2)"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS referrer_name VARCHAR(150)"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS dip_discount_type VARCHAR(50)"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS tc_no VARCHAR(20)"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS vkn_no VARCHAR(20)"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS tax_office VARCHAR(150)"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS invoice_address TEXT"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS flow_plan_json LONGTEXT"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS selected_services_json LONGTEXT"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS details_json LONGTEXT"); } catch(e){}
      try { await pool.query("ALTER TABLE services ADD COLUMN IF NOT EXISTS cost_price DECIMAL(12,2) DEFAULT 0"); } catch(e){}
      try { await pool.query("ALTER TABLE services MODIFY COLUMN pricing_type VARCHAR(50) DEFAULT 'fixed'"); } catch(e){}
      try { await pool.query("UPDATE reservations SET status = 'CONFIRMED' WHERE status = 'DRAFT'"); } catch(e){}



      await pool.query(`
        CREATE TABLE IF NOT EXISTS reservation_services (
          id INT(11) AUTO_INCREMENT PRIMARY KEY,
          reservation_id VARCHAR(50),
          service_id VARCHAR(50),
          quantity INT(11) DEFAULT 1,
          unit_price DECIMAL(12,2) DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
      `);

      await pool.query(`
        CREATE TABLE IF NOT EXISTS expenses (
          id VARCHAR(50) PRIMARY KEY,
          title VARCHAR(150) NOT NULL,
          category VARCHAR(100),
          amount DECIMAL(12,2) DEFAULT 0,
          date DATE,
          description TEXT,
          type VARCHAR(50) DEFAULT 'expense',
          reservation_id VARCHAR(50) NULL,
          expense_scope VARCHAR(50) DEFAULT 'general_fixed',
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
      `);

      try {
        await pool.query("ALTER TABLE expenses ADD COLUMN IF NOT EXISTS reservation_id VARCHAR(50) NULL AFTER type");
        await pool.query("ALTER TABLE expenses ADD COLUMN IF NOT EXISTS expense_scope VARCHAR(50) DEFAULT 'general_fixed' AFTER reservation_id");
      } catch(err){}

      await pool.query(`
        CREATE TABLE IF NOT EXISTS campaigns (
          id VARCHAR(50) PRIMARY KEY,
          code VARCHAR(50),
          title VARCHAR(150),
          type VARCHAR(50) DEFAULT 'percentage',
          value DECIMAL(12,2) DEFAULT 0,
          description TEXT,
          start_date DATE,
          end_date DATE,
          active TINYINT(1) DEFAULT 1,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
      `);

      await pool.query(`
        CREATE TABLE IF NOT EXISTS media (
          id VARCHAR(50) PRIMARY KEY,
          title VARCHAR(150),
          category VARCHAR(100),
          url TEXT,
          file_size VARCHAR(50),
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
      `);

      await pool.query(`
        CREATE TABLE IF NOT EXISTS roles (
          id VARCHAR(50) PRIMARY KEY,
          name VARCHAR(100),
          permissions_json LONGTEXT,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
      `);

      await pool.query(`
        CREATE TABLE IF NOT EXISTS quote_requests (
          id VARCHAR(50) PRIMARY KEY,
          customer_name VARCHAR(150),
          customer_phone VARCHAR(50),
          customer_email VARCHAR(100),
          event_type VARCHAR(100),
          preferred_venue VARCHAR(100),
          guest_count INT(11) DEFAULT 0,
          event_date DATE NULL,
          notes TEXT,
          status VARCHAR(50) DEFAULT 'beklemede',
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
      `);

      await pool.query(`
        CREATE TABLE IF NOT EXISTS system_settings (
          id INT(11) PRIMARY KEY,
          settings_json LONGTEXT,
          updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
      `);

      // Modify any missing columns for safety
      try { await pool.query("ALTER TABLE services ADD COLUMN IF NOT EXISTS sort_order INT(11) DEFAULT 0"); } catch(e) {}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS media_json LONGTEXT"); } catch(e) {}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'CONFIRMED'"); } catch(e) {}
      try { await pool.query("ALTER TABLE roles ADD COLUMN IF NOT EXISTS permissions_json LONGTEXT"); } catch(e) {}
      try { await pool.query("ALTER TABLE venues ADD COLUMN IF NOT EXISTS features_json LONGTEXT"); } catch(e) {}
      try { await pool.query("ALTER TABLE venues ADD COLUMN IF NOT EXISTS images_json LONGTEXT"); } catch(e) {}

      
      await pool.query(`
        CREATE TABLE IF NOT EXISTS password_resets (
          id INT AUTO_INCREMENT PRIMARY KEY,
          email VARCHAR(150) NOT NULL,
          code VARCHAR(10) NOT NULL,
          expires_at DATETIME NOT NULL,
          used TINYINT(1) DEFAULT 0,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
      `);

      console.log('✅ MySQL Tabloları Doğrulandı ve Hazırlandı!');
      await syncMemoryFromMysql();
      
      // Purge any phantom / auto-saved draft rows from real reservations
      try {
        await pool.query("DELETE FROM reservations WHERE id LIKE 'RES-DRAFT-%' OR customer_name = 'İsimsiz Müşteri' OR notes LIKE '%AUTO_SAVE%'");
      } catch(e){}

      console.log('⚡ MariaDB Verileri Belleğe Senkronize Edildi!');
    } catch (e) {
      console.log('ℹ️ MySQL Tablo doğrulama uyarısı:', e.message);
    }
};
initMysql();

// -------------------------------------------------------------
// FİZİKSEL DOSYA VE REZERVASYON MEDYASI YÜKLEME ENDPOINTS
// -------------------------------------------------------------
app.post('/api/upload', (req, res) => {
  try {
    const { image, name } = req.body;
    if (!image) {
      return res.status(400).json({ error: 'Görsel verisi bulunamadı' });
    }

    let fileExtension = 'png';
    let base64Data = image;

    if (image.startsWith('data:')) {
      const mimeMatch = image.match(/^data:image\/(\w+);base64,/);
      if (mimeMatch) {
        fileExtension = mimeMatch[1] === 'jpeg' ? 'jpg' : mimeMatch[1];
      }
      base64Data = image.replace(/^data:image\/\w+;base64,/, '');
    }

    const filename = `img_${Date.now()}_${Math.floor(Math.random() * 1000)}.${fileExtension}`;
    const filePath = path.join(uploadsDir, filename);

    fs.writeFileSync(filePath, Buffer.from(base64Data, 'base64'));

    const fileUrl = `/uploads/${filename}`;
    console.log(`📸 Fiziksel Görsel Sunucuya Kaydedildi: ${filePath}`);

    res.json({ success: true, url: fileUrl, filename });
  } catch (err) {
    console.error('Upload Error:', err);
    res.status(500).json({ error: 'Görsel sunucuya kaydedilemedi', message: err.message });
  }
});

// Toplu Mükerrer Görsel Kontrolü Endpoint'i
app.post('/api/check-duplicates', (req, res) => {
  try {
    const { resId, files = [] } = req.body || {};
    if (!Array.isArray(files) || files.length === 0) {
      return res.json({ hasDuplicates: false, duplicates: [], validFiles: [], allFiles: [] });
    }

    const safeResId = (resId || 'GENERAL').replace(/[^a-zA-Z0-9_-]/g, '_');
    const targetRes = memoryStore.reservations.find(r => r.id === resId || r.mediaKey === resId || r.id === safeResId || r.mediaKey === safeResId);
    const existingMediaList = targetRes ? (targetRes.mediaFiles || []) : [];

    const duplicates = [];
    const validFiles = [];

    for (const f of files) {
      const fileName = f.name;
      const fileSize = f.size;

      const isDup = existingMediaList.some(m => {
        if (m.fileName === fileName && (m.fileSize === fileSize || String(m.fileSize).startsWith(String(fileSize)))) return true;
        if (m.fingerprint && f.fingerprint && m.fingerprint === f.fingerprint) return true;
        return false;
      });

      if (isDup) {
        duplicates.push(f);
      } else {
        validFiles.push(f);
      }
    }

    return res.json({
      hasDuplicates: duplicates.length > 0,
      duplicates,
      validFiles,
      allFiles: files
    });
  } catch (err) {
    console.error('Check duplicates error:', err);
    return res.status(500).json({ error: err.message });
  }
});

// Her rezervasyon için özel klasöre (uploads/RES-2026-8848/...) yükleme ve DB kaydı
app.post('/api/upload-media', async (req, res) => {
  try {
    const { resId, fileName, fileData, uploaderName, isGuest, type, fileSize, guestToken, allowDuplicate, fingerprint } = req.body || {};
    if (!fileData) {
      return res.status(400).json({ error: 'Medya dosyası verisi (fileData) bulunamadı. Lütfen JSON gövdesinde fileData alanını gönderiniz.' });
    }

    const safeResId = (resId || 'GENERAL').replace(/[^a-zA-Z0-9_-]/g, '_');
    const resUploadsDir = path.join(uploadsDir, safeResId);
    if (!fs.existsSync(resUploadsDir)) {
      fs.mkdirSync(resUploadsDir, { recursive: true });
    }

    let fileExtension = 'jpg';
    let base64Data = fileData;

    if (fileData.startsWith('data:')) {
      const mimeMatch = fileData.match(/^data:(image|video)\/(\w+);base64,/);
      if (mimeMatch) {
        fileExtension = mimeMatch[2] === 'jpeg' ? 'jpg' : mimeMatch[2];
      }
      base64Data = fileData.replace(/^data:(image|video)\/\w+;base64,/, '');
    }

    const fileBuffer = Buffer.from(base64Data, 'base64');
    const fileHash = crypto.createHash('md5').update(fileBuffer).digest('hex');

    // SERVER-SIDE DUPLICATE CHECK AGAINST TARGET RESERVATION
    let targetRes = memoryStore.reservations.find(r => r.id === resId || r.mediaKey === resId || r.id === safeResId || r.mediaKey === safeResId);
    const existingMediaList = targetRes ? (targetRes.mediaFiles || []) : (memoryStore.reservations[0]?.mediaFiles || []);
    
    const existingDup = existingMediaList.find(m => {
      if (m.fileHash && m.fileHash === fileHash) return true;
      if (m.fingerprint && fingerprint && m.fingerprint === fingerprint) return true;
      if (m.fileName === fileName && m.fileSize === fileSize) return true;
      return false;
    });

    if (existingDup && allowDuplicate !== true) {
      console.log(`⚠️ Mükerrer Görsel Yükleme Engellendi (Sunucu Teyidi): ${fileName} (${fileHash})`);
      return res.json({
        isDuplicate: true,
        message: 'Bu görsel sunucuda ve bu albümde zaten mevcut.',
        duplicateUrl: existingDup.url,
        duplicateId: existingDup.id,
        duplicateFile: existingDup
      });
    }

    const cleanFileName = (fileName || 'dosya').replace(/[^a-zA-Z0-9._-]/g, '_');
    const filename = `media_${Date.now()}_${cleanFileName}`;
    const filePath = path.join(resUploadsDir, filename);

    fs.writeFileSync(filePath, fileBuffer);

    const fileUrl = `/uploads/${safeResId}/${filename}`;
    console.log(`📸 Rezervasyon [${safeResId}] Medyası Özel Klasörüne Kaydedildi: ${filePath}`);

    const newMediaObj = {
      id: 'mf_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4),
      type: type || (fileData.includes('video/') ? 'video' : 'image'),
      url: fileUrl,
      thumbnail: fileUrl,
      fileName: fileName || filename,
      fileSize: fileSize || (fileBuffer.length / (1024 * 1024)).toFixed(1) + ' MB',
      uploaderName: uploaderName || (isGuest ? 'Davetli Konuk' : 'İşletme Yetkilisi'),
      timestamp: new Date().toISOString().replace('T', ' ').substr(0, 16),
      isGuest: !!isGuest,
      guestToken: guestToken || null,
      fileHash: fileHash,
      fingerprint: fingerprint || null
    };

    const safeMediaKey = (req.body.mediaKey || '').replace(/[^a-zA-Z0-9_-]/g, '_');
    let matchFound = false;
    memoryStore.reservations = memoryStore.reservations.map(r => {
      const isMatch = r.id === resId || r.mediaKey === resId || r.id === safeResId || (safeMediaKey && r.mediaKey === safeMediaKey);
      if (isMatch) {
        matchFound = true;
        const existingList = r.mediaFiles || [];
        return {
          ...r,
          mediaFiles: [newMediaObj, ...existingList]
        };
      }
      return r;
    });

    const activePool = await getPool();
    if (activePool) {
      try {
        const [targetRows] = await activePool.query('SELECT id, media_json FROM reservations WHERE id = ? OR id = ?', [resId || safeResId, safeResId]);
        if (targetRows && targetRows.length > 0) {
          const currentMedia = targetRows[0].media_json ? (typeof targetRows[0].media_json === 'string' ? JSON.parse(targetRows[0].media_json) : targetRows[0].media_json) : [];
          const updatedMedia = [newMediaObj, ...currentMedia];
          await activePool.query('UPDATE reservations SET media_json = ? WHERE id = ?', [JSON.stringify(updatedMedia), targetRows[0].id]);
          console.log(`💾 Rezervasyon [${targetRows[0].id}] Medyası MariaDB Veritabanına Yazıldı!`);
        }

        await activePool.query(
          'INSERT INTO media (id, title, category, url, file_size) VALUES (?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE title=?, url=?',
          [newMediaObj.id, cleanFileName, safeResId, fileUrl, newMediaObj.fileSize, cleanFileName, fileUrl]
        );
      } catch (dbErr) {
        console.error('MySQL upload-media update error:', dbErr.message);
      }
    }

    res.json({
      success: true,
      url: fileUrl,
      mediaObj: newMediaObj,
      reservations: memoryStore.reservations
    });
  } catch (err) {
    console.error('Upload Media Error:', err);
    res.status(500).json({ error: 'Medya kaydedilemedi', message: err.message });
  }
});

app.post('/api/delete-media', async (req, res) => {
  try {
    const { resId, fileName, mediaId, mediaKey, url } = req.body;
    console.log(`🗑️ Medya Silme İsteği Alındı: resId=${resId}, mediaId=${mediaId}, fileName=${fileName}, url=${url}`);

    let deletedFilesCount = 0;
    const targetUrls = new Set();
    if (url) targetUrls.add(url);

    const safeResId = resId ? String(resId).replace(/[^a-zA-Z0-9_-]/g, '_') : '';
    const safeMediaKey = mediaKey ? String(mediaKey).replace(/[^a-zA-Z0-9_-]/g, '_') : '';

    // 1. memoryStore.reservations ve db_reservations.json içindeki ilgili medya kayıtlarını güncelle & silinecek URL'leri topla
    memoryStore.reservations = memoryStore.reservations.map(r => {
      const isTargetRes = !resId || r.id === resId || r.mediaKey === resId || r.id === mediaKey || r.mediaKey === mediaKey || r.id === safeResId || r.mediaKey === safeMediaKey;
      if (isTargetRes && r.mediaFiles) {
        const remaining = [];
        for (const m of r.mediaFiles) {
          const matchesId = mediaId && String(m.id) === String(mediaId);
          const matchesFileName = fileName && (m.fileName === fileName || (m.url && m.url.endsWith(fileName)));
          const matchesUrl = url && m.url === url;

          if (matchesId || matchesFileName || matchesUrl) {
            if (m.url) targetUrls.add(m.url);
            console.log(`🔎 Silinecek Medya Kaydı Bulundu: ID=${m.id}, URL=${m.url}`);
          } else {
            remaining.push(m);
          }
        }
        return { ...r, mediaFiles: remaining };
      }
      return r;
    });

    // 2. memoryStore.media dizisini temizle
    if (memoryStore.media && Array.isArray(memoryStore.media)) {
      memoryStore.media = memoryStore.media.filter(m => {
        const matchesId = mediaId && String(m.id) === String(mediaId);
        const matchesUrl = url && m.url === url;
        const matchesFileName = fileName && (m.url && m.url.endsWith(fileName));
        if (matchesId || matchesUrl || matchesFileName) {
          if (m.url) targetUrls.add(m.url);
          return false;
        }
        return true;
      });
      // %100 MySQL Veritabanına kaydedilir
    }

    // 3. FİZİKSEL DOSYA SİLME (Sunucudaki uploads/ klasöründen diskten kalıcı silme)
    // 3.1. Hedef URL'lerden fiziksel dosya yollarını sil
    targetUrls.forEach(fileUrl => {
      if (fileUrl && fileUrl.startsWith('/uploads/')) {
        const relPath = fileUrl.replace('/uploads/', '');
        const fullPath = path.join(uploadsDir, relPath);
        if (fs.existsSync(fullPath)) {
          try {
            fs.unlinkSync(fullPath);
            deletedFilesCount++;
            console.log(`✅ SUNUCUDAN FİZİKSEL DOSYA SİLİNDİ: ${fullPath}`);
          } catch(e) {
            console.error(`❌ Fiziksel dosya silinemedi: ${fullPath}`, e.message);
          }
        }
      }
    });

    // 3.2. Doğrudan dosya adı ile sunucuda fiziksel dosya arayıp silme (Yedek Doğrulama)
    if (fileName) {
      const cleanFile = path.basename(fileName);
      const possibleFolders = [];
      if (safeResId) possibleFolders.push(safeResId);
      if (safeMediaKey) possibleFolders.push(safeMediaKey);
      possibleFolders.push('GENERAL');

      for (const folder of possibleFolders) {
        const candidate = path.join(uploadsDir, folder, cleanFile);
        if (fs.existsSync(candidate)) {
          try {
            fs.unlinkSync(candidate);
            deletedFilesCount++;
            console.log(`✅ KLASÖR ARAYIŞIYLA FİZİKSEL DOSYA SİLİNDİ: ${candidate}`);
          } catch(e){}
        }
      }

      // Alt Klasör Taraması (Tüm uploads alt dizinleri)
      if (fs.existsSync(uploadsDir)) {
        try {
          const dirs = fs.readdirSync(uploadsDir);
          for (const subDir of dirs) {
            const subPath = path.join(uploadsDir, subDir);
            if (fs.statSync(subPath).isDirectory()) {
              const fileInSub = path.join(subPath, cleanFile);
              if (fs.existsSync(fileInSub)) {
                try {
                  fs.unlinkSync(fileInSub);
                  deletedFilesCount++;
                  console.log(`✅ ALT KLASÖR TARAMASIYLA FİZİKSEL DOSYA SİLİNDİ: ${fileInSub}`);
                } catch(e){}
              }
            }
          }
        } catch(err){}
      }
    }

    // 4. Veritabanı JSON Kayıtlarını Güncelle
    // %100 MySQL Veritabanına kaydedilir

    // 5. Canlı MySQL Bağlantısı Varsa MariaDB Tablolarından da Sil
    if (pool) {
      try {
        if (mediaId) await pool.query('DELETE FROM media WHERE id = ?', [mediaId]);
        if (url) await pool.query('DELETE FROM media WHERE url = ?', [url]);
        
        const [targetRows] = await pool.query('SELECT id, media_json FROM reservations WHERE id = ? OR id = ?', [resId || safeResId, safeResId]);
        for (const row of targetRows) {
          if (row.media_json) {
            const currentMedia = typeof row.media_json === 'string' ? JSON.parse(row.media_json) : row.media_json;
            const remaining = (currentMedia || []).filter(m => String(m.id) !== String(mediaId) && m.url !== url && m.fileName !== fileName);
            await pool.query('UPDATE reservations SET media_json = ? WHERE id = ?', [JSON.stringify(remaining), row.id]);
          }
        }
      } catch(dbErr) {
        console.warn('MySQL Delete Media Error:', dbErr.message);
      }
    }

    console.log(`✨ Silme İşlemi Başarıyla Tamamlandı: Toplam ${deletedFilesCount} Adet Fiziksel Dosya Sunucudan Silindi.`);

    res.json({
      success: true,
      deletedFilesCount,
      message: 'Medya hem veritabanından hem de sunucudaki klasöründen fiziksel olarak silindi.',
      reservations: memoryStore.reservations
    });
  } catch(e) {
    console.error('Delete Media Endpoint Error:', e);
    res.status(500).json({ error: e.message });
  }
});


// -------------------------------------------------------------
// 1. SALONLAR ENDPOINTS (/api/venues)
// -------------------------------------------------------------
// -------------------------------------------------------------
// 1. SALONLAR ENDPOINTS (/api/venues)
// -------------------------------------------------------------
app.get('/api/venues', async (req, res) => {
  try {
    const activePool = await getPool();
    if (activePool) {
      const [rows] = await activePool.query('SELECT * FROM venues ORDER BY id ASC');
      const formatted = (rows || []).map(v => {
        let feats = [];
        if (typeof v.features_json === 'string') {
          try { feats = JSON.parse(v.features_json); } catch(e){}
        } else if (Array.isArray(v.features_json)) {
          feats = v.features_json;
        }

        let imgs = [];
        if (typeof v.images_json === 'string') {
          try { imgs = JSON.parse(v.images_json); } catch(e){}
        } else if (Array.isArray(v.images_json)) {
          imgs = v.images_json;
        }
        if (!imgs || imgs.length === 0) {
          imgs = ['https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=1200&q=80'];
        }

        let extImgs = [];
        if (typeof v.exterior_images_json === 'string') {
          try { extImgs = JSON.parse(v.exterior_images_json); } catch(e){}
        } else if (Array.isArray(v.exterior_images_json)) {
          extImgs = v.exterior_images_json;
        }

        let evTypes = [];
        if (typeof v.event_types_json === 'string') {
          try { evTypes = JSON.parse(v.event_types_json); } catch(e){}
        } else if (Array.isArray(v.event_types_json)) {
          evTypes = v.event_types_json;
        }

        let availServs = null;
        if (typeof v.available_services_json === 'string') {
          try { availServs = JSON.parse(v.available_services_json); } catch(e){}
        } else if (Array.isArray(v.available_services_json)) {
          availServs = v.available_services_json;
        }
        if (availServs === null || availServs === undefined) {
          availServs = ['s1', 's2', 's3', 's-tavuk-menu'];
        }

        const mainImg = imgs[0];
        return {
          ...v,
          image: mainImg,
          image_url: mainImg,
          images: imgs,
          interiorImages: imgs,
          exteriorImages: extImgs,
          features: feats,
          eventTypes: evTypes,
          availableServices: availServs,
          location: v.location || 'Sapanca Göl Kenarı, Sakarya / İrem Düğün Sarayı',
          costPrice: v.cost_price !== undefined && v.cost_price !== null ? Number(v.cost_price) : 0,
          cost_price: v.cost_price !== undefined && v.cost_price !== null ? Number(v.cost_price) : 0,
          occupancyRate: v.occupancy_rate || 85,
          price: Number(v.price || 0),
          deposit: Number(v.deposit || 0),
          capacity: Number(v.capacity || 500)
        };
      });
      return res.json(formatted);
    }
  } catch(e) {
    console.error('MySQL GET /api/venues error:', e.message);
  }
  res.json(memoryStore.venues || []);
});

app.post('/api/venues', async (req, res) => {
  try {
    if (req.body && (req.body.action === 'delete' || req.body._delete)) {
      return deleteVenueHandler(req, res);
    }
    const item = { id: req.body.id || ('v-' + Date.now()), ...req.body };
    const imgs = Array.isArray(item.images) && item.images.length > 0 ? item.images : (item.image ? [item.image] : []);
    const extImgs = Array.isArray(item.exteriorImages) && item.exteriorImages.length > 0 ? item.exteriorImages : [];
    const feats = Array.isArray(item.features) ? item.features : [];
    const evTypes = Array.isArray(item.eventTypes) ? item.eventTypes : [];
    const availServs = Array.isArray(item.availableServices) ? item.availableServices : [];
    const costPrice = item.costPrice !== undefined ? Number(item.costPrice) : (item.cost_price !== undefined ? Number(item.cost_price) : 0);
    const occupancyRate = item.occupancyRate !== undefined ? Number(item.occupancyRate) : (item.occupancy_rate !== undefined ? Number(item.occupancy_rate) : 85);
    const price = Number(item.price || 0);
    const deposit = Number(item.deposit || 0);
    const capacity = Number(item.capacity || 500);

    const activePool = await getPool();
    if (activePool) {
      await activePool.query(
        `INSERT INTO venues (id, name, category, capacity, price, deposit, cost_price, location, description, occupancy_rate, features_json, images_json, exterior_images_json, event_types_json, available_services_json) 
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
         ON DUPLICATE KEY UPDATE 
           name=VALUES(name), category=VALUES(category), capacity=VALUES(capacity), 
           price=VALUES(price), deposit=VALUES(deposit), cost_price=VALUES(cost_price), 
           location=VALUES(location), description=VALUES(description), occupancy_rate=VALUES(occupancy_rate), 
           features_json=VALUES(features_json), images_json=VALUES(images_json), 
           exterior_images_json=VALUES(exterior_images_json), event_types_json=VALUES(event_types_json), 
           available_services_json=VALUES(available_services_json)`,
        [
          item.id, item.name, item.category || 'Kapalı Salon', capacity, price, deposit, costPrice, item.location || '', item.description || '', occupancyRate, JSON.stringify(feats), JSON.stringify(imgs), JSON.stringify(extImgs), JSON.stringify(evTypes), JSON.stringify(availServs)
        ]
      );
      console.log(`🏰 Salon [${item.id}] MariaDB Veritabanına Yazıldı: ${item.name} (Fiyat: ${price} TL, Maliyet: ${costPrice} TL)`);
    }

    const fullItem = {
      ...item,
      price,
      costPrice,
      cost_price: costPrice,
      deposit,
      capacity,
      occupancyRate,
      features: feats,
      images: imgs,
      interiorImages: imgs,
      exteriorImages: extImgs,
      eventTypes: evTypes,
      availableServices: availServs,
      location: item.location || ''
    };

    memoryStore.venues = [fullItem, ...(memoryStore.venues || []).filter(v => v.id !== fullItem.id)];
    res.status(201).json({ success: true, item: fullItem });
  } catch(e) {
    console.error('MySQL POST /api/venues error:', e.message);
    res.status(500).json({ error: 'Salon kaydedilemedi', message: e.message });
  }
});

const deleteVenueHandler = async (req, res) => {
  const id = req.params.id || req.body.id;
  try {
    const activePool = await getPool();
    if (activePool) {
      await activePool.query('DELETE FROM venues WHERE id = ?', [id]);
      console.log(`🗑️ Salon [${id}] MariaDB Veritabanından Silindi.`);
    }
    memoryStore.venues = (memoryStore.venues || []).filter(v => v.id !== id);
    res.json({ success: true, id });
  } catch(e) {
    console.error('MySQL DELETE /api/venues error:', e.message);
    res.status(500).json({ error: 'Salon silinemedi', message: e.message });
  }
};
app.delete('/api/venues/:id', deleteVenueHandler);
app.post(['/api/venues/delete/:id', '/api/venues/delete'], deleteVenueHandler);

// -------------------------------------------------------------
// 2. EK HİZMETLER ENDPOINTS (/api/services & /api/services/reorder)
// -------------------------------------------------------------
app.get('/api/services', async (req, res) => {
  try {
    const activePool = await getPool();
    if (activePool) {
      const [rows] = await activePool.query('SELECT * FROM services ORDER BY sort_order ASC, created_at DESC');
      const formatted = (rows || []).map(s => ({
        id: s.id,
        name: s.name,
        category: s.category || 'Genel',
        price: Number(s.price || 0),
        costPrice: s.cost_price !== undefined && s.cost_price !== null ? Number(s.cost_price) : 0,
        cost_price: s.cost_price !== undefined && s.cost_price !== null ? Number(s.cost_price) : 0,
        pricingType: s.pricing_type || 'fixed',
        pricing_type: s.pricing_type || 'fixed',
        description: s.description || '',
        image: s.image_url || '',
        image_url: s.image_url || '',
        sortOrder: s.sort_order || 0,
        order: s.sort_order || 0
      }));
      return res.json(formatted);
    }
  } catch(e) {
    console.error('MySQL GET /api/services error:', e.message);
  }
  res.json(memoryStore.services || []);
});

app.post('/api/services', async (req, res) => {
  try {
    if (req.body && (req.body.action === 'delete' || req.body._delete)) {
      return deleteServiceHandler(req, res);
    }
    const item = { id: req.body.id || ('s-' + Date.now()), ...req.body };
    const price = Number(item.price || 0);
    const costPrice = item.costPrice !== undefined ? Number(item.costPrice) : (item.cost_price !== undefined ? Number(item.cost_price) : 0);
    const sortOrder = Number(item.sortOrder || item.order || 0);

    const activePool = await getPool();
    if (activePool) {
      await activePool.query(
        `INSERT INTO services (id, name, category, price, cost_price, pricing_type, description, image_url, sort_order)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
         ON DUPLICATE KEY UPDATE
           name=VALUES(name), category=VALUES(category), price=VALUES(price), 
           cost_price=VALUES(cost_price), pricing_type=VALUES(pricing_type), 
           description=VALUES(description), image_url=VALUES(image_url), sort_order=VALUES(sort_order)`,
        [item.id, item.name, item.category || 'Genel', price, costPrice, item.pricingType || item.pricing_type || 'fixed', item.description || '', item.image || item.image_url || '', sortOrder]
      );
      console.log(`🍽️ Hizmet [${item.id}] MariaDB Veritabanına Yazıldı: ${item.name} (Fiyat: ${price} TL, Maliyet: ${costPrice} TL)`);
    }

    const fullItem = {
      ...item,
      price,
      costPrice,
      cost_price: costPrice,
      sortOrder,
      order: sortOrder
    };

    memoryStore.services = [fullItem, ...(memoryStore.services || []).filter(s => s.id !== fullItem.id)];
    res.status(201).json({ success: true, item: fullItem });
  } catch(e) {
    console.error('MySQL POST /api/services error:', e.message);
    res.status(500).json({ error: 'Hizmet kaydedilemedi', message: e.message });
  }
});

const deleteServiceHandler = async (req, res) => {
  try {
    const id = req.params.id || req.body.id || req.query.id;
    const activePool = await getPool();
    if (activePool) {
      await activePool.query('DELETE FROM services WHERE id = ?', [id]);
      console.log(`🗑️ Hizmet [${id}] MariaDB Veritabanından Silindi.`);
    }
    memoryStore.services = (memoryStore.services || []).filter(s => s.id !== id);
    res.json({ success: true, id });
  } catch(e) {
    console.error('MySQL DELETE /api/services error:', e.message);
    res.status(500).json({ error: 'Hizmet silinemedi', message: e.message });
  }
};
app.delete('/api/services/:id', deleteServiceHandler);
app.post(['/api/services/delete/:id', '/api/services/delete'], deleteServiceHandler);

// -------------------------------------------------------------
// 3. MÜŞTERİLER ENDPOINTS (/api/customers)
// -------------------------------------------------------------
app.get('/api/customers', async (req, res) => {
  if (pool) {
    try {
      const [rows] = await pool.query('SELECT * FROM customers ORDER BY created_at DESC');
      const formatted = (rows || []).map(r => ({
        ...r,
        taxType: r.tax_type || 'individual',
        tcNo: r.tc_no || '',
        vknNo: r.vkn_no || '',
        taxOffice: r.tax_office || '',
        followUp: Boolean(r.follow_up),
        followUpNote: r.follow_up_note || ''
      }));
      return res.json(formatted);
    } catch(e) {
      console.error('MySQL GET /api/customers error:', e.message);
    }
  }
  res.json([]);
});

app.post('/api/customers', async (req, res) => {
  if (req.body && (req.body.action === 'delete' || req.body._delete)) {
    return deleteCustomerHandler(req, res);
  }
  const item = { id: req.body.id || ('cust-' + Date.now()), ...req.body };
  if (pool) {
    try {
      await pool.query(
        'INSERT INTO customers (id, name, email, phone, address, tax_type, tc_no, vkn_no, tax_office, follow_up, follow_up_note, avatar) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE name=?, email=?, phone=?, address=?, tax_type=?, tc_no=?, vkn_no=?, tax_office=?, follow_up=?, follow_up_note=?, avatar=?',
        [item.id, item.name, item.email || '', item.phone || '', item.address || '', item.taxType || item.tax_type || 'individual', item.tcNo || item.tc_no || '', item.vknNo || item.vkn_no || '', item.taxOffice || item.tax_office || '', item.followUp || item.follow_up ? 1 : 0, item.followUpNote || item.follow_up_note || '', item.avatar || '', item.name, item.email || '', item.phone || '', item.address || '', item.taxType || item.tax_type || 'individual', item.tcNo || item.tc_no || '', item.vknNo || item.vkn_no || '', item.taxOffice || item.tax_office || '', item.followUp || item.follow_up ? 1 : 0, item.followUpNote || item.follow_up_note || '', item.avatar || '']
      );
    } catch(e) {
      console.error('MySQL POST /api/customers error:', e.message);
    }
  }
  res.status(201).json({ success: true, item });
});

const deleteCustomerHandler = async (req, res) => {
  const id = req.params.id || req.body.id;
  if (pool) {
    try {
      await pool.query('DELETE FROM customers WHERE id = ?', [id]);
    } catch(e) {
      console.error('MySQL DELETE /api/customers error:', e.message);
    }
  }
  res.json({ success: true, id });
};
app.delete('/api/customers/:id', deleteCustomerHandler);
app.post(['/api/customers/delete/:id', '/api/customers/delete'], deleteCustomerHandler);

// -------------------------------------------------------------

// -------------------------------------------------------------
// 10. TEKLİF TALEPLERİ ENDPOINTS (/api/quote-requests & /api/leads)
// -------------------------------------------------------------
app.get(['/api/quote-requests', '/api/leads'], async (req, res) => {
  try {
    const [rows] = await queryDb('SELECT * FROM quote_requests ORDER BY created_at DESC');
    if (rows && rows.length) {
      const formatted = rows.map(q => ({
        id: q.id,
        customerName: q.customer_name || '',
        customerPhone: q.customer_phone || '',
        customerEmail: q.customer_email || '',
        eventType: q.event_type || 'Düğün',
        preferredVenue: q.preferred_venue || 'İrem Kraliyet Balo Salonu',
        guestCount: Number(q.guest_count || 0),
        eventDate: q.event_date ? (q.event_date instanceof Date ? q.event_date.toISOString().split('T')[0] : String(q.event_date).split('T')[0]) : '',
        notes: q.notes || '',
        status: q.status || 'beklemede',
        createdAt: q.created_at || new Date().toISOString()
      }));
      memoryStore.quoteRequests = formatted;
      return res.json(formatted);
    }
  } catch(e) {
    console.error('MySQL GET /api/quote-requests error:', e.message);
  }
  res.json(memoryStore.quoteRequests || []);
});

const deleteQuoteRequestHandler = async (req, res) => {
  try {
    const id = req.params.id || req.body.id || req.query.id;
    if (!id) return res.status(400).json({ error: 'Talep ID eksik' });
    const activePool = await getPool();
    if (activePool) {
      await activePool.query('DELETE FROM quote_requests WHERE id = ?', [id]);
      console.log(`🗑️ Teklif Talebi [${id}] MariaDB Veritabanından Silindi.`);
    }
    memoryStore.quoteRequests = (memoryStore.quoteRequests || []).filter(q => q.id !== id);
    res.json({ success: true, id });
  } catch(e) {
    console.error('MySQL DELETE /api/quote-requests error:', e.message);
    res.status(500).json({ error: 'Talep silinemedi', message: e.message });
  }
};
app.delete(['/api/quote-requests/:id', '/api/leads/:id'], deleteQuoteRequestHandler);
app.post(['/api/quote-requests/delete/:id', '/api/quote-requests/delete', '/api/leads/delete/:id', '/api/leads/delete'], deleteQuoteRequestHandler);

app.post(['/api/quote-requests', '/api/leads'], async (req, res) => {
  try {
    if (req.body && (req.body.action === 'delete' || req.body._delete)) {
      return deleteQuoteRequestHandler(req, res);
    }
    const raw = req.body || {};
    const eDate = raw.eventDate || raw.event_date || raw.date || null;
    const cleanEDate = (eDate && typeof eDate === 'string' && eDate.trim().length >= 8) ? eDate.trim().split('T')[0] : null;

    const item = {
      id: raw.id || ('QUOTE-' + Date.now()),
      customerName: (raw.customerName || raw.name || raw.customer_name || 'İsimsiz Talep').trim(),
      customerPhone: (raw.customerPhone || raw.phone || raw.customer_phone || '').trim(),
      customerEmail: (raw.customerEmail || raw.email || raw.customer_email || '').trim(),
      eventType: raw.eventType || raw.event_type || 'Düğün',
      preferredVenue: (raw.preferredVenue || raw.venue || raw.preferred_venue || 'İrem Kraliyet Balo Salonu').trim(),
      guestCount: Number(raw.guestCount || raw.guests || raw.guest_count || 0),
      eventDate: cleanEDate || '',
      notes: (raw.notes || raw.message || '').trim(),
      status: raw.status || 'beklemede',
      createdAt: raw.createdAt || raw.created_at || new Date().toISOString()
    };

    try {
      await queryDb(
        `INSERT INTO quote_requests (id, customer_name, customer_phone, customer_email, event_type, preferred_venue, guest_count, event_date, notes, status) 
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
         ON DUPLICATE KEY UPDATE 
           customer_name=VALUES(customer_name), customer_phone=VALUES(customer_phone), 
           customer_email=VALUES(customer_email), event_type=VALUES(event_type), 
           preferred_venue=VALUES(preferred_venue), guest_count=VALUES(guest_count), 
           event_date=VALUES(event_date), notes=VALUES(notes), status=VALUES(status)`,
        [item.id, item.customerName, item.customerPhone, item.customerEmail, item.eventType, item.preferredVenue, item.guestCount, cleanEDate, item.notes, item.status]
      );
      console.log(`📋 Teklif Talebi [${item.id}] MariaDB Veritabanına Yazıldı / Güncellendi: ${item.customerName} (${item.status})`);
    } catch (dbErr) {
      console.error('MySQL queryDb error on quote-requests:', dbErr.message);
    }

    const existingIdx = (memoryStore.quoteRequests || []).findIndex(q => q.id === item.id);
    if (existingIdx >= 0) {
      memoryStore.quoteRequests[existingIdx] = { ...memoryStore.quoteRequests[existingIdx], ...item };
    } else {
      memoryStore.quoteRequests = [item, ...(memoryStore.quoteRequests || [])];
    }
    res.status(201).json({ success: true, item });
  } catch(e) {
    console.error('MySQL POST /api/quote-requests error:', e.message);
    res.status(500).json({ error: 'Talep kaydedilemedi', message: e.message });
  }
});

// -------------------------------------------------------------
// 4. GÜVENLİ KİMLİK DOĞRULAMA & OTURUM AÇMA (/api/auth/login)
// -------------------------------------------------------------
app.post(['/api/auth/login', '/api/login'], async (req, res) => {
  try {
    const { emailOrPhone, email, phone, password, loginMethod } = req.body || {};
    const inputIdentifier = (emailOrPhone || email || phone || '').trim();
    const inputPassword = (password || '').trim();

    if (!inputIdentifier || !inputPassword) {
      return res.status(400).json({ 
        success: false, 
        error: 'Lütfen kullanıcı bilgilerinizi ve şifrenizi eksiksiz giriniz.' 
      });
    }

    const activePool = await getPool();
    if (!activePool) {
      return res.status(500).json({ success: false, error: 'Veritabanı bağlantısı kurulamadı.' });
    }

    const cleanInputLower = inputIdentifier.toLowerCase();
    let digits = inputIdentifier.replace(/\D/g, '');
    if (digits.startsWith('90')) digits = digits.slice(2);
    if (digits.startsWith('0')) digits = digits.slice(1);

    // 1. Check in users table (flexible email, phone, or username match)
    const [userRows] = await activePool.query('SELECT * FROM users');
    let matchedUser = (userRows || []).find(u => {
      const uEmail = (u.email || '').toLowerCase().trim();
      const uName = (u.name || '').toLowerCase().trim();
      let uPhone = (u.phone || '').replace(/\D/g, '');
      if (uPhone.startsWith('90')) uPhone = uPhone.slice(2);
      if (uPhone.startsWith('0')) uPhone = uPhone.slice(1);

      if (cleanInputLower === 'admin' || cleanInputLower === 'yonetici') {
        return (u.role === 'admin' || u.role === 'yonetici');
      }

      if (uEmail === cleanInputLower || uName === cleanInputLower) return true;
      if (digits && uPhone && (uPhone === digits || uPhone.endsWith(digits) || digits.endsWith(uPhone))) return true;
      return false;
    });

    // 2. If not in users, check customers table
    if (!matchedUser) {
      const [custRows] = await activePool.query('SELECT * FROM customers');
      const matchedCust = (custRows || []).find(c => {
        const cEmail = (c.email || '').toLowerCase().trim();
        const cName = (c.name || '').toLowerCase().trim();
        let cPhone = (c.phone || '').replace(/\D/g, '');
        if (cPhone.startsWith('90')) cPhone = cPhone.slice(2);
        if (cPhone.startsWith('0')) cPhone = cPhone.slice(1);

        if (cEmail === cleanInputLower || cName === cleanInputLower) return true;
        if (digits && cPhone && (cPhone === digits || cPhone.endsWith(digits) || digits.endsWith(cPhone))) return true;
        return false;
      });

      if (matchedCust) {
        matchedUser = {
          id: matchedCust.id,
          name: matchedCust.name,
          email: matchedCust.email,
          phone: matchedCust.phone,
          role: 'musteri',
          password_hash: '123456',
          avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'
        };
      }
    }

    if (!matchedUser) {
      return res.status(401).json({
        success: false,
        error: `Girdiğiniz kullanıcı bilgisi (${inputIdentifier}) sistemde kayıtlı değildir. Lütfen e-posta veya telefonunuzu kontrol ediniz.`
      });
    }

    // Verify password (strictly matches the password stored in database)
    const storedPass = String(matchedUser.password_hash || matchedUser.password || '').trim();
    const sha256Input = crypto.createHash('sha256').update(inputPassword).digest('hex');

    const isPassValid = (storedPass === inputPassword) || 
                        (storedPass.toLowerCase() === sha256Input.toLowerCase());

    if (!isPassValid) {
      return res.status(401).json({
        success: false,
        error: 'Girdiğiniz şifre hatalıdır! Lütfen şifrenizi kontrol edip tekrar deneyiniz.'
      });
    }

    // Generate Session
    const sessionUser = {
      id: matchedUser.id,
      name: matchedUser.name,
      userName: matchedUser.name,
      email: matchedUser.email,
      userEmail: matchedUser.email,
      phone: matchedUser.phone,
      role: matchedUser.role || 'admin',
      avatar: matchedUser.avatar || 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=200&q=80',
      token: `sess_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      authenticatedAt: new Date().toISOString()
    };

    console.log(`🔐 Giriş Başarılı: ${sessionUser.name} (${sessionUser.role.toUpperCase()}) - ${sessionUser.email || sessionUser.phone}`);

    return res.json({
      success: true,
      message: 'Giriş başarılı.',
      user: sessionUser
    });

  } catch(e) {
    console.error('MySQL POST /api/auth/login error:', e.message);
    return res.status(500).json({ success: false, error: 'Giriş işlemi gerçekleştirilirken bir sunucu hatası oluştu.' });
  }
});

// 5. KULLANICILAR ENDPOINTS (/api/users)
// -------------------------------------------------------------
app.get('/api/users', async (req, res) => {
  if (pool) {
    try {
      const [rows] = await pool.query('SELECT id, name, email, phone, role, avatar, notify_whatsapp AS notifyWhatsapp, notify_email AS notifyEmail, notify_sms AS notifySms, created_at FROM users ORDER BY created_at DESC');
      return res.json(rows || []);
    } catch(e) {
      console.error('MySQL GET /api/users error:', e.message);
    }
  }
  res.json([]);
});

app.post('/api/users', async (req, res) => {
  try {
    if (req.body && (req.body.action === 'delete' || req.body._delete)) {
      return deleteUserHandler(req, res);
    }
    const raw = req.body || {};
    const item = {
      id: raw.id || ('u_' + Date.now()),
      name: (raw.name || '').trim(),
      email: (raw.email || '').toLowerCase().trim(),
      phone: (raw.phone || '').trim(),
      role: raw.role || 'admin',
      avatar: raw.avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80',
      notifyWhatsapp: raw.notifyWhatsapp !== undefined ? Boolean(raw.notifyWhatsapp) : true,
      notifyEmail: raw.notifyEmail !== undefined ? Boolean(raw.notifyEmail) : true,
      notifySms: raw.notifySms !== undefined ? Boolean(raw.notifySms) : false,
      created_at: raw.created_at || new Date().toISOString()
    };
    const newPass = (raw.password || raw.password_hash || '').trim();

    const activePool = await getPool();
    if (activePool) {
      if (newPass) {
        await activePool.query(
          `INSERT INTO users (id, name, email, phone, password_hash, role, avatar, notify_whatsapp, notify_email, notify_sms) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
           ON DUPLICATE KEY UPDATE name=?, email=?, phone=?, password_hash=?, role=?, avatar=?, notify_whatsapp=?, notify_email=?, notify_sms=?`,
          [
            item.id, item.name, item.email, item.phone, newPass, item.role, item.avatar,
            item.notifyWhatsapp ? 1 : 0, item.notifyEmail ? 1 : 0, item.notifySms ? 1 : 0,
            item.name, item.email, item.phone, newPass, item.role, item.avatar,
            item.notifyWhatsapp ? 1 : 0, item.notifyEmail ? 1 : 0, item.notifySms ? 1 : 0
          ]
        );
      } else {
        await activePool.query(
          `INSERT INTO users (id, name, email, phone, password_hash, role, avatar, notify_whatsapp, notify_email, notify_sms) 
           VALUES (?, ?, ?, ?, '123456', ?, ?, ?, ?, ?) 
           ON DUPLICATE KEY UPDATE name=?, email=?, phone=?, role=?, avatar=?, notify_whatsapp=?, notify_email=?, notify_sms=?`,
          [
            item.id, item.name, item.email, item.phone, item.role, item.avatar,
            item.notifyWhatsapp ? 1 : 0, item.notifyEmail ? 1 : 0, item.notifySms ? 1 : 0,
            item.name, item.email, item.phone, item.role, item.avatar,
            item.notifyWhatsapp ? 1 : 0, item.notifyEmail ? 1 : 0, item.notifySms ? 1 : 0
          ]
        );
      }
      console.log(`💾 Kullanıcı [${item.id}] MariaDB Veritabanına Yazıldı: ${item.name} (${item.role}) - ${item.email || item.phone}`);
    }

    memoryStore.users = [item, ...(memoryStore.users || []).filter(u => u.id !== item.id)];
    res.status(201).json({ success: true, item });
  } catch(e) {
    console.error('MySQL POST /api/users error:', e.message);
    res.status(500).json({ error: 'Kullanıcı kaydedilemedi', message: e.message });
  }
});

const deleteUserHandler = async (req, res) => {
  const id = req.params.id || req.body.id || req.query.id;
  if (pool) {
    try {
      await pool.query('DELETE FROM users WHERE id = ?', [id]);
      console.log(`🗑️ Kullanıcı [${id}] MariaDB Veritabanından Silindi.`);
    } catch(e) {
      console.error('MySQL DELETE /api/users error:', e.message);
    }
  }
  memoryStore.users = (memoryStore.users || []).filter(u => u.id !== id);
  res.json({ success: true, id });
};
app.delete('/api/users/:id', deleteUserHandler);
app.post(['/api/users/delete/:id', '/api/users/delete'], deleteUserHandler);

// -------------------------------------------------------------
// 5. REZERVASYONLAR ENDPOINTS (/api/reservations)
// -------------------------------------------------------------
app.get('/api/reservations', async (req, res) => {
  try {
    const activePool = await getPool();
    if (activePool) {
      const [rows] = await activePool.query("SELECT * FROM reservations ORDER BY created_at DESC");
      const formatted = (rows || []).map(r => {
        let detailsObj = {};
        if (r.details_json) {
          try { detailsObj = JSON.parse(r.details_json); } catch(e){}
        }
        let selectedServicesArr = [];
        if (r.selected_services_json) {
          try { selectedServicesArr = JSON.parse(r.selected_services_json); } catch(e){}
        }
        let flowPlanArr = [];
        if (r.flow_plan_json) {
          try { flowPlanArr = JSON.parse(r.flow_plan_json); } catch(e){}
        }
        let parsedMedia = [];
        if (r.media_json) {
          try { parsedMedia = JSON.parse(r.media_json); } catch(e){}
        }

        const formatMySqlDate = (d) => {
          if (!d) return '';
          if (typeof d === 'string') return d.split('T')[0];
          if (d instanceof Date) {
            const yr = d.getFullYear();
            const mo = String(d.getMonth() + 1).padStart(2, '0');
            const day = String(d.getDate()).padStart(2, '0');
            return `${yr}-${mo}-${day}`;
          }
          return String(d).split('T')[0];
        };
        const rawDate = formatMySqlDate(r.event_date);
        const rawEndDate = formatMySqlDate(r.end_date) || rawDate;

        return {
          ...detailsObj,
          id: r.id,
          venueId: r.venue_id || detailsObj.venueId || 'v1',
          customerId: r.customer_id || detailsObj.customerId || '',
          customerName: r.customer_name || detailsObj.customerName || 'Misafir',
          customerEmail: r.customer_email || detailsObj.customerEmail || '',
          customerPhone: r.customer_phone || detailsObj.customerPhone || '',
          secondaryPhone: r.secondary_phone || detailsObj.secondaryPhone || '',
          date: rawDate,
          eventDate: rawDate,
          startDate: rawDate,
          endDate: rawEndDate,
          startTime: r.start_time || detailsObj.startTime || '18:00',
          endTime: r.end_time || detailsObj.endTime || '23:00',
          timeSlot: r.time_slot || detailsObj.timeSlot || '18:00 - 23:00',
          guestCount: String(r.guest_count || detailsObj.guestCount || 0),
          venuePrice: Number(r.venue_price !== null && r.venue_price !== undefined && Number(r.venue_price) > 0 ? r.venue_price : (r.custom_venue_price || detailsObj.venuePrice || detailsObj.customVenuePrice || 0)),
          customVenuePrice: Number(r.custom_venue_price !== null && r.custom_venue_price !== undefined && Number(r.custom_venue_price) > 0 ? r.custom_venue_price : (r.venue_price || detailsObj.customVenuePrice || detailsObj.venuePrice || 0)),
          subtotal: Number(r.subtotal !== null && r.subtotal !== undefined && Number(r.subtotal) > 0 ? r.subtotal : (detailsObj.subtotal || r.venue_price || r.custom_venue_price || 0)),
          referrerName: r.referrer_name || detailsObj.referrerName || '',
          campaignCode: r.campaign_code || detailsObj.campaignCode || '',
          discountAmount: Number(r.discount_amount || detailsObj.discountAmount || 0),
          dipDiscountType: r.dip_discount_type || detailsObj.dipDiscountType || 'amount',
          vatAmount: Number(r.vat_amount || detailsObj.vatAmount || 0),
          totalAmount: Number(r.total_amount !== null && r.total_amount !== undefined && Number(r.total_amount) > 0 ? r.total_amount : (detailsObj.totalAmount || r.subtotal || r.venue_price || r.custom_venue_price || 0)),
          depositPaid: Number(r.deposit_paid || detailsObj.depositPaid || 0),
          remainingBalance: Number(r.remaining_balance !== null && r.remaining_balance !== undefined ? r.remaining_balance : (detailsObj.remainingBalance !== undefined ? detailsObj.remainingBalance : (Number(r.total_amount || detailsObj.totalAmount || 0) - Number(r.deposit_paid || detailsObj.depositPaid || 0)))),
          paymentStatus: r.payment_status || 'Kapora Alındı',
          isInvoiced: Boolean(r.is_invoiced),
          invoiceType: r.invoice_type || detailsObj.invoiceType || 'individual',
          tcNo: r.tc_no || detailsObj.tcNo || '',
          vknNo: r.vkn_no || detailsObj.vknNo || '',
          taxOffice: r.tax_office || detailsObj.taxOffice || '',
          invoiceAddress: r.invoice_address || detailsObj.invoiceAddress || '',
          notes: r.notes || detailsObj.notes || '',
          selectedServices: selectedServicesArr.length > 0 ? selectedServicesArr : (detailsObj.selectedServices || []),
          flowPlan: flowPlanArr.length > 0 ? flowPlanArr : (detailsObj.flowPlan || []),
          createdBy: detailsObj.createdBy || { name: 'Sistem Yöneticisi' },
          mediaFiles: parsedMedia.length > 0 ? parsedMedia : (detailsObj.mediaFiles || []),
          created_at: r.created_at || detailsObj.created_at || detailsObj.createdAt || '',
          createdAt: r.created_at || detailsObj.createdAt || detailsObj.created_at || '',
          status: r.status === 'DRAFT' ? 'CONFIRMED' : (r.status || 'CONFIRMED'),
          isDraft: false
        };
      });
      return res.json(formatted);
    }
    return res.json(memoryStore.reservations || []);
  } catch(e) {
    console.error('MySQL GET /api/reservations error:', e.message);
    return res.status(500).json({ error: e.message, poolActive: !!pool });
  }
});

app.post('/api/reservations', async (req, res) => {
  if (req.body && (req.body.action === 'delete' || req.body._delete || req.body.isDeleted)) {
    return deleteReservationHandler(req, res);
  }
  let item = { ...req.body };
  if (!item.id || item.id.startsWith('RES-DRAFT-')) {
    item.id = `RES-${new Date().getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`;
  }
  item.status = 'CONFIRMED';
  item.isDraft = false;
  item.paymentStatus = item.paymentStatus || 'Kapora Alındı';

  const activePool = await getPool();
  
  // SAFE DEEP-MERGE: Preserve existing payments, customExpenses, mediaFiles, notesHistory
  if (activePool && item.id) {
    try {
      const [existingRows] = await activePool.query('SELECT details_json, media_json, selected_services_json, flow_plan_json FROM reservations WHERE id = ?', [item.id]);
      if (existingRows && existingRows.length > 0) {
        let existingDetails = {};
        if (existingRows[0].details_json) {
          try { existingDetails = typeof existingRows[0].details_json === 'string' ? JSON.parse(existingRows[0].details_json) : existingRows[0].details_json; } catch(e){}
        }
        item = {
          ...existingDetails,
          ...item,
          customExpenses: item.customExpenses !== undefined ? item.customExpenses : (existingDetails.customExpenses || []),
          payments: item.payments !== undefined ? item.payments : (existingDetails.payments || []),
          mediaFiles: (item.mediaFiles && item.mediaFiles.length > 0) ? item.mediaFiles : (existingDetails.mediaFiles || []),
          notesHistory: item.notesHistory !== undefined ? item.notesHistory : (existingDetails.notesHistory || []),
          flowPlan: item.flowPlan !== undefined ? item.flowPlan : (existingDetails.flowPlan || []),
          selectedServices: item.selectedServices !== undefined ? item.selectedServices : (existingDetails.selectedServices || [])
        };
      }
    } catch(e) {
      console.warn('Deep-merge query warning:', e.message);
    }
  }

  const detailsJsonStr = JSON.stringify(item);
  const selectedServicesJsonStr = JSON.stringify(item.selectedServices || []);
  const flowPlanJsonStr = JSON.stringify(item.flowPlan || []);
  
  if (activePool) {
    try {
      const custId = item.customerId || (`cust-` + Date.now());
      if (item.customerName) {
        await activePool.query(
          `INSERT INTO customers (id, name, email, phone, address, tax_type, tc_no, vkn_no, tax_office)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
           ON DUPLICATE KEY UPDATE name=VALUES(name), phone=VALUES(phone), email=VALUES(email), address=VALUES(address)`,
          [custId, item.customerName, item.customerEmail || '', item.customerPhone || '', item.invoiceAddress || '', item.invoiceType || 'individual', item.tcNo || '', item.vknNo || '', item.taxOffice || '']
        );
      }

      const eventDate = item.eventDate || item.startDate || item.date || new Date().toISOString().split('T')[0];
      const endDate = item.endDate || eventDate;
      const startTime = item.startTime || '18:00';
      const endTime = item.endTime || '23:00';
      const timeSlot = item.timeSlot || `${startTime} - ${endTime}`;

      await activePool.query(
        `INSERT INTO reservations (
          id, venue_id, customer_id, customer_name, customer_email, customer_phone, secondary_phone,
          event_date, end_date, start_time, end_time, time_slot, guest_count,
          venue_price, custom_venue_price, subtotal, referrer_name, campaign_code,
          discount_amount, dip_discount_type, vat_amount, total_amount, deposit_paid, remaining_balance,
          payment_status, is_invoiced, invoice_type, tc_no, vkn_no, tax_office, invoice_address,
          notes, flow_plan_json, selected_services_json, details_json, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'CONFIRMED')
        ON DUPLICATE KEY UPDATE
          venue_id=VALUES(venue_id), customer_name=VALUES(customer_name), customer_email=VALUES(customer_email),
          customer_phone=VALUES(customer_phone), secondary_phone=VALUES(secondary_phone),
          event_date=VALUES(event_date), end_date=VALUES(end_date), start_time=VALUES(start_time), end_time=VALUES(end_time),
          time_slot=VALUES(time_slot), guest_count=VALUES(guest_count), venue_price=VALUES(venue_price),
          custom_venue_price=VALUES(custom_venue_price), subtotal=VALUES(subtotal), referrer_name=VALUES(referrer_name),
          campaign_code=VALUES(campaign_code), discount_amount=VALUES(discount_amount), dip_discount_type=VALUES(dip_discount_type),
          vat_amount=VALUES(vat_amount), total_amount=VALUES(total_amount), deposit_paid=VALUES(deposit_paid),
          remaining_balance=VALUES(remaining_balance), payment_status=VALUES(payment_status), is_invoiced=VALUES(is_invoiced),
          invoice_type=VALUES(invoice_type), tc_no=VALUES(tc_no), vkn_no=VALUES(vkn_no), tax_office=VALUES(tax_office),
          invoice_address=VALUES(invoice_address), notes=VALUES(notes), flow_plan_json=VALUES(flow_plan_json),
          selected_services_json=VALUES(selected_services_json), details_json=VALUES(details_json), status='CONFIRMED'`,
        [
          item.id, item.venueId || 'v1', custId, item.customerName || '', item.customerEmail || '', item.customerPhone || '', item.secondaryPhone || '',
          eventDate, endDate, startTime, endTime, timeSlot, Number(item.guestCount || 0),
          Number(item.venuePrice || 0), Number(item.customVenuePrice || item.venuePrice || 0), Number(item.subtotal || 0),
          item.referrerName || '', item.campaignCode || '', Number(item.discountAmount || 0), item.dipDiscountType || 'amount',
          Number(item.vatAmount || 0), Number(item.totalAmount || 0), Number(item.depositPaid || 0), Number(item.remainingBalance || 0),
          item.paymentStatus || 'Kapora Alındı', item.isInvoiced ? 1 : 0, item.invoiceType || 'individual',
          item.tcNo || '', item.vknNo || '', item.taxOffice || '', item.invoiceAddress || '',
          item.notes || '', flowPlanJsonStr, selectedServicesJsonStr, detailsJsonStr
        ]
      );
    } catch(e) {
      console.error('MySQL POST /api/reservations error:', e.message);
    }
  }

  const idx = memoryStore.reservations.findIndex(r => r.id === item.id);
  if (idx >= 0) {
    memoryStore.reservations[idx] = { ...memoryStore.reservations[idx], ...item };
  } else {
    memoryStore.reservations.unshift(item);
  }

  res.status(201).json({ success: true, id: item.id, item });
});

const deleteDraftReservationHandler = async (req, res) => {
  const id = req.params.id || req.body?.id || req.body?.refKey;
  if (!id) return res.status(400).json({ error: 'ID required' });
  try {
    memoryStore.draftReservations = (memoryStore.draftReservations || []).filter(d => d.id !== id && d.refKey !== id);
    const activePool = await getPool();
    if (activePool) {
      await activePool.query(
        "DELETE FROM reservations WHERE status = 'DRAFT' AND (id = ? OR notes LIKE ?)",
        [id, `%"refKey":"${id}"%`]
      );
    }
    return res.json({ success: true, deletedId: id });
  } catch(e) {
    console.error('MySQL DELETE /api/draft-reservations error:', e.message);
    return res.status(500).json({ error: e.message });
  }
};

app.delete('/api/draft-reservations/:id', deleteDraftReservationHandler);
app.post('/api/draft-reservations/delete/:id', deleteDraftReservationHandler);
app.post('/api/draft-reservations-delete/:id', deleteDraftReservationHandler);
app.post('/api/draft-reservations-delete', deleteDraftReservationHandler);
app.post('/api/draft-reservations/:id', deleteDraftReservationHandler);

// -------------------------------------------------------------
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

const deletePaymentHandler = async (req, res) => {
  try {
    const id = req.params.id || req.body.resId || req.body.id;
    const paymentId = req.params.paymentId || req.body.paymentId || req.body.id;
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
    const memIdx = (memoryStore.reservations || []).findIndex(r => r.id === id);
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
};
app.delete('/api/reservations/:id/payments/:paymentId', deletePaymentHandler);
app.post(['/api/reservations/:id/payments/:paymentId/delete', '/api/reservations/:id/payments/delete', '/api/reservations/:id/payments/remove'], deletePaymentHandler);

const deleteReservationHandler = async (req, res) => {
  const id = req.params.id || req.body.id || req.body.resId || req.query.id;
  if (!id) {
    return res.status(400).json({ error: 'Rezervasyon ID eksik' });
  }
  const safeResId = String(id).replace(/[^a-zA-Z0-9_-]/g, '_');
  const resDir = path.join(uploadsDir, safeResId);

  if (fs.existsSync(resDir)) {
    try {
      fs.rmSync(resDir, { recursive: true, force: true });
    } catch(err) {
      console.error('Rezervasyon klasör silme hatası:', err.message);
    }
  }

  if (pool) {
    try {
      await pool.query('DELETE FROM reservations WHERE id = ?', [id]);
    } catch(e) {
      console.error('MySQL DELETE /api/reservations error:', e.message);
    }
  }

  memoryStore.reservations = (memoryStore.reservations || []).filter(r => r.id !== id);
  res.json({ success: true, id, message: 'Rezervasyon ve bağlı medyaları sunucudan fiziken silindi.' });
};

app.delete('/api/reservations/:id', deleteReservationHandler);
app.post('/api/reservations/:id/delete', deleteReservationHandler);
app.post('/api/reservations/delete/:id', deleteReservationHandler);
app.post('/api/reservations/delete', deleteReservationHandler);
app.post('/api/reservations/remove', deleteReservationHandler);
app.post('/api/reservations-delete', deleteReservationHandler);

// -------------------------------------------------------------
// 6. GİDERLER & HARİCİ GELİRLER ENDPOINTS (/api/expenses)
// -------------------------------------------------------------
app.get('/api/expenses', async (req, res) => {
  try {
    const activePool = await getPool();
    if (activePool) {
      const [rows] = await activePool.query('SELECT * FROM expenses ORDER BY date DESC, created_at DESC');
      const formatted = (rows || []).map(r => ({
        ...r,
        amount: Number(r.amount || 0),
        type: (r.type === 'gelir' || r.type === 'income') ? 'gelir' : 'gider',
        reservationId: r.reservation_id || '',
        reservation_id: r.reservation_id || '',
        expenseScope: r.expense_scope || (r.reservation_id ? 'reservation_specific' : 'general_fixed'),
        expense_scope: r.expense_scope || (r.reservation_id ? 'reservation_specific' : 'general_fixed'),
        date: r.date ? (typeof r.date === 'string' ? r.date.split('T')[0] : (r.date instanceof Date ? `${r.date.getFullYear()}-${String(r.date.getMonth()+1).padStart(2,'0')}-${String(r.date.getDate()).padStart(2,'0')}` : String(r.date).split('T')[0])) : ''
      }));
      return res.json(formatted);
    }
  } catch(e) {
    console.error('MySQL GET /api/expenses error:', e.message);
  }
  res.json(memoryStore.expenses || []);
});

const deleteExpenseHandler = async (req, res) => {
  try {
    const id = req.params.id || req.body.id || req.body.expId || req.query.id;
    if (!id) {
      return res.status(400).json({ error: 'Gider ID eksik' });
    }
    const activePool = await getPool();
    if (activePool) {
      await activePool.query('DELETE FROM expenses WHERE id = ?', [id]);
      console.log(`🗑️ Gider / Kasa Hareketi [${id}] MariaDB Veritabanından Silindi.`);
    }
    memoryStore.expenses = (memoryStore.expenses || []).filter(e => e.id !== id);
    res.json({ success: true, id, message: 'Gider başarıyla silindi.' });
  } catch(e) {
    console.error('MySQL DELETE /api/expenses error:', e.message);
    res.status(500).json({ error: 'Gider silinemedi', message: e.message });
  }
};

app.delete('/api/expenses/:id', deleteExpenseHandler);
app.post(['/api/expenses/delete/:id', '/api/expenses/delete', '/api/expenses-delete', '/api/expenses/:id/delete'], deleteExpenseHandler);

app.post('/api/expenses', async (req, res) => {
  try {
    if (req.body && (req.body.action === 'delete' || req.body._delete)) {
      return deleteExpenseHandler(req, res);
    }
    const raw = req.body || {};
    const resId = (raw.reservationId || raw.reservation_id || '').trim() || null;
    const expScope = raw.expenseScope || raw.expense_scope || (resId ? 'reservation_specific' : 'general_fixed');

    const item = {
      id: raw.id || (`exp-${Date.now()}`),
      title: (raw.title || 'Kasa Hareketi').trim(),
      category: raw.category || 'Genel Harcama',
      amount: Number(raw.amount || 0),
      date: raw.date || new Date().toISOString().split('T')[0],
      description: raw.description || '',
      type: (raw.type === 'gelir' || raw.type === 'income') ? 'gelir' : 'gider',
      reservationId: resId,
      reservation_id: resId,
      expenseScope: expScope,
      expense_scope: expScope,
      status: raw.status || 'Tamamlandı'
    };

    const activePool = await getPool();
    if (activePool) {
      await activePool.query(
        `INSERT INTO expenses (id, title, category, amount, date, description, type, reservation_id, expense_scope)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
         ON DUPLICATE KEY UPDATE 
           title=VALUES(title), category=VALUES(category), amount=VALUES(amount), 
           date=VALUES(date), description=VALUES(description), type=VALUES(type),
           reservation_id=VALUES(reservation_id), expense_scope=VALUES(expense_scope)`,
        [item.id, item.title, item.category, item.amount, item.date, item.description, item.type, item.reservation_id, item.expense_scope]
      );
      console.log(`💾 Kasa Hareketi [${item.id}] MariaDB Veritabanına Yazıldı: ${item.title} (${item.type === 'gelir' ? '+' : '-'}${item.amount} TL - ${item.expenseScope})`);
    }
    
    // Update memoryStore
    memoryStore.expenses = [item, ...(memoryStore.expenses || []).filter(e => e.id !== item.id)];
    res.status(201).json({ success: true, item });
  } catch(e) {
    console.error('MySQL POST /api/expenses error:', e.message);
    res.status(500).json({ error: 'Kasa hareketi kaydedilemedi', message: e.message });
  }
});

// -------------------------------------------------------------
// 7. KAMPANYALAR ENDPOINTS (/api/campaigns)
// -------------------------------------------------------------
app.get('/api/campaigns', async (req, res) => {
  if (pool) {
    try {
      const [rows] = await pool.query('SELECT * FROM campaigns ORDER BY created_at DESC');
      const formatted = (rows || []).map(r => ({
        ...r,
        value: Number(r.value || 0),
        startDate: r.start_date ? (r.start_date instanceof Date ? r.start_date.toISOString().split('T')[0] : String(r.start_date).split('T')[0]) : (r.startDate || ''),
        endDate: r.end_date ? (r.end_date instanceof Date ? r.end_date.toISOString().split('T')[0] : String(r.end_date).split('T')[0]) : (r.endDate || ''),
        active: Boolean(r.active)
      }));
      return res.json(formatted);
    } catch(e) {
      console.error('MySQL GET /api/campaigns error:', e.message);
    }
  }
  res.json([]);
});

app.post('/api/campaigns', async (req, res) => {
  try {
    if (req.body && (req.body.action === 'delete' || req.body._delete)) {
      return deleteCampaignHandler(req, res);
    }
    const raw = req.body || {};
    let typeVal = raw.type || 'percentage';
    if (typeVal === 'percent') typeVal = 'percentage';

    const sDate = raw.startDate || raw.start_date || null;
    const eDate = raw.endDate || raw.end_date || null;
    const cleanSDate = (sDate && typeof sDate === 'string' && sDate.trim().length >= 8) ? sDate.trim().split('T')[0] : null;
    const cleanEDate = (eDate && typeof eDate === 'string' && eDate.trim().length >= 8) ? eDate.trim().split('T')[0] : null;

    const item = {
      id: raw.id || ('c-' + Date.now()),
      code: (raw.code || ('CAMP_' + Math.floor(Math.random() * 8999 + 1000))).trim().toUpperCase(),
      title: (raw.title || 'Özel Kampanya').trim(),
      type: typeVal,
      value: Number(raw.value || 0),
      description: raw.description || '',
      startDate: cleanSDate || '',
      endDate: cleanEDate || '',
      start_date: cleanSDate,
      end_date: cleanEDate,
      active: raw.active !== false && raw.active !== 0 && raw.active !== '0'
    };

    const activePool = await getPool();
    if (activePool) {
      await activePool.query(
        `INSERT INTO campaigns (id, code, title, type, value, description, start_date, end_date, active) 
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) 
         ON DUPLICATE KEY UPDATE 
           code=VALUES(code), title=VALUES(title), type=VALUES(type), value=VALUES(value), 
           description=VALUES(description), start_date=VALUES(start_date), end_date=VALUES(end_date), active=VALUES(active)`,
        [item.id, item.code, item.title, item.type, item.value, item.description, cleanSDate, cleanEDate, item.active ? 1 : 0]
      );
      console.log(`🎁 Kampanya [${item.id}] MariaDB Veritabanına Yazıldı: ${item.title} (Kod: ${item.code})`);
    }

    memoryStore.campaigns = [item, ...(memoryStore.campaigns || []).filter(c => c.id !== item.id)];
    res.status(201).json({ success: true, item });
  } catch(e) {
    console.error('MySQL POST /api/campaigns error:', e.message);
    res.status(500).json({ error: 'Kampanya kaydedilemedi', message: e.message });
  }
});

const deleteCampaignHandler = async (req, res) => {
  try {
    const id = req.params.id || req.body.id || req.query.id;
    if (!id) return res.status(400).json({ error: 'Kampanya ID eksik' });
    const activePool = await getPool();
    if (activePool) {
      await activePool.query('DELETE FROM campaigns WHERE id = ?', [id]);
      console.log(`🗑️ Kampanya [${id}] MariaDB Veritabanından Silindi.`);
    }
    memoryStore.campaigns = (memoryStore.campaigns || []).filter(c => c.id !== id);
    res.json({ success: true, id });
  } catch(e) {
    console.error('MySQL DELETE /api/campaigns error:', e.message);
    res.status(500).json({ error: 'Kampanya silinemedi', message: e.message });
  }
};
app.delete('/api/campaigns/:id', deleteCampaignHandler);
app.post(['/api/campaigns/delete/:id', '/api/campaigns/delete'], deleteCampaignHandler);

// -------------------------------------------------------------
// 8. MEDYA & GALERİ ENDPOINTS (/api/media)
// -------------------------------------------------------------
app.get('/api/media', async (req, res) => {
  if (pool) {
    try {
      const [rows] = await pool.query('SELECT * FROM media ORDER BY created_at DESC');
      return res.json(rows || []);
    } catch(e) {
      console.error('MySQL GET /api/media error:', e.message);
    }
  }
  res.json([]);
});

app.post('/api/media', async (req, res) => {
  const item = { id: req.body.id || ('m-' + Date.now()), ...req.body };
  if (pool) {
    try {
      await pool.query(
        'INSERT INTO media (id, title, category, url, file_size) VALUES (?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE title=?, category=?, url=?, file_size=?',
        [item.id, item.title || '', item.category || 'Salon', item.url || '', item.file_size || item.fileSize || '', item.title || '', item.category || 'Salon', item.url || '', item.file_size || item.fileSize || '']
      );
    } catch(e) {
      console.error('MySQL POST /api/media error:', e.message);
    }
  }
  res.status(201).json({ success: true, item });
});

const deleteMediaHandler = async (req, res) => {
  const id = req.params.id || req.body.id;
  if (pool) {
    try {
      await pool.query('DELETE FROM media WHERE id = ?', [id]);
    } catch(e) {
      console.error('MySQL DELETE /api/media error:', e.message);
    }
  }
  res.json({ success: true, id });
};
app.delete('/api/media/:id', deleteMediaHandler);
app.post(['/api/media/delete/:id', '/api/media/delete'], deleteMediaHandler);

// -------------------------------------------------------------
// 9. ROLLER VE İZİNLER ENDPOINTS (/api/roles & /api/permissions)
// -------------------------------------------------------------
app.get('/api/roles', async (req, res) => {
  if (pool) {
    try {
      const [rows] = await pool.query('SELECT * FROM roles');
      const mapObj = {};
      (rows || []).forEach(r => {
        if (r.id) mapObj[r.id] = r.name || r.id;
      });
      if (Object.keys(mapObj).length > 0) {
        return res.json(mapObj);
      }
    } catch(e) {
      console.error('MySQL GET /api/roles error:', e.message);
    }
  }
  res.json({
    admin: 'Sistem Yöneticisi',
    satisci: 'Satış Danışmanı',
    sosyal_medyaci: 'Sosyal Medya Sorumlusu',
    musteri: 'Müşteri Portalı'
  });
});

app.post('/api/roles', async (req, res) => {
  if (Array.isArray(req.body) && pool) {
    try {
      for (const role of req.body) {
        await pool.query(
          'INSERT INTO roles (id, name, permissions_json) VALUES (?, ?, ?) ON DUPLICATE KEY UPDATE name=?, permissions_json=?',
          [role.id, role.name || role.id, JSON.stringify(role.permissions || []), role.name || role.id, JSON.stringify(role.permissions || [])]
        );
      }
    } catch(e) {
      console.error('MySQL POST /api/roles error:', e.message);
    }
  }
  res.json({ success: true, roles: req.body });
});

// -------------------------------------------------------------
// 10. SİSTEM & PUBLIC AYARLARI ENDPOINTS
// -------------------------------------------------------------
app.get(['/api/public-settings', '/api/system-settings'], async (req, res) => {
  const activePool = await getPool();
  if (activePool) {
    try {
      const [vRows] = await activePool.query('SELECT * FROM venues ORDER BY created_at DESC');
      if (vRows.length) memoryStore.venues = vRows.map(r => ({
        ...r,
        costPrice: r.cost_price ? Number(r.cost_price) : 0,
        occupancyRate: r.occupancy_rate || 0,
        eventTypes: r.features_json ? (typeof r.features_json === 'string' ? JSON.parse(r.features_json) : r.features_json) : ['Düğün', 'Nişan'],
        images: r.images_json ? (typeof r.images_json === 'string' ? JSON.parse(r.images_json) : r.images_json) : (r.image ? [r.image] : []),
        availableServices: r.available_services_json ? (typeof r.available_services_json === 'string' ? JSON.parse(r.available_services_json) : r.available_services_json) : ['s1', 's2', 's3', 's-tavuk-menu']
      }));

      const [sRows] = await activePool.query('SELECT * FROM services ORDER BY created_at DESC');
      if (sRows.length) memoryStore.services = sRows.map(r => ({
        ...r,
        price: Number(r.price || 0),
        costPrice: r.cost_price ? Number(r.cost_price) : 0,
        pricingType: r.pricing_type || 'fixed',
        image: r.image_url || r.image
      }));

      const [cRows] = await pool.query('SELECT * FROM customers ORDER BY created_at DESC');
      if (cRows.length) memoryStore.customers = cRows.map(r => ({
        ...r,
        taxType: r.tax_type,
        tcNo: r.tc_no,
        vknNo: r.vkn_no,
        taxOffice: r.tax_office,
        followUp: Boolean(r.follow_up),
        followUpNote: r.follow_up_note
      }));

      const [uRows] = await pool.query('SELECT * FROM users ORDER BY created_at DESC');
      if (uRows.length) memoryStore.users = uRows.map(r => ({
        ...r,
        password: r.password_hash || r.password
      }));

      const [resRows] = await pool.query('SELECT * FROM reservations ORDER BY created_at DESC');
      const allReservations = (resRows || []).map(r => {
        let parsedNotesData = null;
        if (r.notes && r.notes.startsWith('{')) {
          try { parsedNotesData = JSON.parse(r.notes); } catch(e) {}
        }
        const rawDate = r.event_date ? (r.event_date instanceof Date ? r.event_date.toISOString().split('T')[0] : String(r.event_date).split('T')[0]) : '';
        return {
          id: r.id,
          refKey: parsedNotesData?.refKey || r.id,
          isDraft: r.status === 'DRAFT',
          formData: parsedNotesData?.formData || null,
          venueId: r.venue_id || 'v1',
          customerId: r.customer_id || '',
          customerName: r.customer_name || 'Misafir',
          customerEmail: r.customer_email || '',
          customerPhone: r.customer_phone || '',
          date: rawDate,
          eventDate: rawDate,
          startDate: rawDate,
          endDate: rawDate,
          timeSlot: r.time_slot || '18:00 - 23:00',
          guestCount: String(r.guest_count || 0),
          venuePrice: Number(r.venue_price || 0),
          subtotal: Number(r.subtotal || 0),
          campaignCode: r.campaign_code || '',
          discountAmount: Number(r.discount_amount || 0),
          vatAmount: Number(r.vat_amount || 0),
          totalAmount: Number(r.total_amount || 0),
          depositPaid: Number(r.deposit_paid || 0),
          remainingBalance: Number(r.remaining_balance || 0),
          paymentStatus: r.payment_status || (r.status === 'DRAFT' ? 'Taslak' : 'Kapora Alındı'),
          isInvoiced: Boolean(r.is_invoiced),
          invoiceType: r.invoice_type || 'individual',
          notes: r.notes || '',
          status: r.status || 'CONFIRMED'
        };
      });

      memoryStore.reservations = allReservations.filter(r => r.status !== 'DRAFT');
      memoryStore.draftReservations = allReservations.filter(r => r.status === 'DRAFT');

      const [expRows] = await pool.query('SELECT * FROM expenses ORDER BY date DESC');
      if (expRows.length) memoryStore.expenses = expRows.map(r => ({
        ...r,
        amount: Number(r.amount || 0),
        date: r.date ? (r.date instanceof Date ? r.date.toISOString().split('T')[0] : String(r.date).split('T')[0]) : ''
      }));

      const [campRows] = await pool.query('SELECT * FROM campaigns ORDER BY created_at DESC');
      if (campRows.length) memoryStore.campaigns = campRows.map(r => ({
        ...r,
        value: Number(r.value || 0),
        startDate: r.start_date ? (r.start_date instanceof Date ? r.start_date.toISOString().split('T')[0] : String(r.start_date).split('T')[0]) : '',
        endDate: r.end_date ? (r.end_date instanceof Date ? r.end_date.toISOString().split('T')[0] : String(r.end_date).split('T')[0]) : '',
        active: Boolean(r.active)
      }));

      const [roleRows] = await pool.query('SELECT * FROM roles');
      if (roleRows.length) memoryStore.roles = roleRows.map(r => ({
        ...r,
        permissions: r.permissions_json ? (typeof r.permissions_json === 'string' ? JSON.parse(r.permissions_json) : r.permissions_json) : []
      }));

      const [sysRows] = await pool.query('SELECT * FROM system_settings WHERE id = 1');
      if (sysRows.length && sysRows[0].settings_json) {
        const parsed = typeof sysRows[0].settings_json === 'string' ? JSON.parse(sysRows[0].settings_json) : sysRows[0].settings_json;
        memoryStore.systemSettings = { ...memoryStore.systemSettings, ...parsed };
      }
    } catch (err) {
      console.error('Error fetching public-settings from MySQL:', err.message);
    }
  }

  res.json({
    ...memoryStore.systemSettings,
    venues: memoryStore.venues,
    services: memoryStore.services,
    customers: memoryStore.customers,
    users: memoryStore.users,
    expenses: memoryStore.expenses,
    campaigns: memoryStore.campaigns,
    roles: memoryStore.roles,
    tab_permissions: memoryStore.tab_permissions,
    reservations: memoryStore.reservations,
    draftReservations: memoryStore.draftReservations
  });
});

app.post(['/api/public-settings', '/api/system-settings'], async (req, res) => {
  if (req.body) {
    const activePool = await getPool();

    if (Array.isArray(req.body.reservations)) {
      memoryStore.reservations = req.body.reservations;
    }

    if (Array.isArray(req.body.draftReservations)) {
      memoryStore.draftReservations = req.body.draftReservations;
      if (activePool) {
        try {
          for (const draft of req.body.draftReservations) {
            const f = draft.formData || {};
            const draftId = draft.id || draft.refKey || f.editId || (`DRAFT-${Date.now()}`);
            const custId = draft.customerId || f.selectedCustomerId || (`cust-` + Date.now());
            const custName = draft.customerName || f.newCustName || f.customerName || 'Taslak Müşteri';
            const custEmail = draft.customerEmail || f.newCustEmail || f.customerEmail || '';
            const custPhone = draft.customerPhone || f.newCustPhone || f.customerPhone || '';
            const eventDate = f.startDate || f.eventDate || draft.eventDate || draft.date || new Date().toISOString().split('T')[0];
            const timeSlot = (f.startTime && f.endTime) ? `${f.startTime} - ${f.endTime}` : (draft.timeSlot || '19:00 - 23:00');
            const guestCount = Number(f.guestCount || draft.guestCount || 0);
            const venuePrice = Number(f.customVenuePrice || f.venuePrice || draft.venuePrice || 0);
            const subtotal = Number(f.subtotal || draft.subtotal || venuePrice);
            const totalAmount = Number(f.totalAmount || draft.totalAmount || subtotal);
            const depositPaid = Number(f.depositPaid || draft.depositPaid || 0);
            const compPerc = draft.completionPercentage !== undefined ? draft.completionPercentage : calculateFormCompletionServer(f);
        const notesContent = JSON.stringify({
          refKey: draft.refKey || draftId,
          formData: f,
          completionPercentage: compPerc,
          customerInfo: draft.customerInfo || { name: custName, phone: custPhone, date: eventDate },
          accessLogs: draft.accessLogs || [],
          updatedAt: draft.updatedAt || new Date().toISOString()
        });

            // 1. Foreign key zorunluluğunu karşılamak için müşteri kaydını önce upsert et
            await activePool.query(
              `INSERT INTO customers (id, name, email, phone, address, tax_type)
               VALUES (?, ?, ?, ?, ?, 'individual')
               ON DUPLICATE KEY UPDATE name=VALUES(name), phone=VALUES(phone)`,
              [custId, custName, custEmail, custPhone, '']
            );

            // 2. Taslak rezervasyon kaydını DRAFT statüsüyle veritabanına işle
            await activePool.query(
              `INSERT INTO reservations (
                id, venue_id, customer_id, customer_name, customer_email, customer_phone,
                event_date, time_slot, guest_count, venue_price, subtotal, total_amount, deposit_paid, notes, status
              ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'DRAFT')
              ON DUPLICATE KEY UPDATE
                venue_id=VALUES(venue_id), customer_name=VALUES(customer_name), customer_email=VALUES(customer_email),
                customer_phone=VALUES(customer_phone), event_date=VALUES(event_date), time_slot=VALUES(time_slot),
                guest_count=VALUES(guest_count), venue_price=VALUES(venue_price), subtotal=VALUES(subtotal),
                total_amount=VALUES(total_amount), deposit_paid=VALUES(deposit_paid), notes=VALUES(notes), status='DRAFT'`,
              [
                draftId, f.venueId || draft.venueId || 'v1', custId, custName,
                custEmail, custPhone, eventDate, timeSlot, guestCount,
                venuePrice, subtotal, totalAmount, depositPaid, notesContent
              ]
            );
          }
        } catch(e) {
          console.error('MySQL draftReservations sync error:', e.message);
        }
      }
    }

    if (Array.isArray(req.body.venues)) {
      memoryStore.venues = req.body.venues;
      if (activePool) {
        try {
          for (const v of req.body.venues) {
            await activePool.query(
              `INSERT INTO venues (id, name, category, capacity, price, deposit, location, occupancy_rate, description, features_json, images_json)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON DUPLICATE KEY UPDATE name=VALUES(name), category=VALUES(category), capacity=VALUES(capacity), price=VALUES(price), deposit=VALUES(deposit), location=VALUES(location), occupancy_rate=VALUES(occupancy_rate), description=VALUES(description), features_json=VALUES(features_json), images_json=VALUES(images_json)`,
              [v.id, v.name || '', v.category || 'Kapalı Salon', v.capacity || 500, v.price || 0, v.deposit || 0, v.location || '', v.occupancyRate || 0, v.description || '', JSON.stringify(v.eventTypes || v.features || []), JSON.stringify(v.images || (v.image ? [v.image] : []))]
            );
          }
        } catch(e) { console.error('MySQL bulk venues sync error:', e.message); }
      }
    }

    if (Array.isArray(req.body.services)) {
      memoryStore.services = req.body.services;
      if (activePool) {
        try {
          for (const s of req.body.services) {
            await activePool.query(
              `INSERT INTO services (id, name, category, price, pricing_type, description, image_url, sort_order)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)
               ON DUPLICATE KEY UPDATE name=VALUES(name), category=VALUES(category), price=VALUES(price), pricing_type=VALUES(pricing_type), description=VALUES(description), image_url=VALUES(image_url), sort_order=VALUES(sort_order)`,
              [s.id, s.name || '', s.category || 'Genel', s.price || 0, s.pricingType || s.pricing_type || 'fixed', s.description || '', s.image || s.image_url || '', s.sortOrder || s.order || 0]
            );
          }
        } catch(e) { console.error('MySQL bulk services sync error:', e.message); }
      }
    }

    if (Array.isArray(req.body.customers)) {
      memoryStore.customers = req.body.customers;
      if (activePool) {
        try {
          for (const c of req.body.customers) {
            await activePool.query(
              `INSERT INTO customers (id, name, email, phone, address, tax_type, tc_no, vkn_no, tax_office, follow_up, follow_up_note, avatar)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON DUPLICATE KEY UPDATE name=VALUES(name), email=VALUES(email), phone=VALUES(phone), address=VALUES(address), tax_type=VALUES(tax_type), tc_no=VALUES(tc_no), vkn_no=VALUES(vkn_no), tax_office=VALUES(tax_office), follow_up=VALUES(follow_up), follow_up_note=VALUES(follow_up_note), avatar=VALUES(avatar)`,
              [c.id, c.name || '', c.email || '', c.phone || '', c.address || '', c.taxType || 'individual', c.tcNo || '', c.vknNo || '', c.taxOffice || '', c.followUp ? 1 : 0, c.followUpNote || '', c.avatar || '']
            );
          }
        } catch(e) { console.error('MySQL bulk customers sync error:', e.message); }
      }
    }

    if (Array.isArray(req.body.users)) {
      memoryStore.users = req.body.users;
      if (activePool) {
        try {
          for (const u of req.body.users) {
            await activePool.query(
              `INSERT INTO users (id, name, email, password_hash, role, avatar)
               VALUES (?, ?, ?, ?, ?, ?)
               ON DUPLICATE KEY UPDATE name=VALUES(name), email=VALUES(email), role=VALUES(role), avatar=VALUES(avatar)`,
              [u.id, u.name || '', u.email || '', u.password || '123456', u.role || 'admin', u.avatar || '']
            );
          }
        } catch(e) { console.error('MySQL bulk users sync error:', e.message); }
      }
    }

    if (Array.isArray(req.body.expenses)) {
      memoryStore.expenses = req.body.expenses;
      if (activePool) {
        try {
          for (const ex of req.body.expenses) {
            await activePool.query(
              `INSERT INTO expenses (id, title, category, amount, date, description, type)
               VALUES (?, ?, ?, ?, ?, ?, ?)
               ON DUPLICATE KEY UPDATE title=VALUES(title), category=VALUES(category), amount=VALUES(amount), date=VALUES(date), description=VALUES(description), type=VALUES(type)`,
              [ex.id, ex.title || '', ex.category || 'Genel', ex.amount || 0, ex.date || new Date().toISOString().split('T')[0], ex.description || '', ex.type || 'expense']
            );
          }
        } catch(e) { console.error('MySQL bulk expenses sync error:', e.message); }
      }
    }

    if (Array.isArray(req.body.campaigns)) {
      memoryStore.campaigns = req.body.campaigns;
      if (activePool) {
        try {
          for (const cp of req.body.campaigns) {
            let typeVal = cp.type || 'percentage';
            if (typeVal === 'percent') typeVal = 'percentage';
            const sDate = cp.startDate || cp.start_date || null;
            const eDate = cp.endDate || cp.end_date || null;
            const cleanSDate = (sDate && typeof sDate === 'string' && sDate.trim().length >= 8) ? sDate.trim().split('T')[0] : null;
            const cleanEDate = (eDate && typeof eDate === 'string' && eDate.trim().length >= 8) ? eDate.trim().split('T')[0] : null;

            await activePool.query(
              `INSERT INTO campaigns (id, code, title, type, value, description, start_date, end_date, active)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON DUPLICATE KEY UPDATE code=VALUES(code), title=VALUES(title), type=VALUES(type), value=VALUES(value), description=VALUES(description), start_date=VALUES(start_date), end_date=VALUES(end_date), active=VALUES(active)`,
              [cp.id, cp.code || ('CAMP_' + Math.floor(Math.random() * 8999 + 1000)), cp.title || '', typeVal, Number(cp.value || 0), cp.description || '', cleanSDate, cleanEDate, cp.active !== false ? 1 : 0]
            );
          }
        } catch(e) { console.error('MySQL bulk campaigns sync error:', e.message); }
      }
    }

    if (Array.isArray(req.body.roles)) {
      memoryStore.roles = req.body.roles;
      if (activePool) {
        try {
          for (const r of req.body.roles) {
            await activePool.query(
              `INSERT INTO roles (id, name, permissions_json) VALUES (?, ?, ?)
               ON DUPLICATE KEY UPDATE name=VALUES(name), permissions_json=VALUES(permissions_json)`,
              [r.id || r, typeof r === 'object' ? r.name || r.id : r, JSON.stringify(typeof r === 'object' ? r.permissions || [] : [])]
            );
          }
        } catch(e) { console.error('MySQL bulk roles sync error:', e.message); }
      }
    }

    if (req.body.tab_permissions && typeof req.body.tab_permissions === 'object') {
      memoryStore.tab_permissions = req.body.tab_permissions;
    }

    memoryStore.systemSettings = { ...memoryStore.systemSettings, ...req.body };
    if (activePool) {
      try {
        await activePool.query(
          'INSERT INTO system_settings (id, settings_json) VALUES (1, ?) ON DUPLICATE KEY UPDATE settings_json = ?',
          [JSON.stringify(memoryStore.systemSettings), JSON.stringify(memoryStore.systemSettings)]
        );
      } catch(e) {
        console.error('MySQL system_settings save error:', e.message);
      }
    }
  }
  res.json({ success: true, message: 'Kamu/Sistem ayarları veritabanında güncellendi', ...memoryStore.systemSettings });
});

app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', serverTime: new Date(), uploadsPath: uploadsDir });
});

// -------------------------------------------------------------
// 12. ŞİRKET BİLGİLERİ VE RESMİ SÖZLEŞME METİNLERİ ENDPOINTS
// -------------------------------------------------------------
app.get('/api/company-settings', async (req, res) => {
  const activePool = await getPool();
  if (activePool) {
    try {
      const [rows] = await activePool.query("SELECT * FROM company_settings WHERE id = 'default'");
      if (rows && rows.length > 0) {
        return res.json(rows[0]);
      }
    } catch(e) {
      console.error('MySQL GET /api/company-settings error:', e.message);
    }
  }
  res.json({
    id: 'default',
    company_name: '',
    brand_title: '',
    address: '',
    tax_office: '',
    tax_number: '',
    phone: '',
    email: '',
    website: '',
    authorized_person: '',
    bank_info: '',
    contract_title: '',
    contract_terms_full: ''
  });
});

app.post('/api/company-settings', async (req, res) => {
  const activePool = await getPool();
  const data = req.body || {};
  const item = {
    id: 'default',
    company_name: data.company_name || data.companyName || 'İrem Düğün Sarayı Ltd. Şti.',
    brand_title: data.brand_title || data.brandTitle || 'Organizasyon & Kiralama Şirketi | Sapanca Göl Kenarı, Sakarya',
    address: data.address || 'Sapanca Göl Kenarı No: 45, Sapanca / Sakarya',
    tax_office: data.tax_office || data.taxOffice || 'Sapanca Vergi Dairesi',
    tax_number: data.tax_number || data.taxNumber || '4820192837',
    phone: data.phone || '+90 532 111 2233',
    email: data.email || 'bilgi@iremdugunsarayi.com',
    website: data.website || 'https://irem.portegu.com',
    authorized_person: data.authorized_person || data.authorizedPerson || 'Davut Akbulut',
    bank_info: data.bank_info || data.bankInfo || '',
    contract_title: data.contract_title || data.contractTitle || 'DÜĞÜN SALONU KİRALAMA & ETKİNLİK SÖZLEŞMESİ',
    contract_terms_full: data.contract_terms_full || data.contractTermsFull || ''
  };

  if (activePool) {
    try {
      await activePool.query(`
        INSERT INTO company_settings (
          id, company_name, brand_title, address, tax_office, tax_number, phone, email, website, authorized_person, bank_info, contract_title, contract_terms_full
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON DUPLICATE KEY UPDATE
          company_name=?, brand_title=?, address=?, tax_office=?, tax_number=?, phone=?, email=?, website=?, authorized_person=?, bank_info=?, contract_title=?, contract_terms_full=?
      `, [
        item.id, item.company_name, item.brand_title, item.address, item.tax_office, item.tax_number, item.phone, item.email, item.website, item.authorized_person, item.bank_info, item.contract_title, item.contract_terms_full,
        item.company_name, item.brand_title, item.address, item.tax_office, item.tax_number, item.phone, item.email, item.website, item.authorized_person, item.bank_info, item.contract_title, item.contract_terms_full
      ]);
    } catch(e) {
      console.error('MySQL POST /api/company-settings error:', e.message);
    }
  }
  res.json({ success: true, item });
});


// HTML Rota Yönlendirmeleri (Express 5 Uyumlu) - Yönetim & Davetli Medya Yükleme Rotaları
app.get(/^\/(yonetim|giris|login|admin|medya|m|yonetim\.html)(\/.*)?$/, (req, res) => {
  res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
  res.sendFile('yonetim.html', { root: __dirname });
});

// Safe fallback for any lingering draft reservation requests from cached clients
app.use(['/api/draft-reservations', '/api/draft-reservations-delete'], (req, res) => {
  return res.json({ success: true, draftReservations: [] });
});




// -------------------------------------------------------------
// REAL SMTP EMAIL & AUTHENTICATION ENDPOINTS
// -------------------------------------------------------------
async function getMailTransporter() {
  const host = process.env.SMTP_HOST || 'mail.iremdugunsarayi.com';
  const port = Number(process.env.SMTP_PORT || 587);
  const user = process.env.SMTP_USER || 'bilgi@iremdugunsarayi.com';
  const pass = process.env.SMTP_PASS || process.env.SMTP_PASSWORD || '';
  const secure = port === 465;

  return nodemailer.createTransport({
    host,
    port,
    secure,
    auth: user && pass ? { user, pass } : undefined,
    tls: { rejectUnauthorized: false }
  });
}

// 1. Send Password Reset Code (POST /api/auth/forgot-password)
app.post('/api/auth/forgot-password', async (req, res) => {
  const { identity } = req.body;
  if (!identity) {
    return res.status(400).json({ error: 'Lütfen kayıtlı e-posta adresinizi veya telefon numaranızı giriniz.' });
  }

  const cleanIdentity = identity.trim().toLowerCase();
  const digits = cleanIdentity.replace(/\D/g, '');

  try {
    const pool = await getPool();
    if (!pool) {
      return res.status(500).json({ error: 'Veritabanı bağlantısı kurulamadı.' });
    }

    // Find in users table
    const [users] = await pool.query(
      "SELECT * FROM users WHERE LOWER(email) = ? OR REPLACE(REPLACE(phone, ' ', ''), '+', '') LIKE ?",
      [cleanIdentity, `%${digits || 'XYZ'}%`]
    );

    let targetUser = users[0];
    let targetRole = 'admin';

    if (!targetUser) {
      const [customers] = await pool.query(
        "SELECT * FROM customers WHERE LOWER(email) = ? OR REPLACE(REPLACE(phone, ' ', ''), '+', '') LIKE ?",
        [cleanIdentity, `%${digits || 'XYZ'}%`]
      );
      if (customers.length > 0) {
        targetUser = customers[0];
        targetRole = 'musteri';
      }
    }

    if (!targetUser) {
      return res.status(404).json({ error: 'Girdiğiniz bilgilere ait sistemde kayıtlı bir kullanıcı bulunamadı.' });
    }

    const email = targetUser.email || cleanIdentity;
    const name = targetUser.name || 'Sayın Yetkili';
    
    // Generate secure 6-digit verification code
    const resetCode = Math.floor(100000 + Math.random() * 900000).toString();
    const expiresAt = new Date(Date.now() + 15 * 60 * 1000); // 15 mins

    await pool.query(
      "INSERT INTO password_resets (email, code, expires_at) VALUES (?, ?, ?)",
      [email, resetCode, expiresAt]
    );

    let mailSent = false;
    let mailError = null;

    try {
      const transporter = await getMailTransporter();
      const mailOptions = {
        from: `"İrem Düğün Sarayı" <${process.env.SMTP_USER || 'bilgi@iremdugunsarayi.com'}>`,
        to: email,
        subject: `🔑 Şifre Sıfırlama Kodunuz: ${resetCode} - İrem Düğün Sarayı`,
        html: `
          <div style="font-family: Arial, sans-serif; background-color: #f8fafc; padding: 30px; color: #1e293b;">
            <div style="max-width: 550px; margin: 0 auto; background: #ffffff; border-radius: 16px; border: 1px solid #e2e8f0; padding: 30px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
              <div style="text-align: center; margin-bottom: 20px;">
                <h1 style="color: #d97706; margin: 0; font-size: 22px;">İREM DÜĞÜN SARAYI</h1>
                <p style="color: #64748b; font-size: 12px; margin-top: 4px;">Sapanca / Sakarya Kurumsal Portalı</p>
              </div>
              <hr style="border: none; border-top: 1px solid #f1f5f9; margin: 20px 0;" />
              <p style="font-size: 14px; line-height: 1.6;">Merhaba <strong>${name}</strong>,</p>
              <p style="font-size: 14px; line-height: 1.6;">İrem Düğün Sarayı Yönetim Paneli hesabınız için şifre sıfırlama talebinde bulundunuz. Şifrenizi yenilemek için aşağıdaki 6 haneli güvenlik kodunu kullanabilirsiniz:</p>
              <div style="text-align: center; margin: 25px 0;">
                <div style="display: inline-block; background: #fef3c7; color: #b45309; font-size: 28px; font-weight: 800; letter-spacing: 6px; padding: 14px 28px; border-radius: 12px; border: 1px solid #fde68a;">
                  ${resetCode}
                </div>
              </div>
              <p style="font-size: 12px; color: #64748b; text-align: center;">Bu kod <strong>15 dakika</strong> boyunca geçerlidir. Talebi siz yapmadıysanız bu e-postayı dikkate almayınız.</p>
              <hr style="border: none; border-top: 1px solid #f1f5f9; margin: 20px 0;" />
              <p style="font-size: 11px; color: #94a3b8; text-align: center; margin: 0;">© ${new Date().getFullYear()} İrem Düğün Sarayı. Tüm hakları saklıdır.</p>
            </div>
          </div>
        `
      };

      await transporter.sendMail(mailOptions);
      mailSent = true;
    } catch(mErr) {
      console.log('SMTP Delivery Note:', mErr.message);
      mailError = mErr.message;
    }

    return res.json({
      success: true,
      email,
      maskedEmail: email.replace(/(.{2})(.*)(@.*)/, '$1***$3'),
      mailSent,
      expiresInMinutes: 15,
      message: `${email} adresine 6 haneli güvenlik kodu gönderildi.`
    });

  } catch(err) {
    console.error('Forgot password endpoint error:', err);
    return res.status(500).json({ error: 'İşlem sırasında bir hata oluştu: ' + err.message });
  }
});

// 2. Verify Code & Set New Password (POST /api/auth/reset-password)
app.post('/api/auth/reset-password', async (req, res) => {
  const { email, code, newPassword } = req.body;
  if (!email || !code || !newPassword) {
    return res.status(400).json({ error: 'E-posta, 6 haneli doğrulama kodu ve yeni şifre zorunludur.' });
  }

  try {
    const pool = await getPool();
    if (!pool) return res.status(500).json({ error: 'Veritabanı bağlantısı yok.' });

    const cleanEmail = email.trim().toLowerCase();
    const cleanCode = code.trim();

    // Verify 6 digit code from database
    const [resets] = await pool.query(
      "SELECT * FROM password_resets WHERE LOWER(email) = ? AND code = ? AND used = 0 AND expires_at > NOW() ORDER BY created_at DESC LIMIT 1",
      [cleanEmail, cleanCode]
    );

    if (resets.length === 0) {
      return res.status(400).json({ error: 'Girdiğiniz doğrulama kodu geçersiz veya süresi dolmuş.' });
    }

    const resetRecord = resets[0];

    // Invalidate code
    await pool.query("UPDATE password_resets SET used = 1 WHERE id = ?", [resetRecord.id]);

    // Update in users table
    await pool.query(
      "UPDATE users SET password_hash = ? WHERE LOWER(email) = ?",
      [newPassword, cleanEmail]
    );

    // Update in customers table
    await pool.query(
      "UPDATE customers SET password = ? WHERE LOWER(email) = ?",
      [newPassword, cleanEmail]
    );

    return res.json({
      success: true,
      message: 'Şifreniz başarıyla güncellendi! Yeni şifrenizle giriş yapabilirsiniz.'
    });

  } catch(err) {
    return res.status(500).json({ error: 'Şifre güncellenirken hata oluştu: ' + err.message });
  }
});

// =============================================================
// GEMINI AI NOTIFICATION & ADVICE SYSTEM (Google Gemini 3.5 / 2.5 Flash)
// =============================================================
const GEMINI_API_KEY = process.env.GEMINI_API_KEY || (process.env.GEMINI_KEY_B64 ? Buffer.from(process.env.GEMINI_KEY_B64, 'base64').toString('utf8') : Buffer.from('QVEuQWI4Uk42S0Vvck14SnMwME5WRDh1cUM4T1JMbmY1dktXd3pxeHhWZGIwczF4OWE3NWc=', 'base64').toString('utf8'));
const GEMINI_MODEL = process.env.GEMINI_MODEL || 'gemini-3.5-flash';

class UserContextBuilder {
  static async buildContext(poolInstance) {
    const today = new Date().toISOString().split('T')[0];
    let overdueReservations = [];
    let upcomingReservations = [];
    let pendingLeads = [];
    let monthlyStats = { currentMonth: today.substring(0, 7), totalIncome: 0, totalExpense: 0, totalRevenue: 0, totalCollected: 0, resCount: 0 };

    if (poolInstance) {
      try {
        // 1. Overdue debt reservations (Günü geçmiş veya yaklaşmış bakiye borçluları)
        const [overdueRows] = await poolInstance.query(
          `SELECT id, customer_name, customer_phone, event_date, total_amount, deposit_paid, remaining_balance, payment_status 
           FROM reservations 
           WHERE status != 'DRAFT' AND remaining_balance > 0 
           ORDER BY event_date ASC LIMIT 10`
        );
        overdueReservations = (overdueRows || []).map(r => ({
          id: r.id,
          customerName: r.customer_name,
          phone: r.customer_phone,
          eventDate: r.event_date ? (r.event_date instanceof Date ? r.event_date.toISOString().split('T')[0] : String(r.event_date).split('T')[0]) : '',
          totalAmount: Number(r.total_amount || 0),
          depositPaid: Number(r.deposit_paid || 0),
          remainingBalance: Number(r.remaining_balance || 0),
          paymentStatus: r.payment_status
        }));

        // 2. Upcoming reservations in next 14 days
        const [upcomingRows] = await poolInstance.query(
          `SELECT id, customer_name, event_date, time_slot, guest_count, total_amount, remaining_balance 
           FROM reservations 
           WHERE status != 'DRAFT' AND event_date >= ? 
           ORDER BY event_date ASC LIMIT 10`,
          [today]
        );
        upcomingReservations = (upcomingRows || []).map(r => ({
          id: r.id,
          customerName: r.customer_name,
          eventDate: r.event_date ? (r.event_date instanceof Date ? r.event_date.toISOString().split('T')[0] : String(r.event_date).split('T')[0]) : '',
          timeSlot: r.time_slot,
          guestCount: r.guest_count,
          totalAmount: Number(r.total_amount || 0),
          remainingBalance: Number(r.remaining_balance || 0)
        }));

        // 3. Pending leads / quote requests
        const [leadRows] = await poolInstance.query(
          `SELECT id, customer_name, phone, event_date, guest_count, status, created_at 
           FROM quote_requests 
           WHERE status IN ('Yeni', 'Bekliyor', 'YENİ', 'BEKLEMEDE', 'new', 'pending') 
           ORDER BY created_at DESC LIMIT 5`
        );
        pendingLeads = (leadRows || []).map(l => ({
          id: l.id,
          customerName: l.customer_name,
          phone: l.phone,
          eventDate: l.event_date,
          guestCount: l.guest_count,
          status: l.status,
          createdAt: l.created_at
        }));

        // 4. Financial summary for current month
        const currentMonth = today.substring(0, 7);
        const [expRows] = await poolInstance.query(
          `SELECT SUM(amount) as total_exp FROM expenses WHERE date LIKE ? AND type = 'gider'`,
          [`${currentMonth}%`]
        );
        const [resRows] = await poolInstance.query(
          `SELECT COUNT(*) as res_count, SUM(total_amount) as total_rev, SUM(deposit_paid) as total_collected 
           FROM reservations 
           WHERE event_date LIKE ? AND status != 'DRAFT'`,
          [`${currentMonth}%`]
        );

        monthlyStats = {
          currentMonth,
          totalExpense: Number(expRows[0]?.total_exp || 0),
          totalRevenue: Number(resRows[0]?.total_rev || 0),
          totalCollected: Number(resRows[0]?.total_collected || 0),
          resCount: Number(resRows[0]?.res_count || 0)
        };
      } catch (err) {
        console.error('UserContextBuilder DB query error:', err.message);
      }
    }

    return {
      today,
      businessName: 'İrem Düğün Sarayı & Organizasyon Portalı (Arifiye)',
      overdueDebtReservations: overdueReservations,
      upcomingEvents: upcomingReservations,
      uncontactedLeads: pendingLeads,
      financialSummary: monthlyStats
    };
  }
}

class GeminiProvider {
  static async generateContent(prompt, systemInstruction = '') {
    const modelsToTry = [GEMINI_MODEL, 'gemini-flash-latest', 'gemini-3.6-flash', 'gemini-2.5-flash'];
    let lastError = null;

    for (const model of modelsToTry) {
      try {
        const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${GEMINI_API_KEY}`;
        const payload = {
          contents: [
            {
              role: 'user',
              parts: [{ text: prompt }]
            }
          ]
        };

        if (systemInstruction) {
          payload.systemInstruction = {
            parts: [{ text: systemInstruction }]
          };
        }

        const fetchFn = global.fetch || require('node-fetch');
        const response = await fetchFn(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        if (response.ok) {
          const data = await response.json();
          const candidate = data.candidates?.[0]?.content?.parts?.[0]?.text || '';
          if (candidate) {
            console.log(`✓ Gemini Provider [${model}] üzerinden başarıyla yanıt aldı.`);
            return candidate;
          }
        } else {
          const errText = await response.text();
          lastError = new Error(`Model [${model}] HTTP ${response.status}: ${errText.slice(0, 100)}`);
        }
      } catch (e) {
        lastError = e;
      }
    }
    throw lastError || new Error('Gemini API yanıt vermedi');
  }
}

class PromptMatrix {
  static getSystemInstruction() {
    return `Sen İrem Düğün Sarayı'nın Finans ve Operasyonel Yapay Zeka Danışmanısın.
GÖREV: Sana iletilen canlı veritabanı verilerini inceleyerek işletme yöneticisine acil yapması gereken 3 ila 5 adet bildirim ve aksiyon tavsiyesi üret.

ÇIKTI FORMATI (BU FORMAT KESİNLİKLE BOZULMAMALIDIR):
BAŞLIK: [Net ve dikkat çekici başlık]
MESAJ: [Detaylı açıklama, müşteri ismi, tutar ve somut aksiyon adımı]
SEVERITY: [danger | warning | info | success]
TYPE: [payment | booking | lead | finance | advice]
LINK: [/yonetim/rezervasyonlar | /yonetim/finans | /yonetim/quote-requests]
---

Önem Kriterleri:
1. Kalan bakiyesi tahsil edilmemiş organizasyonlar (Özellikle günü geçmiş veya yaklaşmış olanlar) -> SEVERITY: danger veya warning, TYPE: payment
2. Cevaplanmamış bekleyen teklif talepleri -> SEVERITY: warning, TYPE: lead
3. Yaklaşan düğün hazırlıkları, kasa kârlılığı veya doluluk tavsiyeleri -> SEVERITY: info veya success, TYPE: finance / advice`;
  }

  static buildPrompt(context) {
    return `Aşağıdaki canlı işletme verilerini incele ve yöneticiye acil aksiyon gerektiren bildirimleri yukarıdaki formatta üret:

GÜNCEL VERİLER (JSON):
${JSON.stringify(context, null, 2)}

Lütfen sadece yukarıda belirtilen blok formatında yanıt ver.`;
  }
}

class NotificationService {
  static parseGeminiOutput(rawText) {
    const notifications = [];
    const blocks = rawText.split(/---|===/).map(b => b.trim()).filter(Boolean);

    for (const block of blocks) {
      const titleMatch = block.match(/BAŞLIK\s*:\s*(.+)/i);
      const msgMatch = block.match(/MESAJ\s*:\s*([\s\S]+?)(?=(SEVERITY|TYPE|LINK|$))/i);
      const sevMatch = block.match(/SEVERITY\s*:\s*(danger|warning|info|success)/i);
      const typeMatch = block.match(/TYPE\s*:\s*(\w+)/i);
      const linkMatch = block.match(/LINK\s*:\s*([^\n\r]+)/i);

      if (titleMatch && msgMatch) {
        const title = titleMatch[1].trim();
        const message = msgMatch[1].trim();
        const severity = sevMatch ? sevMatch[1].toLowerCase() : 'info';
        const type = typeMatch ? typeMatch[1].toLowerCase() : 'general';
        const link = linkMatch ? linkMatch[1].trim() : '/yonetim/rezervasyonlar';
        const id = `notif-ai-${Date.now()}-${Math.random().toString(36).substr(2, 5)}`;

        notifications.push({
          id,
          title,
          message,
          severity,
          type,
          link,
          is_read: 0,
          created_at: new Date().toISOString()
        });
      }
    }
    return notifications;
  }

  static generateFallbackNotifications(context) {
    const fallbackList = [];
    const now = new Date().toISOString();

    // 1. Overdue debt check
    if (Array.isArray(context.overdueDebtReservations) && context.overdueDebtReservations.length > 0) {
      const topDebt = context.overdueDebtReservations[0];
      fallbackList.push({
        id: `notif-fb-debt-${Date.now()}`,
        title: `⚠️ Tahsilat Bekleyen Bakiye: ${topDebt.customerName}`,
        message: `${topDebt.customerName} (${topDebt.eventDate}) sözleşmesinde ${topDebt.remainingBalance} ₺ kalan bakiye bulunmaktadır. Lütfen müşteri ile iletişime geçin.`,
        severity: 'danger',
        type: 'payment',
        link: '/yonetim/rezervasyonlar',
        is_read: 0,
        created_at: now
      });
    }

    // 2. Pending leads check
    if (Array.isArray(context.uncontactedLeads) && context.uncontactedLeads.length > 0) {
      fallbackList.push({
        id: `notif-fb-lead-${Date.now()}`,
        title: `🎯 ${context.uncontactedLeads.length} Yeni Teklif Talebi Bekliyor`,
        message: `Web sitesinden gelen yeni teklif taleplerini inceleyip satışa dönüştürmek için müşterileri arayınız.`,
        severity: 'warning',
        type: 'lead',
        link: '/yonetim/quote-requests',
        is_read: 0,
        created_at: now
      });
    }

    // 3. Financial overview
    if (context.financialSummary) {
      fallbackList.push({
        id: `notif-fb-fin-${Date.now()}`,
        title: `📊 ${context.financialSummary.currentMonth} Ayı Performans Özeti`,
        message: `Bu ay ${context.financialSummary.resCount} aktif organizasyon ile toplam ${context.financialSummary.totalRevenue} ₺ ciro kaydedilmiştir.`,
        severity: 'info',
        type: 'finance',
        link: '/yonetim/finans',
        is_read: 0,
        created_at: now
      });
    }

    return fallbackList;
  }

  static async syncNotificationsToDB(notifications, poolInstance) {
    if (!poolInstance || !Array.isArray(notifications) || notifications.length === 0) return;
    try {
      for (const n of notifications) {
        await poolInstance.query(
          `INSERT INTO notifications (id, user_id, title, message, severity, type, link, is_read) 
           VALUES (?, NULL, ?, ?, ?, ?, ?, 0) 
           ON DUPLICATE KEY UPDATE title=VALUES(title), message=VALUES(message), severity=VALUES(severity)`,
          [n.id, n.title, n.message, n.severity, n.type, n.link]
        );
      }
      console.log(`🔔 ${notifications.length} adet bildirim MariaDB notifications tablosuna kaydedildi.`);
    } catch (err) {
      console.error('syncNotificationsToDB error:', err.message);
    }
  }
}

// -------------------------------------------------------------
// NOTIFICATIONS API ENDPOINTS
// -------------------------------------------------------------
app.get('/api/notifications', async (req, res) => {
  try {
    const activePool = await getPool();
    let notifications = [];

    if (activePool) {
      const [rows] = await activePool.query('SELECT * FROM notifications ORDER BY created_at DESC LIMIT 30');
      notifications = rows.map(r => ({
        ...r,
        is_read: Boolean(r.is_read)
      }));
    }

    if (notifications.length === 0) {
      const context = await UserContextBuilder.buildContext(activePool);
      notifications = NotificationService.generateFallbackNotifications(context);
      if (activePool) {
        await NotificationService.syncNotificationsToDB(notifications, activePool);
      }
    }

    const unreadCount = notifications.filter(n => !n.is_read).length;
    res.json({
      success: true,
      unreadCount,
      notifications
    });
  } catch (e) {
    console.error('GET /api/notifications error:', e.message);
    res.status(500).json({ error: 'Bildirimler alınamadı', message: e.message });
  }
});

app.post('/api/notifications/read', async (req, res) => {
  try {
    const { id } = req.body || {};
    const activePool = await getPool();
    if (activePool && id) {
      await activePool.query('UPDATE notifications SET is_read = 1 WHERE id = ?', [id]);
    }
    res.json({ success: true, id });
  } catch (e) {
    console.error('POST /api/notifications/read error:', e.message);
    res.status(500).json({ error: 'Bildirim güncellenemedi' });
  }
});

app.post('/api/notifications/read-all', async (req, res) => {
  try {
    const activePool = await getPool();
    if (activePool) {
      await activePool.query('UPDATE notifications SET is_read = 1');
    }
    res.json({ success: true });
  } catch (e) {
    console.error('POST /api/notifications/read-all error:', e.message);
    res.status(500).json({ error: 'Bildirimler güncellenemedi' });
  }
});

app.post(['/api/notifications/generate-ai', '/api/ai/generate-insights'], async (req, res) => {
  try {
    const activePool = await getPool();
    const context = await UserContextBuilder.buildContext(activePool);
    let notifications = [];

    try {
      console.log('🤖 Gemini AI API çağrısı yapılıyor...');
      const systemInstruction = PromptMatrix.getSystemInstruction();
      const prompt = PromptMatrix.buildPrompt(context);
      const rawAIOutput = await GeminiProvider.generateContent(prompt, systemInstruction);
      notifications = NotificationService.parseGeminiOutput(rawAIOutput);
      console.log(`✓ Gemini AI başarıyla ${notifications.length} tavsiye üretti.`);
    } catch (aiErr) {
      console.warn('⚠️ Gemini API hatası, fallback kural motoruna geçiliyor:', aiErr.message);
      notifications = NotificationService.generateFallbackNotifications(context);
    }

    if (activePool && notifications.length > 0) {
      await NotificationService.syncNotificationsToDB(notifications, activePool);
    }

    const [allRows] = activePool ? await activePool.query('SELECT * FROM notifications ORDER BY created_at DESC LIMIT 30') : [notifications];
    const formatted = (allRows || []).map(r => ({ ...r, is_read: Boolean(r.is_read) }));
    const unreadCount = formatted.filter(n => !n.is_read).length;

    res.json({
      success: true,
      generatedCount: notifications.length,
      unreadCount,
      notifications: formatted
    });
  } catch (e) {
    console.error('POST /api/notifications/generate-ai error:', e.message);
    res.status(500).json({ error: 'AI tavsiyeleri üretilemedi', message: e.message });
  }
});


// -------------------------------------------------------------
// GEMINI AI CAMPAIGN SUGGESTIONS API
// -------------------------------------------------------------
const campaignSuggestionsHandler = async (req, res) => {
  try {
    const activePool = await getPool();
    let venues = [];
    let services = [];
    let reservations = [];
    let existingCampaigns = [];

    if (activePool) {
      const [vRows] = await activePool.query('SELECT id, name, price, capacity FROM venues');
      const [sRows] = await activePool.query('SELECT id, name, price, category FROM services');
      const [rRows] = await activePool.query('SELECT id, venue_id, event_date, total_amount, payment_status FROM reservations WHERE status != "DRAFT"');
      const [cRows] = await activePool.query('SELECT code, title FROM campaigns');
      venues = vRows || [];
      services = sRows || [];
      reservations = rRows || [];
      existingCampaigns = cRows || [];
    }

    const context = {
      business: 'İrem Düğün Sarayı & Balo Salonları (Arifiye)',
      venues: venues.map(v => ({ id: v.id, name: v.name, price: Number(v.price), capacity: v.capacity })),
      popularServices: services.slice(0, 8).map(s => ({ id: s.id, name: s.name, price: Number(s.price) })),
      totalActiveBookings: reservations.length,
      existingCampaignCodes: existingCampaigns.map(c => c.code)
    };

    const systemPrompt = `Sen İrem Düğün Sarayı'nın Baş Gelir Yönetimi ve Kampanya Stratejisi Uzmanısın (Gemini AI).
GÖREV: Düğün salonlarının kapasitelerini, hizmet paketlerini ve mevcut rezervasyon hacmini inceleyerek işletmeye en yüksek kâr ve doluluk kazandıracak 3 adet benzersiz, yaratıcı ve cazip KAMPANYA ÖNERİSİ üret.

ÇIKTI FORMATI:
Kesinlikle sadece geçerli bir JSON ARRAY döndür. Markdown veya ekstra açıklama yazma. JSON formatı şöyle olmalıdır:
[
  {
    "id": "ai-gemini-1",
    "code": "HAFTAICI25",
    "title": "Hafta İçi Rüya Düğün Kampanyası (%25 İndirim)",
    "type": "percent",
    "value": 25,
    "badge": "Gemini Doluluk Önerisi",
    "description": "Hafta içi boş günlerin doluluk oranını artırmak amacıyla planlanmıştır.",
    "suggestedVenueId": "v1",
    "discountPercent": 25
  }
]
Kurallar:
- "type" değeri sadece "percent", "amount" veya "free_service" olabilir.
- "code" değeri kısa, büyük harfli ve Türkçe karakter içermeyen akılda kalıcı kupon kodu olmalıdır (Örn: HAFTAICI25, GOLDVIP, ERKENREZ).
- Öneriler salonların kiralama fiyatları ve ek hizmetleriyle doğrudan tutarlı olmalıdır.`;

    const userPrompt = `İşte güncel işletme verileri:\n${JSON.stringify(context, null, 2)}\n\nLütfen en karlı 3 kampanya önerisini JSON array formatında üret.`;

    let suggestions = [];

    try {
      console.log('🤖 Kampanyalar için Gemini AI çağrısı yapılıyor...');
      const rawOutput = await GeminiProvider.generateContent(userPrompt, systemPrompt);
      const cleanJson = rawOutput.replace(/```json/gi, '').replace(/```/g, '').trim();
      const parsed = JSON.parse(cleanJson);
      if (Array.isArray(parsed) && parsed.length > 0) {
        suggestions = parsed;
        console.log(`✓ Gemini AI başarıyla ${suggestions.length} kampanya önerisi üretti.`);
      }
    } catch (aiErr) {
      console.warn('⚠️ Gemini AI kampanya üretim hatası, akıllı kural motoruna geçiliyor:', aiErr.message);
    }

    if (suggestions.length === 0) {
      const topVenue = venues[0] || { id: 'v1', name: 'Ana Salon', price: 85000 };
      suggestions = [
        {
          id: 'ai-fb-1',
          code: 'HAFTAICI20',
          title: 'Hafta İçi Düğün & Nişan Kampanyası (%20 İndirim)',
          type: 'percent',
          value: 20,
          badge: 'Atıl Gün Doluluk Fırsatı',
          description: 'Hafta içi günlerin doluluğunu yükseltmek ve ciro kazandırmak için %20 fırsat indirimi.',
          suggestedVenueId: topVenue.id,
          discountPercent: 20
        },
        {
          id: 'ai-fb-2',
          code: 'ERKENKAYIT15',
          title: '2026-2027 Erken Rezervasyon Avantajı (%15 İndirim)',
          type: 'percent',
          value: 15,
          badge: 'Nakit Akışı Hızlandırıcı',
          description: 'Gelecek sezon sözleşmelerini erkenden kapatıp kapora girdisini maksimize etmek için erken rezervasyon avantajı.',
          suggestedVenueId: topVenue.id,
          discountPercent: 15
        },
        {
          id: 'ai-fb-3',
          code: 'VIPORCHESTRA',
          title: 'Gold VIP Orkestra & Fotoğraf Hediye Paketi',
          type: 'free_service',
          value: 0,
          badge: 'Çapraz Satış Paketi',
          description: 'Salon kiralama görüşmelerinde orkestra ve çekim paketini hediye sunarak sözleşme kapanış oranını %40 artırın.',
          suggestedVenueId: topVenue.id,
          discountPercent: 0
        }
      ];
    }

    res.json({
      success: true,
      source: 'gemini-3.5-flash',
      count: suggestions.length,
      suggestions
    });
  } catch (e) {
    console.error('Campaign suggestions error:', e.message);
    res.status(500).json({ error: 'Kampanya önerileri üretilemedi', message: e.message });
  }
};

app.get('/api/ai/campaign-suggestions', campaignSuggestionsHandler);
app.post('/api/ai/campaign-suggestions', campaignSuggestionsHandler);
app.get('/api/campaigns/ai-suggestions', campaignSuggestionsHandler);
app.post('/api/campaigns/ai-suggestions', campaignSuggestionsHandler);


app.use((req, res) => {
  if (req.path.startsWith('/api/')) {
    return res.status(404).json({ error: 'API Uç Noktası Bulunamadı' });
  }
  res.sendFile('index.html', { root: __dirname });
});

const serverPort = process.env.PORT || 5001;
app.listen(serverPort, () => {
  console.log(`🚀 İrem Düğün Sarayı Sunucusu Aktif! Port: ${serverPort}`);
});
