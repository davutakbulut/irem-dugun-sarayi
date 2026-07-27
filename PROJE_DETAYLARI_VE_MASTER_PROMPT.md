# 🏰 İREM DÜĞÜN SARAYI & ORGANİZASYON PLATFORMU
## KAPSAMLI PROJE DETAYLARI VE MASTER PROMPT DOSYASI

> **Not:** Bu doküman, NotebookLM'e yüklenmek üzere hazırlanan **İrem Düğün Sarayı & Organizasyon Şirketi** projesinin tüm mimari, iş mantığı, kullanıcı rolleri (RBAC), finansal kuralları ve UI/UX detaylarını içeren tam kapsamlı master referans kılavuzudur.

---

## 📑 İÇİNDEKİLER
1. [Proje Hakkında & Genel Bilgiler](#1-proje-hakkında--genel-bilgiler)
2. [Teknik Yığın ve Mimari İlkeler](#2-teknik-yığın-ve-mimari-ilkeler)
3. [Tema, Kurumsal Dil & Dinamik Renk Paleti](#3-tema-kurumsal-dil--dinamik-renk-paleti)
4. [Rol Tabanlı Erişim Kontrolü (RBAC) Yetki Matrisi](#4-rol-tabanlı-erişim-kontrolü-rbac-yetki-matrisi)
5. [Yetkisiz Erişim (403 Access Denied) Güvenlik Modülü](#5-yetkisiz-erişim-403-access-denied-güvenlik-modülü)
6. [Temiz ASCII URL Yönlendirme (Routing) Kuralları](#6-temiz-ascii-url-yönlendirme-routing-kuralları)
7. [Çakışma Önleme (Collision Check) & Zaman Dilimleri](#7-çakışma-önleme-collision-check--zaman-dilimleri)
8. [Finansal Hesaplamalar, KDV %20 & Fatura Otomasyonu](#8-finansal-hesaplamalar-kdv-20--fatura-otomasyonu)
9. [Otomatik İletişim & WhatsApp Entegrasyonu](#9-otomatik-iletişim--whatsapp-entegrasyonu)
10. [Yapay Zeka (AI) Destekli Raporlar ve Öneriler](#10-yapay-zeka-ai-destekli-raporlar-ve-öneriler)

---

## 1. PROJE HAKKINDA & GENEL BİLGİLER
- **Şirket Adı:** İrem Düğün Sarayı & Organizasyon Şirketi
- **Lokasyon:** Sapanca Göl Kenarı, Sakarya
- **İletişim:** +90 532 111 2233 | admin@iremdugunsarayi.com
- **Sektör:** Düğün Salonu Kiralama, Kır Düğünü, Kına Gecesi, Nişan ve Kurumsal Etkinlik Organizasyonu.

---

## 2. TEKNİK YIĞIN VE MİMARİ İLKELER
1. **Frontend Core:** React 18 (JS/JSX) + Semantik HTML5.
2. **Single Page Application (SPA):** Tüm sekme geçişleri, modallar ve bildirimler **sayfa yenilenmeden** gerçekleşir.
3. **Stil Sistem:** Tailwind CSS + Custom CSS Variables + Lucide Icons + Google Fonts (Inter & Outfit).
4. **Veri Yönetimi:** React State & In-Memory / LocalStorage mock veritabanı.

---

## 3. TEMA, KURUMSAL DİL & DİNAMİK RENK PALETİ
- **Varsayılan Tema:** **Şık Krem / Beyaz Kurumsal Mod (Fresh White & Cream Corporate Mode)**.
- **Alternatif Tema:** **Gece Lüks Şampanya Modu (Dark Mode)**.
- **Dinamik CSS Değişkenleri (CSS Variables):**
  - `--color-gold`: `#d97706` (Ana Altın/Şampanya Vurgusu)
  - `--color-bg`: `#faf9f6` (Ferah Krem Arka Plan)
  - `--color-card`: `#ffffff` (Saf Beyaz Kartlar)
- **Canlı Renk Özelleştirici (Customizer):** Header alanındaki `🎨` renk butonu ile ana renk paleti anlık olarak değiştirilebilir.

---

## 4. ROL TABANLI ERİŞİM KONTROLÜ (RBAC) YETKİ MATRİSİ

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

## 5. YETKİSİZ ERİŞİM (403 ACCESS DENIED) GÜVENLİK MODÜLÜ
- Kullanıcı yetkisi olmayan bir modüle doğrudan URL adresi (`#/finans`) veya başka yollarla erişmeye çalıştığında sistem otomatik olarak **"Hata 403 / Yetkisiz Erişim"** uyarı ekranını görüntüler.
- Ekranda kullanıcının mevcut rolü, erişmeye çalıştığı modül adı ve **"Güvenli Anasayfaya Dön"** yönlendirme butonu bulunur.

---

## 6. TEMİZ ASCII URL YÖNLENDİRME (ROUTING) KURALLARI
URL adreslerinde rol parametreleri (`?rol=...`) kaldırılmış ve Türkçe karakter içermeyen temiz ASCII bağlantılar kullanılmıştır:

- `#/anasayfa`
- `#/dugun-salonlari`
- `#/ek-hizmetler`
- `#/rezervasyonlar`
- `#/takvim`
- `#/kampanyalar`
- `#/finans`
- `#/musteri-rehberi`
- `#/kullanici-yonetimi`
- `#/raporlar-ai`
- `#/medya-yukle`

---

## 7. ÇAKIŞMA ÖNLEME (COLLISION CHECK) & ZAMAN DİLİMLERİ
Aynı salonda, aynı tarihte çift rezervasyon (çakışma) yapılmasını engeller.
- **Zaman Dilimleri:** `13:00 - 17:00` (Gündüz) ve `19:00 - 23:00` (Gece).
- Çakışma tespit edildiğinde sistem rezervasyonu engeller ve kullanıcıyı uyarır.

---

## 8. FİNANSAL HESAPLAMALAR, KDV %20 & FATURA OTOMASYONU
- **Ara Toplam:** Salon Fiyatı + Seçilen Ek Hizmetler (Kişi Sayısı x Birim Fiyat).
- **Kampanya İndirimi:** İndirim tutarı ara toplamdan düşülür.
- **KDV Oranı:** Kalan tutar üzerinden **%20 KDV** eklenir.
- **Ödeme Takibi:** Alınan kapora düşülür, kalan net bakiye anlık olarak takip edilir.

---

## 9. OTOMATİK İLETİŞİM & WHATSAPP ENTEGRASYONU
- Müşteri kartında yer alan WhatsApp butonları ile müşterinin telefon numarasına otomatik kişiselleştirilmiş doğrudan mesaj bağlantısı (`https://wa.me/...`) üretilir.

---

## 10. YAPAY ZEKA (AI) DESTEKLİ RAPORLAR VE ÖNERİLER
- Hafta içi düşük doluluk oranlarına sahip günleri tespit ederek otomatik indirim ve kampanya paketleri önerir.
- Sık birlikte satın alınan ek hizmetleri analiz ederek avantajlı düğün paketleri oluşturma teklifleri sunar.

---
*İrem Düğün Sarayı & Organizasyon Şirketi Mimarisi - Tüm Hakları Saklıdır (2026).*
