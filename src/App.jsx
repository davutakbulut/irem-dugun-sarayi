import React, { useState, useEffect, useMemo } from 'react';
import {
  ROLE_NAMES,
  TAB_TO_SLUG,
  SLUG_TO_TAB,
  INITIAL_TAB_PERMISSIONS,
  INITIAL_VENUES,
  INITIAL_SERVICES,
  INITIAL_CAMPAIGNS,
  INITIAL_USERS,
  INITIAL_RESERVATIONS,
  INITIAL_CUSTOMERS,
  AI_RECOMMENDATIONS
} from './constants';

import { HeaderComponent, SidebarComponent } from './components/Navigation';
import MobileDrawer from './components/MobileDrawer';
import { ToastNotification } from './components/CommonUI';

import DashboardPageComponent from './pages/DashboardPage';
import CreateReservationPageComponent from './pages/CreateReservationPage';
import VenuesPageComponent from './pages/VenuesPage';
import ServicesPageComponent from './pages/ServicesPage';
import ReservationsPageComponent from './pages/ReservationsPage';
import CalendarPageComponent from './pages/CalendarPage';
import CampaignsPageComponent from './pages/CampaignsPage';
import FinancePageComponent from './pages/FinancePage';
import CustomersPageComponent from './pages/CustomersPage';
import UsersPageComponent from './pages/UsersPage';
import ReportsPageComponent from './pages/ReportsPage';
import MediaPageComponent from './pages/MediaPage';
import ProfilePageComponent from './pages/ProfilePage';
import SettingsPageComponent from './pages/SettingsPage';

import {
  VenueModalComponent,
  ServiceModalComponent,
  CampaignModalComponent,
  UserModalComponent,
  CustomerFormModal,
  ReservationDetailModal,
  EmailNotificationModal
} from './components/Modals';

export default function App() {
  const [theme, setTheme] = useState('light');
  const [activePalette, setActivePalette] = useState('gold');
  const [activeRole, setActiveRole] = useState('admin');
  const [rolesState, setRolesState] = useState(ROLE_NAMES);
  const [tabPermissionsState, setTabPermissionsState] = useState(INITIAL_TAB_PERMISSIONS);
  const [isCacheEnabled, setIsCacheEnabled] = useState(true);
  const [toastMessage, setToastMessage] = useState('');
  const [isToastVisible, setIsToastVisible] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const [activeTab, setActiveTab] = useState('dashboard');

  const [venues, setVenues] = useState(INITIAL_VENUES);
  const [services, setServices] = useState(INITIAL_SERVICES);
  const [campaigns, setCampaigns] = useState(INITIAL_CAMPAIGNS);
  const [users, setUsers] = useState(INITIAL_USERS);
  const [reservations, setReservations] = useState(INITIAL_RESERVATIONS);
  const [customers, setCustomers] = useState(INITIAL_CUSTOMERS);

  const [venueModalData, setVenueModalData] = useState(null);
  const [serviceModalData, setServiceModalData] = useState(null);
  const [campaignModalData, setCampaignModalData] = useState(null);
  const [userModalData, setUserModalData] = useState(null);
  const [customerModalData, setCustomerModalData] = useState(null);
  const [emailModalData, setEmailModalData] = useState(null);
  const [selectedResForDetail, setSelectedResForDetail] = useState(null);

  const [resSearchQuery, setResSearchQuery] = useState('');
  const [resStatusFilter, setResStatusFilter] = useState('ALL');

  const showToast = (msg) => {
    setToastMessage(msg);
    setIsToastVisible(true);
    setTimeout(() => setIsToastVisible(false), 3000);
  };

  useEffect(() => {
    const handleHashChange = () => {
      const hash = window.location.hash.replace('#/', '');
      if (hash && SLUG_TO_TAB[hash]) {
        setActiveTab(SLUG_TO_TAB[hash]);
      } else if (!hash) {
        setActiveTab('dashboard');
      }
    };

    window.addEventListener('hashchange', handleHashChange);
    handleHashChange();
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  const navigateTo = (tabId) => {
    setActiveTab(tabId);
    if (TAB_TO_SLUG[tabId]) {
      window.location.hash = `#/${TAB_TO_SLUG[tabId]}`;
    }
  };

  const handleSaveVenue = (venue) => {
    setVenues(prev => venue.id ? prev.map(v => v.id === venue.id ? venue : v) : [...prev, venue]);
    showToast('🏛️ Düğün Salonu Başarıyla Kaydedildi!');
    setVenueModalData(null);
  };

  const handleDeleteVenue = (id) => {
    if (confirm('Bu düğün salonunu silmek istediğinize emin misiniz?')) {
      setVenues(prev => prev.filter(v => v.id !== id));
      showToast('🗑️ Düğün Salonu Silindi.');
    }
  };

  const handleSaveService = (service) => {
    setServices(prev => service.id ? prev.map(s => s.id === service.id ? service : s) : [...prev, service]);
    showToast('✨ Ek Hizmet Başarıyla Kaydedildi!');
    setServiceModalData(null);
  };

  const handleDeleteService = (id) => {
    if (confirm('Bu ek hizmeti silmek istediğinize emin misiniz?')) {
      setServices(prev => prev.filter(s => s.id !== id));
      showToast('🗑️ Ek Hizmet Silindi.');
    }
  };

  const handleSaveCampaign = (campaign) => {
    setCampaigns(prev => campaign.id ? prev.map(c => c.id === campaign.id ? campaign : c) : [...prev, campaign]);
    showToast('🎁 Kampanya Başarıyla Kaydedildi!');
    setCampaignModalData(null);
  };

  const handleDeleteCampaign = (id) => {
    if (confirm('Bu kampanyayı silmek istediğinize emin misiniz?')) {
      setCampaigns(prev => prev.filter(c => c.id !== id));
      showToast('🗑️ Kampanya Silindi.');
    }
  };

  const handleAddCampaignFromAI = (aiCampaign) => {
    setCampaigns(prev => [aiCampaign, ...prev]);
  };

  const handleSaveUser = (user) => {
    setUsers(prev => user.id ? prev.map(u => u.id === user.id ? user : u) : [...prev, user]);
    showToast('⚙️ Kullanıcı Hesabı Başarıyla Kaydedildi!');
    setUserModalData(null);
  };

  const handleDeleteUser = (id) => {
    if (confirm('Bu kullanıcıyı silmek istediğinize emin misiniz?')) {
      setUsers(prev => prev.filter(u => u.id !== id));
      showToast('🗑️ Kullanıcı Silindi.');
    }
  };

  const handleDeleteCustomer = (id) => {
    if (confirm('Bu müşteri kartını silmek istediğinize emin misiniz?')) {
      setCustomers(prev => prev.filter(c => c.id !== id));
      showToast('🗑️ Müşteri Kartı Silindi.');
    }
  };

  const handleRescheduleReservation = (resId, newDate) => {
    setReservations(prev => prev.map(r => r.id === resId ? { ...r, date: newDate } : r));
    showToast(`📅 Rezervasyon Tarihi Güncellendi: ${newDate}`);
  };

  const handlePrintInvoice = (res) => {
    alert(`📄 REZERVASYON FATURASI & SÖZLEŞMESİ YAZDIRILIYOR\n-----------------------------------\nSözleşme No: ${res.id}\nMüşteri: ${res.customerName}\nToplam Tutar: ${res.totalAmount} ₺\nTahsil Kaparo: ${res.depositPaid} ₺`);
  };

  const financialStats = useMemo(() => {
    const totalRev = reservations.reduce((sum, r) => sum + r.totalAmount, 0);
    const totalDep = reservations.reduce((sum, r) => sum + r.depositPaid, 0);
    const remaining = Math.max(0, totalRev - totalDep);
    return { totalRevenue: totalRev, totalDeposit: totalDep, remainingBalance: remaining, activeReservationsCount: reservations.length };
  }, [reservations]);

  const filteredReservations = useMemo(() => {
    return reservations.filter(r => {
      const matchSearch = r.customerName.toLowerCase().includes(resSearchQuery.toLowerCase()) || r.id.toLowerCase().includes(resSearchQuery.toLowerCase());
      const matchStatus = resStatusFilter === 'ALL' || r.paymentStatus === resStatusFilter;
      return matchSearch && matchStatus;
    });
  }, [reservations, resSearchQuery, resStatusFilter]);

  const isTabAllowed = useMemo(() => {
    const allowedRoles = tabPermissionsState[activeTab.split('-')[0]] || [];
    return allowedRoles.includes(activeRole);
  }, [activeTab, tabPermissionsState, activeRole]);

  return (
    <div className={`min-h-screen transition-colors duration-300 ${theme === 'dark' ? 'dark bg-brand-dark text-gray-100' : 'bg-slate-50 text-slate-900'}`}>
      
      <HeaderComponent
        activeRole={activeRole}
        rolesState={rolesState}
        onRoleChange={setActiveRole}
        theme={theme}
        onToggleTheme={() => setTheme(prev => prev === 'dark' ? 'light' : 'dark')}
        activePalette={activePalette}
        onSelectPalette={setActivePalette}
        isMobileMenuOpen={isMobileMenuOpen}
        setIsMobileMenuOpen={setIsMobileMenuOpen}
        navigateTo={navigateTo}
      />

      <div className="max-w-7xl mx-auto flex pt-4 px-4 pb-24 lg:pb-8">
        
        <SidebarComponent
          activeTab={activeTab}
          activeRole={activeRole}
          tabPermissionsState={tabPermissionsState}
          navigateTo={navigateTo}
        />

        <main className="flex-1 lg:pl-6">
          {!isTabAllowed ? (
            <div className="glass-panel p-8 max-w-lg mx-auto mt-12 rounded-3xl text-center space-y-4 border border-red-500/40 shadow-2xl">
              <div className="text-5xl">🚫</div>
              <h2 className="text-xl font-bold text-slate-800 dark:text-gray-100">Bu Sayfaya Erişim Yetkiniz Bulunmamaktadır</h2>
              <p className="text-xs text-slate-500 dark:text-gray-400">Mevcut rolünüz ({ROLE_NAMES[activeRole]}) bu modüle erişim sağlama yetkisine sahip değildir.</p>
              <button onClick={() => navigateTo('dashboard')} className="gold-button font-bold px-6 py-2.5 rounded-xl text-xs">Anasayfaya Dön</button>
            </div>
          ) : (
            <>
              {activeTab === 'dashboard' && (
                <DashboardPageComponent
                  stats={financialStats}
                  reservations={reservations}
                  venues={venues}
                  services={services}
                  onNewResClick={() => navigateTo('create-reservation')}
                  onDetailClick={setSelectedResForDetail}
                  navigateTo={navigateTo}
                />
              )}

              {activeTab === 'create-reservation' && (
                <CreateReservationPageComponent
                  venues={venues}
                  services={services}
                  campaigns={campaigns}
                  customers={customers}
                  onSaveReservation={r => setReservations(prev => [...prev, r])}
                  showToast={showToast}
                  navigateTo={navigateTo}
                />
              )}

              {activeTab === 'venues' && (
                <VenuesPageComponent
                  venues={venues}
                  onAddClick={() => setVenueModalData('new')}
                  onEditClick={v => setVenueModalData(v)}
                  onDeleteClick={handleDeleteVenue}
                />
              )}

              {activeTab === 'services' && (
                <ServicesPageComponent
                  services={services}
                  onAddClick={() => setServiceModalData('new')}
                  onEditClick={s => setServiceModalData(s)}
                  onDeleteClick={handleDeleteService}
                />
              )}

              {activeTab === 'reservations' && (
                <ReservationsPageComponent
                  reservations={filteredReservations}
                  venues={venues}
                  searchQuery={resSearchQuery}
                  setSearchQuery={setResSearchQuery}
                  statusFilter={resStatusFilter}
                  setStatusFilter={setResStatusFilter}
                  onNewResClick={() => navigateTo('create-reservation')}
                  onDetailClick={setSelectedResForDetail}
                />
              )}

              {activeTab === 'calendar' && (
                <CalendarPageComponent
                  reservations={reservations}
                  venues={venues}
                  onResClick={setSelectedResForDetail}
                  onReschedule={handleRescheduleReservation}
                />
              )}

              {activeTab === 'campaigns' && (
                <CampaignsPageComponent
                  campaigns={campaigns}
                  onAddClick={() => setCampaignModalData('new')}
                  onEditClick={c => setCampaignModalData(c)}
                  onDeleteClick={handleDeleteCampaign}
                />
              )}

              {activeTab === 'finance' && (
                <FinancePageComponent
                  financialStats={financialStats}
                  reservations={reservations}
                />
              )}

              {activeTab === 'customers' && (
                <CustomersPageComponent
                  customers={customers}
                  onAddClick={() => setCustomerModalData('new')}
                  onEditClick={c => setCustomerModalData(c)}
                  onDeleteClick={handleDeleteCustomer}
                />
              )}

              {activeTab === 'users' && (
                <UsersPageComponent
                  users={users}
                  onAddClick={() => setUserModalData('new')}
                  onEditClick={u => setUserModalData(u)}
                  onDeleteClick={handleDeleteUser}
                />
              )}

              {activeTab === 'reports' && (
                <ReportsPageComponent
                  reservations={reservations}
                  aiRecommendations={AI_RECOMMENDATIONS}
                  onAddCampaignFromAI={handleAddCampaignFromAI}
                  showToast={showToast}
                  navigateTo={navigateTo}
                />
              )}

              {activeTab === 'media' && (
                <MediaPageComponent
                  reservations={reservations}
                  showToast={showToast}
                />
              )}

              {activeTab === 'profile' && (
                <ProfilePageComponent
                  currentUser={{ name: 'İrem Yılmaz', email: 'admin@iremdugunsarayi.com', phone: '+90 532 000 0000', avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80' }}
                  activeRole={activeRole}
                  onSaveProfile={() => showToast('👤 Profil Bilgileri Başarıyla Güncellendi!')}
                  showToast={showToast}
                  onRoleChange={setActiveRole}
                />
              )}

              {activeTab.startsWith('settings') && (
                <SettingsPageComponent
                  activeRole={activeRole}
                  rolesState={rolesState}
                  tabPermissionsState={tabPermissionsState}
                  onTogglePermission={(tab, role) => {
                    setTabPermissionsState(prev => {
                      const current = prev[tab] || [];
                      const updated = current.includes(role) ? current.filter(r => r !== role) : [...current, role];
                      return { ...prev, [tab]: updated };
                    });
                    showToast('🛡️ Rol Erişimi Güncellendi');
                  }}
                  isCacheEnabled={isCacheEnabled}
                  onToggleCache={setIsCacheEnabled}
                  showToast={showToast}
                  activePalette={activePalette}
                  onSelectPalette={setActivePalette}
                  initialSubTab={activeTab === 'settings-appearance' ? 'appearance' : activeTab === 'settings-performance' ? 'performance' : activeTab === 'settings-rbac' ? 'rbac' : 'appearance'}
                />
              )}
            </>
          )}
        </main>
      </div>

      <MobileDrawer
        isOpen={isMobileMenuOpen}
        onClose={() => setIsMobileMenuOpen(false)}
        activeTab={activeTab}
        activeRole={activeRole}
        tabPermissionsState={tabPermissionsState}
        navigateTo={navigateTo}
      />

      {venueModalData && <VenueModalComponent venue={venueModalData === 'new' ? null : venueModalData} onClose={() => setVenueModalData(null)} onSave={handleSaveVenue} />}
      {serviceModalData && <ServiceModalComponent service={serviceModalData === 'new' ? null : serviceModalData} onClose={() => setServiceModalData(null)} onSave={handleSaveService} />}
      {campaignModalData && <CampaignModalComponent campaign={campaignModalData === 'new' ? null : campaignModalData} onClose={() => setCampaignModalData(null)} onSave={handleSaveCampaign} />}
      {userModalData && <UserModalComponent user={userModalData === 'new' ? null : userModalData} onClose={() => setUserModalData(null)} onSave={handleSaveUser} />}
      {customerModalData && <CustomerFormModal customer={customerModalData === 'new' ? null : customerModalData} onClose={() => setCustomerModalData(null)} onSave={c => { setCustomers(prev => [...prev, c]); setCustomerModalData(null); showToast('👤 Müşteri Kaydedildi!'); }} />}
      {selectedResForDetail && (
        <ReservationDetailModal
          res={selectedResForDetail}
          venues={venues}
          services={services}
          onClose={() => setSelectedResForDetail(null)}
          onPrintInvoice={() => handlePrintInvoice(selectedResForDetail)}
          onShowEmail={(r) => setEmailModalData({ to: r.customerEmail || 'musteri@example.com', name: r.customerName, subject: 'Rezervasyonunuz Oluşturuldu!', type: 'reservation', res: r })}
          onUpdatePayment={(id, dep, stat) => {
            setReservations(prev => prev.map(r => r.id === id ? { ...r, depositPaid: dep, remainingBalance: Math.max(0, r.totalAmount - dep), paymentStatus: stat } : r));
            showToast('💳 Ödeme & Sözleşme Güncellendi!');
            setSelectedResForDetail(null);
          }}
        />
      )}
      {emailModalData && <EmailNotificationModal emailData={emailModalData} onClose={() => setEmailModalData(null)} />}

      <ToastNotification message={toastMessage} isVisible={isToastVisible} onClose={() => setIsToastVisible(false)} />
    </div>
  );
}
