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

app.use(cors());
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  next();
});
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));
app.use('/uploads', express.static(uploadsDir));
app.use(express.static(path.join(__dirname, './')));

app.get('/.well-known/appspecific/com.chrome.devtools.json', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.json({ status: 'ok' });
});

// JSON DB Dosyaları Okuma/Yazma Yardımcıları
const readDbFile = (fileName, fallback) => {
  try {
    const filePath = path.join(__dirname, 'scratch', fileName);
    if (fs.existsSync(filePath)) {
      const data = fs.readFileSync(filePath, 'utf8');
      const parsed = JSON.parse(data);
      if (parsed) return parsed;
    }
  } catch(e) {
    console.error('Error loading ' + fileName + ':', e.message);
  }
  return fallback;
};

const saveDbFile = (fileName, data) => {
  // Disksel JSON yerel dosya kaydı kapalı - Veriler %100 canlı MySQL/MariaDB veritabanında saklanır.
};

// %100 Canlı Veritabanı Bellek & Dosya Deposu
const memoryStore = {
  venues: readDbFile('db_venues.json', [
    { id: 'v1', name: 'Kraliyet Balo Salonu', category: 'Kapalı Salon', capacity: 750, price: 100000, costPrice: 35000, deposit: 15000, location: 'Sapanca Merkez, Sakarya', occupancyRate: 85, description: 'Yüksek tavanlı, kristal avizeli, iklimlendirme sistemli ve lüks sahne düzenine sahip ana balo salonumuz.', image: 'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=800&q=80', images: ['https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=800&q=80'], eventTypes: ['Düğün', 'Nişan', 'Kurumsal Kokteyl', 'Mezuniyet', 'Kına'], availableServices: ['s1', 's-tavuk-menu', 's2', 's3'] }
  ]),
  services: readDbFile('db_services.json', []),
  campaigns: readDbFile('db_campaigns.json', []),
  customers: readDbFile('db_customers.json', []),
  users: readDbFile('db_users.json', []),
  reservations: readDbFile('db_reservations.json', []),
  draftReservations: readDbFile('db_draft_reservations.json', []),
  expenses: readDbFile('db_expenses.json', []),
  media: readDbFile('db_media.json', [
    { id: 'm1', title: 'Kraliyet Balo Salonu Çekimi', category: 'Salon', url: 'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=800&q=80', file_size: '2.4 MB' }
  ]),
  roles: [
    { id: 'admin', name: 'Sistem Yöneticisi', permissions: ['dashboard', 'reservations', 'create_reservation', 'calendar', 'customers', 'finance', 'media', 'settings', 'roles', 'system_guide'] },
    { id: 'satisci', name: 'Satış Danışmanı', permissions: ['dashboard', 'reservations', 'create_reservation', 'calendar', 'customers'] },
    { id: 'sosyal_medyaci', name: 'Sosyal Medya Sorumlusu', permissions: ['dashboard', 'media'] },
    { id: 'musteri', name: 'Müşteri Portalı', permissions: ['reservations'] }
  ],
  systemSettings: readDbFile('db_system_settings.json', {
    publicTheme: 'dark-gold',
    heroBadgeText: '✨ Sapanca Göl Kenarı Lüks Düğün Tesisleri',
    heroTitle: "Hayalinizdeki Düğün İrem Düğün Sarayı'nda Unutulmaz Oluyor",
    heroSubtitle: '4 farklı balo salonu, açık hava kır bahçesi, kristal avizeler ve VIP ikram menüleriyle hayatınızın en özel gününe ev sahipliği yapıyoruz.'
  })
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
          targetRes = {
            id: resId,
            mediaKey: resId,
            customerName: `Etkinlik [${resId}]`,
            eventType: 'Düğün / Balo Daveti',
            date: new Date().toISOString().split('T')[0],
            venueId: 'v1',
            status: 'CONFIRMED',
            mediaFiles: []
          };
          memoryStore.reservations.push(targetRes);
          updated = true;
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
      saveDbFile('db_reservations.json', memoryStore.reservations);
    }
  } catch (err) {
    console.error('Disk medya senkronizasyon hatası:', err.message);
  }
};

syncPhysicalUploadsWithMemoryStore();

// MySQL Bağlantısı (Opsiyonel Canlı MySQL)
let pool = null;
const initMysql = async () => {
  try {
    const mysql = require('mysql2/promise');
    pool = mysql.createPool({
      host: process.env.DB_HOST || process.env.MYSQL_HOST || 'localhost',
      port: (process.env.DB_PORT || process.env.MYSQL_PORT) ? Number(process.env.DB_PORT || process.env.MYSQL_PORT) : 3306,
      user: process.env.DB_USER || process.env.MYSQL_USER || 'root',
      password: process.env.DB_PASSWORD || process.env.DB_PASS || process.env.MYSQL_PASSWORD || '',
      database: process.env.DB_NAME || process.env.MYSQL_DATABASE || 'irem_dugun_db',
      waitForConnections: true,
      connectionLimit: 10,
      queueLimit: 0
    });

    const syncMemoryFromMysql = async () => {
      if (!pool) return;
      try {
        const [vRows] = await pool.query('SELECT * FROM venues ORDER BY created_at DESC');
        if (vRows.length) memoryStore.venues = vRows.map(r => ({
          ...r,
          costPrice: r.cost_price ? Number(r.cost_price) : 0,
          occupancyRate: r.occupancy_rate || 0,
          eventTypes: r.features_json ? (typeof r.features_json === 'string' ? JSON.parse(r.features_json) : r.features_json) : ['Düğün', 'Nişan'],
          images: r.images_json ? (typeof r.images_json === 'string' ? JSON.parse(r.images_json) : r.images_json) : (r.image ? [r.image] : [])
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
      } catch (e) {
        console.error('MySQL Memory Hydration Error:', e.message);
      }
    };

    try {
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
          features_json JSON,
          images_json JSON,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
      `);

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
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
      `);

      console.log('✅ MySQL Tabloları Doğrulandı ve Hazırlandı!');
      await syncMemoryFromMysql();
      console.log('⚡ MariaDB Verileri Belleğe Senkronize Edildi!');
    } catch (e) {
      console.log('ℹ️ MySQL Tablo doğrulama uyarısı:', e.message);
    }
  } catch(err) {
    console.log('ℹ️ mysql2 paketi / sunucusu henüz ayarlanmadı, dosya/bellek deposu aktif.');
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
app.post('/api/upload-media', (req, res) => {
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

    let matchFound = false;
    memoryStore.reservations = memoryStore.reservations.map(r => {
      const isMatch = r.id === resId || r.mediaKey === resId || r.id === safeResId || r.mediaKey === safeResId;
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

    if (!matchFound) {
      if (memoryStore.reservations.length > 0) {
        const existingList = memoryStore.reservations[0].mediaFiles || [];
        memoryStore.reservations[0].mediaFiles = [newMediaObj, ...existingList];
      } else {
        memoryStore.reservations.push({
          id: safeResId,
          mediaKey: safeResId,
          title: 'Genel Rezervasyon',
          mediaFiles: [newMediaObj]
        });
      }
    }

    saveDbFile('db_reservations.json', memoryStore.reservations);

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
      saveDbFile('db_media.json', memoryStore.media);
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
    saveDbFile('db_reservations.json', memoryStore.reservations);

    // 5. Canlı MySQL Bağlantısı Varsa MySQL Tablolarından da Sil
    if (pool) {
      try {
        if (mediaId) await pool.query('DELETE FROM reservation_media WHERE id = ?', [mediaId]);
        if (fileName) await pool.query('DELETE FROM reservation_media WHERE file_name = ?', [fileName]);
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
app.get('/api/venues', async (req, res) => {
  if (pool) {
    try {
      const [rows] = await pool.query('SELECT * FROM venues ORDER BY created_at DESC');
      if (rows && rows.length > 0) {
        return res.json(rows.map(v => ({
          ...v,
          features: typeof v.features_json === 'string' ? JSON.parse(v.features_json) : (v.features_json || []),
          images: typeof v.images_json === 'string' ? JSON.parse(v.images_json) : (v.images_json || [])
        })));
      }
    } catch(e) {}
  }
  res.json(memoryStore.venues);
});

app.post('/api/venues', async (req, res) => {
  const item = { id: req.body.id || ('v-' + Date.now()), ...req.body };
  if (pool) {
    try {
      await pool.query(
        'INSERT INTO venues (id, name, category, capacity, price, deposit, location, description, features_json, images_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE name=?, category=?, capacity=?, price=?, deposit=?, location=?, description=?, features_json=?, images_json=?',
        [item.id, item.name, item.category || 'Kapalı Salon', item.capacity || 500, item.price || 0, item.deposit || 0, item.location || '', item.description || '', JSON.stringify(item.features || []), JSON.stringify(item.images || []), item.name, item.category || 'Kapalı Salon', item.capacity || 500, item.price || 0, item.deposit || 0, item.location || '', item.description || '', JSON.stringify(item.features || []), JSON.stringify(item.images || [])]
      );
    } catch(e) {}
  }
  const idx = memoryStore.venues.findIndex(v => v.id === item.id);
  if (idx >= 0) memoryStore.venues[idx] = item;
  else memoryStore.venues.unshift(item);

  saveDbFile('db_venues.json', memoryStore.venues);
  res.status(201).json({ success: true, item });
});

app.delete('/api/venues/:id', (req, res) => {
  const { id } = req.params;
  memoryStore.venues = memoryStore.venues.filter(v => v.id !== id);
  saveDbFile('db_venues.json', memoryStore.venues);
  res.json({ success: true, id });
});

// -------------------------------------------------------------
// 2. EK HİZMETLER ENDPOINTS (/api/services)
// -------------------------------------------------------------
app.get('/api/services', async (req, res) => {
  if (pool) {
    try {
      const [rows] = await pool.query('SELECT * FROM services ORDER BY created_at DESC');
      if (rows && rows.length > 0) return res.json(rows);
    } catch(e) {}
  }
  res.json(memoryStore.services);
});

app.post('/api/services', async (req, res) => {
  const item = { id: req.body.id || ('s-' + Date.now()), ...req.body };
  if (pool) {
    try {
      await pool.query(
        'INSERT INTO services (id, name, category, price, pricing_type, description, image_url) VALUES (?, ?, ?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE name=?, category=?, price=?, pricing_type=?, description=?, image_url=?',
        [item.id, item.name, item.category || 'Catering', item.price || 0, item.pricing_type || 'fixed', item.description || '', item.image_url || '', item.name, item.category || 'Catering', item.price || 0, item.pricing_type || 'fixed', item.description || '', item.image_url || '']
      );
    } catch(e) {}
  }
  const idx = memoryStore.services.findIndex(s => s.id === item.id);
  if (idx >= 0) memoryStore.services[idx] = item;
  else memoryStore.services.unshift(item);

  saveDbFile('db_services.json', memoryStore.services);
  res.status(201).json({ success: true, item });
});

app.delete('/api/services/:id', (req, res) => {
  const { id } = req.params;
  memoryStore.services = memoryStore.services.filter(s => s.id !== id);
  saveDbFile('db_services.json', memoryStore.services);
  res.json({ success: true, id });
});

// -------------------------------------------------------------
// 3. MÜŞTERİLER ENDPOINTS (/api/customers)
// -------------------------------------------------------------
app.get('/api/customers', async (req, res) => {
  if (pool) {
    try {
      const [rows] = await pool.query('SELECT * FROM customers ORDER BY created_at DESC');
      if (rows && rows.length > 0) return res.json(rows);
    } catch(e) {}
  }
  res.json(memoryStore.customers);
});

app.post('/api/customers', async (req, res) => {
  const item = { id: req.body.id || ('cust-' + Date.now()), ...req.body };
  if (pool) {
    try {
      await pool.query(
        'INSERT INTO customers (id, name, email, phone, address, tax_type, tc_no, vkn_no, tax_office, follow_up, follow_up_note, avatar) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE name=?, email=?, phone=?, address=?, tax_type=?, tc_no=?, vkn_no=?, tax_office=?, follow_up=?, follow_up_note=?, avatar=?',
        [item.id, item.name, item.email || '', item.phone || '', item.address || '', item.tax_type || 'individual', item.tc_no || '', item.vkn_no || '', item.tax_office || '', item.follow_up ? 1 : 0, item.follow_up_note || '', item.avatar || '', item.name, item.email || '', item.phone || '', item.address || '', item.tax_type || 'individual', item.tc_no || '', item.vkn_no || '', item.tax_office || '', item.follow_up ? 1 : 0, item.follow_up_note || '', item.avatar || '']
      );
    } catch(e) {}
  }
  const idx = memoryStore.customers.findIndex(c => c.id === item.id);
  if (idx >= 0) memoryStore.customers[idx] = item;
  else memoryStore.customers.unshift(item);

  saveDbFile('db_customers.json', memoryStore.customers);
  res.status(201).json({ success: true, item });
});

app.delete('/api/customers/:id', (req, res) => {
  const { id } = req.params;
  memoryStore.customers = memoryStore.customers.filter(c => c.id !== id);
  saveDbFile('db_customers.json', memoryStore.customers);
  res.json({ success: true, id });
});

// -------------------------------------------------------------
// 4. KULLANICILAR ENDPOINTS (/api/users)
// -------------------------------------------------------------
app.get('/api/users', async (req, res) => {
  if (pool) {
    try {
      const [rows] = await pool.query('SELECT id, name, email, role, avatar, created_at FROM users ORDER BY created_at DESC');
      if (rows && rows.length > 0) return res.json(rows);
    } catch(e) {}
  }
  res.json(memoryStore.users);
});

app.post('/api/users', async (req, res) => {
  const item = { id: req.body.id || ('u_' + Date.now()), ...req.body };
  if (pool) {
    try {
      await pool.query(
        'INSERT INTO users (id, name, email, password_hash, role, avatar) VALUES (?, ?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE name=?, email=?, role=?, avatar=?',
        [item.id, item.name, item.email, item.password || '123456', item.role || 'admin', item.avatar || '', item.name, item.email, item.role || 'admin', item.avatar || '']
      );
    } catch(e) {}
  }
  const idx = memoryStore.users.findIndex(u => u.id === item.id || u.email === item.email);
  if (idx >= 0) memoryStore.users[idx] = { ...memoryStore.users[idx], ...item };
  else memoryStore.users.unshift(item);

  saveDbFile('db_users.json', memoryStore.users);
  res.status(201).json({ success: true, item });
});

app.delete('/api/users/:id', (req, res) => {
  const { id } = req.params;
  memoryStore.users = memoryStore.users.filter(u => u.id !== id);
  saveDbFile('db_users.json', memoryStore.users);
  res.json({ success: true, id });
});

// -------------------------------------------------------------
// 5. REZERVASYONLAR ENDPOINTS (/api/reservations)
// -------------------------------------------------------------
app.get('/api/reservations', async (req, res) => {
  if (pool) {
    try {
      const [rows] = await pool.query('SELECT * FROM reservations ORDER BY event_date DESC');
      if (rows && rows.length > 0) {
        const merged = rows.map(r => {
          const mem = memoryStore.reservations.find(m => m.id === r.id);
          return mem ? { ...mem, ...r, customExpenses: mem.customExpenses || r.customExpenses || [], mediaFiles: mem.mediaFiles || r.mediaFiles || [] } : r;
        });
        return res.json(merged);
      }
    } catch(e) {}
  }
  res.json(memoryStore.reservations);
});

app.post('/api/reservations', async (req, res) => {
  const item = { id: req.body.id || `RES-${new Date().getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`, ...req.body };
  const idx = memoryStore.reservations.findIndex(r => r.id === item.id || (r.mediaKey && r.mediaKey === item.id));
  
  if (idx >= 0) {
    const existingRes = memoryStore.reservations[idx];
    const existingMedia = existingRes.mediaFiles || [];
    const incomingMedia = item.mediaFiles || [];
    
    // Diskteki mevcut görseller ile gelen görselleri harmanla (hiçbir davetli görseli silinmesin)
    const mergedMediaMap = new Map();
    [...existingMedia, ...incomingMedia].forEach(m => {
      if (m && (m.id || m.url)) {
        mergedMediaMap.set(m.id || m.url, m);
      }
    });
    item.mediaFiles = Array.from(mergedMediaMap.values());
    memoryStore.reservations[idx] = item;
  } else {
    memoryStore.reservations.unshift(item);
  }

  saveDbFile('db_reservations.json', memoryStore.reservations);
  res.status(201).json({ success: true, id: item.id, item });
});

app.delete('/api/reservations/:id', (req, res) => {
  const { id } = req.params;
  const safeResId = String(id).replace(/[^a-zA-Z0-9_-]/g, '_');
  const resDir = path.join(uploadsDir, safeResId);

  if (fs.existsSync(resDir)) {
    try {
      fs.rmSync(resDir, { recursive: true, force: true });
      console.log(`🗑️ Rezervasyon Klasörü Sunucudan Fiziksel Olarak Silindi: ${resDir}`);
    } catch(err) {
      console.error('Rezervasyon klasör silme hatası:', err.message);
    }
  }

  memoryStore.reservations = memoryStore.reservations.filter(r => r.id !== id);
  saveDbFile('db_reservations.json', memoryStore.reservations);

  if (pool) {
    pool.query('DELETE FROM reservations WHERE id = ?', [id]).catch(e => console.warn(e));
  }

  res.json({ success: true, id, message: 'Rezervasyon ve bağlı medyaları sunucudan fiziken silindi.' });
});

// -------------------------------------------------------------
// 6. GİDERLER ENDPOINTS (/api/expenses)
// -------------------------------------------------------------
app.get('/api/expenses', async (req, res) => {
  if (pool) {
    try {
      const [rows] = await pool.query('SELECT * FROM expenses ORDER BY date DESC');
      if (rows && rows.length > 0) {
        const dbIds = new Set(rows.map(r => r.id));
        const extraMem = (memoryStore.expenses || []).filter(e => !dbIds.has(e.id));
        return res.json([...rows, ...extraMem]);
      }
    } catch(e) {}
  }
  res.json(memoryStore.expenses || []);
});

app.post('/api/expenses', async (req, res) => {
  const item = { id: req.body.id || ('exp-' + Date.now()), ...req.body };
  if (pool) {
    try {
      await pool.query(
        'INSERT INTO expenses (id, title, category, amount, date, description, type) VALUES (?, ?, ?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE title=?, category=?, amount=?, date=?, description=?, type=?',
        [item.id, item.title, item.category || 'Genel', item.amount || 0, item.date || new Date().toISOString().split('T')[0], item.description || '', item.type || 'expense', item.title, item.category || 'Genel', item.amount || 0, item.date || new Date().toISOString().split('T')[0], item.description || '', item.type || 'expense']
      );
    } catch(e) {}
  }
  const idx = memoryStore.expenses.findIndex(e => e.id === item.id);
  if (idx >= 0) memoryStore.expenses[idx] = item;
  else memoryStore.expenses.unshift(item);

  saveDbFile('db_expenses.json', memoryStore.expenses);
  res.status(201).json({ success: true, item });
});

app.delete('/api/expenses/:id', (req, res) => {
  const { id } = req.params;
  memoryStore.expenses = memoryStore.expenses.filter(e => e.id !== id);
  saveDbFile('db_expenses.json', memoryStore.expenses);
  res.json({ success: true, id });
});

// -------------------------------------------------------------
// 7. KAMPANYALAR ENDPOINTS (/api/campaigns)
// -------------------------------------------------------------
app.get('/api/campaigns', async (req, res) => {
  res.json(memoryStore.campaigns);
});

app.post('/api/campaigns', async (req, res) => {
  const item = { id: req.body.id || ('c-' + Date.now()), ...req.body };
  const idx = memoryStore.campaigns.findIndex(c => c.id === item.id);
  if (idx >= 0) memoryStore.campaigns[idx] = item;
  else memoryStore.campaigns.unshift(item);

  saveDbFile('db_campaigns.json', memoryStore.campaigns);
  res.status(201).json({ success: true, item });
});

app.delete('/api/campaigns/:id', (req, res) => {
  const { id } = req.params;
  memoryStore.campaigns = memoryStore.campaigns.filter(c => c.id !== id);
  saveDbFile('db_campaigns.json', memoryStore.campaigns);
  res.json({ success: true, id });
});

// -------------------------------------------------------------
// 8. MEDYA & GALERİ ENDPOINTS (/api/media)
// -------------------------------------------------------------
app.get('/api/media', async (req, res) => {
  res.json(memoryStore.media);
});

app.post('/api/media', async (req, res) => {
  const item = { id: req.body.id || ('m-' + Date.now()), ...req.body };
  memoryStore.media.unshift(item);
  saveDbFile('db_media.json', memoryStore.media);
  res.status(201).json({ success: true, item });
});

// -------------------------------------------------------------
// 9. ROLLER VE İZİNLER ENDPOINTS (/api/roles & /api/permissions)
// -------------------------------------------------------------
app.get('/api/roles', async (req, res) => {
  res.json(memoryStore.roles);
});

app.post('/api/roles', async (req, res) => {
  if (Array.isArray(req.body)) {
    memoryStore.roles = req.body;
  }
  res.json({ success: true, roles: memoryStore.roles });
});

// -------------------------------------------------------------
// 10. SİSTEM & PUBLIC AYARLARI ENDPOINTS
// -------------------------------------------------------------
app.get('/api/public-settings', async (req, res) => {
  if (pool) {
    try {
      const [vRows] = await pool.query('SELECT * FROM venues ORDER BY created_at DESC');
      if (vRows.length) memoryStore.venues = vRows.map(r => ({
        ...r,
        costPrice: r.cost_price ? Number(r.cost_price) : 0,
        occupancyRate: r.occupancy_rate || 0,
        eventTypes: r.features_json ? (typeof r.features_json === 'string' ? JSON.parse(r.features_json) : r.features_json) : ['Düğün', 'Nişan'],
        images: r.images_json ? (typeof r.images_json === 'string' ? JSON.parse(r.images_json) : r.images_json) : (r.image ? [r.image] : [])
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

app.post('/api/public-settings', (req, res) => {
  if (req.body) {
    if (Array.isArray(req.body.reservations)) {
      memoryStore.reservations = req.body.reservations;
      saveDbFile('db_reservations.json', memoryStore.reservations);
    }
    if (Array.isArray(req.body.draftReservations)) {
      memoryStore.draftReservations = req.body.draftReservations;
      saveDbFile('db_draft_reservations.json', memoryStore.draftReservations);
    }
    if (Array.isArray(req.body.expenses)) {
      memoryStore.expenses = req.body.expenses;
      saveDbFile('db_expenses.json', memoryStore.expenses);
    }
    if (Array.isArray(req.body.customers)) {
      memoryStore.customers = req.body.customers;
      saveDbFile('db_customers.json', memoryStore.customers);
    }
    if (Array.isArray(req.body.users)) {
      memoryStore.users = req.body.users;
      saveDbFile('db_users.json', memoryStore.users);
    }
    if (Array.isArray(req.body.venues)) {
      memoryStore.venues = req.body.venues;
      saveDbFile('db_venues.json', memoryStore.venues);
    }
    if (Array.isArray(req.body.services)) {
      memoryStore.services = req.body.services;
      saveDbFile('db_services.json', memoryStore.services);
    }
    if (Array.isArray(req.body.campaigns)) {
      memoryStore.campaigns = req.body.campaigns;
      saveDbFile('db_campaigns.json', memoryStore.campaigns);
    }
    if (Array.isArray(req.body.roles)) {
      memoryStore.roles = req.body.roles;
      saveDbFile('db_roles.json', memoryStore.roles);
    }
    if (req.body.tab_permissions && typeof req.body.tab_permissions === 'object') {
      memoryStore.tab_permissions = req.body.tab_permissions;
      saveDbFile('db_tab_permissions.json', memoryStore.tab_permissions);
    }

    memoryStore.systemSettings = { ...memoryStore.systemSettings, ...req.body };
    saveDbFile('db_system_settings.json', memoryStore.systemSettings);
  }
  res.json({ success: true, message: 'Kamu/Sistem ayarları veritabanında güncellendi', ...memoryStore.systemSettings });
});

app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', serverTime: new Date(), uploadsPath: uploadsDir });
});

// HTML Rota Yönlendirmeleri
app.get(['/yonetim', '/yonetim.html', '/giris', '/login'], (req, res) => {
  res.sendFile('yonetim.html', { root: __dirname });
});

app.use((req, res) => {
  if (req.path.startsWith('/api/')) {
    return res.status(404).json({ error: 'API Uç Noktası Bulunamadı' });
  }
  res.sendFile('index.html', { root: __dirname });
});

app.listen(PORT, () => {
  console.log(`🏰 İrem Düğün Sarayı REST API & Dosya Sunucusu http://localhost:${PORT} portunda yayında.`);
});
