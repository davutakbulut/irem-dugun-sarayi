import re
import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add TAB_TO_SLUG and SLUG_TO_TAB mapping for system-guide
html = html.replace(
    "'settings-errors': 'ayarlar/simulasyon'",
    "'settings-errors': 'ayarlar/simulasyon',\n        'system-guide': 'sistem-kilavuzu'"
)

html = html.replace(
    "'ayarlar/simulasyon': 'settings-errors'",
    "'ayarlar/simulasyon': 'settings-errors',\n        'sistem-kilavuzu': 'system-guide'"
)

# 2. Add TAB_LABELS for system-guide
html = html.replace(
    "'settings-errors': 'Hata Simülasyonu'",
    "'settings-errors': 'Hata Simülasyonu',\n        'system-guide': 'Sistem Kılavuzu & Mimarisi'"
)

# 3. Add system-guide to TAB_PERMISSIONS default list
html = html.replace(
    "'settings-errors': ['admin'],",
    "'settings-errors': ['admin'],\n      'system-guide': ['admin', 'satisci', 'sosyal_medyaci', 'musteri'],"
)

# 4. Add SystemGuidePageComponent definition before App component
guide_component_code = """
      /* ------------------------------------------------------------------- */
      /* SYSTEM MASTER GUIDE & ARCHITECTURE PAGE COMPONENT (v1.4.45)        */
      /* ------------------------------------------------------------------- */
      function SystemGuidePageComponent({ navigateTo, activeRole, themeColor, menuLayout }) {
        const [activeSection, setActiveSection] = useState('overview');

        const systemPages = [
          { id: 'dashboard', title: 'Anasayfa / İstatistikler', icon: 'chart', emoji: '📊', desc: 'Canlı finansal ve operasyonel istatistikler, AI önerileri, takvim önizleme, VIP hızlı eylem butonları.' },
          { id: 'create-reservation', title: 'Yeni Rezervasyon Oluştur', icon: 'sparkles', emoji: '✨', desc: '4 adımlı sözleşme sihirbazı, salon ve ek hizmet seçimi, tarih/saat çakışma önleyici, mobil kayan bakiye çekmecesi.' },
          { id: 'reservations', title: 'Rezervasyon Listesi & Sözleşmeler', icon: 'list', emoji: '📋', desc: 'Arama/filtreleme, yazdırılabilir fatura/sözleşme modalı, e-posta bilgilendirme modalı, canlı ödeme durumları.' },
          { id: 'calendar', title: 'İnteraktif Takvim', icon: 'calendar', emoji: '📅', desc: 'Dinamik ay navigasyonu, gün bazlı rezervasyon detayları, takvim üzerinden doğrudan yeni rezervasyon tetikleme.' },
          { id: 'venues', title: 'Düğün Salonları', icon: 'venue', emoji: '🏰', desc: 'Salon kapasite ve VIP fiyat yönetimi, görsel detay modalı, salon ekleme/düzenleme/silme.' },
          { id: 'services', title: 'Ek Hizmetler', icon: 'gift', emoji: '🎁', desc: 'Sabit, kişi başı ve saatlik fiyatlandırma türleri, ek hizmet tanımlama ve yönetim paneli.' },
          { id: 'finance', title: 'Finans Kasa & Gider Yönetimi', icon: 'money', emoji: '💰', desc: 'Gelir/gider işlem kaydı tablosu, gider ekleme modalı, net kasa dengesi ve finansal özet.' },
          { id: 'customers', title: 'Müşteri Rehberi (CRM)', icon: 'user', emoji: '👥', desc: 'Müşteri iletişim kartları, geçmiş rezervasyon kayıtları, CRM müşteri yönetimi.' },
          { id: 'campaigns', title: 'Kampanyalar & AI Önerileri', icon: 'campaign', emoji: '🏷️', desc: 'Aktif sezon indirimleri, AI önerilerini tek tıkla kampanyaya dönüştürme ve salona uygulama.' },
          { id: 'reports', title: 'Raporlar & Analizler', icon: 'chart', emoji: '📈', desc: 'SVG Gelir Dağılımı Donut Grafiği, Salon Tercih Oranları Bar Grafiği, dinamik doluluk hesabı.' },
          { id: 'media', title: 'Medya & Galeri Yükleyici', icon: 'camera', emoji: '📸', desc: 'Çoklu fotoğraf yükleme, mükerrer resim yükleme engelleme, galeri filtreleme.' },
          { id: 'mind-map', title: 'Zihin Haritası (Mind Map)', icon: 'sparkles', emoji: '🧠', desc: 'İnteraktif mimari ve fonksiyon düğüm şeması, sistem modülleri görselleştirmesi.' },
          { id: 'roles', title: 'Rol Yönetimi & İzin Matrisi (RBAC)', icon: 'shield', emoji: '🛡️', desc: 'Dinamik rol tanımlama (Admin, Satışçı, Müşteri vb.), sayfa bazlı izin erişim matrisi.' },
          { id: 'users', title: 'Kullanıcı Yönetimi', icon: 'user', emoji: '👥', desc: 'Kullanıcı hesapları, rol atama, şifre belirleme ve üye yönetimi.' },
          { id: 'profile', title: 'Profil Yönetimi', icon: 'user', emoji: '👤', desc: 'Profil resmi, kişisel bilgiler, şifre güncelleme ve hızlı rol değiştirici.' },
          { id: 'settings', title: 'Sistem Ayarları', icon: 'settings', emoji: '⚙️', desc: 'Görünüm ve 11 tema seçimi, Masaüstü Menü Düzeni (Dikey Sol / Yatay Üst), Hata Simülasyonu (404, 301, 403, 500), Önbellek Yönetimi.' }
        ];

        const themesList = [
          { id: 'gold', name: '👑 Altın & Şampanya (Klasik Gold)', desc: 'Altın ve canlı turuncu gradyanlar, yuvarlak hatlar (rounded-2xl).' },
          { id: 'emerald', name: '💎 Zümrüt Yeşili (Royal Emerald)', desc: 'Asil zümrüt yeşili tonları, keskin oval köşeler (rounded-xl).' },
          { id: 'sapphire', name: '🔷 Gece Mavisi (Deep Sapphire)', desc: 'Derin gece mavisi, kurumsal ve şık tasarım (rounded-xl).' },
          { id: 'rose', name: '🌸 Gül Altını (Rose Gold)', desc: 'Zarif pembe ve gül altını gradyanları (rounded-2xl).' },
          { id: 'violet', name: '🍇 Gece Moru (Midnight Violet)', desc: 'Gizemli mor ve leylak tonları (rounded-xl).' },
          { id: 'obsidian', name: '⬛ Obsidian Gold (Kurumsal Siyah & Altın)', desc: 'Lüks siyah & altın, tam keskin köşeler (rounded-none).' },
          { id: 'sapphire_clean', name: '💎 Sapphire Clean (Safir Mavisi Minimal)', desc: 'Minimalist açık safir mavisi, hafif oval (rounded-md).' },
          { id: 'platinum', name: '🪙 Platinum Silver (Platin Gümüş VIP)', desc: 'VIP platin gümüş ve füme tonları (rounded-lg).' },
          { id: 'emerald_royal', name: '🌲 Emerald Royal (Kraliyet Zümrütü)', desc: 'Koyu orman yeşili ve altın detaylar (rounded-2xl).' },
          { id: 'titanium', name: '⚡ Titanium Tech (Titanyum Metal)', desc: 'Teknolojik koyu titanyum ve mavi vurucu noktalar (rounded-md).' },
          { id: 'apple', name: ' Apple (2026 HIG Clean Design System)', desc: 'Apple HIG vizyonu, buzlu cam ve tam yuvarlak butonlar (rounded-full).' }
        ];

        const vercelSkillsList = [
          { name: 'find-skills', desc: 'Açık ajan ekosisteminden yeni yetenek arama ve bağlama.' },
          { name: 'web-design-guidelines', desc: 'Vercel UX/UI standartları, tipografi ve renk rehberi.' },
          { name: 'react-best-practices', desc: 'React & Next.js 0ms render ve performans optimizasyon kuralları.' },
          { name: 'composition-patterns', desc: 'İleri seviye bileşen mimarisi ve prop desenleri.' },
          { name: 'react-view-transitions', desc: 'Sayfa ve eleman arası yumuşak animasyon geçişleri.' },
          { name: 'vercel-optimize', desc: 'Tam kaynak kodu tarama ve performans teşhis araçları.' },
          { name: 'deploy-to-vercel', desc: 'Vercel canlı yayın ve dağıtım otomasyonu.' },
          { name: 'writing-guidelines', desc: 'Kurumsal metin ve mikro-kopya yazım kuralları.' },
          { name: 'vercel-cli-with-tokens', desc: 'Vercel CLI ve ortam değişkenleri yönetimi.' },
          { name: 'react-native-skills', desc: 'Mobil cihaz uyumluluk standartları.' }
        ];

        return (
          <div className="w-full space-y-8 animate-fade-in pb-16">
            {/* HERO HEADER */}
            <div className="glass-panel p-6 sm:p-8 rounded-3xl border-2 border-amber-500/40 bg-gradient-to-r from-amber-500/10 via-slate-900/80 to-amber-500/10 shadow-xl relative overflow-hidden text-slate-800 dark:text-gray-100">
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 relative z-10">
                <div className="space-y-2">
                  <div className="flex items-center space-x-2">
                    <span className="text-2xl">📖</span>
                    <h2 className="text-2xl sm:text-3xl font-heading font-black gold-gradient-text tracking-wide uppercase">
                      İrem Düğün Sarayı — Sistem Master Kılavuzu & Mimarisi
                    </h2>
                  </div>
                  <p className="text-xs sm:text-sm text-slate-600 dark:text-gray-300 font-medium leading-relaxed max-w-3xl">
                    Bu sayfa, platform içerisindeki tüm sayfaların, modüllerin, 11 adet kurumsal temanın, veritabanı mimarisinin ve 10 adet Vercel Labs Ajan Yeteneğinin eksiksiz kütüphanesidir.
                  </p>
                </div>
                <div className="flex flex-wrap items-center gap-2 shrink-0">
                  <span className="px-3.5 py-1.5 rounded-full bg-emerald-500/20 text-emerald-700 dark:text-emerald-300 border border-emerald-500/40 font-black text-xs shadow-xs">
                    Sistem Sürümü: v1.4.45
                  </span>
                  <span className="px-3.5 py-1.5 rounded-full bg-amber-500/20 text-amber-800 dark:text-gold-400 border border-amber-500/40 font-black text-xs shadow-xs">
                    Aktif Tema: {themeColor || 'nordic-light'}
                  </span>
                </div>
              </div>
            </div>

            {/* NAVIGATION TAB BAR */}
            <div className="flex flex-wrap gap-2 border-b border-slate-200 dark:border-brand-border/40 pb-3">
              {[
                { id: 'overview', label: '🏛️ Mimari Özeti', icon: 'settings' },
                { id: 'pages', label: '📱 16 Sayfa & Modül', icon: 'list' },
                { id: 'themes', label: '🎨 11 Kurumsal Tema', icon: 'sparkles' },
                { id: 'skills', label: '🚀 10 Vercel Ajan Skills', icon: 'shield' }
              ].map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveSection(tab.id)}
                  className={`px-4 py-2.5 rounded-xl font-bold text-xs transition-all duration-200 flex items-center space-x-2 cursor-pointer ${
                    activeSection === tab.id
                      ? 'gold-button shadow-md scale-[1.02]'
                      : 'bg-white dark:bg-brand-card text-slate-700 dark:text-gray-300 border border-slate-200 dark:border-brand-border hover:border-amber-500/50'
                  }`}
                >
                  <span>{tab.label}</span>
                </button>
              ))}
            </div>

            {/* SECTION 1: ARCHITECTURE OVERVIEW */}
            {activeSection === 'overview' && (
              <div className="space-y-6 animate-fade-in">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="glass-panel p-6 rounded-3xl border border-amber-500/30 space-y-3 shadow-md">
                    <div className="w-10 h-10 rounded-2xl bg-amber-500/20 text-amber-500 flex items-center justify-center text-xl font-bold">🗄️</div>
                    <h3 className="font-heading font-extrabold text-base text-slate-800 dark:text-gray-100">Tek Sunucu Veritabanı Mimarisi</h3>
                    <p className="text-xs text-slate-500 dark:text-gray-400 leading-relaxed">
                      Tema ve Masaüstü Menü seçimi dahil tüm Genel Ayarlar <code className="bg-amber-500/10 px-1.5 py-0.5 rounded text-amber-600 font-mono">/api/system-settings</code> REST endpointi üzerinden sunucunun <code className="bg-amber-500/10 px-1.5 py-0.5 rounded text-amber-600 font-mono">db_system_settings.json</code> veritabanına kaydedilir.
                    </p>
                  </div>

                  <div className="glass-panel p-6 rounded-3xl border border-amber-500/30 space-y-3 shadow-md">
                    <div className="w-10 h-10 rounded-2xl bg-emerald-500/20 text-emerald-500 flex items-center justify-center text-xl font-bold">⚡</div>
                    <h3 className="font-heading font-extrabold text-base text-slate-800 dark:text-gray-100">0ms Server HTML Enjeksiyonu</h3>
                    <p className="text-xs text-slate-500 dark:text-gray-400 leading-relaxed">
                      Sunucu ilk HTTP yanıtında veritabanındaki aktif temayı ve menü düzenini doğrudan yanıt HTML etiketine <code className="bg-emerald-500/10 px-1.5 py-0.5 rounded text-emerald-600 font-mono">data-ui-theme</code> ve <code className="bg-emerald-500/10 px-1.5 py-0.5 rounded text-emerald-600 font-mono">data-menu-layout</code> olarak basar. Sıfır renk sıçraması yaşanır.
                    </p>
                  </div>

                  <div className="glass-panel p-6 rounded-3xl border border-amber-500/30 space-y-3 shadow-md">
                    <div className="w-10 h-10 rounded-2xl bg-blue-500/20 text-blue-500 flex items-center justify-center text-xl font-bold">🔄</div>
                    <h3 className="font-heading font-extrabold text-base text-slate-800 dark:text-gray-100">Ağ Dayanıklılığı & Retry Koruması</h3>
                    <p className="text-xs text-slate-500 dark:text-gray-400 leading-relaxed">
                      Sunucu yenilenmelerinde veya mikro kesintilerde <code className="bg-blue-500/10 px-1.5 py-0.5 rounded text-blue-600 font-mono">window.fetchWithRetry</code> devreye girerek ağ isteklerini 3 kez otomatik olarak yeniden dener.
                    </p>
                  </div>
                </div>

                <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border space-y-4">
                  <h3 className="font-heading font-extrabold text-lg text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                    <span>🛠️ Üretim Derleme Mimarisi & Önbellek Kırma (Cache-Busting)</span>
                  </h3>
                  <p className="text-xs text-slate-600 dark:text-gray-300 leading-relaxed">
                    Uygulamamızdaki tüm JSX bileşenleri <code className="bg-slate-100 dark:bg-brand-dark px-2 py-1 rounded font-mono">scratch/build_precompiled.py</code> betiği ile Babel standalone kullanılarak önceden derlenir ve <code className="bg-slate-100 dark:bg-brand-dark px-2 py-1 rounded font-mono">src/app.compiled.js</code> dosyasına kaydedilir. Yükleme scripti <code className="bg-slate-100 dark:bg-brand-dark px-2 py-1 rounded font-mono">src/app.compiled.js?v=timestamp</code> parametresiyle çağrılarak tarayıcının her zaman taze JavaScript çalıştırması garanti altına alınır.
                  </p>
                </div>
              </div>
            )}

            {/* SECTION 2: ALL PAGES & MODULES */}
            {activeSection === 'pages' && (
              <div className="space-y-4 animate-fade-in">
                <div className="flex justify-between items-center">
                  <h3 className="font-heading font-extrabold text-lg text-slate-800 dark:text-gray-100">
                    Sistemde Yer Alan 16 Ana Sayfa ve Modül
                  </h3>
                  <span className="text-xs font-bold px-3 py-1 rounded-full bg-amber-500/10 text-amber-700 dark:text-gold-400 border border-amber-500/20">
                    Toplam: 16 Modül
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {systemPages.map((page, idx) => (
                    <div key={page.id} className="glass-panel p-5 rounded-2xl border border-slate-200 dark:border-brand-border/60 hover:border-amber-500/50 transition space-y-2">
                      <div className="flex justify-between items-center">
                        <div className="flex items-center space-x-2 font-bold text-sm text-slate-800 dark:text-gray-100">
                          <span className="text-lg">{page.emoji}</span>
                          <span>{idx + 1}. {page.title}</span>
                        </div>
                        <button
                          onClick={() => navigateTo && navigateTo(page.id)}
                          className="text-[10px] font-extrabold px-2.5 py-1 rounded-lg gold-button transition hover:scale-105 cursor-pointer"
                        >
                          Sayfaya Git →
                        </button>
                      </div>
                      <p className="text-xs text-slate-500 dark:text-gray-400 leading-relaxed">
                        {page.desc}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* SECTION 3: ALL 11 CORPORATE THEMES */}
            {activeSection === 'themes' && (
              <div className="space-y-4 animate-fade-in">
                <div className="flex justify-between items-center">
                  <h3 className="font-heading font-extrabold text-lg text-slate-800 dark:text-gray-100">
                    11 Adet Kurumsal UI Tema ve Renk Paleti
                  </h3>
                  <span className="text-xs font-bold px-3 py-1 rounded-full bg-amber-500/10 text-amber-700 dark:text-gold-400 border border-amber-500/20">
                    Sürüm: 2026 Premium Design
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {themesList.map((t) => (
                    <div
                      key={t.id}
                      className={`glass-panel p-5 rounded-2xl border-2 transition space-y-2 ${
                        (themeColor || 'nordic-light') === t.id
                          ? 'border-amber-500 bg-amber-500/10 shadow-lg ring-2 ring-amber-500/20'
                          : 'border-slate-200 dark:border-brand-border'
                      }`}
                    >
                      <div className="flex justify-between items-center">
                        <h4 className="font-bold text-sm text-slate-800 dark:text-gray-100">{t.name}</h4>
                        {(themeColor || 'nordic-light') === t.id && (
                          <span className="text-[9px] font-black px-2 py-0.5 rounded-full gold-button">AKTİF</span>
                        )}
                      </div>
                      <p className="text-xs text-slate-500 dark:text-gray-400 leading-relaxed">
                        {t.desc}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* SECTION 4: VERCEL LABS SKILLS */}
            {activeSection === 'skills' && (
              <div className="space-y-4 animate-fade-in">
                <div className="flex justify-between items-center">
                  <h3 className="font-heading font-extrabold text-lg text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                    <span>🚀 10 Adet Vercel Labs Ajan Yeteneği (skills.sh)</span>
                  </h3>
                  <span className="text-xs font-bold px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30">
                    Konum: .skills/
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {vercelSkillsList.map((s, idx) => (
                    <div key={s.name} className="glass-panel p-5 rounded-2xl border border-slate-200 dark:border-brand-border space-y-2">
                      <div className="flex justify-between items-center">
                        <div className="font-bold text-xs font-mono text-amber-700 dark:text-gold-400 flex items-center space-x-1.5">
                          <span>{idx + 1}.</span>
                          <span>vercel-labs/{s.name}</span>
                        </div>
                        <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-slate-100 dark:bg-brand-card text-slate-600 dark:text-gray-300 border border-slate-200 dark:border-brand-border">
                          SKILL.md
                        </span>
                      </div>
                      <p className="text-xs text-slate-500 dark:text-gray-400 leading-relaxed">
                        {s.desc}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        );
      }
"""

if "function SystemGuidePageComponent" not in html:
    idx = html.find("function App()")
    if idx != -1:
        html = html[:idx] + guide_component_code + "\n\n      " + html[idx:]
        print("Added SystemGuidePageComponent definition to index.html!")

# 5. Add route renderer for activeTab === 'system-guide' in App component
old_render_route = "activeTab==='simulasyon-500'&&/*#__PURE__*/React.createElement(ServerErrorScreen"

new_render_route = """activeTab==='system-guide'&&<SystemGuidePageComponent navigateTo={navigateTo} activeRole={activeRole} themeColor={themeColor} menuLayout={menuLayout} />,
            activeTab==='simulasyon-500'&&/*#__PURE__*/React.createElement(ServerErrorScreen"""

if old_render_route in html and "activeTab==='system-guide'" not in html:
    html = html.replace(old_render_route, new_render_route)
    print("Added system-guide route renderer to App component in index.html!")

# 6. Add "Sistem Kılavuzu & Mimarisi" at the very bottom of the Navigation Menu under YÖNETİM & AYARLAR
old_settings_nav_item = "{id:'settings',label:'Sistem Ayarları',icon:'settings',fallbackEmoji:'⚙️'}"
new_settings_nav_item = "{id:'settings',label:'Sistem Ayarları',icon:'settings',fallbackEmoji:'⚙️'},\n                  {id:'system-guide',label:'Sistem Kılavuzu & Mimarisi',icon:'sparkles',fallbackEmoji:'📖',badge:'V1.4'}"

if old_settings_nav_item in html and "system-guide" not in html:
    html = html.replace(old_settings_nav_item, new_settings_nav_item)
    print("Added Sistem Kılavuzu & Mimarisi to bottom of navigation menu in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with Master System Instruction & Architecture Page successfully!")
