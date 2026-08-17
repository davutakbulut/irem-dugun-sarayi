# 🏰 İREM DÜĞÜN SARAYI & ORGANİZASYON PLATFORMU
## KAPSAMLI PROJE DETAYLARI VE MASTER PROMPT DOSYASI

> **Not:** Bu doküman, NotebookLM'e yüklenmek üzere hazırlanan **İrem Düğün Sarayı & Organizasyon Şirketi** projesinin tüm mimari, iş mantığı, kullanıcı rolleri (RBAC), Tam Sayfa Rezervasyon & Kiralama Çalışma Alanı (`#/yeni-rezervasyon`), Otomatik Müşteri Üyelik Kaydı, Akış Planlaması, Canlı Takvim Önizlemesi, Resmi Sözleşme Çıktısı, Kalıcı Geliştirme Kuralları, NotebookLM / MCP entegrasyon kuralları ve eklenen eklentilerin (plugins) detaylarını içeren tam kapsamlı master referans kılavuzudur.

---

## 🛑 CORE GELİŞTİRME, VERİ KORUMA VE ÇALIŞMA PROTOKOLÜ (CORE PROTOCOLS & USER DIRECTIVES)

> **[TEMEL CORE KURALLAR]:**
> 1. **SORULARA HER ZAMAN İLK OLARAK DOĞRUDAN VE EKSİKSİZ YANIT VERME KURALI:** Kullanıcı herhangi bir soru sorduğunda (Örn: "Güvenlik açığı oluşturmaz mı?", "İkonu eksik sayfa var mı?"), AJAN ÖNCE MUSTAKİLEN DOĞRUDAN VE AÇIK YANIT VERECEK, ardından teknik iş ve kod geliştirmesine geçecektir.
> 2. **MODÜLER DOSYA YAPISI ÜZERİNDE ÇALIŞMA (`src/*`):** Monolitik devasa dosyaları (index.html vb.) tekrarlı okuyup taramak YASAKTIR! Çalışmalar projedeki ayrıştırılmış modüler dosyalar (`src/pages/*`, `src/components/*`) üzerinde nokta atışı yürütülerek çoklu geliştirici ve yüksek performanslı çalışma ortamı korunacaktır.
> 3. **NOTEBOOKLM VE MCP İLE NOKTA ATIŞI SORGULAMA:** Projenin tüm master kuralları, tasarım rehberleri ve mimarisi NotebookLM / Bilgi Bankasında saklanır. Gereksiz geniş kod taraması yapmak yerine MCP üzerinden NotebookLM'e nokta atışı sorgu atılarak bilgi alınacaktır.
> 4. **NORDIC VE KURUMSAL TEMALARDA SIFIR EMOJİ VE VEKTÖREL SVG İKON KURALI:** Nordic, Obsidian Gold, Sapphire, Platinum, Emerald ve Titanium temalarında ham emojiler (🔍, 🔄, 🛡️, 💥, 🚀 vb.) KESİNLİKLE KULLANILMAYACAK; yerlerine keskin vektörel SVG ikonları (`ThemeIcon` / `SvgIcon`) yerleştirilecektir.
> 5. **HATA SAYFALARI İZOLASYONU VE MÜSTAKİL HTML DOSYALARI:** Hata ve uyarı sayfalarında (404, 301, 403, 500) bilgi sızıntısını (Information Disclosure) önlemek için Header, Sidebar ve Mobil Footer tamamen gizlenip tam ekran izolasyonu sağlanacaktır. Kök dizindeki bağımsız müstakil dosyalar (`404.html`, `301.html`, `403.html`, `500.html`) güncel tutulacaktır.
> 6. **KİŞİSEL VERİ VE TARAYICI DOKUNULMAZLIĞI:** Kullanıcının kişisel bilgisayarına, Chrome profillerine veya kayıtlı verilerine asla müdahale edilmeyecektir.
> 7. **MEVCUT SUBAGENT'I YENİDEN KULLANMA:** Her işlem için sıfırdan subagent açmak yerine mevcut aktif test ajanı (`send_message` ile) kullanılacaktır.
> 8. **SIFIR YAPILANDIRMALI AKILLI DİNAMİK YÖNLENDİRİCİ & SLUG GÜVENCE PROTOKOLÜ (ZERO-CONFIG DYNAMIC PROXY ROUTING):**
>    - **a) Statik Çoklu Sözlük Kısıtlamasının Yasaklanması (Anti-Pattern Prevention):** Yeni bir sayfa/sekme eklendiğinde 4-5 ayrı statik sözlükte (`SLUG_TO_TAB`, `TAB_TO_SLUG`, `TAB_TO_PATH`, `TAB_PERMISSIONS`) elle kopyala-yapıştır yapma zorunluluğu KESİNLİKLE YASAKTIR.
>    - **b) JavaScript Proxy Tabanlı Dinamik Çözümleme (Smart Dynamic Proxy):** `SLUG_TO_TAB`, `TAB_TO_SLUG` ve `TAB_TO_PATH` nesneleri dinamik `Proxy` olarak çalışır. URL'e gelen herhangi bir slug (`/yonetim/{sayfa-adi}` veya `/{ziyaretci-sayfasi}`) bilinen takma adlarda olmasa dahi doğrudan hedef sekme ismi olarak kabul edilir ve otomatik olarak açılır.
>    - **c) Kalıcı F5 / Yenileme Dokunulmazlığı (Zero-404 Guarantee):** Hem Ziyaretçi Web Sitesinde (`index.html`) hem Yönetim Panelinde (`yonetim.html`) doğrudan URL ile girişlerde veya tarayıcı yenilemelerinde (F5/Reload) sayfanın 404'e veya sessizce anasayfaya düşmesi engellenmiştir.
>    - **d) RBAC Yetkilendirme Varsayılan Açık İlkesi (Default-Allow for Authenticated Users):** Yeni bir sekme eklendiğinde izin matrisinde unutulsa dahi admin ve giriş yapmış yetkili personel için sayfa kilitlenmez, varsayılan açık izinle çalışır.
>    - **e) Modüler Hata İzolasyonu (Fault Isolation):** Her sayfa bağımsız `BlockErrorBoundary` / `ErrorBoundary` ile sarılmalıdır. Bir sayfada runtime hatası olsa dahi menü, üst bar ve diğer sayfalar etkilenmeden çalışacaktır.
>    - **f) Pre-Push Sözdizimi & AST Doğrulaması:** Kod güncellemeleri tamamlandığında, push yapılmadan önce `@babel/parser` ile sözdizimi denetlenecek, syntax hatası olan kod repoya aktarılmayacaktır.
>    - **g) Standartlara Uygun SVG Vektörleri:** SVG `<path d="...">` tanımlarında React DOM ve W3C standartlarına tam uyumlu boşluklu koordinatlar kullanılacak, konsolda uyarı veren sıkıştırılmış malformed path'ler eklenmeyecektir.

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
12. [Yetkisiz Erişim (403 Access Denied) Ve Hata Ekranları Güvenlik Modülü](#12-yetkisiz-erişim-403-access-denied-ve-hata-ekranları-güvenlik-modülü)

---

## 1. PROJE HAKKINDA & GENEL BİLGİLER
- **Şirket Adı:** İrem Düğün Sarayı & Organizasyon Şirketi
- **Lokasyon:** Arifiye Merkez, Sakarya
- **İletişim:** +90 532 111 2233 | admin@iremdugunsarayi.com
- **Sektör:** Düğün Salonu Kiralama, Kır Düğünü, Kına Gecesi, Nişan ve Kurumsal Etkinlik Organizasyonu.

---
*İrem Düğün Sarayı & Organizasyon Şirketi Mimarisi - Tüm Hakları Saklıdır (2026).*
