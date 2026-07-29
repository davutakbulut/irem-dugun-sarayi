/**
 * İREM DÜĞÜN SARAYI & ORGANİZASYON PLATFORMU
 * Shared Mock Data & Initial System Datasets
 */

export const INITIAL_VENUES = [
  {
    id: 'v1',
    name: 'Safir Balo Salonu (Kapsamlı İç Mekan)',
    category: 'Kapalı Balo Salonu',
    capacity: 1000,
    price: 85000,
    deposit: 15000,
    location: 'Ana Bina 1. Kat',
    description: 'Kristal avizeler, yüksek tavan, profesyonel ses-ışık sistemi ve havalandırma.',
    features: ['Gelişmiş Ses & Işık', 'Merkezi İklimlendirme', 'Gelin Odu & Hazırlık Odası', 'Özel Otopark & Vale', 'Canlı Yayın Altyapısı'],
    image: 'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=800&q=80',
    images: [
      'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1527529482837-4698179dc6ce?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    id: 'v2',
    name: 'Yakut Kır Bahçesi (Açık Hava)',
    category: 'Kır Bahçesi',
    capacity: 1500,
    price: 110000,
    deposit: 20000,
    location: 'Doğa Alanı & Bahçe',
    description: 'Doğal çim alan, peyzaj aydınlatmaları, şelale konsepti ve dev dans pisti.',
    features: ['Peyzaj Aydınlatması', 'Olumsuz Hava Şartı Açılır Tente', 'Geniş Otopark', 'Çocuk Oyun Alanı', 'VIP Karşılama Ekibi'],
    image: 'https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?auto=format&fit=crop&w=800&q=80',
    images: [
      'https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    id: 'v3',
    name: 'Zümrüt VIP Salon (Butik & Nişan)',
    category: 'Butik Salon',
    capacity: 400,
    price: 45000,
    deposit: 10000,
    location: 'Ana Bina 2. Kat',
    description: 'Sıcak atmosfer, modern dekorasyon, nişan, kına ve küçük resepsiyonlar için ideal.',
    features: ['Modern Dekorasyon', 'Akustik Ses Sistemi', 'Kına Tahtı & Konsept', 'Özel İkramlık Mutfak'],
    image: 'https://images.unsplash.com/photo-1520854221256-17451cc331bf?auto=format&fit=crop&w=800&q=80',
    images: [
      'https://images.unsplash.com/photo-1520854221256-17451cc331bf?auto=format&fit=crop&w=800&q=80'
    ]
  }
];

export const INITIAL_SERVICES = [
  { id: 's1', name: 'Ordövr Tabaklı Yemek Menüsü', category: 'Catering', price: 250, pricingType: 'per_person', description: '6 Çeşit Soğuk Ordövr, Ara Sıcak, Kırmızı/Beyaz Et Seçeneği, Meyve & Meşrubat.' },
  { id: 's2', name: 'Ordövr Tabaksız Standart Menü', category: 'Catering', price: 180, pricingType: 'per_person', description: 'Ana Yemek (Tavuk/Et Sote), Pilav, Salata, Yaş Pasta ve Sınırsız Meşrubat.' },
  { id: 's3', name: 'Kuru Pasta & Meşrubat İkramı', category: 'Catering', price: 80, pricingType: 'per_person', description: 'Taze Tatlı/Tuzlu Kuru Pasta Çeşitleri, Yaş Pasta ve Çay/Meşrubat İkramı.' },
  { id: 's4', name: 'Profesyonel 4K Fotoğraf & Video Çekimi', category: 'Medya', price: 18000, pricingType: 'fixed', description: '2 Çift Kameralı HD Çekim, Jimmy Jib, Dron Çekimi ve Tüm Ham Fotoğraflar USB.' },
  { id: 's5', name: 'Canlı Orkestra & Sanatçı Performansı', category: 'Müzik', price: 22000, pricingType: 'fixed', description: '4 Kişilik Profesyonel Orkestra, Solist, DJ Performansı ve Ses Sistemi.' },
  { id: 's6', name: 'Görkemli Sis & Volkan Şovu', category: 'Efekt', price: 6500, pricingType: 'fixed', description: 'İlk Dans ve Pasta Kesiminde 8 Adet Soğuk Volkan, Kuru Buz Sis Şovu.' },
  { id: 's7', name: 'Lüks VIP Gelin Arabası Süsleme & Şoför', category: 'Ulaşım', price: 7500, pricingType: 'fixed', description: 'Özel Çiçek Tasarımı, Şehir İçi Şoförlü VIP Araç Hizmeti.' }
];

export const INITIAL_CUSTOMERS = [
  { id: 'c1', name: 'Ahmet Yılmaz & Zeynep Demir', phone: '0 (532) 111 22 33', email: 'ahmet.zeynep@email.com', tcNo: '12345678901', address: 'Kadıköy, İstanbul', totalBookings: 1, registryDate: '2026-01-15' },
  { id: 'c2', name: 'Mehmet Kaya & Elif Şahin', phone: '0 (533) 444 55 66', email: 'mehmet.elif@email.com', tcNo: '98765432109', address: 'Çankaya, Ankara', totalBookings: 2, registryDate: '2026-02-01' },
  { id: 'c3', name: 'Burak Can & Seda Öztürk', phone: '0 (535) 777 88 99', email: 'burak.seda@email.com', tcNo: '45678901234', address: 'Nilüfer, Bursa', totalBookings: 1, registryDate: '2026-03-10' }
];

export const INITIAL_RESERVATIONS = [
  {
    id: 'RES-2026-1001',
    venueId: 'v1',
    customerId: 'c1',
    customerName: 'Ahmet Yılmaz & Zeynep Demir',
    customerPhone: '0 (532) 111 22 33',
    customerEmail: 'ahmet.zeynep@email.com',
    eventDate: '2026-08-15',
    startDate: '2026-08-15',
    endDate: '2026-08-15',
    startTime: '19:00',
    endTime: '23:30',
    timeSlot: '19:00 - 23:30',
    guestCount: 600,
    venuePrice: 85000,
    selectedServices: [
      { serviceId: 's1', quantity: 600, isPaid: true },
      { serviceId: 's4', quantity: 1, isPaid: true },
      { serviceId: 's6', quantity: 1, isPaid: false }
    ],
    subtotal: 259500,
    campaignCode: 'YAZ2026',
    discountAmount: 15000,
    vatAmount: 48900,
    totalAmount: 293400,
    depositPaid: 50000,
    remainingBalance: 243400,
    paymentStatus: 'Kapora Alındı',
    isInvoiced: true,
    invoiceType: 'individual',
    tcNo: '12345678901',
    notes: 'Gelin odası ikramı ekstra meyve tabağı olsun.',
    flowPlan: [
      { time: '19:00', title: 'Misafir Karşılama ve Kokteyl' },
      { time: '20:00', title: 'Çiftin Salona Girişi ve İlk Dans' },
      { time: '21:30', title: 'Pasta Kesimi ve Takı Merasimi' },
      { time: '23:30', title: 'Kapanış ve Uğurlama' }
    ]
  },
  {
    id: 'RES-2026-1002',
    venueId: 'v2',
    customerId: 'c2',
    customerName: 'Mehmet Kaya & Elif Şahin',
    customerPhone: '0 (533) 444 55 66',
    customerEmail: 'mehmet.elif@email.com',
    eventDate: '2026-09-20',
    startDate: '2026-09-20',
    endDate: '2026-09-20',
    startTime: '18:30',
    endTime: '23:00',
    timeSlot: '18:30 - 23:00',
    guestCount: 800,
    venuePrice: 110000,
    selectedServices: [
      { serviceId: 's2', quantity: 800, isPaid: true },
      { serviceId: 's5', quantity: 1, isPaid: true }
    ],
    subtotal: 276000,
    campaignCode: '',
    discountAmount: 0,
    vatAmount: 55200,
    totalAmount: 331200,
    depositPaid: 331200,
    remainingBalance: 0,
    paymentStatus: 'Tamamlandı',
    isInvoiced: true,
    invoiceType: 'corporate',
    vknNo: '9876543210',
    taxOffice: 'Çankaya VD',
    notes: 'Orkestra yöresel şarkılara ağırlık verecek.',
    flowPlan: [
      { time: '18:30', title: 'Karşılama Müzikleri' },
      { time: '19:30', title: 'Giriş ve Nikah Akit Merasimi' },
      { time: '21:00', title: 'Canlı Orkestra & Halaylar' },
      { time: '23:00', title: 'Kapanış' }
    ]
  }
];

export const INITIAL_CAMPAIGNS = [
  { id: 'cmp1', code: 'YAZ2026', title: 'Erken Yaz Rezervasyon İndirimi', discountType: 'fixed', discountValue: 15000, minGuest: 400, validUntil: '2026-08-31', active: true, description: '400 kişi ve üzeri erken rezervasyonlarda 15.000 ₺ net indirim.' },
  { id: 'cmp2', code: 'BUTIK10', title: 'Zümrüt VIP Salon %10 İndirim', discountType: 'percent', discountValue: 10, minGuest: 200, validUntil: '2026-10-15', active: true, description: 'Hafta içi Zümrüt salonda geçerli %10 indirim.' }
];

export const INITIAL_USERS = [
  { id: 'u1', name: 'Davut Akbulut', email: 'davut@iremdugun.com', role: 'SuperAdmin', title: 'Genel Müdürü & Sistem Yöneticisi', avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80' },
  { id: 'u2', name: 'Selin Yılmaz', email: 'selin@iremdugun.com', role: 'Manager', title: 'Operasyon & Satış Müdürü', avatar: 'https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=200&q=80' },
  { id: 'u3', name: 'Caner Öztürk', email: 'caner@iremdugun.com', role: 'Staff', title: 'Etkinlik & Sahne Koordinatörü', avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80' }
];

export const DEFAULT_FLOW_PLAN = [
  { time: '19:00', title: 'Misafir Karşılama ve Kokteyl İkramı' },
  { time: '20:00', title: 'Görkemli Çift Girişi ve İlk Dans' },
  { time: '20:30', title: 'Yemek / İkram Servisi ve Slayt Gösterisi' },
  { time: '21:30', title: 'Pasta Kesim Merasimi & Volkan Şovu' },
  { time: '22:00', title: 'Takı Töreni ve Tebrikler' },
  { time: '23:30', title: 'Kapanış ve Uğurlama' }
];

export const INITIAL_SYSTEM_LOGS = [
  { id: 'l1', timestamp: '2026-07-29 14:30', user: 'Davut Akbulut', action: 'Yeni Rezervasyon', detail: 'RES-2026-1001 oluşturuldu (Safir Balo Salonu)' },
  { id: 'l2', timestamp: '2026-07-29 15:15', user: 'Selin Yılmaz', action: 'Kapora Tahsilatı', detail: 'RES-2026-1001 için ₺50.000 tahsil edildi' },
  { id: 'l3', timestamp: '2026-07-29 16:00', user: 'Davut Akbulut', action: 'Tema Değişikliği', detail: 'Kurumsal Tema: Obsidian Gold aktif edildi' }
];
