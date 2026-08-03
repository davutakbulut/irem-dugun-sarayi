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
  INITIAL_SYSTEM_LOGS,
  ROLE_NAMES,
  TAB_PERMISSIONS
} from './constants/mockData';

import { parseHashRoute, fetchWithRetry, TAB_TO_SLUG, SLUG_TO_TAB } from './utils/formatters';

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
import { RolesPageComponent as RolesPage } from './pages/RolesPage';
import { SystemGuidePageComponent as SystemGuidePage } from './pages/SystemGuidePage';
import { MediaComponent as MediaPage } from './pages/MediaPage';
import { ProfileComponent as ProfilePage } from './pages/ProfilePage';
import { MindMapPageComponent as MindMapPage } from './pages/MindMapPage';
import { Page404, Page301, Page403, Page500 } from './pages/ErrorPages';

export default function App() {
  // Global State
  const [activeTab, setActiveTab] = useState(() => {
    const parsed = parseHashRoute();
    if (parsed && parsed.tab && parsed.tab !== 'simulasyon-404') {
      return parsed.tab;
    }
    const hash = (window.location.hash || '').replace('#/', '').replace('#', '').split('?')[0];
    if (hash === 'zihin-haritasi' || hash === 'mind-map') return 'mind-map';
    if (hash === 'yeni-rezervasyon') return 'create-reservation';
    return 'create-reservation';
  });

  const [activeRole, setActiveRole] = useState('admin');
  const [rolesState, setRolesState] = useState(ROLE_NAMES);
  const [tabPermissionsState, setTabPermissionsState] = useState(TAB_PERMISSIONS);

  const [currentTheme, setCurrentTheme] = useState(() => {
    if (typeof document !== 'undefined') {
      return document.documentElement.getAttribute('data-ui-theme') || 'obsidian-gold';
    }
    return 'obsidian-gold';
  });

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

  // Floating Notification Modal State
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

  // Sync Theme & UI Attributes to DOM HTML Element
  useEffect(() => {
    if (typeof document !== 'undefined') {
      document.documentElement.setAttribute('data-ui-theme', currentTheme);
      document.documentElement.setAttribute('data-theme', currentTheme);
      if (currentTheme === 'nordic-light' || currentTheme === 'platinum-silver') {
        document.documentElement.classList.remove('dark');
        document.documentElement.classList.add('light');
      } else {
        document.documentElement.classList.remove('light');
        document.documentElement.classList.add('dark');
      }
    }
  }, [currentTheme]);

  // Initial Fetch from Backend Database (/api/system-settings)
  useEffect(() => {
    try {
      fetchWithRetry('/api/system-settings')
        .then(res => res.json())
        .then(data => {
          if (data) {
            if (data.reservations && Array.isArray(data.reservations) && data.reservations.length > 0) {
              setReservations(data.reservations);
            }
            if (data.venues && Array.isArray(data.venues) && data.venues.length > 0) {
              setVenues(data.venues);
            }
            if (data.services && Array.isArray(data.services) && data.services.length > 0) {
              setServices(data.services);
            }
            if (data.customers && Array.isArray(data.customers) && data.customers.length > 0) {
              setCustomers(data.customers);
            }
            if (data.themeColor) {
              setCurrentTheme(data.themeColor);
            }
          }
        })
        .catch(() => {});
    } catch(e) {}
  }, []);

  // Sync Hash Route & URL Changes
  useEffect(() => {
    const handleHashChange = () => {
      const parsed = parseHashRoute();
      if (parsed && parsed.tab) {
        setActiveTab(parsed.tab);
      }
    };
    window.addEventListener('hashchange', handleHashChange);
    window.addEventListener('popstate', handleHashChange);
    return () => {
      window.removeEventListener('hashchange', handleHashChange);
      window.removeEventListener('popstate', handleHashChange);
    };
  }, []);

  const navigateTo = (tabKey) => {
    setActiveTab(tabKey);
    const slug = TAB_TO_SLUG[tabKey] || tabKey;
    if (typeof window !== 'undefined') {
      window.location.hash = `#/${slug}`;
    }
  };

  // Role Management Handlers
  const handleAddRole = (roleId, roleName) => {
    const cleanId = roleId.trim().toLowerCase().replace(/[^a-z0-9_]/g, '_');
    if (!cleanId || !roleName.trim()) return;
    setRolesState(prev => ({ ...prev, [cleanId]: roleName }));
    setTabPermissionsState(prev => {
      const updated = { ...prev };
      Object.keys(updated).forEach(t => {
        if (!updated[t].includes(cleanId)) {
          updated[t] = [...updated[t], cleanId];
        }
      });
      return updated;
    });
    showAlert('🛡️ Yeni Rol Eklendi', `"${roleName}" rolü başarıyla tanımlandı.`);
  };

  const handleEditRole = (roleId, newRoleName) => {
    if (!newRoleName.trim()) return;
    setRolesState(prev => ({ ...prev, [roleId]: newRoleName }));
    showAlert('✏️ Rol Güncellendi', `"${newRoleName}" rol unvanı güncellendi.`);
  };

  const handleDeleteRole = (roleId) => {
    if (roleId === 'admin') {
      showAlert('⚠️ Uyarı', 'Admin rolü sistemin ana rolüdür, silinemez!');
      return;
    }
    setRolesState(prev => {
      const copy = { ...prev };
      delete copy[roleId];
      return copy;
    });
    setTabPermissionsState(prev => {
      const updated = { ...prev };
      Object.keys(updated).forEach(t => {
        updated[t] = (updated[t] || []).filter(r => r !== roleId);
      });
      return updated;
    });
    showAlert('🗑️ Rol Silindi', `Rol (${roleId}) ve izinleri silindi.`);
  };

  const handleToggleTabPermission = (tabId, roleId) => {
    setTabPermissionsState(prev => {
      const current = prev[tabId] || [];
      const updated = current.includes(roleId)
        ? current.filter(r => r !== roleId)
        : [...current, roleId];
      return { ...prev, [tabId]: updated };
    });
  };

  // Reservation Handlers
  const handleSaveReservation = (newRes, newCustObj) => {
    if (newCustObj) {
      setCustomers(prev => [newCustObj, ...prev]);
    }
    setReservations(prev => [newRes, ...prev]);
    showAlert('🎉 REZERVASYON VE SÖZLEŞME OLUŞTURULDU!', `${newRes.customerName} için ${newRes.id} sözleşme koduyla rezervasyon başarıyla kaydedildi.`);
    navigateTo('reservations');
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
    navigateTo('campaigns');
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

  const activeUser = currentUser || users[0] || { name: 'Davut Akbulut', role: 'admin' };

  return (
    <div className="flex h-screen bg-slate-900 dark:bg-brand-dark text-slate-100 font-sans overflow-hidden">
      
      {/* FLOATING ALERT POPUP */}
      <NotificationPopup alertModal={alertModal} onClose={closeAlert} />

      {/* SIDEBAR NAVIGATION */}
      <SidebarComponent
        activeTab={activeTab}
        onTabChange={navigateTo}
        activeRole={activeRole}
        onRoleChange={setActiveRole}
        rolesState={rolesState}
      />

      {/* MAIN CONTENT AREA */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden bg-slate-100 dark:bg-brand-dark text-slate-800 dark:text-gray-200">
        
        {/* TOP HEADER */}
        <HeaderComponent
          activeTab={activeTab}
          onTabChange={navigateTo}
          activeRole={activeRole}
          onRoleChange={setActiveRole}
          currentUser={activeUser}
          rolesState={rolesState}
        />

        {/* PAGE CONTENT CONTAINER WITH FAULT ISOLATION */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 custom-scrollbar">
          {activeTab === 'dashboard' && (
            <PageErrorBoundary pageName="Anasayfa / İstatistikler" onNavigateHome={navigateTo}>
              <DashboardPage
                activeRole={activeRole}
                venues={venues}
                reservations={reservations}
                onNewResClick={() => navigateTo('create-reservation')}
                onTabChange={navigateTo}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'create-reservation' && (
            <PageErrorBoundary pageName="Yeni Rezervasyon Oluştur" onNavigateHome={navigateTo}>
              <CreateReservationPage
                venues={venues}
                services={services}
                customers={customers}
                campaigns={campaigns}
                reservations={reservations}
                onSaveReservation={handleSaveReservation}
                onCancel={() => navigateTo('reservations')}
                showToast={(msg) => showAlert('ℹ️ Bilgi', msg)}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'reservations' && (
            <PageErrorBoundary pageName="Rezervasyonlarım & Takvim" onNavigateHome={navigateTo}>
              <ReservationsListPage
                reservations={reservations}
                venues={venues}
                services={services}
                customers={customers}
                campaigns={campaigns}
                onNewResClick={() => navigateTo('create-reservation')}
                onUpdateReservation={handleUpdateReservation}
                onDeleteReservation={handleDeleteReservation}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'calendar' && (
            <PageErrorBoundary pageName="Takvim Görünümü" onNavigateHome={navigateTo}>
              <CalendarPage
                reservations={reservations}
                venues={venues}
                onResClick={() => navigateTo('reservations')}
                onReschedule={handleRescheduleReservation}
                onCreateNewForDate={(dStr) => navigateTo('create-reservation')}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'finance' && (
            <PageErrorBoundary pageName="Finans & Kasa" onNavigateHome={navigateTo}>
              <FinancePage
                financialStats={{ totalRev: reservations.reduce((a, b) => a + Number(b.totalAmount || 0), 0), totalDeposit: 45000 }}
                reservations={reservations}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'venues' && (
            <PageErrorBoundary pageName="Düğün Salonlarım" onNavigateHome={navigateTo}>
              <VenuesPage
                venues={venues}
                onAddVenue={handleAddVenue}
                onEditVenue={handleEditVenue}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'services' && (
            <PageErrorBoundary pageName="Ek Hizmetlerim" onNavigateHome={navigateTo}>
              <ServicesPage
                services={services}
                onAddService={handleAddService}
                onEditService={handleEditService}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'customers' && (
            <PageErrorBoundary pageName="Müşteri Rehberi" onNavigateHome={navigateTo}>
              <CustomersPage
                customers={customers}
                onAddCustomer={handleAddCustomer}
                onEditCustomer={handleEditCustomer}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'campaigns' && (
            <PageErrorBoundary pageName="Kampanyalar" onNavigateHome={navigateTo}>
              <CampaignsPage
                campaigns={campaigns}
                onAddCampaign={handleAddCampaign}
                onEditCampaign={handleEditCampaign}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'reports' && (
            <PageErrorBoundary pageName="Finans & Raporlar" onNavigateHome={navigateTo}>
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
            <PageErrorBoundary pageName="Kullanıcı Yönetimi" onNavigateHome={navigateTo}>
              <UsersPage
                users={users}
                onAddUser={handleAddUser}
                onEditUser={handleEditUser}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'roles' && (
            <PageErrorBoundary pageName="Rol Yönetimi & İzinler" onNavigateHome={navigateTo}>
              <RolesPage
                activeRole={activeRole}
                roles={rolesState}
                users={users}
                tabPermissions={tabPermissionsState}
                onAddRole={handleAddRole}
                onEditRole={handleEditRole}
                onDeleteRole={handleDeleteRole}
                onToggleTabPermission={handleToggleTabPermission}
                showToast={(msg) => showAlert('🛡️ Rol İzinleri', msg)}
                navigateTo={navigateTo}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'system-guide' && (
            <PageErrorBoundary pageName="Sistem Master Kılavuzu" onNavigateHome={navigateTo}>
              <SystemGuidePage
                navigateTo={navigateTo}
                activeRole={activeRole}
                themeColor={currentTheme}
                menuLayout="vertical"
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'media' && (
            <PageErrorBoundary pageName="Medya Galerisi" onNavigateHome={navigateTo}>
              <MediaPage
                reservations={reservations}
                showToast={(msg) => showAlert('📸 Medya Galerisi', msg)}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'profile' && (
            <PageErrorBoundary pageName="Profilim & Güvenlik" onNavigateHome={navigateTo}>
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
            <PageErrorBoundary pageName="Zihin Haritası" onNavigateHome={navigateTo}>
              <MindMapPage navigateTo={navigateTo} />
            </PageErrorBoundary>
          )}

          {(activeTab === 'settings' || activeTab.startsWith('settings-')) && (
            <PageErrorBoundary pageName="Ayarlar" onNavigateHome={navigateTo}>
              <SettingsPage
                activeRole={activeRole}
                roles={rolesState}
                tabPermissions={tabPermissionsState}
                onAddRole={handleAddRole}
                onEditRole={handleEditRole}
                onDeleteRole={handleDeleteRole}
                onToggleTabPermission={handleToggleTabPermission}
                themeColor={currentTheme}
                onThemeColorChange={setCurrentTheme}
                isCacheEnabled={true}
                onToggleCache={() => {}}
                onClearCache={() => {}}
                showToast={(msg) => showAlert('⚙️ Ayarlar', msg)}
                onNavigate={navigateTo}
                initialSubTab={activeTab === 'settings-rbac' ? 'rbac' : activeTab === 'settings-errors' ? 'error-sim' : 'appearance'}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'simulasyon-301' && (
            <PageErrorBoundary pageName="Yönlendirme" onNavigateHome={navigateTo}>
              <Page301
                targetRoute="reservations"
                targetName="Rezervasyonlar & Canlı Takvim"
                onNavigate={navigateTo}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'simulasyon-403' && (
            <PageErrorBoundary pageName="Erişim Engellendi" onNavigateHome={navigateTo}>
              <Page403
                requiredRole="Süper Yönetici (SuperAdmin)"
                onNavigate={navigateTo}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'simulasyon-500' && (
            <PageErrorBoundary pageName="Sunucu Hatası" onNavigateHome={navigateTo}>
              <Page500
                errorDetails="Veritabanı bağlantı zaman aşımı (ETIMEDOUT)."
                onNavigate={navigateTo}
              />
            </PageErrorBoundary>
          )}

          {/* FALLBACK 404 ROUTE */}
          {(![
            'dashboard', 'create-reservation', 'reservations', 'calendar', 'finance', 
            'venues', 'services', 'customers', 'campaigns', 'reports', 'users', 'roles',
            'system-guide', 'media', 'profile', 'mind-map', 'settings', 'settings-appearance', 
            'settings-performance', 'settings-rbac', 'settings-indexing', 'settings-errors', 
            'simulasyon-301', 'simulasyon-403', 'simulasyon-500'
          ].includes(activeTab) || activeTab === 'simulasyon-404') && (
            <PageErrorBoundary pageName="Sayfa Bulunamadı" onNavigateHome={navigateTo}>
              <Page404 onNavigate={navigateTo} />
            </PageErrorBoundary>
          )}
        </main>
      </div>

      {/* MOBILE FIXED BOTTOM SUMMARY BAR */}
      <MobileBottomSummaryBar />
    </div>
  );
}
