# 🏛️ İrem Düğün Sarayı - Ön Yüz ve Yönetim Mimarisi Kuralları

Bu proje **iki kesin ve bağımsız katmandan** oluşur:

## 1. 🌐 Ön Yüz Web Sitesi (Public Site) - Ana Domain (`/`)
- **Hedef**: Düğün salonunu inceleyen çiftler, misafirler, SEO arama motorları.
- **Erişim Yolu**: `/`, `/salonlar`, `/360-tur`, `/organizasyonlar`, `/videolar`, `/blog`, `/hakkimizda`, `/iletisim`, `/musteri-giris`
- **Giriş Şartı**: **KESİNLİKLE YOKTUR!** Hiçbir oturum kontrolü yapılmaz. Sayfa anında açılır.
- **Yönlendirme**: Ana domain ziyaretleri asla `/giris` veya üye oturum açma ekranına yönlendirilemez!
- **İndeksleme**: Google SEO meta etiketleri ve Schema.org `EventVenue` ile tam indekse açıktır.

## 2. 🔐 Yönetim Paneli (Admin Platform) - Yönetim Alanı (`/yonetim`)
- **Hedef**: Tesis yöneticisi, salon müdürü, organizasyon sorumlusu, muhasebeci.
- **Erişim Yolu**: `/yonetim`, `/giris`, `/login`, `yonetim.html`
- **Giriş Şartı**: **OTURUM DOĞRULAMASI ZORUNLUDUR.** Oturum yoksa `LoginComponent` gösterilir.
- **Rol Yetkileri (RBAC)**: Admin, Salon Müdürü, Satışçı, Müşteri (VIP Müşteri Portalı).

## ⚠️ Ajan Kuralları (Mecburi İlkeler):
1. Ana domain (`/`) kodlarında `sessionUser` yok diye asla `/giris` yönlendirmesi (`pushState('/giris')`) koyma!
2. Ön Yüz bileşenleri (`PublicLayout`, `HomePage`, `HallsPage` vb.) yönetim panelinin state veya sidebar yapısından tam bağımsızdır.
3. `/yonetim` rotaları haricinde hiçbir yerde `LoginComponent` otomatik render edilemez.
