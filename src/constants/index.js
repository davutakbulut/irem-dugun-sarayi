// --- CONSTANTS, ROLES, PERMISSIONS, THEMES & MOCK DATA ---

export const ROLE_NAMES = {
  admin: 'Admin 👑',
  satisci: 'Satış Müdürü 💼',
  sosyal_medyaci: 'Sosyal Medya 📸',
  musteri: 'Müşteri 💑'
};

export const TAB_TO_SLUG = {
  'dashboard': 'anasayfa',
  'create-reservation': 'yeni-rezervasyon',
  'venues': 'dugun-salonlari',
  'services': 'ek-hizmetler',
  'reservations': 'rezervasyonlarim',
  'calendar': 'takvim',
  'campaigns': 'kampanyalar',
  'finance': 'finans',
  'customers': 'musteri-rehberi',
  'users': 'kullanici-yonetimi',
  'reports': 'raporlar',
  'media': 'medya-galerisi',
  'profile': 'profil',
  'settings': 'ayarlar',
  'settings-appearance': 'ayarlar/gorunum',
  'settings-performance': 'ayarlar/onbellek',
  'settings-rbac': 'ayarlar/rol-izinleri'
};

export const SLUG_TO_TAB = Object.entries(TAB_TO_SLUG).reduce((acc, [tab, slug]) => {
  acc[slug] = tab;
  return acc;
}, {});

export const INITIAL_TAB_PERMISSIONS = {
  'dashboard': ['admin', 'satisci', 'sosyal_medyaci', 'musteri'],
  'create-reservation': ['admin', 'satisci'],
  'venues': ['admin', 'satisci', 'sosyal_medyaci', 'musteri'],
  'services': ['admin', 'satisci', 'sosyal_medyaci'],
  'reservations': ['admin', 'satisci', 'musteri'],
  'calendar': ['admin', 'satisci', 'sosyal_medyaci', 'musteri'],
  'campaigns': ['admin', 'satisci', 'musteri'],
  'finance': ['admin'],
  'customers': ['admin', 'satisci'],
  'users': ['admin'],
  'reports': ['admin', 'satisci'],
  'media': ['admin', 'sosyal_medyaci'],
  'profile': ['admin', 'satisci', 'sosyal_medyaci', 'musteri'],
  'settings': ['admin']
};

// 5 KURUMSAL TEMA PALETİ JETONLARI (GELİŞTİRİCİLER TARAFINDAN GENİŞLETİLEBİLİR)
export const THEME_PALETTES = [
  { id: 'gold', name: 'Altın & Şampanya 👑', primaryColor: '#d97706', description: 'Lüks balo ve kır düğünü konsepti (Varsayılan)' },
  { id: 'emerald', name: 'Zümrüt Yeşili 💚', primaryColor: '#059669', description: 'Doğa ve açık hava kır bahçesi konsepti' },
  { id: 'sapphire', name: 'Safir Mavi 💙', primaryColor: '#2563eb', description: 'Kraliyet ve kurumsal balo salonu konsepti' },
  { id: 'rose', name: 'Gül Altını 🌹', primaryColor: '#e11d48', description: 'Romantik ve lüks davet konsepti' },
  { id: 'violet', name: 'Mor Lüks 💜', primaryColor: '#7c3aed', description: 'VIP gece ve sahne ışıkları konsepti' }
];

export const formatCurrency = (amount) => {
  return new Intl.NumberFormat('tr-TR', { style: 'currency', currency: 'TRY', maximumFractionDigits: 0 }).format(amount || 0);
};

export const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' }).format(date);
};

export const INITIAL_VENUES = [
  {
    id: 'v1',
    name: 'Kraliyet Balo Salonu',
    category: 'Kapalı Salon',
    capacity: 750,
    price: 65000,
    deposit: 15000,
    location: 'Sapanca Merkez, Sakarya',
    occupancyRate: 85,
    description: 'Yüksek tavanlı, kristal avizeli, iklimlendirme sistemli ve lüks sahne düzenine sahip ana balo salonumuz.',
    features: ['Kristal Avizeler', 'Gelişmiş Ses & Işık', 'Gelin Odası VİP', 'Jeneratör', 'Otopark (300 Araç)'],
    image: 'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=800&q=80',
    images: ['https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=800&q=80'],
    eventTypes: ['Düğün', 'Nişan', 'Kurumsal Kokteyl', 'Mezuniyet']
  },
  {
    id: 'v2',
    name: 'Kır Bahçesi VİP',
    category: 'Açık Hava / Kır Bahçesi',
    capacity: 1000,
    price: 85000,
    deposit: 20000,
    location: 'Göl Kenarı, Sapanca, Sakarya',
    occupancyRate: 92,
    description: 'Sapanca Gölü manzaralı, asırlık çınar ağaçları altında büyüleyici açık hava kır düğünü alanı.',
    features: ['Göl Manzarası', 'Açılır-Kapanır Tente', 'Peyzaj Işıklandırma', 'Çocuk Oyun Alanı'],
    image: 'https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?auto=format&fit=crop&w=800&q=80',
    images: ['https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?auto=format&fit=crop&w=800&q=80'],
    eventTypes: ['Kır Düğünü', 'Sünnet Düğünü', 'Açık Hava Kokteyl']
  },
  {
    id: 'v3',
    name: 'Zümrüt Butik Salon',
    category: 'Kapalı Salon',
    capacity: 300,
    price: 40000,
    deposit: 10000,
    location: 'Sapanca Merkez, Sakarya',
    occupancyRate: 70,
    description: 'Butik nişan, kına ve samimi aile organizasyonları için tasarlanmış şık salon.',
    features: ['Kına Tahtı Düzeni', 'Butik İkram Servisi', 'Özel Akustik Tavan'],
    image: 'https://images.unsplash.com/photo-1527529482837-4698179dc6ce?auto=format&fit=crop&w=800&q=80',
    images: ['https://images.unsplash.com/photo-1527529482837-4698179dc6ce?auto=format&fit=crop&w=800&q=80'],
    eventTypes: ['Kına Gecesi', 'Nişan', 'Söz']
  }
];

export const INITIAL_SERVICES = [
  { id: 's1', name: 'Canlı Orkestra & Solist Paketi', pricingType: 'flat', price: 18000, image: 'https://images.unsplash.com/photo-1465847899084-d164df4dedc6?auto=format&fit=crop&w=400&q=80', description: '6 kişilik profesyonel sahne orkestrası ve solist performansı.' },
  { id: 's2', name: 'Gurme Yemek Menüsü (Kişi Başı)', pricingType: 'per_person', price: 350, image: 'https://images.unsplash.com/photo-1555244162-803834f70033?auto=format&fit=crop&w=400&q=80', description: 'Ordövr tabağı, ara sıcak, et ana yemek ve özel düğün pastası.' },
  { id: 's3', name: '4K Drone & Video Çekim Ekibi', pricingType: 'flat', price: 15000, image: 'https://images.unsplash.com/photo-1537633552985-df8429e8048b?auto=format&fit=crop&w=400&q=80', description: '2 kameraman, 1 drone operatörü ile tüm gün sinematik çekim.' },
  { id: 's4', name: 'Volkan & Sis Gösteri Paketi', pricingType: 'flat', price: 6000, image: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=400&q=80', description: 'Giriş ve ilk dans esnasında 8 adet soğuk volkan ve ağır sis şovu.' }
];

export const INITIAL_CAMPAIGNS = [
  { id: 'c1', code: 'ERKEN2026', title: 'Erken Rezervasyon %15 İndirimi', type: 'percent', value: 15, description: '2026 yılı sonuna kadar yapılan tüm kiralama rezervasyonlarında %15 net indirim.' },
  { id: 'c2', code: 'DRONEHEDİYE', title: 'Ücretsiz 4K Drone Çekim Hediyesi', type: 'free_service', value: 0, description: 'Kır bahçesi kiralamalarında 12.000 TL değerinde Drone çekim paketi hediye!' },
  { id: 'c3', code: 'YAZINDIRIM', title: 'Hafta İçi Düğünlerde 10.000 TL İndirim', type: 'amount', value: 10000, description: 'Pazartesi-Perşembe günleri yapılan düğünlerde 10.000 TL nakit indirim.' }
];

export const INITIAL_USERS = [
  { id: 'u1', name: 'İrem Yılmaz', email: 'admin@iremdugunsarayi.com', role: 'admin', avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80' },
  { id: 'u2', name: 'Ahmet Kaya', email: 'ahmet@iremdugunsarayi.com', role: 'satisci', avatar: 'https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=200&q=80' },
  { id: 'u3', name: 'Zeynep Demir', email: 'zeynep@iremdugunsarayi.com', role: 'sosyal_medyaci', avatar: 'https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=200&q=80' },
  { id: 'u4', name: 'Elif & Mehmet Can', email: 'elifcan@gmail.com', role: 'musteri', avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80' }
];

export const INITIAL_RESERVATIONS = [
  {
    id: 'REZ-2026-001',
    customerName: 'Elif & Mehmet Can',
    customerPhone: '+90 532 111 2233',
    customerEmail: 'elifcan@gmail.com',
    venueId: 'v1',
    date: '2026-08-15',
    timeSlot: 'Akşam (19:00 - 23:30)',
    guestCount: 600,
    selectedServiceIds: ['s1', 's2'],
    campaignCode: 'ERKEN2026',
    totalAmount: 233750,
    depositPaid: 50000,
    remainingBalance: 183750,
    paymentStatus: 'Kapora Alındı',
    notes: 'Gelin odasına özel karşılama ikramları hazırlanacak.'
  },
  {
    id: 'REZ-2026-002',
    customerName: 'Zeynep & Murat Aksu',
    customerPhone: '+90 533 999 8877',
    customerEmail: 'zeynepmurat@gmail.com',
    venueId: 'v2',
    date: '2026-08-20',
    timeSlot: 'Akşam (19:00 - 23:30)',
    guestCount: 800,
    selectedServiceIds: ['s1', 's3', 's4'],
    campaignCode: 'DRONEHEDİYE',
    totalAmount: 124000,
    depositPaid: 124000,
    remainingBalance: 0,
    paymentStatus: 'Ödendi',
    notes: 'Açık hava havai fişek izni alındı.'
  }
];

export const INITIAL_CUSTOMERS = [
  { id: 'cust-1', name: 'Elif & Mehmet Can', phone: '+90 532 111 2233', email: 'elifcan@gmail.com', date: '2026-08-15', totalRes: 1, status: 'Aktif Rezervasyon', avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80' },
  { id: 'cust-2', name: 'Zeynep & Murat Aksu', phone: '+90 533 999 8877', email: 'zeynepmurat@gmail.com', date: '2026-08-20', totalRes: 1, status: 'Ödendi', avatar: 'https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=200&q=80' }
];

export const AI_RECOMMENDATIONS = [
  { id: 'ai-1', title: '🎯 Ağustos Ayı Kır Bahçesi Fiyat Çarpanı Önerisi', description: 'Ağustos hafta sonları doluluk %92 seviyesine ulaştı. Kır bahçesi kiralama paket fiyatını %10 artırmanız gelirinizi 140.000 ₺ yükseltebilir.', actionText: 'Fiyatı Güncelle' },
  { id: 'ai-2', title: '💡 Drone Çekimi Çapraz Satış Fırsatı', description: 'Son 5 kiralama rezervasyonunda ek drone çekimi seçilmedi. İndirimli paket sunarak ek 60.000 ₺ ciro elde edebilirsiniz.', actionText: 'Kampanya Başlat' }
];
