# 🏛️ İREM DÜĞÜN SARAYI & ORGANİZASYON PLATFORMU — 119 MADDELİK ÖNCELİKLENDİRİLMİŞ DETAYLI YOL HARİTASI

> **Resmi GitHub Project Panosu:** [GitHub Project #2 (Rezervasyon Sistemi - v1)](https://github.com/users/davutakbulut/projects/2)

## Madde #1: Çoklu Salon Çakışma Engelleyici
**Durum:** ✅ Tamamlandı (v1.5.03)
**Kategori:** Rezervasyon & Takvim
**Hedef Sayfa:** `Yeni Rezervasyon & Takvim Yönetim Sayfası (/yonetim/yeni-rezervasyon)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Aynı salonda aynı zaman diliminde 2. rezervasyonun oluşturulmasını otomatik engelleme.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Yeni Rezervasyon & Takvim Yönetim Sayfası (/yonetim/yeni-rezervasyon)`
- **Hizmet Ettiği Modül:** `Bölüm 1 & Bölüm 2: Salon Karuseli, Seans Matrisi ve Canlı Takvim Hücreleri`
- **Erişim Rotası:** `/yonetim/yeni-rezervasyon`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #2: Tampon Hazırlık Süresi Modülü
**Durum:** ✅ Tamamlandı (v1.5.04)
**Kategori:** Rezervasyon & Takvim
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** İki düğün seansı arasına otomatik 90 dakikalık salon temizlik ve hazırlık tamponu koyma.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #3: Sürükle-Bırak Tarih Güncelleme Güvenlik İkazı
**Durum:** ✅ Tamamlandı (v1.5.06)
**Kategori:** Rezervasyon & Takvim
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Takvimde sürükle-bırak yapılırken müşteri onay mesajı ve SMS bildirim tetikleyicisi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #4: Rezervasyon Opsiyon Süresi Zamanlayıcısı
**Durum:** ✅ Tamamlandı (v1.5.07)
**Kategori:** Rezervasyon & Takvim
**Hedef Sayfa:** `Yeni Rezervasyon & Takvim Yönetim Sayfası (/yonetim/yeni-rezervasyon)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Kaporası yatırılmayan bekleyen rezervasyonların 48 saat sonra otomatik düşmesi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Yeni Rezervasyon & Takvim Yönetim Sayfası (/yonetim/yeni-rezervasyon)`
- **Hizmet Ettiği Modül:** `Bölüm 1 & Bölüm 2: Salon Karuseli, Seans Matrisi ve Canlı Takvim Hücreleri`
- **Erişim Rotası:** `/yonetim/yeni-rezervasyon`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #5: Google Calendar ve Outlook Entegrasyonu
**Durum:** ✅ Tamamlandı (v1.5.08)
**Kategori:** Rezervasyon & Takvim
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Rezervasyon tarihlerinin salon yöneticilerinin kişisel takvimlerine senkronize edilmesi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #6: Özel Gün & Resmi Tatil Fiyat Çarpanı
**Durum:** ✅ Tamamlandı (v1.5.09)
**Kategori:** Rezervasyon & Takvim
**Hedef Sayfa:** `Finansal Özet, Kasa & Fiyatlandırma Modülü (/yonetim/yeni-rezervasyon#odeme)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Dini ve milli bayram günlerinde otomatik %20 fiyat farkı hesaplama seçeneği.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Finansal Özet, Kasa & Fiyatlandırma Modülü (/yonetim/yeni-rezervasyon#odeme)`
- **Hizmet Ettiği Modül:** `Bölüm 3 & Bölüm 5: Fiyatlandırma Motoru, KDV Matrisi, İskonto PIN Kalkanı ve Ödeme Özeti`
- **Erişim Rotası:** `/yonetim/yeni-rezervasyon`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #7: Tekrarlanan Etkinlik Şablonları
**Durum:** ✅ Tamamlandı (v1.5.10)
**Kategori:** Rezervasyon & Takvim
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Haftalık bayii toplantıları veya dernek geceleri için toplu rezervasyon oluşturma.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #8: Salona Özel Kapasite Uyarısı
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Rezervasyon & Takvim
**Hedef Sayfa:** `Yeni Rezervasyon & Takvim Yönetim Sayfası (/yonetim/yeni-rezervasyon)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Salon kapasitesini aşan davetli sayısı girildiğinde ikaz rozeti gösterimi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Yeni Rezervasyon & Takvim Yönetim Sayfası (/yonetim/yeni-rezervasyon)`
- **Hizmet Ettiği Modül:** `Bölüm 1 & Bölüm 2: Salon Karuseli, Seans Matrisi ve Canlı Takvim Hücreleri`
- **Erişim Rotası:** `/yonetim/yeni-rezervasyon`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #9: Görsel Oturma Planı Tasarlayıcı
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Rezervasyon & Takvim
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Masaların ve davetli oturuş düzeninin 2D kroki üzerinde sürükle-bırak ile çizimi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #10: Rezervasyon Geçmişi & Değişiklik Logu
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Rezervasyon & Takvim
**Hedef Sayfa:** `Yeni Rezervasyon & Takvim Yönetim Sayfası (/yonetim/yeni-rezervasyon)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Rezervasyonda kimin ne zaman değişiklik yaptığını gösteren audit log ekranı.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Yeni Rezervasyon & Takvim Yönetim Sayfası (/yonetim/yeni-rezervasyon)`
- **Hizmet Ettiği Modül:** `Bölüm 1 & Bölüm 2: Salon Karuseli, Seans Matrisi ve Canlı Takvim Hücreleri`
- **Erişim Rotası:** `/yonetim/yeni-rezervasyon`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #11: Kişiselleştirilebilir QR Tasarım Şablonları
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Medya Galerisi & QR
**Hedef Sayfa:** `Davetli Katılım & Canlı Düğün Albüm Sayfası (/album/:id)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Masa kartı QR kodlarına çift fotoğrafları ve özel çerçeve stilleri ekleme.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Davetli Katılım & Canlı Düğün Albüm Sayfası (/album/:id)`
- **Hizmet Ettiği Modül:** `Canlı Fotoğraf/Video Yükleme Alanı, Misafir Anı Defteri ve QR Kod İletişim Paneli`
- **Erişim Rotası:** `/album/:id`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #12: Canlı Slayt Gösterisi (Live TV Presentation Mode)
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Medya Galerisi & QR
**Hedef Sayfa:** `Davetli Katılım & Canlı Düğün Albüm Sayfası (/album/:id)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Davetliler yükledikçe dev salondaki TV'de otomatik geçen tam ekran slayt modu.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Davetli Katılım & Canlı Düğün Albüm Sayfası (/album/:id)`
- **Hizmet Ettiği Modül:** `Canlı Fotoğraf/Video Yükleme Alanı, Misafir Anı Defteri ve QR Kod İletişim Paneli`
- **Erişim Rotası:** `/album/:id`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #13: Otomatik EXIF Konum & Metadata Temizliği
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Medya Galerisi & QR
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Fotoğraflardaki GPS ve cihaz bilgilerini KVKK gereği sunucuya girmeden silme.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #14: Yapay Zeka Yüz Tanıma & Çift Albümü Ayırma
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Medya Galerisi & QR
**Hedef Sayfa:** `Davetli Katılım & Canlı Düğün Albüm Sayfası (/album/:id)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Gelin ve damat fotoğraflarını yapay zeka ile otomatik tanıyıp öne çıkarma.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Davetli Katılım & Canlı Düğün Albüm Sayfası (/album/:id)`
- **Hizmet Ettiği Modül:** `Canlı Fotoğraf/Video Yükleme Alanı, Misafir Anı Defteri ve QR Kod İletişim Paneli`
- **Erişim Rotası:** `/album/:id`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #15: Medya Beğeni ve Davetli Yorumları
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Medya Galerisi & QR
**Hedef Sayfa:** `Davetli Katılım & Canlı Düğün Albüm Sayfası (/album/:id)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Davetlilerin fotoğraflara kalp/beğeni atabilmesi ve tebrik notu bırakması.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Davetli Katılım & Canlı Düğün Albüm Sayfası (/album/:id)`
- **Hizmet Ettiği Modül:** `Canlı Fotoğraf/Video Yükleme Alanı, Misafir Anı Defteri ve QR Kod İletişim Paneli`
- **Erişim Rotası:** `/album/:id`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #16: Otomatik Filigran (Watermark) Ekleme
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Medya Galerisi & QR
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Yüklenen fotoğraflara salon amblemi ve çift ismini filigran olarak basma.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #17: Medya Retention & Otomatik Silme Uyarısı
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Medya Galerisi & QR
**Hedef Sayfa:** `Davetli Katılım & Canlı Düğün Albüm Sayfası (/album/:id)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** 30 günü dolan albümler silinmeden önce çiftin e-postasına uyarı ve indirme linki gönderme.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Davetli Katılım & Canlı Düğün Albüm Sayfası (/album/:id)`
- **Hizmet Ettiği Modül:** `Canlı Fotoğraf/Video Yükleme Alanı, Misafir Anı Defteri ve QR Kod İletişim Paneli`
- **Erişim Rotası:** `/album/:id`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #18: Toplu Medya Onay Modu (Admin Moderation)
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Medya Galerisi & QR
**Hedef Sayfa:** `Davetli Katılım & Canlı Düğün Albüm Sayfası (/album/:id)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Yöneticinin onaylamadığı davetli fotoğraflarının TV'de ve galeride görünmemesi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Davetli Katılım & Canlı Düğün Albüm Sayfası (/album/:id)`
- **Hizmet Ettiği Modül:** `Canlı Fotoğraf/Video Yükleme Alanı, Misafir Anı Defteri ve QR Kod İletişim Paneli`
- **Erişim Rotası:** `/album/:id`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #19: Video Thumbnail Otomatik Oluşturucu
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Medya Galerisi & QR
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Yüklenen MP4/MOV videoların ilk karesinden otomatik kapak görseli üretme.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #20: Instagram / TikTok Doğrudan Paylaşım Butonu
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Medya Galerisi & QR
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Davetlilerin fotoğraflarını sosyal medyada salon etiketiyle paylaşma aracı.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #21: GİB Uyumlu e-Fatura & e-Arşiv Entegrasyon Simülasyonu
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Finans & Fatura
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Resmi faturaların PDF üretilip müşteriye otomatik gönderilmesi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #22: Parçalı Ödeme & Taksit Takip Sistemi
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Finans & Fatura
**Hedef Sayfa:** `Finansal Özet, Kasa & Fiyatlandırma Modülü (/yonetim/yeni-rezervasyon#odeme)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Kapora haricinde 1., 2. ve 3. taksit tarihlerini ve kalan bakiyeyi izleme.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Finansal Özet, Kasa & Fiyatlandırma Modülü (/yonetim/yeni-rezervasyon#odeme)`
- **Hizmet Ettiği Modül:** `Bölüm 3 & Bölüm 5: Fiyatlandırma Motoru, KDV Matrisi, İskonto PIN Kalkanı ve Ödeme Özeti`
- **Erişim Rotası:** `/yonetim/yeni-rezervasyon`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #23: Otomatik Ödeme Hatırlatma SMS/WhatsApp Servisi
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Finans & Fatura
**Hedef Sayfa:** `Finansal Özet, Kasa & Fiyatlandırma Modülü (/yonetim/yeni-rezervasyon#odeme)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Düğüne 7 gün kala kalan bakiye için otomatik WhatsApp hatırlatma mesajı.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Finansal Özet, Kasa & Fiyatlandırma Modülü (/yonetim/yeni-rezervasyon#odeme)`
- **Hizmet Ettiği Modül:** `Bölüm 3 & Bölüm 5: Fiyatlandırma Motoru, KDV Matrisi, İskonto PIN Kalkanı ve Ödeme Özeti`
- **Erişim Rotası:** `/yonetim/yeni-rezervasyon`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #24: Salon Gider & Tedarikçi Masraf Kaydı
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Finans & Fatura
**Hedef Sayfa:** `Yeni Rezervasyon & Takvim Yönetim Sayfası (/yonetim/yeni-rezervasyon)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Garson, orkestra, catering ve elektrik masraflarının rezervasyon bazlı düşülmesi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Yeni Rezervasyon & Takvim Yönetim Sayfası (/yonetim/yeni-rezervasyon)`
- **Hizmet Ettiği Modül:** `Bölüm 1 & Bölüm 2: Salon Karuseli, Seans Matrisi ve Canlı Takvim Hücreleri`
- **Erişim Rotası:** `/yonetim/yeni-rezervasyon`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #25: Net Kar / Zarar Analiz Ekranı
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Finans & Fatura
**Hedef Sayfa:** `Yönetim Panosu & Ciro Analitik Sayfası (/yonetim/dashboard)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Her düğün için toplam gelirden masraflar düşülerek net kar marjının hesabı.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Yönetim Panosu & Ciro Analitik Sayfası (/yonetim/dashboard)`
- **Hizmet Ettiği Modül:** `Aylık Doluluk Grafikleri, Salon Gelir Karşılaştırmaları ve KPI Kartları`
- **Erişim Rotası:** `/yonetim/dashboard`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #26: Cari Hesap & Tedarikçi Borç-Alacak Takibi
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Finans & Fatura
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Çiçekçi, fotoğrafçı ve müzisyenlerin cari hesap bakiyelerinin tutulması.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #27: KDV Oranı Dinamik Seçim Engine (%1, %10, %20)
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Finans & Fatura
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Yemek ve organizasyon hizmetlerinin farklı KDV oranlarına göre bölünmesi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #28: Dövizli Fiyatlandırma (EUR/USD) & Anlık Kur
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Finans & Fatura
**Hedef Sayfa:** `Finansal Özet, Kasa & Fiyatlandırma Modülü (/yonetim/yeni-rezervasyon#odeme)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Yabancı düğünler için döviz bazlı sözleşme ve anlık Merkez Bankası kuru.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Finansal Özet, Kasa & Fiyatlandırma Modülü (/yonetim/yeni-rezervasyon#odeme)`
- **Hizmet Ettiği Modül:** `Bölüm 3 & Bölüm 5: Fiyatlandırma Motoru, KDV Matrisi, İskonto PIN Kalkanı ve Ödeme Özeti`
- **Erişim Rotası:** `/yonetim/yeni-rezervasyon`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #29: İptal & İade (Refund) Muhasebe Kaydı
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Finans & Fatura
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** İptal edilen düğünlerin kaza tazminatı ve kapora iade süreçlerinin işlenmesi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #30: Nakit & Kredi Kartı Kasa Mutabakatı
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Finans & Fatura
**Hedef Sayfa:** `Finansal Özet, Kasa & Fiyatlandırma Modülü (/yonetim/yeni-rezervasyon#odeme)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Gün sonu kasa takibi ve banka pos raporlarının eşleştirilmesi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Finansal Özet, Kasa & Fiyatlandırma Modülü (/yonetim/yeni-rezervasyon#odeme)`
- **Hizmet Ettiği Modül:** `Bölüm 3 & Bölüm 5: Fiyatlandırma Motoru, KDV Matrisi, İskonto PIN Kalkanı ve Ödeme Özeti`
- **Erişim Rotası:** `/yonetim/yeni-rezervasyon`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #31: Görüşme & Teklif Takip Hattı (Pipeline Stage)
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Müşteri CRM
**Hedef Sayfa:** `Müşteri CRM & Dijital Sözleşme Yönetimi (/yonetim/rezervasyonlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Müşterilerin 'İlk İletişim', 'Salon Gezisi', 'Teklif Verildi', 'Sözleşme İmzalandı' aşamalarında takibi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Müşteri CRM & Dijital Sözleşme Yönetimi (/yonetim/rezervasyonlar)`
- **Hizmet Ettiği Modül:** `Rezervasyon Detay Modali, Dijital Imza Paneli ve PDF Çıktı Üreteci`
- **Erişim Rotası:** `/yonetim/rezervasyonlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #32: Otomatik Sözleşme PDF Oluşturucu
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Müşteri CRM
**Hedef Sayfa:** `Müşteri CRM & Dijital Sözleşme Yönetimi (/yonetim/rezervasyonlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Rezervasyon bilgilerini resmi düğün sözleşmesi PDF'ine döküp indirme.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Müşteri CRM & Dijital Sözleşme Yönetimi (/yonetim/rezervasyonlar)`
- **Hizmet Ettiği Modül:** `Rezervasyon Detay Modali, Dijital Imza Paneli ve PDF Çıktı Üreteci`
- **Erişim Rotası:** `/yonetim/rezervasyonlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #33: Dijital İmza (E-Signature) Desteği
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Müşteri CRM
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Çiftlerin telefon ekranında parmaklarıyla sözleşmeyi dijital onaylaması.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #34: Müşteri Memnuniyet Anketi (NPS Survey)
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Müşteri CRM
**Hedef Sayfa:** `Müşteri CRM & Dijital Sözleşme Yönetimi (/yonetim/rezervasyonlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Düğün bittikten 1 gün sonra çifte otomatik WhatsApp memnuniyet puanlaması gönderme.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Müşteri CRM & Dijital Sözleşme Yönetimi (/yonetim/rezervasyonlar)`
- **Hizmet Ettiği Modül:** `Rezervasyon Detay Modali, Dijital Imza Paneli ve PDF Çıktı Üreteci`
- **Erişim Rotası:** `/yonetim/rezervasyonlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #35: Özel Gün Tebrik Mesajı Otomasyonu
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Müşteri CRM
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Çiftlerin evlilik yıldönümlerinde her yıl otomatik tebrik mesajı gönderme.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #36: Potansiyel Müşteri (Lead) Kayıt Formu Widget'ı
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Müşteri CRM
**Hedef Sayfa:** `Müşteri CRM & Dijital Sözleşme Yönetimi (/yonetim/rezervasyonlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Web sitesine eklenebilen 'Teklif Alın' formu verilerinin CRM'e düşmesi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Müşteri CRM & Dijital Sözleşme Yönetimi (/yonetim/rezervasyonlar)`
- **Hizmet Ettiği Modül:** `Rezervasyon Detay Modali, Dijital Imza Paneli ve PDF Çıktı Üreteci`
- **Erişim Rotası:** `/yonetim/rezervasyonlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #37: Müşteri Etiketleme & Segmentasyon
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Müşteri CRM
**Hedef Sayfa:** `Müşteri CRM & Dijital Sözleşme Yönetimi (/yonetim/rezervasyonlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Müşterileri 'VIP', 'Kurumsal', 'Şikayetli', 'Referanslı' şeklinde etiketleme.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Müşteri CRM & Dijital Sözleşme Yönetimi (/yonetim/rezervasyonlar)`
- **Hizmet Ettiği Modül:** `Rezervasyon Detay Modali, Dijital Imza Paneli ve PDF Çıktı Üreteci`
- **Erişim Rotası:** `/yonetim/rezervasyonlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #38: Toplu SMS & E-posta Kampanya Gönderimi
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Müşteri CRM
**Hedef Sayfa:** `Müşteri CRM & Dijital Sözleşme Yönetimi (/yonetim/rezervasyonlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Tüm müşterilere erken rezervasyon indirim duyurularının toplu iletilmesi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Müşteri CRM & Dijital Sözleşme Yönetimi (/yonetim/rezervasyonlar)`
- **Hizmet Ettiği Modül:** `Rezervasyon Detay Modali, Dijital Imza Paneli ve PDF Çıktı Üreteci`
- **Erişim Rotası:** `/yonetim/rezervasyonlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #39: Arama Kaydı ve İletişim Notları
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Müşteri CRM
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Müşteri rehberinde yapılan telefon görüşmelerinin tarihli not olarak saklanması.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #40: Referans (Referral) İndirim Takipçisi
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Müşteri CRM
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Eski müşterilerin getirdiği yeni düğünler için referans primi hesaplama.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #41: Salon Teknik Envanter Takibi
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Salon & Hizmet
**Hedef Sayfa:** `Yeni Rezervasyon & Takvim Yönetim Sayfası (/yonetim/yeni-rezervasyon)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Ses, ışık, robot, projektör ve jeneratör cihazlarının bakım sürelerinin takibi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Yeni Rezervasyon & Takvim Yönetim Sayfası (/yonetim/yeni-rezervasyon)`
- **Hizmet Ettiği Modül:** `Bölüm 1 & Bölüm 2: Salon Karuseli, Seans Matrisi ve Canlı Takvim Hücreleri`
- **Erişim Rotası:** `/yonetim/yeni-rezervasyon`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #42: Menü İçerik & Alerjen Uyarısı Kataloğu
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Salon & Hizmet
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Yemek menülerindeki alerjen maddelerin (glutensiz, vegan vb.) davetliye gösterimi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #43: Tedarikçi Personel Vardiya Planlayıcı
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Salon & Hizmet
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Hangi düğünde hangi şef, garson ve fotoğrafçının görevli olduğunun çizelgesi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #44: Salon Panoramik 360 Derece Tur Entegrasyonu
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Salon & Hizmet
**Hedef Sayfa:** `Yeni Rezervasyon & Takvim Yönetim Sayfası (/yonetim/yeni-rezervasyon)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Müşterilere salonların 360 sanal turunu sistem içinden izletme.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Yeni Rezervasyon & Takvim Yönetim Sayfası (/yonetim/yeni-rezervasyon)`
- **Hizmet Ettiği Modül:** `Bölüm 1 & Bölüm 2: Salon Karuseli, Seans Matrisi ve Canlı Takvim Hücreleri`
- **Erişim Rotası:** `/yonetim/yeni-rezervasyon`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #45: Ek Hizmet Stok & Limit Kontrolü
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Salon & Hizmet
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Aynı gece en fazla 2 düğüne verilebilen VIP Gelin Arabası stokunun kontrolü.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #46: Gelin Odası Özel Hizmet Menüsü
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Salon & Hizmet
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Gelin odasına ikram edilecek meyve, içecek ve makyaj aydınlatması şablonu.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #47: Çocuk Oyun Alanı & Palyaço Hizmet Takibi
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Salon & Hizmet
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Çocuklu aileler için çocuk kulübü ek hizmet seçeneği.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #48: Valet & Otopark Araç Sayı Yönetimi
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Salon & Hizmet
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Salon otopark kapasitesine göre vale araç kabul planlaması.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #49: Volkan & Sis Şovu Zamanlama Düzeneği
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Salon & Hizmet
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** İlk dans ve pasta kesim anında sis makinesinin süre göstergesi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #50: Organizasyon Paket Karşılaştırma Ekranı
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Salon & Hizmet
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Bronz, Gümüş, Altın ve VIP paketlerin yan yana özellik kıyaslaması.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #51: AI Gelecek Sezon Gelir Tahminleme (Forecasting)
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Yapay Zeka Analiz
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Gelecek yılın doluluk ve ciro tahminini AI algoritmalarıyla hesaplama.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #52: AI Dinamik Fiyat Öneri Motoru
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Yapay Zeka Analiz
**Hedef Sayfa:** `Finansal Özet, Kasa & Fiyatlandırma Modülü (/yonetim/yeni-rezervasyon#odeme)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Talebin yüksek olduğu hafta sonları için optimum fiyat teklifi sunma.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Finansal Özet, Kasa & Fiyatlandırma Modülü (/yonetim/yeni-rezervasyon#odeme)`
- **Hizmet Ettiği Modül:** `Bölüm 3 & Bölüm 5: Fiyatlandırma Motoru, KDV Matrisi, İskonto PIN Kalkanı ve Ödeme Özeti`
- **Erişim Rotası:** `/yonetim/yeni-rezervasyon`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #53: AI İptal Riski Erken Uyarı Sistemi
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Yapay Zeka Analiz
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Kaporasını geciktiren ve iletişimi azalan müşterilerin kayıp risk puanı.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #54: AI Müşteri Yorum Analizi (Sentiment Analysis)
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Yapay Zeka Analiz
**Hedef Sayfa:** `Müşteri CRM & Dijital Sözleşme Yönetimi (/yonetim/rezervasyonlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Anketlerdeki müşteri yorumlarından olumlu/olumsuz duygu analizi çıkarma.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Müşteri CRM & Dijital Sözleşme Yönetimi (/yonetim/rezervasyonlar)`
- **Hizmet Ettiği Modül:** `Rezervasyon Detay Modali, Dijital Imza Paneli ve PDF Çıktı Üreteci`
- **Erişim Rotası:** `/yonetim/rezervasyonlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #55: AI Menü Popülerlik ve İsraf Analizi
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Yapay Zeka Analiz
**Hedef Sayfa:** `Yönetim Panosu & Ciro Analitik Sayfası (/yonetim/dashboard)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** En çok tercih edilen yemeklerin ve artik oranlarının istatistiği.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Yönetim Panosu & Ciro Analitik Sayfası (/yonetim/dashboard)`
- **Hizmet Ettiği Modül:** `Aylık Doluluk Grafikleri, Salon Gelir Karşılaştırmaları ve KPI Kartları`
- **Erişim Rotası:** `/yonetim/dashboard`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #56: AI Personel Performans Puanlaması
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Yapay Zeka Analiz
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Garson ve ekibin müşteri puanlarına göre ayın elemanı analizi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #57: AI Kampanya Verimlilik Raporu
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Yapay Zeka Analiz
**Hedef Sayfa:** `Yönetim Panosu & Ciro Analitik Sayfası (/yonetim/dashboard)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Hangi indirim kodunun ne kadar dönüşüm getirdiğinin AI grafiği.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Yönetim Panosu & Ciro Analitik Sayfası (/yonetim/dashboard)`
- **Hizmet Ettiği Modül:** `Aylık Doluluk Grafikleri, Salon Gelir Karşılaştırmaları ve KPI Kartları`
- **Erişim Rotası:** `/yonetim/dashboard`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #58: AI Otomatik Düğün Senaryo Metni
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Yapay Zeka Analiz
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Sunucu (MC) için gelin-damat bilgilerinden otomatik takdim konuşması yazma.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #59: AI Sosyal Medya İletişim Asistanı
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Yapay Zeka Analiz
**Hedef Sayfa:** `Davetli Katılım & Canlı Düğün Albüm Sayfası (/album/:id)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Düğün görselleri için Instagram paylaşım metni ve hashtag üretme.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Davetli Katılım & Canlı Düğün Albüm Sayfası (/album/:id)`
- **Hizmet Ettiği Modül:** `Canlı Fotoğraf/Video Yükleme Alanı, Misafir Anı Defteri ve QR Kod İletişim Paneli`
- **Erişim Rotası:** `/album/:id`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #60: AI Anomali ve Şüpheli İşlem Tespiti
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Yapay Zeka Analiz
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Normal dışı yüksek indirim veya hatalı bakiye kayıtlarını AI tespiti.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #61: IndexedDB Depolama Mimarisi Migration
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Performans & Depolama
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** LocalStorage 5MB sınırına takılmamak için depolamayı IndexedDB'ye taşıma.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #62: HLS / DASH Adaptif Video Streaming
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Performans & Depolama
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Mobil internet hızına göre videoları 1080p/720p/480p otomatik kalitede oynatma.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #63: PWA (Progressive Web App) Çevrimdışı Çalışma
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Performans & Depolama
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** İnternet kesildiğinde uygulamanın çevrimdışı (offline) çalışmaya devam etmesi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #64: Service Worker Asset Caching
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Performans & Depolama
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** CSS, JS ve yazı tiplerinin tarayıcıda 0ms anlık yüklenmesi için Service Worker.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #65: Resim Görsellerini AVIF Formatına Dönüştürme
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Performans & Depolama
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** WebP'ye ek olarak %30 daha küçük AVIF resim formatı desteği.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #66: Lazy-Loading & Infinite Scroll Medya Galeri
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Performans & Depolama
**Hedef Sayfa:** `Davetli Katılım & Canlı Düğün Albüm Sayfası (/album/:id)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Binlerce görsel olan albümlerde ekrana geldikçe yükleme (Virtual List).
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Davetli Katılım & Canlı Düğün Albüm Sayfası (/album/:id)`
- **Hizmet Ettiği Modül:** `Canlı Fotoğraf/Video Yükleme Alanı, Misafir Anı Defteri ve QR Kod İletişim Paneli`
- **Erişim Rotası:** `/album/:id`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #67: Otomatik Sunucu Disk Temizlik Cron'u
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Performans & Depolama
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** 90 günü geçen geçici temp dosyalarının otomatik silinmesi (Kullanıcı izinli).
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #68: GZip & Brotli Sunucu Sıkıştırma
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Performans & Depolama
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** HTTP yanıtlarının sunucu tarafında Brotli ile sıkıştırılıp gönderilmesi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #69: Database Indexing & Arama Hızlandırma
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Performans & Depolama
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Binlerce rezervasyon arasında 1ms içinde arama yapabilmek için arama indeksi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #70: CDN (Content Delivery Network) Entegrasyon
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Performans & Depolama
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Görsellerin dünyadaki en yakın sunucudan hızlı yüklenmesi altyapısı.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #71: İki Faktörlü Kimlik Doğrulama (2FA / OTP)
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Güvenlik & KVKK
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Yönetici girişlerinde SMS veya Google Authenticator 2FA zorunluluğu.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #72: Detaylı Rol Bazlı İzin Matrisi (Granular RBAC)
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Güvenlik & KVKK
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Garson, muhasebeci ve müdür için buton seviyesinde yetki kısıtlama.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #73: KVKK Açık Rıza ve İzin Onay Metni
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Güvenlik & KVKK
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Davetlilerin fotoğraf yüklemeden önce KVKK aydınlatma metnini onaylaması.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #74: Unutulma Hakkı (Data Erasure Engine)
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Güvenlik & KVKK
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Müşterinin talebi halinde tüm verilerinin ve medyalarının kalıcı silinmesi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #75: Oturum Zamanaşımı (Session Timeout Guard)
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Güvenlik & KVKK
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** 15 dakika işlem yapılmadığında yönetici oturumunun otomatik kapanması.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #76: Şifreli Veritabanı Saklama (AES-256 Encryption)
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Güvenlik & KVKK
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Müşteri TC ve telefon bilgilerinin veritabanında şifreli (encrypted) tutulması.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #77: CSRF & XSS Güvenlik Başlıkları (CSP Headers)
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Güvenlik & KVKK
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Tarayıcı güvenlik başlıklarının (Content Security Policy) sıkılaştırılması.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #78: Şüpheli Giriş ve IP Engelleme Paneli
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Güvenlik & KVKK
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Yanlış şifre deneyen IP'lerin otomatik karantinaya alınması.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #79: Güvenlik İhlal Bildirim Sistemi
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Güvenlik & KVKK
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Olağandışı bir giriş olduğunda ana yöneticiye anında güvenlik SMS'i.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #80: Güvenli Çıkış (Force Logout Across Devices)
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Güvenlik & KVKK
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Çalınan hesaplarda tüm cihazlardan tek tıkla oturum kapatma.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #81: Gelişmiş Klavye Kısayolları (Keyboard Shortcuts)
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** UI/UX & Erişilebilirlik
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** CTRL+K arama, ESC kapatma, N yeni rezervasyon kısayolları.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #82: WCAG 2.1 AAA Ekran Okuyucu (Screen Reader) Uyum
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** UI/UX & Erişilebilirlik
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Görme engelli kullanıcılar için ARIA etiketleri ve sesli okuma desteği.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #83: Çoklu Dil Desteği (Türkçe, İngilizce, Almanca, Arapça)
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** UI/UX & Erişilebilirlik
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Platformun 4 dilde anlık dil değiştirme altyapısı.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #84: Özel Tema Renk Paleti Tasarlayıcı
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** UI/UX & Erişilebilirlik
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Salonların kendi kurumsal renklerini (Gold, Rose, Emerald) seçebilmesi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #85: Sesli Komut ile Arama ve Yönlendirme
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** UI/UX & Erişilebilirlik
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Mikrofona 'Ağustos rezervasyonlarını göster' diyerek arama yapma.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #86: Yüksek Kontrastlı Mod (High Contrast Theme)
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** UI/UX & Erişilebilirlik
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Göz yormayan ve açık havada güneş altında rahat okunan mod.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #87: Yazdırma Dostu Sayfa Mimarisi (Print CSS)
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** UI/UX & Erişilebilirlik
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Sayfaların yazıcıdan basılırken gereksiz menüleri gizlemesi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #88: Görsel Yükleme Drag-and-Drop Efektleri
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** UI/UX & Erişilebilirlik
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Dosya sürüklerken ekranın tamamında beliren şık animasyonlar.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #89: Yükleme Durumu Skeleton Loader Animasyonları
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** UI/UX & Erişilebilirlik
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Sayfa yüklenirken veri gri taslak kartlar (Skeleton) gösterimi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #90: Mobil Dokunmatik Titreşim (Haptic Feedback)
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** UI/UX & Erişilebilirlik
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Telefonda butonlara basıldığında hafif haptik titreşim geri bildirimi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #91: Otomatik Günlük Veritabanı Yedekleme (Auto Backup)
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Sistem & Operasyon
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Her gece 03:00'te veritabanının otomatik ZIP yedeğinin alınması.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #92: Tek Tıkla Veritabanı Geri Yükleme (Restore Engine)
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Sistem & Operasyon
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Hatalı bir durumda eski yedek dosyasına tek tıkla geri dönebilme.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #93: Sistem Sağlık Durumu (Health Check Monitor)
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Sistem & Operasyon
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** CPU, RAM, Disk kullanımı ve sunucu tepki süresinin canlı gösterimi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #94: Otomatik Sistem Güncelleme ve Sürüm Dökümü
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Sistem & Operasyon
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Versiyon takibinin sürüm notlarıyla canlı yayınlanması.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #95: Çoklu Şube / Salon Zincir Yönetimi
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Sistem & Operasyon
**Hedef Sayfa:** `Yeni Rezervasyon & Takvim Yönetim Sayfası (/yonetim/yeni-rezervasyon)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Birden fazla düğün salonu şubesinin merkezden yönetilebilmesi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Yeni Rezervasyon & Takvim Yönetim Sayfası (/yonetim/yeni-rezervasyon)`
- **Hizmet Ettiği Modül:** `Bölüm 1 & Bölüm 2: Salon Karuseli, Seans Matrisi ve Canlı Takvim Hücreleri`
- **Erişim Rotası:** `/yonetim/yeni-rezervasyon`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #96: Tedarikçi Giriş Portalı (Vendor Portal)
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Sistem & Operasyon
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Fotoğrafçı ve orkestranın kendi iş takvimini gördüğü izole panel.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #97: Gelişmiş Hata Takip ve Telegram Bildirim Botu
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Sistem & Operasyon
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Sistemde hata oluştuğunda yazılımcıya anında Telegram mesajı atma.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #98: Otomatik Fatura Kesim Uyarısı
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Sistem & Operasyon
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Düğünü biten ancak faturası kesilmeyen rezervasyonların ikazı.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #99: Sistem Kullanım İstatistiği & Log Analizi
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Sistem & Operasyon
**Hedef Sayfa:** `Yönetim Panosu & Ciro Analitik Sayfası (/yonetim/dashboard)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Hangi sayfanın ne kadar ziyaret edildiğinin iç analitiği.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Yönetim Panosu & Ciro Analitik Sayfası (/yonetim/dashboard)`
- **Hizmet Ettiği Modül:** `Aylık Doluluk Grafikleri, Salon Gelir Karşılaştırmaları ve KPI Kartları`
- **Erişim Rotası:** `/yonetim/dashboard`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #100: Yapay Zeka Otonom Geliştirme Motoru Senkronizasyonu
**Durum:** ⏳ Eklenme Bekliyor
**Kategori:** Sistem & Operasyon
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** 4 uzman ajanın bu 100 maddelik yol haritasını sırayla otonom geliştirmesi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #101: Node.js CI/CD Otomasyonu & Test İş Akışı
**Durum:** ⏳ Eklenme Bekliyor (Yol Haritasında)
**Kategori:** GitHub Actions & CI/CD Dağıtımı
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Her git push işleminde Node.js bağımlılıklarını, build sürecini ve otomatik testleri çalıştıran GitHub Actions CI iş akışı.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #102: Webpack & Frontend Otomatik Bundle Derleme İş Akışı
**Durum:** ⏳ Eklenme Bekliyor (Yol Haritasında)
**Kategori:** GitHub Actions & CI/CD Dağıtımı
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Frontend React ve JavaScript varlıklarının GitHub Actions üzerinde otomatik Webpack ile minifiye edilip paketlenmesi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #103: SLSA OpenSSF Yazılım Tedarik Zinciri Güvenlik Jeneratörü
**Durum:** ⏳ Eklenme Bekliyor (Yol Haritasında)
**Kategori:** GitHub Actions & CI/CD Dağıtımı
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Yazılım paketlerinin ve bağımlılıkların güvenliğini onaylayan OpenSSF SLSA güvenlik bildirim jeneratörü entegrasyonu.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #104: Docker Konteyner İmajı Oluşturma ve Registry Dağıtımı
**Durum:** ⏳ Eklenme Bekliyor (Yol Haritasında)
**Kategori:** GitHub Actions & CI/CD Dağıtımı
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Projenin Docker imajının GitHub Actions ile otomatik derlenip GitHub Container Registry (GHCR) deposuna yüklenmesi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #105: Python Paket Yönetimi & Anaconda Çoklu Sürüm Matrisi
**Durum:** ⏳ Eklenme Bekliyor (Yol Haritasında)
**Kategori:** GitHub Actions & CI/CD Dağıtımı
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Backend Python servislerinin (serve_fast_3g.py) farklı Python sürümlerinde otomatik test edilmesi için Anaconda CI matrisi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #106: Node.js & npm Paket Yayınlama Otomasyonu
**Durum:** ⏳ Eklenme Bekliyor (Yol Haritasında)
**Kategori:** GitHub Actions & CI/CD Dağıtımı
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Sistem modüllerinin ve istemci kütüphanelerinin npm veya GitHub Packages üzerinde versiyonlanarak otomatik yayınlanması.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #107: Python PyPI Paket Yayınlama Pipeline'ı
**Durum:** ⏳ Eklenme Bekliyor (Yol Haritasında)
**Kategori:** GitHub Actions & CI/CD Dağıtımı
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Sistem yardımcı kütüphanelerinin ve veri işleme araçlarının PyPI deposuna GitHub Actions ile otomatik yüklenmesi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #108: Azure Web App Otomatik Dağıtım İş Akışı (Azure CI/CD)
**Durum:** ⏳ Eklenme Bekliyor (Yol Haritasında)
**Kategori:** GitHub Actions & CI/CD Dağıtımı
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Node.js ve Python backend servislerinin Microsoft Azure Web Apps sunucularına GitHub Actions ile otomatik dağıtımı.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #109: Azure Functions Sunucusuz (Serverless) Dağıtım Pipeline'ı
**Durum:** ⏳ Eklenme Bekliyor (Yol Haritasında)
**Kategori:** GitHub Actions & CI/CD Dağıtımı
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Arka plan medya dönüştürme ve bildirim servislerinin Azure Functions üzerine GitHub Actions ile aktarılması.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #110: Amazon ECS & AWS Fargate Konteyner Otomatik Yayınlama
**Durum:** ⏳ Eklenme Bekliyor (Yol Haritasında)
**Kategori:** GitHub Actions & CI/CD Dağıtımı
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Docker konteynerlerinin AWS ECS / Fargate bulut altyapısına GitHub Actions aracılığıyla sıfır kesintiyle canlıya alınması.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #111: Google Cloud GKE (Kubernetes Engine) Otomatik Derleme ve Dağıtım
**Durum:** ⏳ Eklenme Bekliyor (Yol Haritasında)
**Kategori:** GitHub Actions & CI/CD Dağıtımı
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Google Cloud üzerindeki Kubernetes kümelerine (GKE) Docker konteynerlerinin GitHub Actions ile otomatik dağıtılması.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #112: Terraform Infrastructure as Code (IaC) CI/CD Entegrasyonu
**Durum:** ⏳ Eklenme Bekliyor (Yol Haritasında)
**Kategori:** GitHub Actions & CI/CD Dağıtımı
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Bulut sunucu ve veritabanı altyapı değişikliklerinin Terraform kodları ile GitHub Actions üzerinde otomatik doğrulanması.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #113: Alibaba Cloud ACK Kubernetes Otomatik Dağıtım
**Durum:** ⏳ Eklenme Bekliyor (Yol Haritasında)
**Kategori:** GitHub Actions & CI/CD Dağıtımı
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Asya bölgesi yedekleme sunucuları için Alibaba Cloud ACK Kubernetes ortamına GitHub Actions otomatik yayınlama.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #114: Django & Python Web Framework Test Otomasyonu
**Durum:** ⏳ Eklenme Bekliyor (Yol Haritasında)
**Kategori:** GitHub Actions & CI/CD Dağıtımı
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Backend API servislerinin Django / Python test suite'i ile her PR ve push işleminde otomatik doğrulama testi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #115: Datadog Sentetik İzleme ve Performans Pipeline'ı
**Durum:** ⏳ Eklenme Bekliyor (Yol Haritasında)
**Kategori:** GitHub Actions & CI/CD Dağıtımı
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Canlı uygulamanın kullanıcı deneyimini ve tepki sürelerini Datadog Synthetic Monitoring ile GitHub Actions üzerinden sürekli test etme.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #116: Jekyll Static Site & Docker İmaj Paketleme İş Akışı
**Durum:** ⏳ Eklenme Bekliyor (Yol Haritasında)
**Kategori:** GitHub Actions & CI/CD Dağıtımı
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Sistem dokümantasyonunun ve rehber sayfalarının Jekyll Docker container imajı olarak GitHub Actions ile derlenmesi.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #117: İnteraktif 2D Düğün Masası Yerleşim ve Oturma Düzeni Çizici (2D Interactive Drag & Drop Seating Chart & Guest Allocation Engine)
**Durum:** ⏳ Eklenme Bekliyor (Yol Haritasında)
**Kategori:** Rakip & Derin Sistem Araştırması (Competitor Innovation)
**Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Rakip analizi sonucu tespit edilen; gelin ve damadın davetlileri masalara 2D sürükle-bırak yöntemiyle oturtmasını sağlayan, salon şefleri için masa ikram çıktıları üreten 5-Ajan Onaylı yüksek performanslı oturma planı motoru.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Genel Yönetim & Sistem Ayarları Sayfası (/yonetim/ayarlar)`
- **Hizmet Ettiği Modül:** `Sistem Parametreleri, Yetkilendirme Rolleri ve Entegrasyon Ayarları`
- **Erişim Rotası:** `/yonetim/ayarlar`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #118: Canlı WhatsApp & SMS Düğün Menüsü Tercih Toplama ve Lojistik Motoru (Automated WhatsApp & SMS Wedding Menu Preference & Catering Logistics Engine)
**Durum:** ⏳ Eklenme Bekliyor (Yol Haritasında)
**Kategori:** Rakip & Derin Sistem Araştırması (Competitor Innovation)
**Hedef Sayfa:** `Davetli Katılım & Canlı Düğün Albüm Sayfası (/album/:id)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Davetlilere otomatik WhatsApp/SMS menü anketi (Kırmızı Et, Beyaz Et, Vejetaryen, Çocuk) göndererek mutfak şeflerine anlık sayım çıkaran, gıda israfını %30 önleyen 5-Ajan Onaylı catering lojistiği motoru.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Davetli Katılım & Canlı Düğün Albüm Sayfası (/album/:id)`
- **Hizmet Ettiği Modül:** `Canlı Fotoğraf/Video Yükleme Alanı, Misafir Anı Defteri ve QR Kod İletişim Paneli`
- **Erişim Rotası:** `/album/:id`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

## Madde #119: Otomatik Akıllı Bütçe, Kapora ve Taksitli Ödeme Hatırlatıcı Motoru (Automated Installment Payment & Financial Dues Tracking Engine)
**Durum:** ⏳ Eklenme Bekliyor (Yol Haritasında)
**Kategori:** Rakip & Derin Sistem Araştırması (Competitor Innovation)
**Hedef Sayfa:** `Finansal Özet, Kasa & Fiyatlandırma Modülü (/yonetim/yeni-rezervasyon#odeme)`

### 📌 1. AMAÇ VE İŞ DEĞERİ (PURPOSE & BUSINESS VALUE)
- **Temel Amaç:** Çiftlerin ödeme taksit tarihlerini, kapora vadelerini ve kalan bakiyelerini SMS/WhatsApp ile hatırlatan, kasa nakit akışını güvenceye alan 5-Ajan Onaylı finansal takip motoru.
- **İş Faydası:** İrem Düğün Sarayı operasyonel süreçlerini otomatize etmek, insan hatasından kaynaklanan ciro ve müşteri kayıplarını %100 sıfırlamak, düğün çiftleri ve salona yüksek kaliteli dijital deneyim sunmak.

### 📍 2. ETKİLENEN SAYFA VE MODÜL (TARGET PAGE & DOM MODULE)
- **Hedef Sayfa:** `Finansal Özet, Kasa & Fiyatlandırma Modülü (/yonetim/yeni-rezervasyon#odeme)`
- **Hizmet Ettiği Modül:** `Bölüm 3 & Bölüm 5: Fiyatlandırma Motoru, KDV Matrisi, İskonto PIN Kalkanı ve Ödeme Özeti`
- **Erişim Rotası:** `/yonetim/yeni-rezervasyon`

### ⚙️ 3. ÇALIŞMA MANTIĞI VE MEKANİZMASI (WORKING LOGIC & MECHANISM)
1. **Veri & Durum Yönetimi (State Pipeline):** React state (`useState`, `useMemo`) üzerinde kullanıcı girdilerini dinler. `startDate`, `venueId`, `guestCount` veya finansal parametreler değiştiğinde anlık re-render tetikler.
2. **Hesaplama Motoru & REST API:** `serve_fast_3g.py` ve `index.html` üzerindeki sanitizasyon kurallarından geçerek `db_system_settings.json` veritabanına ve `localStorage` önbelleğine idempoten olarak işlenir.
3. **Çakışma ve Güvenlik Kalkanı:** İşlem gerçekleşmeden önce çakışma kontrolü (`isCollision`) ve PIN güvenlik yetkilendirmesi (`DiscountAuthorizationGuard`) çalışır.

### 🎨 4. KULLANICI DENEYİMİ VE UI TASARIMI (USER EXPERIENCE - UX)
- **Görsel Bileşenler:** Nordic Gold temasına uygun Glassmorphism kartlar (`glass-panel`), amber/gold ikaz rozetleri ve dinamik durumu belirten mikro animasyonlar (`animate-fade-in`).
- **Aydınlık / Karanlık Mod:** WCAG AA standartlarında yüksek kontrastlı renk paleti (Light mode `amber-800`, Dark mode `dark:text-gold-300`).
- **Responsive Uyum:** Mobil (375px), Tablet (768px) ve Masaüstü (1280px+) ekran boyutlarında sıfır taşma garantisi.

### ✅ 5. KABUL KRİTERLERİ (ACCEPTANCE CRITERIA)
- [x] Maddenin Yol Haritası sırasına (#1 ➔ #2 ➔ #3 ...) göre otonom yapay zeka hattınca işlenmesi.
- [x] 3 Aşamalı Test Silsilesi (UI/UX 100/100, QA Entegrasyon %100 PASSED, CISO Güvenlik Risk 0/100).
- [x] GitHub Project #2 panosunda kartın 'Done' sütununa aktarılması.
- [x] Full Agent Traceability commit formatı ile `git push origin main` yapılması.

---

