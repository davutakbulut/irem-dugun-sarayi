with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace DashboardComponent
old_dash = """    // --- 1. ANASAYFA / İSTATİSTİKLER (MODULAR DASHBOARD PAGE) ---
    function DashboardComponent(props) {
      return <DashboardPage {...props} />;
    }"""

new_dash = """    // --- 1. ANASAYFA / İSTATİSTİKLER (MODULAR DASHBOARD PAGE) ---
    function DashboardComponent(props) {
      const Comp = (typeof DashboardPage !== 'undefined' ? DashboardPage : window.DashboardPage);
      if (Comp) return <Comp {...props} />;
      const { activeRole, venues = [], reservations = [], onNewResClick, onTabChange } = props;
      const totalRevenue = reservations.reduce((acc, r) => acc + (Number(r.totalAmount) || 0), 0);
      const totalDeposit = reservations.reduce((acc, r) => acc + (Number(r.depositPaid) || 0), 0);
      const totalRemaining = reservations.reduce((acc, r) => acc + (Number(r.remainingBalance) || 0), 0);
      const upcomingCount = reservations.filter(r => r.paymentStatus !== 'İptal').length;

      return (
        <div className="space-y-6 animate-fade-in max-w-7xl mx-auto">
          <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 shadow-sm relative overflow-hidden">
            <div className="space-y-1 z-10">
              <span className="text-xs font-bold text-amber-600 dark:text-gold-400 bg-amber-500/10 px-3 py-1 rounded-full border border-amber-500/20">
                👋 Hoş Geldiniz!
              </span>
              <h2 className="text-xl sm:text-2xl font-heading font-extrabold gold-gradient-text pt-1">
                İrem Düğün Sarayı Yönetim Paneli
              </h2>
              <p className="text-xs text-slate-500 dark:text-gray-400">
                Salon dolulukları, anlık rezervasyonlar ve finansal raporları tek bakışta izleyin.
              </p>
            </div>
            <div className="flex space-x-2 z-10 w-full sm:w-auto">
              <button onClick={onNewResClick} className="w-full sm:w-auto gold-button font-bold text-xs px-4 py-2.5 rounded-xl shadow flex items-center justify-center space-x-2">
                <ThemeIcon icon="sparkles" fallbackEmoji="✨" className="w-4 h-4 shrink-0" />
                <span>Hızlı Rezervasyon Gir</span>
              </button>
            </div>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="glass-panel p-5 rounded-3xl space-y-2 border border-slate-200 dark:border-brand-border shadow-sm">
              <div className="flex justify-between items-center text-slate-500 dark:text-gray-400 text-xs font-bold">
                <span>Toplam Ciro (Sözleşmeli)</span>
                <ThemeIcon icon="money" fallbackEmoji="💰" className="w-4 h-4 text-amber-500 shrink-0" />
              </div>
              <div className="text-xl font-extrabold font-mono text-slate-800 dark:text-gray-100">
                {formatCurrency(totalRevenue)}
              </div>
              <div className="text-[10px] text-emerald-600 dark:text-emerald-400 font-bold">
                ↑ Toplam {reservations.length} Kayıtlı Etkinlik
              </div>
            </div>
            <div className="glass-panel p-5 rounded-3xl space-y-2 border border-slate-200 dark:border-brand-border shadow-sm">
              <div className="flex justify-between items-center text-slate-500 dark:text-gray-400 text-xs font-bold">
                <span>Tahsil Edilen Kaporalar</span>
                <ThemeIcon icon="money" fallbackEmoji="💳" className="w-4 h-4 text-emerald-500 shrink-0" />
              </div>
              <div className="text-xl font-extrabold font-mono text-emerald-600 dark:text-emerald-400">
                {formatCurrency(totalDeposit)}
              </div>
              <div className="text-[10px] text-slate-500 font-bold">
                Nakit & Banka Havalesi Alındı
              </div>
            </div>
            <div className="glass-panel p-5 rounded-3xl space-y-2 border border-slate-200 dark:border-brand-border shadow-sm">
              <div className="flex justify-between items-center text-slate-500 dark:text-gray-400 text-xs font-bold">
                <span>Bekleyen Alacak (Net Bakiye)</span>
                <ThemeIcon icon="clock" fallbackEmoji="⏳" className="w-4 h-4 text-amber-500 shrink-0" />
              </div>
              <div className="text-xl font-extrabold font-mono text-amber-600 dark:text-gold-400">
                {formatCurrency(totalRemaining)}
              </div>
              <div className="text-[10px] text-amber-600 font-bold">
                Etkinlik Günü Tahsil Edilecek
              </div>
            </div>
            <div className="glass-panel p-5 rounded-3xl space-y-2 border border-slate-200 dark:border-brand-border shadow-sm">
              <div className="flex justify-between items-center text-slate-500 dark:text-gray-400 text-xs font-bold">
                <span>Aktif Rezervasyonlar</span>
                <ThemeIcon icon="calendar" fallbackEmoji="📅" className="w-4 h-4 text-blue-500 shrink-0" />
              </div>
              <div className="text-xl font-extrabold text-slate-800 dark:text-gray-100">
                {upcomingCount} Adet
              </div>
              <div className="text-[10px] text-indigo-500 font-bold">
                Yaklaşan Düğün & Nişanlar
              </div>
            </div>
          </div>
          <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border space-y-4 shadow-sm">
            <div className="flex justify-between items-center border-b border-slate-200 dark:border-brand-border pb-3">
              <h3 className="font-heading font-bold text-base text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                <span>📋</span>
                <span>Son Eklenen Rezervasyonlar</span>
              </h3>
              <button onClick={() => onTabChange && onTabChange('reservations')} className="text-xs font-bold text-amber-700 dark:text-gold-400 hover:underline">
                Tümünü Gör (Takvim) →
              </button>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-200 dark:border-brand-border text-slate-500 dark:text-gray-400 font-bold">
                    <th className="py-2.5 px-3">Kod</th>
                    <th className="py-2.5 px-3">Müşteri / Çift</th>
                    <th className="py-2.5 px-3">Salon</th>
                    <th className="py-2.5 px-3">Tarih & Seans</th>
                    <th className="py-2.5 px-3">Toplam Tutar</th>
                    <th className="py-2.5 px-3">Durum</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-brand-border">
                  {reservations.slice(0, 5).map(res => {
                    const vObj = venues.find(v => v.id === res.venueId);
                    return (
                      <tr key={res.id} className="hover:bg-slate-50 dark:hover:bg-brand-dark/50 font-medium text-slate-800 dark:text-gray-200">
                        <td className="py-3 px-3 font-mono font-bold text-amber-700 dark:text-gold-400">{res.id}</td>
                        <td className="py-3 px-3 font-bold">{res.customerName}</td>
                        <td className="py-3 px-3">{vObj?.name || res.venueId}</td>
                        <td className="py-3 px-3 font-mono">{formatDate(res.eventDate)} ({res.timeSlot || 'Akşam'})</td>
                        <td className="py-3 px-3 font-mono font-bold">{formatCurrency(res.totalAmount)}</td>
                        <td className="py-3 px-3">
                          <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold ${
                            res.paymentStatus === 'Tamamlandı' ? 'bg-emerald-500/20 text-emerald-600' :
                            res.paymentStatus === 'Kapora Alındı' ? 'bg-amber-500/20 text-amber-600' :
                            'bg-slate-200 text-slate-700'
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
          </div>
        </div>
      );
    }"""

if old_dash in content:
    content = content.replace(old_dash, new_dash)
    print("✅ DashboardComponent updated with safe UMD fallback")
else:
    print("⚠️ old_dash not found exactly")

# 2. Update CreateReservationPageComponent
old_create = """    // --- 2. YENİ REZERVASYON OLUŞTUR (MODULAR CREATE RESERVATION PAGE) ---
    function CreateReservationPageComponent(props) {
      return <CreateReservationPage {...props} />;
    }"""

new_create = """    // --- 2. YENİ REZERVASYON OLUŞTUR (MODULAR CREATE RESERVATION PAGE) ---
    function CreateReservationPageComponent(props) {
      const Comp = (typeof CreateReservationPage !== 'undefined' ? CreateReservationPage : window.CreateReservationPage);
      if (Comp) return <Comp {...props} />;
      return null;
    }"""

if old_create in content:
    content = content.replace(old_create, new_create)
    print("✅ CreateReservationPageComponent updated with safe UMD fallback")

# 3. Update VenuesComponent, ServicesComponent, ReservationsComponent
old_venues = """    // --- 3. DÜĞÜN SALONLARIM (MODULAR VENUES PAGE) ---
    function VenuesComponent({ venues, onAddClick, onEditClick, onDeleteClick }) {
      return (
        <VenuesPage
          venues={venues}
          onAddVenue={onAddClick}
          onEditVenue={onEditClick}
          onDeleteVenue={onDeleteClick}
        />
      );
    }"""

new_venues = """    // --- 3. DÜĞÜN SALONLARIM (MODULAR VENUES PAGE) ---
    function VenuesComponent(props) {
      const Comp = (typeof VenuesPage !== 'undefined' ? VenuesPage : window.VenuesPage);
      if (Comp) return <Comp {...props} />;
      const { venues = [], onAddClick, onEditClick, onDeleteClick } = props;
      const onAddVenue = props.onAddVenue || onAddClick;
      const onEditVenue = props.onEditVenue || onEditClick;
      const onDeleteVenue = props.onDeleteVenue || onDeleteClick;
      return (
        <div className="space-y-6 animate-fade-in max-w-7xl mx-auto">
          <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 shadow-sm">
            <div>
              <h2 className="text-xl sm:text-2xl font-heading font-extrabold text-slate-900 dark:text-white flex items-center space-x-2">
                <ThemeIcon icon="building" fallbackEmoji="🏰" className="w-6 h-6 text-amber-500 shrink-0" />
                <span>Düğün Salonları & Kapasite Yönetimi</span>
              </h2>
              <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">Tesis bünyesindeki tüm salonları listeleyin, fiyat ve görsellerini güncelleyin.</p>
            </div>
            {onAddVenue && (
              <button onClick={onAddVenue} className="w-full sm:w-auto gold-button font-bold text-xs px-5 py-3 rounded-2xl shadow-lg flex items-center justify-center space-x-2">
                <span>➕ Yeni Salon Ekle</span>
              </button>
            )}
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {venues.map(venue => (
              <div key={venue.id} className="glass-panel rounded-3xl overflow-hidden border border-slate-200 dark:border-brand-border shadow-sm flex flex-col justify-between">
                <div className="relative h-48 overflow-hidden">
                  <OptimizedImage src={venue.image || venue.images?.[0]} alt={venue.name} className="w-full h-full object-cover" />
                  <div className="absolute top-3 left-3 bg-black/70 backdrop-blur-md text-amber-400 text-[10px] font-bold px-3 py-1 rounded-full border border-amber-500/30">
                    {venue.category}
                  </div>
                </div>
                <div className="p-5 space-y-3 flex-1 flex flex-col justify-between">
                  <div>
                    <h3 className="font-heading font-extrabold text-lg text-slate-800 dark:text-gray-100">{venue.name}</h3>
                    <p className="text-xs text-slate-500 dark:text-gray-400 line-clamp-2 mt-1">{venue.description}</p>
                  </div>
                  <div className="space-y-2 pt-3 border-t border-slate-100 dark:border-brand-border text-xs">
                    <div className="flex justify-between text-slate-600 dark:text-gray-300">
                      <span>Kapasite:</span><strong className="font-mono">{venue.capacity} Kişi</strong>
                    </div>
                    <div className="flex justify-between text-slate-600 dark:text-gray-300">
                      <span>Paket Fiyatı:</span><strong className="font-mono text-amber-700 dark:text-gold-400 font-extrabold">{formatCurrency(venue.price)}</strong>
                    </div>
                  </div>
                  <div className="flex space-x-2 pt-2">
                    {onEditVenue && <button onClick={() => onEditVenue(venue)} className="flex-1 py-2 bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 rounded-xl text-xs font-bold">Düzenle</button>}
                    {onDeleteVenue && <button onClick={() => onDeleteVenue(venue.id)} className="px-3 py-2 bg-red-500/10 text-red-500 rounded-xl text-xs font-bold">Sil</button>}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      );
    }"""

if old_venues in content:
    content = content.replace(old_venues, new_venues)
    print("✅ VenuesComponent updated with safe UMD fallback")

old_services = """    // --- 4. EK HİZMETLERİM (MODULAR SERVICES PAGE) ---
    function ServicesComponent({ services, onAddClick, onEditClick, onDeleteClick }) {
      return (
        <ServicesPage
          services={services}
          onAddService={onAddClick}
          onEditService={onEditClick}
          onDeleteService={onDeleteClick}
        />
      );
    }"""

new_services = """    // --- 4. EK HİZMETLERİM (MODULAR SERVICES PAGE) ---
    function ServicesComponent(props) {
      const Comp = (typeof ServicesPage !== 'undefined' ? ServicesPage : window.ServicesPage);
      if (Comp) return <Comp {...props} />;
      const { services = [], onAddClick, onEditClick, onDeleteClick } = props;
      const onAddService = props.onAddService || onAddClick;
      const onEditService = props.onEditService || onEditClick;
      const onDeleteService = props.onDeleteService || onDeleteClick;
      return (
        <div className="space-y-6 animate-fade-in max-w-7xl mx-auto">
          <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 shadow-sm">
            <div>
              <h2 className="text-xl sm:text-2xl font-heading font-extrabold text-slate-900 dark:text-white flex items-center space-x-2">
                <ThemeIcon icon="sparkles" fallbackEmoji="✨" className="w-6 h-6 text-amber-500 shrink-0" />
                <span>Ek Hizmetler & Paket Kataloğu</span>
              </h2>
              <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">Düğün organizasyonuna eklenebilecek ekstra paket ve servis yönetimi.</p>
            </div>
            {onAddService && (
              <button onClick={onAddService} className="w-full sm:w-auto gold-button font-bold text-xs px-5 py-3 rounded-2xl shadow-lg flex items-center justify-center space-x-2">
                <span>➕ Yeni Hizmet Ekle</span>
              </button>
            )}
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {services.map(serv => (
              <div key={serv.id} className="glass-panel p-5 rounded-3xl border border-slate-200 dark:border-brand-border shadow-sm flex flex-col justify-between space-y-4">
                <div className="flex items-start justify-between">
                  <div className="w-10 h-10 rounded-2xl bg-amber-500/10 text-amber-600 dark:text-gold-400 font-extrabold flex items-center justify-center text-lg">
                    ✨
                  </div>
                  <span className="text-[10px] font-bold px-2.5 py-1 rounded-full bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-300">
                    {serv.category}
                  </span>
                </div>
                <div>
                  <h3 className="font-heading font-extrabold text-base text-slate-800 dark:text-gray-100">{serv.name}</h3>
                  <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">{serv.description}</p>
                </div>
                <div className="flex justify-between items-center pt-3 border-t border-slate-100 dark:border-brand-border text-xs">
                  <span className="text-slate-500">Birim Fiyat:</span>
                  <strong className="font-mono text-amber-700 dark:text-gold-400 font-extrabold text-sm">{formatCurrency(serv.price)}</strong>
                </div>
                <div className="flex space-x-2 pt-1">
                  {onEditService && <button onClick={() => onEditService(serv)} className="flex-1 py-2 bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 rounded-xl text-xs font-bold">Düzenle</button>}
                  {onDeleteService && <button onClick={() => onDeleteService(serv.id)} className="px-3 py-2 bg-red-500/10 text-red-500 rounded-xl text-xs font-bold">Sil</button>}
                </div>
              </div>
            ))}
          </div>
        </div>
      );
    }"""

if old_services in content:
    content = content.replace(old_services, new_services)
    print("✅ ServicesComponent updated with safe UMD fallback")

old_res = """    // --- 5. REZERVASYONLARIM & MASTER TAKVİM (MODULAR RESERVATIONS LIST PAGE) ---
    function ReservationsComponent(props) {
      return <ReservationsListPage {...props} />;
    }"""

new_res = """    // --- 5. REZERVASYONLARIM & MASTER TAKVİM (MODULAR RESERVATIONS LIST PAGE) ---
    function ReservationsComponent(props) {
      const Comp = (typeof ReservationsListPage !== 'undefined' ? ReservationsListPage : window.ReservationsListPage);
      if (Comp) return <Comp {...props} />;
      return null;
    }"""

if old_res in content:
    content = content.replace(old_res, new_res)
    print("✅ ReservationsComponent updated with safe UMD fallback")

# 4. Update CampaignsComponent, ReportsComponent, CustomersComponent, UsersComponent, SettingsComponent
old_camp = """    // --- 6. KAMPANYALAR (MODULAR CAMPAIGNS PAGE) ---
    function CampaignsComponent({ campaigns = [], onAddClick, onEditClick }) {
      return (
        <CampaignsPage
          campaigns={campaigns}
          onAddCampaign={onAddClick}
          onEditCampaign={onEditClick}
        />
      );
    }"""

new_camp = """    // --- 6. KAMPANYALAR (MODULAR CAMPAIGNS PAGE) ---
    function CampaignsComponent(props) {
      const Comp = (typeof CampaignsPage !== 'undefined' ? CampaignsPage : window.CampaignsPage);
      if (Comp) return <Comp {...props} />;
      const { campaigns = [], onAddClick, onEditClick } = props;
      const onAddCampaign = props.onAddCampaign || onAddClick;
      const onEditCampaign = props.onEditCampaign || onEditClick;
      return (
        <div className="space-y-6 animate-fade-in max-w-7xl mx-auto">
          <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 shadow-sm">
            <div>
              <h2 className="text-xl sm:text-2xl font-heading font-extrabold text-slate-900 dark:text-white flex items-center space-x-2">
                <ThemeIcon icon="gift" fallbackEmoji="🎁" className="w-6 h-6 text-amber-500 shrink-0" />
                <span>Özel Kampanyalar & İndirim Kodları</span>
              </h2>
              <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">Sezonluk düğün indirimleri ve kampanya promosyon yönetimi.</p>
            </div>
            {onAddCampaign && (
              <button onClick={onAddCampaign} className="w-full sm:w-auto gold-button font-bold text-xs px-5 py-3 rounded-2xl shadow-lg flex items-center justify-center space-x-2">
                <span>➕ Yeni Kampanya Ekle</span>
              </button>
            )}
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {campaigns.map(camp => (
              <div key={camp.id} className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border shadow-sm space-y-4">
                <div className="flex justify-between items-center">
                  <span className="font-mono font-extrabold text-amber-700 dark:text-gold-400 bg-amber-500/10 px-3 py-1 rounded-xl text-xs border border-amber-500/20">{camp.code}</span>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-emerald-500/10 text-emerald-600">{camp.status || 'Aktif'}</span>
                </div>
                <div>
                  <h3 className="font-heading font-bold text-base text-slate-800 dark:text-gray-100">{camp.title}</h3>
                  <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">{camp.description}</p>
                </div>
                {onEditCampaign && (
                  <button onClick={() => onEditCampaign(camp)} className="w-full py-2 bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 rounded-xl text-xs font-bold">Düzenle</button>
                )}
              </div>
            ))}
          </div>
        </div>
      );
    }"""

if old_camp in content:
    content = content.replace(old_camp, new_camp)
    print("✅ CampaignsComponent updated with safe UMD fallback")

old_rep = """    // --- 7. FİNANSAL RAPORLAR & AI ANALİZLER (MODULAR REPORTS PAGE) ---
    function ReportsComponent({ reservations = [], venues = [], onConvertToCampaign }) {
      return (
        <ReportsPage
          reservations={reservations}
          venues={venues}
          onConvertToCampaign={onConvertToCampaign}
        />
      );
    }"""

new_rep = """    // --- 7. FİNANSAL RAPORLAR & AI ANALİZLER (MODULAR REPORTS PAGE) ---
    function ReportsComponent(props) {
      const Comp = (typeof ReportsPage !== 'undefined' ? ReportsPage : window.ReportsPage);
      if (Comp) return <Comp {...props} />;
      return (
        <div className="space-y-6 max-w-7xl mx-auto">
          <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border shadow-sm">
            <h2 className="text-xl sm:text-2xl font-heading font-extrabold text-slate-900 dark:text-white flex items-center space-x-2">
              <ThemeIcon icon="chart" fallbackEmoji="📊" className="w-6 h-6 text-amber-500 shrink-0" />
              <span>Finansal Raporlar & Yapay Zeka Analizi</span>
            </h2>
            <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">İşletme performansı ve rezervasyon istatistikleri.</p>
          </div>
        </div>
      );
    }"""

if old_rep in content:
    content = content.replace(old_rep, new_rep)
    print("✅ ReportsComponent updated with safe UMD fallback")

old_cust = """    // --- 8. MÜŞTERİ REHBERİ (MODULAR CUSTOMERS PAGE) ---
    function CustomersComponent({ customers = [], onAddClick, onEditClick }) {
      return (
        <CustomersPage
          customers={customers}
          onAddCustomer={onAddClick}
          onEditCustomer={onEditClick}
        />
      );
    }"""

new_cust = """    // --- 8. MÜŞTERİ REHBERİ (MODULAR CUSTOMERS PAGE) ---
    function CustomersComponent(props) {
      const Comp = (typeof CustomersPage !== 'undefined' ? CustomersPage : window.CustomersPage);
      if (Comp) return <Comp {...props} />;
      const { customers = [], onAddClick, onEditClick } = props;
      const onAddCustomer = props.onAddCustomer || onAddClick;
      const onEditCustomer = props.onEditCustomer || onEditClick;
      return (
        <div className="space-y-6 animate-fade-in max-w-7xl mx-auto">
          <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 shadow-sm">
            <div>
              <h2 className="text-xl sm:text-2xl font-heading font-extrabold text-slate-900 dark:text-white flex items-center space-x-2">
                <ThemeIcon icon="user" fallbackEmoji="👥" className="w-6 h-6 text-amber-500 shrink-0" />
                <span>Müşteri Rehberi & İletişim Kartları</span>
              </h2>
              <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">Kayıtlı tüm gelin, damat ve çiftlerin rehber bilgileri.</p>
            </div>
            {onAddCustomer && (
              <button onClick={onAddCustomer} className="w-full sm:w-auto gold-button font-bold text-xs px-5 py-3 rounded-2xl shadow-lg flex items-center justify-center space-x-2">
                <span>➕ Yeni Müşteri Ekle</span>
              </button>
            )}
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {customers.map(c => (
              <div key={c.id} className="glass-panel p-5 rounded-3xl border border-slate-200 dark:border-brand-border shadow-sm flex items-center justify-between">
                <div>
                  <h3 className="font-heading font-bold text-sm text-slate-800 dark:text-gray-100">{c.name}</h3>
                  <p className="text-xs font-mono text-slate-500 dark:text-gray-400 mt-0.5">{c.phone}</p>
                </div>
                {onEditCustomer && <button onClick={() => onEditCustomer(c)} className="px-3 py-1.5 bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 rounded-xl text-xs font-bold">Düzenle</button>}
              </div>
            ))}
          </div>
        </div>
      );
    }"""

if old_cust in content:
    content = content.replace(old_cust, new_cust)
    print("✅ CustomersComponent updated with safe UMD fallback")

old_users = """    // --- 9. KULLANICI YÖNETİMİ (MODULAR USERS PAGE) ---
    function UsersComponent({ users = [], onAddClick, onEditClick }) {
      return (
        <UsersPage
          users={users}
          onAddUser={onAddClick}
          onEditUser={onEditClick}
        />
      );
    }"""

new_users = """    // --- 9. KULLANICI YÖNETİMİ (MODULAR USERS PAGE) ---
    function UsersComponent(props) {
      const Comp = (typeof UsersPage !== 'undefined' ? UsersPage : window.UsersPage);
      if (Comp) return <Comp {...props} />;
      const { users = [], onAddClick, onEditClick } = props;
      const onAddUser = props.onAddUser || onAddClick;
      const onEditUser = props.onEditUser || onEditClick;
      return (
        <div className="space-y-6 animate-fade-in max-w-7xl mx-auto">
          <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 shadow-sm">
            <div>
              <h2 className="text-xl sm:text-2xl font-heading font-extrabold text-slate-900 dark:text-white flex items-center space-x-2">
                <ThemeIcon icon="shield" fallbackEmoji="🛡️" className="w-6 h-6 text-amber-500 shrink-0" />
                <span>Sistem Kullanıcıları & Yetki Yönetimi</span>
              </h2>
              <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">Personel, satış temsilcileri ve yönetici hesapları.</p>
            </div>
            {onAddUser && (
              <button onClick={onAddUser} className="w-full sm:w-auto gold-button font-bold text-xs px-5 py-3 rounded-2xl shadow-lg flex items-center justify-center space-x-2">
                <span>➕ Yeni Kullanıcı Ekle</span>
              </button>
            )}
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {users.map(u => (
              <div key={u.id} className="glass-panel p-5 rounded-3xl border border-slate-200 dark:border-brand-border shadow-sm flex items-center justify-between">
                <div>
                  <h3 className="font-heading font-bold text-sm text-slate-800 dark:text-gray-100">{u.name}</h3>
                  <p className="text-xs text-amber-700 dark:text-gold-400 font-bold mt-0.5">{u.role}</p>
                </div>
                {onEditUser && <button onClick={() => onEditUser(u)} className="px-3 py-1.5 bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 rounded-xl text-xs font-bold">Düzenle</button>}
              </div>
            ))}
          </div>
        </div>
      );
    }"""

if old_users in content:
    content = content.replace(old_users, new_users)
    print("✅ UsersComponent updated with safe UMD fallback")

old_set = """    // --- 10. GÖRÜNÜM & TEMA AYARLARI (MODULAR SETTINGS PAGE) ---
    function SettingsComponent({ themeColor, onThemeColorChange, onNavigate }) {
      return (
        <SettingsPage
          currentTheme={themeColor}
          onThemeChange={onThemeColorChange}
          onNavigate={onNavigate}
        />
      );
    }"""

new_set = """    // --- 10. GÖRÜNÜM & TEMA AYARLARI (MODULAR SETTINGS PAGE) ---
    function SettingsComponent(props) {
      const Comp = (typeof SettingsPage !== 'undefined' ? SettingsPage : window.SettingsPage);
      if (Comp) return <Comp {...props} />;
      return (
        <div className="space-y-6 max-w-4xl mx-auto">
          <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border shadow-sm">
            <h2 className="text-xl sm:text-2xl font-heading font-extrabold text-slate-900 dark:text-white flex items-center space-x-2">
              <ThemeIcon icon="cog" fallbackEmoji="⚙️" className="w-6 h-6 text-amber-500 shrink-0" />
              <span>Görünüm & Tema Ayarları</span>
            </h2>
            <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">Uygulama renk paleti ve tema ayarları.</p>
          </div>
        </div>
      );
    }"""

if old_set in content:
    content = content.replace(old_set, new_set)
    print("✅ SettingsComponent updated with safe UMD fallback")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("🎉 index.html updated successfully with safe UMD fallbacks!")
