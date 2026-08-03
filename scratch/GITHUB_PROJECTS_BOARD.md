# 📊 İrem Düğün Sarayı — Resmi GitHub Projects Live Kanban Board

🔗 **Resmi GitHub Proje Panosu:** [https://github.com/users/davutakbulut/projects/2](https://github.com/users/davutakbulut/projects/2) (`Rezervasyon Sistemi - v1`)

Bu döküman ve canlı pano, otonom yapay zeka geliştirme hattı tarafından anlık olarak senkronize edilir.

---

## 📌 EN SON KARARLI SÜRÜMDEN (v1.4.99) ALINAN EKSİKLER VE YAPILACAKLAR (TO DO LIST)

- [x] **Eksik #1: Anasayfa & İstatistikler (`DashboardPage.jsx`)** — Status: `✅ Tamamlandı`
  > *Açıklama:* `generateSmartAIRecommendations` import eklendi. Canlı doluluk (%92), ciro grafikleri ve AI öneri kartları aktif.

- [x] **Eksik #2: Yeni Rezervasyon Sihirbazı (`CreateReservationPage.jsx`)** — Status: `✅ Tamamlandı`
  > *Açıklama:* Sihirbaz 1. adımındaki HTML div kapanış düzeni düzeltildi. %1, %10, %20 dinamik KDV hesaplama ve PDF indirme bağlandı.

- [x] **Eksik #3: Düğün Salonları Yönetimi (`VenuesPage.jsx`)** — Status: `✅ Tamamlandı`
  > *Açıklama:* `OptimizedImage` bileşeni entegre edildi. Salon doluluk ve kapora kartları eklendi.

- [x] **Eksik #4: Ek Hizmetler Kataloğu (`ServicesPage.jsx`)** — Status: `✅ Tamamlandı`
  > *Açıklama:* Kişi başı ve sabit fiyatlandırma simgeleri ve düzenleme modalları aktif.

- [x] **Eksik #5: Rezervasyon Listesi (`ReservationsListPage.jsx`)** — Status: `✅ Tamamlandı`
  > *Açıklama:* WhatsApp otomatik ödeme hatırlatma link parametreleri ve PDF fatura dökümü düzeltildi.

- [x] **Eksik #6: İnteraktif Takvim (`CalendarPage.jsx`)** — Status: `✅ Tamamlandı`
  > *Açıklama:* Takvim hücrelerine tıklandığında tarihi seçili olarak Yeni Rezervasyona aktaran `prefilledDate` bağlandı.

- [x] **Eksik #7: Kampanyalar & AI Önerileri (`CampaignsPage.jsx`)** — Status: `✅ Tamamlandı`
  > *Açıklama:* AI tarafından önerilen kiralama fırsatlarının tek tıkla canlı kampanyaya dönüştürülmesi bağlandı.

- [x] **Eksik #8: Finans & Kasa Yönetimi (`FinancePage.jsx`)** — Status: `✅ Tamamlandı`
  > *Açıklama:* `ExpenseVendorTracker v1.5.28` (Salon Masraf Kaydı) ve `VendorLedgerTracker v1.5.29` (Cari Hesap Takibi) entegre edildi.

- [x] **Eksik #9: Müşteri Rehberi CRM (`CustomersPage.jsx`)** — Status: `✅ Tamamlandı`
  > *Açıklama:* Bireysel (TC) ve Kurumsal (VKN) vergi detayları ve telefon numarası maskesi düzeltildi.

- [x] **Eksik #10: Kullanıcı Yönetimi (`UsersPage.jsx`)** — Status: `✅ Tamamlandı`
  > *Açıklama:* Kullanıcı profil kartları ve yetki rolleri eşleşti.

- [x] **Eksik #11: Rol & İzin Matrisi RBAC (`RolesPage.jsx`)** — Status: `✅ Tamamlandı`
  > *Açıklama:* Backend `/api/system-settings` REST API entegrasyonu tamamlandı; sayfa yenilendiğinde roller sıfırlanmıyor.

- [x] **Eksik #12: Raporlar & AI Analitiği (`ReportsPage.jsx`)** — Status: `✅ Tamamlandı`
  > *Açıklama:* Gelir dağılımı donut grafiği ve salon tercih oranları aktifleştirildi.

- [x] **Eksik #13: Medya & Foto Yükleme (`MediaPage.jsx`)** — Status: `✅ Tamamlandı`
  > *Açıklama:* Davetli medyasının fiziki disk klasörüne (`/uploads/{resId}/`) kaydedilmesi ve ZIP indirme aktif.

- [x] **Eksik #14: Profilim & Güvenlik Ayarları (`ProfilePage.jsx`)** — Status: `✅ Tamamlandı`
  > *Açıklama:* `ROLE_NAMES` import hatası çözüldü. Kullanıcı fotoğraf, e-posta ve şifre değiştirme aktif.

- [x] **Eksik #15: Zihin Haritası MindMap (`MindMapPage.jsx`)** — Status: `✅ Tamamlandı`
  > *Açıklama:* Mimari düğüm tıklama yönlendirmeleri bağlandı.

- [x] **Eksik #16: Sistem Kılavuzu & Mimarisi (`SystemGuidePage.jsx`)** — Status: `✅ Tamamlandı`
  > *Açıklama:* Canlı sistem sürümü modalı (`VersionHistoryModal`) bağlandı.

- [x] **Eksik #17: Genel Ayarlar & Görünüm (`SettingsPage.jsx`)** — Status: `✅ Tamamlandı`
  > *Açıklama:* 11 tema CSS bildirimi ve önbellek temizleme fonksiyonu bağlandı.

- [x] **Eksik #18: HTTP Hata Simülasyonları (`ErrorPages.jsx`)** — Status: `✅ Tamamlandı`
  > *Açıklama:* 404, 301, 403 ve 500 dayanıklılık ekranları yönlendirme butonlarıyla aktifleştirildi.

---

## ✅ DONE (TAMAMLANAN YAPAY ZEKA GELİŞTİRMELERİ)

- [x] **Madde #1: Çoklu Salon Çakışma Engelleyici** — Status: `✅ Tamamlandı (v1.5.03)`
- [x] **Madde #2: Tampon Hazırlık Süresi Modülü** — Status: `✅ Tamamlandı (v1.5.04)`

---

## 🔄 IN PROGRESS (AKTİF GELİŞTİRİLEN VE TEST EDİLEN)

- [ ] **Madde #3: Sürükle-Bırak Tarih Güncelleme Güvenlik İkazı** (Rezervasyon & Takvim)

---

## 📋 TO DO (BEKLEYEN YOL HARİTASI MADDELERİ)

- [ ] **Madde #4: Rezervasyon Opsiyon Süresi Zamanlayıcısı** (48 Saatlik Otomatik Düşme)
- [ ] **Madde #5: Google Calendar ve Outlook Takvim Entegrasyonu**
- [ ] **Madde #6: Özel Gün & Resmi Tatil Fiyat Çarpanı (%20 Bayram İndirimi/Farkı)**
- [ ] **Madde #7: Tekrarlanan Etkinlik Şablonları (Kurumsal Toplantı / Gala)**
- [ ] **Madde #8: Salona Özel Kapasite İkaz Rozeti**
- [ ] **Madde #9: Görsel Oturma Planı Tasarlayıcı (2D Kroki & Masa Düzeni)**
- [ ] **Madde #10: Rezervasyon Değişiklik Audit Log Ekranı**
