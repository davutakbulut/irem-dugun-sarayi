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

### 4. 🛡️ Yeni Sayfa / Modül Geliştirme, Hata İzolasyonu & Rota Güvence Protokolü
- **Çift Yönlü Router & Slug Senkronizasyonu:** Yeni veya güncellenen her sayfa/sekme için `activeTab` tanımlanırken; `SLUG_TO_TAB`, `TAB_TO_SLUG` ve `TAB_TO_PATH` haritaları eksiksiz doldurulmalıdır. Sayfa linki doğrudan tarayıcıdan F5 ile yenilendiğinde asla 404 hatasına düşmemelidir.
- **Modüler Hata İzolasyonu (Error Boundary):** Her sayfa bağımsız `BlockErrorBoundary` / `ErrorBoundary` ile sarılmalıdır. Bir sayfada runtime hatası oluşsa dahi diğer sayfalar, üst menü ve navigasyon barı kesintisiz çalışmaya devam edecektir.
- **Pre-Push Sözdizimi & AST Doğrulaması:** Kod değişiklikleri tamamlandığında, push yapılmadan önce `@babel/parser` ile sözdizimi denetlenecek, tek bir syntax hatası olan kod bile repoya aktarılmayacaktır.
- **Standartlara Uygun SVG Vektörleri:** SVG `<path d="...">` tanımlarında React DOM ve W3C standartlarına tam uyumlu, boşlukları düzgün vektör koordinatları kullanılacak, konsolda attribute uyarısı veren sıkıştırılmış malformed path'ler engellenecektir.

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

### 🛡️ Temel İlkeler & Dokunulmazlıklar
- **Önce Anla:** Karar merdiveni problemi ve akışı tamamen anladıktan sonra çalıştırılır.
- **Kök Neden Düzeltmesi:** Semptomu değil, kök nedeni ortak noktadan çöz.
- **Sıfır Aşırı Mühendislik:** İstenmeyen soyutlamalar, gereksiz boilerplate ve karmaşık yapılar YASAKTIR.
- **Dokunulmazlık:** Güvenlik, doğrulama (input validation), hata yönetimi ve erişilebilirlikten asla taviz verilemez.
