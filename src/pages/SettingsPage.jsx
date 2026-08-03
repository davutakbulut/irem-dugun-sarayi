import React, { useState, useEffect, useRef } from 'react';
import { RedAlertConfirmModal } from '../components/Modals.jsx';
import { Page404 as Page404Component, Page301 as Page301Component, Page403 as Page403Component, Page500 as Page500Component } from './ErrorPages.jsx';
import { createPortal } from 'react-dom';
import { ThemeIcon } from '../components/ThemeIcon.jsx';

export function SettingsComponent({
      activeRole,
      roles,
      tabPermissions,
      onAddRole,
      onEditRole,
      onDeleteRole,
      onToggleTabPermission,
      themeColor,
      onThemeColorChange,
      menuLayout = 'vertical',
      onMenuLayoutChange,
      isCacheEnabled,
      onToggleCache,
      onClearCache,
      onSeedDatabase,
      showToast,
      onNavigate,
      initialSubTab = 'appearance'
    }) {
      const [settingsTab, setSettingsTab] = useState(initialSubTab);
      const [draftTheme, setDraftTheme] = useState(() => {
        const domTheme = typeof document !== 'undefined' ? document.documentElement.getAttribute('data-ui-theme') : null;
        return themeColor || domTheme || '';
      });

      useEffect(() => {
        if (themeColor) {
          setDraftTheme(themeColor);
        }
      }, [themeColor]);

      useEffect(() => {
        if (initialSubTab) setSettingsTab(initialSubTab);
      }, [initialSubTab]);

      // New role form state
      const [newRoleId, setNewRoleId] = useState('');
      const [newRoleName, setNewRoleName] = useState('');

      const handleCreateRole = (e) => {
        e.preventDefault();
        if (!newRoleId || !newRoleName) return;
        const cleanId = newRoleId.toLowerCase().replace(/[^a-z0-9_]/g, '');
        if (roles[cleanId]) {
          showToast('⚠️ Bu rol Kimliği (ID) zaten mevcut!');
          return;
        }
        onAddRole(cleanId, newRoleName);
        setNewRoleId('');
        setNewRoleName('');
        showToast(`🎉 Yeni Rol "${newRoleName}" Başarıyla Oluşturuldu!`);
      };

      const colorPalettes = [
        { id: 'gold', name: '👑 Altın & Şampanya (Varsayılan)', primary: '#d97706', hover: '#b45309', radiusBadge: 'rounded-2xl' },
        { id: 'emerald', name: '💎 Zümrüt Yeşili (Royal Emerald)', primary: '#059669', hover: '#047857', radiusBadge: 'rounded-xl' },
        { id: 'sapphire', name: '🔷 Gece Mavisi (Deep Sapphire)', primary: '#2563eb', hover: '#1d4ed8', radiusBadge: 'rounded-xl' },
        { id: 'rose', name: '🌸 Gül Altını (Rose Gold)', primary: '#e11d48', hover: '#be123c', radiusBadge: 'rounded-2xl' },
        { id: 'violet', name: '🍇 Gece Moru (Midnight Violet)', primary: '#7c3aed', hover: '#6d28d9', radiusBadge: 'rounded-xl' },
        { id: 'obsidian', name: '⬛ Obsidian Gold (Kurumsal Siyah & Altın)', primary: '#18181b', hover: '#09090b', radiusBadge: 'rounded-none' },
        { id: 'sapphire_clean', name: '💎 Sapphire Clean (Safir Mavisi Minimal)', primary: '#0284c7', hover: '#0369a1', radiusBadge: 'rounded-md' },
        { id: 'platinum', name: '🪙 Platinum Silver (Platin Gümüş VIP)', primary: '#475569', hover: '#334155', radiusBadge: 'rounded-lg' },
        { id: 'emerald_royal', name: '🌲 Emerald Royal (Kraliyet Zümrütü)', primary: '#047857', hover: '#065f46', radiusBadge: 'rounded-2xl' },
        { id: 'titanium', name: '⚡ Titanium Tech (Titanyum Koyu Metal)', primary: '#3b82f6', hover: '#1d4ed8', radiusBadge: 'rounded-md' },
        { id: 'apple', name: ' Apple (2026 HIG Minimalist & Clean)', primary: '#0071E3', hover: '#0077ED', radiusBadge: 'rounded-full' }
      ];

      const [simulatedError, setSimulatedError] = useState(null);
      const [redAlertModalData, setRedAlertModalData] = useState(null);

      const allPagesList = [
        { id: 'dashboard', name: 'Genel Bakış & İstatistikler' },
        { id: 'create-reservation', name: 'Yeni Rezervasyon Oluştur' },
        { id: 'reservations', name: 'Rezervasyon Listesi & Sözleşmeler' },
        { id: 'calendar', name: 'İnteraktif Takvim' },
        { id: 'venues', name: 'Düğün Salonları' },
        { id: 'services', name: 'Ek Hizmetler' },
        { id: 'finance', name: 'Finans Kasa & Gider Yönetimi' },
        { id: 'customers', name: 'Müşteri Rehberi (CRM)' },
        { id: 'campaigns', name: 'Kampanyalar & AI Önerileri' },
        { id: 'reports', name: 'Raporlar & Analizler' },
        { id: 'media', name: 'Medya & Galeri Yükleyici' },
        { id: 'users', name: 'Kullanıcı Yönetimi (RBAC)' },
        { id: 'settings', name: 'Sistem Ayarları' }
      ];

      if (simulatedError === '404') {
        return (
          <div className="space-y-4">
            <button onClick={() => setSimulatedError(null)} className="px-4 py-2 rounded-xl bg-slate-800 text-white font-bold text-xs">← Simülasyondan Çık</button>
            <Page404Component onNavigate={(route) => { setSimulatedError(null); if (onNavigate) onNavigate(route); }} />
          </div>
        );
      }
      if (simulatedError === '301') {
        return (
          <div className="space-y-4">
            <button onClick={() => setSimulatedError(null)} className="px-4 py-2 rounded-xl bg-slate-800 text-white font-bold text-xs">← Simülasyondan Çık</button>
            <Page301Component onNavigate={(route) => { setSimulatedError(null); if (onNavigate) onNavigate(route); }} />
          </div>
        );
      }
      if (simulatedError === '403') {
        return (
          <div className="space-y-4">
            <button onClick={() => setSimulatedError(null)} className="px-4 py-2 rounded-xl bg-slate-800 text-white font-bold text-xs">← Simülasyondan Çık</button>
            <Page403Component onNavigate={(route) => { setSimulatedError(null); if (onNavigate) onNavigate(route); }} />
          </div>
        );
      }
      if (simulatedError === '500') {
        return (
          <div className="space-y-4">
            <button onClick={() => setSimulatedError(null)} className="px-4 py-2 rounded-xl bg-slate-800 text-white font-bold text-xs">← Simülasyondan Çık (Sistemi Sıfırla)</button>
            <Page500Component errorDetails="Simüle Edilen 500 Sunucu Çökme ve Beklenmeyen İstisna Testi" onNavigate={(route) => { setSimulatedError(null); if (onNavigate) onNavigate(route); }} />
          </div>
        );
      }

      return (
        <div className="w-full space-y-6 animate-fade-in pb-16">
          {/* PAGE HEADER */}
          <div className="glass-panel p-6 rounded-3xl border border-amber-500/30 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 shadow-sm">
            <div>
              <div className="flex items-center space-x-2">
                <ThemeIcon icon="settings" fallbackEmoji="⚙️" className="w-6 h-6 text-amber-500 shrink-0" />
                <h2 className="text-xl sm:text-2xl font-heading font-extrabold gold-gradient-text">
                  Sistem Ayarları & Yapılandırma Paneli
                </h2>
              </div>
              <p className="text-xs text-slate-500 dark:text-gray-400 mt-1 font-medium">
                Tema tercihlerini, görünüm mimarisini, önbellek ve hata simülasyonlarını tam ekranda yönetin.
              </p>
            </div>

            <button
              type="button"
              onClick={() => onNavigate && onNavigate('roles')}
              className="px-4 py-2 bg-amber-500/10 text-amber-800 dark:text-gold-400 border border-amber-500/30 rounded-xl text-xs font-bold hover:bg-amber-500 hover:text-slate-900 transition flex items-center space-x-1.5 shrink-0"
            >
              <ThemeIcon icon="shield" fallbackEmoji="🛡️" className="w-4 h-4 shrink-0" />
              <ThemeIcon icon="shield" fallbackEmoji="" className="w-4 h-4 text-amber-500 inline-block mr-1.5" /><span>Rol Yönetimi Sayfasına Git →</span>
            </button>
          </div>

          {/* TOP TAB NAVIGATION BAR */}
          <div className="flex flex-wrap gap-2 border-b border-slate-200 dark:border-brand-border pb-3">
            <button
              onClick={() => setSettingsTab('appearance')}
              className={`px-4 py-2.5 rounded-xl font-bold text-xs transition-all duration-200 flex items-center space-x-2 ${
                settingsTab === 'appearance' ? 'gold-button shadow-md' : 'bg-white dark:bg-brand-card text-slate-700 dark:text-gray-300 border border-slate-200 dark:border-brand-border hover:border-amber-500/50'
              }`}
            >
              <ThemeIcon icon="sparkles" fallbackEmoji="🎨" className="w-4 h-4 shrink-0" />
              <span>Görünüm & Temalar</span>
            </button>



            <button
              onClick={() => setSettingsTab('error-sim')}
              className={`px-4 py-2.5 rounded-xl font-bold text-xs transition-all duration-200 flex items-center space-x-2 ${
                settingsTab === 'error-sim' ? 'gold-button shadow-md' : 'bg-white dark:bg-brand-card text-slate-700 dark:text-gray-300 border border-slate-200 dark:border-brand-border hover:border-amber-500/50'
              }`}
            >
              <ThemeIcon icon="warning" fallbackEmoji="🚨" className="w-4 h-4 shrink-0" />
              <span>Hata & Yönlendirme Simülasyonu</span>
            </button>

            <button
              onClick={() => setSettingsTab('performance')}
              className={`px-4 py-2.5 rounded-xl font-bold text-xs transition-all duration-200 flex items-center space-x-2 ${
                settingsTab === 'performance' ? 'gold-button shadow-md' : 'bg-white dark:bg-brand-card text-slate-700 dark:text-gray-300 border border-slate-200 dark:border-brand-border hover:border-amber-500/50'
              }`}
            >
              <ThemeIcon icon="chart" fallbackEmoji="⚡" className="w-4 h-4 shrink-0" />
              <span>Önbellek & Performans</span>
            </button>
          </div>

          {/* TAB 1: APPEARANCE & VISUAL THEME SELECTION WITH PREVIEWS */}
          {settingsTab === 'appearance' && (
            <div className="space-y-6">
              {/* MENU LAYOUT CONFIGURATION (DİKEY vs YATAY MENÜ SEÇİMİ) */}
              <div className="glass-panel p-6 rounded-3xl space-y-4 border border-amber-500/30 shadow-md">
                <div className="flex justify-between items-center border-b pb-4 border-slate-200 dark:border-brand-border/40">
                  <div>
                    <h3 className="font-heading font-extrabold text-lg text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                      <ThemeIcon icon="settings" fallbackEmoji="📐" className="w-5 h-5 text-amber-500 shrink-0" />
                      <span>Masaüstü Menü Yerleşimi & Navigasyon Modu</span>
                    </h3>
                    <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">
                      Sistem gezinti menünüzü klasik Dikey Sol Panel veya geniş ekranlara uygun Yatay Üst Bar olarak tercih edin.
                    </p>
                  </div>
                  <span className="text-xs font-bold px-3 py-1 rounded-full bg-amber-500/10 text-amber-800 dark:text-gold-400 border border-amber-500/20">
                    Aktif: {menuLayout === 'horizontal' ? 'Yatay Üst Menü ══' : 'Dikey Sol Menü 📌'}
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                  {/* OPTION 1: DİKEY SOL MENÜ */}
                  <div
                    onClick={() => onMenuLayoutChange && onMenuLayoutChange('vertical')}
                    className={`p-5 rounded-2xl border-2 cursor-pointer transition-all duration-300 space-y-3 ${
                      menuLayout === 'vertical'
                        ? 'border-amber-500 bg-amber-500/10 shadow-lg ring-4 ring-amber-500/20 scale-[1.01]'
                        : 'border-slate-200 dark:border-brand-border bg-white dark:bg-brand-card hover:border-amber-500/40'
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <div className="flex items-center space-x-2 font-bold text-sm text-slate-800 dark:text-gray-100">
                        <ThemeIcon icon="list" fallbackEmoji="📌" className="w-5 h-5 text-amber-500 shrink-0" />
                        <span>Dikey Sol Menü (Klasik Sidebar)</span>
                      </div>
                      {menuLayout === 'vertical' && (
                        <span className="text-[10px] font-black px-2 py-0.5 rounded-full gold-button">SEÇİLDİ</span>
                      )}
                    </div>
                    <p className="text-xs text-slate-500 dark:text-gray-400 leading-relaxed">
                      Sol tarafta dikey panel olarak yer alır. Tüm kategoriler ve alt gezinti bağlantıları dikey listede gösterilir.
                    </p>
                  </div>

                  {/* OPTION 2: YATAY ÜST MENÜ */}
                  <div
                    onClick={() => onMenuLayoutChange && onMenuLayoutChange('horizontal')}
                    className={`p-5 rounded-2xl border-2 cursor-pointer transition-all duration-300 space-y-3 ${
                      menuLayout === 'horizontal'
                        ? 'border-amber-500 bg-amber-500/10 shadow-lg ring-4 ring-amber-500/20 scale-[1.01]'
                        : 'border-slate-200 dark:border-brand-border bg-white dark:bg-brand-card hover:border-amber-500/40'
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <div className="flex items-center space-x-2 font-bold text-sm text-slate-800 dark:text-gray-100">
                        <ThemeIcon icon="chart" fallbackEmoji="══" className="w-5 h-5 text-amber-500 shrink-0" />
                        <span>Yatay Üst Menü (Modern Bar)</span>
                      </div>
                      {menuLayout === 'horizontal' && (
                        <span className="text-[10px] font-black px-2 py-0.5 rounded-full gold-button">SEÇİLDİ</span>
                      )}
                    </div>
                    <p className="text-xs text-slate-500 dark:text-gray-400 leading-relaxed">
                      Üst başlığın hemen altında yatay gezinti barı olarak yer alır. Ekran alanını maksimum genişlikte kullanmanızı sağlar.
                    </p>
                  </div>
                </div>
              </div>
              <div className="glass-panel p-6 rounded-3xl space-y-6 border border-amber-500/30 shadow-md">
                <div className="flex justify-between items-center border-b pb-4 border-slate-200 dark:border-brand-border/40">
                  <div>
                    <h3 className="font-heading font-extrabold text-lg text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                      <ThemeIcon icon="paint" fallbackEmoji="🎨" className="w-5 h-5 text-amber-500 shrink-0" />
                      <span>Kurumsal Arayüz Mimarisi & Tema Kartları</span>
                    </h3>
                    <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">
                      Tasarım çizginizi, buton hatlarınızı, kart mimarinizi ve renk kimliğinizi görsel kart önizlemeleri ile seçip kaydet düğmesiyle kalıcı hale getirin.
                    </p>
                  </div>
                </div>

                {/* INTERACTIVE VISUAL THEME PREVIEW CARDS */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  
                  {/* THEME PREVIEW CARD 1: MEVCUT RENKLİ & YUMUŞAK TEMA */}
                  <div
                    onClick={() => setDraftTheme('gold')}
                    style={{ borderRadius: '24px' }}
                    className={`p-5 border-2 cursor-pointer transition-all duration-300 space-y-4 relative ${
                      draftTheme === 'gold'
                        ? 'border-amber-500 bg-amber-500/10 shadow-xl ring-4 ring-amber-500/20 scale-[1.01]'
                        : 'border-slate-200 dark:border-brand-border/60 bg-white dark:bg-brand-card hover:border-amber-500/40'
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <div className="flex items-center space-x-2">
                        <span className="text-2xl">👑</span>
                        <div>
                          <h4 className="font-heading font-extrabold text-sm text-amber-900 dark:text-amber-300">Klasik Şampanya Altını (Canlı & Yuvarlak Hatlı)</h4>
                          <span className="text-[10px] text-amber-700 dark:text-amber-400 font-mono font-bold">Yuvarlak Hatlar (rounded-2xl) • Canlı Turuncu/Altın Gradyanlar</span>
                        </div>
                      </div>
                      {draftTheme === 'gold' && <span style={{ borderRadius: '9999px', background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)' }} className="text-white font-extrabold text-[10px] px-2.5 py-0.5 shadow">SEÇİLDİ</span>}
                    </div>

                    {/* MINI LIVE ISOLATED COMPONENT PREVIEW */}
                    <div style={{ borderRadius: '16px', background: '#FFFBEB', borderColor: '#FDE68A' }} className="p-4 border space-y-3 shadow-inner">
                      <div className="text-[10px] font-bold text-amber-700 uppercase tracking-wider">CANLI TEMA ÖNİZLEMESİ (ORİJİNAL):</div>
                      <div className="flex items-center justify-between">
                        <span style={{ background: 'linear-gradient(135deg, #D97706 0%, #B45309 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }} className="font-heading font-extrabold text-xs">İrem Düğün Sarayı</span>
                        <div style={{ borderRadius: '16px', background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)', color: '#ffffff', boxShadow: '0 4px 14px rgba(217, 119, 6, 0.35)' }} className="font-bold text-[11px] px-3.5 py-1.5">Canlı Buton</div>
                      </div>
                      <div style={{ borderRadius: '16px', background: '#FFFFFF', borderColor: '#FCD34D' }} className="p-3 border text-[11px] space-y-1">
                        <div className="font-bold text-amber-900">Kraliyet Balo Salonu</div>
                        <div className="text-[10px] text-amber-700">750 Kişilik Yumuşak Yuvarlak Balo Mimarisi</div>
                      </div>
                    </div>
                  </div>

                  {/* THEME PREVIEW CARD 2: QUIET LUXURY & MINIMALIST HIGH-END ARCHITECTURE DARK THEME */}
                  <div
                    onClick={() => setDraftTheme('elite-luxury')}
                    style={{ borderRadius: '0px' }}
                    className={`p-5 border-2 cursor-pointer transition-all duration-300 space-y-4 relative ${
                      draftTheme === 'elite-luxury' || draftTheme === 'obsidian'
                        ? 'border-[#D4AF37] bg-[#14161D] text-[#F8FAFC] shadow-2xl ring-4 ring-[#D4AF37]/20 scale-[1.01]'
                        : 'border-[#22252F] bg-[#0B0C0E] text-[#94A3B8] hover:border-[#D4AF37]/40'
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <div className="flex items-center space-x-2">
                        <span className="text-2xl">🖤👑</span>
                        <div>
                          <h4 className="font-heading font-bold text-sm text-[#D4AF37] uppercase tracking-wider">Quiet Luxury & Minimalist Architecture</h4>
                          <span className="text-[10px] text-[#94A3B8] font-mono font-bold">Obsidian (#0B0C0E) • Champagne Gold (#D4AF37) • 0px Border-Radius</span>
                        </div>
                      </div>
                      {(draftTheme === 'elite-luxury' || draftTheme === 'obsidian') && <span style={{ borderRadius: '0px' }} className="bg-[#D4AF37] text-[#0B0C0E] font-extrabold text-[10px] px-2.5 py-0.5 tracking-widest shadow">SEÇİLDİ</span>}
                    </div>

                    {/* MINI LIVE ISOLATED COMPONENT PREVIEW */}
                    <div style={{ borderRadius: '0px', background: '#0B0C0E', borderColor: 'rgba(212, 175, 55, 0.3)' }} className="p-4 border space-y-3">
                      <div className="text-[10px] font-mono text-[#94A3B8] uppercase tracking-widest">QUIET LUXURY TOKENS ÖNİZLEME:</div>
                      <div className="flex items-center justify-between">
                        <span className="font-heading font-bold text-xs text-[#F8FAFC] uppercase tracking-wider">İrem Balo Sarayı</span>
                        <div style={{ borderRadius: '0px', background: '#D4AF37', color: '#0B0C0E' }} className="font-bold text-[10px] uppercase px-3 py-1.5 tracking-wider">PRIMARY BUTTON</div>
                      </div>
                      <div style={{ borderRadius: '0px', background: '#14161D', borderColor: 'rgba(255, 255, 255, 0.08)' }} className="p-3 border text-[11px]">
                        <div className="font-bold text-[#F8FAFC]">Kraliyet Balo Salonu (VİP)</div>
                        <div className="text-[10px] text-[#94A3B8]">750 Kişilik High-End Balo Mimarisi</div>
                      </div>
                    </div>
                  </div>

                  {/* THEME PREVIEW CARD 3: NORDIC CLARITY & PREMIUM SCANDINAVIAN MINIMAL (LIGHT THEME) */}
                  <div
                    onClick={() => setDraftTheme('nordic-light')}
                    style={{ borderRadius: '0px' }}
                    className={`p-5 border-2 cursor-pointer transition-all duration-300 space-y-4 relative ${
                      draftTheme === 'nordic-light'
                        ? 'border-[#0F172A] bg-[#FAFAFA] text-[#0F172A] shadow-xl ring-4 ring-[#0F172A]/10 scale-[1.01]'
                        : 'border-[#E2E8F0] bg-white text-[#64748B] hover:border-[#0F172A]/30'
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <div className="flex items-center space-x-2">
                        <ThemeIcon icon="venue" fallbackEmoji="" className="w-6 h-6 text-[#0F172A] shrink-0" />
                        <div>
                          <h4 className="font-heading font-bold text-sm text-[#0F172A] uppercase tracking-wider">Nordic Clarity & Scandinavian Minimal</h4>
                          <span className="text-[10px] text-[#64748B] font-mono font-bold">Alabaster (#FAFAFA) • Midnight Navy (#0F172A) • 0px Sharp Geometry</span>
                        </div>
                      </div>
                      {draftTheme === 'nordic-light' && <span style={{ borderRadius: '0px' }} className="bg-[#0F172A] text-white font-extrabold text-[10px] px-2.5 py-0.5 tracking-widest shadow">SEÇİLDİ</span>}
                    </div>

                    {/* MINI LIVE ISOLATED COMPONENT PREVIEW */}
                    <div style={{ borderRadius: '0px', background: '#FAFAFA', borderColor: '#E2E8F0' }} className="p-4 border space-y-3">
                      <div className="text-[10px] font-mono text-[#64748B] uppercase tracking-widest">NORDIC CLARITY LIGHT PREVIEW:</div>
                      <div className="flex items-center justify-between">
                        <span className="font-heading font-bold text-xs text-[#0F172A] uppercase tracking-wider">İrem Balo Sarayı</span>
                        <div style={{ borderRadius: '0px', background: '#0F172A', color: '#FFFFFF' }} className="font-bold text-[10px] uppercase px-3 py-1.5 tracking-wider">NORDIC BUTTON</div>
                      </div>
                      <div style={{ borderRadius: '0px', background: '#FFFFFF', borderColor: '#E2E8F0' }} className="p-3 border text-[11px] shadow-sm">
                        <div className="font-bold text-[#0F172A]">Kraliyet Balo Salonu (VİP)</div>
                        <div className="text-[10px] text-[#64748B]">750 Kişilik Mimari Aydınlık Düzen</div>
                      </div>
                    </div>
                  </div>

                  {/* THEME PREVIEW CARD 4: NEO-MINIMALIST SAFİR */}
                  <div
                    onClick={() => setDraftTheme('sapphire-minimal')}
                    style={{ borderRadius: '12px' }}
                    className={`p-5 border-2 cursor-pointer transition-all duration-300 space-y-4 relative ${
                      draftTheme === 'sapphire-minimal' || draftTheme === 'sapphire_clean'
                        ? 'border-[#0284C7] bg-[#1E293B] text-[#F8FAFC] shadow-2xl ring-4 ring-[#0284C7]/30 scale-[1.01]'
                        : 'border-[#334155] bg-[#0F172A] text-[#94A3B8] hover:border-[#0284C7]/50'
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <div className="flex items-center space-x-2">
                        <span className="text-2xl">🔷⚡</span>
                        <div>
                          <h4 className="font-heading font-extrabold text-sm text-[#38BDF8] tracking-wide">Neo-Minimalist Safir (Tech Corporate)</h4>
                          <span className="text-[10px] text-[#94A3B8] font-mono font-bold">Deep Slate (#0F172A) • Electric Blue (#0284C7) • 8px Rounded</span>
                        </div>
                      </div>
                      {(draftTheme === 'sapphire-minimal' || draftTheme === 'sapphire_clean') && <span style={{ borderRadius: '6px' }} className="bg-[#0284C7] text-white font-extrabold text-[10px] px-2.5 py-0.5 shadow">SEÇİLDİ</span>}
                    </div>

                    {/* MINI LIVE ISOLATED COMPONENT PREVIEW */}
                    <div style={{ borderRadius: '8px', background: '#0F172A', borderColor: '#334155' }} className="p-4 border space-y-3">
                      <div className="text-[10px] font-mono text-[#38BDF8] uppercase tracking-widest">SAFİR TECH DESIGN TOKENS ÖNİZLEME:</div>
                      <div className="flex items-center justify-between">
                        <span className="font-heading font-extrabold text-xs text-[#F8FAFC]">İrem Safir Sarayı</span>
                        <div style={{ borderRadius: '8px', background: '#0284C7', color: '#FFFFFF', boxShadow: '0 4px 14px rgba(2, 132, 199, 0.4)' }} className="font-bold text-[10px] px-3.5 py-1.5">SAFİR BUTON</div>
                      </div>
                      <div style={{ borderRadius: '8px', background: '#1E293B', borderColor: '#334155' }} className="p-3 border text-[11px]">
                        <div className="font-bold text-[#F8FAFC]">Kraliyet Safir Balo Düzeni</div>
                        <div className="text-[10px] text-[#94A3B8]">Modern Dijital Teknoloji Balo Mimarisi</div>
                      </div>
                    </div>
                  </div>

                  {/* THEME PREVIEW CARD 5: KRALİYET ZÜMRÜT KIR BAHÇESİ */}
                  <div
                    onClick={() => setDraftTheme('emerald-royal')}
                    style={{ borderRadius: '16px' }}
                    className={`p-5 border-2 cursor-pointer transition-all duration-300 space-y-4 relative ${
                      draftTheme === 'emerald-royal' || draftTheme === 'emerald_royal'
                        ? 'border-[#34D399] bg-[#064E3B] text-[#ECFDF5] shadow-2xl ring-4 ring-[#10B981]/30 scale-[1.01]'
                        : 'border-emerald-900/60 bg-[#042F2E] text-[#A7F3D0] hover:border-[#34D399]/50'
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <div className="flex items-center space-x-2">
                        <span className="text-2xl">🌿🏰</span>
                        <div>
                          <h4 className="font-heading font-extrabold text-sm text-[#34D399] tracking-wide">Kraliyet Zümrüt Kır Bahçesi (Botanık Lüks)</h4>
                          <span className="text-[10px] text-[#A7F3D0] font-mono font-bold">Forest Emerald (#042F2E) • Mint Gold Trim (#34D399) • 14px Curved</span>
                        </div>
                      </div>
                      {(draftTheme === 'emerald-royal' || draftTheme === 'emerald_royal') && <span style={{ borderRadius: '12px' }} className="bg-[#10B981] text-white font-extrabold text-[10px] px-2.5 py-0.5 shadow">SEÇİLDİ</span>}
                    </div>

                    {/* MINI LIVE ISOLATED COMPONENT PREVIEW */}
                    <div style={{ borderRadius: '14px', background: '#042F2E', borderColor: 'rgba(52, 211, 153, 0.3)' }} className="p-4 border space-y-3">
                      <div className="text-[10px] font-mono text-[#34D399] uppercase tracking-widest">ZÜMRÜT BOTANİK PREVIEW:</div>
                      <div className="flex items-center justify-between">
                        <span className="font-heading font-extrabold text-xs text-[#ECFDF5]">Kır Bahçesi VİP Estate</span>
                        <div style={{ borderRadius: '14px', background: 'linear-gradient(135deg, #10B981 0%, #047857 100%)', color: '#FFFFFF', border: '1px solid #34D399', boxShadow: '0 4px 14px rgba(16, 185, 129, 0.35)' }} className="font-bold text-[10px] px-3.5 py-1.5">ZÜMRÜT BUTON</div>
                      </div>
                      <div style={{ borderRadius: '14px', background: '#064E3B', borderColor: 'rgba(52, 211, 153, 0.3)' }} className="p-3 border text-[11px]">
                        <div className="font-bold text-[#ECFDF5]">Doğal Kır Bahçesi & Botanik Balo Düzeni</div>
                        <div className="text-[10px] text-[#A7F3D0]">Zümrüt Yeşili & Çim Alan Organizasyonu</div>
                      </div>
                    </div>
                  </div>

                  {/* THEME PREVIEW CARD:  APPLE (2026 HUMAN INTERFACE GUIDELINES) */}
                  <div
                    onClick={() => setDraftTheme('apple')}
                    style={{ borderRadius: '20px' }}
                    className={`p-5 border-2 cursor-pointer transition-all duration-300 space-y-4 relative ${
                      draftTheme === 'apple' || draftTheme === 'apple-light'
                        ? 'border-[#0071E3] bg-[#F5F5F7] text-[#1D1D1F] shadow-xl ring-4 ring-[#0071E3]/20 scale-[1.01]'
                        : 'border-slate-200 dark:border-brand-border/60 bg-white dark:bg-brand-card hover:border-[#0071E3]/40'
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <div className="flex items-center space-x-2">
                        <span className="text-2xl"></span>
                        <div>
                          <h4 className="font-heading font-extrabold text-sm text-[#1D1D1F] dark:text-gray-100">Apple (2026 HIG Clean Design System)</h4>
                          <span className="text-[10px] text-[#86868B] font-mono font-bold">SF Pro Typography • Cupertino Blue (#0071E3) • Frosted Glass & Pill Buttons</span>
                        </div>
                      </div>
                      {(draftTheme === 'apple' || draftTheme === 'apple-light') && <span style={{ borderRadius: '980px', background: '#0071E3' }} className="text-white font-extrabold text-[10px] px-3 py-0.5 shadow">SEÇİLDİ</span>}
                    </div>

                    {/* MINI LIVE ISOLATED COMPONENT PREVIEW */}
                    <div style={{ borderRadius: '18px', background: 'rgba(255, 255, 255, 0.85)', borderColor: 'rgba(0, 0, 0, 0.08)', backdropFilter: 'blur(20px)' }} className="p-4 border space-y-3 shadow-sm">
                      <div className="text-[10px] font-bold text-[#86868B] uppercase tracking-wider"> APPLE 2026 HIG PREVIEW:</div>
                      <div className="flex items-center justify-between">
                        <span style={{ color: '#1D1D1F', letterSpacing: '-0.02em' }} className="font-heading font-extrabold text-xs">İrem Düğün Sarayı</span>
                        <div style={{ borderRadius: '980px', background: '#0071E3', color: '#ffffff', boxShadow: '0 2px 10px rgba(0, 113, 227, 0.3)' }} className="font-semibold text-[11px] px-4 py-1.5">Action Pill</div>
                      </div>
                      <div style={{ borderRadius: '14px', background: '#FFFFFF', borderColor: 'rgba(0, 0, 0, 0.06)' }} className="p-3 border text-[11px] space-y-1">
                        <div className="font-bold text-[#1D1D1F]">Royal Grand Hall</div>
                        <div className="text-[10px] text-[#86868B]">SF Pro Display • Frosted Glass Card Architecture</div>
                      </div>
                    </div>
                  </div>

                </div>

                {/* SAVE CHANGES BUTTON */}
                <div className="pt-4 border-t border-slate-200 dark:border-brand-border/40 flex justify-between items-center">
                  <div className="text-xs text-slate-500 dark:text-gray-400">
                    Seçilen Tasarım Çizgisi: <strong className="text-amber-700 dark:text-gold-400 uppercase font-mono font-bold">{draftTheme}</strong>
                  </div>
                  <button
                    type="button"
                    onClick={() => {
                      onThemeColorChange(draftTheme);
                      if (draftTheme && draftTheme !== 'gold' && draftTheme !== 'classic_gold') {
                        document.documentElement.setAttribute('data-ui-theme', draftTheme);
                      } else {
                        document.documentElement.removeAttribute('data-ui-theme');
                      }
                      
                      // CRITICAL: PERMANENTLY POST TO BACKEND SERVER DATABASE
                      try {
                        window.fetchWithRetry('/api/system-settings', {
                          method: 'POST',
                          headers: { 'Content-Type': 'application/json' },
                          body: JSON.stringify({ themeColor: draftTheme, updatedAt: new Date().toISOString(), updatedBy: 'admin' })
                        }).then(r => r.json()).then(res => {
                          console.log('✅ System theme saved to backend DB:', res);
                        }).catch(err => console.error('❌ Failed to save theme to backend DB:', err));
                      } catch(e) {}

                      showToast(`🎨 Tasarım Konsepti Başarıyla Veritabanına Kaydedildi! (${draftTheme})`);
                    }}
                    className="gold-button font-bold text-xs py-3 px-8 rounded-2xl shadow-xl hover:scale-105 transition flex items-center space-x-2"
                  >
                    <span>💾 Değişiklikleri Kaydet & Tüm Sistemde Uygula ✓</span>
                  </button>
                </div>

              </div>
            </div>
          )}

          {/* TAB 2: PERFORMANCE & CACHE */}
          {settingsTab === 'performance' && (
            <div className="space-y-6">
              <div className="glass-panel p-6 rounded-3xl space-y-6 border border-slate-200 dark:border-brand-border/40 shadow-sm">
                <h3 className="font-heading font-extrabold text-base text-slate-800 dark:text-gray-100 border-b pb-3 flex items-center space-x-2">
                  <span>⚡ Önbellekleme (Caching Engine) Yönetimi</span>
                </h3>

                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-slate-50 dark:bg-brand-dark p-4 rounded-2xl border border-slate-200 dark:border-brand-border/40">
                  <div>
                    <h4 className="font-bold text-sm text-slate-800 dark:text-gray-100">Sistem Önbellekleme (LocalStorage Persistence)</h4>
                    <p className="text-xs text-slate-500 dark:text-gray-400 mt-0.5">
                      Açık olduğunda verileriniz taranırken yerel depolamadan 0ms ile yüklenir. Kapalıyken her yenilemede canlı çekilir.
                    </p>
                  </div>

                  <label className="flex items-center space-x-3 cursor-pointer font-extrabold text-xs shrink-0 bg-white dark:bg-brand-card px-4 py-2 rounded-xl border border-slate-200 dark:border-brand-border shadow-sm">
                    <span>Önbellekleme:</span>
                    <input
                      type="checkbox"
                      checked={isCacheEnabled}
                      onChange={e => {
                        onToggleCache(e.target.checked);
                        showToast(e.target.checked ? '⚡ Önbellekleme AKTİF Edildi' : '⚠️ Önbellekleme DEVRE DIŞI Bırakıldı');
                      }}
                      className="w-5 h-5 accent-amber-600 rounded cursor-pointer"
                    />
                    <span className={isCacheEnabled ? 'text-emerald-600 font-bold' : 'text-red-500 font-bold'}>
                      {isCacheEnabled ? 'AÇIK ✓' : 'KAPALI ✕'}
                    </span>
                  </label>
                </div>

                <div className="pt-2 flex flex-col sm:flex-row justify-between items-center gap-4 border-t border-slate-200 dark:border-brand-border/40">
                  <div className="text-xs text-slate-500 dark:text-gray-400">
                    Sistem önbelleğinde saklanan kayıtlar: <strong className="text-slate-800 dark:text-gray-200">Salonlar, Ek Hizmetler, Müşteriler, Rezervasyonlar</strong>
                  </div>

                  <div className="flex flex-wrap gap-2">
                    <button
                      type="button"
                      onClick={() => {
                        if (onSeedDatabase) {
                          onSeedDatabase();
                        }
                      }}
                      className="gold-button font-extrabold px-5 py-2.5 rounded-xl text-xs shadow-md hover:scale-105 transition"
                    >
                      🏰 Veritabanını Tohumla & Tüm Varsayılanları Oluştur
                    </button>

                    <button
                      type="button"
                      onClick={() => {
                        setRedAlertModalData({
                          title: '⚠️ ÖNBELLEK VE SİSTEM VERİSİ SIFIRLANACAK',
                          message: 'Sistemde depolanan tüm yerel ayarlar, salon tercihleri ve önbellek verileri sıfırlanacaktır. Devam etmek istiyor musunuz?',
                          confirmText: 'Evet, Önbelleği Sıfırla',
                          onConfirm: () => {
                            onClearCache();
                            showToast('🗑️ Yerel Önbellek Tamamen Sıfırlandı!');
                          }
                        });
                      }}
                      className="bg-red-500/10 hover:bg-red-500 text-red-700 hover:text-white border border-red-500/40 font-bold px-5 py-2.5 rounded-xl text-xs transition shadow"
                    >
                      🗑️ Önbelleği Temizle & Sıfırla
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 3: DYNAMIC ROLES & RBAC MATRIX */}
          {settingsTab === 'rbac' && (
            <div className="space-y-6">
              {/* CREATE NEW ROLE FORM */}
              <form onSubmit={handleCreateRole} className="glass-panel p-6 rounded-3xl space-y-4 border border-amber-500/30 shadow-sm">
                <h3 className="font-heading font-extrabold text-base text-slate-800 dark:text-gray-100 border-b pb-2 flex items-center space-x-2">
                  <span>➕ Yeni Kullanıcı Rolü Tanımla</span>
                </h3>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                  <div>
                    <label className="font-bold text-slate-700 dark:text-gray-300 block mb-1">Rol Kimliği (Kod):</label>
                    <input
                      type="text"
                      placeholder="Örn: muhasebe, on_buro"
                      value={newRoleId}
                      onChange={e => setNewRoleId(e.target.value)}
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold"
                      required
                    />
                  </div>

                  <div>
                    <label className="font-bold text-slate-700 dark:text-gray-300 block mb-1">Rol Görünen Adı & İkon:</label>
                    <input
                      type="text"
                      placeholder="Örn: Muhasebe Sorumlusu 📊"
                      value={newRoleName}
                      onChange={e => setNewRoleName(e.target.value)}
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold"
                      required
                    />
                  </div>

                  <div className="flex items-end">
                    <button type="submit" className="w-full gold-button font-bold py-2.5 rounded-xl text-xs shadow hover:scale-[1.02] transition">
                      Sisteme Rolü Ekle +
                    </button>
                  </div>
                </div>
              </form>

              {/* PERMISSIONS MATRIX TABLE */}
              <div className="glass-panel p-6 rounded-3xl space-y-4 border border-slate-200 dark:border-brand-border/40 shadow-sm overflow-x-auto">
                <div className="flex justify-between items-center border-b pb-3">
                  <h3 className="font-heading font-extrabold text-base text-slate-800 dark:text-gray-100">
                    🛡️ Rol Tabanlı Sayfa İzin Matrisi (RBAC Matrix)
                  </h3>
                  <span className="text-[10px] text-amber-700 dark:text-gold-400 font-bold bg-amber-500/10 px-3 py-1 rounded-full border border-amber-500/30">
                    Canlı Güncellenir
                  </span>
                </div>

                <table className="w-full text-left border-collapse text-xs">
                  <thead>
                    <tr className="border-b border-slate-200 dark:border-brand-border/40 bg-slate-50 dark:bg-brand-dark text-slate-700 dark:text-gray-300">
                      <th className="p-3 font-extrabold rounded-l-xl">Sistem Paneli / Sayfa</th>
                      {Object.keys(roles).map(roleId => (
                        <th key={roleId} className="p-3 font-extrabold text-center whitespace-nowrap border-l border-slate-200 dark:border-brand-border/40">
                          <div className="flex flex-col items-center space-y-1">
                            <span className="text-xs">{roles[roleId]}</span>
                            <span className="text-[9px] font-mono text-slate-400">({roleId})</span>
                            <div className="flex items-center space-x-1 pt-1">
                              <button
                                type="button"
                                title="Rol Adını Düzenle"
                                onClick={() => {
                                  const name = prompt(`"${roles[roleId]}" rolü için yeni unvan yazınız:`, roles[roleId]);
                                  if (name && onEditRole) onEditRole(roleId, name);
                                }}
                                className="p-1 text-blue-500 hover:text-blue-700 hover:bg-blue-500/10 rounded transition"
                              >
                                ✏️
                              </button>
                              {roleId !== 'admin' && (
                                <button
                                  type="button"
                                  title="Rolü Sil"
                                  onClick={() => {
                                    if (confirm(`"${roles[roleId]}" (${roleId}) rolünü ve tüm izinlerini silmek istediğinize emin misiniz?`)) {
                                      if (onDeleteRole) onDeleteRole(roleId);
                                    }
                                  }}
                                  className="p-1 text-red-500 hover:text-red-700 hover:bg-red-500/10 rounded transition"
                                >
                                  🗑️
                                </button>
                              )}
                            </div>
                          </div>
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {Object.keys(TAB_LABELS).map(tabId => (
                      <tr key={tabId} className="border-b border-slate-100 dark:border-brand-border/30 hover:bg-slate-500/5 transition">
                        <td className="p-3 font-bold text-slate-800 dark:text-gray-200">
                          {TAB_LABELS[tabId]}
                        </td>
                        {Object.keys(roles).map(roleId => {
                          const isAllowed = (tabPermissions[tabId] || []).includes(roleId);
                          return (
                            <td key={roleId} className="p-3 text-center">
                              <input
                                type="checkbox"
                                checked={isAllowed}
                                onChange={() => onToggleTabPermission(tabId, roleId)}
                                className="w-4 h-4 accent-amber-600 rounded cursor-pointer"
                              />
                            </td>
                          );
                        })}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* TAB 4: ERROR & REDIRECTION PAGES LIVE SIMULATION PANEL */}
          {(settingsTab === 'error-sim' || settingsTab === 'errors') && (
            <div className="space-y-6">
              <div className="glass-panel p-6 rounded-3xl space-y-6 border border-red-500/30 shadow-md">
                <div className="flex justify-between items-center border-b pb-4 border-slate-200 dark:border-brand-border/40">
                  <div>
                    <h3 className="font-heading font-extrabold text-lg text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                      <span>🚨 Özel Hata & Yönlendirme Sayfaları Canlı Simülasyon Paneli</span>
                    </h3>
                    <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">
                      Sistemdeki HTTP 404 (Bulunamadı), 301 (Kalıcı Yönlendirme), 403 (Yetkisiz Erişim) ve 500 (Sistem Hatası) ekranlarını canlı simüle edin.
                    </p>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs font-bold">
                  {/* SIMULATE 404 */}
                  <div className="p-4 bg-amber-500/10 border border-amber-500/30 rounded-2xl space-y-2">
                    <span className="text-amber-800 dark:text-gold-400 text-sm font-extrabold flex items-center space-x-1.5">
                      <ThemeIcon icon="search" fallbackEmoji="" className="w-4 h-4 text-amber-500 shrink-0" />
                      <span>HTTP 404 - Sayfa Bulunamadı</span>
                    </span>
                    <p className="text-[11px] text-slate-600 dark:text-gray-300 font-normal">Geçersiz rota veya silinmiş içeriklerde arama çubuğu ve hızlı aksiyon butonlarıyla gösterilir.</p>
                    <button
                      onClick={() => { if (onNavigate) { onNavigate('simulasyon-404'); } else { window.location.hash = '#/simulasyon-404'; } }}
                      className="w-full bg-amber-500 text-slate-900 font-extrabold py-2 rounded-xl text-xs shadow hover:scale-[1.02] transition inline-flex items-center justify-center space-x-1.5"
                    >
                      <ThemeIcon icon="sparkles" fallbackEmoji="" className="w-3.5 h-3.5 shrink-0" />
                      <span>404 Ekranını Simüle Et</span>
                    </button>
                  </div>

                  {/* SIMULATE 301 */}
                  <div className="p-4 bg-blue-500/10 border border-blue-500/30 rounded-2xl space-y-2">
                    <span className="text-blue-700 dark:text-blue-400 text-sm font-extrabold flex items-center space-x-1.5">
                      <ThemeIcon icon="refresh" fallbackEmoji="" className="w-4 h-4 text-blue-500 shrink-0" />
                      <span>HTTP 301 - Kalıcı Yönlendirme</span>
                    </span>
                    <p className="text-[11px] text-slate-600 dark:text-gray-300 font-normal">Eski veya taşınmış rotalarda geri sayım sayacı ile otomatik hedef sayfaya yönlendirir.</p>
                    <button
                      onClick={() => { if (onNavigate) { onNavigate('simulasyon-301'); } else { window.location.hash = '#/simulasyon-301'; } }}
                      className="w-full bg-blue-600 text-white font-extrabold py-2 rounded-xl text-xs shadow hover:scale-[1.02] transition inline-flex items-center justify-center space-x-1.5"
                    >
                      <ThemeIcon icon="sparkles" fallbackEmoji="" className="w-3.5 h-3.5 shrink-0" />
                      <span>301 Ekranını Simüle Et</span>
                    </button>
                  </div>

                  {/* SIMULATE 403 */}
                  <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-2xl space-y-2">
                    <span className="text-red-700 dark:text-red-400 text-sm font-extrabold flex items-center space-x-1.5">
                      <ThemeIcon icon="shield" fallbackEmoji="" className="w-4 h-4 text-red-500 shrink-0" />
                      <span>HTTP 403 - Yetkisiz Erişim Uyarısı</span>
                    </span>
                    <p className="text-[11px] text-slate-600 dark:text-gray-300 font-normal">Kullanıcı rolünün izin vermediği sayfalarda yetki isteme butonuyla uyarı verir.</p>
                    <button
                      onClick={() => { if (onNavigate) { onNavigate('simulasyon-403'); } else { window.location.hash = '#/simulasyon-403'; } }}
                      className="w-full bg-red-600 text-white font-extrabold py-2 rounded-xl text-xs shadow hover:scale-[1.02] transition inline-flex items-center justify-center space-x-1.5"
                    >
                      <ThemeIcon icon="sparkles" fallbackEmoji="" className="w-3.5 h-3.5 shrink-0" />
                      <span>403 Ekranını Simüle Et</span>
                    </button>
                  </div>

                  {/* SIMULATE 500 */}
                  <div className="p-4 bg-purple-500/10 border border-purple-500/30 rounded-2xl space-y-2">
                    <span className="text-purple-700 dark:text-purple-400 text-sm font-extrabold flex items-center space-x-1.5">
                      <ThemeIcon icon="alert" fallbackEmoji="" className="w-4 h-4 text-purple-500 shrink-0" />
                      <span>HTTP 500 - Sunucu / Sistem Hatası</span>
                    </span>
                    <p className="text-[11px] text-slate-600 dark:text-gray-300 font-normal">Çalışma zamanı istisnalarında akordeon teknik hata detayı ve sistemi yeniden başlatma butonu sunar.</p>
                    <button
                      onClick={() => { if (onNavigate) { onNavigate('simulasyon-500'); } else { window.location.hash = '#/simulasyon-500'; } }}
                      className="w-full bg-purple-600 text-white font-extrabold py-2 rounded-xl text-xs shadow hover:scale-[1.02] transition inline-flex items-center justify-center space-x-1.5"
                    >
                      <ThemeIcon icon="sparkles" fallbackEmoji="" className="w-3.5 h-3.5 shrink-0" />
                      <span>500 Ekranını Simüle Et</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* RED ALERT CONFIRMATION MODAL */}
          {redAlertModalData && (
            <RedAlertConfirmModal
              isOpen={true}
              title={redAlertModalData.title}
              message={redAlertModalData.message}
              confirmText={redAlertModalData.confirmText}
              onConfirm={() => {
                redAlertModalData.onConfirm();
                setRedAlertModalData(null);
              }}
              onClose={() => setRedAlertModalData(null)}
            />
          )}
        </div>
      );
    }

    // --- RESERVATION DETAIL MODAL ---
