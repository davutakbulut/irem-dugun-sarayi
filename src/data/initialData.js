// İrem Düğün Sarayı - Full Dynamic Database Initial Records

export const venues = [
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
    eventTypes: ['Düğün', 'Nişan', 'Kurumsal Kokteyl', 'Mezuniyet'],
    availableServices: ['s1', 's2', 's3', 's4', 's5', 's6', 's7']
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
    eventTypes: ['Kır Düğünü', 'Sünnet Düğünü', 'Açık Hava Kokteyl'],
    availableServices: ['s1', 's2', 's3', 's5', 's6', 's8']
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
    image: 'https://images.unsplash.com/photo-1527529482837-4698179dc6ce?auto=format&fit=crop&w=800&q=80',
    images: ['https://images.unsplash.com/photo-1527529482837-4698179dc6ce?auto=format&fit=crop&w=800&q=80'],
    eventTypes: ['Kına Gecesi', 'Butik Nişan', 'Bekarlığa Veda'],
    availableServices: ['s2', 's3', 's4', 's5']
  },
  {
    id: 'v4',
    name: 'Kehribar Havuz Başı',
    category: 'Havuz Başı',
    capacity: 600,
    price: 55000,
    deposit: 12000,
    location: 'Sapanca Palmiye Bahçesi',
    occupancyRate: 78,
    description: 'Palmiye ağaçlarıyla çevrili, tropikal aydınlatmalı havuz başı düğün ve resepsiyon alanı.',
    features: ['Işıklandırılmış Havuz', 'Tropikal Peyzaj', 'VIP Bar', 'Canlı Müzik Sahnesi'],
    image: 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&w=800&q=80',
    images: ['https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&w=800&q=80'],
    eventTypes: ['Havuz Başı Düğün', 'Resepsiyon', 'Parti'],
    availableServices: ['s1', 's2', 's3', 's5', 's6']
  },
  {
    id: 'v5',
    name: 'Kehribar VİP Salon',
    category: 'VİP Salon',
    capacity: 500,
    price: 70000,
    deposit: 15000,
    location: 'Sapanca Kehribar Kompleksi',
    occupancyRate: 80,
    description: 'Özel VİP konsepti, ses geçirmeyen akustik duvar kaplamaları ve özel vale hizmeti ile premium salonumuz.',
    features: ['Akustik Ses Yalıtımı', 'Özel Vale', 'VİP İkram Salonu', 'LED Ekran Sahne'],
    image: 'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&w=800&q=80',
    images: ['https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&w=800&q=80'],
    eventTypes: ['VİP Düğün', 'Kurumsal Gala', 'Ödül Töreni'],
    availableServices: ['s1', 's2', 's3', 's4', 's6', 's7']
  }
];

export const services = [
  { id: 's1', name: 'Gurme Yemek Servisi (Et Menü)', category: 'Catering', price: 350, pricingType: 'per_person', description: 'Ordövr, Dana Biftek, düğün pastası.', image: 'https://images.unsplash.com/photo-1555244162-803834f70033?auto=format&fit=crop&w=600&q=80' },
  { id: 's2', name: 'Fotoğraf & 4K Video Paketi', category: 'Medya', price: 18000, pricingType: 'fixed', description: 'Dış çekim, 4K sinematik albüm.', image: 'https://images.unsplash.com/photo-1537633552985-df8429e8048b?auto=format&fit=crop&w=600&q=80' },
  { id: 's3', name: 'Canlı Müzik Orkestrası & DJ', category: 'Eğlence', price: 25000, pricingType: 'fixed', description: '6 kişilik orkestra ve DJ.', image: 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=600&q=80' },
  { id: 's4', name: 'Masa & Sahne Süsleme', category: 'Dekorasyon', price: 15000, pricingType: 'fixed', description: 'Canlı çiçekler ve şamdanlar.', image: 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=600&q=80' },
  { id: 's5', name: 'Volkan, Konfeti & Işık Şovu', category: 'Efekt', price: 8000, pricingType: 'fixed', description: 'Soğuk volkan ve konfeti.', image: 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=600&q=80' },
  { id: 's6', name: 'VİP Karşılama Kokteyli & İkram Barı', category: 'Catering', price: 150, pricingType: 'per_person', description: 'Karşılama şampanyası, kanapeler ve taze meyve barları.', image: 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?auto=format&fit=crop&w=600&q=80' },
  { id: 's7', name: 'Profesyonel Garson & Servis Ekibi', category: 'Servis', price: 12000, pricingType: 'fixed', description: '10 kişilik eğitimli üniformalı servis ekibi.', image: 'https://images.unsplash.com/photo-1530103862676-de8c9debad1d?auto=format&fit=crop&w=600&q=80' },
  { id: 's8', name: 'Çocuk Oyun Alanı & Palyaço', category: 'Eğlence', price: 6000, pricingType: 'fixed', description: 'Çocuk animatörü, yüz boyama ve eğlenceli oyun alanı.', image: 'https://images.unsplash.com/photo-1502086223501-7ea6ecd79368?auto=format&fit=crop&w=600&q=80' }
];

export const campaigns = [
  { id: 'c1', code: 'IREM2026', title: 'Erken Rezervasyon %10 İndirim', type: 'percentage', value: 10, description: 'Tüm rezervasyonlarda %10 indirim!', startDate: '2026-01-01', endDate: '2026-12-31', active: true },
  { id: 'c2', code: 'HEDIYE-FOTO', title: 'Fotoğraf Çekimi Hediye!', type: 'free_service', serviceId: 's2', description: 'Kır Bahçesi kiralayana Fotoğraf Paketi HEDİYE!', startDate: '2026-05-01', endDate: '2026-09-30', active: true },
  { id: 'c3', code: 'VIP5000', title: '5.000 TL Nakit İndirim', type: 'flat_discount', value: 5000, description: 'Doğrudan 5.000 TL kiralama indirimi.', startDate: '2026-03-01', endDate: '2026-11-30', active: true },
  { id: 'c4', code: 'BAHAR2026', title: 'Bahar Düğünlerine %15 İndirim', type: 'percentage', value: 15, description: 'Nisan - Mayıs ayı rezervasyonlarına özel %15 fırsat.', startDate: '2026-04-01', endDate: '2026-05-31', active: true }
];

export const customers = [
  { id: 'cust1', name: 'Ahmet Yılmaz & Ayşe Kaya', email: 'ahmet.yilmaz@example.com', phone: '+90 532 111 2233', secondaryPhone: '+90 535 999 8877', address: 'Atatürk Mah. Sapanca / Sakarya', taxType: 'individual', tcNo: '12345678901', taxOffice: 'Sapanca VD', followUp: true, followUpNote: 'Sünnet düğünü için 2 yıl sonra görüşülecek.', avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80' },
  { id: 'cust2', name: 'Mehmet Demir (Demir İnşaat)', email: 'mehmet@demiras.com', phone: '+90 533 444 5566', secondaryPhone: '+90 216 333 2211', address: 'Bağdat Cad. Kadıköy / İstanbul', taxType: 'corporate', vknNo: '9876543210', taxOffice: 'Kadıköy VD', followUp: false, followUpNote: '', avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80' },
  { id: 'cust3', name: 'Zeynep Çelik & Burak Şahin', email: 'zeynep.celik@example.com', phone: '+90 542 777 8899', secondaryPhone: '+90 544 111 3344', address: 'Serdivan Mah. Adapazarı / Sakarya', taxType: 'individual', tcNo: '23456789012', taxOffice: 'Adapazarı VD', followUp: true, followUpNote: 'Kına gecesi için ek masa talebi olabilir.', avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=200&q=80' },
  { id: 'cust4', name: 'Elif Aydın (Aydın Holding)', email: 'elif@aydinholding.com', phone: '+90 530 555 6677', secondaryPhone: '+90 212 444 0011', address: 'Levent Mah. Beşiktaş / İstanbul', taxType: 'corporate', vknNo: '1122334455', taxOffice: 'Zincirlikuyu VD', followUp: false, followUpNote: '', avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80' }
];

export const initialReservations = [
  {
    id: 'RES-2026-001',
    venueId: 'v1',
    customerId: 'cust1',
    customerName: 'Ahmet Yılmaz & Ayşe Kaya',
    customerEmail: 'ahmet.yilmaz@example.com',
    customerPhone: '+90 532 111 2233',
    secondaryPhone: '+90 535 999 8877',
    date: '2026-08-15',
    timeSlot: '19:00-23:00',
    guestCount: 500,
    selectedServices: [
      { serviceId: 's1', quantity: 500, unitPrice: 350, isPaid: true },
      { serviceId: 's2', quantity: 1, unitPrice: 18000, isPaid: true },
      { serviceId: 's3', quantity: 1, unitPrice: 25000, isPaid: false }
    ],
    venuePrice: 65000,
    subtotal: 283000,
    campaignCode: 'IREM2026',
    discountAmount: 28300,
    vatAmount: 50940,
    totalAmount: 305640,
    depositPaid: 50000,
    remainingBalance: 255640,
    paymentStatus: 'Kapora Alındı',
    isInvoiced: true,
    invoiceType: 'individual',
    taxOffice: 'Sapanca VD',
    tcNo: '12345678901',
    invoiceAddress: 'Atatürk Mah. Sapanca / Sakarya',
    notes: 'Gelin odasına taze meyve sepeti ve ikram hazırlanacak.',
    flowPlan: [
      { time: '19:00', title: 'Misafir Karşılama & Kokteyl' },
      { time: '19:30', title: 'Gelin Damat Giriş & İlk Dans' },
      { time: '20:15', title: 'Yemek Servisi' },
      { time: '21:30', title: 'Pasta Kesimi & Şov' },
      { time: '22:00', title: 'Takı & Eğlence' }
    ],
    mediaGallery: [
      { id: 'm1', url: 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80', uploadedBy: 'Sosyal Medya Ekibi' }
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
    timeSlot: '13:00-17:00',
    guestCount: 800,
    selectedServices: [
      { serviceId: 's1', quantity: 800, unitPrice: 350, isPaid: true },
      { serviceId: 's4', quantity: 1, unitPrice: 15000, isPaid: true }
    ],
    venuePrice: 85000,
    subtotal: 380000,
    campaignCode: 'VIP5000',
    discountAmount: 5000,
    vatAmount: 75000,
    totalAmount: 450000,
    depositPaid: 450000,
    remainingBalance: 0,
    paymentStatus: 'Ödendi',
    isInvoiced: true,
    invoiceType: 'corporate',
    taxOffice: 'Kadıköy VD',
    vknNo: '9876543210',
    invoiceAddress: 'Bağdat Cad. Kadıköy / İstanbul',
    notes: 'Kurumsal bayii toplantısı ve gala yemeği.',
    flowPlan: [
      { time: '13:00', title: 'Açılış Konuşması' },
      { time: '14:00', title: 'Gala Yemeği' }
    ],
    mediaGallery: []
  },
  {
    id: 'RES-2026-003',
    venueId: 'v3',
    customerId: 'cust3',
    customerName: 'Zeynep Çelik & Burak Şahin',
    customerEmail: 'zeynep.celik@example.com',
    customerPhone: '+90 542 777 8899',
    date: '2026-08-28',
    timeSlot: '18:00-22:00',
    guestCount: 350,
    selectedServices: [
      { serviceId: 's2', quantity: 1, unitPrice: 18000, isPaid: true },
      { serviceId: 's4', quantity: 1, unitPrice: 15000, isPaid: true }
    ],
    venuePrice: 45000,
    subtotal: 78000,
    campaignCode: 'IREM2026',
    discountAmount: 7800,
    vatAmount: 14040,
    totalAmount: 84240,
    depositPaid: 20000,
    remainingBalance: 64240,
    paymentStatus: 'Kapora Alındı',
    isInvoiced: false,
    invoiceType: 'individual',
    taxOffice: 'Adapazarı VD',
    tcNo: '23456789012',
    invoiceAddress: 'Serdivan Mah. Adapazarı / Sakarya',
    notes: 'Kına tahtı kırmızı kadife kumaş ile kaplanacak.',
    flowPlan: [
      { time: '18:00', title: 'Kına Karşılama' },
      { time: '19:30', title: 'Kına Yakma Seremonisi' }
    ],
    mediaGallery: []
  },
  {
    id: 'RES-2026-004',
    venueId: 'v5',
    customerId: 'cust4',
    customerName: 'Elif Aydın (Aydın Holding)',
    customerEmail: 'elif@aydinholding.com',
    customerPhone: '+90 530 555 6677',
    date: '2026-10-12',
    timeSlot: '19:00-23:00',
    guestCount: 450,
    selectedServices: [
      { serviceId: 's1', quantity: 450, unitPrice: 350, isPaid: true },
      { serviceId: 's6', quantity: 450, unitPrice: 150, isPaid: true },
      { serviceId: 's7', quantity: 1, unitPrice: 12000, isPaid: true }
    ],
    venuePrice: 70000,
    subtotal: 307000,
    campaignCode: 'VIP5000',
    discountAmount: 5000,
    vatAmount: 60400,
    totalAmount: 362400,
    depositPaid: 100000,
    remainingBalance: 262400,
    paymentStatus: 'Kapora Alındı',
    isInvoiced: true,
    invoiceType: 'corporate',
    taxOffice: 'Zincirlikuyu VD',
    vknNo: '1122334455',
    invoiceAddress: 'Levent Mah. Beşiktaş / İstanbul',
    notes: 'Ödül töreni öncesi VİP kokteyl düzenlenecek.',
    flowPlan: [
      { time: '19:00', title: 'VİP Karşılama Kokteyli' },
      { time: '20:00', title: 'Ödül Töreni & Sunum' }
    ],
    mediaGallery: []
  }
];

export const users = [
  { id: 'u1', name: 'İrem Yılmaz (Admin)', email: 'admin@iremdugunsarayi.com', role: 'admin', avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80' },
  { id: 'u2', name: 'Canan Güneş (Satış Müdürü)', email: 'satis@iremdugunsarayi.com', role: 'satisci', avatar: 'https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=200&q=80' },
  { id: 'u3', name: 'Murat Arslan (Sosyal Medya)', email: 'sosyal@iremdugunsarayi.com', role: 'sosyal_medyaci', avatar: 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=200&q=80' },
  { id: 'u4', name: 'Ahmet Yılmaz (Müşteri)', email: 'ahmet.yilmaz@example.com', role: 'musteri', avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80' }
];

export const financialStats = {
  totalRev: initialReservations.reduce((acc, r) => acc + (r.totalAmount || 0), 0),
  totalDeposit: initialReservations.reduce((acc, r) => acc + (r.depositPaid || 0), 0),
  totalPending: initialReservations.reduce((acc, r) => acc + (r.remainingBalance || 0), 0)
};

// Aliases for backwards compatibility
export const INITIAL_VENUES = venues;
export const INITIAL_SERVICES = services;
export const INITIAL_CAMPAIGNS = campaigns;
export const INITIAL_CUSTOMERS = customers;
export const INITIAL_RESERVATIONS = initialReservations;
export const INITIAL_USERS = users;
