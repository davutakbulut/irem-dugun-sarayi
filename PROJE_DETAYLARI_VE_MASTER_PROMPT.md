# 🏰 İREM DÜĞÜN SARAYI & ORGANİZASYON PLATFORMU
## KAPSAMLI PROJE DETAYLARI VE MASTER PROMPT DOSYASI

> **Not:** Bu doküman, NotebookLM'e yüklenmek üzere hazırlanan **İrem Düğün Sarayı & Organizasyon Şirketi** projesinin tüm mimari, iş mantığı, kullanıcı rolleri (RBAC), Tam Sayfa Rezervasyon & Kiralama Çalışma Alanı (`#/yeni-rezervasyon`), Otomatik Müşteri Üyelik Kaydı, Akış Planlaması, Canlı Takvim Önizlemesi, Resmi Sözleşme Çıktısı, MySQL veritabanı şeması ve eklenen eklentilerin (plugins) detaylarını içeren tam kapsamlı master referans kılavuzudur.

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
4. [Tam Sayfa Rezervasyon & Kiralama Çalışma Alanı (#/yeni-rezervasyon)](#4-tam-sayfa-rezervasyon--kiralama-çalışma-alanı-yeni-rezervasyon)
5. [Otomatik Müşteri Üyelik Kaydı & İletişim Bilgileri](#5-otomatik-müşteri-üyelik-kaydı--iletişim-bilgileri)
6. [Hizmet Bazlı Kişi Sayıları, Kapora & Ödeme Statüsü](#6-hizmet-bazlı-kişi-sayıları-kapora--ödeme-statüsü)
7. [Fatura Bilgileri (Bireysel TC / Tüzel VKN) & %20 KDV](#7-fatura-bilgileri-bireysel-tc--tüzel-vkn--20-kdv)
8. [Organizasyon & Etkinlik Akış Planlama Ekranı](#8-organizasyon--etkinlik-akış-planlama-ekranı)
9. [Canlı Takvim Ön İzlemesi & Çakışma Kontrolü](#9-canlı-takvim-ön-izlemesi--çakışma-kontrolü)
10. [Yazdırılabilir Resmi Düğün Sözleşmesi ve Fatura Çıktısı](#10-yazdırılabilir-resmi-düğün-sözleşmesi-ve-fatura-çıktısı)
11. [Rol Tabanlı Erişim Kontrolü (RBAC) Yetki Matrisi](#11-rol-tabanlı-erişim-kontrolü-rbac-yetki-matrisi)
12. [Yetkisiz Erişim (403 Access Denied) Güvenlik Modülü](#12-yetkisiz-erişim-403-access-denied-güvenlik-modülü)

---

## 1. PROJE HAKKINDA & GENEL BİLGİLER
- **Şirket Adı:** İrem Düğün Sarayı & Organizasyon Şirketi
- **Lokasyon:** Sapanca Göl Kenarı, Sakarya
- **İletişim:** +90 532 111 2233 | admin@iremdugunsarayi.com
- **Sektör:** Düğün Salonu Kiralama, Kır Düğünü, Kına Gecesi, Nişan ve Kurumsal Etkinlik Organizasyonu.

---

## 4. TAM SAYFA REZERVASYON & KİRALAMA ÇALIŞMA ALANI (#/yeni-rezervasyon)
- Pop-up modallar yerine sol menüde de yer alan **"➕ Yeni Rezervasyon Oluştur"** sekmeli ayrı bir tam sayfa çalışma alanı.
- Tüm form 7 ana bölümde tek ekranda yönetilir:
  1. Salon & Tarih/Saat Seçimi (`13:00-17:00` / `19:00-23:00` / Özel Saat).
  2. Otomatik Müşteri Üyelik Kaydı & İkinci İletişim Telefonu.
  3. Hizmet Bazlı Kişi Sayıları, Adetler & Ödendi İşaretleri.
  4. Finans, Referans Kodu (`IREM2026`, `VIP5000`) & Kapora Bilgileri.
  5. Fatura Bilgileri (Bireysel TC / Tüzel VKN, Vergi Dairesi, Adres).
  6. Etkinlik Akış Planlama Çizelgesi.
  7. Sağ Sütunda Canlı İnteraktif Takvim Önizleme Kartı & Anlık Hesap Dökümü.

---
*İrem Düğün Sarayı & Organizasyon Şirketi Mimarisi - Tüm Hakları Saklıdır (2026).*
