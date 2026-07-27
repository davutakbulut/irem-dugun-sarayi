// İrem Düğün Sarayı & Organizasyon Yönetim Platformu - Main SPA Application Component

const { useState, useEffect, useMemo } = React;

// Import Mock Data & Helpers
import {
  INITIAL_VENUES,
  INITIAL_SERVICES,
  INITIAL_CAMPAIGNS,
  INITIAL_CUSTOMERS,
  INITIAL_RESERVATIONS,
  INITIAL_USERS,
  AI_RECOMMENDATIONS
} from './data/mockData.js';

import {
  formatCurrency,
  formatDate,
  checkBookingCollision,
  generateWhatsAppLink,
  generateWelcomeEmailHTML,
  generateReservationEmailHTML
} from './utils/helpers.js';

export default function App() {
  // --- Persistent State ---
  const [venues, setVenues] = useState(() => {
    const saved = localStorage.getItem('irem_venues');
    return saved ? JSON.parse(saved) : INITIAL_VENUES;
  });

  const [services, setServices] = useState(() => {
    const saved = localStorage.getItem('irem_services');
    return saved ? JSON.parse(saved) : INITIAL_SERVICES;
  });

  const [campaigns, setCampaigns] = useState(() => {
    const saved = localStorage.getItem('irem_campaigns');
    return saved ? JSON.parse(saved) : INITIAL_CAMPAIGNS;
  });

  const [customers, setCustomers] = useState(() => {
    const saved = localStorage.getItem('irem_customers');
    return saved ? JSON.parse(saved) : INITIAL_CUSTOMERS;
  });

  const [reservations, setReservations] = useState(() => {
    const saved = localStorage.getItem('irem_reservations');
    return saved ? JSON.parse(saved) : INITIAL_RESERVATIONS;
  });

  const [users, setUsers] = useState(() => {
    const saved = localStorage.getItem('irem_users');
    return saved ? JSON.parse(saved) : INITIAL_USERS;
  });

  // --- Active Role & Navigation State ---
  const [activeRole, setActiveRole] = useState('admin'); // admin, satisci, sosyal_medyaci, musteri
  const [activeTab, setActiveTab] = useState('dashboard'); // dashboard, venues, services, reservations, calendar, campaigns, finance, customers, users, reports, media
  const [themeMode, setThemeMode] = useState('dark'); // dark or light

  // --- UI Toast & Modal States ---
  const [toast, setToast] = useState(null);
  const [emailModalData, setEmailModalData] = useState(null); // { subject, htmlContent }
  const [newResModalOpen, setNewResModalOpen] = useState(false);
  const [selectedResForDetail, setSelectedResForDetail] = useState(null);
  const [selectedResForMedia, setSelectedResForMedia] = useState(null);

  // --- Search & Filter States ---
  const [resSearchQuery, setResSearchQuery] = useState('');
  const [resStatusFilter, setResStatusFilter] = useState('all');
  const [resVenueFilter, setResVenueFilter] = useState('all');

  // --- New Reservation Wizard Form State ---
  const [resForm, setResForm] = useState({
    venueId: 'v1',
    date: new Date().toISOString().split('T')[0],
    timeSlot: '19:00-23:00',
    guestCount: 400,
    selectedServices: [], // array of { serviceId, quantity }
    customerName: '',
    customerEmail: '',
    customerPhone: '',
    customerAddress: '',
    taxType: 'individual',
    tcNo: '',
    vknNo: '',
    taxOffice: '',
    campaignCode: '',
    depositPaid: 20000,
    notes: '',
    flowPlan: [
      { time: '19:00', title: 'Misafir Karşılama' },
      { time: '19:30', title: 'Gelin & Damat Giriş ve Dans' },
      { time: '20:30', title: 'Yemek İkramı' },
      { time: '21:30', title: 'Pasta Kesimi & Şov' },
      { time: '22:00', title: 'Eğlence ve Müzik' }
    ]
  });

  // Collision state
  const [collisionWarning, setCollisionWarning] = useState(null);

  // Save state changes to localStorage
  useEffect(() => { localStorage.setItem('irem_venues', JSON.stringify(venues)); }, [venues]);
  useEffect(() => { localStorage.setItem('irem_services', JSON.stringify(services)); }, [services]);
  useEffect(() => { localStorage.setItem('irem_campaigns', JSON.stringify(campaigns)); }, [campaigns]);
  useEffect(() => { localStorage.setItem('irem_customers', JSON.stringify(customers)); }, [customers]);
  useEffect(() => { localStorage.setItem('irem_reservations', JSON.stringify(reservations)); }, [reservations]);
  useEffect(() => { localStorage.setItem('irem_users', JSON.stringify(users)); }, [users]);

  // Check collision whenever reservation form date, venueId, or timeSlot changes
  useEffect(() => {
    const collision = checkBookingCollision(reservations, resForm.venueId, resForm.date, resForm.timeSlot);
    if (collision) {
      const venue = venues.find(v => v.id === resForm.venueId);
      setCollisionWarning(`⚠️ UYARI: ${venue?.name || 'Seçilen Salon'} için ${formatDate(resForm.date)} tarihinde ${resForm.timeSlot} saat diliminde (${collision.customerName}) adına çakışan rezervasyon bulunmaktadır! Lütfen farklı saat veya salon seçiniz.`);
    } else {
      setCollisionWarning(null);
    }
  }, [resForm.venueId, resForm.date, resForm.timeSlot, reservations, venues]);

  // Toast Helper
  const showToast = (msg, type = 'success') => {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 4000);
  };

  // Re-calculate totals for wizard form
  const resFormTotals = useMemo(() => {
    const venue = venues.find(v => v.id === resForm.venueId);
    const venuePrice = venue ? venue.price : 0;
    
    let servicesTotal = 0;
    resForm.selectedServices.forEach(item => {
      const srv = services.find(s => s.id === item.serviceId);
      if (srv) {
        const qty = srv.pricingType === 'per_person' ? resForm.guestCount : (item.quantity || 1);
        servicesTotal += srv.price * qty;
      }
    });

    const subtotal = venuePrice + servicesTotal;
    
    // Campaign calculation
    let discount = 0;
    if (resForm.campaignCode) {
      const camp = campaigns.find(c => c.code.toUpperCase() === resForm.campaignCode.toUpperCase() && c.active);
      if (camp) {
        if (camp.type === 'percentage') {
          discount = (subtotal * camp.value) / 100;
        } else if (camp.type === 'flat_discount') {
          discount = camp.value;
        } else if (camp.type === 'free_service') {
          const freeSrv = services.find(s => s.id === camp.serviceId);
          if (freeSrv) discount = freeSrv.price;
        }
      }
    }

    const afterDiscount = Math.max(0, subtotal - discount);
    const vat = afterDiscount * 0.20;
    const total = afterDiscount + vat;
    const remaining = Math.max(0, total - (Number(resForm.depositPaid) || 0));

    return { venuePrice, servicesTotal, subtotal, discount, vat, total, remaining };
  }, [resForm, venues, services, campaigns]);

  // Handle Creating New Reservation
  const handleSaveReservation = (e) => {
    e.preventDefault();
    if (collisionWarning) {
      showToast('Çakışan rezervasyon varken kayıt yapılamaz!', 'error');
      return;
    }
    if (!resForm.customerName || !resForm.customerEmail || !resForm.customerPhone) {
      showToast('Lütfen müşteri bilgilerini eksiksiz doldurunuz!', 'error');
      return;
    }

    // Check if customer exists, if not auto-register
    let existingCust = customers.find(c => c.email.toLowerCase() === resForm.customerEmail.toLowerCase());
    let generatedPassword = null;

    if (!existingCust) {
      generatedPassword = 'Irem' + Math.floor(1000 + Math.random() * 9000);
      const newCust = {
        id: 'cust-' + Date.now(),
        name: resForm.customerName,
        email: resForm.customerEmail,
        phone: resForm.customerPhone,
        address: resForm.customerAddress || 'Sapanca / Sakarya',
        taxType: resForm.taxType,
        tcNo: resForm.tcNo,
        vknNo: resForm.vknNo,
        taxOffice: resForm.taxOffice,
        followUp: true,
        followUpNote: 'Yeni otomatik üye oluşturuldu.',
        avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=200&q=80'
      };
      setCustomers(prev => [...prev, newCust]);
      existingCust = newCust;

      // Add to users list as musteri role
      setUsers(prev => [...prev, {
        id: 'u-' + Date.now(),
        name: resForm.customerName,
        email: resForm.customerEmail,
        role: 'musteri',
        avatar: newCust.avatar
      }]);

      // Show welcome email automation modal!
      const welcomeHTML = generateWelcomeEmailHTML(resForm.customerName, resForm.customerEmail, generatedPassword);
      setEmailModalData({
        subject: 'Erişiminiz Açıldı! – İrem Düğün Sarayı',
        htmlContent: welcomeHTML,
        recipient: resForm.customerEmail
      });
    }

    // Build reservation object
    const venue = venues.find(v => v.id === resForm.venueId);
    const newRes = {
      id: 'RES-2026-' + Math.floor(100 + Math.random() * 900),
      venueId: resForm.venueId,
      customerId: existingCust.id,
      customerName: resForm.customerName,
      customerEmail: resForm.customerEmail,
      customerPhone: resForm.customerPhone,
      date: resForm.date,
      timeSlot: resForm.timeSlot,
      guestCount: Number(resForm.guestCount),
      selectedServices: resForm.selectedServices.map(s => {
        const srv = services.find(srv => srv.id === s.serviceId);
        return {
          serviceId: s.serviceId,
          quantity: srv.pricingType === 'per_person' ? Number(resForm.guestCount) : (s.quantity || 1),
          unitPrice: srv ? srv.price : 0
        };
      }),
      venuePrice: resFormTotals.venuePrice,
      subtotal: resFormTotals.subtotal,
      campaignCode: resForm.campaignCode,
      discountAmount: resFormTotals.discount,
      vatAmount: resFormTotals.vat,
      totalAmount: resFormTotals.total,
      depositPaid: Number(resForm.depositPaid) || 0,
      remainingBalance: resFormTotals.remaining,
      paymentStatus: (Number(resForm.depositPaid) >= resFormTotals.total) ? 'Ödendi' : (Number(resForm.depositPaid) > 0 ? 'Kapora Alındı' : 'Bekliyor'),
      isInvoiced: true,
      invoiceType: resForm.taxType,
      tcNo: resForm.tcNo,
      vknNo: resForm.vknNo,
      taxOffice: resForm.taxOffice,
      notes: resForm.notes,
      flowPlan: resForm.flowPlan,
      mediaGallery: []
    };

    setReservations(prev => [newRes, ...prev]);
    setNewResModalOpen(false);
    showToast('🎉 Rezervasyon ve Otomatik Üyelik Başarıyla Oluşturuldu!');

    // Show reservation confirmation email after welcome email
    if (!generatedPassword) {
      const resHTML = generateReservationEmailHTML(newRes, venue?.name || '', newRes.selectedServices.map(s => {
        const srv = services.find(x => x.id === s.serviceId);
        return { name: srv?.name || '', quantity: s.quantity, total: s.unitPrice * s.quantity };
      }));
      setEmailModalData({
        subject: 'Rezervasyonunuz Oluşturuldu! – İrem Düğün Sarayı',
        htmlContent: resHTML,
        recipient: resForm.customerEmail
      });
    }
  };

  // Automated Status Check: If date passed & remaining balance == 0 -> set to "Tamamlandı"
  useEffect(() => {
    const today = new Date().toISOString().split('T')[0];
    setReservations(prev => prev.map(res => {
      if (res.date < today && res.remainingBalance === 0 && res.paymentStatus !== 'Tamamlandı') {
        return { ...res, paymentStatus: 'Tamamlandı' };
      }
      return res;
    }));
  }, []);

  // Filtered Reservations
  const filteredReservations = useMemo(() => {
    return reservations.filter(r => {
      const matchSearch = r.id.toLowerCase().includes(resSearchQuery.toLowerCase()) ||
                          r.customerName.toLowerCase().includes(resSearchQuery.toLowerCase()) ||
                          r.customerPhone.includes(resSearchQuery);
      const matchStatus = resStatusFilter === 'all' || r.paymentStatus === resStatusFilter;
      const matchVenue = resVenueFilter === 'all' || r.venueId === resVenueFilter;
      return matchSearch && matchStatus && matchVenue;
    });
  }, [reservations, resSearchQuery, resStatusFilter, resVenueFilter]);

  // Financial Stats Calculation (for Admin)
  const financialStats = useMemo(() => {
    const totalRev = reservations.reduce((acc, r) => acc + r.totalAmount, 0);
    const totalDeposit = reservations.reduce((acc, r) => acc + r.depositPaid, 0);
    const totalPending = reservations.reduce((acc, r) => acc + r.remainingBalance, 0);
    const totalVat = reservations.reduce((acc, r) => acc + r.vatAmount, 0);
    return { totalRev, totalDeposit, totalPending, totalVat };
  }, [reservations]);

  return (
    <div className={`min-h-screen ${themeMode === 'dark' ? 'bg-[#0b0f17] text-gray-100' : 'bg-gray-50 text-gray-900'} flex flex-col font-sans transition-colors duration-300`}>
      
      {/* --- HEADER --- */}
      <header className="sticky top-0 z-40 glass-panel border-b border-brand-border/40 px-4 lg:px-8 py-3 flex items-center justify-between shadow-xl">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl gold-button flex items-center justify-center font-bold text-gray-950 text-xl shadow-lg shadow-gold-500/20">
            👑
          </div>
          <div>
            <h1 className="font-heading font-extrabold text-lg lg:text-xl gold-gradient-text tracking-wide">
              İREM DÜĞÜN SARAYI
            </h1>
            <p className="text-xs text-gold-400 font-medium">Organizasyon & Kiralama Portalı</p>
          </div>
        </div>

        {/* Role Switcher & Controls */}
        <div className="flex items-center space-x-3 lg:space-x-6">
          
          {/* Quick Role Switcher Simulator */}
          <div className="bg-brand-card/90 border border-gold-500/30 rounded-full p-1 flex items-center shadow-inner">
            <span className="text-xs font-semibold px-2 text-gold-400 hidden sm:inline">Rol:</span>
            {[
              { id: 'admin', label: 'Admin 👑' },
              { id: 'satisci', label: 'Satışçı 💼' },
              { id: 'sosyal_medyaci', label: 'Sosyal Medya 📸' },
              { id: 'musteri', label: 'Müşteri 💑' }
            ].map(role => (
              <button
                key={role.id}
                onClick={() => {
                  setActiveRole(role.id);
                  showToast(`Rol Değiştirildi: ${role.label}`);
                }}
                className={`px-3 py-1 text-xs font-semibold rounded-full transition-all duration-200 ${
                  activeRole === role.id
                    ? 'bg-gold-500 text-gray-950 font-bold shadow-md'
                    : 'text-gray-400 hover:text-gray-200'
                }`}
              >
                {role.label}
              </button>
            ))}
          </div>

          {/* Theme Toggle */}
          <button
            onClick={() => setThemeMode(prev => prev === 'dark' ? 'light' : 'dark')}
            className="p-2 rounded-xl bg-brand-card border border-brand-border text-gold-400 hover:bg-gold-500/10 transition"
            title="Tema Değiştir"
          >
            {themeMode === 'dark' ? '☀️' : '🌙'}
          </button>

          {/* User Profile Avatar */}
          <div className="flex items-center space-x-2">
            <img
              src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=150&q=80"
              alt="Profil"
              className="w-9 h-9 rounded-full border-2 border-gold-500/60 object-cover"
            />
            <div className="hidden lg:block text-left">
              <div className="text-xs font-bold text-gray-200">İrem Yılmaz</div>
              <div className="text-[10px] text-gold-400 capitalize">{activeRole}</div>
            </div>
          </div>

        </div>
      </header>

      {/* --- BODY MAIN LAYOUT --- */}
      <div className="flex-1 flex overflow-hidden">
        
        {/* --- DESKTOP SIDEBAR --- */}
        <aside className="w-64 glass-panel border-r border-brand-border/40 p-4 hidden lg:flex flex-col justify-between">
          <nav className="space-y-1">
            <div className="text-[10px] font-bold text-gray-400 uppercase tracking-wider px-3 mb-2">Menü</div>
            
            {[
              { id: 'dashboard', label: 'Anasayfa / İstatistikler', icon: '📊', roles: ['admin', 'satisci', 'sosyal_medyaci', 'musteri'] },
              { id: 'venues', label: 'Düğün Salonlarım', icon: '🏛️', roles: ['admin', 'satisci'] },
              { id: 'services', label: 'Ek Hizmetler', icon: '✨', roles: ['admin', 'satisci'] },
              { id: 'reservations', label: 'Rezervasyonlarım', icon: '📋', roles: ['admin', 'satisci'] },
              { id: 'calendar', label: 'Takvim Görünümü', icon: '📅', roles: ['admin', 'satisci'] },
              { id: 'campaigns', label: 'Kampanyalar', icon: '🎁', roles: ['admin'] },
              { id: 'finance', label: 'Finans & Fature', icon: '💰', roles: ['admin'] },
              { id: 'customers', label: 'Müşteri Rehberi', icon: '👥', roles: ['admin', 'satisci'] },
              { id: 'users', label: 'Kullanıcı Yönetimi', icon: '⚙️', roles: ['admin'] },
              { id: 'reports', label: 'Raporlar & AI Öneri', icon: '📈', roles: ['admin'] },
              { id: 'media', label: 'Medya & Foto Yükle', icon: '📷', roles: ['sosyal_medyaci', 'admin', 'musteri'] }
            ]
            .filter(item => item.roles.includes(activeRole))
            .map(item => (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl font-medium text-sm transition-all duration-200 ${
                  activeTab === item.id
                    ? 'bg-gold-500/20 text-gold-400 border border-gold-500/30 shadow-md font-semibold'
                    : 'text-gray-400 hover:bg-brand-card hover:text-gray-200'
                }`}
              >
                <span className="text-lg">{item.icon}</span>
                <span>{item.label}</span>
              </button>
            ))}
          </nav>

          <div className="bg-brand-card/70 border border-gold-500/20 rounded-2xl p-4 text-center">
            <div className="text-2xl mb-1">🏰</div>
            <div className="text-xs font-bold text-gold-400">İrem Düğün Sarayı</div>
            <div className="text-[10px] text-gray-400 mt-1">Sapanca / Sakarya</div>
            <div className="text-[10px] text-gray-500 mt-2 font-mono">+90 555 555 55 55</div>
          </div>
        </aside>

        {/* --- MAIN CONTENT AREA --- */}
        <main className="flex-1 p-4 lg:p-8 overflow-y-auto pb-24 lg:pb-8">
          
          {/* Toast Notification */}
          {toast && (
            <div className={`fixed top-20 right-6 z-50 px-5 py-3 rounded-xl shadow-2xl font-medium text-sm flex items-center space-x-2 border transition-all animate-bounce ${
              toast.type === 'error' ? 'bg-red-950/90 text-red-200 border-red-500/50' : 'bg-emerald-950/90 text-emerald-200 border-emerald-500/50'
            }`}>
              <span>{toast.msg}</span>
            </div>
          )}

          {/* Dynamic Content Views */}
          {activeTab === 'dashboard' && (
            <DashboardView
              activeRole={activeRole}
              venues={venues}
              reservations={reservations}
              financialStats={financialStats}
              onNewResClick={() => setNewResModalOpen(true)}
              onTabChange={setActiveTab}
            />
          )}

          {activeTab === 'venues' && (
            <VenuesView venues={venues} setVenues={setVenues} showToast={showToast} />
          )}

          {activeTab === 'services' && (
            <ServicesView services={services} setServices={setServices} showToast={showToast} />
          )}

          {activeTab === 'reservations' && (
            <ReservationsView
              reservations={filteredReservations}
              venues={venues}
              searchQuery={resSearchQuery}
              setSearchQuery={setResSearchQuery}
              statusFilter={resStatusFilter}
              setStatusFilter={setResStatusFilter}
              venueFilter={resVenueFilter}
              setVenueFilter={setResVenueFilter}
              onNewResClick={() => setNewResModalOpen(true)}
              onDetailClick={setSelectedResForDetail}
              showToast={showToast}
            />
          )}

          {activeTab === 'calendar' && (
            <CalendarView reservations={reservations} venues={venues} onResClick={setSelectedResForDetail} />
          )}

          {activeTab === 'campaigns' && (
            <CampaignsView campaigns={campaigns} setCampaigns={setCampaigns} showToast={showToast} />
          )}

          {activeTab === 'finance' && (
            <FinanceView financialStats={financialStats} reservations={reservations} />
          )}

          {activeTab === 'customers' && (
            <CustomersView customers={customers} showToast={showToast} />
          )}

          {activeTab === 'users' && (
            <UsersView users={users} setUsers={setUsers} showToast={showToast} />
          )}

          {activeTab === 'reports' && (
            <ReportsView reservations={reservations} aiRecommendations={AI_RECOMMENDATIONS} />
          )}

          {activeTab === 'media' && (
            <MediaView reservations={reservations} setReservations={setReservations} showToast={showToast} />
          )}

        </main>
      </div>

      {/* --- MOBILE BOTTOM TAB BAR --- */}
      <div className="lg:hidden fixed bottom-0 left-0 right-0 glass-panel border-t border-brand-border/40 px-2 py-2 z-40 flex justify-around items-center">
        {[
          { id: 'dashboard', label: 'Anasayfa', icon: '📊' },
          { id: 'reservations', label: 'Rezervasyon', icon: '📋' },
          { id: 'calendar', label: 'Takvim', icon: '📅' },
          { id: 'venues', label: 'Salonlar', icon: '🏛️' }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex flex-col items-center py-1 px-3 rounded-xl transition ${
              activeTab === tab.id ? 'text-gold-400 font-bold bg-gold-500/10' : 'text-gray-400'
            }`}
          >
            <span className="text-xl">{tab.icon}</span>
            <span className="text-[10px]">{tab.label}</span>
          </button>
        ))}
      </div>

      {/* --- MODAL: NEW RESERVATION WIZARD --- */}
      {newResModalOpen && (
        <NewReservationModal
          resForm={resForm}
          setResForm={setResForm}
          resFormTotals={resFormTotals}
          collisionWarning={collisionWarning}
          venues={venues}
          services={services}
          campaigns={campaigns}
          onClose={() => setNewResModalOpen(false)}
          onSave={handleSaveReservation}
        />
      )}

      {/* --- MODAL: RESERVATION DETAIL --- */}
      {selectedResForDetail && (
        <ReservationDetailModal
          res={selectedResForDetail}
          venues={venues}
          services={services}
          onClose={() => setSelectedResForDetail(null)}
        />
      )}

      {/* --- MODAL: AUTOMATED EMAIL PREVIEW SIMULATOR --- */}
      {emailModalData && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-brand-card border border-gold-500/40 rounded-2xl max-w-2xl w-full p-6 shadow-2xl space-y-4 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between border-b border-brand-border pb-3">
              <div>
                <span className="bg-gold-500/20 text-gold-400 text-xs px-2.5 py-1 rounded-full font-bold">
                  ⚡ Otomasyon E-Posta Simülasyonu
                </span>
                <h3 className="text-lg font-bold text-gray-100 mt-1">{emailModalData.subject}</h3>
                <div className="text-xs text-gray-400">Alıcı: {emailModalData.recipient}</div>
              </div>
              <button
                onClick={() => setEmailModalData(null)}
                className="text-gray-400 hover:text-white text-xl font-bold p-2"
              >
                ✕
              </button>
            </div>

            {/* Email Preview Frame */}
            <div
              className="bg-brand-dark rounded-xl p-4 border border-brand-border text-sm overflow-x-auto"
              dangerouslySetInnerHTML={{ __html: emailModalData.htmlContent }}
            />

            <div className="flex justify-end pt-2">
              <button
                onClick={() => setEmailModalData(null)}
                className="gold-button text-gray-950 font-bold px-6 py-2 rounded-xl text-sm shadow-lg"
              >
                Tamam ve Kapat
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}


// ==========================================
// 1. DASHBOARD VIEW (Role-Based)
// ==========================================
function DashboardView({ activeRole, venues, reservations, financialStats, onNewResClick, onTabChange }) {
  const upcomingCount = reservations.filter(r => r.paymentStatus !== 'Tamamlandı').length;

  return (
    <div className="space-y-6">
      
      {/* Banner */}
      <div className="glass-panel p-6 rounded-3xl border border-gold-500/30 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 relative overflow-hidden">
        <div className="absolute -right-10 -bottom-10 opacity-10 text-9xl">👑</div>
        <div>
          <span className="bg-gold-500/20 text-gold-400 text-xs font-bold px-3 py-1 rounded-full border border-gold-500/30">
            {activeRole === 'admin' && '👑 Admin Yönetim Paneli'}
            {activeRole === 'satisci' && '💼 Satış & Doluluk Ekranı'}
            {activeRole === 'sosyal_medyaci' && '📸 Medya Yükleme Paneli'}
            {activeRole === 'musteri' && '💖 Özel Müşteri Portalı'}
          </span>
          <h2 className="text-2xl lg:text-3xl font-heading font-extrabold text-gray-100 mt-2">
            Hoş Geldiniz, İrem Hanım ✨
          </h2>
          <p className="text-sm text-gray-400 mt-1">
            İrem Düğün Sarayı güncel rezervasyon durumu ve organizasyon hareketleri.
          </p>
        </div>

        {(activeRole === 'admin' || activeRole === 'satisci') && (
          <button
            onClick={onNewResClick}
            className="gold-button text-gray-950 font-bold px-6 py-3 rounded-2xl shadow-xl flex items-center space-x-2 text-sm"
          >
            <span>➕</span>
            <span>Yeni Rezervasyon Oluştur</span>
          </button>
        )}
      </div>

      {/* --- ADMIN DASHBOARD --- */}
      {activeRole === 'admin' && (
        <>
          {/* Stat Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <StatCard icon="🏛️" title="Toplam Düğün Salonu" value={venues.length} sub={`${reservations.length} Toplam Rezervasyon`} />
            <StatCard icon="📅" title="Bu Ayın Boş Günleri" value="12 Gün" sub="Doluluk Oranı %82" highlight />
            <StatCard icon="💰" title="Son Ay Toplam Kazanç" value={formatCurrency(financialStats.totalRev)} sub="Tahsil edilen tutar" />
            <StatCard icon="⏳" title="Toplam Bekleyen Ödemeler" value={formatCurrency(financialStats.totalPending)} sub="Kalan bakiyeler toplamı" danger />
          </div>

          {/* Quick Actions & Recent Table */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 glass-panel p-6 rounded-2xl border border-brand-border/40 space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="font-heading font-bold text-lg text-gray-100">Son Rezervasyonlar</h3>
                <button onClick={() => onTabChange('reservations')} className="text-xs text-gold-400 hover:underline">Tümünü Gör →</button>
              </div>
              <RecentReservationsTable reservations={reservations.slice(0, 5)} venues={venues} />
            </div>

            <div className="glass-panel p-6 rounded-2xl border border-brand-border/40 space-y-4">
              <h3 className="font-heading font-bold text-lg text-gray-100">Hızlı İşlemler</h3>
              <div className="space-y-2">
                <button onClick={onNewResClick} className="w-full text-left p-3 rounded-xl bg-brand-card hover:bg-gold-500/10 border border-brand-border text-sm font-medium flex items-center justify-between text-gray-200">
                  <span>➕ Yeni Rezervasyon Ekle</span>
                  <span>→</span>
                </button>
                <button onClick={() => onTabChange('services')} className="w-full text-left p-3 rounded-xl bg-brand-card hover:bg-gold-500/10 border border-brand-border text-sm font-medium flex items-center justify-between text-gray-200">
                  <span>✨ Yeni Hizmet Tanımla</span>
                  <span>→</span>
                </button>
                <button onClick={() => onTabChange('campaigns')} className="w-full text-left p-3 rounded-xl bg-brand-card hover:bg-gold-500/10 border border-brand-border text-sm font-medium flex items-center justify-between text-gray-200">
                  <span>🎁 İndirim Kuponu Oluştur</span>
                  <span>→</span>
                </button>
                <button onClick={() => onTabChange('reports')} className="w-full text-left p-3 rounded-xl bg-brand-card hover:bg-gold-500/10 border border-brand-border text-sm font-medium flex items-center justify-between text-gray-200">
                  <span>📈 AI Raporları İncele</span>
                  <span>→</span>
                </button>
              </div>
            </div>
          </div>
        </>
      )}

      {/* --- SATIŞÇI DASHBOARD (Strictly NO revenue stats) --- */}
      {activeRole === 'satisci' && (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <StatCard icon="🏛️" title="Aktif Salon Sayısı" value={venues.length} sub="Tüm salonlar hazır" />
            <StatCard icon="📆" title="Ayın Boş Günleri" value="12 Gün" sub="Kiralanabilir en uygun günler" highlight />
            <StatCard icon="💳" title="Kapora Alınanlar" value={reservations.filter(r => r.depositPaid > 0).length} sub="Onaylı Rezervasyon" />
            <StatCard icon="⚠️" title="Kapora Alınmayanlar" value={reservations.filter(r => r.depositPaid === 0).length} sub="Beklemedeki Kayıtlar" danger />
          </div>

          {/* Optimal Days Recommender Card */}
          <div className="glass-panel p-6 rounded-2xl border border-gold-500/30 space-y-3">
            <div className="flex items-center space-x-2">
              <span className="text-2xl">💡</span>
              <h3 className="font-heading font-bold text-lg text-gold-400">Rezerve Edilecek En Uygun Gün Önerileri</h3>
            </div>
            <p className="text-xs text-gray-300">
              Satış ekibi için öncelikli önerilen boş günler: <strong>14 Ağustos Salı (Gündüz & Gece)</strong>, <strong>22 Ağustos Çarşamba</strong>. Müşterilerinize bu tarihleri önererek doluluk oranınızı artırabilirsiniz.
            </p>
          </div>

          <div className="glass-panel p-6 rounded-2xl border border-brand-border/40">
            <h3 className="font-heading font-bold text-lg text-gray-100 mb-4">Rezervasyon Doluluk Listesi</h3>
            <RecentReservationsTable reservations={reservations} venues={venues} hideFinancials />
          </div>
        </>
      )}

      {/* --- SOSYAL MEDYACI DASHBOARD --- */}
      {activeRole === 'sosyal_medyaci' && (
        <div className="glass-panel p-8 rounded-3xl border border-brand-border/40 text-center max-w-xl mx-auto space-y-6">
          <div className="text-5xl">📸</div>
          <h3 className="text-2xl font-heading font-bold text-gold-400">Rezervasyon Ara & Fotoğraf/Video Yükle</h3>
          <p className="text-xs text-gray-400">
            Düğün öncesi veya sonrasında çekilen medya dosyalarını yüklemek için rezervasyon kodunu giriniz.
          </p>
          <button
            onClick={() => onTabChange('media')}
            className="gold-button text-gray-950 font-bold px-8 py-3 rounded-2xl shadow-xl w-full text-sm"
          >
            📷 Medya Yükleme Ekranına Git
          </button>
        </div>
      )}

      {/* --- MÜŞTERİ DASHBOARD --- */}
      {activeRole === 'musteri' && (
        <div className="space-y-6">
          <div className="glass-panel p-6 rounded-2xl border border-gold-500/40 space-y-4">
            <div className="flex items-center justify-between border-b border-brand-border/40 pb-3">
              <div>
                <span className="bg-emerald-500/20 text-emerald-400 text-xs px-2.5 py-1 rounded-full font-bold">
                  Onaylı Rezervasyonum
                </span>
                <h3 className="text-xl font-bold text-gray-100 mt-1">Ahmet Yılmaz & Ayşe Kaya Düğün Töreni</h3>
              </div>
              <div className="text-right">
                <div className="text-xs text-gray-400">Rezervasyon Kodu</div>
                <div className="text-sm font-mono font-bold text-gold-400">RES-2026-001</div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <div className="bg-brand-dark p-3 rounded-xl border border-brand-border">
                <div className="text-xs text-gray-400">Düğün Salonu</div>
                <div className="font-bold text-gray-200">Kraliyet Balo Salonu</div>
              </div>
              <div className="bg-brand-dark p-3 rounded-xl border border-brand-border">
                <div className="text-xs text-gray-400">Tarih & Saat</div>
                <div className="font-bold text-gray-200">15 Ağustos 2026 (19:00 - 23:00)</div>
              </div>
              <div className="bg-brand-dark p-3 rounded-xl border border-brand-border">
                <div className="text-xs text-gray-400">Ödeme Durumu</div>
                <div className="font-bold text-emerald-400">Kapora Ödendi (₺50.000)</div>
              </div>
            </div>

            {/* Event Timeline Flow */}
            <div className="space-y-2 pt-2">
              <h4 className="font-heading font-bold text-sm text-gold-400">⏰ Düğün Günü Etkinlik Akış Planınız</h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
                {[
                  { time: '19:00', title: 'Misafir Karşılama & Kokteyl' },
                  { time: '19:30', title: 'Gelin Damat Girişi & Dans' },
                  { time: '20:15', title: 'Gurme Yemek Servisi' },
                  { time: '21:30', title: 'Pasta Kesimi & Volkan Şov' },
                  { time: '22:00', title: 'Takı & Orkestra Eğlencesi' },
                  { time: '23:00', title: 'Uğurlama' }
                ].map((item, idx) => (
                  <div key={idx} className="bg-brand-card p-2.5 rounded-xl border border-brand-border flex items-center space-x-3 text-xs">
                    <span className="bg-gold-500/20 text-gold-400 font-bold px-2 py-1 rounded-lg">{item.time}</span>
                    <span className="text-gray-200 font-medium">{item.title}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="pt-3 flex justify-end">
              <button onClick={() => onTabChange('media')} className="gold-button text-gray-950 font-bold px-6 py-2.5 rounded-xl text-xs">
                📸 Düğün Fotoğraflarını & Galeriyi Görüntüle
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}


// Helper StatCard Component
function StatCard({ icon, title, value, sub, highlight, danger }) {
  return (
    <div className={`glass-panel p-5 rounded-2xl border transition-all duration-200 hover:scale-[1.02] ${
      highlight ? 'border-gold-500/50 shadow-lg shadow-gold-500/10' : danger ? 'border-red-500/40' : 'border-brand-border/40'
    }`}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold text-gray-400">{title}</span>
        <span className="text-xl">{icon}</span>
      </div>
      <div className={`text-2xl lg:text-3xl font-extrabold mt-2 font-heading ${
        highlight ? 'gold-gradient-text' : danger ? 'text-red-400' : 'text-gray-100'
      }`}>
        {value}
      </div>
      <div className="text-[11px] text-gray-500 mt-1">{sub}</div>
    </div>
  );
}


// Recent Reservations Table Component
function RecentReservationsTable({ reservations, venues, hideFinancials }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left text-xs">
        <thead className="bg-brand-card text-gray-400 uppercase font-semibold border-b border-brand-border">
          <tr>
            <th className="p-3">Kod</th>
            <th className="p-3">Müşteri</th>
            <th className="p-3">Salon</th>
            <th className="p-3">Tarih</th>
            {!hideFinancials && <th className="p-3">Toplam Tutar</th>}
            <th className="p-3">Durum</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-brand-border/30">
          {reservations.map(res => {
            const venue = venues.find(v => v.id === res.venueId);
            return (
              <tr key={res.id} className="hover:bg-brand-card/50 transition">
                <td className="p-3 font-mono font-bold text-gold-400">{res.id}</td>
                <td className="p-3 font-medium text-gray-200">{res.customerName}</td>
                <td className="p-3 text-gray-300">{venue?.name || '-'}</td>
                <td className="p-3 text-gray-400">{formatDate(res.date)}</td>
                {!hideFinancials && <td className="p-3 font-bold text-gray-100">{formatCurrency(res.totalAmount)}</td>}
                <td className="p-3">
                  <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold ${
                    res.paymentStatus === 'Ödendi' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' :
                    res.paymentStatus === 'Kapora Alındı' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
                    res.paymentStatus === 'Tamamlandı' ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30' :
                    'bg-red-500/20 text-red-400 border border-red-500/30'
                  }`}>
                    {res.paymentStatus}
                  </span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}


// ==========================================
// 2. VENUES VIEW
// ==========================================
function VenuesView({ venues, setVenues, showToast }) {
  const [modalOpen, setModalOpen] = useState(false);
  const [editingVenue, setEditingVenue] = useState(null);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Düğün Salonlarım</h2>
          <p className="text-xs text-gray-400 mt-1">Lüks balo salonları ve açık hava kır bahçesi alanlarınız.</p>
        </div>
        <button
          onClick={() => { setEditingVenue(null); setModalOpen(true); }}
          className="gold-button text-gray-950 font-bold px-5 py-2.5 rounded-xl text-xs flex items-center space-x-2"
        >
          <span>🏛️ Yeni Salon Ekle</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {venues.map(venue => (
          <div key={venue.id} className="glass-panel rounded-3xl border border-brand-border/40 overflow-hidden space-y-4 hover:border-gold-500/50 transition duration-300">
            <div className="relative h-48">
              <img src={venue.images[0]} alt={venue.name} className="w-full h-full object-cover" />
              <div className="absolute top-3 right-3 bg-brand-dark/80 backdrop-blur-md px-3 py-1 rounded-full text-xs font-bold text-gold-400 border border-gold-500/30">
                %{venue.occupancyRate} Doluluk
              </div>
            </div>
            <div className="p-5 space-y-3">
              <div className="flex items-center justify-between">
                <h3 className="font-heading font-bold text-lg text-gray-100">{venue.name}</h3>
                <span className="text-xs text-gold-400 font-bold bg-gold-500/10 px-2.5 py-1 rounded-full border border-gold-500/20">{venue.category}</span>
              </div>
              <p className="text-xs text-gray-400 line-clamp-2">{venue.description}</p>
              
              <div className="grid grid-cols-2 gap-2 text-xs pt-2">
                <div className="bg-brand-dark p-2 rounded-xl border border-brand-border">
                  <div className="text-[10px] text-gray-500">Kapasite</div>
                  <div className="font-bold text-gray-200">{venue.capacity} Kişilik</div>
                </div>
                <div className="bg-brand-dark p-2 rounded-xl border border-brand-border">
                  <div className="text-[10px] text-gray-500">Günlük Taban Fiyat</div>
                  <div className="font-bold text-gold-400">{formatCurrency(venue.price)}</div>
                </div>
              </div>

              <div className="pt-2 flex justify-between items-center text-xs">
                <span className="text-gray-500">Kapora: <strong className="text-gray-300">{formatCurrency(venue.deposit)}</strong></span>
                <button
                  onClick={() => { setEditingVenue(venue); setModalOpen(true); }}
                  className="px-4 py-1.5 rounded-lg bg-brand-card hover:bg-gold-500/20 text-gold-400 border border-gold-500/30 font-bold transition"
                >
                  Düzenle ✏️
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}


// ==========================================
// 3. SERVICES VIEW
// ==========================================
function ServicesView({ services, setServices, showToast }) {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Ek Hizmetlerim</h2>
          <p className="text-xs text-gray-400 mt-1">Düğün organizasyonlarına eklenebilir paket ve hizmetler.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {services.map(srv => (
          <div key={srv.id} className="glass-panel p-5 rounded-2xl border border-brand-border/40 flex flex-col justify-between space-y-4">
            <div className="space-y-2">
              <div className="h-36 rounded-xl overflow-hidden mb-3 border border-brand-border">
                <img src={srv.image} alt={srv.name} className="w-full h-full object-cover" />
              </div>
              <div className="flex items-center justify-between">
                <span className="text-[10px] uppercase font-bold text-gold-400 bg-gold-500/10 px-2 py-0.5 rounded-full border border-gold-500/20">{srv.category}</span>
                <span className="text-xs text-gray-400 font-medium">
                  {srv.pricingType === 'per_person' ? 'Kişi Başı' : 'Sabit Fiyat'}
                </span>
              </div>
              <h3 className="font-heading font-bold text-base text-gray-100">{srv.name}</h3>
              <p className="text-xs text-gray-400">{srv.description}</p>
            </div>
            <div className="flex items-center justify-between pt-3 border-t border-brand-border/40">
              <div className="text-lg font-extrabold text-gold-400 font-heading">
                {formatCurrency(srv.price)}
                {srv.pricingType === 'per_person' && <span className="text-xs text-gray-400 font-normal"> / kişi</span>}
              </div>
              <button className="px-3 py-1 rounded-lg bg-brand-card hover:bg-gold-500/20 text-gold-400 border border-gold-500/30 text-xs font-bold">
                Düzenle
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}


// ==========================================
// 4. RESERVATIONS VIEW
// ==========================================
function ReservationsView({ reservations, venues, searchQuery, setSearchQuery, statusFilter, setStatusFilter, venueFilter, setVenueFilter, onNewResClick, onDetailClick }) {
  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Tüm Rezervasyonlar</h2>
          <p className="text-xs text-gray-400 mt-1">Kayıtlı rezervasyonların listesi ve ödeme takibi.</p>
        </div>
        <button onClick={onNewResClick} className="gold-button text-gray-950 font-bold px-5 py-2.5 rounded-xl text-xs">
          ➕ Yeni Rezervasyon Ekle
        </button>
      </div>

      {/* Filter Bar */}
      <div className="glass-panel p-4 rounded-2xl border border-brand-border/40 flex flex-wrap items-center gap-3">
        <input
          type="text"
          placeholder="Rezervasyon kodu, müşteri veya telefon..."
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
          className="bg-brand-dark border border-brand-border rounded-xl px-4 py-2 text-xs text-gray-200 focus:outline-none focus:border-gold-500 w-full sm:w-64"
        />

        <select
          value={statusFilter}
          onChange={e => setStatusFilter(e.target.value)}
          className="bg-brand-dark border border-brand-border rounded-xl px-3 py-2 text-xs text-gray-200 focus:outline-none focus:border-gold-500"
        >
          <option value="all">Tüm Ödeme Durumları</option>
          <option value="Bekliyor">Bekliyor</option>
          <option value="Kapora Alındı">Kapora Alındı</option>
          <option value="Ödendi">Ödendi</option>
          <option value="Tamamlandı">Tamamlandı</option>
        </select>

        <select
          value={venueFilter}
          onChange={e => setVenueFilter(e.target.value)}
          className="bg-brand-dark border border-brand-border rounded-xl px-3 py-2 text-xs text-gray-200 focus:outline-none focus:border-gold-500"
        >
          <option value="all">Tüm Salonlar</option>
          {venues.map(v => <option key={v.id} value={v.id}>{v.name}</option>)}
        </select>
      </div>

      {/* Table */}
      <div className="glass-panel rounded-2xl border border-brand-border/40 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-brand-card text-gray-400 uppercase font-semibold border-b border-brand-border">
              <tr>
                <th className="p-3.5">Kod</th>
                <th className="p-3.5">Müşteri</th>
                <th className="p-3.5">Salon</th>
                <th className="p-3.5">Tarih / Saat</th>
                <th className="p-3.5">Davetli</th>
                <th className="p-3.5">Toplam Tutar</th>
                <th className="p-3.5">Alınan Kapora</th>
                <th className="p-3.5">Kalan Bakiye</th>
                <th className="p-3.5">Durum</th>
                <th className="p-3.5 text-right">İşlem</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-brand-border/30">
              {reservations.map(res => {
                const venue = venues.find(v => v.id === res.venueId);
                return (
                  <tr key={res.id} className="hover:bg-brand-card/50 transition">
                    <td className="p-3.5 font-mono font-bold text-gold-400">{res.id}</td>
                    <td className="p-3.5 font-medium text-gray-200">
                      <div>{res.customerName}</div>
                      <div className="text-[10px] text-gray-500">{res.customerPhone}</div>
                    </td>
                    <td className="p-3.5 text-gray-300 font-medium">{venue?.name || '-'}</td>
                    <td className="p-3.5 text-gray-300">
                      <div>{formatDate(res.date)}</div>
                      <div className="text-[10px] text-gold-400">{res.timeSlot}</div>
                    </td>
                    <td className="p-3.5 text-gray-300 font-bold">{res.guestCount} Kişi</td>
                    <td className="p-3.5 font-bold text-gray-100">{formatCurrency(res.totalAmount)}</td>
                    <td className="p-3.5 text-emerald-400 font-bold">{formatCurrency(res.depositPaid)}</td>
                    <td className="p-3.5 text-red-400 font-bold">{formatCurrency(res.remainingBalance)}</td>
                    <td className="p-3.5">
                      <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold ${
                        res.paymentStatus === 'Ödendi' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' :
                        res.paymentStatus === 'Kapora Alındı' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
                        res.paymentStatus === 'Tamamlandı' ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30' :
                        'bg-red-500/20 text-red-400 border border-red-500/30'
                      }`}>
                        {res.paymentStatus}
                      </span>
                    </td>
                    <td className="p-3.5 text-right">
                      <button
                        onClick={() => onDetailClick(res)}
                        className="px-3 py-1 rounded-lg bg-gold-500/20 hover:bg-gold-500 text-gold-400 hover:text-gray-950 font-bold border border-gold-500/30 transition text-[11px]"
                      >
                        Detay 🔍
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}


// ==========================================
// 5. CALENDAR VIEW
// ==========================================
function CalendarView({ reservations, venues, onResClick }) {
  const daysInMonth = Array.from({ length: 31 }, (_, i) => i + 1);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">İnteraktif Rezervasyon Takvimi</h2>
        <p className="text-xs text-gray-400 mt-1">Ağustos 2026 doluluk görünümü ve tıklanabilir etkinlikler.</p>
      </div>

      <div className="glass-panel p-6 rounded-3xl border border-brand-border/40 space-y-4">
        <div className="flex items-center justify-between border-b border-brand-border pb-4">
          <h3 className="font-heading font-bold text-lg text-gold-400">📅 Ağustos 2026</h3>
          <div className="flex space-x-2 text-xs">
            <span className="flex items-center space-x-1"><span className="w-3 h-3 rounded-full bg-amber-500 inline-block"></span> <span>Kapora Alındı</span></span>
            <span className="flex items-center space-x-1"><span className="w-3 h-3 rounded-full bg-emerald-500 inline-block"></span> <span>Ödendi</span></span>
          </div>
        </div>

        {/* Calendar Grid */}
        <div className="grid grid-cols-7 gap-2 text-center text-xs">
          {['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'].map(day => (
            <div key={day} className="font-bold text-gray-400 py-2 bg-brand-card rounded-lg">{day}</div>
          ))}

          {daysInMonth.map(day => {
            const dateStr = `2026-08-${day < 10 ? '0' + day : day}`;
            const dayRes = reservations.filter(r => r.date === dateStr);

            return (
              <div
                key={day}
                className={`min-h-[90px] p-2 rounded-xl border text-left flex flex-col justify-between transition ${
                  dayRes.length > 0 ? 'bg-brand-card/90 border-gold-500/40' : 'bg-brand-dark/40 border-brand-border/30 hover:border-gray-600'
                }`}
              >
                <div className="font-bold text-gray-300 text-xs">{day}</div>
                
                <div className="space-y-1">
                  {dayRes.map(res => {
                    const venue = venues.find(v => v.id === res.venueId);
                    return (
                      <button
                        key={res.id}
                        onClick={() => onResClick(res)}
                        className={`w-full text-left p-1 rounded text-[10px] font-bold truncate transition ${
                          res.paymentStatus === 'Ödendi' ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                        }`}
                      >
                        {res.timeSlot.includes('19:00') ? '🌙' : '☀️'} {venue?.name.split(' ')[0]} ({res.customerName.split(' ')[0]})
                      </button>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}


// ==========================================
// 6. CAMPAIGNS VIEW
// ==========================================
function CampaignsView({ campaigns, setCampaigns, showToast }) {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Özel Kampanyalar</h2>
          <p className="text-xs text-gray-400 mt-1">İndirim kuponları ve hediye hizmet tanımları.</p>
        </div>
        <button className="gold-button text-gray-950 font-bold px-5 py-2.5 rounded-xl text-xs">
          🎁 Yeni Kampanya Tanımla
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {campaigns.map(c => (
          <div key={c.id} className="glass-panel p-6 rounded-3xl border border-gold-500/30 space-y-3 relative overflow-hidden">
            <div className="flex justify-between items-start">
              <span className="bg-gold-500/20 text-gold-400 font-mono font-bold text-xs px-3 py-1 rounded-full border border-gold-500/30">
                {c.code}
              </span>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${c.active ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'}`}>
                {c.active ? 'Aktif' : 'Pasif'}
              </span>
            </div>
            <h3 className="font-heading font-bold text-lg text-gray-100">{c.title}</h3>
            <p className="text-xs text-gray-400">{c.description}</p>
            <div className="text-[10px] text-gray-500 pt-2 border-t border-brand-border">
              Geçerlilik: {c.startDate} - {c.endDate}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}


// ==========================================
// 7. FINANCE VIEW
// ==========================================
function FinanceView({ financialStats, reservations }) {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Finans & Fatura Yönetimi</h2>
        <p className="text-xs text-gray-400 mt-1">Ciro, tahsilat, hak edişler ve KDV hesap dökümleri.</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard icon="💰" title="Toplam Rezervasyon Cirosu" value={formatCurrency(financialStats.totalRev)} sub="Tüm onaylı sözleşmeler" />
        <StatCard icon="💳" title="Alınan Kaporalar" value={formatCurrency(financialStats.totalDeposit)} sub="Tahsil edilen nakit" highlight />
        <StatCard icon="⏳" title="Tahsil Edilecek Bakiye" value={formatCurrency(financialStats.totalPending)} sub="Gelecek ödemeler" danger />
        <StatCard icon="🧾" title="Toplam KDV Tutarı (%20)" value={formatCurrency(financialStats.totalVat)} sub="Faturalandırılan KDV" />
      </div>

      <div className="glass-panel p-6 rounded-2xl border border-brand-border/40">
        <h3 className="font-heading font-bold text-lg text-gray-100 mb-4">Fatura Döküm Listesi</h3>
        <RecentReservationsTable reservations={reservations} venues={[]} />
      </div>
    </div>
  );
}


// ==========================================
// 8. CUSTOMERS & WHATSAPP VIEW
// ==========================================
function CustomersView({ customers, showToast }) {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Müşteri Rehberi</h2>
          <p className="text-xs text-gray-400 mt-1">Kayıtlı müşterileriniz ve doğrudan WhatsApp iletişimi.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {customers.map(cust => (
          <div key={cust.id} className="glass-panel p-6 rounded-3xl border border-brand-border/40 flex items-start space-x-4">
            <img src={cust.avatar} alt={cust.name} className="w-16 h-16 rounded-2xl object-cover border border-gold-500/40" />
            <div className="flex-1 space-y-2">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-heading font-bold text-base text-gray-100">{cust.name}</h3>
                  <div className="text-xs text-gray-400">{cust.email} | {cust.phone}</div>
                </div>
                <span className="bg-brand-card text-gold-400 text-[10px] font-bold px-2 py-1 rounded-full border border-gold-500/20">
                  {cust.taxType === 'corporate' ? 'Kurumsal' : 'Bireysel'}
                </span>
              </div>

              <div className="text-xs text-gray-400 bg-brand-dark p-2 rounded-xl border border-brand-border">
                📍 {cust.address}
              </div>

              {cust.followUp && (
                <div className="text-[11px] text-amber-400 bg-amber-500/10 p-2 rounded-xl border border-amber-500/20">
                  🔔 <strong>Tekrar Aranacak:</strong> {cust.followUpNote}
                </div>
              )}

              {/* Direct WhatsApp Button */}
              <div className="pt-2 flex justify-end">
                <a
                  href={generateWhatsAppLink(cust.phone)}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-4 py-2 rounded-xl text-xs flex items-center space-x-2 shadow-lg transition"
                >
                  <span>💬</span>
                  <span>WhatsApp ile Konuşma Başlat</span>
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}


// ==========================================
// 9. USERS VIEW
// ==========================================
function UsersView({ users, setUsers, showToast }) {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Kullanıcı Yönetimi</h2>
          <p className="text-xs text-gray-400 mt-1">Sistem yetkilileri ve rol tanımları.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {users.map(u => (
          <div key={u.id} className="glass-panel p-5 rounded-2xl border border-brand-border/40 text-center space-y-3">
            <img src={u.avatar} alt={u.name} className="w-20 h-20 rounded-full mx-auto object-cover border-2 border-gold-500/50 shadow-md" />
            <div>
              <h3 className="font-heading font-bold text-sm text-gray-100">{u.name}</h3>
              <div className="text-xs text-gray-400 truncate">{u.email}</div>
            </div>
            <span className="inline-block bg-gold-500/20 text-gold-400 text-xs font-bold px-3 py-1 rounded-full uppercase border border-gold-500/30">
              {u.role}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}


// ==========================================
// 10. REPORTS & AI VIEW
// ==========================================
function ReportsView({ reservations, aiRecommendations }) {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Raporlar & AI Öneriler</h2>
        <p className="text-xs text-gray-400 mt-1">İşletme analizleri ve akıllı gelir artırma tavsiyeleri.</p>
      </div>

      {/* AI Recommendation Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {aiRecommendations.map(rec => (
          <div key={rec.id} className="glass-panel p-6 rounded-3xl border border-gold-500/40 space-y-3 relative">
            <div className="flex justify-between items-center">
              <span className="bg-gold-500/20 text-gold-400 text-xs font-bold px-3 py-1 rounded-full">
                ✨ Yapay Zeka Tavsiyesi
              </span>
              <span className="text-xs font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded">
                {rec.badge}
              </span>
            </div>
            <h3 className="font-heading font-bold text-lg text-gray-100">{rec.title}</h3>
            <p className="text-xs text-gray-300 leading-relaxed">{rec.description}</p>
            <button className="gold-button text-gray-950 font-bold px-4 py-2 rounded-xl text-xs">
              {rec.actionText}
            </button>
          </div>
        ))}
      </div>

      {/* Analysis Bar Charts Simulation */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-panel p-5 rounded-2xl border border-brand-border/40 space-y-2">
          <h4 className="font-heading font-bold text-sm text-gold-400">🔥 En Çok Rağbet Gören Aylar</h4>
          <div className="space-y-1 text-xs">
            <div className="flex justify-between text-gray-300"><span>Ağustos</span><strong>%94 Doluluk</strong></div>
            <div className="w-full bg-brand-dark h-2 rounded-full"><div className="bg-gold-500 h-2 rounded-full w-[94%]"></div></div>
            <div className="flex justify-between text-gray-300 pt-1"><span>Eylül</span><strong>%88 Doluluk</strong></div>
            <div className="w-full bg-brand-dark h-2 rounded-full"><div className="bg-gold-500 h-2 rounded-full w-[88%]"></div></div>
            <div className="flex justify-between text-gray-300 pt-1"><span>Temmuz</span><strong>%85 Doluluk</strong></div>
            <div className="w-full bg-brand-dark h-2 rounded-full"><div className="bg-gold-500 h-2 rounded-full w-[85%]"></div></div>
          </div>
        </div>

        <div className="glass-panel p-5 rounded-2xl border border-brand-border/40 space-y-2">
          <h4 className="font-heading font-bold text-sm text-gold-400">📅 En Çok Rağbet Gören Günler</h4>
          <div className="space-y-1 text-xs">
            <div className="flex justify-between text-gray-300"><span>Cumartesi</span><strong>%98 Tercih</strong></div>
            <div className="w-full bg-brand-dark h-2 rounded-full"><div className="bg-emerald-500 h-2 rounded-full w-[98%]"></div></div>
            <div className="flex justify-between text-gray-300 pt-1"><span>Pazar</span><strong>%90 Tercih</strong></div>
            <div className="w-full bg-brand-dark h-2 rounded-full"><div className="bg-emerald-500 h-2 rounded-full w-[90%]"></div></div>
            <div className="flex justify-between text-gray-300 pt-1"><span>Cuma</span><strong>%72 Tercih</strong></div>
            <div className="w-full bg-brand-dark h-2 rounded-full"><div className="bg-emerald-500 h-2 rounded-full w-[72%]"></div></div>
          </div>
        </div>

        <div className="glass-panel p-5 rounded-2xl border border-brand-border/40 space-y-2">
          <h4 className="font-heading font-bold text-sm text-gold-400">⏰ En Çok Tercih Edilen Saatler</h4>
          <div className="space-y-1 text-xs">
            <div className="flex justify-between text-gray-300"><span>19:00 - 23:00 (Gece)</span><strong>%82 Tercih</strong></div>
            <div className="w-full bg-brand-dark h-2 rounded-full"><div className="bg-amber-500 h-2 rounded-full w-[82%]"></div></div>
            <div className="flex justify-between text-gray-300 pt-1"><span>13:00 - 17:00 (Gündüz)</span><strong>%18 Tercih</strong></div>
            <div className="w-full bg-brand-dark h-2 rounded-full"><div className="bg-amber-500 h-2 rounded-full w-[18%]"></div></div>
          </div>
        </div>
      </div>
    </div>
  );
}


// ==========================================
// 11. MEDIA & GALLERY VIEW
// ==========================================
function MediaView({ reservations, setReservations, showToast }) {
  const [selectedResId, setSelectedResId] = useState(reservations[0]?.id || '');
  const targetRes = reservations.find(r => r.id === selectedResId);

  const sampleImages = [
    'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80',
    'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=800&q=80',
    'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=800&q=80'
  ];

  const handleSimulateUpload = () => {
    if (!targetRes) return;
    const newMedia = {
      id: 'm-' + Date.now(),
      url: sampleImages[Math.floor(Math.random() * sampleImages.length)],
      type: 'image',
      uploadedBy: 'Sosyal Medya Ekibi'
    };

    setReservations(prev => prev.map(r => {
      if (r.id === selectedResId) {
        return { ...r, mediaGallery: [newMedia, ...r.mediaGallery] };
      }
      return r;
    }));

    showToast('📸 Fotoğraf Galerisi Başarıyla Güncellendi!');
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Etkinlik Medya Galerisi</h2>
        <p className="text-xs text-gray-400 mt-1">Rezervasyon seçip fotoğraf ve video içeriklerini yükleyiniz.</p>
      </div>

      <div className="glass-panel p-6 rounded-3xl border border-brand-border/40 space-y-4">
        <label className="text-xs font-bold text-gray-300">Rezervasyon Seçiniz:</label>
        <select
          value={selectedResId}
          onChange={e => setSelectedResId(e.target.value)}
          className="bg-brand-dark border border-brand-border rounded-xl px-4 py-2.5 text-xs text-gray-200 focus:outline-none focus:border-gold-500 w-full"
        >
          {reservations.map(r => (
            <option key={r.id} value={r.id}>
              {r.id} - {r.customerName} ({r.date})
            </option>
          ))}
        </select>

        {/* Upload Dropzone Simulator */}
        <div className="border-2 border-dashed border-gold-500/40 rounded-2xl p-8 text-center space-y-3 bg-brand-dark/50 hover:bg-brand-dark transition">
          <div className="text-4xl">📤</div>
          <div className="text-sm font-bold text-gray-200">Fotoğraf & Videoları Sürükleyip Bırakın</div>
          <div className="text-xs text-gray-500">PNG, JPG, MP4 (Maks 500MB)</div>
          <button onClick={handleSimulateUpload} className="gold-button text-gray-950 font-bold px-6 py-2 rounded-xl text-xs">
            ✨ Örnek Medya Yükle
          </button>
        </div>

        {/* Media Gallery Grid */}
        {targetRes && (
          <div className="space-y-3 pt-4 border-t border-brand-border">
            <h3 className="font-heading font-bold text-sm text-gold-400">🖼️ Yüklü Medyalar ({targetRes.mediaGallery.length})</h3>
            {targetRes.mediaGallery.length === 0 ? (
              <div className="text-xs text-gray-500 italic text-center py-6">Henüz bu rezervasyona medya yüklenmemiş.</div>
            ) : (
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                {targetRes.mediaGallery.map(item => (
                  <div key={item.id} className="relative h-36 rounded-xl overflow-hidden border border-brand-border group">
                    <img src={item.url} alt="Etkinlik" className="w-full h-full object-cover group-hover:scale-105 transition duration-300" />
                    <div className="absolute bottom-0 inset-x-0 bg-brand-dark/80 backdrop-blur-md p-1.5 text-[10px] text-gray-300 truncate">
                      {item.uploadedBy}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}


// ==========================================
// 12. NEW RESERVATION WIZARD MODAL
// ==========================================
function NewReservationModal({ resForm, setResForm, resFormTotals, collisionWarning, venues, services, campaigns, onClose, onSave }) {
  const [step, setStep] = useState(1);

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
      <div className="bg-brand-card border border-gold-500/40 rounded-3xl max-w-3xl w-full p-6 shadow-2xl space-y-6 max-h-[90vh] overflow-y-auto">
        
        {/* Header */}
        <div className="flex justify-between items-center border-b border-brand-border pb-4">
          <div>
            <span className="text-xs text-gold-400 font-bold uppercase tracking-wider">Adım {step} / 3</span>
            <h3 className="text-xl font-heading font-bold text-gray-100 mt-0.5">Yeni Rezervasyon Sihirbazı</h3>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-white text-xl">✕</button>
        </div>

        {/* Collision Warning Banner */}
        {collisionWarning && (
          <div className="bg-red-950/80 border border-red-500/50 p-3 rounded-xl text-xs text-red-200 font-medium">
            {collisionWarning}
          </div>
        )}

        <form onSubmit={onSave} className="space-y-6">
          
          {/* STEP 1: Salon, Tarih & Saat */}
          {step === 1 && (
            <div className="space-y-4">
              <h4 className="font-heading font-bold text-sm text-gold-400">1. Salon & Tarih Seçimi</h4>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="text-xs text-gray-400 block mb-1">Düğün Salonu:</label>
                  <select
                    value={resForm.venueId}
                    onChange={e => setResForm({ ...resForm, venueId: e.target.value })}
                    className="w-full bg-brand-dark border border-brand-border rounded-xl p-2.5 text-xs text-gray-200 focus:border-gold-500"
                  >
                    {venues.map(v => (
                      <option key={v.id} value={v.id}>{v.name} ({formatCurrency(v.price)})</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="text-xs text-gray-400 block mb-1">Etkinlik Tarihi:</label>
                  <input
                    type="date"
                    value={resForm.date}
                    onChange={e => setResForm({ ...resForm, date: e.target.value })}
                    className="w-full bg-brand-dark border border-brand-border rounded-xl p-2.5 text-xs text-gray-200 focus:border-gold-500"
                  />
                </div>

                <div>
                  <label className="text-xs text-gray-400 block mb-1">Saat Aralığı:</label>
                  <select
                    value={resForm.timeSlot}
                    onChange={e => setResForm({ ...resForm, timeSlot: e.target.value })}
                    className="w-full bg-brand-dark border border-brand-border rounded-xl p-2.5 text-xs text-gray-200 focus:border-gold-500"
                  >
                    <option value="19:00-23:00">19:00 - 23:00 (Gece)</option>
                    <option value="13:00-17:00">13:00 - 17:00 (Gündüz)</option>
                  </select>
                </div>

                <div>
                  <label className="text-xs text-gray-400 block mb-1">Davetli Kişi Sayısı:</label>
                  <input
                    type="number"
                    value={resForm.guestCount}
                    onChange={e => setResForm({ ...resForm, guestCount: Math.max(1, Number(e.target.value)) })}
                    className="w-full bg-brand-dark border border-brand-border rounded-xl p-2.5 text-xs text-gray-200 focus:border-gold-500"
                  />
                </div>
              </div>

              {/* Extra Services Checklist */}
              <div className="pt-2 space-y-2">
                <label className="text-xs text-gray-400 block">Ek Hizmetler Seçimi:</label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {services.map(srv => {
                    const isChecked = resForm.selectedServices.some(s => s.serviceId === srv.id);
                    return (
                      <label key={srv.id} className={`p-3 rounded-xl border flex items-center justify-between text-xs cursor-pointer transition ${
                        isChecked ? 'bg-gold-500/20 border-gold-500 text-gold-300 font-bold' : 'bg-brand-dark border-brand-border text-gray-300'
                      }`}>
                        <div className="flex items-center space-x-2">
                          <input
                            type="checkbox"
                            checked={isChecked}
                            onChange={e => {
                              if (e.target.checked) {
                                setResForm({ ...resForm, selectedServices: [...resForm.selectedServices, { serviceId: srv.id, quantity: 1 }] });
                              } else {
                                setResForm({ ...resForm, selectedServices: resForm.selectedServices.filter(s => s.serviceId !== srv.id) });
                              }
                            }}
                          />
                          <span>{srv.name}</span>
                        </div>
                        <span className="font-mono text-gold-400">{formatCurrency(srv.price)}</span>
                      </label>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

          {/* STEP 2: Müşteri & Fatura Bilgileri */}
          {step === 2 && (
            <div className="space-y-4">
              <h4 className="font-heading font-bold text-sm text-gold-400">2. Müşteri & Fatura Detayları</h4>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="text-xs text-gray-400 block mb-1">Müşteri Ad Soyad / Şirket Unvanı:</label>
                  <input
                    type="text"
                    required
                    placeholder="Örn: Ahmet Yılmaz"
                    value={resForm.customerName}
                    onChange={e => setResForm({ ...resForm, customerName: e.target.value })}
                    className="w-full bg-brand-dark border border-brand-border rounded-xl p-2.5 text-xs text-gray-200 focus:border-gold-500"
                  />
                </div>

                <div>
                  <label className="text-xs text-gray-400 block mb-1">E-Posta Adresi (Otomatik Üyelik Gönderilecek):</label>
                  <input
                    type="email"
                    required
                    placeholder="ahmet@example.com"
                    value={resForm.customerEmail}
                    onChange={e => setResForm({ ...resForm, customerEmail: e.target.value })}
                    className="w-full bg-brand-dark border border-brand-border rounded-xl p-2.5 text-xs text-gray-200 focus:border-gold-500"
                  />
                </div>

                <div>
                  <label className="text-xs text-gray-400 block mb-1">Telefon Numarası:</label>
                  <input
                    type="tel"
                    required
                    placeholder="+90 5XX XXX XX XX"
                    value={resForm.customerPhone}
                    onChange={e => setResForm({ ...resForm, customerPhone: e.target.value })}
                    className="w-full bg-brand-dark border border-brand-border rounded-xl p-2.5 text-xs text-gray-200 focus:border-gold-500"
                  />
                </div>

                <div>
                  <label className="text-xs text-gray-400 block mb-1">Fatura Tipi:</label>
                  <select
                    value={resForm.taxType}
                    onChange={e => setResForm({ ...resForm, taxType: e.target.value })}
                    className="w-full bg-brand-dark border border-brand-border rounded-xl p-2.5 text-xs text-gray-200 focus:border-gold-500"
                  >
                    <option value="individual">Bireysel Fatura (T.C. Kimlik)</option>
                    <option value="corporate">Kurumsal Fatura (VKN)</option>
                  </select>
                </div>

                {resForm.taxType === 'individual' ? (
                  <div>
                    <label className="text-xs text-gray-400 block mb-1">T.C. Kimlik No:</label>
                    <input
                      type="text"
                      placeholder="11 haneli T.C. No"
                      value={resForm.tcNo}
                      onChange={e => setResForm({ ...resForm, tcNo: e.target.value })}
                      className="w-full bg-brand-dark border border-brand-border rounded-xl p-2.5 text-xs text-gray-200 focus:border-gold-500"
                    />
                  </div>
                ) : (
                  <div>
                    <label className="text-xs text-gray-400 block mb-1">VKN (Vergi Kimlik No):</label>
                    <input
                      type="text"
                      placeholder="10 haneli VKN"
                      value={resForm.vknNo}
                      onChange={e => setResForm({ ...resForm, vknNo: e.target.value })}
                      className="w-full bg-brand-dark border border-brand-border rounded-xl p-2.5 text-xs text-gray-200 focus:border-gold-500"
                    />
                  </div>
                )}

                <div>
                  <label className="text-xs text-gray-400 block mb-1">Vergi Dairesi:</label>
                  <input
                    type="text"
                    placeholder="Örn: Sapanca VD"
                    value={resForm.taxOffice}
                    onChange={e => setResForm({ ...resForm, taxOffice: e.target.value })}
                    className="w-full bg-brand-dark border border-brand-border rounded-xl p-2.5 text-xs text-gray-200 focus:border-gold-500"
                  />
                </div>
              </div>
            </div>
          )}

          {/* STEP 3: Kampanya Kodu, Kapora & Özet */}
          {step === 3 && (
            <div className="space-y-4">
              <h4 className="font-heading font-bold text-sm text-gold-400">3. Kampanya, Kapora & Hesaplama Özeti</h4>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="text-xs text-gray-400 block mb-1">Referans / Kampanya Kodu:</label>
                  <input
                    type="text"
                    placeholder="Örn: IREM2026"
                    value={resForm.campaignCode}
                    onChange={e => setResForm({ ...resForm, campaignCode: e.target.value })}
                    className="w-full bg-brand-dark border border-brand-border rounded-xl p-2.5 text-xs text-gray-200 focus:border-gold-500 uppercase"
                  />
                </div>

                <div>
                  <label className="text-xs text-gray-400 block mb-1">Alınan Kapora Tutarı (TL):</label>
                  <input
                    type="number"
                    value={resForm.depositPaid}
                    onChange={e => setResForm({ ...resForm, depositPaid: Number(e.target.value) })}
                    className="w-full bg-brand-dark border border-brand-border rounded-xl p-2.5 text-xs text-gray-200 focus:border-gold-500"
                  />
                </div>
              </div>

              {/* Dynamic Price Breakdown Box */}
              <div className="bg-brand-dark p-4 rounded-2xl border border-gold-500/40 space-y-2 text-xs">
                <div className="flex justify-between text-gray-300"><span>Salon Kiralama Bedeli:</span><strong>{formatCurrency(resFormTotals.venuePrice)}</strong></div>
                <div className="flex justify-between text-gray-300"><span>Seçilen Hizmetler Toplamı:</span><strong>{formatCurrency(resFormTotals.servicesTotal)}</strong></div>
                {resFormTotals.discount > 0 && (
                  <div className="flex justify-between text-emerald-400 font-bold"><span>Kampanya İndirimi:</span><span>-{formatCurrency(resFormTotals.discount)}</span></div>
                )}
                <div className="flex justify-between text-gray-400"><span>KDV (%20 Dahil):</span><strong>{formatCurrency(resFormTotals.vat)}</strong></div>
                <div className="flex justify-between text-base font-bold text-gold-400 border-t border-brand-border pt-2">
                  <span>Genel Toplam Tutar:</span>
                  <span>{formatCurrency(resFormTotals.total)}</span>
                </div>
                <div className="flex justify-between text-emerald-400"><span>Alınan Kapora:</span><strong>{formatCurrency(resForm.depositPaid)}</strong></div>
                <div className="flex justify-between text-red-400 font-bold"><span>Kalan Ödenecek Bakiye:</span><strong>{formatCurrency(resFormTotals.remaining)}</strong></div>
              </div>
            </div>
          )}

          {/* Navigation Controls */}
          <div className="flex justify-between pt-4 border-t border-brand-border">
            {step > 1 ? (
              <button type="button" onClick={() => setStep(step - 1)} className="px-5 py-2 rounded-xl bg-brand-card text-gray-300 text-xs font-bold">
                ← Geri
              </button>
            ) : <div />}

            {step < 3 ? (
              <button type="button" onClick={() => setStep(step + 1)} className="gold-button text-gray-950 font-bold px-6 py-2 rounded-xl text-xs">
                İleri →
              </button>
            ) : (
              <button
                type="submit"
                disabled={!!collisionWarning}
                className="gold-button text-gray-950 font-bold px-8 py-2.5 rounded-xl text-xs disabled:opacity-50"
              >
                🎉 Rezervasyonu Onayla ve Kaydet
              </button>
            )}
          </div>

        </form>

      </div>
    </div>
  );
}


// ==========================================
// 13. RESERVATION DETAIL MODAL
// ==========================================
function ReservationDetailModal({ res, venues, services, onClose }) {
  const venue = venues.find(v => v.id === res.venueId);

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
      <div className="bg-brand-card border border-gold-500/40 rounded-3xl max-w-2xl w-full p-6 shadow-2xl space-y-6 max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center border-b border-brand-border pb-4">
          <div>
            <span className="font-mono text-gold-400 font-bold text-xs">{res.id}</span>
            <h3 className="text-xl font-heading font-bold text-gray-100">{res.customerName}</h3>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-white text-xl">✕</button>
        </div>

        <div className="grid grid-cols-2 gap-3 text-xs">
          <div className="bg-brand-dark p-3 rounded-xl border border-brand-border">
            <div className="text-gray-500">Düğün Salonu</div>
            <div className="font-bold text-gray-200">{venue?.name || '-'}</div>
          </div>
          <div className="bg-brand-dark p-3 rounded-xl border border-brand-border">
            <div className="text-gray-500">Tarih & Saat</div>
            <div className="font-bold text-gray-200">{formatDate(res.date)} ({res.timeSlot})</div>
          </div>
          <div className="bg-brand-dark p-3 rounded-xl border border-brand-border">
            <div className="text-gray-500">Toplam Tutar</div>
            <div className="font-bold text-gold-400">{formatCurrency(res.totalAmount)}</div>
          </div>
          <div className="bg-brand-dark p-3 rounded-xl border border-brand-border">
            <div className="text-gray-500">Kalan Bakiye</div>
            <div className="font-bold text-red-400">{formatCurrency(res.remainingBalance)}</div>
          </div>
        </div>

        <div className="space-y-2">
          <h4 className="font-heading font-bold text-xs text-gold-400 uppercase">Etkinlik Akış Planı</h4>
          <div className="space-y-1 text-xs">
            {res.flowPlan.map((item, idx) => (
              <div key={idx} className="bg-brand-dark p-2 rounded-lg border border-brand-border flex justify-between">
                <span className="font-bold text-gold-400">{item.time}</span>
                <span className="text-gray-300">{item.title}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="flex justify-end pt-4 border-t border-brand-border">
          <button onClick={onClose} className="gold-button text-gray-950 font-bold px-6 py-2 rounded-xl text-xs">
            Kapat
          </button>
        </div>
      </div>
    </div>
  );
}
