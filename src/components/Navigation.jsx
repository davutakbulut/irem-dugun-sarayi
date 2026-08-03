import React, { useState } from 'react';
import { ThemeIcon } from './ThemeIcon';

export function SidebarComponent({ activeTab, onTabChange, activeRole, onRoleChange, isSidebarOpen }) {
  const [collapsedGroups, setCollapsedGroups] = useState({
    'MÜŞTERİ & ANALİZ': true,
    'YÖNETİM & AYARLAR': true,
    'YÖNETİM & SİMÜLASYON': true,
    'Sistem Ayarları': true
  });

  const toggleGroup = (groupTitle) => {
    setCollapsedGroups(prev => ({
      ...prev,
      [groupTitle]: !prev[groupTitle]
    }));
  };

  const menuGroups = [
    {
      title: 'ANA PANOLAR',
      icon: 'chart',
      fallbackEmoji: '📌',
      items: [
        { id: 'dashboard', label: 'Genel Bakış', icon: 'chart', fallbackEmoji: '📊' },
        { id: 'create-reservation', label: 'Yeni Rezervasyon', icon: 'sparkles', fallbackEmoji: '✨', badge: 'YENİ' }
      ]
    },
    {
      title: 'REZERVASYON & TAKVİM',
      icon: 'calendar',
      fallbackEmoji: '📅',
      items: [
        { id: 'reservations', label: 'Rezervasyon Listesi', icon: 'list', fallbackEmoji: '📋' },
        { id: 'calendar', label: 'İnteraktif Takvim', icon: 'calendar', fallbackEmoji: '📅' }
      ]
    },
    {
      title: 'İŞLETME & FİNANS',
      icon: 'money',
      fallbackEmoji: '💰',
      items: [
        { id: 'finance', label: 'Finans Kasa & Gider', icon: 'money', fallbackEmoji: '💰', badge: 'CANLI' },
        { id: 'venues', label: 'Etkinlik Mekanları', icon: 'venue', fallbackEmoji: '🏰' },
        { id: 'services', label: 'Ek Hizmetler', icon: 'gift', fallbackEmoji: '🎁' },
        { id: 'campaigns', label: 'Kampanyalar & AI', icon: 'campaign', fallbackEmoji: '🏷️' }
      ]
    },
    {
      title: 'MÜŞTERİ & ANALİZ',
      icon: 'user',
      fallbackEmoji: '👥',
      items: [
        { id: 'customers', label: 'Müşteri Rehberi (CRM)', icon: 'user', fallbackEmoji: '👥' },
        { id: 'reports', label: 'Raporlar & Grafikler', icon: 'chart', fallbackEmoji: '📈' },
        { id: 'media', label: 'Medya & Foto Galeri', icon: 'camera', fallbackEmoji: '📸' }
      ]
    },
    {
      title: 'YÖNETİM & AYARLAR',
      icon: 'settings',
      fallbackEmoji: '⚙️',
      items: [
        { id: 'mind-map', label: 'Zihin Haritası (MindMap)', icon: 'sparkles', fallbackEmoji: '🧠', badge: 'YENİ' },
        { id: 'roles', label: 'Rol Yönetimi & İzinler', icon: 'shield', fallbackEmoji: '🛡️', badge: 'YENİ' },
        { id: 'users', label: 'Kullanıcı Yönetimi', icon: 'user', fallbackEmoji: '👥' },
        { id: 'settings', label: 'Sistem Ayarları', icon: 'settings', fallbackEmoji: '⚙️' }
      ]
    }
  ];

  if (isSidebarOpen === false) return null;

  return (
    <aside className="w-64 bg-white dark:bg-brand-card border-r border-slate-200 dark:border-brand-border hidden lg:flex flex-col justify-between shrink-0 shadow-sm transition-all duration-300 custom-scrollbar overflow-y-auto sticky top-0 h-[calc(100vh-105px)] z-20">
      <div className="flex-1 min-h-0 flex flex-col">
        {/* LOGO & BRANDING */}
        <div className="p-4 border-b border-slate-200 dark:border-brand-border flex items-center space-x-3 shrink-0">
          <div className="w-9 h-9 rounded-2xl gold-button flex items-center justify-center font-bold text-xl shadow-lg shrink-0">
            <ThemeIcon icon="crown" fallbackEmoji="👑" className="w-5 h-5 shrink-0" />
          </div>
          <div>
            <h1 className="font-heading font-extrabold text-sm text-slate-800 dark:text-gray-100 gold-gradient-text tracking-wide whitespace-nowrap">
              İREM DÜĞÜN SARAYI
            </h1>
            <p className="text-[9px] text-amber-600 dark:text-gold-400 font-bold">Kurumsal Yönetim V2.0</p>
          </div>
        </div>

        {/* NAVIGATION CATEGORIES & LINKS WITH INTERNAL SCROLL */}
        <nav className="p-3 space-y-3 custom-scrollbar overflow-y-auto flex-1 min-h-0">
          {menuGroups.map(group => {
            const isCollapsed = !!collapsedGroups[group.title];

            return (
              <div key={group.title} className="space-y-1 border-b border-slate-100 dark:border-brand-border/20 pb-2 last:border-0">
                <button
                  type="button"
                  onClick={() => toggleGroup(group.title)}
                  className="w-full text-[10px] font-extrabold text-slate-400 dark:text-gray-500 uppercase tracking-widest px-2.5 py-1 flex items-center justify-between hover:text-amber-500 transition cursor-pointer select-none rounded-lg hover:bg-slate-100 dark:hover:bg-brand-dark/50"
                >
                  <div className="flex items-center space-x-1.5">
                    <ThemeIcon icon={group.icon} fallbackEmoji={group.fallbackEmoji} className="w-3.5 h-3.5 shrink-0 opacity-70" />
                    <span>{group.title}</span>
                  </div>
                  <span className={`text-[9px] text-amber-500 transition duration-200 transform ${isCollapsed ? '-rotate-90' : 'rotate-0'}`}>
                    ▼
                  </span>
                </button>

                {!isCollapsed && (
                  <div className="space-y-1">
                    {group.items.map(item => {
                      if (item.roleNeeded && activeRole !== item.roleNeeded && activeRole !== 'SuperAdmin') {
                        return null;
                      }

                      const isActive = activeTab === item.id;
                      return (
                        <button
                          key={item.id}
                          onClick={() => onTabChange(item.id)}
                          className={`w-full flex items-center justify-between px-3 py-1.5 rounded-xl font-bold text-xs transition-all duration-200 ${
                            isActive
                              ? 'gold-button shadow-md transform translate-x-1'
                              : 'text-slate-700 dark:text-gray-300 hover:bg-slate-100 dark:hover:bg-brand-dark'
                          }`}
                        >
                          <div className="flex items-center space-x-2.5">
                            <ThemeIcon icon={item.icon} fallbackEmoji={item.fallbackEmoji} className="w-4 h-4 shrink-0" />
                            <span>{item.label}</span>
                          </div>
                          {item.badge && (
                            <span className={`text-[9px] font-extrabold px-2 py-0.5 rounded-full shadow ${
                              item.badge === 'CANLI' ? 'bg-emerald-500 text-white' :
                              item.badge === 'RBAC' ? 'bg-purple-600 text-white' :
                              item.badge === 'TEST' ? 'bg-red-500 text-white' : 'bg-amber-500 text-white'
                            }`}>
                              {item.badge}
                            </span>
                          )}
                        </button>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })}
        </nav>
      </div>

      {/* FOOTER */}
      <div className="p-3 border-t border-slate-200 dark:border-brand-border space-y-1 bg-slate-50/50 dark:bg-brand-dark/50 shrink-0">
        <div className="text-[10px] text-center text-slate-400 dark:text-gray-500 font-bold">
          İrem Düğün Sarayı v2.0 • Vite React
        </div>
      </div>
    </aside>
  );
}

export function HeaderComponent({
  activeTab,
  onTabChange,
  activeRole,
  onRoleChange,
  currentUser,
  isSidebarOpen,
  onToggleSidebar
}) {
  const getHeaderTitle = () => {
    switch (activeTab) {
      case 'dashboard': return { icon: 'chart', title: 'Genel Bakış & Performans Özeti' };
      case 'mind-map': return { icon: 'sparkles', title: 'İnteraktif Sistem Zihin Haritası & Akış Topolojisi' };
      case 'create-reservation': return { icon: 'sparkles', title: 'Yeni Rezervasyon & Sözleşme Kartı' };
      case 'reservations': return { icon: 'list', title: 'Rezervasyon Yönetimi & Sözleşmeler' };
      case 'calendar': return { icon: 'calendar', title: 'İnteraktif Takvim & Seans Denetimi' };
      case 'finance': return { icon: 'money', title: 'Finans Kasa, Gider & Fatura Yönetimi' };
      case 'venues': return { icon: 'venue', title: 'Düğün Salonları & Kapasite Bilgileri' };
      case 'services': return { icon: 'gift', title: 'Ek Hizmetler & Birim Fiyatlar' };
      case 'customers': return { icon: 'user', title: 'Müşteri Rehberi & CRM Üyelikleri' };
      case 'campaigns': return { icon: 'campaign', title: 'Kampanyalar & AI Öneri Motoru' };
      case 'reports': return { icon: 'chart', title: 'Raporlar & SVG Finansal Analizler' };
      case 'users': return { icon: 'shield', title: 'Yetkili Personel Listesi (RBAC)' };
      case 'settings-rbac': return { icon: 'shield', title: 'Rol & Sayfa İzin Matrisi (RBAC)' };
      case 'settings-errors': return { icon: 'warning', title: 'Canlı Sistem Hata & Yönlendirme Simülatörü' };
      case 'settings': return { icon: 'settings', title: 'Sistem Ayarları & Kurumsal Temalar' };
      case 'media': return { icon: 'camera', title: 'Medya & Galeri Yükleyici' };
      case 'profile': return { icon: 'user', title: 'Profilim & Güvenlik Ayarları' };
      default: return { icon: 'chart', title: 'İrem Düğün Sarayı Platformu' };
    }
  };

  const currentHeader = getHeaderTitle();

  return (
    <header className="sticky top-0 z-30 bg-white/90 dark:bg-brand-card/90 backdrop-blur-md border-b border-slate-200 dark:border-brand-border shadow-sm flex flex-col">
      {/* ROW 1: TOP MAIN HEADER BAR */}
      <div className="h-16 px-4 sm:px-6 flex items-center justify-between">
        {/* LEFT: MENU TOGGLE BUTTON + LOGO & BRAND */}
        <div className="flex items-center space-x-3">
          <button
            onClick={onToggleSidebar}
            className="p-2 rounded-xl bg-slate-100 dark:bg-brand-dark hover:bg-amber-500/10 text-slate-700 dark:text-gray-200 border border-slate-200 dark:border-brand-border transition shadow-2xs cursor-pointer lg:hidden"
            title="Yan Menüyü Aç/Kapat"
            aria-label="Menüyü Aç/Kapat"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path>
            </svg>
          </button>

          <div
            onClick={() => onTabChange('dashboard')}
            className="flex items-center space-x-2.5 cursor-pointer group"
          >
            <div className="w-9 h-9 rounded-xl gold-button flex items-center justify-center font-extrabold text-base shadow-sm shrink-0 group-hover:scale-105 transition">
              <ThemeIcon icon="crown" fallbackEmoji="🏰" className="w-5 h-5 shrink-0" />
            </div>
            <div>
              <h1 className="font-heading font-extrabold text-sm sm:text-base gold-gradient-text leading-tight tracking-tight">
                İREM DÜĞÜN SARAYI
              </h1>
              <p className="text-[9px] text-slate-500 dark:text-gray-400 font-bold uppercase tracking-wider hidden sm:block">
                Kurumsal Yönetim Portal
              </p>
            </div>
          </div>

          <div className="hidden lg:flex items-center space-x-2 border-l border-slate-200 dark:border-brand-border pl-3 ml-2">
            <span className="bg-amber-500/10 text-amber-800 dark:text-gold-400 font-bold text-xs px-2.5 py-1 rounded-lg border border-amber-500/20 flex items-center space-x-1.5">
              <ThemeIcon icon={currentHeader.icon} fallbackEmoji="📊" className="w-3.5 h-3.5" />
              <span>{currentHeader.title}</span>
            </span>
          </div>
        </div>

        {/* RIGHT: QUICK ACTION & PROFILE AVATAR */}
        <div className="flex items-center space-x-3">
          {activeTab !== 'create-reservation' && (
            <button
              onClick={() => onTabChange('create-reservation')}
              className="gold-button font-bold text-xs px-3.5 py-2 rounded-xl shadow flex items-center space-x-1.5 hover:scale-105 transition cursor-pointer"
            >
              <ThemeIcon icon="plus" fallbackEmoji="➕" className="w-3.5 h-3.5 shrink-0" />
              <span className="hidden sm:inline">Yeni Rezervasyon</span>
            </button>
          )}

          <div
            onClick={() => onTabChange('profile')}
            className="flex items-center space-x-2.5 border-l border-slate-200 dark:border-brand-border pl-3 cursor-pointer hover:opacity-80 transition"
          >
            <img
              src={currentUser?.avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'}
              alt="User"
              className="w-9 h-9 rounded-full object-cover border-2 border-amber-500/50 shadow-sm"
            />
            <div className="hidden md:block text-left">
              <div className="text-xs font-bold text-slate-800 dark:text-gray-100 leading-tight">
                {currentUser?.name || 'Davut Akbulut'}
              </div>
              <div className="text-[10px] text-amber-600 dark:text-gold-400 font-bold">
                {activeRole}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ROW 2: CONVENIENCE SUB-BAR FOR RBAC ROLE SWITCHER */}
      <div className="bg-slate-50/80 dark:bg-brand-dark/80 border-t border-slate-200/80 dark:border-brand-border/80 px-4 sm:px-6 py-1.5 flex items-center justify-between text-xs font-bold">
        <div className="flex items-center space-x-2 overflow-x-auto custom-scrollbar">
          <span className="text-[10px] uppercase font-extrabold text-slate-400 dark:text-gray-400 flex items-center space-x-1 shrink-0">
            <ThemeIcon icon="shield" fallbackEmoji="🛡️" className="w-3.5 h-3.5 text-amber-500" />
            <span>Hızlı Rol Değiştir:</span>
          </span>
          <div className="flex items-center space-x-1 shrink-0">
            {[
              { id: 'SuperAdmin', label: '👑 SuperAdmin' },
              { id: 'Manager', label: '💼 Müdür' },
              { id: 'Staff', label: '👤 Personel' }
            ].map(r => (
              <button
                key={r.id}
                onClick={() => onRoleChange && onRoleChange(r.id)}
                className={`px-2.5 py-1 rounded-lg text-[10px] font-bold transition cursor-pointer ${
                  activeRole === r.id
                    ? 'bg-amber-500 text-white shadow-xs'
                    : 'bg-white dark:bg-brand-card text-slate-600 dark:text-gray-300 border border-slate-200 dark:border-brand-border hover:bg-slate-100'
                }`}
              >
                {r.label}
              </button>
            ))}
          </div>
        </div>

        <div className="hidden sm:flex items-center space-x-2 text-[10px] text-slate-400 shrink-0">
          <span className="bg-emerald-500/10 text-emerald-600 font-bold px-2 py-0.5 rounded-full border border-emerald-500/20">
            🟢 Canlı Altyapı (v2.0)
          </span>
        </div>
      </div>
    </header>
  );
}

export function HorizontalNavbarComponent({ activeTab, onTabChange, activeRole }) {
  const [activeHoverGroup, setActiveHoverGroup] = useState(null);

  const menuGroups = [
    {
      id: 'dashboard-group',
      title: 'Ana Panolar',
      icon: 'chart',
      fallbackEmoji: '📌',
      showcaseTitle: 'İrem Düğün Sarayı Yönetim Paneli',
      showcaseDesc: 'Salon doluluk oranlarınızı, anlık rezervasyon hareketlerinizi ve performans verilerinizi tek ekrandan canlı takip edin.',
      showcaseImg: 'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=600&q=80',
      items: [
        { id: 'dashboard', label: 'Anasayfa / İstatistikler', desc: 'Genel ciro, doluluk ve AI önerileri', icon: 'chart', fallbackEmoji: '📊' },
        { id: 'create-reservation', label: 'Yeni Rezervasyon Oluştur', desc: 'Hızlı salon kiralama ve sözleşme girişi', icon: 'sparkles', fallbackEmoji: '✨', badge: 'YENİ' }
      ]
    },
    {
      id: 'calendar-group',
      title: 'Rezervasyon & Takvim',
      icon: 'calendar',
      fallbackEmoji: '📅',
      showcaseTitle: 'Düğün & Etkinlik Takvimi',
      showcaseDesc: 'Tüm düğün salonlarınızın opsiyonlu ve kesinleşmiş davet tarihlerini takvim üzerinden interaktif yönetin.',
      showcaseImg: 'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&w=600&q=80',
      items: [
        { id: 'reservations', label: 'Rezervasyon Listesi', desc: 'Filtrelenebilir davet kaydı ve faturasız döküm', icon: 'list', fallbackEmoji: '📋' },
        { id: 'calendar', label: 'İnteraktif Düğün Takvimi', desc: 'Ay/Gün bazlı doluluk kontrolü ve etkinlikler', icon: 'calendar', fallbackEmoji: '📅' }
      ]
    },
    {
      id: 'finance-group',
      title: 'İşletme & Finans',
      icon: 'money',
      fallbackEmoji: '💰',
      showcaseTitle: 'Finansal Yönetim & Salon İndirimleri',
      showcaseDesc: 'Kasa giriş-çıkışları, gider kayıtları ve AI destekli kampanya fiyat otomasyonu ile karlılığınızı artırın.',
      showcaseImg: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=600&q=80',
      items: [
        { id: 'finance', label: 'Finans Kasa & Gider Yönetimi', desc: 'Anlık kasa durumu, alacaklar ve harcamalar', icon: 'money', fallbackEmoji: '💰', badge: 'CANLI' },
        { id: 'venues', label: 'Etkinlik Mekanları', desc: 'Mekan kapasiteleri, özel imkanları ve paket fiyatları', icon: 'venue', fallbackEmoji: '🏰' },
        { id: 'services', label: 'Ek Hizmetler & Paketler', desc: 'Orkestra, fotoğrafçı, menü ve süsleme paketleri', icon: 'gift', fallbackEmoji: '🎁' },
        { id: 'campaigns', label: 'Kampanyalar & AI Fiyatlama', desc: 'Sezonluk indirimler ve dinamik fiyat motoru', icon: 'campaign', fallbackEmoji: '🏷️' }
      ]
    },
    {
      id: 'crm-group',
      title: 'Müşteri & Analiz',
      icon: 'user',
      fallbackEmoji: '👥',
      showcaseTitle: 'Müşteri Rehberi (CRM) & Foto Galeri',
      showcaseDesc: 'Gelin ve damat adaylarının iletişim geçmişini tutun, yapılan organizasyonların fotoğraf ve videolarını sergileyin.',
      showcaseImg: 'https://images.unsplash.com/photo-1537633552985-df8429e8048b?auto=format&fit=crop&w=600&q=80',
      items: [
        { id: 'customers', label: 'Müşteri Rehberi (CRM)', desc: 'Gelin & Damat bilgileri, özel notlar ve kayıtlar', icon: 'user', fallbackEmoji: '👥' },
        { id: 'reports', label: 'Raporlar & Grafikler', desc: 'Salon tercih oranları, doluluk ve ciro analizleri', icon: 'chart', fallbackEmoji: '📈' },
        { id: 'media', label: 'Medya & Foto Galeri', desc: 'Salon fotoğrafları, videoları ve organizasyon albümleri', icon: 'camera', fallbackEmoji: '📸' }
      ]
    },
    {
      id: 'admin-group',
      title: 'Yönetim & Ayarlar',
      icon: 'settings',
      fallbackEmoji: '⚙️',
      showcaseTitle: 'Personel Yetkileri & Sistem Ayarları',
      showcaseDesc: 'RBAC rol matrisi ile personel yetkilerini denetleyin, 5 kurumsal tema ve performans önbelleğini yönetin.',
      showcaseImg: 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=600&q=80',
      items: [
        { id: 'users', label: 'Personel (RBAC Yetkileri)', desc: 'Kullanıcı rolleri, şifre tanımları ve erişim matrisi', icon: 'shield', fallbackEmoji: '🛡️' },
        { id: 'settings-appearance', label: 'Görünüm & Temalar', desc: '5 kurumsal renk teması, buton tarzları ve görünüm modu', icon: 'sparkles', fallbackEmoji: '🎨' },
        { id: 'settings-rbac', label: 'Rol & İzin Matrisi', desc: 'Sayfa bazlı rol erişim yetkilerini özelleştirme', icon: 'shield', fallbackEmoji: '🛡️', badge: 'RBAC' },
        { id: 'settings-errors', label: 'Hata & Simülasyon', desc: '404, 500 ve yönlendirme testi simülatörü', icon: 'warning', fallbackEmoji: '🚨', badge: 'TEST' },
        { id: 'settings-performance', label: 'Önbellek & Performans', desc: 'Sistem belleği, önbellek temizleme ve hızlandırma', icon: 'chart', fallbackEmoji: '⚡' },
        { id: 'profile', label: 'Profilim & Güvenlik', desc: 'Kişisel hesap bilgileri, e-posta ve güvenlik', icon: 'user', fallbackEmoji: '👤' },
        { id: 'settings', label: 'Tüm Sistem Ayarları', desc: 'Genel yapılandırma ve gelişmiş tercihler', icon: 'settings', fallbackEmoji: '⚙️' }
      ]
    }
  ];

  const currentGroupData = menuGroups.find(g => g.id === activeHoverGroup);

  return (
    <div
      className="relative z-50 bg-white dark:bg-brand-card border-t border-b border-slate-200 dark:border-brand-border/60 shadow-xs"
      onMouseLeave={() => setActiveHoverGroup(null)}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2 flex items-center justify-start text-xs">
        <nav className="flex items-center space-x-1 sm:space-x-2 md:space-x-4 lg:space-x-6 overflow-x-auto lg:overflow-x-visible custom-scrollbar w-full">
          {menuGroups.map((group) => {
            const validGroupItems = group.items.filter(item => {
              if (activeRole === 'admin' || activeRole === 'SuperAdmin') return true;
              const allowed = TAB_PERMISSIONS[item.id] || TAB_PERMISSIONS[item.id.split('-')[0]] || ['admin'];
              return allowed.includes(activeRole);
            });
            if (validGroupItems.length === 0) return null;

            const isGroupActive = validGroupItems.some(item => activeTab === item.id || activeTab.startsWith(item.id));
            const isHovered = activeHoverGroup === group.id;

            return (
              <React.Fragment key={group.id}>
                <button
                  type="button"
                  onMouseEnter={() => setActiveHoverGroup(group.id)}
                  onClick={() => setActiveHoverGroup(prev => prev === group.id ? null : group.id)}
                  className={`px-3.5 py-1.5 rounded-xl font-bold transition-all flex items-center space-x-2 cursor-pointer whitespace-nowrap text-xs md:text-sm ${
                    isHovered || isGroupActive
                      ? 'text-amber-800 dark:text-gold-300 font-extrabold border-b-2 border-amber-500 bg-amber-500/10'
                      : 'text-slate-700 dark:text-gray-300 hover:text-amber-800 dark:hover:text-gold-300 hover:bg-slate-100 dark:hover:bg-brand-dark/50'
                  }`}
                >
                  <ThemeIcon icon={group.icon} fallbackEmoji={group.fallbackEmoji} className="w-4 h-4 text-amber-500 shrink-0" />
                  <span className="whitespace-nowrap">{group.title}</span>
                </button>
              </React.Fragment>
            );
          })}
        </nav>
      </div>

      {activeHoverGroup && currentGroupData && (
        <div className="absolute top-full left-0 right-0 bg-white dark:bg-slate-900 border-b-4 border-amber-500 shadow-[0_30px_70px_rgba(0,0,0,0.4)] z-40 animate-fade-in">
          <div className="max-w-7xl mx-auto p-6 grid grid-cols-1 md:grid-cols-3 gap-8 bg-white dark:bg-slate-900">
            <div className="md:col-span-2 space-y-4">
              <div className="flex items-center space-x-2 border-b border-slate-100 dark:border-brand-border/40 pb-3">
                <ThemeIcon icon={currentGroupData.icon} fallbackEmoji={currentGroupData.fallbackEmoji} className="w-5 h-5 text-amber-500" />
                <h3 className="font-heading font-extrabold text-sm text-slate-900 dark:text-gray-100 uppercase tracking-wider">
                  {currentGroupData.title} Bağlantıları
                </h3>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {currentGroupData.items.filter(item => {
                  if (activeRole === 'admin' || activeRole === 'SuperAdmin') return true;
                  const allowed = TAB_PERMISSIONS[item.id] || TAB_PERMISSIONS[item.id.split('-')[0]] || ['admin'];
                  return allowed.includes(activeRole);
                }).map(item => {
                  const isItemActive = activeTab === item.id || activeTab.startsWith(item.id);
                  return (
                    <button
                      key={item.id}
                      onClick={() => {
                        onTabChange(item.id);
                        setActiveHoverGroup(null);
                      }}
                      className={`p-3.5 rounded-2xl border text-left transition-all duration-200 group flex items-start space-x-3 cursor-pointer ${
                        isItemActive
                          ? 'bg-amber-500/15 border-amber-500/40 shadow-sm'
                          : 'bg-slate-50/60 dark:bg-brand-dark/50 border-slate-200/80 dark:border-brand-border/60 hover:bg-white dark:hover:bg-brand-dark hover:border-amber-500/40 hover:shadow-md'
                      }`}
                    >
                      <div className="p-2 rounded-xl bg-amber-500/10 text-amber-600 dark:text-gold-400 group-hover:bg-amber-500 group-hover:text-white transition shrink-0 mt-0.5">
                        <ThemeIcon icon={item.icon} fallbackEmoji={item.fallbackEmoji} className="w-4 h-4" />
                      </div>
                      <div className="space-y-0.5 min-w-0">
                        <div className="flex items-center space-x-2">
                          <span className="font-bold text-xs text-slate-800 dark:text-gray-100 group-hover:text-amber-800 dark:group-hover:text-gold-300 transition truncate">
                            {item.label}
                          </span>
                          {item.badge && (
                            <span className="text-[9px] font-black px-1.5 py-0.5 rounded-full bg-amber-500 text-white shrink-0">
                              {item.badge}
                            </span>
                          )}
                        </div>
                        <p className="text-[11px] text-slate-500 dark:text-gray-400 leading-normal line-clamp-2">
                          {item.desc}
                        </p>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            <div className="hidden md:block">
              <div className="relative rounded-2xl overflow-hidden border border-slate-200 dark:border-brand-border shadow-md h-full min-h-[200px] flex flex-col justify-end p-5 group">
                <img
                  src={currentGroupData.showcaseImg}
                  alt={currentGroupData.showcaseTitle}
                  className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition duration-500"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-slate-950/90 via-slate-950/40 to-transparent"></div>
                <div className="relative z-10 space-y-1.5 text-white">
                  <span className="text-[10px] font-black px-2 py-0.5 rounded-md gold-button uppercase tracking-wider inline-block">
                    Öne Çıkan Özellik
                  </span>
                  <h4 className="font-heading font-extrabold text-sm text-white">
                    {currentGroupData.showcaseTitle}
                  </h4>
                  <p className="text-[11px] text-slate-200 leading-relaxed">
                    {currentGroupData.showcaseDesc}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
