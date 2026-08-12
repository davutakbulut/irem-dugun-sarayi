import os

new_nodes = """  {
    id: 'page-quote-requests',
    title: 'Teklif Talepleri & Leads (WhatsApp Motoru)',
    icon: 'crown',
    fallbackEmoji: '',
    category: 'Lead Management',
    color: 'from-amber-600 to-yellow-700',
    borderColor: 'border-amber-600',
    bgColor: 'bg-amber-600/10',
    summary: 'Ön yüzdeki 4 adımlı lüks LeadModal ve WhatsApp entegreli müşteri teklif talepleri paneli.',
    whatItDoes: 'Kamu ön yüzünden (Header ve Hero) gelen düğün ve davet fiyat teklif taleplerini veritabanında toplar, durum takibi ve tek tıkla Rezervasyona Dönüştürme sağlar.',
    connectedNodes: ['public-front-end', 'page-create-reservation', 'page-customers', 'mysql-backend-resilience'],
    readsState: ['quoteRequests', 'venues'],
    mutatesState: ['quoteRequests', 'reservations'],
    whichFeatures: [
      '4 Adımlı Ekran Ortalamalı Portallı Teklif Al Modalı (LeadModal)',
      'Otomatik WhatsApp Chat Mesajı Metin Oluşturucu (wa.me/905471440054)',
      'Teklif Talepleri Yönetim Paneli (Teklif Talepleri / Leads)',
      'Tek Tıkla "Rezervasyona Dönüştür" Aksiyonu & Durum Filtreleme (Beklemede, Görüşüldü, Onaylandı)'
    ],
    whyWeBuiltIt: 'Web sitemize gelen potansiyel müşteri adaylarını anında WhatsApp temsilcimize bağlamak ve yönetim panelinde kayıt altına alıp rezervasyona dönüştürmek için geliştirdik.',
    rulesAndCore: [
      'Kural 1: "Ücretsiz Teklif Al" butonuna basıldığında talep hem MySQL veritabanına kaydedilmeli hem de WhatsApp sohbeti başlatmalıdır.',
      'Kural 2: "Rezervasyona Dönüştür" seçildiğinde müşteri bilgileri otomatik Rezervasyon Sihirbazına aktarılmalıdır.'
    ],
    stepByStepFlow: [
      '1. Adım: Ziyaretçi ön yüzdeki "Teklif Al" butonuna basar, 4 adımlı açık renkli modal açılır.',
      '2. Adım: Form doldurulunca veri kaydedilir ve WhatsApp yönlendirmesi gerçekleşir.',
      '3. Adım: Yönetim panelindeki Teklif Talepleri sayfasından müşteri adayı takip edilir ve rezervasyona dönüştürülür.'
    ],
    relatedRoute: 'teklif-talepleri'
  },
  {
    id: 'public-front-end',
    title: 'Kamu Ön Yüzü & 90vw Mobil Çekmece',
    icon: 'venue',
    fallbackEmoji: '',
    category: 'Public Site',
    color: 'from-emerald-500 to-teal-700',
    borderColor: 'border-emerald-500',
    bgColor: 'bg-emerald-500/10',
    summary: '6 Bağımsız Semantik Section, 90vw Cam Mobil Çekmece ve Resmî WhatsApp Widget.',
    whatItDoes: 'Görsel açıdan büyüleyici, Sapanca Göl kıyısı lüks balo tesisini tanıtan kamu ön yüzünü ve mobil navigasyonu sunar.',
    connectedNodes: ['page-quote-requests', 'wedding-error-pages', 'theme-iconography'],
    readsState: ['venues', 'services', 'reviews'],
    mutatesState: [],
    whichFeatures: [
      '6 Standalone Semantik Bölüm: #section-hero, #section-welcome, #section-services, #section-halls, #section-menus, #section-testimonials',
      '90vw Sağdan Kayarak Açılan Cam Mobil Çekmece (PublicNavbar)',
      'Resmî WhatsApp Canlı Destek Widget (PublicFooter & 360° Dönme Animasyonu)',
      'Video Hero Background & #25D366 Kurumsal Yeşil WhatsApp CTA Butonu'
    ],
    whyWeBuiltIt: 'Ziyaretçileri ilk bakışta etkilemek, mobil cihazlarda mükemmel bir navigasyon sunmak ve rezervasyon dönüşümünü maksimuma çıkarmak için inşa ettik.',
    rulesAndCore: [
      'Kural 1: Mobil menü açıldığında ekran kaydırma kilitlenmeli, masaüstü bağlantıları ile %100 senkronize çalışmalıdır.',
      'Kural 2: Header ve Hero Teklif Al butonları birebir aynı Portallı LeadModal bileşenini açmalıdır.'
    ],
    stepByStepFlow: [
      '1. Adım: Ziyaretçi siteye girer, video hero ve canlı tesis görsellerini inceler.',
      '2. Adım: Mobilde sağdaki menü butonuna basarak 90vw cam çekmeceyi açar.',
      '3. Adım: Teklif Al veya WhatsApp butonlarıyla doğrudan iletişim kurar.'
    ],
    relatedRoute: 'public-home'
  },
  {
    id: 'wedding-error-pages',
    title: 'Düğün Temalı Hata Sayfaları & Catch-All',
    icon: 'warning',
    fallbackEmoji: '',
    category: 'Security & Routing',
    color: 'from-rose-600 to-red-700',
    borderColor: 'border-rose-600',
    bgColor: 'bg-rose-600/10',
    summary: 'NotFoundPage (404), ServerErrorPage (500), ForbiddenPage (403) ve Catch-All Router.',
    whatItDoes: 'Sitede bulunmayan veya yetkisiz sayfalara erişilmeye çalışıldığında düğün konseptli şık hata sayfaları gösterir.',
    connectedNodes: ['public-front-end', 'core-arch'],
    readsState: [],
    mutatesState: [],
    whichFeatures: [
      'NotFoundPage (404): "Aradığınız Sayfa Bir Düğün Masalı Gibi Kayboldu..."',
      'ServerErrorPage (500): "Orkestramız Kısa Bir Mola Verdi..."',
      'ForbiddenPage (403): "VIP Gelin & Damat Odasına İzinsiz Giriş Engellendi"',
      'Catch-All Router: Yanlış URL isteklerini otomatik yakalayıp 404 PublicLayout içine yönlendirme'
    ],
    whyWeBuiltIt: 'Hata durumlarında bile marka prestijini korumak ve kullanıcıyı siteden kaçırmadan ana sayfaya yönlendirmek için geliştirdik.',
    rulesAndCore: [
      'Kural 1: Olmayan tüm harici bağlantılar (/invalid-page, /xyz) otomatik 404 masal sayfasına yönlendirilmelidir.',
      'Kural 2: Hata sayfaları kamu teması (PublicLayout) içinde altın taç ikonlarıyla estetik sunulmalıdır.'
    ],
    stepByStepFlow: [
      '1. Adım: Kullanıcı hatalı bir URL yazar.',
      '2. Adım: Catch-All yönlendirici isteği yakalar ve NotFoundPage bileşenini yükler.',
      '3. Adım: Kullanıcı "Ana Sayfaya Dön" veya "Salona Git" butonuyla akışa geri katılır.'
    ],
    relatedRoute: '404'
  },
  {
    id: 'mysql-backend-resilience',
    title: 'MySQL DB & Plesk POST-Delete Resilience',
    icon: 'settings',
    fallbackEmoji: '',
    category: 'Backend & Server',
    color: 'from-blue-600 to-indigo-800',
    borderColor: 'border-blue-600',
    bgColor: 'bg-blue-600/10',
    summary: 'Express + MySQL Veritabanı, IIS/Plesk HTTP DELETE 403 engeli için POST Fallback Middleware.',
    whatItDoes: 'Tüm rezervasyon, müşteri, hizmet, kullanıcı ve taslak verilerini MySQL veritabanında saklar ve sunucu güvenliğini yönetir.',
    connectedNodes: ['core-arch', 'user-profile-db-sync', 'page-reservations', 'page-quote-requests'],
    readsState: ['poolActive', 'dbStatus'],
    mutatesState: ['reservations', 'draftReservations', 'users'],
    whichFeatures: [
      'MySQL İlişkisel Veritabanı Bağlantı Havuzu (mysql2 Connection Pool)',
      'Plesk/IIS POST Fallback Middleware (HTTP DELETE 403 Forbidden engeline karşı otomatik POST dönüştürme)',
      'window.fetchWithRetry Dayanıklılık Katmanı (403/404/500 durumlarında otomatik sessiz tolerans)',
      'web.config Otomatik IIS Yeniden Başlatma Tetikleyicisi'
    ],
    whyWeBuiltIt: 'Plesk ve WAF güvenlik duvarlarının DELETE isteklerini engellemesini tamamen çözmek ve verileri kalıcı MySQL veritabanında saklamak için inşa ettik.',
    rulesAndCore: [
      'Kural 1: DELETE istekleri engellendiğinde sistem kesintiye uğramadan POST kanalıyla veriyi silmelidir.',
      'Kural 2: MySQL bağlantısı koptuğunda bellek deposu (memoryStore) devreye girerek kesintisiz hizmet vermelidir.'
    ],
    stepByStepFlow: [
      '1. Adım: Ön yüz silme veya kaydetme isteği gönderir.',
      '2. Adım: Sunucu isteği MySQL veritabanına yansıtır.',
      '3. Adım: Plesk DELETE engeli verirse POST fallback ara katmanı devreye girerek işlemi başarıyla tamamlar.'
    ],
    relatedRoute: 'settings-performance'
  },
  {
    id: 'user-profile-db-sync',
    title: 'Veritabanı Senkronizeli Profil Mimarisi',
    icon: 'user',
    fallbackEmoji: '',
    category: 'Security & Management',
    color: 'from-purple-600 to-indigo-700',
    borderColor: 'border-purple-600',
    bgColor: 'bg-purple-600/10',
    summary: 'Kullanıcı profilinin (Ad, E-posta, Rol, Avatar) hem yerelde hem canlı VPS\'te MySQL ile canlı senkronizasyonu.',
    whatItDoes: 'Giriş yapan yöneticinin profil verilerini MySQL users tablosu ile otomatik eşleştirir ve tüm ortamlarda eşit tutar.',
    connectedNodes: ['mysql-backend-resilience', 'page-rbac-settings'],
    readsState: ['currentUserState', 'users'],
    mutatesState: ['currentUserState', 'users'],
    whichFeatures: [
      'MySQL Users Tablosu Otomatik Eşleşme (app mount anında /api/users sorgusu)',
      'Ortak Standart Profil Görseli & Avatar Yönetimi',
      'Profil Düzenleme Veritabanı Kaydı (Profilim sayfasında güncellenen bilgilerin MySQL ve LocalStorage eşzamanlı güncellenmesi)',
      'Sessiz Oturum Yenileme Engine'
    ],
    whyWeBuiltIt: 'Farklı cihazlarda veya yerel/canlı sunucularda profil resimlerinin veya kullanıcı adlarının farklı görünmesini engellemek için kurduk.',
    rulesAndCore: [
      'Kural 1: Profil bilgisi değiştiğinde hem MySQL veritabanı hem de aktif kullanıcı durumu anında güncellenmelidir.',
      'Kural 2: Veritabanında kayıtlı kullanıcı avatarı varsayılan olarak header profil resmini beslemelidir.'
    ],
    stepByStepFlow: [
      '1. Adım: Uygulama açılır, /api/users MySQL sorgusu atılır.',
      '2. Adım: Giriş yapan kullanıcının avatarı ve adı veritabanından çekilip header alanına işlenir.',
      '3. Adım: Profilim sayfasından yapılan değişiklikler anında MySQL veritabanına kaydedilir.'
    ],
    relatedRoute: 'profile'
  },
"""

files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for f_path in files:
    if not os.path.exists(f_path):
        continue
    with open(f_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if "page-quote-requests" not in content and "const MIND_MAP_DATA = [" in content:
        content = content.replace("const MIND_MAP_DATA = [\n", "const MIND_MAP_DATA = [\n" + new_nodes)
        with open(f_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully added 5 new architecture nodes to MIND_MAP_DATA in {f_path}!")
    else:
        print(f"MIND_MAP_DATA already contains new nodes or marker missing in {f_path}!")

print("Zihin haritası güncelleme işlemi tamamlandı!")
