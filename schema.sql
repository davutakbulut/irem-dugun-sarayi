-- ============================================================
-- İREM DÜĞÜN SARAYI & ORGANİZASYON PLATFORMU
-- KAPSAMLI MYSQL VERİTABANI ŞEMASI (schema.sql)
-- ============================================================

CREATE DATABASE IF NOT EXISTS irem_dugun_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE irem_dugun_db;

-- 1. DÜĞÜN SALONLARI TABLOSU (venues)
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. EK HİZMETLER TABLOSU (services)
CREATE TABLE IF NOT EXISTS services (
  id VARCHAR(50) PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  category VARCHAR(100) NOT NULL DEFAULT 'Catering',
  price DECIMAL(12,2) NOT NULL DEFAULT 0.00,
  pricing_type ENUM('fixed', 'per_person') NOT NULL DEFAULT 'fixed',
  description TEXT,
  image_url TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. KAMPANYALAR TABLOSU (campaigns)
CREATE TABLE IF NOT EXISTS campaigns (
  id VARCHAR(50) PRIMARY KEY,
  code VARCHAR(50) NOT NULL UNIQUE,
  title VARCHAR(150) NOT NULL,
  type ENUM('percentage', 'flat_discount', 'free_service') NOT NULL DEFAULT 'percentage',
  value DECIMAL(12,2) DEFAULT 0.00,
  description TEXT,
  start_date DATE,
  end_date DATE,
  active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. MÜŞTERİ REHBERİ TABLOSU (customers)
CREATE TABLE IF NOT EXISTS customers (
  id VARCHAR(50) PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  email VARCHAR(150),
  phone VARCHAR(50) NOT NULL,
  address TEXT,
  tax_type ENUM('individual', 'corporate') NOT NULL DEFAULT 'individual',
  tc_no VARCHAR(20),
  vkn_no VARCHAR(20),
  tax_office VARCHAR(100),
  follow_up BOOLEAN DEFAULT FALSE,
  follow_up_note TEXT,
  avatar TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. KULLANICILAR VE ROLLER TABLOSU (users)
CREATE TABLE IF NOT EXISTS users (
  id VARCHAR(50) PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  email VARCHAR(150) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('admin', 'satisci', 'sosyal_medyaci', 'musteri') NOT NULL DEFAULT 'musteri',
  avatar TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. REZERVASYONLAR TABLOSU (reservations)
CREATE TABLE IF NOT EXISTS reservations (
  id VARCHAR(50) PRIMARY KEY,
  venue_id VARCHAR(50) NOT NULL,
  customer_id VARCHAR(50) NOT NULL,
  customer_name VARCHAR(150) NOT NULL,
  customer_email VARCHAR(150),
  customer_phone VARCHAR(50),
  event_date DATE NOT NULL,
  time_slot VARCHAR(50) NOT NULL,
  guest_count INT NOT NULL DEFAULT 100,
  venue_price DECIMAL(12,2) NOT NULL DEFAULT 0.00,
  subtotal DECIMAL(12,2) NOT NULL DEFAULT 0.00,
  campaign_code VARCHAR(50),
  discount_amount DECIMAL(12,2) DEFAULT 0.00,
  vat_amount DECIMAL(12,2) NOT NULL DEFAULT 0.00,
  total_amount DECIMAL(12,2) NOT NULL DEFAULT 0.00,
  deposit_paid DECIMAL(12,2) DEFAULT 0.00,
  remaining_balance DECIMAL(12,2) NOT NULL DEFAULT 0.00,
  payment_status ENUM('Bekliyor', 'Kapora Alındı', 'Ödendi', 'Tamamlandı') NOT NULL DEFAULT 'Bekliyor',
  is_invoiced BOOLEAN DEFAULT FALSE,
  invoice_type ENUM('individual', 'corporate') DEFAULT 'individual',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (venue_id) REFERENCES venues(id) ON DELETE CASCADE,
  FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
  UNIQUE KEY unique_venue_slot (venue_id, event_date, time_slot)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. REZERVASYON EK HİZMETLERİ İLİŞKİ TABLOSU (reservation_services)
CREATE TABLE IF NOT EXISTS reservation_services (
  id INT AUTO_INCREMENT PRIMARY KEY,
  reservation_id VARCHAR(50) NOT NULL,
  service_id VARCHAR(50) NOT NULL,
  quantity INT NOT NULL DEFAULT 1,
  unit_price DECIMAL(12,2) NOT NULL DEFAULT 0.00,
  FOREIGN KEY (reservation_id) REFERENCES reservations(id) ON DELETE CASCADE,
  FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. REZERVASYON AKIŞ PLANI TABLOSU (reservation_flow)
CREATE TABLE IF NOT EXISTS reservation_flow (
  id INT AUTO_INCREMENT PRIMARY KEY,
  reservation_id VARCHAR(50) NOT NULL,
  time_slot VARCHAR(20) NOT NULL,
  title VARCHAR(255) NOT NULL,
  FOREIGN KEY (reservation_id) REFERENCES reservations(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 9. MEDYA VE FOTOĞRAF GALERİSİ TABLOSU (reservation_media)
CREATE TABLE IF NOT EXISTS reservation_media (
  id VARCHAR(50) PRIMARY KEY,
  reservation_id VARCHAR(50) NOT NULL,
  media_url TEXT NOT NULL,
  uploaded_by VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (reservation_id) REFERENCES reservations(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- ÖRNEK BAŞLANGIÇ VERİLERİ (SEED DATA)
-- ============================================================

INSERT INTO venues (id, name, category, capacity, price, deposit, location, occupancy_rate, description, features_json, images_json) VALUES
('v1', 'Kraliyet Balo Salonu', 'Kapalı Salon', 750, 65000.00, 15000.00, 'Sapanca Merkez, Sakarya', 85, 'Yüksek tavanlı, kristal avizeli lüks balo salonu.', '["Kristal Avizeler", "Gelişmiş Ses & Işık", "Gelin Odayı VİP", "Jeneratör", "Otopark (300 Araç)"]', '["https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=800&q=80"]'),
('v2', 'Kır Bahçesi VİP', 'Açık Hava / Kır Bahçesi', 1000, 85000.00, 20000.00, 'Göl Kenarı, Sapanca, Sakarya', 92, 'Sapanca Gölü manzaralı kır düğünü alanı.', '["Göl Manzarası", "Açılır-Kapanır Tente", "Peyzaj Işıklandırma", "Çocuk Oyun Alanı"]', '["https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?auto=format&fit=crop&w=800&q=80"]'),
('v3', 'Bosphorus Teras & Kına Salonu', 'Butik / Teras', 400, 45000.00, 10000.00, 'Sapanca Panoramik Teras', 70, 'Kına geceleri ve nişan organizasyonları için otantik teras.', '["Kına Tahtı Konsepti", "Otantik Dekoru", "Panoramik Manzara", "DJ Performansı"]', '["https://images.unsplash.com/photo-1527529482837-4698179dc6ce?auto=format&fit=crop&w=800&q=80"]');

INSERT INTO services (id, name, category, price, pricing_type, description, image_url) VALUES
('s1', 'Gurme Yemek Servisi (Et Menü)', 'Catering', 350.00, 'per_person', 'Ordövr, Dana Biftek, düğün pastası.', 'https://images.unsplash.com/photo-1555244162-803834f70033?auto=format&fit=crop&w=600&q=80'),
('s2', 'Fotoğraf & 4K Video Paketi', 'Medya', 18000.00, 'fixed', 'Dış çekim, 4K sinematik albüm.', 'https://images.unsplash.com/photo-1537633552985-df8429e8048b?auto=format&fit=crop&w=600&q=80'),
('s3', 'Canlı Müzik Orkestrası & DJ', 'Eğlence', 25000.00, 'fixed', '6 kişilik orkestra ve DJ.', 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=600&q=80'),
('s4', 'Masa & Sahne Süsleme', 'Dekorasyon', 15000.00, 'fixed', 'Canlı çiçekler ve şamdanlar.', 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=600&q=80'),
('s5', 'Volkan, Konfeti & Işık Şovu', 'Efekt', 8000.00, 'fixed', 'Soğuk volkan ve konfeti.', 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=600&q=80');

INSERT INTO campaigns (id, code, title, type, value, description, start_date, end_date, active) VALUES
('c1', 'IREM2026', 'Erken Rezervasyon %10 İndirim', 'percentage', 10.00, 'Tüm rezervasyonlarda %10 indirim!', '2026-01-01', '2026-12-31', TRUE),
('c2', 'HEDIYE-FOTO', 'Fotoğraf Çekimi Hediye!', 'free_service', 0.00, 'Kır Bahçesi kiralayana Fotoğraf Paketi HEDİYE!', '2026-05-01', '2026-09-30', TRUE),
('c3', 'VIP5000', '5.000 TL Nakit İndirim', 'flat_discount', 5000.00, 'Doğrudan 5.000 TL kiralama indirimi.', '2026-03-01', '2026-11-30', TRUE);

INSERT INTO customers (id, name, email, phone, address, tax_type, tc_no, tax_office, follow_up, follow_up_note, avatar) VALUES
('cust1', 'Ahmet Yılmaz & Ayşe Kaya', 'ahmet.yilmaz@example.com', '+90 532 111 2233', 'Atatürk Mah. Sapanca / Sakarya', 'individual', '12345678901', 'Sapanca VD', TRUE, 'Sünnet düğünü için 2 yıl sonra görüşülecek.', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'),
('cust2', 'Mehmet Demir (Demir İnşaat)', 'mehmet@demiras.com', '+90 533 444 5566', 'Bağdat Cad. Kadıköy / İstanbul', 'corporate', NULL, 'Kadıköy VD', FALSE, NULL, 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80');

INSERT INTO users (id, name, email, password_hash, role, avatar) VALUES
('u1', 'İrem Yılmaz (Admin)', 'admin@iremdugunsarayi.com', '$2b$10$YourHashedPasswordHere', 'admin', 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80'),
('u2', 'Canan Güneş (Satış Müdürü)', 'satis@iremdugunsarayi.com', '$2b$10$YourHashedPasswordHere', 'satisci', 'https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=200&q=80'),
('u3', 'Murat Arslan (Sosyal Medya)', 'sosyal@iremdugunsarayi.com', '$2b$10$YourHashedPasswordHere', 'sosyal_medyaci', 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=200&q=80'),
('u4', 'Ahmet Yılmaz (Müşteri)', 'ahmet.yilmaz@example.com', '$2b$10$YourHashedPasswordHere', 'musteri', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80');

INSERT INTO reservations (id, venue_id, customer_id, customer_name, customer_email, customer_phone, event_date, time_slot, guest_count, venue_price, subtotal, campaign_code, discount_amount, vat_amount, total_amount, deposit_paid, remaining_balance, payment_status, is_invoiced, invoice_type) VALUES
('RES-2026-001', 'v1', 'cust1', 'Ahmet Yılmaz & Ayşe Kaya', 'ahmet.yilmaz@example.com', '+90 532 111 2233', '2026-08-15', '19:00-23:00', 500, 65000.00, 283000.00, 'IREM2026', 28300.00, 50940.00, 305640.00, 50000.00, 255640.00, 'Kapora Alındı', TRUE, 'individual'),
('RES-2026-002', 'v2', 'cust2', 'Mehmet Demir (Demir İnşaat)', 'mehmet@demiras.com', '+90 533 444 5566', '2026-09-05', '13:00-17:00', 800, 85000.00, 380000.00, 'VIP5000', 5000.00, 75000.00, 450000.00, 450000.00, 0.00, 'Ödendi', TRUE, 'corporate');
