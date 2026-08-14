import React, { useState, useEffect } from 'react';
import { SidebarComponent, HeaderComponent } from './components/Navigation';
import { MobileBottomSummaryBar } from './components/MobileBottomSummaryBar';
import MobileDrawer from './components/MobileDrawer';
import { NotificationPopup } from './components/NotificationPopup';
import { PageErrorBoundary } from './components/PageErrorBoundary';
import { GlobalFooterComponent } from './components/Footer';
import {
  VersionHistoryModalComponent,
  VenueModalComponent,
  ServiceModalComponent,
  CustomerFormModal,
  CampaignModalComponent,
  UserModalComponent
} from './components/Modals';

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
import { Page404, Page301, Page403, Page500 } from './pages/ErrorPages';

// Public Standalone Front-End Website Components
import PublicLayout from './components/public/PublicLayout';
import HomePage from './pages/public/HomePage';
import HallsPage from './pages/public/HallsPage';
import VirtualTourPage from './pages/public/VirtualTourPage';
import OrganizationsPage from './pages/public/OrganizationsPage';
import VideosPage from './pages/public/VideosPage';
import BlogPage from './pages/public/BlogPage';
import AboutUsPage from './pages/public/AboutUsPage';
import ContactPage from './pages/public/ContactPage';
import CustomerLoginPage from './pages/public/CustomerLoginPage';
import CustomerRegisterPage from './pages/public/CustomerRegisterPage';

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
  const [isMobileDrawerOpen, setIsMobileDrawerOpen] = useState(false);
  const [systemVersion, setSystemVersion] = useState('v1.5.30');
  const [versionHistoryState, setVersionHistoryState] = useState([]);
  const [isVersionModalOpen, setIsVersionModalOpen] = useState(false);

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

  // Management CRUD Modal Data States
  const [venueModalData, setVenueModalData] = useState(null);
  const [serviceModalData, setServiceModalData] = useState(null);
  const [customerModalData, setCustomerModalData] = useState(null);
  const [campaignModalData, setCampaignModalData] = useState(null);
  const [userModalData, setUserModalData] = useState(null);

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
      if (currentTheme === 'nordic-light' || currentTheme === 'platinum-silver' || currentTheme === 'apple') {
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
            if (data.campaigns && Array.isArray(data.campaigns) && data.campaigns.length > 0) {
              setCampaigns(data.campaigns);
            }
            if (data.users && Array.isArray(data.users) && data.users.length > 0) {
              setUsers(data.users);
            }
            if (data.roles && typeof data.roles === 'object' && Object.keys(data.roles).length > 0) {
              setRolesState(data.roles);
            }
            if (data.tabPermissions && typeof data.tabPermissions === 'object' && Object.keys(data.tabPermissions).length > 0) {
              setTabPermissionsState(data.tabPermissions);
            }
            if (data.systemVersion) {
              setSystemVersion(data.systemVersion);
            }
            if (data.versionHistory && Array.isArray(data.versionHistory)) {
              setVersionHistoryState(data.versionHistory);
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
    if (!tabKey) return;
    
    let route = String(tabKey).trim();
    if (route.startsWith('/')) {
      route = route.replace(/^\/+/, '');
    }

    // Public route mapping
    let targetPublicTab = null;
    let targetSlug = route;

    if (route === 'salonlar' || route === 'salonlarimiz' || route === 'public-halls') {
      targetPublicTab = 'public-halls';
      targetSlug = 'salonlar';
    } else if (route === '360-tur' || route === 'sanal-tur' || route === 'public-virtual-tour') {
      targetPublicTab = 'public-virtual-tour';
      targetSlug = '360-tur';
    } else if (route === 'organizasyonlar' || route === 'public-organizations') {
      targetPublicTab = 'public-organizations';
      targetSlug = 'organizasyonlar';
    } else if (route === 'videolar' || route === 'public-videos') {
      targetPublicTab = 'public-videos';
      targetSlug = 'videolar';
    } else if (route === 'blog' || route === 'public-blog') {
      targetPublicTab = 'public-blog';
      targetSlug = 'blog';
    } else if (route === 'hakkimizda' || route === 'kurumsal' || route === 'public-about') {
      targetPublicTab = 'public-about';
      targetSlug = 'hakkimizda';
    } else if (route === 'iletisim' || route === 'public-contact') {
      targetPublicTab = 'public-contact';
      targetSlug = 'iletisim';
    } else if (route === 'musteri-giris' || route === 'public-customer-login') {
      targetPublicTab = 'public-customer-login';
      targetSlug = 'musteri-giris';
    } else if (route === 'musteri-kayit' || route === 'public-customer-register') {
      targetPublicTab = 'public-customer-register';
      targetSlug = 'musteri-kayit';
    } else if (route === '' || route === 'public-home' || route === 'home') {
      targetPublicTab = 'public-home';
      targetSlug = '';
    }

    if (targetPublicTab) {
      setActiveTab(targetPublicTab);
      if (typeof window !== 'undefined') {
        window.location.hash = targetSlug ? `#/${targetSlug}` : '#/';
      }
      return;
    }

    // Admin tab navigation
    setActiveTab(tabKey);
    const slug = TAB_TO_SLUG[tabKey] || tabKey;
    if (typeof window !== 'undefined') {
      window.location.hash = `#/${slug}`;
    }
  };

  // Helper to persist roles & permissions to backend
  const persistRolesAndPermissions = (updatedRoles, updatedPermissions) => {
    try {
      const fetchFn = window.fetchWithRetry || fetch;
      fetchFn('/api/system-settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          roles: updatedRoles,
          tabPermissions: updatedPermissions,
          updatedAt: new Date().toISOString(),
          updatedBy: 'admin'
        })
      });
    } catch(e) {}
  };

  // Role Management Handlers
  const handleAddRole = (roleId, roleName) => {
    const cleanId = roleId.trim().toLowerCase().replace(/[^a-z0-9_]/g, '_');
    if (!cleanId || !roleName.trim()) return;
    const newRoles = { ...rolesState, [cleanId]: roleName };
    const newPerms = { ...tabPermissionsState };
    Object.keys(newPerms).forEach(t => {
      if (!newPerms[t].includes(cleanId)) {
        newPerms[t] = [...newPerms[t], cleanId];
      }
    });
    setRolesState(newRoles);
    setTabPermissionsState(newPerms);
    persistRolesAndPermissions(newRoles, newPerms);
    showAlert('🛡️ Yeni Rol Eklendi', `"${roleName}" rolü başarıyla tanımlandı.`);
  };

  const handleEditRole = (roleId, newRoleName) => {
    if (!newRoleName.trim()) return;
    const newRoles = { ...rolesState, [roleId]: newRoleName };
    setRolesState(newRoles);
    persistRolesAndPermissions(newRoles, tabPermissionsState);
    showAlert('✏️ Rol Güncellendi', `"${newRoleName}" rol unvanı güncellendi.`);
  };

  const handleDeleteRole = (roleId) => {
    if (roleId === 'admin') {
      showAlert('⚠️ Uyarı', 'Admin rolü sistemin ana rolüdür, silinemez!');
      return;
    }
    const newRoles = { ...rolesState };
    delete newRoles[roleId];
    const newPerms = { ...tabPermissionsState };
    Object.keys(newPerms).forEach(t => {
      newPerms[t] = (newPerms[t] || []).filter(r => r !== roleId);
    });
    setRolesState(newRoles);
    setTabPermissionsState(newPerms);
    persistRolesAndPermissions(newRoles, newPerms);
    showAlert('🗑️ Rol Silindi', `Rol (${roleId}) ve izinleri silindi.`);
  };

  const handleToggleTabPermission = (tabId, roleId) => {
    const current = tabPermissionsState[tabId] || [];
    const updatedList = current.includes(roleId)
      ? current.filter(r => r !== roleId)
      : [...current, roleId];
    const newPerms = { ...tabPermissionsState, [tabId]: updatedList };
    setTabPermissionsState(newPerms);
    persistRolesAndPermissions(rolesState, newPerms);
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
  const handleSaveVenue = async (vObj) => {
    try {
      const isEdit = venues.some(v => v.id === vObj.id);
      const res = await fetch('/api/venues', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(vObj)
      });
      if (res.ok) {
        setVenues(prev => isEdit ? prev.map(x => x.id === vObj.id ? vObj : x) : [vObj, ...prev]);
        setVenueModalData(null);
        showAlert('🏰 Düğün Salonu Kaydedildi', `${vObj.name} başarıyla veritabanına kaydedildi.`);
      }
    } catch (e) {
      setVenues(prev => prev.some(x => x.id === vObj.id) ? prev.map(x => x.id === vObj.id ? vObj : x) : [vObj, ...prev]);
      setVenueModalData(null);
      showAlert('🏰 Düğün Salonu Kaydedildi', `${vObj.name} kaydedildi.`);
    }
  };

  const handleDeleteVenue = async (venueId) => {
    try {
      await fetch(`/api/venues/${venueId}`, { method: 'DELETE' });
    } catch (e) {}
    setVenues(prev => prev.filter(v => v.id !== venueId));
    showAlert('🗑️ Salon Silindi', `Salon başarıyla sistemden kaldırıldı.`);
  };

  const handleUpdateVenuePrice = (venueId, newPrice) => {
    setVenues(prev => prev.map(v => v.id === venueId ? { ...v, price: newPrice } : v));
    showAlert('💰 Salon Fiyatı Güncellendi', `Salon paket fiyatı ${newPrice.toLocaleString('tr-TR')} ₺ olarak güncellendi.`);
  };

  // Service Handlers
  const handleSaveService = async (sObj) => {
    try {
      const isEdit = services.some(s => s.id === sObj.id);
      const res = await fetch('/api/services', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(sObj)
      });
      if (res.ok) {
        setServices(prev => isEdit ? prev.map(x => x.id === sObj.id ? sObj : x) : [sObj, ...prev]);
        setServiceModalData(null);
        showAlert('🎁 Ek Hizmet Kaydedildi', `${sObj.name} başarıyla kaydedildi.`);
      }
    } catch (e) {
      setServices(prev => prev.some(x => x.id === sObj.id) ? prev.map(x => x.id === sObj.id ? sObj : x) : [sObj, ...prev]);
      setServiceModalData(null);
      showAlert('🎁 Ek Hizmet Kaydedildi', `${sObj.name} kaydedildi.`);
    }
  };

  const handleDeleteService = async (serviceId) => {
    try {
      await fetch(`/api/services/${serviceId}`, { method: 'DELETE' });
    } catch (e) {}
    setServices(prev => prev.filter(s => s.id !== serviceId));
    showAlert('🗑️ Ek Hizmet Silindi', `Hizmet sistemden kaldırıldı.`);
  };

  // Customer Handlers
  const handleSaveCustomer = async (cObj) => {
    try {
      const isEdit = customers.some(c => c.id === cObj.id);
      const res = await fetch('/api/customers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(cObj)
      });
      if (res.ok) {
        setCustomers(prev => isEdit ? prev.map(x => x.id === cObj.id ? cObj : x) : [cObj, ...prev]);
        setCustomerModalData(null);
        showAlert('👥 Müşteri Kaydedildi', `${cObj.name} müşteri rehberine kaydedildi.`);
      }
    } catch (e) {
      setCustomers(prev => prev.some(x => x.id === cObj.id) ? prev.map(x => x.id === cObj.id ? cObj : x) : [cObj, ...prev]);
      setCustomerModalData(null);
      showAlert('👥 Müşteri Kaydedildi', `${cObj.name} müşteri rehberine kaydedildi.`);
    }
  };

  const handleDeleteCustomer = async (customerId) => {
    try {
      await fetch(`/api/customers/${customerId}`, { method: 'DELETE' });
    } catch (e) {}
    setCustomers(prev => prev.filter(c => c.id !== customerId));
    showAlert('🗑️ Müşteri Silindi', `Müşteri kaydı silindi.`);
  };

  // Campaign Handlers
  const handleSaveCampaign = async (cObj) => {
    const isEdit = campaigns.some(c => c.id === cObj.id);
    setCampaigns(prev => isEdit ? prev.map(x => x.id === cObj.id ? cObj : x) : [cObj, ...prev]);
    setCampaignModalData(null);
    showAlert('🔥 Kampanya Kaydedildi', `${cObj.title} (${cObj.code}) tanımlandı.`);
  };

  const handleDeleteCampaign = (campaignId) => {
    setCampaigns(prev => prev.filter(c => c.id !== campaignId));
    showAlert('🗑️ Kampanya Silindi', `Kampanya kaldırıldı.`);
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
  const handleSaveUser = async (uObj) => {
    try {
      const isEdit = users.some(u => u.id === uObj.id);
      const res = await fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(uObj)
      });
      if (res.ok) {
        setUsers(prev => isEdit ? prev.map(x => x.id === uObj.id ? uObj : x) : [uObj, ...prev]);
        setUserModalData(null);
        showAlert('🛡️ Personel Kaydedildi', `${uObj.name} sisteme kaydedildi.`);
      }
    } catch (e) {
      setUsers(prev => prev.some(x => x.id === uObj.id) ? prev.map(x => x.id === uObj.id ? uObj : x) : [uObj, ...prev]);
      setUserModalData(null);
      showAlert('🛡️ Personel Kaydedildi', `${uObj.name} kaydedildi.`);
    }
  };

  const handleDeleteUser = async (userId) => {
    try {
      await fetch(`/api/users/${userId}`, { method: 'DELETE' });
    } catch (e) {}
    setUsers(prev => prev.filter(u => u.id !== userId));
    showAlert('🗑️ Personel Silindi', `Kullanıcı kaldırıldı.`);
  };

  // 1. MANAGEMENT ROUTE DETECTION (STRICTLY FOR /yonetim, /giris, /login ONLY)
  const pathname = typeof window !== 'undefined' ? (window.location.pathname || '/').toLowerCase() : '/';
  const isManagementRoute = pathname.startsWith('/yonetim') || pathname === '/giris' || pathname === '/login';

  // 2. MAIN PUBLIC DOMAIN GUARD (ALWAYS OPENS PUBLIC SITE WITHOUT LOGIN PROMPT)
  if (!isManagementRoute) {
    let currentPublicTab = activeTab;
    if (!currentPublicTab || !currentPublicTab.startsWith('public-')) {
      if (pathname === '/salonlar' || pathname === '/salonlarimiz') currentPublicTab = 'public-halls';
      else if (pathname === '/360-tur' || pathname === '/sanal-tur') currentPublicTab = 'public-virtual-tour';
      else if (pathname === '/organizasyonlar') currentPublicTab = 'public-organizations';
      else if (pathname === '/videolar') currentPublicTab = 'public-videos';
      else if (pathname === '/blog') currentPublicTab = 'public-blog';
      else if (pathname === '/hakkimizda') currentPublicTab = 'public-about';
      else if (pathname === '/iletisim') currentPublicTab = 'public-contact';
      else if (pathname === '/musteri-giris') currentPublicTab = 'public-customer-login';
      else if (pathname === '/musteri-kayit') currentPublicTab = 'public-customer-register';
      else currentPublicTab = 'public-home';
    }

    return (
      <PublicLayout currentRoute={pathname} navigateTo={navigateTo}>
        {(currentPublicTab === 'public-home' || currentPublicTab === 'home-gateway') && <HomePage navigateTo={navigateTo} />}
        {currentPublicTab === 'public-halls' && <HallsPage navigateTo={navigateTo} />}
        {currentPublicTab === 'public-virtual-tour' && <VirtualTourPage navigateTo={navigateTo} />}
        {currentPublicTab === 'public-organizations' && <OrganizationsPage navigateTo={navigateTo} />}
        {currentPublicTab === 'public-videos' && <VideosPage navigateTo={navigateTo} />}
        {currentPublicTab === 'public-blog' && <BlogPage navigateTo={navigateTo} />}
        {currentPublicTab === 'public-about' && <AboutUsPage navigateTo={navigateTo} />}
        {currentPublicTab === 'public-contact' && <ContactPage navigateTo={navigateTo} />}
        {currentPublicTab === 'public-customer-login' && <CustomerLoginPage navigateTo={navigateTo} />}
        {currentPublicTab === 'public-customer-register' && <CustomerRegisterPage navigateTo={navigateTo} />}
      </PublicLayout>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-slate-100 dark:bg-brand-dark text-slate-800 dark:text-gray-200 font-sans relative w-full max-w-full overflow-x-hidden">
      
      {/* FLOATING ALERT POPUP */}
      <NotificationPopup alertModal={alertModal} onClose={closeAlert} />

      {/* TOP HEADER */}
      <HeaderComponent
        activeTab={activeTab}
        onTabChange={navigateTo}
        activeRole={activeRole}
        onRoleChange={setActiveRole}
        currentUser={activeUser}
        rolesState={rolesState}
        onToggleSidebar={() => setIsMobileDrawerOpen(prev => !prev)}
        systemVersion={systemVersion}
        onOpenVersionModal={() => setIsVersionModalOpen(true)}
      />

      {/* MAIN CONTENT & SIDEBAR WRAPPER */}
      <div className="flex-1 flex min-h-0 w-full max-w-full">
        {/* SIDEBAR NAVIGATION */}
        <SidebarComponent
          activeTab={activeTab}
          onTabChange={navigateTo}
          activeRole={activeRole}
          onRoleChange={setActiveRole}
          rolesState={rolesState}
        />

        {/* PAGE CONTENT CONTAINER WITH FAULT ISOLATION */}
        <main className="flex-1 p-4 sm:p-6 min-w-0 w-full max-w-full">
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
                financialStats={{ totalRev: reservations.reduce((a, b) => a + Number(b.totalAmount || 0), 0), totalDeposit: reservations.reduce((a, b) => a + Number(b.depositPaid || 0), 0) }}
                reservations={reservations}
                setReservations={setReservations}
                venues={venues}
                services={services}
                onUpdateReservation={handleUpdateReservation}
                showToast={(msg) => showAlert('💰 Finans Bildirimi', msg)}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'venues' && (
            <PageErrorBoundary pageName="Düğün Salonlarım" onNavigateHome={navigateTo}>
              <VenuesPage
                venues={venues}
                services={services}
                onAddClick={() => setVenueModalData('new')}
                onEditClick={(v) => setVenueModalData(v)}
                onDeleteClick={handleDeleteVenue}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'services' && (
            <PageErrorBoundary pageName="Ek Hizmetlerim" onNavigateHome={navigateTo}>
              <ServicesPage
                services={services}
                onAddClick={() => setServiceModalData('new')}
                onEditClick={(s) => setServiceModalData(s)}
                onDeleteClick={handleDeleteService}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'customers' && (
            <PageErrorBoundary pageName="Müşteri Rehberi" onNavigateHome={navigateTo}>
              <CustomersPage
                customers={customers}
                onAddClick={() => setCustomerModalData('new')}
                onEditClick={(c) => setCustomerModalData(c)}
                onDeleteClick={handleDeleteCustomer}
              />
            </PageErrorBoundary>
          )}

          {activeTab === 'campaigns' && (
            <PageErrorBoundary pageName="Kampanyalar" onNavigateHome={navigateTo}>
              <CampaignsPage
                campaigns={campaigns}
                venues={venues}
                services={services}
                reservations={reservations}
                onAddClick={() => setCampaignModalData('new')}
                onEditClick={(c) => setCampaignModalData(c)}
                onDeleteClick={handleDeleteCampaign}
                onConvertToCampaign={handleConvertToCampaign}
                onUpdateVenuePrice={handleUpdateVenuePrice}
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
                onAddClick={() => setUserModalData('new')}
                onEditClick={(u) => setUserModalData(u)}
                onDeleteClick={handleDeleteUser}
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

      {/* FULL-WIDTH GLOBAL FOOTER AT VERY BOTTOM OF PAGE */}
      <GlobalFooterComponent
        onNavigate={navigateTo}
        activeRole={activeRole}
        campaigns={campaigns}
        showToast={showAlert}
        systemVersion={systemVersion}
        onOpenVersionModal={() => setIsVersionModalOpen(true)}
      />

      {/* MOBILE FIXED BOTTOM SUMMARY BAR */}
      <MobileBottomSummaryBar />

      {/* MOBILE NAVIGATION DRAWER */}
      <MobileDrawer
        isOpen={isMobileDrawerOpen}
        onClose={() => setIsMobileDrawerOpen(false)}
        activeTab={activeTab}
        activeRole={activeRole}
        tabPermissionsState={tabPermissionsState}
        navigateTo={navigateTo}
      />

      {/* VERSION HISTORY MODAL */}
      <VersionHistoryModalComponent
        isOpen={isVersionModalOpen}
        onClose={() => setIsVersionModalOpen(false)}
        systemVersion={systemVersion}
        versionHistory={versionHistoryState}
      />

      {/* CRUD MANAGEMENT MODALS */}
      {venueModalData && (
        <VenueModalComponent
          venue={venueModalData === 'new' ? null : venueModalData}
          allServices={services}
          onClose={() => setVenueModalData(null)}
          onSave={handleSaveVenue}
        />
      )}

      {serviceModalData && (
        <ServiceModalComponent
          service={serviceModalData === 'new' ? null : serviceModalData}
          onClose={() => setServiceModalData(null)}
          onSave={handleSaveService}
        />
      )}

      {customerModalData && (
        <CustomerFormModal
          customer={customerModalData === 'new' ? null : customerModalData}
          onClose={() => setCustomerModalData(null)}
          onSave={handleSaveCustomer}
        />
      )}

      {campaignModalData && (
        <CampaignModalComponent
          campaign={campaignModalData === 'new' ? null : campaignModalData}
          campaigns={campaigns}
          onClose={() => setCampaignModalData(null)}
          onSave={handleSaveCampaign}
        />
      )}

      {userModalData && (
        <UserModalComponent
          user={userModalData === 'new' ? null : userModalData}
          onClose={() => setUserModalData(null)}
          onSave={handleSaveUser}
        />
      )}
    </div>
  );
}
