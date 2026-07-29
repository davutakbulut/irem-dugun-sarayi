import React from 'react';
import { THEME_PALETTES } from '../constants';
import { ThemeIcon } from '../components/ThemeIcon';

export function SettingsPage({ currentTheme, onThemeChange, buttonStyle, onButtonStyleChange, onNavigate }) {
  const corporateThemes = THEME_PALETTES;

  return (
    <div className="space-y-6 max-w-7xl mx-auto animate-fade-in">
      {/* HEADER */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex justify-between items-center shadow-sm">
        <div>
          <h2 className="text-xl sm:text-2xl font-heading font-extrabold text-slate-900 dark:text-white flex items-center space-x-2">
            <ThemeIcon icon="settings" fallbackEmoji="⚙️" className="w-6 h-6 text-amber-500 shrink-0" />
            <span>Sistem Ayarları & Kurumsal Tema Tercihleri</span>
          </h2>
          <p className="text-xs text-slate-500 dark:text-gray-400">
            Arayüz görünümünü kurum kimliğinize göre özelleştirin, buton keskinliklerini ayarlayın.
          </p>
        </div>
      </div>

      {/* THEMES SELECTION CARDS */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border space-y-4 shadow-sm">
        <h3 className="font-heading font-bold text-base text-slate-900 dark:text-white flex items-center space-x-2">
          <ThemeIcon icon="paint" fallbackEmoji="🎨" className="w-5 h-5 text-amber-500 shrink-0" />
          <span>Kurumsal Arayüz Renk Teması</span>
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {corporateThemes.map(theme => {
            const isSelected = currentTheme === theme.id;
            return (
              <div
                key={theme.id}
                onClick={() => onThemeChange(theme.id)}
                className={`p-5 rounded-3xl border-2 transition-all duration-300 cursor-pointer space-y-3 flex flex-col justify-between shadow-sm ${
                  isSelected
                    ? 'border-amber-500 bg-amber-500/10 ring-2 ring-amber-500/40'
                    : 'border-slate-200 dark:border-brand-border bg-slate-50 dark:bg-brand-dark hover:border-amber-500/50'
                }`}
              >
                <div className="space-y-2">
                  <div className="flex justify-between items-center flex-wrap gap-1">
                    <span className="text-[9px] font-extrabold bg-slate-200 dark:bg-brand-card text-slate-700 dark:text-gray-300 px-2 py-0.5 rounded-full">
                      {theme.isZeroEmoji ? '❄️ SIFIR EMOJİ DIRECTIVE' : (theme.geometry || 'KURUMSAL KONSEPT')}
                    </span>
                    {isSelected && (
                      <span className="text-[10px] font-extrabold gold-button px-2.5 py-0.5 rounded-full shadow">
                        AKTİF TEMA ✓
                      </span>
                    )}
                  </div>

                  <h4 className="font-heading font-extrabold text-sm text-slate-900 dark:text-white flex items-center space-x-2">
                    <span>{theme.name}</span>
                  </h4>
                  <p className="text-xs text-slate-500 dark:text-gray-400">{theme.description}</p>
                </div>

                <div className="pt-2 border-t border-slate-200 dark:border-brand-border flex items-center justify-between text-[10px] font-bold">
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 rounded-full border border-white/40 shadow-sm" style={{ backgroundColor: theme.primaryColor }}></div>
                    <span className="text-slate-500">{theme.primaryColor}</span>
                  </div>
                  <span className="bg-slate-100 dark:bg-brand-card px-2 py-0.5 rounded text-amber-600 dark:text-gold-400">
                    Geometri: {theme.geometry || 'rounded-md'}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* BUTTON ROUNDNESS / SHARPNESS */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border space-y-4 shadow-sm">
        <h3 className="font-heading font-bold text-base text-slate-900 dark:text-white flex items-center space-x-2">
          <span>🔲</span>
          <span>Buton ve Kart Keskinlik Stili</span>
        </h3>

        <div className="flex flex-wrap gap-4 text-xs font-bold">
          <button
            onClick={() => onButtonStyleChange('rounded-xl')}
            className={`px-5 py-3 rounded-xl border transition ${buttonStyle === 'rounded-xl' ? 'gold-button shadow' : 'bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300'}`}
          >
            Özel Yuvarlatılmış Kavisli (Rounded XL)
          </button>
          <button
            onClick={() => onButtonStyleChange('rounded-none')}
            className={`px-5 py-3 rounded-none border transition ${buttonStyle === 'rounded-none' ? 'gold-button shadow' : 'bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300'}`}
          >
            Keskin Kurumsal Köşeler (Rounded None)
          </button>
        </div>
      </div>

      {/* ERROR & REDIRECT PAGES TEST PANEL */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border space-y-4 shadow-sm">
        <div>
          <h3 className="font-heading font-bold text-base text-slate-900 dark:text-white flex items-center space-x-2">
            <span>🚨</span>
            <span>Hata & Yönlendirme Sayfaları Canlı Simülasyon Paneli</span>
          </h3>
          <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">
            HTTP 404 Sayfa Bulunamadı, 301 Kalıcı Yönlendirme, 403 Yetkisiz Erişim ve 500 Sistem Hatası sayfalarını canlı olarak önizleyin.
          </p>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-bold">
          <button
            onClick={() => onNavigate && onNavigate('simulasyon-404')}
            className="p-3 bg-amber-500/10 text-amber-800 dark:text-gold-400 border border-amber-500/30 rounded-2xl hover:bg-amber-500/20 transition flex flex-col items-center space-y-1"
          >
            <span className="text-xl">🔍</span>
            <span>404 Bulunamadı</span>
          </button>

          <button
            onClick={() => onNavigate && onNavigate('simulasyon-301')}
            className="p-3 bg-amber-500/10 text-amber-800 dark:text-gold-400 border border-amber-500/30 rounded-2xl hover:bg-amber-500/20 transition flex flex-col items-center space-y-1"
          >
            <span className="text-xl">🔄</span>
            <span>301 Yönlendirme</span>
          </button>

          <button
            onClick={() => onNavigate && onNavigate('simulasyon-403')}
            className="p-3 bg-red-500/10 text-red-700 dark:text-red-400 border border-red-500/30 rounded-2xl hover:bg-red-500/20 transition flex flex-col items-center space-y-1"
          >
            <span className="text-xl">🛡️</span>
            <span>403 Yetkisiz Erişim</span>
          </button>

          <button
            onClick={() => onNavigate && onNavigate('simulasyon-500')}
            className="p-3 bg-red-500/10 text-red-700 dark:text-red-400 border border-red-500/30 rounded-2xl hover:bg-red-500/20 transition flex flex-col items-center space-y-1"
          >
            <span className="text-xl">💥</span>
            <span>500 Sunucu Hatası</span>
          </button>
        </div>
      </div>
    </div>
  );
}
