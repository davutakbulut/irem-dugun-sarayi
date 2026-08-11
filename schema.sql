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

-- 8. GİDERLER TABLOSU (expenses)
CREATE TABLE IF NOT EXISTS expenses (
  id VARCHAR(50) PRIMARY KEY,
  title VARCHAR(150) NOT NULL,
  category VARCHAR(100) NOT NULL DEFAULT 'Genel',
  amount DECIMAL(12,2) NOT NULL DEFAULT 0.00,
  date DATE NOT NULL,
  description TEXT,
  type ENUM('expense', 'income') NOT NULL DEFAULT 'expense',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 9. MEDYA FOTOĞRAF VE DOSYALAR TABLOSU (media)
CREATE TABLE IF NOT EXISTS media (
  id VARCHAR(50) PRIMARY KEY,
  title VARCHAR(150),
  category VARCHAR(100) DEFAULT 'Genel',
  url TEXT NOT NULL,
  file_size VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 10. ROLLER VE İZİNLER TABLOSU (roles)
CREATE TABLE IF NOT EXISTS roles (
  id VARCHAR(50) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  permissions_json JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 11. SİSTEM VE TEMA AYARLARI TABLOSU (system_settings)
CREATE TABLE IF NOT EXISTS system_settings (
  id INT PRIMARY KEY DEFAULT 1,
  settings_json JSON NOT NULL,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
