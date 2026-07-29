import React from 'react';

export function SettingsPage({ currentTheme, onThemeChange, buttonStyle, onButtonStyleChange }) {
  const corporateThemes = [
    {
      id: 'obsidian-gold',
      name: 'Obsidian Gold (Varsayılan Lüks)',
      badge: 'KURUMSAL KONSEPT',
      accentColor: '#d97706',
      bgPreview: 'bg-slate-900',
      description: 'Derin obsidyen siyahı ve 24k altın ışıltılarıyla zenginleştirilmiş VIP balo konsepti.'
    },
    {
      id: 'sapphire-clean',
      name: 'Sapphire Clean (Modern Safir)',
      badge: 'KURUMSAL DİJİTAL',
      accentColor: '#2563eb',
      bgPreview: 'bg-slate-950',
      description: 'Safir mavisi ve beyaz tonlarda ultra net, kurumsal ve ferah yönetim arayüzü.'
    },
    {
      id: 'platinum-silver',
      name: 'Platinum Silver (Aydınlık Platin)',
      badge: 'LIGHT TEMA',
      accentColor: '#475569',
      bgPreview: 'bg-slate-100',
      description: 'Platin grisi, gümüş vurgular ve göz yormayan aydınlık kurumsal tasarım.'
    },
    {
      id: 'emerald-royal',
      name: 'Emerald Royal (Kraliyet Zümrütü)',
      badge: 'VIP KONSEPT',
      accentColor: '#059669',
      bgPreview: 'bg-emerald-950',
      description: 'Zümrüt yeşili ve koyu tonlarla doğa ile lüksü buluşturan premium tema.'
    },
    {
      id: 'titanium-tech',
      name: 'Titanium Tech (Teknolojik Titanyum)',
      badge: 'DARK TECH',
      accentColor: '#64748b',
      bgPreview: 'bg-zinc-950',
      description: 'Titanyum grisi ve neon çizgi efektleriyle yüksek teknolojili yönetim deneyimi.'
    }
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto animate-fade-in">
      {/* HEADER */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex justify-between items-center shadow-sm">
        <div>
          <h2 className="text-xl sm:text-2xl font-heading font-extrabold text-slate-900 dark:text-white">
            ⚙️ Sistem Ayarları & 5 Kurumsal Tema Tercihi
          </h2>
          <p className="text-xs text-slate-500 dark:text-gray-400">
            Arayüz görünümünü kurum kimliğinize göre özelleştirin, buton keskinliklerini ayarlayın.
          </p>
        </div>
      </div>

      {/* THEMES SELECTION CARDS */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border space-y-4 shadow-sm">
        <h3 className="font-heading font-bold text-base text-slate-900 dark:text-white flex items-center space-x-2">
          <span>🎨</span>
          <span>5 Kurumsal Arayüz Renk Teması</span>
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
                  <div className="flex justify-between items-center">
                    <span className="text-[9px] font-extrabold bg-slate-200 dark:bg-brand-card text-slate-700 dark:text-gray-300 px-2 py-0.5 rounded-full">
                      {theme.badge}
                    </span>
                    {isSelected && (
                      <span className="text-[10px] font-extrabold gold-button px-2.5 py-0.5 rounded-full shadow">
                        AKTİF TEMA ✓
                      </span>
                    )}
                  </div>

                  <h4 className="font-heading font-extrabold text-sm text-slate-900 dark:text-white">
                    {theme.name}
                  </h4>
                  <p className="text-xs text-slate-500 dark:text-gray-400">{theme.description}</p>
                </div>

                <div className="pt-2 border-t border-slate-200 dark:border-brand-border flex items-center space-x-2">
                  <div className="w-5 h-5 rounded-full border border-white/40 shadow-sm" style={{ backgroundColor: theme.accentColor }}></div>
                  <span className="text-[10px] font-bold text-slate-500">Vurgu Rengi Kodu: {theme.accentColor}</span>
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
            onClick={() => onNavigate && onNavigate('404')}
            className="p-3 bg-amber-500/10 text-amber-800 dark:text-gold-400 border border-amber-500/30 rounded-2xl hover:bg-amber-500/20 transition flex flex-col items-center space-y-1"
          >
            <span className="text-xl">🔍</span>
            <span>404 Bulunamadı</span>
          </button>

          <button
            onClick={() => onNavigate && onNavigate('301')}
            className="p-3 bg-amber-500/10 text-amber-800 dark:text-gold-400 border border-amber-500/30 rounded-2xl hover:bg-amber-500/20 transition flex flex-col items-center space-y-1"
          >
            <span className="text-xl">🔄</span>
            <span>301 Yönlendirme</span>
          </button>

          <button
            onClick={() => onNavigate && onNavigate('403')}
            className="p-3 bg-red-500/10 text-red-700 dark:text-red-400 border border-red-500/30 rounded-2xl hover:bg-red-500/20 transition flex flex-col items-center space-y-1"
          >
            <span className="text-xl">🛡️</span>
            <span>403 Yetkisiz Erişim</span>
          </button>

          <button
            onClick={() => onNavigate && onNavigate('500')}
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
