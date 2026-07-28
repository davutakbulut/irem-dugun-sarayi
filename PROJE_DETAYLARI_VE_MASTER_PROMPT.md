# 🏰 İREM DÜĞÜN SARAYI & ORGANİZASYON PLATFORMU
## KAPSAMLI PROJE DETAYLARI VE MASTER PROMPT DOSYASI

> **Not:** Bu doküman, NotebookLM'e yüklenmek üzere hazırlanan **İrem Düğün Sarayı & Organizasyon Şirketi** projesinin tüm mimari, iş mantığı, kullanıcı rolleri (RBAC), Tam Sayfa Rezervasyon & Kiralama Çalışma Alanı (`#/yeni-rezervasyon`), Canlı Görünür Ekranda Tarayıcı Testleri (Headful Mode), Otomatik Müşteri Üyelik Kaydı, Akış Planlaması, Canlı Takvim Önizlemesi, Resmi Sözleşme Çıktısı, Kalıcı Geliştirme Kuralları ve eklenen eklentilerin (plugins) detaylarını içeren tam kapsamlı master referans kılavuzudur.

---

## 🛑 KRİTİK GELİŞTİRME, SUBAGENT VE CANLI TEST KURALLARI (USER DIRECTIVES)

> **[ÖNEMLİ KURALLAR]:** Her işlem/kod değişikliğinde:
> 1. **Çok Yönlü Yetenek & Skill Değerlendirmesi:** Alınan karar ve çözümün mantıklı olup olmadığı tüm bağlı beceriler (`frontend-design`, `security-guidance`, `superpowers`, `claude-mem`, `a11y-debugging`, `chrome-devtools`) kılavuzları aktif olarak okunup çağrılarak sorgulanacaktır.
> 2. **Mevcut Subagent'ı Yeniden Kullanma & Öğretme:** Her işlem için sıfırdan yeni subagent açmak YASAKTIR! Mevcut aktif test ajanı (`send_message` ile) kullanılacak, ajana yeni talimatlar iletilerek geçmiş hatalardan ders çıkarması ve tecrübe kazanması sağlanacaktır.
> 3. **CANLI VE GÖRÜNÜR EKRANDA OTOMASYON TESTİ (Headful Mode):** Yapılan her işlemden sonra uygulama **mutlaka** kullanıcının ekranında **canlı ve görünür bir Chrome penceresi** açılarak (`send_message`) test edilecek, kullanıcı tıklamaları kendi gözleriyle canlı olarak izleyebilecektir!

---

## 📑 İÇİNDEKİLER
1. [Proje Hakkında & Genel Bilgiler](#1-proje-hakkında--genel-bilgiler)
2. [Teknik Yığın ve Mimari İlkeler](#2-teknik-yığın-ve-mimari-ilkeler)
3. [Eklenen Eklentiler & Beceriler (Plugins & Skills)](#3-eklenen-eklentiler--beceriler-plugins--skills)
4. [Tam Sayfa Rezervasyon & Kiralama Çalışma Alanı (#/yeni-rezervasyon)](#4-tam-sayfa-rezervasyon--kiralama-çalışma-alanı-yeni-rezervasyon)
5. [Canlı Ekranda İzlenebilir Otomasyon Testleri (Headful Mode)](#5-canlı-ekranda-izlenebilir-otomasyon-testleri-headful-mode)
6. [Otomatik Müşteri Üyelik Kaydı & İletişim Bilgileri](#6-otomatik-müşteri-üyelik-kaydı--iletişim-bilgileri)
7. [Hizmet Bazlı Kişi Sayıları, Kapora & Ödeme Statüsü](#7-hizmet-bazlı-kişi-sayıları-kapora--ödeme-statüsü)
8. [Fatura Bilgileri (Bireysel TC / Tüzel VKN) & %20 KDV](#8-fatura-bilgileri-bireysel-tc--tüzel-vkn--20-kdv)
9. [Organizasyon & Etkinlik Akış Planlama Ekranı](#9-organizasyon--etkinlik-akış-planlama-ekranı)
10. [Canlı Takvim Ön İzlemesi & Çakışma Kontrolü](#10-canlı-takvim-ön-izlemesi--çakışma-kontrolü)
11. [Yazdırılabilir Resmi Düğün Sözleşmesi ve Fatura Çıktısı](#11-yazdırılabilir-resmi-düğün-sözleşmesi-ve-fatura-çıktısı)
12. [Rol Tabanlı Erişim Kontrolü (RBAC) Yetki Matrisi](#12-rol-tabanlı-erişim-kontrolü-rbac-yetki-matrisi)
13. [Yetkisiz Erişim (403 Access Denied) Güvenlik Modülü](#13-yetkisiz-erişim-403-access-denied-güvenlik-modülü)

---

## 1. PROJE HAKKINDA & GENEL BİLGİLER
- **Şirket Adı:** İrem Düğün Sarayı & Organizasyon Şirketi
- **Lokasyon:** Sapanca Göl Kenarı, Sakarya
- **İletişim:** +90 532 111 2233 | admin@iremdugunsarayi.com
- **Sektör:** Düğün Salonu Kiralama, Kır Düğünü, Kına Gecesi, Nişan ve Kurumsal Etkinlik Organizasyonu.

---

## 5. CANLI EKRANDA İZLENEBİLİR OTOMASYON TESTLERİ (HEADFUL MODE)
- Testler arka planda gizli kalmaz; kullanıcının ekranında **canlı bir Chrome penceresi** olarak açılır.
- Kullanıcı buton tıklamalarını, form doldurmalarını ve takvim etkileşimlerini kendi ekranında anlık olarak izler.

---
*İrem Düğün Sarayı & Organizasyon Şirketi Mimarisi - Tüm Hakları Saklıdır (2026).*
