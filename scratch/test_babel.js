
    const { useState, useEffect, useMemo, useCallback, useRef } = React;

    const INITIAL_VENUES = [
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
        eventTypes: ['Kına Gecesi', 'Butik Nişan', 'Bekarlığa Veda']
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
        eventTypes: ['Havuz Başı Düğün', 'Resepsiyon', 'Parti']
      }
    ];

    const INITIAL_SERVICES = [
      { id: 's1', name: 'Gurme Yemek Servisi (Et Menü)', category: 'Catering', price: 350, pricingType: 'per_person', description: 'Ordövr, Dana Biftek, düğün pastası.', image: 'https://images.unsplash.com/photo-1555244162-803834f70033?auto=format&fit=crop&w=600&q=80' },
      { id: 's2', name: 'Fotoğraf & 4K Video Paketi', category: 'Medya', price: 18000, pricingType: 'fixed', description: 'Dış çekim, 4K sinematik albüm.', image: 'https://images.unsplash.com/photo-1537633552985-df8429e8048b?auto=format&fit=crop&w=600&q=80' },
      { id: 's3', name: 'Canlı Müzik Orkestrası & DJ', category: 'Eğlence', price: 25000, pricingType: 'fixed', description: '6 kişilik orkestra ve DJ.', image: 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=600&q=80' },
      { id: 's4', name: 'Masa & Sahne Süsleme', category: 'Dekorasyon', price: 15000, pricingType: 'fixed', description: 'Canlı çiçekler ve şamdanlar.', image: 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=600&q=80' },
      { id: 's5', name: 'Volkan, Konfeti & Işık Şovu', category: 'Efekt', price: 8000, pricingType: 'fixed', description: 'Soğuk volkan ve konfeti.', image: 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=600&q=80' }
    ];

    const INITIAL_CAMPAIGNS = [
      { id: 'c1', code: 'IREM2026', title: 'Erken Rezervasyon %10 İndirim', type: 'percentage', value: 10, description: 'Tüm rezervasyonlarda %10 indirim!', startDate: '2026-01-01', endDate: '2026-12-31', active: true },
      { id: 'c2', code: 'HEDIYE-FOTO', title: 'Fotoğraf Çekimi Hediye!', type: 'free_service', serviceId: 's2', description: 'Kır Bahçesi kiralayana Fotoğraf Paketi HEDİYE!', startDate: '2026-05-01', endDate: '2026-09-30', active: true },
      { id: 'c3', code: 'VIP5000', title: '5.000 TL Nakit İndirim', type: 'flat_discount', value: 5000, description: 'Doğrudan 5.000 TL kiralama indirimi.', startDate: '2026-03-01', endDate: '2026-11-30', active: true }
    ];

    const INITIAL_CUSTOMERS = [
      { id: 'cust1', name: 'Ahmet Yılmaz & Ayşe Kaya', email: 'ahmet.yilmaz@example.com', phone: '+90 532 111 2233', secondaryPhone: '+90 535 999 8877', address: 'Atatürk Mah. Sapanca / Sakarya', taxType: 'individual', tcNo: '12345678901', taxOffice: 'Sapanca VD', followUp: true, followUpNote: 'Sünnet düğünü için 2 yıl sonra görüşülecek.', avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80' },
      { id: 'cust2', name: 'Mehmet Demir (Demir İnşaat)', email: 'mehmet@demiras.com', phone: '+90 533 444 5566', secondaryPhone: '+90 216 333 2211', address: 'Bağdat Cad. Kadıköy / İstanbul', taxType: 'corporate', vknNo: '9876543210', taxOffice: 'Kadıköy VD', followUp: false, followUpNote: '', avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80' }
    ];

    const INITIAL_RESERVATIONS = [
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
      }
    ];

    const INITIAL_USERS = [
      { id: 'u1', name: 'İrem Yılmaz (Admin)', email: 'admin@iremdugunsarayi.com', role: 'admin', avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80' },
      { id: 'u2', name: 'Canan Güneş (Satış Müdürü)', email: 'satis@iremdugunsarayi.com', role: 'satisci', avatar: 'https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=200&q=80' },
      { id: 'u3', name: 'Murat Arslan (Sosyal Medya)', email: 'sosyal@iremdugunsarayi.com', role: 'sosyal_medyaci', avatar: 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=200&q=80' },
      { id: 'u4', name: 'Ahmet Yılmaz (Müşteri)', email: 'ahmet.yilmaz@example.com', role: 'musteri', avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80' }
    ];

    const AI_RECOMMENDATIONS = [
      { id: 'r1', title: 'Hafta İçi Salı/Çarşamba Doluluk Fırsatı', badge: 'Gelir Artırma', description: 'Hafta içi Salı günlerinde doluluk %15 seviyesinde. Salı günlerine özel %25 indirimli paketle aylık gelirinizi ₺95.000 artırabilirsiniz.', actionText: 'Kampanya Oluştur' },
      { id: 'r2', title: 'Popüler Hizmet Paketi Önerisi', badge: 'Paket Önerisi', description: 'Müşterilerinizin %78\'i "Gurme Yemek" ile "Volkan Gösterisi" satın alıyor. Paket halinde %10 indirimle sunabilirsiniz.', actionText: 'Paket Oluştur' }
    ];

    const TAB_TO_SLUG = {
      'dashboard': 'anasayfa',
      'create-reservation': 'yeni-rezervasyon',
      'venues': 'dugun-salonlari',
      'services': 'ek-hizmetler',
      'reservations': 'rezervasyonlar',
      'calendar': 'takvim',
      'campaigns': 'kampanyalar',
      'finance': 'finans',
      'customers': 'musteri-rehberi',
      'users': 'kullanici-yonetimi',
      'reports': 'raporlar-ai',
      'media': 'medya-yukle'
    };

    const SLUG_TO_TAB = {
      'anasayfa': 'dashboard',
      'yeni-rezervasyon': 'create-reservation',
      'dugun-salonlari': 'venues',
      'ek-hizmetler': 'services',
      'rezervasyonlar': 'reservations',
      'takvim': 'calendar',
      'kampanyalar': 'campaigns',
      'finans': 'finance',
      'musteri-rehberi': 'customers',
      'kullanici-yonetimi': 'users',
      'raporlar-ai': 'reports',
      'medya-yukle': 'media'
    };

    const TAB_LABELS = {
      'dashboard': 'Anasayfa / İstatistikler',
      'create-reservation': '➕ Yeni Rezervasyon Oluştur',
      'venues': 'Düğün Salonlarım',
      'services': 'Ek Hizmetlerim',
      'reservations': 'Rezervasyonlar',
      'calendar': 'Takvim Görünümü',
      'campaigns': 'Kampanyalar',
      'finance': 'Finans & Fatura Yönetimi',
      'customers': 'Müşteri Rehberi',
      'users': 'Kullanıcı Yönetimi',
      'reports': 'Raporlar & AI Önerileri',
      'media': 'Medya & Foto Yükleme'
    };

    const TAB_PERMISSIONS = {
      'dashboard': ['admin', 'satisci', 'sosyal_medyaci', 'musteri'],
      'create-reservation': ['admin', 'satisci'],
      'venues': ['admin', 'satisci'],
      'services': ['admin', 'satisci'],
      'reservations': ['admin', 'satisci'],
      'calendar': ['admin', 'satisci'],
      'campaigns': ['admin'],
      'finance': ['admin'],
      'customers': ['admin', 'satisci'],
      'users': ['admin'],
      'reports': ['admin'],
      'media': ['admin', 'sosyal_medyaci', 'musteri']
    };

    const ROLE_NAMES = {
      'admin': 'Admin 👑',
      'satisci': 'Satışçı 💼',
      'sosyal_medyaci': 'Sosyal Medya 📸',
      'musteri': 'Müşteri 💑'
    };

    function formatCurrency(amount) {
      if (amount === undefined || amount === null) return '₺0';
      return new Intl.NumberFormat('tr-TR', { style: 'currency', currency: 'TRY', maximumFractionDigits: 0 }).format(amount);
    }
    function formatDate(dateString) {
      if (!dateString) return '';
      return new Intl.DateTimeFormat('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' }).format(new Date(dateString));
    }
    function generateWhatsAppLink(phone, customerName = '', date = '', remaining = '') {
      const cleanPhone = phone ? phone.replace(/[^0-9]/g, '') : '';
      const text = `Merhabalar Sayın ${customerName}, İrem Düğün Sarayı & Organizasyon Şirketi ${date ? date + ' tarihli ' : ''}rezervasyonunuz hakkında bilgilendirmedir. Kalan Bakiyeniz: ${remaining ? formatCurrency(remaining) : 'Detaylar için iletişime geçiniz.'}`;
      return `https://wa.me/${cleanPhone}?text=${encodeURIComponent(text)}`;
    }

    function getHashTab() {
      const slug = window.location.hash.replace('#/', '').replace('#', '');
      return SLUG_TO_TAB[slug] || 'dashboard';
    }

    // --- MAIN APP COMPONENT ---
    function App() {
      const [venues, setVenues] = useState(INITIAL_VENUES);
      const [services, setServices] = useState(INITIAL_SERVICES);
      const [campaigns, setCampaigns] = useState(INITIAL_CAMPAIGNS);
      const [customers, setCustomers] = useState(INITIAL_CUSTOMERS);
      const [reservations, setReservations] = useState(INITIAL_RESERVATIONS);
      const [users, setUsers] = useState(INITIAL_USERS);

      const [activeRole, setActiveRole] = useState('admin');
      const [activeTab, setActiveTabState] = useState(getHashTab);

      const [toast, setToast] = useState(null);

      // Modals State
      const [selectedResForDetail, setSelectedResForDetail] = useState(null);
      const [customerModalData, setCustomerModalData] = useState(null);

      const [resSearchQuery, setResSearchQuery] = useState('');
      const [resStatusFilter, setResStatusFilter] = useState('all');

      const navigateTo = (tab) => {
        setActiveTabState(tab);
        const tabSlug = TAB_TO_SLUG[tab] || 'anasayfa';
        const newUrl = `${window.location.pathname}#/${tabSlug}`;
        window.history.pushState({ tab }, '', newUrl);
      };

      useEffect(() => {
        const handlePopState = () => {
          setActiveTabState(getHashTab());
        };
        window.addEventListener('popstate', handlePopState);
        window.addEventListener('hashchange', handlePopState);
        return () => {
          window.removeEventListener('popstate', handlePopState);
          window.removeEventListener('hashchange', handlePopState);
        };
      }, []);

      const showToast = (msg, type = 'success') => {
        setToast({ msg, type });
        setTimeout(() => setToast(null), 4000);
      };

      const financialStats = useMemo(() => {
        const totalRev = reservations.reduce((acc, r) => acc + r.totalAmount, 0);
        const totalDeposit = reservations.reduce((acc, r) => acc + r.depositPaid, 0);
        const totalPending = reservations.reduce((acc, r) => acc + r.remainingBalance, 0);
        return { totalRev, totalDeposit, totalPending };
      }, [reservations]);

      const filteredReservations = useMemo(() => {
        return reservations.filter(r => {
          const matchSearch = r.id.toLowerCase().includes(resSearchQuery.toLowerCase()) || r.customerName.toLowerCase().includes(resSearchQuery.toLowerCase());
          const matchStatus = resStatusFilter === 'all' || r.paymentStatus === resStatusFilter;
          return matchSearch && matchStatus;
        });
      }, [reservations, resSearchQuery, resStatusFilter]);

      const isAuthorized = useMemo(() => {
        const allowedRoles = TAB_PERMISSIONS[activeTab] || ['admin'];
        return allowedRoles.includes(activeRole);
      }, [activeTab, activeRole]);

      // Print Invoice Helper
      const handlePrintInvoice = (res) => {
        const venue = venues.find(v => v.id === res.venueId);
        const printWin = window.open('', '_blank', 'width=900,height=700');
        printWin.document.write(`
          <!DOCTYPE html>
          <html>
          <head>
            <title>İrem Düğün Sarayı - Resmi Sözleşme & Fatura (${res.id})</title>
            <style>
              body { font-family: 'Segoe UI', Arial, sans-serif; padding: 40px; color: #1e293b; line-height: 1.5; }
              .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #d97706; padding-bottom: 20px; }
              .logo { font-size: 24px; font-weight: bold; color: #b45309; }
              .title { font-size: 18px; font-weight: bold; text-align: center; margin: 30px 0 10px 0; color: #0f172a; text-transform: uppercase; }
              .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 25px; }
              .card { background: #f8fafc; border: 1px solid #cbd5e1; padding: 15px; border-radius: 8px; font-size: 13px; }
              table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 13px; }
              th, td { border: 1px solid #cbd5e1; padding: 10px; text-align: left; }
              th { background: #f1f5f9; font-weight: bold; }
              .totals { margin-top: 20px; text-align: right; font-size: 14px; }
              .totals div { margin-bottom: 5px; }
              .grand-total { font-size: 18px; font-weight: bold; color: #b45309; }
              .signatures { display: flex; justify-content: space-between; margin-top: 50px; font-size: 13px; }
              .sig-box { border-top: 1px solid #94a3b8; width: 200px; text-align: center; padding-top: 8px; }
            </style>
          </head>
          <body>
            <div class="header">
              <div>
                <div class="logo">👑 İREM DÜĞÜN SARAYI</div>
                <div style="font-size: 12px; color: #64748b;">Organizasyon & Kiralama Şirketi | Sapanca Göl Kenarı, Sakarya</div>
              </div>
              <div style="text-align: right;">
                <div style="font-size: 16px; font-weight: bold;">SÖZLEŞME & FATURA</div>
                <div style="font-size: 12px; color: #64748b;">Belge No: <strong>${res.id}</strong></div>
                <div style="font-size: 12px; color: #64748b;">Tarih: ${new Date().toLocaleDateString('tr-TR')}</div>
              </div>
            </div>

            <div class="title">DÜĞÜN SALONU KİRALAMA & ETKİNLİK SÖZLEŞMESİ</div>

            <div class="grid">
              <div class="card">
                <strong>ŞİRKET BİLGİLERİ (Hizmet Veren):</strong><br>
                İrem Düğün Sarayı Ltd. Şti.<br>
                Sapanca Göl Kenarı No: 45, Sakarya<br>
                Sapanca Vergi Dairesi | VKN: 4820192837<br>
                Tel: +90 532 111 2233
              </div>
              <div class="card">
                <strong>MÜŞTERİ BİLGİLERİ (Hizmet Alan):</strong><br>
                ${res.customerName}<br>
                Tel: ${res.customerPhone}<br>
                E-posta: ${res.customerEmail}<br>
                Fatura Tipi: ${res.invoiceType === 'corporate' ? 'Kurumsal (VKN)' : 'Bireysel (TC No)'}
              </div>
            </div>

            <div class="card" style="margin-bottom: 20px;">
              <strong>ETKİNLİK DETAYLARI:</strong><br>
              Salon: <strong>${venue?.name || 'Kraliyet Balo Salonu'}</strong> | Etkinlik Tarihi: <strong>${formatDate(res.date)}</strong> | Saat Dilimi: <strong>${res.timeSlot}</strong> | Davetli Sayısı: <strong>${res.guestCount} Kişi</strong>
            </div>

            <table>
              <thead>
                <tr>
                  <th>Hizmet / Kalem Açıklaması</th>
                  <th>Miktar / Kişi</th>
                  <th>Birim Fiyat</th>
                  <th>Toplam Tutarı</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>${venue?.name || 'Salon Kiralama Bedeli'}</td>
                  <td>1 Paket</td>
                  <td>${formatCurrency(res.venuePrice)}</td>
                  <td>${formatCurrency(res.venuePrice)}</td>
                </tr>
                ${res.selectedServices.map(s => {
                  const serv = services.find(x => x.id === s.serviceId);
                  return `
                    <tr>
                      <td>${serv?.name || 'Ek Hizmet'} ${s.isPaid ? '(Ödendi ✓)' : ''}</td>
                      <td>${s.quantity} ${serv?.pricingType === 'per_person' ? 'Kişi' : 'Adet'}</td>
                      <td>${formatCurrency(s.unitPrice)}</td>
                      <td>${formatCurrency(s.quantity * s.unitPrice)}</td>
                    </tr>
                  `;
                }).join('')}
              </tbody>
            </table>

            <div class="totals">
              <div>Ara Toplam: <strong>${formatCurrency(res.subtotal)}</strong></div>
              ${res.discountAmount > 0 ? `<div>Kampanya İndirimi (${res.campaignCode || 'İndirim'}): <strong style="color:#dc2626;">-${formatCurrency(res.discountAmount)}</strong></div>` : ''}
              <div>Hesaplanan KDV (%20): <strong>${formatCurrency(res.vatAmount)}</strong></div>
              <div class="grand-total">Genel Toplam Tutar: ${formatCurrency(res.totalAmount)}</div>
              <div style="margin-top:8px;">Tahsil Edilen Kapora: <strong style="color:#16a34a;">${formatCurrency(res.depositPaid)}</strong></div>
              <div>Kalan Ödenecek Bakiye: <strong style="color:#dc2626;">${formatCurrency(res.remainingBalance)}</strong></div>
            </div>

            <div class="signatures">
              <div class="sig-box">İrem Düğün Sarayı Yetkilisi<br>(İmza & Kaşe)</div>
              <div class="sig-box">Müşteri / Kiracı<br>(İmza)</div>
            </div>
          </body>
          </html>
        `);
        printWin.document.close();
        printWin.focus();
        setTimeout(() => printWin.print(), 500);
      };

      return (
        <div className="min-h-screen flex flex-col font-sans transition-colors duration-300">
          
          {/* HEADER */}
          <header role="banner" className="sticky top-0 z-40 glass-panel px-3 sm:px-6 py-2.5 flex flex-col sm:flex-row items-center justify-between gap-2 shadow-md">
            <div className="flex items-center justify-between w-full sm:w-auto">
              <div className="flex items-center space-x-2.5 cursor-pointer" onClick={() => navigateTo('dashboard')} role="button" tabIndex={0} aria-label="İrem Düğün Sarayı Ana Sayfa">
                <div className="w-9 h-9 sm:w-10 sm:h-10 rounded-xl gold-button flex items-center justify-center font-bold text-lg sm:text-xl shadow-lg" aria-hidden="true">
                  👑
                </div>
                <div>
                  <h1 className="font-heading font-extrabold text-base sm:text-lg lg:text-xl gold-gradient-text tracking-wide whitespace-nowrap">
                    İREM DÜĞÜN SARAYI
                  </h1>
                  <p className="text-[9px] sm:text-[10px] text-amber-600 dark:text-gold-400 font-medium">Kurumsal Organizasyon Portalı</p>
                </div>
              </div>
              <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=150&q=80" alt="Kullanıcı Profil Resmi" className="w-8 h-8 rounded-full border-2 border-amber-500/60 object-cover sm:hidden" />
            </div>

            {/* Controls & Role Switcher */}
            <div className="flex items-center space-x-2 w-full sm:w-auto overflow-x-auto no-scrollbar py-0.5 justify-center sm:justify-end">
              <div className="bg-white/90 dark:bg-brand-card/90 border border-amber-500/30 rounded-full p-1 flex items-center shadow-inner whitespace-nowrap overflow-x-auto no-scrollbar" role="group" aria-label="Kullanıcı Rolü Değiştirici">
                <span className="text-[10px] sm:text-[11px] font-semibold px-1.5 text-amber-700 dark:text-gold-400 hidden md:inline">Rol:</span>
                {[
                  { id: 'admin', label: 'Admin 👑' },
                  { id: 'satisci', label: 'Satışçı 💼' },
                  { id: 'sosyal_medyaci', label: 'Sosyal Medya 📸' },
                  { id: 'musteri', label: 'Müşteri 💑' }
                ].map(r => (
                  <button
                    key={r.id}
                    onClick={() => {
                      setActiveRole(r.id);
                      showToast(`Rol Değiştirildi: ${r.label}`);
                    }}
                    className={`px-2.5 sm:px-3 py-1 text-[10px] sm:text-xs font-semibold rounded-full transition whitespace-nowrap ${
                      activeRole === r.id ? 'gold-button font-bold shadow' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900'
                    }`}
                    aria-pressed={activeRole === r.id}
                  >
                    {r.label}
                  </button>
                ))}
              </div>

              <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=150&q=80" alt="Kullanıcı Profil Resmi" className="w-9 h-9 rounded-full border-2 border-amber-500/60 object-cover hidden sm:block shrink-0" />
            </div>
          </header>

          {/* LAYOUT BODY */}
          <div className="flex-1 flex overflow-hidden">
            
            {/* SIDEBAR */}
            <aside aria-label="Ana Gezinti Menüsü" className="w-64 glass-panel p-4 hidden lg:flex flex-col justify-between border-r border-slate-200 dark:border-brand-border/40">
              <nav className="space-y-1">
                <div className="text-[10px] font-bold text-slate-400 dark:text-gray-400 uppercase tracking-wider px-3 mb-2">Menü</div>
                {[
                  { id: 'dashboard', label: 'Anasayfa / İstatistikler', icon: '📊', roles: ['admin', 'satisci', 'sosyal_medyaci', 'musteri'] },
                  { id: 'create-reservation', label: '➕ Yeni Rezervasyon Oluştur', icon: '📝', roles: ['admin', 'satisci'] },
                  { id: 'venues', label: 'Düğün Salonlarım', icon: '🏛️', roles: ['admin', 'satisci'] },
                  { id: 'services', label: 'Ek Hizmetler', icon: '✨', roles: ['admin', 'satisci'] },
                  { id: 'reservations', label: 'Rezervasyonlarım', icon: '📋', roles: ['admin', 'satisci'] },
                  { id: 'calendar', label: 'Takvim Görünümü', icon: '📅', roles: ['admin', 'satisci'] },
                  { id: 'campaigns', label: 'Kampanyalar', icon: '🎁', roles: ['admin'] },
                  { id: 'finance', label: 'Finans & Fatura', icon: '💰', roles: ['admin'] },
                  { id: 'customers', label: 'Müşteri Rehberi', icon: '👥', roles: ['admin', 'satisci'] },
                  { id: 'users', label: 'Kullanıcı Yönetimi', icon: '⚙️', roles: ['admin'] },
                  { id: 'reports', label: 'Raporlar & AI Öneri', icon: '📈', roles: ['admin'] },
                  { id: 'media', label: 'Medya & Foto Yükle', icon: '📷', roles: ['sosyal_medyaci', 'admin', 'musteri'] }
                ]
                .filter(item => item.roles.includes(activeRole))
                .map(item => (
                  <a
                    key={item.id}
                    href={`#/${TAB_TO_SLUG[item.id]}`}
                    onClick={(e) => {
                      e.preventDefault();
                      navigateTo(item.id);
                    }}
                    className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl font-medium text-xs transition ${
                      activeTab === item.id ? 'bg-amber-500/10 text-amber-800 dark:text-gold-400 border border-amber-500/30 font-bold shadow-sm' : 'text-slate-600 dark:text-gray-400 hover:bg-slate-100 dark:hover:bg-brand-card hover:text-slate-900'
                    }`}
                    aria-current={activeTab === item.id ? 'page' : undefined}
                  >
                    <span className="text-base" aria-hidden="true">{item.icon}</span>
                    <span>{item.label}</span>
                  </a>
                ))}
              </nav>

              <div className="bg-white dark:bg-brand-card p-4 rounded-2xl border border-amber-500/20 text-center space-y-1 shadow-sm">
                <div className="text-xl" aria-hidden="true">🏰</div>
                <div className="text-xs font-bold text-amber-700 dark:text-gold-400">İrem Düğün Sarayı</div>
                <div className="text-[10px] text-slate-500 dark:text-gray-400">Sapanca / Sakarya</div>
              </div>
            </aside>

            {/* MAIN CONTENT AREA */}
            <main role="main" className="flex-1 p-4 lg:p-8 overflow-y-auto pb-24 lg:pb-8">
              
              {toast && (
                <div role="status" aria-live="polite" className="fixed top-20 right-6 z-50 px-5 py-3 rounded-xl bg-emerald-900 text-emerald-100 border border-emerald-500/50 shadow-2xl font-medium text-xs">
                  {toast.msg}
                </div>
              )}

              {/* RBAC PERMISSION GUARD */}
              {!isAuthorized ? (
                <UnauthorizedAccessScreen
                  pageTitle={TAB_LABELS[activeTab] || activeTab}
                  activeRoleName={ROLE_NAMES[activeRole]}
                  onGoHome={() => navigateTo('dashboard')}
                />
              ) : (
                <>
                  {activeTab === 'dashboard' && (
                    <DashboardComponent activeRole={activeRole} venues={venues} reservations={reservations} financialStats={financialStats} onNewResClick={() => navigateTo('create-reservation')} onTabChange={navigateTo} />
                  )}

                  {activeTab === 'create-reservation' && (
                    <CreateReservationPageComponent
                      venues={venues}
                      services={services}
                      customers={customers}
                      campaigns={campaigns}
                      reservations={reservations}
                      onSaveReservation={(newRes, newCust) => {
                        if (newCust) setCustomers(prev => [...prev, newCust]);
                        setReservations(prev => [newRes, ...prev]);
                        showToast('🎉 Yeni Rezervasyon ve Sözleşme Başarıyla Oluşturuldu!');
                        navigateTo('reservations');
                      }}
                      onCancel={() => navigateTo('reservations')}
                    />
                  )}

                  {activeTab === 'venues' && (
                    <VenuesComponent venues={venues} />
                  )}

                  {activeTab === 'services' && (
                    <ServicesComponent services={services} />
                  )}

                  {activeTab === 'reservations' && (
                    <ReservationsComponent reservations={filteredReservations} venues={venues} searchQuery={resSearchQuery} setSearchQuery={setResSearchQuery} statusFilter={resStatusFilter} setStatusFilter={setResStatusFilter} onNewResClick={() => navigateTo('create-reservation')} onDetailClick={setSelectedResForDetail} />
                  )}

                  {activeTab === 'calendar' && (
                    <CalendarComponent reservations={reservations} venues={venues} onResClick={setSelectedResForDetail} />
                  )}

                  {activeTab === 'campaigns' && (
                    <CampaignsComponent campaigns={campaigns} />
                  )}

                  {activeTab === 'finance' && (
                    <FinanceComponent financialStats={financialStats} reservations={reservations} />
                  )}

                  {activeTab === 'customers' && (
                    <CustomersComponent customers={customers} onAddClick={() => setCustomerModalData('new')} onEditClick={c => setCustomerModalData(c)} />
                  )}

                  {activeTab === 'users' && (
                    <UsersComponent users={users} />
                  )}

                  {activeTab === 'reports' && (
                    <ReportsComponent reservations={reservations} aiRecommendations={AI_RECOMMENDATIONS} />
                  )}

                  {activeTab === 'media' && (
                    <MediaComponent reservations={reservations} showToast={showToast} />
                  )}
                </>
              )}

            </main>
          </div>

          {/* MOBILE TAB BAR */}
          <nav aria-label="Mobil Gezinti Menüsü" className="lg:hidden fixed bottom-0 left-0 right-0 glass-panel border-t border-slate-200 dark:border-brand-border/40 px-2 py-2 z-40 flex justify-around items-center">
            {[
              { id: 'dashboard', label: 'Anasayfa', icon: '📊' },
              { id: 'create-reservation', label: 'Ekle', icon: '📝' },
              { id: 'reservations', label: 'Rezervasyon', icon: '📋' },
              { id: 'calendar', label: 'Takvim', icon: '📅' }
            ].map(tab => (
              <a key={tab.id} href={`#/${TAB_TO_SLUG[tab.id]}`} onClick={(e) => { e.preventDefault(); navigateTo(tab.id); }} className={`flex flex-col items-center py-1 px-3 rounded-xl ${activeTab === tab.id ? 'text-amber-700 dark:text-gold-400 font-bold bg-amber-500/10' : 'text-slate-500 dark:text-gray-400'}`} aria-current={activeTab === tab.id ? 'page' : undefined}>
                <span className="text-lg" aria-hidden="true">{tab.icon}</span>
                <span className="text-[10px]">{tab.label}</span>
              </a>
            ))}
          </nav>

          {/* MODALS */}
          {customerModalData && (
            <CustomerFormModal
              customer={customerModalData === 'new' ? null : customerModalData}
              onClose={() => setCustomerModalData(null)}
              onSave={(c) => {
                setCustomers(prev => c.id ? prev.map(x => x.id === c.id ? c : x) : [...prev, { ...c, id: 'cust-' + Date.now(), avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80' }]);
                showToast('👤 Müşteri Kartı Başarıyla Kaydedildi!');
                setCustomerModalData(null);
              }}
            />
          )}

          {selectedResForDetail && (
            <ReservationDetailModal
              res={selectedResForDetail}
              venues={venues}
              services={services}
              onClose={() => setSelectedResForDetail(null)}
              onPrintInvoice={() => handlePrintInvoice(selectedResForDetail)}
              onUpdatePayment={(id, dep, stat) => {
                setReservations(prev => prev.map(r => r.id === id ? { ...r, depositPaid: dep, remainingBalance: Math.max(0, r.totalAmount - dep), paymentStatus: stat } : r));
                showToast('💳 Ödeme & Sözleşme Güncellendi!');
                setSelectedResForDetail(null);
              }}
            />
          )}

        </div>
      );
    }

    // --- FULL PAGE VENUE DETAIL POPUP MODAL COMPONENT ---
    function VenueDetailModalComponent({ venue, onClose, onSelectVenue }) {
      if (!venue) return null;

      const interiorImages = [
        venue.image || 'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=800&q=80'
      ];

      const exteriorImages = [
        'https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1527529482837-4698179dc6ce?auto=format&fit=crop&w=800&q=80'
      ];

      const supportedEvents = [
        { title: 'Düğün Organizasyonu', icon: '💍', desc: 'Yemekli & Yemeksiz Düğün Baloları' },
        { title: 'Kına Gecesi Konsepti', icon: '👑', desc: 'Taht, Otantik Süslemeler & DJ' },
        { title: 'Nişan & Söz Töreni', icon: '✨', desc: 'Butik ve Şık Kutlamalar' },
        { title: 'Kurumsal Gala & Lansman', icon: '🥂', desc: 'VIP Şirket Etkinlikleri' }
      ];

      const availableServices = [
        'Gurme Yemek Servisi (Et / Tavuk / Vejetaryen)',
        '4K Fotoğraf & Sinematik Video Çekimi',
        'Canlı Müzik Orkestrası & Profesyonel DJ',
        'Özel Çiçekli Masa ve Sahne Dekoru',
        'Gelin Odası İkramları & VIP Karşılama'
      ];

      return (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/80 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 animate-fade-in">
          <div className="bg-white dark:bg-brand-card border border-amber-500/30 w-full max-w-4xl rounded-3xl shadow-2xl overflow-hidden my-auto space-y-0">
            
            {/* MODAL HEADER */}
            <div className="relative h-64 sm:h-80 overflow-hidden">
              <img src={venue.image} alt={venue.name} className="w-full h-full object-cover" />
              <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/40 to-transparent flex flex-col justify-end p-6 text-white">
                <div className="flex justify-between items-end">
                  <div>
                    <span className="gold-button text-xs font-bold px-3 py-1 rounded-full shadow">
                      📍 {venue.location || 'Sapanca Göl Kenarı, Sakarya'}
                    </span>
                    <h2 className="text-2xl sm:text-3xl font-heading font-extrabold text-white mt-2 drop-shadow">
                      {venue.name}
                    </h2>
                    <p className="text-xs text-gray-200 mt-1 max-w-2xl">{venue.description}</p>
                  </div>
                  <button onClick={onClose} className="w-10 h-10 rounded-full bg-white/20 hover:bg-red-600 text-white font-bold text-lg flex items-center justify-center backdrop-blur-md transition border border-white/30">
                    ✕
                  </button>
                </div>
              </div>
            </div>

            {/* MODAL CONTENT BODY */}
            <div className="p-6 space-y-6 max-h-[60vh] overflow-y-auto custom-scrollbar text-xs">
              
              {/* KEY SPECS GRID */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div className="bg-amber-500/10 border border-amber-500/30 p-3.5 rounded-2xl">
                  <span className="text-slate-500 block text-[11px] font-bold">Kapasite:</span>
                  <span className="text-base font-extrabold text-amber-800 dark:text-gold-400">👥 {venue.capacity} Kişi</span>
                </div>

                <div className="bg-amber-500/10 border border-amber-500/30 p-3.5 rounded-2xl">
                  <span className="text-slate-500 block text-[11px] font-bold">Kiralama Liste Fiyatı:</span>
                  <span className="text-base font-extrabold text-amber-800 dark:text-gold-400">{formatCurrency(venue.price)}</span>
                </div>

                <div className="bg-emerald-500/10 border border-emerald-500/30 p-3.5 rounded-2xl">
                  <span className="text-slate-500 block text-[11px] font-bold">Kapora Bedeli:</span>
                  <span className="text-base font-extrabold text-emerald-600">{formatCurrency(venue.deposit || 15000)}</span>
                </div>

                <div className="bg-blue-500/10 border border-blue-500/30 p-3.5 rounded-2xl">
                  <span className="text-slate-500 block text-[11px] font-bold">Sezonluk Doluluk Oranı:</span>
                  <div className="flex items-center space-x-2 mt-1">
                    <div className="flex-1 bg-slate-200 dark:bg-brand-dark h-2 rounded-full overflow-hidden">
                      <div className="bg-blue-600 h-full rounded-full" style={{ width: `${venue.occupancyRate || 85}%` }}></div>
                    </div>
                    <span className="font-extrabold text-blue-600">%{venue.occupancyRate || 85}</span>
                  </div>
                </div>
              </div>

              {/* İÇ GÖRSELLERİ GALERİSİ */}
              <div className="space-y-2">
                <h3 className="font-bold text-sm text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                  <span>🏰</span>
                  <span>İç Mekan & Balo Salonu Görselleri:</span>
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  {interiorImages.map((img, i) => (
                    <img key={i} src={img} alt="İç Mekan" className="w-full h-32 object-cover rounded-2xl border border-slate-200 dark:border-brand-border shadow-sm hover:scale-[1.02] transition" />
                  ))}
                </div>
              </div>

              {/* DIŞ GÖRSELLERİ GALERİSİ */}
              <div className="space-y-2">
                <h3 className="font-bold text-sm text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                  <span>🌅</span>
                  <span>Dış Mekan & Göl Manzarası Görselleri:</span>
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  {exteriorImages.map((img, i) => (
                    <img key={i} src={img} alt="Dış Mekan" className="w-full h-32 object-cover rounded-2xl border border-slate-200 dark:border-brand-border shadow-sm hover:scale-[1.02] transition" />
                  ))}
                </div>
              </div>

              {/* YAPILABİLECEK ETKİNLİKLER */}
              <div className="space-y-2">
                <h3 className="font-bold text-sm text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                  <span>🎉</span>
                  <span>Yapılabilecek Etkinlik Türleri:</span>
                </h3>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  {supportedEvents.map((ev, i) => (
                    <div key={i} className="bg-slate-50 dark:bg-brand-dark p-3 rounded-2xl border border-slate-200 dark:border-brand-border text-center space-y-1">
                      <div className="text-xl">{ev.icon}</div>
                      <div className="font-bold text-slate-800 dark:text-gray-200 text-xs">{ev.title}</div>
                      <div className="text-[10px] text-slate-500">{ev.desc}</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* SEÇİLEBİLECEK HİZMETLER */}
              <div className="space-y-2">
                <h3 className="font-bold text-sm text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                  <span>✨</span>
                  <span>Dahil Edilebilir Hizmet Paket İçerikleri:</span>
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {availableServices.map((srv, i) => (
                    <div key={i} className="flex items-center space-x-2 bg-slate-50 dark:bg-brand-dark p-2.5 rounded-xl border border-slate-200 dark:border-brand-border font-semibold text-slate-700 dark:text-gray-300">
                      <span className="text-emerald-500 font-bold">✓</span>
                      <span>{srv}</span>
                    </div>
                  ))}
                </div>
              </div>

            </div>

            {/* MODAL FOOTER */}
            <div className="p-4 bg-slate-50 dark:bg-brand-dark border-t border-slate-200 dark:border-brand-border flex justify-between items-center">
              <button onClick={onClose} className="px-5 py-2.5 bg-slate-200 dark:bg-brand-card text-slate-700 dark:text-gray-300 rounded-xl text-xs font-bold hover:bg-slate-300">
                Kapat
              </button>
              <button
                onClick={() => {
                  onSelectVenue(venue);
                  onClose();
                }}
                className="gold-button font-extrabold px-6 py-2.5 rounded-xl text-xs shadow-lg"
              >
                Bu Salonu Seç ve Rezervasyona Ekle ✓
              </button>
            </div>

          </div>
        </div>
      );
    }

    // --- FULL PAGE DEDICATED RESERVATION WORKSPACE COMPONENT ---
    function CreateReservationPageComponent({ venues, services, customers, campaigns, reservations, onSaveReservation, onCancel }) {
      // 1. Venue, Start/End Date & Time
      const venueCarouselRef = useRef(null);
      const [selectedVenueForDetail, setSelectedVenueForDetail] = useState(null);
      const [venueId, setVenueId] = useState(venues[0]?.id || 'v1');
      const [customVenuePrice, setCustomVenuePrice] = useState(venues[0]?.price || 65000);
      const [startDate, setStartDate] = useState('2026-08-25');
      const [startTime, setStartTime] = useState('19:00');
      const [endDate, setEndDate] = useState('2026-08-25');
      const [endTime, setEndTime] = useState('23:00');
      const [guestCount, setGuestCount] = useState(500);

      const eventDate = startDate;
      const activeSlot = `${startTime} - ${endTime}`;

      const scrollVenueCarouselLeft = () => {
        if (venueCarouselRef.current) {
          venueCarouselRef.current.scrollBy({ left: -260, behavior: 'smooth' });
        }
      };
      const scrollVenueCarouselRight = () => {
        if (venueCarouselRef.current) {
          venueCarouselRef.current.scrollBy({ left: 260, behavior: 'smooth' });
        }
      };

      // Update customVenuePrice when venueId changes
      useEffect(() => {
        const v = venues.find(x => x.id === venueId);
        if (v) setCustomVenuePrice(v.price);
      }, [venueId]);

      // 2. Customer & Auto-Membership (DEFAULT TO NEW MEMBER)
      const [customerMode, setCustomerMode] = useState('new'); // 'new' or 'existing'
      const [selectedCustomerId, setSelectedCustomerId] = useState(customers[0]?.id || 'cust1');
      const [customerSearchQuery, setCustomerSearchQuery] = useState('');
      const [newCustName, setNewCustName] = useState('');
      const [newCustEmail, setNewCustEmail] = useState('');
      const [newCustPhone, setNewCustPhone] = useState('');
      const [newCustSecondaryPhone, setNewCustSecondaryPhone] = useState('');

      // 3. Services & Per-service Guest Quantities & Paid status & Custom Unit Prices
      const [selectedServices, setSelectedServices] = useState([
        { serviceId: 's1', quantity: 500, customUnitPrice: 350, isPaid: true },
        { serviceId: 's2', quantity: 1, customUnitPrice: 18000, isPaid: true },
        { serviceId: 's3', quantity: 1, customUnitPrice: 25000, isPaid: false }
      ]);

      // 4. Financials, Referrer, Deposit & Promo
      const [referrerName, setReferrerName] = useState('');
      const [campaignCode, setCampaignCode] = useState('');
      const [hasDeposit, setHasDeposit] = useState(true);
      const [depositPaid, setDepositPaid] = useState(40000);
      const [paymentStatus, setPaymentStatus] = useState('Kapora Alındı');

      // 5. Invoicing Details (Bireysel / Tüzel) - DEFAULT TO UNCHECKED
      const [isInvoiced, setIsInvoiced] = useState(false);
      const [invoiceType, setInvoiceType] = useState('individual'); // 'individual' or 'corporate'
      const [tcNo, setTcNo] = useState('12345678901');
      const [vknNo, setVknNo] = useState('9876543210');
      const [taxOffice, setTaxOffice] = useState('Sapanca VD');
      const [invoiceAddress, setInvoiceAddress] = useState('Atatürk Mah. Sapanca / Sakarya');

      // 6. Flow Planning & Notes (Draggable & Reorderable)
      const [flowPlan, setFlowPlan] = useState([
        { time: '19:00', title: 'Misafir Karşılama & Kokteyl' },
        { time: '19:30', title: 'Gelin Damat Giriş & İlk Dans' },
        { time: '20:15', title: 'Yemek Servisi' },
        { time: '21:30', title: 'Pasta Kesimi & Şov' },
        { time: '22:00', title: 'Takı & Eğlence' }
      ]);
      const [draggedIdx, setDraggedIdx] = useState(null);
      const [dragOverIdx, setDragOverIdx] = useState(null);
      const [notes, setNotes] = useState('Özel çiçek süslemeleri ve gelin odası ikramları dahildir.');

      const handleDragStart = (e, index) => {
        setDraggedIdx(index);
        e.dataTransfer.effectAllowed = "move";
        e.dataTransfer.setData("text/plain", index.toString());
      };

      const handleDragOver = (e, index) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = "move";
        if (dragOverIdx !== index) {
          setDragOverIdx(index);
        }
      };

      const handleDrop = (e, index) => {
        e.preventDefault();
        if (draggedIdx === null || draggedIdx === index) return;
        setFlowPlan(prev => {
          const list = [...prev];
          const [removed] = list.splice(draggedIdx, 1);
          list.splice(index, 0, removed);
          return list;
        });
        setDraggedIdx(null);
        setDragOverIdx(null);
      };

      const handleDragEnd = () => {
        setDraggedIdx(null);
        setDragOverIdx(null);
      };

      const moveFlowItemUp = (index) => {
        if (index <= 0) return;
        setFlowPlan(prev => {
          const list = [...prev];
          const temp = list[index - 1];
          list[index - 1] = list[index];
          list[index] = temp;
          return list;
        });
      };

      const moveFlowItemDown = (index) => {
        setFlowPlan(prev => {
          if (index >= prev.length - 1) return prev;
          const list = [...prev];
          const temp = list[index + 1];
          list[index + 1] = list[index];
          list[index] = temp;
          return list;
        });
      };

      // Collision Check Logic
      const collisionDetected = useMemo(() => {
        return reservations.some(r => r.venueId === venueId && r.date === eventDate && r.timeSlot === activeSlot);
      }, [reservations, venueId, eventDate, activeSlot]);

      const selectedVenue = venues.find(v => v.id === venueId);
      const existingCustomer = customers.find(c => c.id === selectedCustomerId);

      // Financial Calculation
      const calculations = useMemo(() => {
        const vPrice = Number(customVenuePrice) || 0;
        let servTotal = 0;
        const mappedServices = selectedServices.map(item => {
          const s = services.find(x => x.id === item.serviceId);
          if (!s) return null;
          const unitPrice = item.customUnitPrice !== undefined ? Number(item.customUnitPrice) : s.price;
          const qty = s.pricingType === 'per_person' ? item.quantity : 1;
          const cost = unitPrice * qty;
          servTotal += cost;
          return { serviceId: s.id, quantity: qty, unitPrice, isPaid: item.isPaid };
        }).filter(Boolean);

        const sub = vPrice + servTotal;
        let disc = 0;
        if (campaignCode === 'IREM2026') disc = sub * 0.10;
        else if (campaignCode === 'VIP5000') disc = 5000;

        const afterDisc = Math.max(0, sub - disc);
        const vat = isInvoiced ? afterDisc * 0.20 : 0;
        const grandTotal = afterDisc + vat;
        const dep = hasDeposit ? depositPaid : 0;
        const remaining = Math.max(0, grandTotal - dep);

        return { vPrice, servTotal, sub, disc, vat, grandTotal, dep, remaining, mappedServices };
      }, [customVenuePrice, selectedServices, campaignCode, hasDeposit, depositPaid, isInvoiced, services]);

      const handleAddFlowItem = () => {
        setFlowPlan(prev => [...prev, { time: '22:30', title: 'Yeni Akış Adımı' }]);
      };
      const handleRemoveFlowItem = (index) => {
        setFlowPlan(prev => prev.filter((_, i) => i !== index));
      };

      const handleSubmit = () => {
        if (collisionDetected) return;
        
        let custId = selectedCustomerId;
        let custName = existingCustomer?.name || 'Müşteri';
        let custEmail = existingCustomer?.email || '';
        let custPhone = existingCustomer?.phone || '';
        let custSecondaryPhone = existingCustomer?.secondaryPhone || '';
        let newCustomerObj = null;

        if (customerMode === 'new') {
          custId = 'cust-' + Date.now();
          custName = newCustName || 'Yeni Müşteri';
          custEmail = newCustEmail;
          custPhone = newCustPhone;
          custSecondaryPhone = newCustSecondaryPhone;
          newCustomerObj = {
            id: custId,
            name: custName,
            email: custEmail,
            phone: custPhone,
            secondaryPhone: custSecondaryPhone,
            address: invoiceAddress,
            taxType: invoiceType,
            tcNo: invoiceType === 'individual' ? tcNo : '',
            vknNo: invoiceType === 'corporate' ? vknNo : '',
            taxOffice,
            followUp: false,
            followUpNote: 'Otomatik kayıt oluşturan üye',
            avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'
          };
        }

        const newRes = {
          id: `RES-${new Date().getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`,
          venueId,
          customerId: custId,
          customerName: custName,
          customerEmail: custEmail,
          customerPhone: custPhone,
          secondaryPhone: custSecondaryPhone,
          date: eventDate,
          timeSlot: activeSlot,
          guestCount,
          selectedServices: calculations.mappedServices,
          venuePrice: calculations.vPrice,
          subtotal: calculations.sub,
          campaignCode,
          discountAmount: calculations.disc,
          vatAmount: calculations.vat,
          totalAmount: calculations.grandTotal,
          depositPaid: calculations.dep,
          remainingBalance: calculations.remaining,
          paymentStatus: paymentStatus,
          isInvoiced,
          invoiceType,
          tcNo: invoiceType === 'individual' ? tcNo : '',
          vknNo: invoiceType === 'corporate' ? vknNo : '',
          taxOffice,
          invoiceAddress,
          notes,
          flowPlan,
          mediaGallery: []
        };

        onSaveReservation(newRes, newCustomerObj);
      };

      return (
        <div className="space-y-6 max-w-7xl mx-auto pb-12">
          
          {/* VENUE DETAIL POPUP MODAL */}
          {selectedVenueForDetail && (
            <VenueDetailModalComponent
              venue={selectedVenueForDetail}
              onClose={() => setSelectedVenueForDetail(null)}
              onSelectVenue={(v) => {
                setVenueId(v.id);
                setCustomVenuePrice(v.price);
              }}
            />
          )}

          {/* PAGE HEADER */}
          <div className="glass-panel p-4 sm:p-6 rounded-3xl border border-amber-500/30 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 shadow-sm">
            <div className="space-y-1">
              <span className="inline-block bg-amber-500/10 text-amber-800 dark:text-gold-400 text-[11px] sm:text-xs font-bold px-3 py-1 rounded-full border border-amber-500/20 leading-normal">
                📝 Rezervasyon Oluşturma ve Kiralama
              </span>
              <h2 className="text-xl sm:text-2xl font-heading font-extrabold gold-gradient-text mt-1">
                Hayalinizdeki düğünü birlikte planlayalım!
              </h2>
              <p className="text-[11px] sm:text-xs text-slate-500 dark:text-gray-400">Salon kiralama, hizmet adetleri, müşteri üyelik kaydı, fatura ve etkinlik akışını tek ekranda yönetin.</p>
            </div>
            <button onClick={onCancel} className="w-full sm:w-auto px-4 py-2.5 bg-slate-100 dark:bg-brand-card text-slate-700 dark:text-gray-300 rounded-xl text-xs font-bold hover:bg-slate-200 text-center whitespace-nowrap shrink-0">
              ← Rezervasyon Listesine Dön
            </button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            {/* LEFT COLUMN: FORM SECTIONS (8 Cols) */}
            <div className="lg:col-span-8 space-y-6">
              
              {/* SECTION 1: SALON & TARİH SEÇİMİ (BAŞLIK KALDIRILDI - ALANDAN TASARRUF) */}
              <div className="glass-panel p-3.5 sm:p-6 rounded-3xl space-y-4 shadow-sm border border-slate-200 dark:border-brand-border">

                {/* VISUAL HORIZONTAL SCROLLABLE VENUE CAROUSEL WITH ARROW CONTROLS */}
                <div>
                  <div className="flex justify-between items-center mb-2 px-1">
                    <label className="font-bold text-slate-800 dark:text-gray-200 text-xs flex items-center space-x-1">
                      <span>🏛️ Düğün Salonu Seçin (Yatay Kayan Kartlar):</span>
                    </label>
                    
                    {/* Interactive Arrow Navigation Buttons */}
                    <div className="flex items-center space-x-1.5">
                      <button
                        type="button"
                        onClick={scrollVenueCarouselLeft}
                        className="w-7 h-7 rounded-full border border-amber-500/40 bg-white dark:bg-brand-card text-amber-800 dark:text-gold-400 hover:bg-amber-500 hover:text-white font-bold text-xs shadow flex items-center justify-center transition active:scale-95 cursor-pointer"
                        title="Sola Kaydır"
                        aria-label="Salonları Sola Kaydır"
                      >
                        ❮
                      </button>
                      <button
                        type="button"
                        onClick={scrollVenueCarouselRight}
                        className="w-7 h-7 rounded-full border border-amber-500/40 bg-white dark:bg-brand-card text-amber-800 dark:text-gold-400 hover:bg-amber-500 hover:text-white font-bold text-xs shadow flex items-center justify-center transition active:scale-95 cursor-pointer"
                        title="Sağa Kaydır"
                        aria-label="Salonları Sağa Kaydır"
                      >
                        ❯
                      </button>
                    </div>
                  </div>

                  <div ref={venueCarouselRef} className="flex overflow-x-auto gap-3.5 pb-3 pt-1 no-scrollbar snap-x snap-mandatory scroll-smooth px-1">
                    {venues.map(v => {
                      const isSelected = venueId === v.id;
                      return (
                        <div
                          key={v.id}
                          onClick={() => {
                            setVenueId(v.id);
                            setCustomVenuePrice(v.price);
                          }}
                          className={`shrink-0 w-64 sm:w-68 rounded-2xl border-2 transition-all duration-300 cursor-pointer overflow-hidden snap-start flex flex-col justify-between shadow-sm ${
                            isSelected
                              ? 'border-amber-500 bg-amber-500/10 shadow-md ring-2 ring-amber-500/40'
                              : 'border-slate-200 dark:border-brand-border bg-white dark:bg-brand-card hover:border-amber-500/50'
                          }`}
                        >
                          {/* PHOTO AREA WITH BADGES (NO OVERLAPPING TEXT) */}
                          <div className="relative h-32 sm:h-36 w-full bg-slate-200 dark:bg-brand-dark overflow-hidden shrink-0">
                            <img src={v.image} alt={v.name} className="w-full h-full object-cover transition-transform duration-500 hover:scale-105" />
                            
                            <div className="absolute top-2 right-2 bg-slate-900/80 backdrop-blur-md text-white text-[10px] font-bold px-2 py-0.5 rounded-full border border-white/20 z-10">
                              👥 {v.capacity} Kişi
                            </div>
                            
                            {isSelected && (
                              <div className="absolute top-2 left-2 gold-button text-[11px] font-extrabold px-2.5 py-0.5 rounded-full shadow z-10">
                                SEÇİLDİ ✓
                              </div>
                            )}

                            {/* 🔍 DETAYLAR FULL PAGE POPUP BUTTON */}
                            <button
                              type="button"
                              onClick={(e) => {
                                e.stopPropagation();
                                setSelectedVenueForDetail(v);
                              }}
                              className="absolute bottom-2 right-2 bg-slate-900/90 hover:bg-amber-600 text-white text-[10px] font-bold px-2 py-1 rounded-lg border border-white/30 transition flex items-center space-x-1 shadow z-10"
                              title="Salon Detaylarını Göster"
                            >
                              <span>🔍</span>
                              <span>Detaylar</span>
                            </button>
                          </div>

                          {/* CARD BODY CONTENT BELOW PHOTO (STRICTLY SEPARATED) */}
                          <div className="p-3 space-y-1.5 flex-1 flex flex-col justify-between bg-white dark:bg-brand-card">
                            <div>
                              <h4 className="font-heading font-extrabold text-xs sm:text-sm text-slate-800 dark:text-gray-100 leading-tight">
                                {v.name}
                              </h4>
                              <p className="text-[10px] text-slate-500 dark:text-gray-400 line-clamp-1 mt-1">{v.description}</p>
                            </div>

                            <div className="pt-2 border-t border-slate-100 dark:border-brand-border flex justify-between items-center text-xs">
                              <span className="text-[10px] font-bold text-slate-500">Liste Fiyatı:</span>
                              <span className="font-extrabold text-xs text-amber-700 dark:text-gold-400">{formatCurrency(v.price)}</span>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs pt-1">
                  <div>
                    <label className="font-bold text-slate-700 dark:text-gray-300 block mb-1">Bu Rezervasyona Özel Salon Kiralama Fiyatı (TL):</label>
                    <input
                      type="number"
                      value={customVenuePrice}
                      onChange={e => setCustomVenuePrice(Number(e.target.value))}
                      className="w-full bg-amber-500/10 border border-amber-500/40 rounded-xl p-2.5 text-amber-800 dark:text-gold-400 font-extrabold"
                    />
                  </div>

                  <div>
                    <label className="font-bold text-slate-700 dark:text-gray-300 block mb-1">Davetli Sayısı (Kişi):</label>
                    <input type="number" value={guestCount} onChange={e => setGuestCount(Number(e.target.value))} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold" />
                  </div>
                </div>

                {/* START AND END DATE & TIME SELECTION */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs pt-2 border-t border-slate-100 dark:border-brand-border">
                  <div className="space-y-2">
                    <label className="font-bold text-slate-800 dark:text-gray-200 block">📅 Etkinlik Başlangıç Tarihi & Saati:</label>
                    <div className="grid grid-cols-2 gap-2">
                      <input type="date" value={startDate} onChange={e => setStartDate(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold" />
                      <input type="time" value={startTime} onChange={e => setStartTime(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold" />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <label className="font-bold text-slate-800 dark:text-gray-200 block">🏁 Etkinlik Bitiş Tarihi & Saati:</label>
                    <div className="grid grid-cols-2 gap-2">
                      <input type="date" value={endDate} onChange={e => setEndDate(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold" />
                      <input type="time" value={endTime} onChange={e => setEndTime(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold" />
                    </div>
                  </div>
                </div>

                {/* LIVE CALENDAR PREVIEW & OCCUPANCY TIMELINE */}
                <div className="bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border p-4 rounded-2xl space-y-2 text-xs">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-slate-800 dark:text-gray-200 flex items-center space-x-1">
                      <span>🗓️ Canlı Takvim & Çakışma Önizlemesi ({selectedVenue?.name}):</span>
                    </span>
                    <span className="text-[10px] bg-amber-500/10 text-amber-800 dark:text-gold-400 font-bold px-2 py-0.5 rounded-full border border-amber-500/20">
                      Seçilen: {formatDate(startDate)} ({startTime} - {endTime})
                    </span>
                  </div>

                  <div className="grid grid-cols-7 gap-1 text-center font-bold text-[10px] text-slate-500 pt-1">
                    <span>Pzt</span><span>Sal</span><span>Çar</span><span>Per</span><span>Cum</span><span>Cmt</span><span>Paz</span>
                  </div>

                  {/* MINI CALENDAR DAYS GRID */}
                  <div className="grid grid-cols-7 gap-1 text-[11px]">
                    {[...Array(14)].map((_, i) => {
                      const dayDate = new Date(2026, 7, 20 + i);
                      const dateStr = dayDate.toISOString().split('T')[0];
                      const isSelectedDate = dateStr === startDate;
                      const hasExistingBooking = reservations.some(r => r.venueId === venueId && r.eventDate === dateStr && r.status !== 'İptal');

                      return (
                        <div
                          key={dateStr}
                          onClick={() => {
                            setStartDate(dateStr);
                            setEndDate(dateStr);
                          }}
                          className={`p-2 rounded-xl text-center cursor-pointer transition border flex flex-col justify-between h-12 ${
                            isSelectedDate
                              ? 'gold-button shadow font-extrabold border-amber-500'
                              : hasExistingBooking
                              ? 'bg-red-500/10 border-red-500/30 text-red-700 dark:text-red-400 font-bold'
                              : 'bg-white dark:bg-brand-card border-slate-200 dark:border-brand-border text-slate-700 dark:text-gray-300 hover:border-amber-500/50'
                          }`}
                        >
                          <span className="text-[9px] opacity-75">{dayDate.getDate()} Ağu</span>
                          <span className="text-[9px] font-bold">
                            {isSelectedDate ? 'SEÇİLDİ' : hasExistingBooking ? 'DOLU 🔒' : 'BOŞ ✨'}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {collisionDetected && (
                  <div className="bg-red-500/10 border border-red-500/40 p-4 rounded-2xl text-red-600 dark:text-red-400 font-bold text-xs flex items-center space-x-3 shadow-sm">
                    <span className="text-xl">⚠️</span>
                    <div>
                      <div>ÇAKIŞMA UYARISI: Daha önce rezerve edilmiş gün/saat!</div>
                      <div className="text-[11px] font-normal mt-0.5">Seçtiğiniz <strong>{selectedVenue?.name}</strong> salonu <strong>{formatDate(startDate)}</strong> tarihinde <strong>{activeSlot}</strong> saat diliminde doludur. Lütfen farklı bir gün veya saat dilimi seçiniz.</div>
                    </div>
                  </div>
                )}
              </div>

              {/* SECTION 2: MÜŞTERİ BİLGİLERİ VE OTOMATİK ÜYELİK (BAŞLIK & DÜĞME HİZALAMASI YENİLENDİ) */}
              <div className="glass-panel p-6 rounded-3xl space-y-4 shadow-sm border border-slate-200 dark:border-brand-border">
                <div className="border-b border-slate-200 dark:border-brand-border pb-3 space-y-3">
                  <div className="flex items-center space-x-2">
                    <span className="text-lg">👥</span>
                    <h3 className="font-bold text-base text-slate-800 dark:text-gray-100">2. Müşteri İletişim & Otomatik Üyelik Kartı</h3>
                  </div>

                  {/* MODES BUTTONS MOVED BELOW TITLE AND CENTERED ON MOBILE (AUTOMATIC MEMBER FIRST) */}
                  <div className="flex flex-wrap justify-center sm:justify-start gap-2 text-xs font-bold">
                    <button onClick={() => setCustomerMode('new')} className={`px-3.5 py-2 rounded-xl border transition ${customerMode === 'new' ? 'gold-button shadow' : 'bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-400'}`}>
                      ➕ Otomatik Yeni Üyelik Oluştur
                    </button>
                    <button onClick={() => setCustomerMode('existing')} className={`px-3.5 py-2 rounded-xl border transition ${customerMode === 'existing' ? 'gold-button shadow' : 'bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-400'}`}>
                      👥 Müşteri Rehberinden Seç
                    </button>
                  </div>
                </div>

                {customerMode === 'existing' ? (
                  <div className="text-xs space-y-2">
                    <label className="font-bold text-slate-700 dark:text-gray-300 block">Mevcut Müşteri Ara ve Seçin:</label>
                    
                    {/* SEARCHABLE LIVE INPUT FOR EXISTING CUSTOMERS */}
                    <input
                      type="text"
                      placeholder="🔍 Ad, Soyad, Telefon veya E-posta ile Hızlı Ara..."
                      value={customerSearchQuery}
                      onChange={e => setCustomerSearchQuery(e.target.value)}
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-amber-500/40 rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-medium shadow-sm focus:ring-2 focus:ring-amber-500"
                    />

                    <select
                      value={selectedCustomerId}
                      onChange={e => setSelectedCustomerId(e.target.value)}
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold"
                    >
                      {customers
                        .filter(c => {
                          if (!customerSearchQuery.trim()) return true;
                          const q = customerSearchQuery.toLowerCase();
                          return (c.name || '').toLowerCase().includes(q) || (c.phone || '').includes(q) || (c.email || '').toLowerCase().includes(q);
                        })
                        .map(c => (
                          <option key={c.id} value={c.id}>
                            {c.name} (Tel: {c.phone} | {c.email})
                          </option>
                        ))}
                    </select>
                  </div>
                ) : (
                  <div className="space-y-3 text-xs">
                    <div className="bg-amber-500/10 border border-amber-500/30 p-2.5 rounded-xl text-amber-800 dark:text-gold-400 font-bold">
                      ✨ Bu kişi için sistemde otomatik olarak yeni üye ve müşteri kartı oluşturulacaktır.
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      <div><label className="font-bold block mb-1">Adı Soyadı / Firma Unvanı:</label><input type="text" placeholder="Örn: Mehmet Yılmaz & Zeynep Can" value={newCustName} onChange={e => setNewCustName(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5" /></div>
                      <div><label className="font-bold block mb-1">E-posta Adresi:</label><input type="email" placeholder="ornek@domain.com" value={newCustEmail} onChange={e => setNewCustEmail(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5" /></div>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      <div><label className="font-bold block mb-1">Birincil Telefon (+90):</label><input type="text" placeholder="+90 532 000 0000" value={newCustPhone} onChange={e => setNewCustPhone(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5" /></div>
                      <div><label className="font-bold block mb-1">İkinci İletişim / Yakın Telefonu:</label><input type="text" placeholder="+90 535 000 0000 (Anne/Baba Tel)" value={newCustSecondaryPhone} onChange={e => setNewCustSecondaryPhone(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5" /></div>
                    </div>
                  </div>
                )}
              </div>

              {/* SECTION 3: HİZMETLER VE HİZMET BAZLI KİŞİ SAYILARI */}
              <div className="glass-panel p-6 rounded-3xl space-y-4 shadow-sm border border-slate-200 dark:border-brand-border">
                <div className="flex items-center space-x-2 border-b border-slate-200 dark:border-brand-border pb-3">
                  <span className="text-lg">✨</span>
                  <h3 className="font-bold text-base text-slate-800 dark:text-gray-100">3. Alınan Ek Hizmetler & Hizmet Bazlı Kişi/Adet Sayıları</h3>
                </div>

                <div className="space-y-3">
                  {services.map(s => {
                    const found = selectedServices.find(x => x.serviceId === s.id);
                    const isSelected = !!found;
                    const qty = found ? found.quantity : (s.pricingType === 'per_person' ? guestCount : 1);
                    const isPaid = found ? found.isPaid : false;

                    return (
                      <div key={s.id} className={`p-4 rounded-2xl border transition space-y-2 ${isSelected ? 'bg-amber-500/10 border-amber-500/50' : 'bg-slate-50 dark:bg-brand-dark border-slate-200 dark:border-brand-border'}`}>
                        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
                          <label className="flex items-center space-x-3 cursor-pointer">
                            <input
                              type="checkbox"
                              checked={isSelected}
                              onChange={e => {
                                if (e.target.checked) {
                                  setSelectedServices(prev => [...prev, { serviceId: s.id, quantity: s.pricingType === 'per_person' ? guestCount : 1, isPaid: false }]);
                                } else {
                                  setSelectedServices(prev => prev.filter(x => x.serviceId !== s.id));
                                }
                              }}
                              className="w-5 h-5 accent-amber-600 rounded"
                            />
                            <div>
                              <div className="font-bold text-xs text-slate-800 dark:text-gray-200">{s.name}</div>
                              <div className="text-[10px] text-slate-500">{s.description} | {formatCurrency(s.price)} {s.pricingType === 'per_person' ? '/Kişi' : '/Paket'}</div>
                            </div>
                          </label>

                          {isSelected && (
                            <div className="flex flex-wrap items-center gap-3 text-xs">
                              <div className="flex items-center space-x-1">
                                <span className="font-bold">Özel Birim Fiyat (TL):</span>
                                <input
                                  type="number"
                                  value={found.customUnitPrice !== undefined ? found.customUnitPrice : s.price}
                                  onChange={e => {
                                    const val = Number(e.target.value);
                                    setSelectedServices(prev => prev.map(x => x.serviceId === s.id ? { ...x, customUnitPrice: val } : x));
                                  }}
                                  className="w-24 bg-amber-500/10 border border-amber-500/40 rounded-lg p-1 font-bold text-center text-amber-800 dark:text-gold-400"
                                />
                              </div>

                              {s.pricingType === 'per_person' && (
                                <div className="flex items-center space-x-1">
                                  <span className="font-bold">Kişi Sayısı:</span>
                                  <input
                                    type="number"
                                    value={qty}
                                    onChange={e => {
                                      const val = Number(e.target.value);
                                      setSelectedServices(prev => prev.map(x => x.serviceId === s.id ? { ...x, quantity: val } : x));
                                    }}
                                    className="w-20 bg-white dark:bg-brand-card border border-slate-200 rounded-lg p-1 font-bold text-center"
                                  />
                                </div>
                              )}

                              {/* UNCHECKED PAID STATE STYLING FIX */}
                              <label className={`flex items-center space-x-1 font-bold cursor-pointer ${isPaid ? 'text-emerald-600' : 'text-slate-500 dark:text-gray-400'}`}>
                                <input
                                  type="checkbox"
                                  checked={isPaid}
                                  onChange={e => {
                                    const checked = e.target.checked;
                                    setSelectedServices(prev => prev.map(x => x.serviceId === s.id ? { ...x, isPaid: checked } : x));
                                  }}
                                  className={`w-4 h-4 ${isPaid ? 'accent-emerald-600' : 'accent-slate-400'}`}
                                />
                                <span>{isPaid ? 'Ödendi ✓' : 'Ödenmedi'}</span>
                              </label>
                            </div>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* SECTION 4: FİNANS, REFERANS BİLGİLERİ VE KAPORA */}
              <div className="glass-panel p-6 rounded-3xl space-y-4 shadow-sm border border-slate-200 dark:border-brand-border">
                <div className="flex items-center space-x-2 border-b border-slate-200 dark:border-brand-border pb-3">
                  <span className="text-lg">💰</span>
                  <h3 className="font-bold text-base text-slate-800 dark:text-gray-100">4. Ödeme, Kapora & İndirim Kodu Bilgileri</h3>
                </div>

                {/* REFERRER NAME INPUT AT THE VERY TOP */}
                <div className="text-xs">
                  <label className="font-bold block mb-1">Referans / Aracılık Eden (İsim Soyisim):</label>
                  <input
                    type="text"
                    placeholder="Örn: Ahmet Yılmaz (Organizasyon Koçu / Aile Yakını)"
                    value={referrerName}
                    onChange={e => setReferrerName(e.target.value)}
                    className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-200"
                  />
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
                  <div>
                    <label className="font-bold block mb-1">İndirim Kodu:</label>
                    <select value={campaignCode} onChange={e => setCampaignCode(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold">
                      <option value="">İndirim Kodu Yok</option>
                      {campaigns.map(c => <option key={c.id} value={c.code}>{c.code} - {c.title}</option>)}
                    </select>
                  </div>

                  <div>
                    <label className="font-bold block mb-1">Kapora Ödendi Mi?</label>
                    <select value={hasDeposit ? 'yes' : 'no'} onChange={e => setHasDeposit(e.target.value === 'yes')} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold">
                      <option value="yes">Evet, Kapora Alındı</option>
                      <option value="no">Hayır, Henüz Ödenmedi</option>
                    </select>
                  </div>

                  {hasDeposit && (
                    <div>
                      <label className="font-bold block mb-1">Ödenen Kapora Tutarı (TL):</label>
                      <input type="number" value={depositPaid} onChange={e => setDepositPaid(Number(e.target.value))} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold text-emerald-600" />
                    </div>
                  )}
                </div>

                <div className="text-xs">
                  <label className="font-bold block mb-1">Genel Ödeme Statüsü:</label>
                  <select value={paymentStatus} onChange={e => setPaymentStatus(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold">
                    <option value="Bekliyor">Bekliyor</option>
                    <option value="Kapora Alındı">Kapora Alındı</option>
                    <option value="Ödendi">Ödendi (Tam ödeme yapıldı)</option>
                    <option value="Tamamlandı">Tamamlandı</option>
                  </select>
                </div>
              </div>

              {/* SECTION 5: FATURA BİLGİLERİ (BAŞLIK VE TİK HİZALAMASI YENİLENDİ) */}
              <div className="glass-panel p-6 rounded-3xl space-y-4 shadow-sm border border-slate-200 dark:border-brand-border">
                <div className="border-b border-slate-200 dark:border-brand-border pb-3 space-y-2">
                  <div className="flex items-center space-x-2">
                    <span className="text-lg">📄</span>
                    <h3 className="font-bold text-base text-slate-800 dark:text-gray-100">5. Fatura Bilgileri (Resmi Belge Düzenleme)</h3>
                  </div>
                  
                  {/* INVOICE TOGGLE PLACED ON OWN ROW BELOW TITLE (UNCHECKED BY DEFAULT) */}
                  <label className="flex items-center space-x-2 text-xs font-bold cursor-pointer pt-1">
                    <input type="checkbox" checked={isInvoiced} onChange={e => setIsInvoiced(e.target.checked)} className="w-4 h-4 accent-amber-600" />
                    <span>Faturalı İşlem (%20 KDV Hesapla)</span>
                  </label>
                </div>

                {isInvoiced && (
                  <div className="space-y-4 text-xs">
                    <div>
                      <label className="font-bold block mb-1">Fatura Tipi:</label>
                      <div className="flex space-x-4">
                        <label className="flex items-center space-x-2 cursor-pointer font-bold">
                          <input type="radio" name="invType" value="individual" checked={invoiceType === 'individual'} onChange={() => setInvoiceType('individual')} className="accent-amber-600" />
                          <span>Bireysel Fatura (TC Kimlik No)</span>
                        </label>
                        <label className="flex items-center space-x-2 cursor-pointer font-bold">
                          <input type="radio" name="invType" value="corporate" checked={invoiceType === 'corporate'} onChange={() => setInvoiceType('corporate')} className="accent-amber-600" />
                          <span>Tüzel / Kurumsal Fatura (VKN)</span>
                        </label>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      {invoiceType === 'individual' ? (
                        <div><label className="font-bold block mb-1">TC Kimlik No:</label><input type="text" value={tcNo} onChange={e => setTcNo(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5" /></div>
                      ) : (
                        <div><label className="font-bold block mb-1">Vergi Kimlik No (VKN):</label><input type="text" value={vknNo} onChange={e => setVknNo(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5" /></div>
                      )}
                      <div><label className="font-bold block mb-1">Vergi Dairesi:</label><input type="text" value={taxOffice} onChange={e => setTaxOffice(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5" /></div>
                    </div>

                    <div>
                      <label className="font-bold block mb-1">Fatura Adresi:</label>
                      <textarea value={invoiceAddress} onChange={e => setInvoiceAddress(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 h-16" />
                    </div>
                  </div>
                )}
              </div>

              {/* SECTION 6: ETKİNLİK AKIŞ PLANLAMA (DOKUNMATİK & SÜRÜKLE LE BIRAK) */}
              <div className="glass-panel p-4 sm:p-6 rounded-3xl space-y-4 shadow-sm border border-slate-200 dark:border-brand-border">
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center border-b border-slate-200 dark:border-brand-border pb-3 gap-2">
                  <div className="flex items-center space-x-2">
                    <span className="text-lg">⏱️</span>
                    <div>
                      <h3 className="font-bold text-base text-slate-800 dark:text-gray-100">6. Organizasyon & Etkinlik Akış Planlaması</h3>
                      <p className="text-[11px] text-amber-700 dark:text-gold-400 font-medium">💡 Masaüstünde (⋮⋮) simgesiyle sürükleyebilir veya mobilde (▲/▼) oklarıyla sırasını değiştirebilirsiniz.</p>
                    </div>
                  </div>
                  <button onClick={handleAddFlowItem} className="w-full sm:w-auto px-3 py-1.5 bg-amber-500/10 hover:bg-amber-500/20 text-amber-800 dark:text-gold-400 font-bold rounded-xl text-xs border border-amber-500/30 text-center">➕ Akış Adımı Ekle</button>
                </div>

                <div className="space-y-2 text-xs">
                  {flowPlan.map((item, idx) => (
                    <div
                      key={idx}
                      draggable={true}
                      onDragStart={(e) => handleDragStart(e, idx)}
                      onDragOver={(e) => handleDragOver(e, idx)}
                      onDrop={(e) => handleDrop(e, idx)}
                      onDragEnd={handleDragEnd}
                      className={`flex items-center space-x-2 sm:space-x-3 p-2 sm:p-2.5 rounded-xl border transition-all cursor-move ${
                        draggedIdx === idx
                          ? 'opacity-40 bg-amber-500/20 border-amber-500 scale-95'
                          : dragOverIdx === idx
                          ? 'bg-amber-500/20 border-amber-500 border-2 scale-[1.02] shadow-md'
                          : 'bg-slate-50 dark:bg-brand-dark border-slate-200 dark:border-brand-border hover:border-amber-500/50'
                      }`}
                    >
                      <div className="hidden sm:flex items-center cursor-grab active:cursor-grabbing text-slate-400 hover:text-amber-600 font-bold px-1 text-sm select-none" title="Masaüstünde Sürükle ve Sıralamayı Değiştir">
                        ⋮⋮
                      </div>

                      {/* Touch & Mobile Up/Down Move Buttons */}
                      <div className="flex flex-col space-y-0.5 shrink-0">
                        <button
                          type="button"
                          onClick={() => moveFlowItemUp(idx)}
                          disabled={idx === 0}
                          className="w-5 h-4 flex items-center justify-center bg-slate-200 dark:bg-brand-card text-slate-700 dark:text-gray-300 rounded text-[9px] font-bold disabled:opacity-20 hover:bg-amber-500 hover:text-white"
                          title="Yukarı Taşı"
                        >
                          ▲
                        </button>
                        <button
                          type="button"
                          onClick={() => moveFlowItemDown(idx)}
                          disabled={idx === flowPlan.length - 1}
                          className="w-5 h-4 flex items-center justify-center bg-slate-200 dark:bg-brand-card text-slate-700 dark:text-gray-300 rounded text-[9px] font-bold disabled:opacity-20 hover:bg-amber-500 hover:text-white"
                          title="Aşağı Taşı"
                        >
                          ▼
                        </button>
                      </div>

                      <input
                        type="text"
                        value={item.time}
                        onChange={e => {
                          const val = e.target.value;
                          setFlowPlan(prev => prev.map((x, i) => i === idx ? { ...x, time: val } : x));
                        }}
                        className="w-16 sm:w-20 bg-white dark:bg-brand-card border border-slate-200 rounded-lg p-1.5 font-mono font-bold text-center text-slate-800 dark:text-gray-200 text-xs shrink-0"
                      />
                      <input
                        type="text"
                        value={item.title}
                        onChange={e => {
                          const val = e.target.value;
                          setFlowPlan(prev => prev.map((x, i) => i === idx ? { ...x, title: val } : x));
                        }}
                        className="flex-1 bg-white dark:bg-brand-card border border-slate-200 rounded-lg p-1.5 font-bold text-slate-800 dark:text-gray-200 text-xs min-w-0"
                      />
                      <button onClick={() => handleRemoveFlowItem(idx)} className="text-red-500 hover:text-red-700 font-bold px-1.5 text-sm shrink-0" title="Adımı Sil">✕</button>
                    </div>
                  ))}
                </div>
              </div>

              {/* SECTION 7: OPERASYONEL EK NOTLAR */}
              <div className="glass-panel p-6 rounded-3xl space-y-3 shadow-sm border border-slate-200 dark:border-brand-border text-xs">
                <label className="font-bold text-slate-800 dark:text-gray-100 block">7. Operasyonel Ek Notlar & Özel İstekler:</label>
                <textarea value={notes} onChange={e => setNotes(e.target.value)} placeholder="Gelin odası ikramları, çiçek renk tercihleri, özel teknik ekipman talepleri..." className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-3 h-20" />
              </div>

            </div>

            {/* RIGHT COLUMN: LIVE INTERACTIVE PREVIEW & SUMMARY CARD (4 Cols) */}
            <div className="lg:col-span-4 space-y-6">
              
              {/* TAKVİM ÖN İZLEME KARTI */}
              <div className="glass-panel p-5 rounded-3xl space-y-3 shadow-sm border border-amber-500/30">
                <div className="flex justify-between items-center border-b border-slate-200 pb-2">
                  <span className="font-bold text-xs text-amber-700 dark:text-gold-400">📅 Takvim Canlı Ön İzlemesi</span>
                  <span className="text-[10px] bg-amber-500/10 text-amber-800 font-bold px-2 py-0.5 rounded">{eventDate}</span>
                </div>
                
                <div className="bg-slate-50 dark:bg-brand-dark p-3 rounded-2xl border text-center space-y-2 text-xs">
                  <div className="font-bold text-slate-800 dark:text-gray-100">{formatDate(eventDate)}</div>
                  <div className="text-amber-700 dark:text-gold-400 font-bold">{selectedVenue?.name}</div>
                  <div className="text-[11px] font-mono text-slate-600 bg-white dark:bg-brand-card py-1 px-2 rounded-lg border">{activeSlot}</div>
                  {collisionDetected ? (
                    <div className="bg-red-500/10 text-red-600 font-bold p-2 rounded-lg text-[10px]">⚠️ BU SAAT DİLİMİ DOLUDUR</div>
                  ) : (
                    <div className="bg-emerald-500/10 text-emerald-600 font-bold p-2 rounded-lg text-[10px]">✅ BU SAAT DİLİMİ MÜSAİTTİR</div>
                  )}
                </div>
              </div>

              {/* CANLI FİNANSAL ÖZET & SÖZLEŞME ONAY KARTI */}
              <div className="glass-panel p-6 rounded-3xl space-y-4 shadow-xl border-2 border-amber-500/40 sticky top-24">
                <h3 className="font-bold text-base text-slate-800 dark:text-gray-100 border-b border-slate-200 pb-2">
                  💰 Canlı Hesaplama & Sözleşme Kartı
                </h3>

                <div className="space-y-2 text-xs">
                  <div className="flex justify-between"><span>Salon Bedeli:</span><span className="font-bold">{formatCurrency(calculations.vPrice)}</span></div>
                  <div className="flex justify-between"><span>Seçilen Hizmetler:</span><span className="font-bold">{formatCurrency(calculations.servTotal)}</span></div>
                  <div className="flex justify-between border-t border-slate-200 pt-1"><span>Ara Toplam:</span><span className="font-bold">{formatCurrency(calculations.sub)}</span></div>
                  {calculations.disc > 0 && <div className="flex justify-between text-red-500"><span>Referans İndirimi:</span><span className="font-bold">-{formatCurrency(calculations.disc)}</span></div>}
                  {isInvoiced && <div className="flex justify-between text-slate-600"><span>Hesaplanan KDV (%20):</span><span className="font-bold">{formatCurrency(calculations.vat)}</span></div>}
                  
                  <div className="flex justify-between text-base font-bold text-amber-700 dark:text-gold-400 border-t border-slate-200 pt-2">
                    <span>Genel Toplam Tutar:</span>
                    <span>{formatCurrency(calculations.grandTotal)}</span>
                  </div>

                  <div className="flex justify-between text-emerald-600 pt-1"><span>Tahsil Edilen Kapora:</span><span className="font-bold">{formatCurrency(calculations.dep)}</span></div>
                  <div className="flex justify-between text-red-600 font-bold text-sm bg-red-500/10 p-2 rounded-xl border border-red-500/20">
                    <span>Kalan Ödenecek Bakiye:</span>
                    <span>{formatCurrency(calculations.remaining)}</span>
                  </div>
                </div>

                <div className="pt-2">
                  <button
                    disabled={collisionDetected}
                    onClick={handleSubmit}
                    className={`w-full gold-button font-bold py-3.5 rounded-2xl text-xs shadow-xl flex items-center justify-center space-x-2 ${
                      collisionDetected ? 'opacity-50 cursor-not-allowed' : 'hover:scale-[1.02]'
                    }`}
                  >
                    <span>🎉</span><span>Rezervasyonu ve Sözleşmeyi Kaydet</span>
                  </button>
                </div>

              </div>

            </div>

          </div>
        </div>
      );
    }

    // --- CUSTOMER FORM MODAL ---
    function CustomerFormModal({ customer, onClose, onSave }) {
      const [name, setName] = useState(customer?.name || '');
      const [email, setEmail] = useState(customer?.email || '');
      const [phone, setPhone] = useState(customer?.phone || '');
      const [address, setAddress] = useState(customer?.address || '');
      const [taxType, setTaxType] = useState(customer?.taxType || 'individual');
      const [tcNo, setTcNo] = useState(customer?.tcNo || '');
      const [taxOffice, setTaxOffice] = useState(customer?.taxOffice || '');

      return (
        <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-md flex items-center justify-center p-4" role="dialog" aria-modal="true">
          <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-md w-full p-6 space-y-4 shadow-2xl">
            <h3 className="text-lg font-bold text-slate-800 dark:text-gray-100">{customer ? 'Müşteri Kartı Düzenle' : 'Yeni Müşteri Ekle'}</h3>
            <div className="space-y-3 text-xs">
              <input type="text" placeholder="Müşteri / Firma Adı" value={name} onChange={e => setName(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200" />
              <div className="grid grid-cols-2 gap-2">
                <input type="text" placeholder="Telefon (+90 5...)" value={phone} onChange={e => setPhone(e.target.value)} className="bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200" />
                <input type="email" placeholder="E-posta" value={email} onChange={e => setEmail(e.target.value)} className="bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200" />
              </div>
              <select value={taxType} onChange={e => setTaxType(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold">
                <option value="individual">Bireysel Müşteri (TC No)</option>
                <option value="corporate">Kurumsal Müşteri (VKN)</option>
              </select>
              <div className="grid grid-cols-2 gap-2">
                <input type="text" placeholder={taxType === 'individual' ? 'TC Kimlik No' : 'Vergi Kimlik No (VKN)'} value={tcNo} onChange={e => setTcNo(e.target.value)} className="bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200" />
                <input type="text" placeholder="Vergi Dairesi" value={taxOffice} onChange={e => setTaxOffice(e.target.value)} className="bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200" />
              </div>
              <textarea placeholder="Adres Bilgisi" value={address} onChange={e => setAddress(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 h-16" />
            </div>
            <div className="flex justify-end space-x-2 pt-2 border-t border-slate-200 dark:border-brand-border">
              <button onClick={onClose} className="px-4 py-2 bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-400 rounded-xl text-xs font-bold">İptal</button>
              <button onClick={() => onSave({ ...customer, name, email, phone, address, taxType, tcNo, taxOffice })} className="gold-button font-bold px-5 py-2 rounded-xl text-xs">Müşteriyi Kaydet</button>
            </div>
          </div>
        </div>
      );
    }

    // --- DASHBOARD COMPONENT ---
    function DashboardComponent({ activeRole, venues, reservations, financialStats, onNewResClick, onTabChange }) {
      return (
        <div className="space-y-6">
          <div className="glass-panel p-6 rounded-3xl border border-amber-500/30 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-sm">
            <div>
              <span className="bg-amber-500/10 text-amber-800 dark:text-gold-400 text-xs font-bold px-3 py-1 rounded-full border border-amber-500/20">
                {activeRole === 'admin' && '👑 Admin Kurumsal Yönetim Paneli'}
                {activeRole === 'satisci' && '💼 Satış & Doluluk Ekranı'}
                {activeRole === 'sosyal_medyaci' && '📸 Medya Yükleme Paneli'}
                {activeRole === 'musteri' && '💖 Özel Müşteri Portalı'}
              </span>
              <h2 className="text-2xl font-heading font-extrabold text-slate-800 dark:text-gray-100 mt-2">
                Hoş Geldiniz, İrem Hanım ✨
              </h2>
              <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">İrem Düğün Sarayı güncel rezervasyon durumu ve organizasyon hareketleri.</p>
            </div>

            {(activeRole === 'admin' || activeRole === 'satisci') && (
              <button onClick={onNewResClick} className="gold-button font-bold px-6 py-3 rounded-2xl shadow-lg flex items-center space-x-2 text-xs">
                <span>➕</span><span>Tam Sayfa Yeni Rezervasyon Çalışma Alanı</span>
              </button>
            )}
          </div>

          {activeRole === 'admin' && (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="glass-panel p-5 rounded-2xl border border-slate-200 dark:border-brand-border/40 shadow-sm"><div className="text-xs text-slate-500 dark:text-gray-400">Toplam Düğün Salonu</div><div className="text-2xl font-bold text-slate-800 dark:text-gray-100 mt-1">{venues.length}</div></div>
              <div className="glass-panel p-5 rounded-2xl border border-amber-500/40 shadow-sm"><div className="text-xs text-slate-500 dark:text-gray-400">Bu Ayın Boş Günleri</div><div className="text-2xl font-bold gold-gradient-text mt-1">12 Gün</div></div>
              <div className="glass-panel p-5 rounded-2xl border border-slate-200 dark:border-brand-border/40 shadow-sm"><div className="text-xs text-slate-500 dark:text-gray-400">Son Ay Toplam Kazanç</div><div className="text-2xl font-bold text-slate-800 dark:text-gray-100 mt-1">{formatCurrency(financialStats.totalRev)}</div></div>
              <div className="glass-panel p-5 rounded-2xl border border-red-500/40 shadow-sm"><div className="text-xs text-slate-500 dark:text-gray-400">Bekleyen Ödemeler</div><div className="text-2xl font-bold text-red-500 dark:text-red-400 mt-1">{formatCurrency(financialStats.totalPending)}</div></div>
            </div>
          )}

          {activeRole === 'satisci' && (
            <div className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div className="glass-panel p-5 rounded-2xl"><div className="text-xs text-slate-500 dark:text-gray-400">Salon Sayısı</div><div className="text-2xl font-bold text-slate-800 dark:text-gray-100">{venues.length}</div></div>
                <div className="glass-panel p-5 rounded-2xl border border-amber-500/40"><div className="text-xs text-slate-500 dark:text-gray-400">Ayın Boş Günleri</div><div className="text-2xl font-bold gold-gradient-text">12 Gün</div></div>
                <div className="glass-panel p-5 rounded-2xl border border-emerald-500/40"><div className="text-xs text-slate-500 dark:text-gray-400">Kapora Alınanlar</div><div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400">{reservations.filter(r => r.depositPaid > 0).length}</div></div>
              </div>
            </div>
          )}

        </div>
      );
    }

    // --- VENUES COMPONENT ---
    function VenuesComponent({ venues }) {
      return (
        <div className="space-y-6">
          <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Düğün Salonlarım</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {venues.map(v => (
              <div key={v.id} className="glass-panel rounded-3xl border border-slate-200 dark:border-brand-border/40 overflow-hidden space-y-3 shadow-sm">
                <img src={v.images[0]} alt={`${v.name} Görseli`} className="w-full h-44 object-cover" />
                <div className="p-4 space-y-2">
                  <div className="flex justify-between items-center">
                    <h3 className="font-bold text-base text-slate-800 dark:text-gray-100">{v.name}</h3>
                    <span className="text-[10px] text-amber-700 dark:text-gold-400 font-bold bg-amber-500/10 px-2 py-0.5 rounded-full">{v.category}</span>
                  </div>
                  <p className="text-xs text-slate-500 dark:text-gray-400">{v.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      );
    }

    // --- SERVICES COMPONENT ---
    function ServicesComponent({ services }) {
      return (
        <div className="space-y-6">
          <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Ek Hizmetlerim</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {services.map(s => (
              <div key={s.id} className="glass-panel p-4 rounded-2xl space-y-3 shadow-sm">
                <img src={s.image} alt={`${s.name} Görseli`} className="w-full h-32 object-cover rounded-xl border border-slate-200 dark:border-brand-border" />
                <h3 className="font-bold text-sm text-slate-800 dark:text-gray-100">{s.name}</h3>
                <p className="text-xs text-slate-500 dark:text-gray-400">{s.description}</p>
              </div>
            ))}
          </div>
        </div>
      );
    }

    // --- RESERVATIONS COMPONENT ---
    function ReservationsComponent({ reservations, venues, searchQuery, setSearchQuery, statusFilter, setStatusFilter, onNewResClick, onDetailClick }) {
      return (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Tüm Rezervasyonlar</h2>
            <button onClick={onNewResClick} className="gold-button font-bold px-4 py-2 rounded-xl text-xs">📝 Tam Sayfa Yeni Rezervasyon</button>
          </div>

          <div className="glass-panel p-4 rounded-2xl flex gap-3 shadow-sm">
            <input
              type="text"
              placeholder="Rezervasyon kodu veya müşteri..."
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              className="bg-white dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl px-3 py-2 text-xs text-slate-800 dark:text-gray-200 focus:outline-none focus:border-amber-500 flex-1"
            />
          </div>

          <div className="glass-panel rounded-2xl overflow-hidden border border-slate-200 dark:border-brand-border/40 shadow-sm">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-100 dark:bg-brand-card text-slate-600 dark:text-gray-400 uppercase border-b border-slate-200 dark:border-brand-border">
                <tr>
                  <th scope="col" className="p-3">Kod</th>
                  <th scope="col" className="p-3">Müşteri</th>
                  <th scope="col" className="p-3">Tarih</th>
                  <th scope="col" className="p-3">Toplam Tutar</th>
                  <th scope="col" className="p-3">Durum</th>
                  <th scope="col" className="p-3 text-right">İşlem</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 dark:divide-brand-border/30">
                {reservations.map(r => (
                  <tr key={r.id} className="hover:bg-slate-50 dark:hover:bg-brand-card/50">
                    <td className="p-3 font-mono font-bold text-amber-700 dark:text-gold-400">{r.id}</td>
                    <td className="p-3 font-medium text-slate-800 dark:text-gray-200">{r.customerName}</td>
                    <td className="p-3 text-slate-600 dark:text-gray-300">{formatDate(r.date)}</td>
                    <td className="p-3 font-bold text-slate-800 dark:text-gray-100">{formatCurrency(r.totalAmount)}</td>
                    <td className="p-3"><span className="bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 px-2 py-0.5 rounded text-[10px] font-bold border border-emerald-500/20">{r.paymentStatus}</span></td>
                    <td className="p-3 text-right"><button onClick={() => onDetailClick(r)} className="px-3 py-1 rounded bg-amber-500/10 text-amber-700 dark:text-gold-400 font-bold text-[10px] border border-amber-500/30">Detay 🔍</button></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      );
    }

    // --- CALENDAR COMPONENT ---
    function CalendarComponent({ reservations, venues, onResClick }) {
      return (
        <div className="space-y-6">
          <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">İnteraktif Takvim</h2>
          <div className="glass-panel p-6 rounded-3xl space-y-4 shadow-sm">
            <h3 className="font-bold text-amber-700 dark:text-gold-400">📅 Ağustos 2026</h3>
            <div className="grid grid-cols-7 gap-2 text-center text-xs">
              {['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'].map(d => <div key={d} className="font-bold text-slate-500 dark:text-gray-400 p-2 bg-slate-100 dark:bg-brand-card rounded">{d}</div>)}
              {Array.from({ length: 31 }, (_, i) => i + 1).map(day => {
                const dateStr = `2026-08-${day < 10 ? '0' + day : day}`;
                const dayRes = reservations.filter(r => r.date === dateStr);
                return (
                  <div key={day} className={`min-h-[70px] p-2 rounded-xl border text-left flex flex-col justify-between ${dayRes.length > 0 ? 'bg-amber-50 dark:bg-brand-card border-amber-500/40' : 'bg-white dark:bg-brand-dark/40 border-slate-200 dark:border-brand-border/30'}`}>
                    <span className="font-bold text-xs text-slate-700 dark:text-gray-300">{day}</span>
                    {dayRes.map(r => (
                      <button key={r.id} onClick={() => onResClick(r)} className="bg-amber-500/20 text-amber-900 dark:text-gold-300 p-1 rounded text-[9px] font-bold truncate border border-amber-500/30">
                        {r.customerName.split(' ')[0]}
                      </button>
                    ))}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      );
    }

    // --- CAMPAIGNS COMPONENT ---
    function CampaignsComponent({ campaigns }) {
      return (
        <div className="space-y-6">
          <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Aktif Kampanyalar</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {campaigns.map(c => (
              <div key={c.id} className="glass-panel p-5 rounded-2xl space-y-2 border border-amber-500/30 shadow-sm">
                <span className="bg-amber-500/10 text-amber-800 dark:text-gold-400 font-mono font-bold text-xs px-2.5 py-0.5 rounded-full border border-amber-500/20">{c.code}</span>
                <h3 className="font-bold text-base text-slate-800 dark:text-gray-100">{c.title}</h3>
                <p className="text-xs text-slate-500 dark:text-gray-400">{c.description}</p>
              </div>
            ))}
          </div>
        </div>
      );
    }

    // --- FINANCE COMPONENT ---
    function FinanceComponent({ financialStats, reservations }) {
      return (
        <div className="space-y-6">
          <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Finans Yönetimi</h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="glass-panel p-5 rounded-2xl shadow-sm"><div className="text-xs text-slate-500 dark:text-gray-400">Toplam Ciro</div><div className="text-2xl font-bold text-slate-800 dark:text-gray-100 mt-1">{formatCurrency(financialStats.totalRev)}</div></div>
            <div className="glass-panel p-5 rounded-2xl shadow-sm"><div className="text-xs text-slate-500 dark:text-gray-400">Tahsil Edilen Kapora</div><div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1">{formatCurrency(financialStats.totalDeposit)}</div></div>
            <div className="glass-panel p-5 rounded-2xl shadow-sm"><div className="text-xs text-slate-500 dark:text-gray-400">Kalan Bekleyen Bakiye</div><div className="text-2xl font-bold text-red-500 dark:text-red-400 mt-1">{formatCurrency(financialStats.totalPending)}</div></div>
          </div>
        </div>
      );
    }

    // --- CUSTOMERS COMPONENT ---
    function CustomersComponent({ customers, onAddClick, onEditClick }) {
      return (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Müşteri Rehberi</h2>
            <button onClick={onAddClick} className="gold-button font-bold px-4 py-2 rounded-xl text-xs">👤 Yeni Müşteri Ekle</button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {customers.map(c => (
              <div key={c.id} className="glass-panel p-5 rounded-2xl flex items-start space-x-4 shadow-sm">
                <img src={c.avatar} alt={`${c.name} Avatarı`} className="w-14 h-14 rounded-2xl object-cover border border-amber-500/40" />
                <div className="flex-1 space-y-2">
                  <div className="flex justify-between items-start">
                    <h3 className="font-bold text-sm text-slate-800 dark:text-gray-100">{c.name}</h3>
                    <button onClick={() => onEditClick(c)} className="text-[10px] text-amber-700 font-bold bg-amber-500/10 px-2 py-0.5 rounded">Düzenle ✏️</button>
                  </div>
                  <div className="text-xs text-slate-500 dark:text-gray-400">{c.phone} | {c.email}</div>
                  <div className="text-[11px] text-slate-600 dark:text-gray-400">{c.taxType === 'corporate' ? `Kurumsal VKN: ${c.vknNo || c.tcNo || '-'}` : `Bireysel TC: ${c.tcNo || '-'}`} ({c.taxOffice || 'Sapanca VD'})</div>
                  <a href={generateWhatsAppLink(c.phone, c.name)} target="_blank" rel="noopener noreferrer" className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-3 py-1.5 rounded-lg text-xs inline-flex items-center space-x-1 shadow">
                    <span>💬 WhatsApp İle Mesaj At</span>
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      );
    }

    // --- USERS COMPONENT ---
    function UsersComponent({ users }) {
      return (
        <div className="space-y-6">
          <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Kullanıcı Yönetimi</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {users.map(u => (
              <div key={u.id} className="glass-panel p-5 rounded-2xl text-center space-y-3 shadow-sm">
                <img src={u.avatar} alt={`${u.name} Profil Resmi`} className="w-16 h-16 rounded-full mx-auto object-cover border-2 border-amber-500/50" />
                <div>
                  <h3 className="font-bold text-sm text-slate-800 dark:text-gray-100">{u.name}</h3>
                  <div className="text-xs text-slate-500 dark:text-gray-400 truncate">{u.email}</div>
                </div>
                <span className="bg-amber-500/10 text-amber-800 dark:text-gold-400 text-[10px] font-bold px-2.5 py-0.5 rounded-full uppercase border border-amber-500/20">{u.role}</span>
              </div>
            ))}
          </div>
        </div>
      );
    }

    // --- REPORTS COMPONENT ---
    function ReportsComponent({ reservations, aiRecommendations }) {
      return (
        <div className="space-y-6">
          <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Yapay Zeka Önerileri & Raporlar</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {aiRecommendations.map(rec => (
              <div key={rec.id} className="glass-panel p-6 rounded-3xl space-y-3 border border-amber-500/40 shadow-sm">
                <span className="bg-amber-500/10 text-amber-800 dark:text-gold-400 text-xs font-bold px-3 py-1 rounded-full">✨ AI Öneri</span>
                <h3 className="font-bold text-lg text-slate-800 dark:text-gray-100">{rec.title}</h3>
                <p className="text-xs text-slate-600 dark:text-gray-300">{rec.description}</p>
                <button className="gold-button font-bold px-4 py-2 rounded-xl text-xs">{rec.actionText}</button>
              </div>
            ))}
          </div>
        </div>
      );
    }

    // --- MEDIA COMPONENT ---
    function MediaComponent({ reservations, showToast }) {
      return (
        <div className="space-y-6 max-w-xl mx-auto text-center">
          <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Medya & Foto Yükleme</h2>
          <div className="glass-panel p-8 rounded-3xl space-y-4 shadow-sm">
            <div className="text-4xl" aria-hidden="true">📤</div>
            <p className="text-xs text-slate-600 dark:text-gray-300">Rezervasyon fotoğraf ve video galerisini güncellemek için dosya yükleyin.</p>
            <button onClick={() => showToast('📸 Örnek Medya Galerisi Güncellendi!')} className="gold-button font-bold px-6 py-2.5 rounded-xl text-xs">
              Fotoğraf Yükle
            </button>
          </div>
        </div>
      );
    }

    // --- RESERVATION DETAIL MODAL ---
    function ReservationDetailModal({ res, venues, services, onClose, onPrintInvoice, onUpdatePayment }) {
      const venue = venues.find(v => v.id === res.venueId);
      const [deposit, setDeposit] = useState(res.depositPaid);
      const [status, setStatus] = useState(res.paymentStatus);

      return (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-md flex items-center justify-center p-4" role="dialog" aria-modal="true" aria-labelledby="modal-title">
          <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-xl w-full p-6 space-y-4 max-h-[90vh] overflow-y-auto shadow-2xl">
            <div className="flex justify-between items-center border-b border-slate-200 dark:border-brand-border pb-3">
              <div>
                <span className="font-mono text-amber-700 dark:text-gold-400 font-bold text-xs">{res.id}</span>
                <h3 id="modal-title" className="text-lg font-bold text-slate-800 dark:text-gray-100">{res.customerName}</h3>
              </div>
              <button onClick={onClose} className="text-slate-400 hover:text-slate-600 dark:hover:text-white" aria-label="Modalı Kapat">✕</button>
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="bg-slate-50 dark:bg-brand-dark p-3 rounded-xl border border-slate-200 dark:border-brand-border"><div>Salon</div><div className="font-bold text-slate-800 dark:text-gray-200">{venue?.name || '-'}</div></div>
              <div className="bg-slate-50 dark:bg-brand-dark p-3 rounded-xl border border-slate-200 dark:border-brand-border"><div>Tarih</div><div className="font-bold text-slate-800 dark:text-gray-200">{formatDate(res.date)} ({res.timeSlot})</div></div>
              <div className="bg-slate-50 dark:bg-brand-dark p-3 rounded-xl border border-slate-200 dark:border-brand-border"><div>Toplam Tutar</div><div className="font-bold text-amber-700 dark:text-gold-400">{formatCurrency(res.totalAmount)}</div></div>
              <div className="bg-slate-50 dark:bg-brand-dark p-3 rounded-xl border border-slate-200 dark:border-brand-border"><div>Kalan Bakiye</div><div className="font-bold text-red-500 dark:text-red-400">{formatCurrency(Math.max(0, res.totalAmount - deposit))}</div></div>
            </div>

            <div className="bg-slate-50 dark:bg-brand-dark/70 p-4 rounded-xl border border-amber-500/30 space-y-3">
              <h4 className="font-bold text-xs text-amber-700 dark:text-gold-400">💳 Ödeme ve Kapora Güncelleme</h4>
              <div className="grid grid-cols-2 gap-3 text-xs">
                <div>
                  <label htmlFor="deposit-input" className="text-slate-500 dark:text-gray-400 block mb-1">Tahsil Edilen Kapora (TL):</label>
                  <input id="deposit-input" type="number" value={deposit} onChange={e => setDeposit(Number(e.target.value))} className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-lg p-2 text-slate-800 dark:text-gray-200 font-bold" />
                </div>
                <div>
                  <label htmlFor="status-select" className="text-slate-500 dark:text-gray-400 block mb-1">Ödeme Statüsü:</label>
                  <select id="status-select" value={status} onChange={e => setStatus(e.target.value)} className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-lg p-2 text-slate-800 dark:text-gray-200 font-bold">
                    <option value="Bekliyor">Bekliyor</option>
                    <option value="Kapora Alındı">Kapora Alındı</option>
                    <option value="Ödendi">Ödendi</option>
                    <option value="Tamamlandı">Tamamlandı</option>
                  </select>
                </div>
              </div>
            </div>

            <div className="flex justify-between items-center pt-2 border-t border-slate-200 dark:border-brand-border">
              <button onClick={onPrintInvoice} className="bg-slate-800 hover:bg-slate-900 text-white font-bold px-4 py-2 rounded-xl text-xs inline-flex items-center space-x-1 shadow">
                <span>📄</span><span>Resmi Sözleşme & Fatura Yazdır</span>
              </button>

              <div className="flex space-x-2">
                <button onClick={onClose} className="px-4 py-2 bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-400 rounded-xl text-xs font-bold">Kapat</button>
                <button onClick={() => onUpdatePayment(res.id, deposit, status)} className="gold-button font-bold px-5 py-2 rounded-xl text-xs">Ödemeyi Güncelle</button>
              </div>
            </div>
          </div>
        </div>
      );
    }

    // --- UNAUTHORIZED ACCESS (403) SCREEN ---
    function UnauthorizedAccessScreen({ pageTitle, activeRoleName, onGoHome }) {
      return (
        <div className="glass-panel p-8 max-w-lg mx-auto mt-12 rounded-3xl text-center space-y-4 border border-red-500/40 shadow-2xl">
          <div className="text-5xl" aria-hidden="true">🚫</div>
          <span className="bg-red-500/10 text-red-600 dark:text-red-400 text-xs font-bold px-3 py-1 rounded-full border border-red-500/20">
            Hata 403 / Yetkisiz Erişim Uyarısı
          </span>
          <h2 className="text-xl font-bold text-slate-800 dark:text-gray-100">
            "{pageTitle}" Sayfasına Erişim Yetkiniz Bulunmamaktadır
          </h2>
          <p className="text-xs text-slate-500 dark:text-gray-400">
            Mevcut kullanıcınızın yetki rolü: <strong className="text-amber-700 dark:text-gold-400">{activeRoleName}</strong>.<br />
            Bu sayfa güvenlik ve veri mahremiyeti nedeniyle bu rolün erişimine kısıtlanmıştır.
          </p>
          <div className="pt-2">
            <button onClick={onGoHome} className="gold-button font-bold px-6 py-2.5 rounded-xl text-xs shadow-lg">
              🏠 Güvenli Anasayfaya Dön
            </button>
          </div>
        </div>
      );
    }

    // Render React Root
    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(<App />);
  