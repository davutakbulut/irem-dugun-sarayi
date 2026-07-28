# 🏰 İREM DÜĞÜN SARAYI & ORGANİZASYON PLATFORMU
## KAPSAMLI PROJE DETAYLARI VE MASTER PROMPT DOSYASI

> **Not:** Bu doküman, NotebookLM'e yüklenmek üzere hazırlanan **İrem Düğün Sarayı & Organizasyon Şirketi** projesinin tüm mimari, iş mantığı, kullanıcı rolleri (RBAC), Tam Sayfa Rezervasyon & Kiralama Çalışma Alanı (`#/yeni-rezervasyon`), Otomatik Müşteri Üyelik Kaydı, Akış Planlaması, Canlı Takvim Önizlemesi, Resmi Sözleşme Çıktısı, Kalıcı Geliştirme Kuralları ve eklenen eklentilerin (plugins) detaylarını içeren tam kapsamlı master referans kılavuzudur.

---

## 🛑 KRİTİK GELİŞTİRME, VERİ KORUMA VE TEST KURALLARI (USER DIRECTIVES)

> **[ÖNEMLİ VE KESİN KURALLAR]:**
> 1. **KİŞİSEL VERİ VE TARAYICI DOKUNULMAZLIĞI:** Kullanıcının kişisel bilgisayarına, Chrome profillerine, kayıtlı verilerine veya uygulamalarına asla müdahale edilmeyecek, karıştırılmayacaktır. Tüm otomasyon ve testler tamamen bağımsız izolasyon alanında yürütülecektir.
> 2. **Mevcut Subagent'ı Yeniden Kullanma & Öğretme:** Her işlem için sıfırdan yeni subagent açmak YASAKTIR! Mevcut aktif test ajanı (`send_message` ile) kullanılacak, ajana yeni talimatlar iletilerek geçmiş hatalardan ders çıkarması ve tecrübe kazanması sağlanacaktır.
> 3. **Çok Yönlü Yetenek & Skill Değerlendirmesi:** Alınan karar ve çözümün mantıklı olup olmadığı tüm bağlı beceriler (`frontend-design`, `security-guidance`, `superpowers`, `claude-mem`, `a11y-debugging`, `chrome-devtools`) kılavuzları aktif olarak okunup çağrılarak sorgulanacaktır.
> 4. **Zorunlu Canlı Test:** Yapılan her işlemden sonra uygulama **mutlaka** izole test ajanları (`send_message`) ile doğrulanacak, test edilmeden işlem tamamlandı denmeyecektir!

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
- **Lokancement:** Sapanca Göl Kenarı, Sakarya
- **İletişim:** +90 532 111 2233 | admin@iremdugunsarayi.com
- **Sektör:** Düğün Salonu Kiralama, Kır Düğünü, Kına Gecesi, Nişan ve Kurumsal Etkinlik Organizasyonu.

---
*İrem Düğün Sarayı & Organizasyon Şirketi Mimarisi - Tüm Hakları Saklıdır (2026).*
