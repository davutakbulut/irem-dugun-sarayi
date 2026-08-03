import React, { useState, useEffect } from 'react';
import { SidebarComponent, HeaderComponent } from './components/Navigation';
import { MobileBottomSummaryBar } from './components/MobileBottomSummaryBar';
import { NotificationPopup } from './components/NotificationPopup';
import { PageErrorBoundary } from './components/PageErrorBoundary';

// Data & Pages
import {
  INITIAL_VENUES,
  INITIAL_SERVICES,
  INITIAL_CUSTOMERS,
  INITIAL_RESERVATIONS,
  INITIAL_CAMPAIGNS,
  INITIAL_USERS,
  INITIAL_SYSTEM_LOGS
} from './constants/mockData';

import { DashboardComponent as DashboardPage } from './pages/DashboardPage';
import { CreateReservationPageComponent as CreateReservationPage } from './pages/CreateReservationPage';
import { ReservationsListComponent as ReservationsListPage } from './pages/ReservationsListPage';
import { CalendarComponent as CalendarPage } from './pages/CalendarPage';
import { FinanceComponent as FinancePage } from './pages/FinancePage';
import { CustomersComponent as CustomersPage } from './pages/CustomersPage';
import { CampaignsComponent as CampaignsPage } from './pages/CampaignsPage';
import { ReportsComponent as ReportsPage } from './pages/ReportsPage';
import { SettingsComponent as SettingsPage } from './pages/SettingsPage';
import { VenuesComponent as VenuesPage } from './pages/VenuesPage';
import { ServicesComponent as ServicesPage } from './pages/ServicesPage';
import { UsersComponent as UsersPage } from './pages/UsersPage';
import { MediaComponent as MediaPage } from './pages/MediaPage';
import { ProfileComponent as ProfilePage } from './pages/ProfilePage';
import { MindMapPageComponent as MindMapPage } from './pages/MindMapPage';
import { Page404, Page301, Page403, Page500 } from './pages/ErrorPages';

export default function App() {
  // Global State
  const [activeTab, setActiveTab] = useState(() => {
    const hash = window.location.hash.replace('#/', '').replace('#', '').split('?')[0];
    if (hash === 'zihin-haritasi' || hash === 'mind-map') return 'mind-map';
    return 'create-reservation';
  });
  const [activeRole, setActiveRole] = useState('SuperAdmin');
  const [currentTheme, setCurrentTheme] = useState('obsidian-gold');
  const [currentUser, setCurrentUser] = useState({
    id: 'u-admin',
    name: 'Davut Akbulut',
    email: 'davut@iremdugunsarayi.com',
    phone: '+90 532 123 4567',
    avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'
  });

  const [venues, setVenues] = useState(INITIAL_VENUES);
  const [services, setServices] = useState(INITIAL_SERVICES);
  const [customers, setCustomers] = useState(INITIAL_CUSTOMERS);
  const [reservations, setReservations] = useState(INITIAL_RESERVATIONS);
  const [campaigns, setCampaigns] = useState(INITIAL_CAMPAIGNS);
  const [users, setUsers] = useState(INITIAL_USERS);
  const [systemLogs, setSystemLogs] = useState(INITIAL_SYSTEM_LOGS);

  // Standalone Top-Right Floating Notification Modal State
  const [alertModal, setAlertModal] = useState({
    isOpen: false,
    title: '',
    message: ''
  });

  const showAlert = (title, message) => {
    setAlertModal({ isOpen: true, title, message });
  };

  const closeAlert = () => {
    setAlertModal({ isOpen: false, title: '', message: '' });
  };

  // Sync Theme Attributes
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', currentTheme);
    if (currentTheme === 'platinum-silver') {
      document.documentElement.classList.remove('dark');
    } else {
      document.documentElement.classList.add('dark');
    }
  }, [currentTheme]);

  // Sync Hash Route Changes
  useEffect(() => {
    const handleHashChange = () => {
      const hash = window.location.hash.replace('#/', '').replace('#', '').split('?')[0];
      if (hash === 'zihin-haritasi' || hash === 'mind-map' || hash === 'zihinharitasi') {
        setActiveTab('mind-map');
      } else if (hash === 'anasayfa') {
        setActiveTab('dashboard');
      } else if (hash === 'yeni-rezervasyon' || hash === 'rezervasyon-olustur') {
        setActiveTab('create-reservation');
      } else if (hash === 'dugun-salonlari') {
        setActiveTab('venues');
      } else if (hash === 'ek-hizmetler') {
        setActiveTab('services');
      } else if (hash === 'rezervasyonlar') {
        setActiveTab('reservations');
      } else if (hash === 'takvim') {
        setActiveTab('calendar');
      } else if (hash === 'kampanyalar') {
        setActiveTab('campaigns');
      } else if (hash === 'finans') {
        setActiveTab('finance');
      } else if (hash === 'musteri-rehberi') {
        setActiveTab('customers');
      } else if (hash === 'kullanici-yonetimi') {
        setActiveTab('users');
      } else if (hash === 'raporlar-ai') {
        setActiveTab('reports');
      } else if (hash === 'medya-yukle') {
        setActiveTab('media');
      } else if (hash === 'profil') {
        setActiveTab('profile');
      } else if (hash.startsWith('ayarlar')) {
        setActiveTab(hash.replace('/', '-'));
      }
    };
    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  // Reservation Handlers
  const handleSaveReservation = (newRes, newCustObj) => {
    if (newCustObj) {
      setCustomers(prev => [newCustObj, ...prev]);
    }
    setReservations(prev => [newRes, ...prev]);
    showAlert('🎉 REZERVASYON VE SÖZLEŞME OLUŞTURULDU!', `${newRes.customerName} için ${newRes.id} sözleşme koduyla rezervasyon başarıyla kaydedildi.`);
    setActiveTab('reservations');
  };

  const handleUpdateReservation = (updatedRes) => {
    setReservations(prev => prev.map(r => r.id === updatedRes.id ? updatedRes : r));
    showAlert('✏️ REZERVASYON GÜNCELLENDİ!', `${updatedRes.customerName} için ${updatedRes.id} sözleşme kayıtları güncellendi.`);
  };

  const handleDeleteReservation = (resId) => {
    setReservations(prev => prev.filter(r => r.id !== resId));
    showAlert('🗑️ REZERVASYON SİLİNDİ', `${resId} sözleşme kodlu rezervasyon başarıyla silindi.`);
  };

  const handleRescheduleReservation = (resId, newDate) => {
    setReservations(prev => prev.map(r => r.id === resId ? { ...r, date: newDate, eventDate: newDate, startDate: newDate, endDate: newDate } : r));
    showAlert('📅 Rezervasyon Tarihi Değiştirildi', `${resId} kodlu rezervasyon ${newDate} tarihine başarıyla taşındı.`);
  };

  // Venue Handlers
  const handleAddVenue = (vObj) => {
    setVenues(prev => [vObj, ...prev]);
    showAlert('🏰 Düğün Salonu Eklendi', `${vObj.name} başarıyla sisteme kaydedildi.`);
  };

  const handleEditVenue = (vObj) => {
    setVenues(prev => prev.map(x => x.id === vObj.id ? vObj : x));
    showAlert('✏️ Salon Düzenlendi', `${vObj.name} güncellendi.`);
  };

  const handleUpdateVenuePrice = (venueId, newPrice) => {
    setVenues(prev => prev.map(v => v.id === venueId ? { ...v, price: newPrice } : v));
    showAlert('💰 Salon Fiyatı Güncellendi', `Salon paket fiyatı ${newPrice.toLocaleString('tr-TR')} ₺ olarak güncellendi.`);
  };

  // Service Handlers
  const handleAddService = (sObj) => {
    setServices(prev => [sObj, ...prev]);
    showAlert('🎁 Hizmet Eklendi', `${sObj.name} eklendi.`);
  };

  const handleEditService = (sObj) => {
    setServices(prev => prev.map(x => x.id === sObj.id ? sObj : x));
    showAlert('✏️ Hizmet Güncellendi', `${sObj.name} güncellendi.`);
  };

  // Customer Handlers
  const handleAddCustomer = (cObj) => {
    setCustomers(prev => [cObj, ...prev]);
    showAlert('👥 Müşteri Eklendi', `${cObj.name} eklendi.`);
  };

  const handleEditCustomer = (cObj) => {
    setCustomers(prev => prev.map(x => x.id === cObj.id ? cObj : x));
    showAlert('✏️ Müşteri Güncellendi', `${cObj.name} güncellendi.`);
  };

  // Campaign Handlers
  const handleAddCampaign = (cObj) => {
    setCampaigns(prev => [cObj, ...prev]);
    showAlert('🔥 Kampanya Eklendi', `${cObj.title} (${cObj.code}) tanımlandı.`);
  };

  const handleEditCampaign = (cObj) => {
    setCampaigns(prev => prev.map(x => x.id === cObj.id ? cObj : x));
    showAlert('✏️ Kampanya Güncellendi', `${cObj.title} güncellendi.`);
  };

  const handleConvertToCampaign = (aiObj) => {
    const newCmp = {
      id: 'cmp-' + Date.now(),
      code: aiObj.code,
      title: aiObj.title,
      discountType: aiObj.discountType || 'percentage',
      discountValue: aiObj.discountValue || 10,
      minGuest: 300,
      validUntil: '2026-12-31',
      active: true,
      description: aiObj.description || aiObj.title
    };
    setCampaigns(prev => [newCmp, ...prev]);
    showAlert('🚀 AI Kampanyası Oluşturuldu!', `${aiObj.code} koduyla kampanya tanımlandı.`);
    setActiveTab('campaigns');
  };

  // User Handlers
  const handleAddUser = (uObj) => {
    setUsers(prev => [uObj, ...prev]);
    showAlert('🛡️ Personel Eklendi', `${uObj.name} sisteme eklendi.`);
  };

  const handleEditUser = (uObj) => {
    setUsers(prev => prev.map(x => x.id === uObj.id ? uObj : x));
    showAlert('✏️ Personel Güncellendi', `${uObj.name} güncellendi.`);
  };

  const activeUser = currentUser || users[0] || { name: 'Davut Akbulut', role: 'SuperAdmin' };

  return (
    <div className="flex h-screen bg-slate-900 dark:bg-brand-dark text-slate-100 font-sans overflow-hidden">
      
      {/* FLOATING ALERT POPUP */}
      <NotificationPopup alertModal={alertModal} onClose={closeAlert} />

      {/* SIDEBAR NAVIGATION */}
      <SidebarComponent
        activeTab={activeTab}
        onTabChange={setActiveTab}
        activeRole={activeRole}
        onRoleChange={setActiveRole}
      />

      {/* MAIN CONTENT AREA */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden bg-slate-100 dark:bg-brand-dark text-slate-800 dark:text-gray-200">
        
        {/* TOP HEADER */}
        <HeaderComponent
          activeTab={activeTab}
          onTabChange={setActiveTab}
          activeRole={activeRole}
          currentUser={currentUser}
        />

        {/* PAGE CONTENT CONTAINER WITH FAULT ISOLATION */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 custom-scrollbar">
          {activeTab === 'dashboard' && (
            <PageErrorBoundary pageName="Anasayfa / İstatistikler" onNavigateHome={setActiveTab}>
              <DashboardPage
                activeRole={activeRole}
                venues={venues}
                reservations={reservations}
                onNewResClick={() => setActiveTab('create-reservation')}
                onTabChange={setActiveTab}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'create-reservation' && (
            <PageErrorBoundary pageName="Yeni Rezervasyon Oluştur" onNavigateHome={setActiveTab}>
              <CreateReservationPage
                venues={venues}
                services={services}
                customers={customers}
                campaigns={campaigns}
                reservations={reservations}
                onSaveReservation={handleSaveReservation}
                onCancel={() => setActiveTab('reservations')}
                showToast={(msg) => showAlert('ℹ️ Bilgi', msg)}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'reservations' && (
            <PageErrorBoundary pageName="Rezervasyonlarım & Takvim" onNavigateHome={setActiveTab}>
              <ReservationsListPage
                reservations={reservations}
                venues={venues}
                services={services}
                customers={customers}
                campaigns={campaigns}
                onNewResClick={() => setActiveTab('create-reservation')}
                onUpdateReservation={handleUpdateReservation}
                onDeleteReservation={handleDeleteReservation}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'calendar' && (
            <PageErrorBoundary pageName="Takvim Görünümü" onNavigateHome={setActiveTab}>
              <CalendarPage
                reservations={reservations}
                venues={venues}
                onResClick={() => setActiveTab('reservations')}
                onReschedule={handleRescheduleReservation}
                onCreateNewForDate={(dStr) => setActiveTab('create-reservation')}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'finance' && (
            <PageErrorBoundary pageName="Finans & Kasa" onNavigateHome={setActiveTab}>
              <FinancePage
                financialStats={{ totalRev: reservations.reduce((a, b) => a + Number(b.totalAmount || 0), 0), totalDeposit: 45000 }}
                reservations={reservations}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'venues' && (
            <PageErrorBoundary pageName="Düğün Salonlarım" onNavigateHome={setActiveTab}>
              <VenuesPage
                venues={venues}
                onAddVenue={handleAddVenue}
                onEditVenue={handleEditVenue}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'services' && (
            <PageErrorBoundary pageName="Ek Hizmetlerim" onNavigateHome={setActiveTab}>
              <ServicesPage
                services={services}
                onAddService={handleAddService}
                onEditService={handleEditService}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'customers' && (
            <PageErrorBoundary pageName="Müşteri Rehberi" onNavigateHome={setActiveTab}>
              <CustomersPage
                customers={customers}
                onAddCustomer={handleAddCustomer}
                onEditCustomer={handleEditCustomer}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'campaigns' && (
            <PageErrorBoundary pageName="Kampanyalar" onNavigateHome={setActiveTab}>
              <CampaignsPage
                campaigns={campaigns}
                onAddCampaign={handleAddCampaign}
                onEditCampaign={handleEditCampaign}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'reports' && (
            <PageErrorBoundary pageName="Finans & Raporlar" onNavigateHome={setActiveTab}>
              <ReportsPage
                reservations={reservations}
                venues={venues}
                services={services}
                onConvertToCampaign={handleConvertToCampaign}
                onUpdateVenuePrice={handleUpdateVenuePrice}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'users' && (
            <PageErrorBoundary pageName="Kullanıcı Yönetimi" onNavigateHome={setActiveTab}>
              <UsersPage
                users={users}
                onAddUser={handleAddUser}
                onEditUser={handleEditUser}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'media' && (
            <PageErrorBoundary pageName="Medya Galerisi" onNavigateHome={setActiveTab}>
              <MediaPage
                reservations={reservations}
                showToast={(msg) => showAlert('📸 Medya Galerisi', msg)}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'profile' && (
            <PageErrorBoundary pageName="Profilim & Güvenlik" onNavigateHome={setActiveTab}>
              <ProfilePage
                currentUser={currentUser}
                activeRole={activeRole}
                onSaveProfile={(pData) => {
                  setCurrentUser(prev => ({ ...prev, ...pData }));
                  showAlert('👤 Profil Güncellendi', `${pData.name} bilgileri başarıyla kaydedildi.`);
                }}
                showToast={(msg) => showAlert('👤 Profil', msg)}
                onRoleChange={setActiveRole}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'mind-map' && (
            <PageErrorBoundary pageName="Zihin Haritası" onNavigateHome={setActiveTab}>
              <MindMapPage navigateTo={setActiveTab} />
            </PageErrorBoundary>
          )}

          {(activeTab === 'settings' || activeTab.startsWith('settings-')) && (
            <PageErrorBoundary pageName="Ayarlar" onNavigateHome={setActiveTab}>
              <SettingsPage
                activeRole={activeRole}
                roles={roles}
                tabPermissions={tabPermissions}
                onAddRole={handleAddRole}
                onToggleTabPermission={handleToggleTabPermission}
                themeColor={currentTheme}
                onThemeColorChange={setCurrentTheme}
                isCacheEnabled={true}
                onToggleCache={() => {}}
                onClearCache={() => {}}
                showToast={(msg) => showAlert('⚙️ Ayarlar', msg)}
                onNavigate={setActiveTab}
                initialSubTab={activeTab === 'settings-rbac' ? 'rbac' : activeTab === 'settings-errors' ? 'error-sim' : 'appearance'}
              />
            </PageErrorBoundary>
          )}

          {activeTab === '301' && (
            <PageErrorBoundary pageName="Yönlendirme" onNavigateHome={setActiveTab}>
              <Page301
                targetRoute="reservations"
                targetName="Rezervasyonlar & Canlı Takvim"
                onNavigate={setActiveTab}
              />
            </PageErrorBoundary>
          )}

          {activeTab === '403' && (
            <PageErrorBoundary pageName="Erişim Engellendi" onNavigateHome={setActiveTab}>
              <Page403
                requiredRole="Süper Yönetici (SuperAdmin)"
                onNavigate={setActiveTab}
              />
            </PageErrorBoundary>
          )}

          {activeTab === '500' && (
            <PageErrorBoundary pageName="Sunucu Hatası" onNavigateHome={setActiveTab}>
              <Page500
                errorDetails="Veritabanı bağlantı zaman aşımı (ETIMEDOUT)."
                onNavigate={setActiveTab}
              />
            </PageErrorBoundary>
          )}

          {/* FALLBACK 404 ROUTE */}
          {(!['dashboard', 'create-reservation', 'reservations', 'calendar', 'finance', 'venues', 'services', 'customers', 'campaigns', 'reports', 'users', 'media', 'profile', 'settings', '301', '403', '500'].includes(activeTab) || activeTab === '404') && (
            <PageErrorBoundary pageName="Sayfa Bulunamadı" onNavigateHome={setActiveTab}>
              <Page404 onNavigate={setActiveTab} />
            </PageErrorBoundary>
          )}
        </main>
      </div>

      {/* MOBILE FIXED BOTTOM SUMMARY BAR */}
      <MobileBottomSummaryBar />
    </div>
  );
}
