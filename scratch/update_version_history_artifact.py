import os

file_path = "/Users/davutakbulut/.gemini/antigravity/brain/f60111cc-5bec-4b99-8da2-93a0a75c00b9/version_history.md"

new_content = """# İrem Düğün Sarayı - Sürüm Geçmişi (Version History) & Geliştirme Karşılaştırmaları

> [!IMPORTANT]
> **ZORUNLU ANA KURAL (MANDATORY CORE RULE):**
> Her `git push` işleminde yapılan yeni özellik, hata düzeltmesi veya deneme geliştirmeleri **ÖNCEKİ DURUM VS YENİ DURUM** Karşılaştırmalı Notlar tablosunda detaylandırılarak sürüm notlarına kaydedilmelidir. Sadece commit hash bilgisi vermek YASAKTIR.

---

## [v1.4.5] - 31 Temmuz 2026 (CANLI MEDYA & GÜVENLİK GÜNCELLEMESİ)

### 📊 Önceki Durum vs Yeni Durum Karşılaştırma Tablosu

| Geliştirilen Alan / Özellik | Önceki Durum (Before) | Yeni Durum (After / Geliştirilmiş Hal) | Güncelleme Amacı & Kazanım |
| :--- | :--- | :--- | :--- |
| **1. Medya Linkinde İzolasyon** | `#/medya-yukle?key=...` linkinde sol sidebar, üst header ve rol değiştiriciler açık kalıyordu. | URL'de `key=` veya `mode=guest` olduğu anda **Sidebar, Topbar ve Admin Header %100 gizlenir**. | Davetlilerin yönetim menülerini veya diğer müşterilerin verilerini görmesi engellendi. |
| **2. Sayfa Yenileme Durumu (State Loss)** | Albüme girildiğinde URL değişmediği için F5 yapınca ana karta geri dönüyordu. | Albüme tıklandığında URL **`#/medya-yukle?key=MEDIA-8X92M1KP`** olur; F5 yapınca albüm korunur. | Kesintisiz kullanıcı deneyimi sağlandı. |
| **3. Canlı Senkronizasyon (Real-Time)** | Davetli fotoğraf yükleyince Admin tarafında sayfa yenilenmeden görünmüyordu. | `CustomEvent` + `Storage` + **1 Saniyelik Hızlı Polling** ile Admin panelinde **sayfa yenilenmeden canlı düşer**. | Anlık fotoğraf akışı sağlandı. |
| **4. Medya Kalıcılığı (Persistence)** | Yüklenen bazı görseller oturum değişince veya önbellek silinince kaybolabiliyordu. | Görseller yüklenir yüklenmez `CacheService` ve `localStorage` içine **anında kalıcı yazılır**. | Veri kaybı tamamen önlendi. |
| **5. Link Kopyalama Hatası (`undefined`)** | Kopyalanan link `key=undefined` şeklinde bozuk link üretebiliyordu. | Garanti fallback mekanizması ile **`http://localhost:8008/#/medya-yukle?mode=guest&key=MEDIA-8X92M1KP`** kopyalanır. | Davetli bağlantı paylaşımı hatasız hale getirildi. |
| **6. Medya Silme Özelliği** | Yüklenen fotoğrafları/videoları silme butonu bulunmuyordu. | Her medya kartına **`🗑️ Sil`** butonu eklendi, onay ile albümden silinebiliyor. | Medya yönetimi esnekleştirildi. |
| **7. Geçersiz Key Güvenlik Ekranı** | Olmayan/silinmiş bir Key ile girildiğinde sistem varsayılan ilk albümü gösteriyordu. | Olmayan bir Key ile girildiğinde **`⚠️ Geçersiz veya Bulunamayan Etkinlik Bağlantısı`** uyarısı açılır. | Yetkisiz medya erişimi engellendi. |
| **8. Müşteri E-Posta İzolasyonu** | Müşteri giriş yaptığında tüm etkinliklerin medya albümlerini görebiliyordu. | Müşteri sadece kendi e-postasına/ID'sine tanımlı etkinlik kartlarını görebilir. | Gizlilik ve RBAC güvenliği sağlandı. |

---

## [v1.4.0] - 31 Temmuz 2026 (KARARLI CANLI SÜRÜM)
- **Müstakil Rol Yönetimi:** Rol Yönetimi Sistem Ayarlarından ayrılıp müstakil `#/roller` sayfasına dönüştürüldü (Admin-only).
- **Menü Yapılandırması:** `Zihin Haritası` ve `Rol Yönetimi` bağlantıları `YÖNETİM & AYARLAR` grubu altına alındı.
- **5 Kritik Form Kuralı:** Negatif kişi sayısı/fiyat engellendi, mükerrer kampanya kodu engellendi, geçmiş tarihli rezervasyon engellendi, rol persistent yapıldı.
- **3G Hız Performansı:** Babel pre-compilation ve Gzip sıkıştırma ile LCP < 2.5s seviyesine çekildi.
- **Nordic Crown Logo & Zero-Emoji:** Header logosuna Footer taç rozeti uygulandı, tüm emojiler SVG ThemeIcon bileşenleriyle değiştirildi.

## [v1.3.0] - 30 Temmuz 2026
- **Sub-Header Mimarisi:** Ana header ile menü arasında bağımsız Rol & Canlı Sistem Sub-Header barı kuruldu.
- **Semantik Sürümleme:** Sürüm geçmişi modalı ve versiyon notları entegre edildi.
- **Mega Menü:** Düğün.com stili full-width hover drawer geliştirildi.

## [v1.2.0] - 30 Temmuz 2026
- **Çift Navigasyon Mimarisi:** Dikey Sol Menü ve Yatay Üst Menü tercihi Görünüm ayarlarına eklendi.

## [v1.1.0] - 29 Temmuz 2026
- **RBAC Sayfa & İstatistik Kısıtlamaları:** Ciro ve finans verileri Admin rolüne kısıtlandı.

## [v1.0.0] - 29 Temmuz 2026
- **Modüler Sayfa Mimarisi & 5 Kurumsal Tema:** 11 ana sayfa bileşeni ES modülleri halinde ayrıştırıldı.

## [v0.1.0] - 28 Temmuz 2026
- **Dinamik Düğün Takvimi & Hatasız Modallar:** Ay/Yıl navigasyonu, fatura dökümü ve WhatsApp bildirimleri.

## [v0.0.1] - 27 Temmuz 2026
- **İlk Sürüm Yayını:** Rezervasyon oluşturma formu, müşteri CRM kayıtları ve salon kapasite tanımları.
"""

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated version_history.md artifact with mandatory core rule & detailed before vs after table!")
