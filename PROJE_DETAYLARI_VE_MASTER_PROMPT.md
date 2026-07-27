# 🏰 İREM DÜĞÜN SARAYI & ORGANİZASYON PLATFORMU
## KAPSAMLI PROJE DETAYLARI VE MASTER PROMPT DOSYASI

> **Not:** Bu doküman, NotebookLM'e yüklenmek üzere hazırlanan **İrem Düğün Sarayı & Organizasyon Şirketi** projesinin tüm mimari, iş mantığı, kullanıcı rolleri (RBAC), 3-Adımlı Rezervasyon Sihirbazı, Resmi Sözleşme Çıktısı, Kalıcı Geliştirme Kuralları ve eklenen eklentilerin (plugins) detaylarını içeren tam kapsamlı master referans kılavuzudur.

---

## 🛑 KRİTİK GELİŞTİRME & TEST KURALI (USER DIRECTIVE)

> **[ÖNEMLİ TALİMAT]:** Her işlem/kod değişikliğinden önce ve sonra:
> 1. **Çok Yönlü Yetenek Değerlendirmesi:** Alınan karar ve çözümün mantıklı olup olmadığı tüm beceriler (`frontend-design`, `security-guidance`, `superpowers`, `claude-mem`) açısından sorgulanacaktır.
> 2. **Zorunlu Canlı Test:** Yapılan her işlemden sonra uygulama **mutlaka** canlı tarayıcı test ajanları (`Chrome_DevTools_Test_Agent`) veya otomatik test komutları ile doğrulanacak, test edilmeden işlem tamamlandı denmeyecektir!

---

## 📑 İÇİNDEKİLER
1. [Proje Hakkında & Genel Bilgiler](#1-proje-hakkında--genel-bilgiler)
2. [Teknik Yığın ve Mimari İlkeler](#2-teknik-yığın-ve-mimari-ilkeler)
3. [Eklenen Eklentiler & Beceriler (Plugins & Skills)](#3-eklenen-eklentiler--beceriler-plugins--skills)
4. [3-Adımlı Yeni Rezervasyon & Sözleşme Sihirbazı](#4-3-adımlı-yeni-rezervasyon--sözleşme-sihirbazı)
5. [Yazdırılabilir Resmi Düğün Sözleşmesi ve Fatura Çıktısı](#5-yazdırılabilir-resmi-düğün-sözleşmesi-ve-fatura-çıktısı)
6. [Tema, Kurumsal Dil & Dinamik Renk Paleti](#6-tema-kurumsal-dil--dinamik-renk-paleti)
7. [Rol Tabanlı Erişim Kontrolü (RBAC) Yetki Matrisi](#7-rol-tabanlı-erişim-kontrolü-rbac-yetki-matrisi)
8. [Yetkisiz Erişim (403 Access Denied) Güvenlik Modülü](#8-yetkisiz-erişim-403-access-denied-güvenlik-modülü)
9. [Temiz ASCII URL Yönlendirme (Routing) Kuralları](#9-temiz-ascii-url-yönlendirme-routing-kuralları)
10. [MySQL Veritabanı Mimarisi (schema.sql)](#10-mysql-veritabanı-mimarisi-schemasql)
11. [Çakışma Önleme (Collision Check) & Zaman Dilimleri](#11-çakışma-önleme-collision-check--zaman-dilimleri)
12. [Finansal Hesaplamalar, KDV %20 & Fatura Otomasyonu](#12-finansal-hesaplamalar-kdv-20--fatura-otomasyonu)
13. [Otomatik İletişim & WhatsApp Entegrasyonu](#13-otomatik-iletişim--whatsapp-entegrasyonu)

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
1. **`superpowers`**: Karmaşık otonom görevler ve orkestrasyon.
2. **`frontend-design`**: Lüks UI/UX tasarım standartları ve renk teorisi.
3. **`security-guidance`**: Siber güvenlik audit ve RBAC koruması.
4. **`claude-mem`**: Kalıcı hafıza ve sürekli bağlam takibi.

---

## 4. 3-ADIMLI YENİ REZERVASYON & SÖZLEŞME SİHİRBAZI
- **Adım 1:** Salon Seçimi, Etkinlik Tarihi, Saat Dilimi (`13:00-17:00` / `19:00-23:00`) ve Davetli Sayısı (Canlı Çakışma Önleme Uyarısı ile).
- **Adım 2:** Müşteri Seçimi ve Düğün Paketi Ek Hizmetleri (Yemek Servisi, Fotoğraf & 4K Video, Orkestra, Masa Süsleme, Volkan Gösterisi) seçimi.
- **Adım 3:** Kampanya İndirim Kodu (`IREM2026`, `VIP5000`), Otomatik %20 KDV Hesaplaması, Kapora Girişi, Net Bakiye ve Sözleşme Onayı.

---

## 5. YAZDIRILABİLİR RESMİ DÜĞÜN SÖZLEŞMESİ VE FATURA ÇIKTISI
- Rezervasyon detayından tek tıkla açılan antetli resmi yazdırma şablonu.

---

## 6. TEMA, KURUMSAL DİL & DİNAMİK RENK PALETİ
- **Varsayılan Tema:** **Şık Krem / Beyaz Kurumsal Mod**.

---

## 7. ROL TABANLI ERİŞİM KONTROLÜ (RBAC) YETKİ MATRİSİ
- **Admin 👑**, **Satışçı 💼**, **Sosyal Medya 📸**, **Müşteri 💑**.

---

## 8. YETKİSİZ ERİŞİM (403 ACCESS DENIED) GÜVENLİK MODÜLÜ
- Yetkisiz modül erişimlerinde otomatik devreye giren şık 403 güvenlik uyarı ekranı.

---
*İrem Düğün Sarayı & Organizasyon Şirketi Mimarisi - Tüm Hakları Saklıdır (2026).*
