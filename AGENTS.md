# 🏰 İrem Düğün Sarayı & Balo Tesisleri - AGENTS.md (Sistem Kuralları)

## 📌 PROJE MİMARİ KURAL KÜMESİ (DEĞİŞTİRİLEMEZ)

### 1. 🌐 Ön Yüz Web Sitesi (Public Site - Ana Domain `/`)
- **Dosya**: `index.html`
- **Rotalar**: `/`, `/salonlar`, `/360-tur`, `/organizasyonlar`, `/videolar`, `/blog`, `/hakkimizda`, `/iletisim`
- **Kural**: **%100 Herkese Açık ve Bağımsız.** Hiçbir oturum kontrolü, login engeli veya üye girişi yönlendirmesi YAZILAMAZ. Ana domain'e giren ziyaretçi doğrudan Lüks Düğün Salonu Tanıtım Sitesini görür.

### 2. 🔐 Yönetim Paneli (Admin Platform - Yönetim Alanı `/yonetim`)
- **Dosya**: `yonetim.html`
- **Rotalar**: `/yonetim`, `/giris`, `/login`
- **Kural**: **Kimlik Doğrulaması Zorunlu.** Yalnızca bu rotalarda `sessionUser` denetimi yapılır. Oturum yoksa `LoginComponent` ekranı gösterilir.

### 3. 🎨 Tasarım ve UI/UX Standartları (`modern-web-design-mastery`)
- **Tasarım Sistemi**: GitHub'da en çok yıldız alan modern UI/UX tasarım depoları (`awesome-claude-design`, `awesome-web-prompts`) standartları uygulanır.
- **Visuals**: Glassmorphic paneller (`backdrop-blur-md`), Lüks Altın & Safir HSL renk paleti, Playfair Display/Outfit şık tipografi ve akıcı mikro animasyonlar.

### 4. 🛡️ Sıfır Yapılandırmalı Akıllı Dinamik Yönlendirici & Slug Protokolü (Zero-Config Routing)
- **Proxy Tabanlı Dinamik Çözümleme:** 4-5 farklı statik sözlükte elle satır ekleme saçmalığı yasaktır. Rotalar JavaScript `Proxy` nesneleri üzerinden dinamik olarak çözülür. URL'e gelen herhangi bir slug doğrudan hedef sekme ismi olarak kabul edilir ve otomatik açılır.
- **Kalıcı F5 / Yenileme Güvencesi (Zero-404 Guarantee):** Sayfa doğrudan tarayıcıdan F5 ile yenilendiğinde asla 404 hatasına veya sessiz anasayfa yönlendirmesine düşmez.
- **Pre-Push Sözdizimi & AST Doğrulaması:** Kod değişiklikleri tamamlandığında, push yapılmadan önce `@babel/parser` ile sözdizimi denetlenecek, tek bir syntax hatası olan kod bile repoya aktarılmayacaktır.

### 5. 🗄️ Veritabanı Öncelikli Çalışma ve Kalıcılık Protokolü (Database-First Architecture)
- **Doğrudan SQL / Dedicated API Entegrasyonu:** Sistemdeki tüm varlıklar (Kampanyalar, Kullanıcılar, Rezervasyonlar, Müşteriler, Mekanlar, Hizmetler, Giderler, vb.) doğrudan MariaDB veritabanı uç noktalarına (`/api/*`) yazılmalıdır.
- **Silme & Güncelleme Desteği (Action: 'delete'):** Tüm `POST /api/{entity}` uç noktaları `action === 'delete'` yükünü koşulsuz desteklemeli, `DELETE /api/{entity}/:id` rotaları MariaDB tablosunda `DELETE FROM {table} WHERE id = ?` sorgusunu eksiksiz çalıştırmalıdır.
- **Tarih & Veri Tipi Güvenliği:** Tarih alanlarında boş string yerine `NULL` veya `YYYY-MM-DD` gönderilmeli, tip alanları (`type`, `category`) esnek `VARCHAR(50)` olarak tutulmalıdır.

---
*Bu kural seti tüm geliştirme ve ajan oturumları için geçerlidir.*

---

## 🦚 PONYTAIL - LAZY SENIOR DEV MODE (KALICI VE DEĞİŞTİRİLEMEZ İLKE)

> **Kalıcı Talimat:** Ponytail modu bu projede HER ZAMAN AKTİFTİR ve ASLA KALDIRILAMAZ. Tüm geliştirmelerde, kod değişikliklerinde ve mimari kararlarda HER ŞEY ÖNCE PONYTAIL MERDİVENİNE (Decision Ladder) SORULUR.

### 🪜 Ponytail Karar Merdiveni (Decision Ladder)
Herhangi bir kod yazmadan veya değişiklik yapmadan önce sırasıyla şu basamaklar sorgulanır:

1. **Bu Kod Gerçekten Gerekli mi? (YAGNI):** İhtiyaç yoksa yazma, tek satırla açıkla.
2. **Kod Tabanında Zaten Var mı?:** Projedeki mevcut util, helper veya bileşeni kullan.
3. **Standart Kütüphane Yapıyor mu?:** Stdlib / yerel dil özelliklerini tercih et.
4. **Yerel Platform Özelliği Kapsıyor mu?:** Özel JS yazmak yerine yerel HTML/CSS ve tarayıcı yeteneklerini kullan.
5. **Yüklü Bağımlılık Çözüyor mu?:** Yeni kütüphane eklemek yerine mevcut bağımlılığı kullan.
6. **Tek Satır Olabilir mi?:** En kısa ve temiz biçimde tek satır yap.
7. **Sadece Bunlardan Sonra:** En az ve en temiz çalışan kodu yaz.
