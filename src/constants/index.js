// --- CONSTANTS, ROLES, PERMISSIONS, 10 CORPORATE THEMES & MOCK DATA ---

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

// 7 KURUMSAL & DİNAMİK TEMA PALETİ, GEOMETRİ VE İKON SETLERİ
export const THEME_PALETTES = [
  // 1. NORDIC CLARITY & SCANDINAVIAN MINIMAL (ZERO EMOJI DIRECTIVE)
  {
    id: 'nordic-clarity',
    name: 'Nordic Clarity & Scandinavian Minimal ❄️',
    primaryColor: '#0F172A',
    secondaryColor: '#F8FAFC',
    accentColor: '#94A3B8',
    geometry: 'rounded-md',
    description: 'SIFIR EMOJİ DIRECTIVE: Saf 1.75px İskandinav SVG ikonları, Gece Mavisi (#0F172A), Kutup Beyazı & İskandinav Gümüşü',
    isZeroEmoji: true,
    icons: { crown: 'nordic-crown', venue: 'nordic-building', edit: 'nordic-edit', view: 'nordic-eye', delete: 'nordic-trash' }
  },

  // 2. CLASSIC GOLD (Saray Altını)
  {
    id: 'gold',
    name: 'Classic Gold (Saray Altını) 👑',
    primaryColor: '#D4AF37',
    secondaryColor: '#0B0F19',
    geometry: 'rounded-2xl',
    description: 'Sıcak Altın (#D4AF37) & Siyah (#0B0F19) lüks balo konsepti',
    icons: { crown: '👑', venue: '🏰', edit: '✏️', view: '👁️', delete: '🗑️' }
  },

  // 3. OBSIDIAN GOLD (Derin Siyah)
  {
    id: 'obsidian-gold',
    name: 'Obsidian Gold (Derin Siyah) 🖤',
    primaryColor: '#090A0F',
    accentColor: '#F59E0B',
    geometry: 'rounded-none',
    description: 'Obsidyen (#090A0F) & Şampanya Altını, 0px dik keskin metalik çeperler',
    icons: { crown: '🖤', venue: '🏛️', edit: '🖊️', view: '🌟', delete: '💣' }
  },

  // 4. SAPPHIRE CLEAN (Saf Safir)
  {
    id: 'sapphire-clean',
    name: 'Sapphire Clean (Saf Safir) 🔷',
    primaryColor: '#1E40AF',
    accentColor: '#FFFFFF',
    geometry: 'rounded-md',
    description: 'Safir Mavi (#1E40AF) & Kristal Beyaz, 4px neo-minimalist kavisler',
    icons: { crown: '🔷', venue: '🏢', edit: '📝', view: '🔍', delete: '❌' }
  },

  // 5. PLATINUM SILVER (Platin Gümüş)
  {
    id: 'platinum-silver',
    name: 'Platinum Silver (Platin Gümüş) 🥈',
    primaryColor: '#E2E8F0',
    accentColor: '#334155',
    geometry: 'rounded-sm',
    description: 'Platin Gümüş (#E2E8F0) & Füme (#334155), 2px micro-keskin çizgiler',
    icons: { crown: '🥈', venue: '🏛️', edit: '⚙️', view: '🔍', delete: '🗑️' }
  },

  // 6. EMERALD ROYAL (Zümrüt Balo)
  {
    id: 'emerald-royal',
    name: 'Emerald Royal (Zümrüt Balo) 🌿',
    primaryColor: '#065F46',
    accentColor: '#F59E0B',
    geometry: 'rounded-none',
    description: 'Zümrüt Yeşili (#065F46) & Altın Vurgu, 0px dik zümrüt çeperler',
    icons: { crown: '🌿', venue: '🏡', edit: '✍️', view: '👁️', delete: '🍂' }
  },

  // 7. TITANIUM TECH (Titanyum Gelecek)
  {
    id: 'titanium-tech',
    name: 'Titanium Tech (Titanyum Gelecek) ⚡',
    primaryColor: '#1E293B',
    accentColor: '#38BDF8',
    geometry: 'rounded-md',
    description: 'Titanyum Grisi (#1E293B) & Neon Mavi, 4px teknolojik kavisler',
    icons: { crown: '⚡', venue: '🏬', edit: '🛠️', view: '📡', delete: '🚫' }
  }
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

export const generateSmartAIRecommendations = (reservations = [], venues = [], services = []) => {
  const kbVenue = venues.find(v => v.id === 'v2' || (v.name && v.name.includes('Kır Bahçesi'))) || venues[0];
  const kbOccupancy = kbVenue ? (kbVenue.occupancyRate || 92) : 92;
  const currentKbPrice = kbVenue ? kbVenue.price : 85000;
  const suggestedKbPrice = kbVenue ? Math.round(currentKbPrice * 1.10) : 93500;

  const droneService = services.find(s => s.id === 's3' || (s.name && s.name.toLowerCase().includes('drone'))) || services[2];
  const resCountWithDrone = reservations.filter(r => (r.selectedServiceIds || []).includes(droneService?.id)).length;
  const totalRes = Math.max(1, reservations.length);
  const droneAdoptionRate = Math.round((resCountWithDrone / totalRes) * 100);

  return [
    {
      id: 'ai-1',
      code: 'AĞUSTOS10',
      title: `${kbVenue?.name || 'Kır Bahçesi'} Fiyat Artırım & Fırsat Önerisi (%${kbOccupancy} Doluluk)`,
      type: 'percent',
      value: 10,
      venueId: kbVenue?.id || 'v2',
      venueName: kbVenue?.name || 'Kır Bahçesi VİP',
      currentPrice: currentKbPrice,
      suggestedPrice: suggestedKbPrice,
      description: `${kbVenue?.name || 'Kır Bahçesi VİP'} salonunda hafta sonu doluluğu %${kbOccupancy} seviyesine ulaştı. Kiralama bedelini %10 artırarak ${formatCurrency(suggestedKbPrice)} seviyesine çekmek tahmini 140.000 ₺ ek gelir sağlar.`,
      actionText: 'Tek Tıkla Kampanyaya Dönüştür',
      priceActionText: 'Fiyatı Güncelle & Uygula',
      badge: `%${kbOccupancy} Doluluk Zirvede`,
      canUpdatePrice: true
    },
    {
      id: 'ai-2',
      code: 'DRONE20',
      title: 'Drone Çekimi Çapraz Satış Fırsatı',
      type: 'free_service',
      value: 0,
      description: `Mevcut rezervasyonlarda Drone çekimi tercih oranı %${droneAdoptionRate}. Kır bahçesi kiralamalarında 4K drone çekimini promosyonlu sunarak ek 60.000 ₺ ciro elde edin.`,
      actionText: 'Tek Tıkla Kampanyaya Dönüştür',
      badge: 'Çapraz Satış Trendi',
      canUpdatePrice: false
    },
    {
      id: 'ai-3',
      code: 'SONBAHAR26',
      title: 'Sonbahar Erken Rezervasyon Fırsatı (%20 Net İndirim)',
      type: 'percent',
      value: 20,
      description: 'Eylül ve Ekim düğün tarihleri için %20 Erken Rezervasyon Kampanyası başlatarak salon doluluğunu %100 seviyesine çıkarın.',
      actionText: 'Tek Tıkla Kampanyaya Dönüştür',
      badge: 'Sezonluk Fırsat',
      canUpdatePrice: false
    }
  ];
};

export const AI_RECOMMENDATIONS = generateSmartAIRecommendations(INITIAL_RESERVATIONS, INITIAL_VENUES, INITIAL_SERVICES);

