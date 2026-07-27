// İrem Düğün Sarayı & Organizasyon Şirketi - Pre-populated Mock Data

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
    features: ['Kristal Avizeler', 'Gelişmiş Ses & Işık', 'Gelin Odayı VİP', 'Jeneratör', 'Otopark (300 Araç)'],
    images: [
      'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1545232979-fbfd44e666f4?auto=format&fit=crop&w=800&q=80'
    ],
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
    features: ['Göl Manzarası', 'Açılır-Kapanır Tente', 'Peyzaj Işıklandırma', 'Çocuk Oyun Alanı', 'Valo Hizmeti'],
    images: [
      'https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=800&q=80'
    ],
    eventTypes: ['Kır Düğünü', 'Sünnet Düğünü', 'Açık Hava Kokteyl']
  },
  {
    id: 'v3',
    name: 'Bosphorus Teras & Kına Salonu',
    category: 'Butik / Teras',
    capacity: 400,
    price: 45000,
    deposit: 10000,
    location: 'Sapanca Panoramik Teras',
    occupancyRate: 70,
    description: 'Özel konsept Kına geceleri ve butik nişan organizasyonları için tasarlanmış otantik ve şık teras alanı.',
    features: ['Kına Tahtı Konsepti', 'Otantik Dekoru', 'Panoramik Manzara', 'DJ Performansı'],
    images: [
      'https://images.unsplash.com/photo-1527529482837-4698179dc6ce?auto=format&fit=crop&w=800&q=80'
    ],
    eventTypes: ['Kına Gecesi', 'Butik Nişan', 'Bekarlığa Veda']
  }
];

export const INITIAL_SERVICES = [
  {
    id: 's1',
    name: 'Gurme Yemek Servisi (Kırmızı Et Menü)',
    category: 'Catering',
    price: 350,
    pricingType: 'per_person', // per_person or fixed
    description: 'Ordövr tabağı, ara sıcak, Dana Biftek ana yemek, düğün pastası ve meşrubat ikramı.',
    image: 'https://images.unsplash.com/photo-1555244162-803834f70033?auto=format&fit=crop&w=600&q=80'
  },
  {
    id: 's2',
    name: 'Fotoğraf & 4K Video Çekim Paketi',
    category: 'Medya',
    price: 18000,
    pricingType: 'fixed',
    description: 'Tüm gün dış çekim, 2 kameraman ile 4K sinematik düğün hikayesi, Jimmy Jib ve 500 baskılı albüm.',
    image: 'https://images.unsplash.com/photo-1537633552985-df8429e8048b?auto=format&fit=crop&w=600&q=80'
  },
  {
    id: 's3',
    name: 'Canlı Müzik Orkestrası & DJ',
    category: 'Eğlence',
    price: 25000,
    pricingType: 'fixed',
    description: '6 kişilik profesyonel orkestra, solist, meze müziği ve gece boyu performans gösterecek DJ.',
    image: 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=600&q=80'
  },
  {
    id: 's4',
    name: 'Lüks Masa & Sahne Süsleme Konsepti',
    category: 'Dekorasyon',
    price: 15000,
    pricingType: 'fixed',
    description: 'Canlı çiçek aranjmanları, şamdanlar, konsept gelin yolu ve ışıklı karşılama takı.',
    image: 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=600&q=80'
  },
  {
    id: 's5',
    name: 'Volkan, Konfeti & Işık Gösterisi',
    category: 'Efekt',
    price: 8000,
    pricingType: 'fixed',
    description: 'İlk dans esnasında soğuk volkan şovu, pasta kesiminde sis ve konfeti patlatma.',
    image: 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=600&q=80'
  }
];

export const INITIAL_CAMPAIGNS = [
  {
    id: 'c1',
    code: 'IREM2026',
    title: 'Erken Rezervasyon %10 İndirim',
    type: 'percentage',
    value: 10,
    description: 'Erken rezervasyon yapan tüm müşterilerimize toplam tutar üzerinden %10 indirim!',
    startDate: '2026-01-01',
    endDate: '2026-12-31',
    active: true
  },
  {
    id: 'c2',
    code: 'HEDIYE-FOTO',
    title: 'Kır Bahçesi Kiralayana Fotoğraf Çekimi Hediye!',
    type: 'free_service',
    serviceId: 's2',
    description: 'Kır Bahçesi VİP salonumuzu kiralayan müşterilerimize 4K Video & Fotoğraf Çekim Paketi HEDİYE!',
    startDate: '2026-05-01',
    endDate: '2026-09-30',
    active: true
  },
  {
    id: 'c3',
    code: 'VIP5000',
    title: '5.000 TL Nakit İndirim Kuponu',
    type: 'flat_discount',
    value: 5000,
    description: 'Referans koduyla gelen müşterilere doğrudan 5.000 TL kiralama indirimi.',
    startDate: '2026-03-01',
    endDate: '2026-11-30',
    active: true
  }
];

export const INITIAL_CUSTOMERS = [
  {
    id: 'cust1',
    name: 'Ahmet Yılmaz & Ayşe Kaya',
    email: 'ahmet.yilmaz@example.com',
    phone: '+90 532 111 2233',
    address: 'Atatürk Mah. Karanfil Sok. No:12, Sapanca / Sakarya',
    taxType: 'individual',
    tcNo: '12345678901',
    taxOffice: 'Sapanca VD',
    followUp: true,
    followUpNote: 'Sünnet düğünü için 2 yıl sonra tekrar iletişime geçilecek.',
    avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'
  },
  {
    id: 'cust2',
    name: 'Mehmet Demir (Demir İnşaat A.Ş.)',
    email: 'mehmet@demiras.com',
    phone: '+90 533 444 5566',
    address: 'Bağdat Cad. No:140 Kadıköy / İstanbul',
    taxType: 'corporate',
    vknNo: '9876543210',
    taxOffice: 'Kadıköy VD',
    followUp: false,
    followUpNote: '',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80'
  }
];

export const INITIAL_RESERVATIONS = [
  {
    id: 'RES-2026-001',
    venueId: 'v1',
    customerId: 'cust1',
    customerName: 'Ahmet Yılmaz & Ayşe Kaya',
    customerEmail: 'ahmet.yilmaz@example.com',
    customerPhone: '+90 532 111 2233',
    date: '2026-08-15',
    timeSlot: '19:00-23:00', // Gece
    guestCount: 500,
    selectedServices: [
      { serviceId: 's1', quantity: 500, unitPrice: 350 },
      { serviceId: 's2', quantity: 1, unitPrice: 18000 },
      { serviceId: 's3', quantity: 1, unitPrice: 25000 }
    ],
    venuePrice: 65000,
    subtotal: 283000,
    campaignCode: 'IREM2026',
    discountAmount: 28300,
    vatAmount: 50940, // %20
    totalAmount: 305640,
    depositPaid: 50000,
    remainingBalance: 255640,
    paymentStatus: 'Kapora Alındı', // Bekliyor, Kapora Alındı, Ödendi, Tamamlandı
    isInvoiced: true,
    invoiceType: 'individual',
    tcNo: '12345678901',
    taxOffice: 'Sapanca VD',
    taxAddress: 'Atatürk Mah. Karanfil Sok. No:12, Sapanca / Sakarya',
    notes: 'Gelin masası arkasına ekstra beyaz gül takı isteniyor.',
    flowPlan: [
      { time: '19:00', title: 'Misafir Karşılama & Kokteyl' },
      { time: '19:30', title: 'Gelin & Damat Muhteşem Giriş ve İlk Dans' },
      { time: '20:15', title: 'Gurme Yemek Servisi Başlangıcı' },
      { time: '21:30', title: 'Düğün Pastası Kesimi ve Volkan Şovu' },
      { time: '22:00', title: 'Takı Merasimi ve Canlı Müzik Eğlencesi' },
      { time: '23:00', title: 'Kapanış ve Uğurlama' }
    ],
    mediaGallery: [
      { id: 'm1', url: 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80', type: 'image', uploadedBy: 'Sosyal Medya Ekibi' },
      { id: 'm2', url: 'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=800&q=80', type: 'image', uploadedBy: 'Sosyal Medya Ekibi' }
    ]
  },
  {
    id: 'RES-2026-002',
    venueId: 'v2',
    customerId: 'cust2',
    customerName: 'Mehmet Demir (Demir İnşaat)',
    customerEmail: 'mehmet@demiras.com',
    customerPhone: '+90 533 444 5566',
    date: '2026-09-05',
    timeSlot: '13:00-17:00', // Gündüz
    guestCount: 800,
    selectedServices: [
      { serviceId: 's1', quantity: 800, unitPrice: 350 },
      { serviceId: 's4', quantity: 1, unitPrice: 15000 },
      { serviceId: 's5', quantity: 1, unitPrice: 8000 }
    ],
    venuePrice: 85000,
    subtotal: 388000,
    campaignCode: 'VIP5000',
    discountAmount: 5000,
    vatAmount: 76600,
    totalAmount: 459600,
    depositPaid: 459600,
    remainingBalance: 0,
    paymentStatus: 'Ödendi',
    isInvoiced: true,
    invoiceType: 'corporate',
    vknNo: '9876543210',
    taxOffice: 'Kadıköy VD',
    taxAddress: 'Bağdat Cad. No:140 Kadıköy / İstanbul',
    notes: 'Şirket yıllık Gala Yemeği organizasyonu.',
    flowPlan: [
      { time: '13:00', title: 'Açılış ve Hoşgeldiniz Konuşması' },
      { time: '14:00', title: 'Yemek ve Ödül Töreni' },
      { time: '16:00', title: 'DJ Performansı' }
    ],
    mediaGallery: []
  }
];

export const INITIAL_USERS = [
  { id: 'u1', name: 'İrem Yılmaz (Admin)', email: 'admin@iremdugunsarayi.com', role: 'admin', avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80' },
  { id: 'u2', name: 'Canan Güneş (Satış Müdürü)', email: 'satis@iremdugunsarayi.com', role: 'satisci', avatar: 'https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=200&q=80' },
  { id: 'u3', name: 'Murat Arslan (Sosyal Medya)', email: 'sosyal@iremdugunsarayi.com', role: 'sosyal_medyaci', avatar: 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=200&q=80' },
  { id: 'u4', name: 'Ahmet Yılmaz (Müşteri)', email: 'ahmet.yilmaz@example.com', role: 'musteri', avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80' }
];

export const AI_RECOMMENDATIONS = [
  {
    id: 'r1',
    title: 'Hafta İçi Salı/Çarşamba Doluluk Fırsatı',
    badge: 'Gelir Artırma',
    description: 'Hafta içi Salı günlerinde doluluk oranınız %15 seviyesindedir. Salı ve Çarşamba günlerine özel %25 indirimli "Hafta İçi Butik Paket" oluşturursanız aylık cironuzu ortalama ₺95.000 artırabilirsiniz.',
    actionText: 'Kampanya Oluştur'
  },
  {
    id: 'r2',
    title: 'Popüler Hizmet Paketi Önerisi',
    badge: 'Paketleme Önerisi',
    description: 'Müşterilerinizin %78\'i "Gurme Yemek" servisi ile birlikte "Volkan & Işık Gösterisi" satın alıyor. Bu iki hizmeti paket haline getirip ₺500 indirimle sunarak satış oranını %15 yükseltebilirsiniz.',
    actionText: 'Paket Oluştur'
  }
];
