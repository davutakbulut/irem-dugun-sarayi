import React, { useState } from 'react';
import { ThemeIcon } from '../components/ThemeIcon';

// COMPREHENSIVE MIND MAP NODE DATA WITH STATE DEPENDENCIES & CONNECTED NODES
export const MIND_MAP_DATA = [
  {
    id: 'core-arch',
    title: 'Core Mimari & Altyapı',
    icon: 'sparkles',
    fallbackEmoji: '🏗️',
    category: 'Architecture',
    color: 'from-amber-500 to-amber-600',
    borderColor: 'border-amber-500',
    bgColor: 'bg-amber-500/10',
    summary: 'Çift mimarili senkronizasyon, otomatik taslak kaydı ve Toast notification altyapısı.',
    whatItDoes: 'İrem Düğün Sarayı dijital yönetim platformunun temel teknik ve mimari omurgasını oluşturur.',
    connectedNodes: ['page-dashboard', 'theme-iconography', 'page-create-reservation', 'page-rbac-settings'],
    readsState: ['activeRole', 'currentTheme', 'draftReservations', 'systemLogs'],
    mutatesState: ['draftReservations', 'systemLogs', 'alertModal'],
    whichFeatures: [
      'Dual-Architecture Sync (Monolitik index.html + Modüler React src/ yapısı)',
      'Otomatik Taslak Kaydı Engine (draftReservations & refKey ile kaldığı yerden devam etme)',
      'Global Standalone Toast Notification System (Sağ üst kayar bildirim popupı)',
      'Error Page Guard (Hata simülasyonlarında header & sidebar gizleme kuralı)',
      'LocalStorage Caching & Persistence Engine'
    ],
    whyWeBuiltIt: 'Platformun hem hızlı prototipleme için tek dosyadan çalışabilmesini hem de kurumsal ölçeklenebilirlik için modüler ES2022 Standartlarında kalmasını sağlamak için inşa ettik.',
    rulesAndCore: [
      'Kural 1: Yapılan her UI ve mantık güncellemesi hem index.html hem de src/ bileşenlerinde %100 birebir senkronize edilmelidir.',
      'Kural 2: Hatalı veya eksik veri durumunda asla uygulama çökmemeli, null-safe optional chaining kullanılmalıdır.',
      'Kural 3: Formlar doldurulurken her adımda arka planda draftReservations güncellenmelidir.'
    ],
    stepByStepFlow: [
      '1. Adım: Kullanıcı sisteme girer, LocalStorage önbelleği ve varsayılan durumlar yüklenir.',
      '2. Adım: Herhangi bir işlem yapıldığında (ör. form doldurma) taslak motoru canlı tetiklenir.',
      '3. Adım: Başarılı işlemlerde global Toast popupı kullanıcıya anında geri bildirim verir.'
    ],
    relatedRoute: 'dashboard'
  },
  {
    id: 'theme-iconography',
    title: 'Tema Mimarisi & İkonografi',
    icon: 'sparkles',
    fallbackEmoji: '🎨',
    category: 'UI/UX System',
    color: 'from-blue-500 to-indigo-600',
    borderColor: 'border-blue-500',
    bgColor: 'bg-blue-500/10',
    summary: '5 Kurumsal Tema ve Emojisiz İkon Kuralları (ThemeIcon & NordicSvgMap).',
    whatItDoes: 'Tüm uygulamanın renk paletlerini, tipografisini, buton keskinliklerini ve minimalist ikon setlerini yönetir.',
    connectedNodes: ['core-arch', 'page-dashboard', 'page-create-reservation', 'page-finance'],
    readsState: ['currentTheme'],
    mutatesState: ['currentTheme'],
    whichFeatures: [
      '5 Kurumsal Tema: Nordic Light, Elite Luxury, Obsidian Gold, Sapphire Clean, Emerald Royal',
      'Nordic Light Temasında SIFIR EMOJİ KURALI (Tüm emojiler SVG vektör ikonlara dönüşür)',
      'ThemeIcon Bileşeni & NordicSvgMap Vektör Haritası (52+ Özel SVG İkon)',
      'Responsive Sticky Navigation (sticky top-0 h-[calc(100vh-105px)] kaydırma mimarisi)'
    ],
    whyWeBuiltIt: 'Kullanıcılara modern, lüks ve göz yormayan kurumsal bir deneyim sunmak; Nordic temasında emojiler yerine premium minimalist SVG ikonlar hissettirmek için tasarladık.',
    rulesAndCore: [
      'Kural 1: Nordic Light teması seçiliyken sayfada ham emoji görünmesi YASAKTIR. Tüm ikonlar <ThemeIcon /> ile sarmalanmalıdır.',
      'Kural 2: Tema değiştiğinde HTML data-ui-theme niteliği anında güncellenmeli ve CSS CSS-variables ile renkleri yenilemelidir.',
      'Kural 3: Sidebar ve Header menüleri ekran boyutu ne olursa olsun kırpılmamalı, kendi içinde kaymalıdır.'
    ],
    stepByStepFlow: [
      '1. Adım: Kullanıcı Ayarlar > Görünüm sekmesinden veya header tema butonundan tema seçer.',
      '2. Adım: Uygulama data-ui-theme etiketini değiştirir ve ThemeIcon bileşenleri SVG haritasını günceller.',
      '3. Adım: Nordic temasında tüm ham emojiler minimalist siyah/gri vektör ikonlara dönüşür.'
    ],
    relatedRoute: 'settings-appearance'
  },
  {
    id: 'page-dashboard',
    title: 'Dashboard (Genel Bakış)',
    icon: 'chart',
    fallbackEmoji: '📊',
    category: 'Pages',
    color: 'from-emerald-500 to-teal-600',
    borderColor: 'border-emerald-500',
    bgColor: 'bg-emerald-500/10',
    summary: 'Canlı KPI kartları, yaklaşan düğünler, hızlı işlem barı ve sistem durumu.',
    whatItDoes: 'İşletmenin tüm anlık durumunu, cirosunu, yaklaşan organizasyonlarını tek bakışta özetler.',
    connectedNodes: ['page-create-reservation', 'page-reservations', 'page-finance', 'page-reports-ai'],
    readsState: ['reservations', 'venues', 'services', 'customers', 'campaigns'],
    mutatesState: [],
    whichFeatures: [
      'Canlı KPI Kartları: Bu Ayki Toplam Ciro, Onaylı Düğün Sayısı, Bekleyen Taslaklar, Doluluk Oranı',
      'Yaklaşan Organizasyonlar Listesi & Hızlı Detay Önizleme',
      'Hızlı Kısayol Butonları: Yeni Rezervasyon, Kasa Ekleme, Fatura Kes',
      'AI Öneri Kartı: Doluluk analizi ve tek tıkla aksiyon önerisi'
    ],
    whyWeBuiltIt: 'Salon yöneticisinin ve resepsiyon görevlisinin güne başlarken tüm kritik verileri tek ekranda görmesini sağlamak için inşa ettik.',
    rulesAndCore: [
      'Kural 1: Ciro ve doluluk sayıları statik olmamalı, reservations dizisinden canlı hesaplanmalıdır.',
      'Kural 2: Yaklaşan etkinliklerde müşteri adı, tarih ve seans bilgisi eksiksiz görünmelidir.'
    ],
    stepByStepFlow: [
      '1. Adım: Kullanıcı sisteme girince varsayılan olarak Dashboard açılır.',
      '2. Adım: KPI kartları anlık rezervasyon durumlarını hesaplar.',
      '3. Adım: Hızlı butonlar üzerinden doğrudan rezervasyon veya finans sayfasına geçilir.'
    ],
    relatedRoute: 'dashboard'
  },
  {
    id: 'page-create-reservation',
    title: 'Rezervasyon Oluşturma (Wizard)',
    icon: 'calendar',
    fallbackEmoji: '📝',
    category: 'Pages',
    color: 'from-purple-500 to-pink-600',
    borderColor: 'border-purple-500',
    bgColor: 'bg-purple-500/10',
    summary: '6 adımlı canlı sözleşme ve rezervasyon sihirbazı, otomatik taslak kaydı.',
    whatItDoes: 'Yeni düğün/etkinlik sözleşmesi oluşturur, müşteri bilgilerini, ek hizmetleri, kaporayı ve özel istekleri kaydeder.',
    connectedNodes: ['page-reservations', 'page-calendar', 'page-finance', 'page-customers', 'page-campaigns'],
    readsState: ['venues', 'services', 'customers', 'campaigns', 'draftReservations'],
    mutatesState: ['reservations', 'customers', 'draftReservations'],
    whichFeatures: [
      '6 Adımlı Süreç: Müşteri Seçimi -> Salon/Tarih -> Ek Hizmetler -> Kampanya/İskonto -> Finans/Kapora -> Akış Planı',
      'Anlık Fatura & Sözleşme Hesaplama Motoru (KDV, Kapora, Kalan Bakiye)',
      'Otomatik Taslak Kaydı (RefKey bazlı taslak saklama)',
      'Dinamik Kampanya İndirimi Hesaplayıcı (campaigns dizisinde indirim kodunu tarama)'
    ],
    whyWeBuiltIt: 'Karmaşık düğün organizasyonu sözleşmelerini hatasız, hızlı ve 6 adımda adımlar arası taslak kaydı kaybedilmeden tamamlayabilmek için geliştirdik.',
    rulesAndCore: [
      'Kural 1: Giriş yapılan kampanya kodu canlı doğrulanmalı ve toplam tutardan düşmelidir.',
      'Kural 2: Müşteri adı veya salon seçilmediğinde sözleşme tamamlanamaz.',
      'Kural 3: Başarılı kayıtta müşteri rehberine ve rezervasyon listesine eşzamanlı eklenmelidir.'
    ],
    stepByStepFlow: [
      '1. Adım: Müşteri bilgileri girilir veya var olan rehberden seçilir.',
      '2. Adım: Salon, düğün tarihi ve seans (Gündüz/Gece) seçilir.',
      '3. Adım: Menü, Orkestra, Fotoğraf gibi ek hizmetler eklenir ve kampanya indirim kodu uygulanır.',
      '4. Adım: Alınan kapora yazılır, sözleşme onaylanır ve rezervasyon oluşturulur.'
    ],
    relatedRoute: 'create-reservation'
  },
  {
    id: 'page-reservations',
    title: 'Rezervasyon Listesi & Sözleşmeler',
    icon: 'user',
    fallbackEmoji: '📋',
    category: 'Pages',
    color: 'from-cyan-500 to-blue-600',
    borderColor: 'border-cyan-500',
    bgColor: 'bg-cyan-500/10',
    summary: 'Tüm onaylı ve taslak sözleşmelerin listelenmesi, filtreleme ve yazdırılabilir fatura.',
    whatItDoes: 'Geçmiş ve gelecek tüm düğün kayıtlarını arama, durum bazlı filtreleme ve resmi sözleşme çıktısı alma imkanı sunar.',
    connectedNodes: ['page-create-reservation', 'page-calendar', 'page-finance', 'page-reports-ai'],
    readsState: ['reservations', 'venues', 'customers', 'services'],
    mutatesState: ['reservations'],
    whichFeatures: [
      'Arama & Filtreleme (Sözleşme No, Müşteri Adı, Salon, Tarih Aralığı)',
      'Fatura & Resmi Sözleşme Yazdırma Modalı (A4 Formatlı Print View)',
      'Sözleşme Düzenleme & İptal Etme / Silme (RedAlert Güvenlik Onayı)',
      'Tarih / Seans Değiştirme (Reschedule Engine)'
    ],
    whyWeBuiltIt: 'Salon resepsiyonunun sözleşmeleri tek tıkla arayıp bulması ve müşteriye anında yazdırılabilir çıktı sunması için tasarladık.',
    rulesAndCore: [
      'Kural 1: İptal edilen rezervasyonlar silinmeden önce onay modalı çıkarılmalıdır.',
      'Kural 2: Yazdır butonuna basıldığında A4 formatında temiz fatura şablonu üretilmelidir.'
    ],
    stepByStepFlow: [
      '1. Adım: Rezervasyonlar listesinden ilgili sözleşme bulunur.',
      '2. Adım: "Yazdır" butonuna basılarak resmi PDF/A4 sözleşme çıktısı alınır.',
      '3. Adım: Gerekirse "Tarih Değiştir" veya "Düzenle" ile kayıt güncellenir.'
    ],
    relatedRoute: 'reservations'
  },
  {
    id: 'page-calendar',
    title: 'Dinamik Takvim Yönetimi',
    icon: 'calendar',
    fallbackEmoji: '📅',
    category: 'Pages',
    color: 'from-amber-500 to-orange-600',
    borderColor: 'border-amber-500',
    bgColor: 'bg-amber-500/10',
    summary: 'Aylık/Haftalık görsel düğün takvimi, sürükle-bırak tarih değiştirme.',
    whatItDoes: 'Düğün salonlarının hangi gün ve hangi saat diliminde (Gündüz/Gece) dolu olduğunu takvim üzerinde gösterir.',
    connectedNodes: ['page-create-reservation', 'page-reservations', 'page-venues'],
    readsState: ['reservations', 'venues'],
    mutatesState: ['reservations'],
    whichFeatures: [
      'Dinamik Ay Navigasyonu (Önceki Ay / Bugün / Sonraki Ay)',
      'Salon Bazlı Renkli Etiketleme (Altın Salon, Balo Salonu, vb.)',
      'Boş Gün Tıklaması ile Hızlı Rezervasyon Başlatma',
      'Düğün Günü Detay Popupı (Müşteri, Misafir Sayısı, Kalan Bakiye)'
    ],
    whyWeBuiltIt: 'Müşteriler telefonla tarih sorduğunda hangi salonun ne zaman boş olduğunu saniyeler içinde görebilmek için geliştirdik.',
    rulesAndCore: [
      'Kural 1: Çift rezervasyon (çakışma) durumunda takvim günü kırmızı uyarı vermelidir.',
      'Kural 2: Takvim dinamik ay gün sayısı ve ilk gün indisini doğru hesaplamalıdır.'
    ],
    stepByStepFlow: [
      '1. Adım: Takvimden aranılan ay ve yıla geçilir.',
      '2. Adım: İlgili güne tıklanarak kayıtlı düğün detayları incelenir.',
      '3. Adım: Boş bir güne tıklanarak doğrudan rezervasyon sihirbazı başlatılır.'
    ],
    relatedRoute: 'calendar'
  },
  {
    id: 'page-finance',
    title: 'Finans & Kasa Yönetimi',
    icon: 'finance',
    fallbackEmoji: '💰',
    category: 'Pages',
    color: 'from-emerald-600 to-green-700',
    borderColor: 'border-emerald-600',
    bgColor: 'bg-emerald-600/10',
    summary: 'Gelir/Gider tablosu, net kar hesabı, harcama kaydı ekleme modalı.',
    whatItDoes: 'Düğün kaporalarını, kalan tahsilatları ve orkestra/ikram/personel giderlerini tek kasada yönetir.',
    connectedNodes: ['page-reservations', 'page-reports-ai', 'page-dashboard'],
    readsState: ['reservations', 'financialStats'],
    mutatesState: ['financialStats'],
    whichFeatures: [
      'KPI Kartları: Toplam Ciro, Toplam Gider, Net Kar (Ciro - Gider), Tahsil Edilen Kapora',
      'Birleşik Gelir & Gider İşlem Tablosu (Tarih, Açıklama, Kategori, Tür, Tutar, Durum)',
      'Canlı Arama & Filtreleme (Tümü / Gelirler (+) / Giderler (-))',
      '+ Gider Kaydı Ekle Modalı (Harcama başlığı, Kategori, Tutar, Tarih, Ödeme Durumu)'
    ],
    whyWeBuiltIt: 'Düğün salonunun anlık nakit akışını, kaporaları ve organizasyon maliyetlerini şeffaf şekilde takip etmek için kurduk.',
    rulesAndCore: [
      'Kural 1: Net Kar = Toplam Ciro - Toplam Gider formülüyle canlı hesaplanmalıdır.',
      'Kural 2: Yeni gider eklendiğinde finansal göstergeler anında güncellenmelidir.'
    ],
    stepByStepFlow: [
      '1. Adım: Finans sayfasına girilir, anlık ciro ve gider görülür.',
      '2. Adım: "+ Gider Kaydı Ekle" butonuna basılarak orkestra veya ikram harcaması yazılır.',
      '3. Adım: Net kar göstergesi otomatik güncellenir.'
    ],
    relatedRoute: 'finans'
  },
  {
    id: 'page-reports-ai',
    title: 'Raporlar & AI Analytics',
    icon: 'chart',
    fallbackEmoji: '📈',
    category: 'Pages',
    color: 'from-violet-500 to-purple-700',
    borderColor: 'border-violet-500',
    bgColor: 'bg-violet-500/10',
    summary: 'SVG grafikleri, dinamik doluluk oranları ve Tek Tıkla Kampanya Dönüştürme.',
    whatItDoes: 'Rezervasyon verilerini analiz eder, SVG Gelir ve Salon grafikleri üretir, AI tavsiyeleri sunar.',
    connectedNodes: ['page-finance', 'page-campaigns', 'page-dashboard'],
    readsState: ['reservations', 'venues', 'services'],
    mutatesState: ['campaigns', 'venues'],
    whichFeatures: [
      'Dinamik Doluluk Oranı Hesabı (occupancyRate)',
      'Donut SVG Gelir Dağılımı Grafiği Kartı',
      'Bar SVG Salon Tercih Oranları Grafiği Kartı',
      'AI Öneri Kartları ("Tek Tıkla Kampanyaya Dönüştür" ve "Fiyat Güncelle & Uygula")'
    ],
    whyWeBuiltIt: 'Yapay zekanın boş günleri tespit edip salon sahibine stratejik kampanya ve fiyat önerileri sunması için tasarladık.',
    rulesAndCore: [
      'Kural 1: "Tek Tıkla Kampanyaya Dönüştür" butonuna tıklandığında kampanya anında eklenmeli ve Kampanyalar sayfasına yönlendirilmelidir.',
      'Kural 2: Grafikler CSS/SVG ile responsive olarak çizilmelidir.'
    ],
    stepByStepFlow: [
      '1. Adım: Raporlar sayfasına girilir, grafikler ve doluluk incelenir.',
      '2. Adım: AI öneri kartındaki "Kampanyaya Dönüştür" butonuna basılır.',
      '3. Adım: Otomatik olarak Kampanyalar sayfasına yeni indirim kodu tanımlanır.'
    ],
    relatedRoute: 'raporlar-ai'
  },
  {
    id: 'page-campaigns',
    title: 'Kampanyalar & AI İndirimler',
    icon: 'sparkles',
    fallbackEmoji: '🏷️',
    category: 'Pages',
    color: 'from-rose-500 to-pink-600',
    borderColor: 'border-rose-500',
    bgColor: 'bg-rose-500/10',
    summary: 'İndirim kodları, erken rezervasyon kampanyaları ve AI önerili promosyonlar.',
    whatItDoes: 'Rezervasyon sırasında uygulanabilecek indirim kodlarını ve şartlarını yönetir.',
    connectedNodes: ['page-reports-ai', 'page-create-reservation'],
    readsState: ['campaigns'],
    mutatesState: ['campaigns'],
    whichFeatures: [
      'Aktif & Pasif Kampanya Listesi (İndirim Oranı, Son Geçerlilik Tarihi)',
      'Yeni Kampanya Tanımlama Modalı',
      'AI Otomatik Üretilmiş Kampanya Rozeti'
    ],
    whyWeBuiltIt: 'Düğün sezonu dışı aylarda ve hafta içi günlerde doluluk oranını artıracak esnek kampanyalar oluşturabilmek için tasarladık.',
    rulesAndCore: [
      'Kural 1: Süresi geçen veya pasif olan kampanyalar rezervasyon sihirbazında uygulanamaz.'
    ],
    stepByStepFlow: [
      '1. Adım: Kampanyalar sayfasından indirim kodu ve geçerlilik tarihi oluşturulur.',
      '2. Adım: Rezervasyon oluştururken müşteriye bu kod uygulanır.'
    ],
    relatedRoute: 'kampanyalar'
  },
  {
    id: 'page-venues',
    title: 'Düğün Salonları Yönetimi',
    icon: 'venue',
    fallbackEmoji: '🏰',
    category: 'Pages',
    color: 'from-yellow-600 to-amber-700',
    borderColor: 'border-yellow-600',
    bgColor: 'bg-yellow-600/10',
    summary: 'Salon kapasiteleri, paket fiyatları, görseller ve detay modalı.',
    whatItDoes: 'İşletmeye ait tüm düğün ve balo salonlarının özelliklerini ve görsellerini sergiler.',
    connectedNodes: ['page-create-reservation', 'page-calendar', 'page-reports-ai'],
    readsState: ['venues'],
    mutatesState: ['venues'],
    whichFeatures: [
      'Salon Kartları (Kapasite, Paket Fiyatı, Alan m²)',
      'Salon Detay Modalı (selectedVenueDetail ile zengin açıklama & galeri)',
      'Yeni Salon Ekleme / Fiyat Düzenleme Modalı'
    ],
    whyWeBuiltIt: 'Müşterilere salonların teknik kapasitesini ve görsellerini prestijli şekilde sunabilmek için geliştirdik.',
    rulesAndCore: [
      'Kural 1: Salon fiyatları değiştiğinde yeni rezervasyonlarda güncel fiyat baz alınmalıdır.'
    ],
    stepByStepFlow: [
      '1. Adım: Salonlar sayfasında ilgilenilen salona tıklanarak detay modalı açılır.',
      '2. Adım: Kapasite ve özellikler müşteriye gösterilir.'
    ],
    relatedRoute: 'dugun-salonlari'
  },
  {
    id: 'page-rbac-settings',
    title: 'Rol & İzin Matrisi (RBAC)',
    icon: 'shield',
    fallbackEmoji: '🔒',
    category: 'Security & Management',
    color: 'from-slate-700 to-slate-900',
    borderColor: 'border-slate-600',
    bgColor: 'bg-slate-500/10',
    summary: 'Rol bazlı erişim denetimi (Süper Admin, Moderatör, İyileştirme Uzmanı).',
    whatItDoes: 'Kullanıcıların hangi sayfaları görebileceğini ve hangi butonlara basabileceğini yetkilendirir.',
    connectedNodes: ['core-arch', 'page-users', 'page-profile'],
    readsState: ['roles', 'tabPermissions', 'activeRole'],
    mutatesState: ['roles', 'tabPermissions', 'activeRole'],
    whichFeatures: [
      'Rol Değiştirme Simülasyonu (Header & Profil üzerinden anlık rol değiştirme)',
      'Sayfa Erişim Hakları Matrisi',
      'Kullanıcı Şifre Yönetimi (UserModalComponent password input alanı)'
    ],
    whyWeBuiltIt: 'Resepsiyon personelinin yetkisiz finansal silme veya sistem ayarlarını değiştirmesini engellemek için kurduk.',
    rulesAndCore: [
      'Kural 1: Yetkisiz bir sayfaya girmeye çalışan kullanıcıya 403 Erişim Engellendi ekranı gösterilmelidir.',
      'Kural 2: Kullanıcı ekleme modalında giriş şifresi alanı zorunlu olmalıdır.'
    ],
    stepByStepFlow: [
      '1. Adım: Ayarlar > Rol & İzinler sekmesine gidilir.',
      '2. Adım: Moderatör rolünün Finans silme izni düzenlenir.',
      '3. Adım: Değişiklikler anında rol matrisine yansır.'
    ],
    relatedRoute: 'ayarlar/rol-izinleri'
  }
];

// STATE DATA DEPENDENCY MATRIX FOR VISUALIZATION
export const DATA_FLOW_MATRIX = [
  {
    stateName: 'reservations',
    label: 'Rezervasyonlar & Sözleşmeler',
    storage: 'LocalStorage (irem_cache_reservations)',
    readers: ['Dashboard', 'Rezervasyon Sihirbazı', 'Rezervasyon Listesi', 'Takvim', 'Finans', 'Raporlar AI', 'Medya Galerisi'],
    mutators: ['Rezervasyon Sihirbazı (Ekle)', 'Rezervasyon Listesi (Düzenle/Sil/Ertele)', 'Takvim (Tarih Değiştir)'],
    description: 'Sistemdeki tüm düğün organizasyonu kayıtlarını, ödeme ve tarih verilerini tutan ana state.'
  },
  {
    stateName: 'venues',
    label: 'Düğün Salonları Listesi',
    storage: 'INITIAL_VENUES + LocalStorage',
    readers: ['Dashboard', 'Rezervasyon Sihirbazı', 'Takvim', 'Salonlar Sayfası', 'Raporlar AI'],
    mutators: ['Salonlar Sayfası (Ekle/Düzenle)', 'Raporlar AI (Fiyat Güncelle)'],
    description: 'Salon isimlerini, kapasitelerini, görsellerini ve varsayılan paket fiyatlarını saklar.'
  },
  {
    stateName: 'services',
    label: 'Ek Hizmetler Kataloğu',
    storage: 'INITIAL_SERVICES + LocalStorage',
    readers: ['Rezervasyon Sihirbazı', 'Ek Hizmetler Sayfası', 'Raporlar AI'],
    mutators: ['Ek Hizmetler Sayfası (Ekle/Düzenle)'],
    description: 'Orkestra, Fotoğrafçı, İkram Menüleri gibi organizasyon opsiyonlarını barındırır.'
  },
  {
    stateName: 'customers',
    label: 'Müşteri Rehberi',
    storage: 'INITIAL_CUSTOMERS + LocalStorage',
    readers: ['Rezervasyon Sihirbazı', 'Müşteri Rehberi Sayfası', 'Rezervasyon Listesi'],
    mutators: ['Müşteri Rehberi Sayfası (Ekle/Düzenle)', 'Rezervasyon Sihirbazı (Yeni Müşteri Kaydı)'],
    description: 'Müşteri ad-soyad, telefon, e-posta ve sözleşme geçmişi kayıtları.'
  },
  {
    stateName: 'campaigns',
    label: 'Kampanyalar & AI Promosyonlar',
    storage: 'INITIAL_CAMPAIGNS + LocalStorage',
    readers: ['Rezervasyon Sihirbazı', 'Kampanyalar Sayfası'],
    mutators: ['Kampanyalar Sayfası (Ekle/Düzenle)', 'Raporlar AI (Tek Tıkla Kampanyaya Dönüştür)'],
    description: 'Rezervasyon sihirbazında uygulanan indirim kodları ve tutarları.'
  },
  {
    stateName: 'financialStats',
    label: 'Kasa & Gider Hareketleri',
    storage: 'LocalStorage (irem_cache_financialStats)',
    readers: ['Finans & Kasa Sayfası', 'Dashboard'],
    mutators: ['Finans Sayfası (+ Gider Kaydı Ekle)'],
    description: 'Gider kalemlerini (Orkestra ödemesi, garson ikramları vb.) ve ciro analizini yönetir.'
  },
  {
    stateName: 'activeRole / tabPermissions',
    label: 'RBAC Yetki & Rol Tanımları',
    storage: 'LocalStorage (irem_cache_roles)',
    readers: ['Tüm Sayfalar (PageErrorBoundary / Header / Sidebar)'],
    mutators: ['Settings (Rol & İzin Matrisi)', 'Header Rol Simülatörü'],
    description: 'Kullanıcının erişebileceği modülleri ve buton aksiyon yetkilerini kısıtlar.'
  }
];

// END-TO-END USER WORKFLOWS
export const E2E_WORKFLOWS = [
  {
    id: 'flow-1',
    title: '📝 1. Yeni Müşteri Sözleşmesi & Rezervasyon Kaydı Akışı',
    color: 'border-purple-500 bg-purple-500/10',
    steps: [
      { num: '01', title: 'Müşteri Seçimi / Ekleme', desc: 'Müşteri rehberinden arama yapılır veya yeni müşteri adı & telefonu girilir.' },
      { num: '02', title: 'Salon & Tarih Belirleme', desc: 'Takvim çakışma kontrolü yapılır, Altın Salon veya Balo Salonu gündüz/gece seansı seçilir.' },
      { num: '03', title: 'Hizmet & Kampanya Ekleme', desc: 'Fotoğraf, Orkestra paketi eklenir. Kampanya kodu (ör. IREM2026) girilerek indirim düşülür.' },
      { num: '04', title: 'Kapora Alımı & Sözleşme', desc: 'Alınan kapora tutarı yazılır. Sistem otomatik A4 formatında resmi sözleşme çıktısı üretir.' },
      { num: '05', title: 'Canlı Yansıma', desc: 'Kayıt anında Takvim, Finans Kasası, Dashboard KPI ve Müşteri Rehberine senkronize olur.' }
    ]
  },
  {
    id: 'flow-2',
    title: '🤖 2. AI Rapor Analizi -> Akıllı Kampanya Dönüştürme Akışı',
    color: 'border-violet-500 bg-violet-500/10',
    steps: [
      { num: '01', title: 'Veri Analizi', desc: 'Raporlar & AI Analytics sayfası rezervasyon verilerinden doluluk oranını (occupancyRate) hesaplar.' },
      { num: '02', title: 'AI Fırsat Tespiti', desc: 'Yapay zeka boş kalan günleri (ör. Hafta içi Salı akşamları) tespit edip indirim önerisi kartı üretir.' },
      { num: '03', title: 'Tek Tıkla Dönüştürme', desc: 'Kullanıcı AI Öneri kartındaki "Tek Tıkla Kampanyaya Dönüştür" butonuna tıklar.' },
      { num: '04', title: 'Kampanya Aktivasyonu', desc: 'Sistem Kampanyalar sayfasına yeni %15 indirim kodu tanımlar ve rezervasyon sihirbazında aktif eder.' }
    ]
  },
  {
    id: 'flow-3',
    title: '💰 3. Finans Kasa Hareketleri & Gider Kaydı Akışı',
    color: 'border-emerald-500 bg-emerald-500/10',
    steps: [
      { num: '01', title: 'Kapora Girişi', desc: 'Rezervasyon yapıldığında alınan kapora otomatik olarak Kasa Gelirleri (+) hanesine yazılır.' },
      { num: '02', title: 'Gider Kaydı Oluşturma', desc: 'Finans sayfasından "+ Gider Kaydı Ekle" butonuna basılarak ikram/garson harcaması girilir.' },
      { num: '03', title: 'Net Kar Hesaplama', desc: 'Sistem Net Kar = Toplam Ciro - Toplam Gider formülünü anlık çalıştırıp KPI kartını günceller.' }
    ]
  },
  {
    id: 'flow-4',
    title: '🛡️ 4. Rol Yetki Değişimi & RBAC Güvenlik Bloklama Akışı',
    color: 'border-slate-500 bg-slate-500/10',
    steps: [
      { num: '01', title: 'Yetki Düzenleme', desc: 'Süper Admin Ayarlar > Rol & İzin Matrisinden Moderatör rolünün Finans silme yetkisini kaldırır.' },
      { num: '02', title: 'Canlı Rol Simülasyonu', desc: 'Header menüsünden "Moderatör" rolü seçilerek sistem bu kimlikle test edilir.' },
      { num: '03', title: '403 Erişim Engeli', desc: 'Moderatör Finans silme butonuna bastığında veya yetkisiz adrese gittiğinde 403 Erişim Engellendi ekranı basılır.' }
    ]
  }
];

export function MindMapPage({ navigateTo }) {
  const [selectedNode, setSelectedNode] = useState(MIND_MAP_DATA[0]);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeCategoryFilter, setActiveCategoryFilter] = useState('ALL');
  const [viewMode, setViewMode] = useState('topology'); // 'topology' | 'matrix' | 'workflows' | 'rbac'
  const [zoomLevel, setZoomLevel] = useState(1);

  const categories = ['ALL', 'Architecture', 'UI/UX System', 'Pages', 'Security & Management'];

  const filteredNodes = MIND_MAP_DATA.filter(node => {
    const matchesSearch = node.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          node.summary.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          node.whichFeatures.some(f => f.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesCat = activeCategoryFilter === 'ALL' || node.category === activeCategoryFilter;
    return matchesSearch && matchesCat;
  });

  // Check if a node is connected to the selected node
  const isConnectedNode = (nodeId) => {
    if (!selectedNode) return false;
    return selectedNode.id === nodeId || 
           (selectedNode.connectedNodes && selectedNode.connectedNodes.includes(nodeId));
  };

  return (
    <div className="space-y-6 relative animate-fade-in pb-12">
      
      {/* PAGE HEADER & VIEW MODE TABS */}
      <div className="bg-white dark:bg-brand-card p-6 rounded-3xl border border-slate-200 dark:border-brand-border shadow-sm space-y-4">
        <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 rounded-2xl bg-amber-500/20 border border-amber-500/40 text-amber-700 dark:text-gold-400 flex items-center justify-center text-2xl font-bold">
              <ThemeIcon icon="sparkles" fallbackEmoji="🧠" className="w-6 h-6 shrink-0" />
            </div>
            <div>
              <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">
                İnteraktif Sistem Zihin Haritası & Veri Akış Topolojisi
              </h2>
              <p className="text-xs text-slate-500 dark:text-gray-400 font-medium">
                Modül Bağlantıları, State Bağımlılıkları, Uçtan Uca Kullanıcı Akışları & Mimari Kılavuz
              </p>
            </div>
          </div>

          {/* VIEW MODE SWITCHER BUTTONS */}
          <div className="flex flex-wrap items-center gap-2 bg-slate-100 dark:bg-brand-dark p-1.5 rounded-2xl border border-slate-200 dark:border-brand-border w-full lg:w-auto">
            <button
              onClick={() => setViewMode('topology')}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 ${
                viewMode === 'topology'
                  ? 'gold-button shadow-xs'
                  : 'text-slate-600 dark:text-gray-400 hover:text-amber-500'
              }`}
            >
              <span>🌳 Topoloji & Ağaç</span>
            </button>

            <button
              onClick={() => setViewMode('workflows')}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 ${
                viewMode === 'workflows'
                  ? 'gold-button shadow-xs'
                  : 'text-slate-600 dark:text-gray-400 hover:text-amber-500'
              }`}
            >
              <span>🔀 Uçtan Uca Akışlar</span>
            </button>

            <button
              onClick={() => setViewMode('matrix')}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 ${
                viewMode === 'matrix'
                  ? 'gold-button shadow-xs'
                  : 'text-slate-600 dark:text-gray-400 hover:text-amber-500'
              }`}
            >
              <span>🔗 Veri & State Matrisi</span>
            </button>

            <button
              onClick={() => setViewMode('rbac')}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 ${
                viewMode === 'rbac'
                  ? 'gold-button shadow-xs'
                  : 'text-slate-600 dark:text-gray-400 hover:text-amber-500'
              }`}
            >
              <span>🛡️ Yetki & RBAC</span>
            </button>
          </div>
        </div>

        {/* CONTROLS & FILTERS (Only shown in topology view) */}
        {viewMode === 'topology' && (
          <div className="pt-3 border-t border-slate-100 dark:border-brand-border/60 flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
            {/* CATEGORY BADGES */}
            <div className="flex items-center space-x-2 overflow-x-auto pb-1 custom-scrollbar w-full md:w-auto">
              {categories.map(cat => (
                <button
                  key={cat}
                  onClick={() => setActiveCategoryFilter(cat)}
                  className={`px-3 py-1 rounded-xl text-xs font-bold transition whitespace-nowrap ${
                    activeCategoryFilter === cat
                      ? 'bg-amber-500 text-white shadow-xs'
                      : 'bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-400 border border-slate-200 dark:border-brand-border hover:border-amber-500'
                  }`}
                >
                  {cat === 'ALL' ? '🌐 Tüm Modüller' : cat}
                </button>
              ))}
            </div>

            {/* SEARCH & ZOOM */}
            <div className="flex items-center space-x-3 w-full md:w-auto">
              <div className="relative flex-1 md:w-56">
                <input
                  type="text"
                  placeholder="Zihin Haritasında Ara..."
                  value={searchQuery}
                  onChange={e => setSearchQuery(e.target.value)}
                  className="w-full pl-8 pr-3 py-1.5 bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl text-xs font-bold focus:outline-none focus:border-amber-500 text-slate-800 dark:text-white"
                />
                <span className="absolute left-2.5 top-2 text-slate-400 text-xs">
                  <ThemeIcon icon="search" fallbackEmoji="🔍" className="w-3.5 h-3.5 opacity-60" />
                </span>
              </div>

              <div className="flex items-center space-x-1 bg-slate-100 dark:bg-brand-dark p-1 rounded-xl border border-slate-200 dark:border-brand-border">
                <button
                  onClick={() => setZoomLevel(prev => Math.max(0.7, prev - 0.1))}
                  className="px-2 py-0.5 text-xs font-bold hover:bg-amber-500/20 rounded"
                  title="Uzaklaş"
                >
                  -
                </button>
                <span className="text-[10px] font-mono font-bold px-1 text-slate-800 dark:text-white">{Math.round(zoomLevel * 100)}%</span>
                <button
                  onClick={() => setZoomLevel(prev => Math.min(1.3, prev + 0.1))}
                  className="px-2 py-0.5 text-xs font-bold hover:bg-amber-500/20 rounded"
                  title="Yakınlaş"
                >
                  +
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* VIEW 1: TOPOLOGY & MIND MAP CANVAS */}
      {viewMode === 'topology' && (
        <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border shadow-sm min-h-[620px] overflow-auto custom-scrollbar relative">
          
          <div
            style={{ transform: `scale(${zoomLevel})`, transformOrigin: 'top left' }}
            className="transition-transform duration-200 space-y-8"
          >
            {/* ROOT NODE (CENTER SYSTEM ROOT) */}
            <div className="flex justify-center">
              <div className="bg-gradient-to-r from-amber-500 via-amber-600 to-yellow-600 text-white p-5 rounded-3xl shadow-xl border-4 border-amber-300 dark:border-amber-400/40 text-center max-w-md">
                <div className="text-3xl mb-1 flex justify-center">
                  <ThemeIcon icon="venue" fallbackEmoji="🏰" className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-lg font-heading font-black tracking-wide">
                  İREM DÜĞÜN SARAYI CORE ECOSYSTEM
                </h3>
                <p className="text-[11px] text-amber-100 font-medium mt-1">
                  Çift Mimarili Dijital Yönetim & Organizasyon Platformu
                </p>
                <div className="mt-2 text-[10px] bg-black/20 py-1 px-3 rounded-full inline-block font-mono">
                  Seçili Modül: <strong className="text-gold-400">{selectedNode?.title}</strong> (Bağlantılı modüller parlar)
                </div>
              </div>
            </div>

            {/* CONNECTOR LINE SVG */}
            <div className="w-full flex justify-center opacity-30">
              <div className="w-0.5 h-8 bg-amber-500"></div>
            </div>

            {/* BRANCH NODES GRID */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredNodes.map(node => {
                const isSelected = selectedNode?.id === node.id;
                const connected = isConnectedNode(node.id);

                return (
                  <div
                    key={node.id}
                    onClick={() => setSelectedNode(node)}
                    className={`p-5 rounded-2xl border-2 transition-all cursor-pointer relative group ${
                      isSelected
                        ? `${node.borderColor} bg-white dark:bg-brand-card shadow-2xl scale-[1.03] ring-4 ring-amber-500/30 z-10`
                        : connected
                        ? 'border-amber-400 dark:border-amber-500/80 bg-amber-50/40 dark:bg-amber-950/20 shadow-md scale-[1.01]'
                        : 'border-slate-200 dark:border-brand-border bg-white dark:bg-brand-card hover:border-amber-500/60 shadow-xs'
                    }`}
                  >
                    {/* TOP BADGES */}
                    <div className="flex justify-between items-center mb-3">
                      <span className={`text-[10px] font-extrabold px-2.5 py-0.5 rounded-full ${node.bgColor} text-amber-700 dark:text-gold-400 border border-amber-500/30 uppercase tracking-wider`}>
                        {node.category}
                      </span>
                      {isSelected ? (
                        <span className="text-[10px] font-bold text-amber-600 bg-amber-100 dark:bg-amber-900/40 px-2 py-0.5 rounded-full animate-pulse">
                          🎯 Aktif Seçim
                        </span>
                      ) : connected ? (
                        <span className="text-[10px] font-bold text-amber-600 dark:text-gold-400 bg-amber-500/10 px-2 py-0.5 rounded-full">
                          🔗 Bağlantılı
                        </span>
                      ) : null}
                    </div>

                    {/* TITLE & SUMMARY */}
                    <div className="flex items-center space-x-2 mb-1">
                      <ThemeIcon icon={node.icon} fallbackEmoji={node.fallbackEmoji} className="w-5 h-5 text-amber-500 shrink-0" />
                      <h4 className="font-heading font-bold text-base text-slate-900 dark:text-white group-hover:text-amber-600 transition">
                        {node.title}
                      </h4>
                    </div>
                    <p className="text-xs text-slate-500 dark:text-gray-400 line-clamp-2 font-medium">
                      {node.summary}
                    </p>

                    {/* STATE DEPENDENCY CHIPS */}
                    <div className="mt-3 pt-2 border-t border-slate-100 dark:border-brand-border/40 flex flex-wrap gap-1">
                      {node.readsState?.map(st => (
                        <span key={st} className="text-[9px] bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-400 px-1.5 py-0.5 rounded font-mono">
                          👁️ {st}
                        </span>
                      ))}
                      {node.mutatesState?.map(st => (
                        <span key={st} className="text-[9px] bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 px-1.5 py-0.5 rounded font-mono font-bold">
                          ✏️ {st}
                        </span>
                      ))}
                    </div>

                    {/* BOTTOM ACTION INDICATOR */}
                    <div className="mt-3 flex justify-between items-center text-[11px] font-bold text-amber-600 dark:text-gold-400">
                      <span>İncele & Bağlantıları Gör</span>
                      <span>→</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* VIEW 2: END-TO-END WORKFLOW DIAGRAMS */}
      {viewMode === 'workflows' && (
        <div className="space-y-6">
          {E2E_WORKFLOWS.map(flow => (
            <div key={flow.id} className={`bg-white dark:bg-brand-card p-6 rounded-3xl border-2 ${flow.color} shadow-sm space-y-4`}>
              <h3 className="text-lg font-heading font-extrabold text-slate-900 dark:text-white">
                {flow.title}
              </h3>
              
              <div className="grid grid-cols-1 md:grid-cols-5 gap-3 relative">
                {flow.steps.map((step, idx) => (
                  <div key={idx} className="bg-slate-50 dark:bg-brand-dark p-4 rounded-2xl border border-slate-200 dark:border-brand-border relative flex flex-col justify-between">
                    <div>
                      <div className="w-8 h-8 rounded-xl bg-amber-500 text-white font-black text-xs flex items-center justify-center mb-2 shadow-sm">
                        {step.num}
                      </div>
                      <h4 className="font-bold text-xs text-slate-900 dark:text-white mb-1">
                        {step.title}
                      </h4>
                      <p className="text-[11px] text-slate-500 dark:text-gray-400 leading-relaxed">
                        {step.desc}
                      </p>
                    </div>
                    {idx < flow.steps.length - 1 && (
                      <div className="hidden md:block absolute -right-3 top-1/2 -translate-y-1/2 text-amber-500 text-lg font-bold z-10">
                        ➔
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* VIEW 3: DATA & STATE DEPENDENCY MATRIX */}
      {viewMode === 'matrix' && (
        <div className="bg-white dark:bg-brand-card p-6 rounded-3xl border border-slate-200 dark:border-brand-border shadow-sm space-y-4">
          <div>
            <h3 className="text-xl font-heading font-extrabold text-slate-900 dark:text-white">
              🔗 Hangi Değer Nereye Bağlı? (State Bağımlılık Matrisi)
            </h3>
            <p className="text-xs text-slate-500 dark:text-gray-400">
              Sistemdeki ana state değişkenleri, nereden beslendikleri, hangi modüllerce okundukları ve güncellendikleri
            </p>
          </div>

          <div className="overflow-x-auto custom-scrollbar">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 font-extrabold uppercase border-b border-slate-200 dark:border-brand-border">
                <tr>
                  <th className="p-3">State Değişkeni</th>
                  <th className="p-3">Açıklama & Depo</th>
                  <th className="p-3 text-blue-600 dark:text-blue-400">Veriyi Okuyan Modüller (Readers)</th>
                  <th className="p-3 text-emerald-600 dark:text-emerald-400">Veriyi Değiştiren Modüller (Mutators)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-brand-border/40">
                {DATA_FLOW_MATRIX.map(row => (
                  <tr key={row.stateName} className="hover:bg-slate-50 dark:hover:bg-brand-dark/40 transition">
                    <td className="p-3 font-mono font-bold text-amber-600 dark:text-gold-400 whitespace-nowrap">
                      {row.stateName}
                    </td>
                    <td className="p-3">
                      <div className="font-bold text-slate-800 dark:text-white">{row.label}</div>
                      <div className="text-[10px] text-slate-400 font-mono">{row.storage}</div>
                    </td>
                    <td className="p-3">
                      <div className="flex flex-wrap gap-1">
                        {row.readers.map(r => (
                          <span key={r} className="bg-blue-500/10 text-blue-700 dark:text-blue-300 px-2 py-0.5 rounded text-[10px] font-semibold">
                            {r}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="p-3">
                      <div className="flex flex-wrap gap-1">
                        {row.mutators.map(m => (
                          <span key={m} className="bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 px-2 py-0.5 rounded text-[10px] font-semibold">
                            {m}
                          </span>
                        ))}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* VIEW 4: SECURITY & RBAC SCHEME */}
      {viewMode === 'rbac' && (
        <div className="bg-white dark:bg-brand-card p-6 rounded-3xl border border-slate-200 dark:border-brand-border shadow-sm space-y-6">
          <div>
            <h3 className="text-xl font-heading font-extrabold text-slate-900 dark:text-white">
              🛡️ Rol Bazlı Erişim Denetim Şeması (RBAC Hierarchy)
            </h3>
            <p className="text-xs text-slate-500 dark:text-gray-400">
              Kullanıcı rollerinin sistemdeki yetki sınırları ve korunan modüller
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-amber-500/10 border border-amber-500/40 p-5 rounded-2xl space-y-3">
              <span className="text-xs font-black bg-amber-500 text-white px-3 py-1 rounded-full uppercase tracking-wider">
                👑 Süper Admin (SuperAdmin)
              </span>
              <h4 className="font-bold text-sm text-slate-900 dark:text-white">Tam Sistem Yetkisi</h4>
              <p className="text-xs text-slate-600 dark:text-gray-300">
                Tüm sayfaları görüntüleme, rezervasyon ve finansal kayıt silme, rol izin matrisini değiştirme yetkisi.
              </p>
            </div>

            <div className="bg-blue-500/10 border border-blue-500/40 p-5 rounded-2xl space-y-3">
              <span className="text-xs font-black bg-blue-500 text-white px-3 py-1 rounded-full uppercase tracking-wider">
                🛡️ Moderatör (Moderator)
              </span>
              <h4 className="font-bold text-sm text-slate-900 dark:text-white">Operasyonel Yönetim</h4>
              <p className="text-xs text-slate-600 dark:text-gray-300">
                Rezervasyon ve müşteri ekleme/düzenleme yapar. Finans silme ve RBAC ayarları yetkisi kısıtlanabilir.
              </p>
            </div>

            <div className="bg-slate-500/10 border border-slate-500/40 p-5 rounded-2xl space-y-3">
              <span className="text-xs font-black bg-slate-600 text-white px-3 py-1 rounded-full uppercase tracking-wider">
                👤 Resepsiyon / Satışçı
              </span>
              <h4 className="font-bold text-sm text-slate-900 dark:text-white">Sınırlı Veri Girişi</h4>
              <p className="text-xs text-slate-600 dark:text-gray-300">
                Sadece yeni rezervasyon oluşturma ve takvim inceleme yapabilir. Finans ve ayarlar sayfasına erişimi engellenebilir (403).
              </p>
            </div>
          </div>
        </div>
      )}

      {/* INSPECTOR SIDE-SHEET DRAWER FOR SELECTED NODE */}
      {selectedNode && (
        <div className="fixed inset-y-0 right-0 w-full sm:w-[500px] bg-white dark:bg-brand-card border-l border-slate-200 dark:border-brand-border shadow-2xl z-50 flex flex-col animate-slide-in-right">
          {/* DRAWER HEADER */}
          <div className="p-6 border-b border-slate-200 dark:border-brand-border flex justify-between items-start bg-slate-50 dark:bg-brand-dark/50">
            <div>
              <span className="text-[10px] font-extrabold px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-700 dark:text-gold-400 border border-amber-500/30 uppercase tracking-wider">
                {selectedNode.category}
              </span>
              <div className="flex items-center space-x-2 mt-2">
                <ThemeIcon icon={selectedNode.icon} fallbackEmoji={selectedNode.fallbackEmoji} className="w-6 h-6 text-amber-500 shrink-0" />
                <h3 className="text-xl font-heading font-extrabold text-slate-900 dark:text-white">
                  {selectedNode.title}
                </h3>
              </div>
            </div>
            <button
              onClick={() => setSelectedNode(null)}
              className="w-8 h-8 rounded-full bg-slate-200 dark:bg-brand-dark text-slate-600 dark:text-gray-300 font-bold hover:bg-red-500 hover:text-white transition flex items-center justify-center text-sm"
            >
              ✕
            </button>
          </div>

          {/* QUICK NAVIGATE ACTION BAR */}
          <div className="p-4 bg-amber-500/10 border-b border-amber-500/20 flex justify-between items-center">
            <span className="text-xs font-bold text-amber-800 dark:text-gold-400">
              Bu modülü canlı sistemde denemek ister misiniz?
            </span>
            <button
              onClick={() => {
                if (navigateTo && selectedNode.relatedRoute) {
                  navigateTo(selectedNode.relatedRoute);
                }
              }}
              className="gold-button font-bold text-xs py-1.5 px-4 rounded-xl shadow-sm flex items-center space-x-1"
            >
              <span>🚀 Sayfaya Git</span>
            </button>
          </div>

          {/* DRAWER BODY CONTENT */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar">
            
            {/* CONNECTED NODES CHIPS */}
            {selectedNode.connectedNodes && selectedNode.connectedNodes.length > 0 && (
              <div className="space-y-2">
                <h4 className="font-bold text-xs text-amber-700 dark:text-gold-400 uppercase tracking-wider">
                  🔗 Doğrudan Etkileşimde Olduğu Modüller
                </h4>
                <div className="flex flex-wrap gap-2">
                  {selectedNode.connectedNodes.map(cId => {
                    const targetNode = MIND_MAP_DATA.find(n => n.id === cId);
                    if (!targetNode) return null;
                    return (
                      <button
                        key={cId}
                        onClick={() => setSelectedNode(targetNode)}
                        className="text-xs bg-amber-500/10 hover:bg-amber-500/20 text-amber-800 dark:text-gold-400 px-3 py-1 rounded-xl border border-amber-500/30 transition flex items-center space-x-1 font-semibold"
                      >
                        <span>• {targetNode.title}</span>
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            {/* READS & MUTATES STATE */}
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-slate-50 dark:bg-brand-dark p-3 rounded-2xl border border-slate-200 dark:border-brand-border">
                <div className="text-[10px] font-bold text-blue-600 dark:text-blue-400 uppercase mb-1">
                  👁️ Okuduğu State (Reads)
                </div>
                <div className="flex flex-wrap gap-1">
                  {selectedNode.readsState?.map(s => (
                    <span key={s} className="text-[10px] font-mono bg-blue-500/10 text-blue-700 dark:text-blue-300 px-1.5 py-0.5 rounded">
                      {s}
                    </span>
                  )) || <span className="text-xs text-gray-400">Yok</span>}
                </div>
              </div>

              <div className="bg-slate-50 dark:bg-brand-dark p-3 rounded-2xl border border-slate-200 dark:border-brand-border">
                <div className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 uppercase mb-1">
                  ✏️ Değiştirdiği State (Mutates)
                </div>
                <div className="flex flex-wrap gap-1">
                  {selectedNode.mutatesState?.map(s => (
                    <span key={s} className="text-[10px] font-mono bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 px-1.5 py-0.5 rounded">
                      {s}
                    </span>
                  )) || <span className="text-xs text-gray-400">Yok</span>}
                </div>
              </div>
            </div>

            {/* WHAT IT DOES */}
            <div className="space-y-2">
              <h4 className="font-bold text-xs text-amber-700 dark:text-gold-400 uppercase tracking-wider">
                📌 Modülün Görevi & Amacı
              </h4>
              <p className="text-xs text-slate-700 dark:text-gray-300 leading-relaxed font-medium bg-slate-50 dark:bg-brand-dark p-3 rounded-2xl border border-slate-200 dark:border-brand-border">
                {selectedNode.whatItDoes}
              </p>
            </div>

            {/* FEATURES */}
            <div className="space-y-2">
              <h4 className="font-bold text-xs text-amber-700 dark:text-gold-400 uppercase tracking-wider">
                ✨ İçerdiği Alt Özellikler
              </h4>
              <ul className="space-y-2">
                {selectedNode.whichFeatures.map((feat, idx) => (
                  <li key={idx} className="text-xs text-slate-700 dark:text-gray-300 flex items-start space-x-2 bg-slate-50 dark:bg-brand-dark p-2.5 rounded-xl border border-slate-100 dark:border-brand-border/40 font-medium">
                    <span className="text-amber-500 font-bold">•</span>
                    <span>{feat}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* RULES */}
            <div className="space-y-2">
              <h4 className="font-bold text-xs text-amber-700 dark:text-gold-400 uppercase tracking-wider">
                🛡️ İş Mantığı & Kritik Kurallar
              </h4>
              <ul className="space-y-2">
                {selectedNode.rulesAndCore.map((rule, idx) => (
                  <li key={idx} className="text-xs text-amber-900 dark:text-amber-200 bg-amber-500/10 p-2.5 rounded-xl border border-amber-500/30 font-medium">
                    {rule}
                  </li>
                ))}
              </ul>
            </div>

            {/* STEP BY STEP FLOW */}
            <div className="space-y-2">
              <h4 className="font-bold text-xs text-amber-700 dark:text-gold-400 uppercase tracking-wider">
                🔄 Adım Adım Kullanım Adımları
              </h4>
              <div className="space-y-2">
                {selectedNode.stepByStepFlow.map((step, idx) => (
                  <div key={idx} className="text-xs text-slate-700 dark:text-gray-300 bg-slate-50 dark:bg-brand-dark p-2.5 rounded-xl border border-slate-200 dark:border-brand-border font-medium">
                    {step}
                  </div>
                ))}
              </div>
            </div>

          </div>

          {/* DRAWER FOOTER */}
          <div className="p-4 border-t border-slate-200 dark:border-brand-border bg-slate-50 dark:bg-brand-dark/50 flex justify-end">
            <button
              onClick={() => setSelectedNode(null)}
              className="px-4 py-2 bg-slate-200 dark:bg-brand-dark text-slate-700 dark:text-gray-300 rounded-xl text-xs font-bold hover:bg-slate-300 transition"
            >
              Kapat
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
