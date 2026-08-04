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

---
*Bu kural seti tüm geliştirme ve ajan oturumları için geçerlidir.*
