# 🏰 İREM DÜĞÜN SARAYI & ORGANİZASYON PLATFORMU
## KAPSAMLI PROJE DETAYLARI VE MASTER PROMPT DOSYASI

> **Not:** Bu doküman, NotebookLM'e yüklenmek üzere hazırlanan **İrem Düğün Sarayı & Organizasyon Şirketi** projesinin tüm mimari, iş mantığı, kullanıcı rolleri (RBAC), MySQL veritabanı şeması ve eklenen eklentilerin (plugins) detaylarını içeren tam kapsamlı master referans kılavuzudur.

---

## 📑 İÇİNDEKİLER
1. [Proje Hakkında & Genel Bilgiler](#1-proje-hakkında--genel-bilgiler)
2. [Teknik Yığın ve Mimari İlkeler](#2-teknik-yığın-ve-mimari-ilkeler)
3. [Eklenen Eklentiler & Beceriler (Plugins & Skills)](#3-eklenen-eklentiler--beceriler-plugins--skills)
4. [Tema, Kurumsal Dil & Dinamik Renk Paleti](#4-tema-kurumsal-dil--dinamik-renk-paleti)
5. [Rol Tabanlı Erişim Kontrolü (RBAC) Yetki Matrisi](#5-rol-tabanlı-erişim-kontrolü-rbac-yetki-matrisi)
6. [Yetkisiz Erişim (403 Access Denied) Güvenlik Modülü](#6-yetkisiz-erişim-403-access-denied-güvenlik-modülü)
7. [Temiz ASCII URL Yönlendirme (Routing) Kuralları](#7-temiz-ascii-url-yönlendirme-routing-kuralları)
8. [MySQL Veritabanı Mimarisi (schema.sql)](#8-mysql-veritabanı-mimarisi-schemasql)
9. [Çakışma Önleme (Collision Check) & Zaman Dilimleri](#9-çakışma-önleme-collision-check--zaman-dilimleri)
10. [Finansal Hesaplamalar, KDV %20 & Fatura Otomasyonu](#10-finansal-hesaplamalar-kdv-20--fatura-otomasyonu)
11. [Otomatik İletişim & WhatsApp Entegrasyonu](#11-otomatik-iletişim--whatsapp-entegrasyonu)
12. [Yapay Zeka (AI) Destekli Raporlar ve Öneriler](#12-yapay-zeka-ai-destekli-raporlar-ve-öneriler)

---

## 1. PROJE HAKKINDA & GENEL BİLGİLER
- **Şirket Adı:** İrem Düğün Sarayı & Organizasyon Şirketi
- **Lokasyon:** Sapanca Göl Kenarı, Sakarya
- **İletişim:** +90 532 111 2233 | admin@iremdugunsarayi.com
- **Sektör:** Düğün Salonu Kiralama, Kır Düğünü, Kına Gecesi, Nişan ve Kurumsal Etkinlik Organizasyonu.

---

## 2. TEKNİK YIĞIN VE MİMARİ İLKELER
1. **Frontend Core:** React 18 (JS/JSX) + Semantik HTML5.
2. **Backend API & Database:** Node.js (Express.js) + MySQL 8.0 (`schema.sql`).
3. **Single Page Application (SPA):** Tüm sekme geçişleri, modallar ve bildirimler **sayfa yenilenmeden** gerçekleşir.
4. **Stil Sistem:** Tailwind CSS + Custom CSS Variables + Lucide Icons + Google Fonts (Inter & Outfit).

---

## 3. EKLENEN EKLENTİLER & BECERİLER (PLUGINS & SKILLS)
Sisteme kurulan ve aktif olarak kullanılan 4 güçlü eklenti:
1. **`superpowers`** (`https://github.com/obra/superpowers`): LLM araçları, otonom ajan yetenekleri ve iş akışı optimizasyonları.
2. **`frontend-design`** (`https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design`): Üst düzey UI/UX tasarım standartları, renk paleti ve duyarlı (responsive) web geliştirme ilkeleri.
3. **`security-guidance`** (`https://github.com/anthropics/claude-code/tree/main/plugins/security-guidance`): Güvenlik denetimleri, RBAC yetki doğrulamaları ve girdi veri güvenliği ilkeleri.
4. **`claude-mem`** (`https://github.com/thedotmack/claude-mem`): Kalıcı hafıza, kullanıcı tercihlerini takip ve uzun süreli sohbet senkronizasyonu.

---

## 4. TEMA, KURUMSAL DİL & DİNAMİK RENK PALETİ
- **Varsayılan Tema:** **Şık Krem / Beyaz Kurumsal Mod (Fresh White & Cream Corporate Mode)**.
- **Alternatif Tema:** **Gece Lüks Şampanya Modu (Dark Mode)**.
- **Dinamik CSS Değişkenleri (CSS Variables):**
  - `--color-gold`: `#d97706` (Ana Altın/Şampanya Vurgusu)
  - `--color-bg`: `#faf9f6` (Ferah Krem Arka Plan)
  - `--color-card`: `#ffffff` (Saf Beyaz Kartlar)

---

## 5. ROL TABANLI ERİŞİM KONTROLÜ (RBAC) YETKİ MATRİSİ

Sistemde 4 farklı kullanıcı rolü tanımlanmıştır:

| Sekme / Modül | Admin 👑 | Satışçı 💼 | Sosyal Medya 📸 | Müşteri 💑 |
| :--- | :---: | :---: | :---: | :---: |
| **Anasayfa / İstatistikler** | ✅ Tam Yetki | ✅ Yetkili | ✅ Yetkili | ✅ (Özel Portal) |
| **Düğün Salonlarım** | ✅ Tam Yetki | ✅ Görür/Satış | 🚫 Yetkisiz | 🚫 Yetkisiz |
| **Ek Hizmetler** | ✅ Tam Yetki | ✅ Görür/Satış | 🚫 Yetkisiz | 🚫 Yetkisiz |
| **Rezervasyonlar** | ✅ Tam Yetki | ✅ Yönetir | 🚫 Yetkisiz | 🚫 Yetkisiz |
| **Takvim Görünümü** | ✅ Tam Yetki | ✅ Görür | 🚫 Yetkisiz | 🚫 Yetkisiz |
| **Kampanyalar** | ✅ Tam Yetki | 🚫 Yetkisiz | 🚫 Yetkisiz | 🚫 Yetkisiz |
| **Finans & Fatura** | ✅ Tam Yetki | 🚫 Gizli | 🚫 Yetkisiz | 🚫 Yetkisiz |
| **Müşteri Rehberi** | ✅ Tam Yetki | ✅ Görür/Ekle | 🚫 Yetkisiz | 🚫 Yetkisiz |
| **Kullanıcı Yönetimi** | ✅ Tam Yetki | 🚫 Yetkisiz | 🚫 Yetkisiz | 🚫 Yetkisiz |
| **Raporlar & AI Öneri** | ✅ Tam Yetki | 🚫 Yetkisiz | 🚫 Yetkisiz | 🚫 Yetkisiz |
| **Medya & Foto Yükle** | ✅ Tam Yetki | 🚫 Yetkisiz | ✅ Yükler | ✅ Görür |

---

## 6. YETKİSİZ ERİŞİM (403 ACCESS DENIED) GÜVENLİK MODÜLÜ
- Kullanıcı yetkisi olmayan bir modüle doğrudan URL adresi (`#/finans`) veya başka yollarla erişmeye çalıştığında sistem otomatik olarak **"Hata 403 / Yetkisiz Erişim"** uyarı ekranını görüntüler.

---

## 7. TEMİZ ASCII URL YÖNLENDİRME (ROUTING) KURALLARI
URL adreslerinde Türkçe karakter içermeyen temiz ASCII bağlantılar kullanılmıştır:
- `#/anasayfa`, `#/dugun-salonlari`, `#/ek-hizmetler`, `#/rezervasyonlar`, `#/takvim`, `#/kampanyalar`, `#/finans`, `#/musteri-rehberi`, `#/kullanici-yonetimi`, `#/raporlar-ai`, `#/medya-yukle`.

---

## 8. MYSQL VERİTABANI MİMARİSİ (schema.sql)
1. `venues`, `services`, `campaigns`, `customers`, `users`, `reservations`, `reservation_services`, `reservation_flow`, `reservation_media`.

---

## 9. ÇAKIŞMA ÖNLEME (COLLISION CHECK) & ZAMAN DİLİMLERİ
- **Zaman Dilimleri:** `13:00 - 17:00` (Gündüz) ve `19:00 - 23:00` (Gece).
- **MySQL Unique Constraint:** `UNIQUE KEY unique_venue_slot (venue_id, event_date, time_slot)`.

---

## 10. FİNANSAL HESAPLAMALAR, KDV %20 & FATURA OTOMASYONU
- Ara toplam, %20 KDV, kapora ve net bakiye otomasyonu.

---

## 11. OTOMATİK İLETİŞİM & WHATSAPP ENTEGRASYONU
- Doğrudan mesaj bağlantısı (`https://wa.me/...`).

---

## 12. YAPAY ZEKA (AI) DESTEKLİ RAPORLAR VE ÖNERİLER
- Hafta içi doluluk paketleri ve popüler hizmet önerileri.

---
*İrem Düğün Sarayı & Organizasyon Şirketi Mimarisi - Tüm Hakları Saklıdır (2026).*
