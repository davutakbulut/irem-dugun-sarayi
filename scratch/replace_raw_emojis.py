import re

file_path = '/Users/davutakbulut/.gemini/antigravity/scratch/irem_dugun_sarayi/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Exact replacement dictionary for specific JSX lines/strings
replacements = {
    '<div class="logo">👑 İREM DÜĞÜN SARAYI</div>': '<div class="logo"><ThemeIcon icon="crown" fallbackEmoji="👑" className="w-5 h-5 inline-block mr-1" /> İREM DÜĞÜN SARAYI</div>',
    '<span>👤</span>': '<ThemeIcon icon="user" fallbackEmoji="👤" className="w-4 h-4 shrink-0 inline-block" />',
    '<span>⚙️</span>': '<ThemeIcon icon="settings" fallbackEmoji="⚙️" className="w-4 h-4 shrink-0 inline-block" />',
    '<span>🚪</span>': '<ThemeIcon icon="door" fallbackEmoji="🚪" className="w-4 h-4 shrink-0 inline-block" />',
    '<span className="text-base">⚙️</span>': '<ThemeIcon icon="settings" fallbackEmoji="⚙️" className="w-4 h-4 shrink-0 inline-block" />',
    '<span className="text-base">🎨</span>': '<ThemeIcon icon="paint" fallbackEmoji="🎨" className="w-4 h-4 shrink-0 inline-block" />',
    '<span className="text-base">⚡</span>': '<ThemeIcon icon="zap" fallbackEmoji="⚡" className="w-4 h-4 shrink-0 inline-block" />',
    '<span className="text-base">🛡️</span>': '<ThemeIcon icon="shield" fallbackEmoji="🛡️" className="w-4 h-4 shrink-0 inline-block" />',
    '<span>🎨</span>': '<ThemeIcon icon="paint" fallbackEmoji="🎨" className="w-4 h-4 shrink-0 inline-block" />',
    '<span>⚡</span>': '<ThemeIcon icon="zap" fallbackEmoji="⚡" className="w-4 h-4 shrink-0 inline-block" />',
    '<span>🛡️</span>': '<ThemeIcon icon="shield" fallbackEmoji="🛡️" className="w-4 h-4 shrink-0 inline-block" />',
    '<span>➕</span>': '<ThemeIcon icon="plus" fallbackEmoji="➕" className="w-4 h-4 shrink-0 inline-block" />',
    '<span>📅</span>': '<ThemeIcon icon="calendar" fallbackEmoji="📅" className="w-4 h-4 shrink-0 inline-block" />',
    '<span>🎁</span>': '<ThemeIcon icon="gift" fallbackEmoji="🎁" className="w-4 h-4 shrink-0 inline-block" />',
    '<span>💡</span>': '<ThemeIcon icon="idea" fallbackEmoji="💡" className="w-4 h-4 shrink-0 inline-block" />',
    '<span>🎉</span>': '<ThemeIcon icon="celebrate" fallbackEmoji="🎉" className="w-4 h-4 shrink-0 inline-block" />',
    '<span>📄</span>': '<ThemeIcon icon="print" fallbackEmoji="📄" className="w-4 h-4 shrink-0 inline-block" />',
    '<span>✉️</span>': '<ThemeIcon icon="email" fallbackEmoji="✉️" className="w-4 h-4 shrink-0 inline-block" />',
    '<span>💳</span>': '<ThemeIcon icon="card" fallbackEmoji="💳" className="w-4 h-4 shrink-0 inline-block" />',
    '<span>📜</span>': '<ThemeIcon icon="document" fallbackEmoji="📜" className="w-4 h-4 shrink-0 inline-block" />',
    '<span>📝</span>': '<ThemeIcon icon="notes" fallbackEmoji="📝" className="w-4 h-4 shrink-0 inline-block" />',
    '<span>🔍</span>': '<ThemeIcon icon="search" fallbackEmoji="🔍" className="w-4 h-4 shrink-0 inline-block" />',
    '<span>📍': '<span><ThemeIcon icon="location" fallbackEmoji="📍" className="w-3.5 h-3.5 inline-block mr-1" />',

    # Navigation menu items labels
    "{ id: 'create-reservation', label: '➕ Yeni Rezervasyon Oluştur',": "{ id: 'create-reservation', label: 'Yeni Rezervasyon Oluştur',",

    # Headers in Modals & Forms
    "{venue ? '🏰 Düğün Salonunu Düzenle' : '➕ Yeni Düğün Salonu Ekle'}": "{venue ? <><ThemeIcon icon=\"venue\" fallbackEmoji=\"🏰\" className=\"w-5 h-5 inline-block mr-1.5 text-amber-500\" /> Düğün Salonunu Düzenle</> : <><ThemeIcon icon=\"plus\" fallbackEmoji=\"➕\" className=\"w-5 h-5 inline-block mr-1.5 text-amber-500\" /> Yeni Düğün Salonu Ekle</>}",
    "{service ? '✨ Ek Hizmeti Düzenle' : '➕ Yeni Ek Hizmet Ekle'}": "{service ? <><ThemeIcon icon=\"sparkles\" fallbackEmoji=\"✨\" className=\"w-5 h-5 inline-block mr-1.5 text-amber-500\" /> Ek Hizmeti Düzenle</> : <><ThemeIcon icon=\"plus\" fallbackEmoji=\"➕\" className=\"w-5 h-5 inline-block mr-1.5 text-amber-500\" /> Yeni Ek Hizmet Ekle</>}",
    "{campaign ? '🎁 Kampanyayı Düzenle' : '➕ Yeni Özel Kampanya Ekle'}": "{campaign ? <><ThemeIcon icon=\"gift\" fallbackEmoji=\"🎁\" className=\"w-5 h-5 inline-block mr-1.5 text-amber-500\" /> Kampanyayı Düzenle</> : <><ThemeIcon icon=\"plus\" fallbackEmoji=\"➕\" className=\"w-5 h-5 inline-block mr-1.5 text-amber-500\" /> Yeni Özel Kampanya Ekle</>}",
    "{user ? '⚙️ Kullanıcıyı Düzenle' : '➕ Yeni Kullanıcı Ekle'}": "{user ? <><ThemeIcon icon=\"settings\" fallbackEmoji=\"⚙️\" className=\"w-5 h-5 inline-block mr-1.5 text-amber-500\" /> Kullanıcıyı Düzenle</> : <><ThemeIcon icon=\"plus\" fallbackEmoji=\"➕\" className=\"w-5 h-5 inline-block mr-1.5 text-amber-500\" /> Yeni Kullanıcı Ekle</>}",

    # Form card headers in CreateReservationPageComponent
    '<span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider">🏰 1. Salon & Kapasite Seçimi:</span>': '<span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider"><ThemeIcon icon="venue" fallbackEmoji="🏰" className="w-4 h-4 inline-block mr-1 shrink-0" /> 1. Salon & Kapasite Seçimi:</span>',
    '<span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider">⏰ 2. Etkinlik Tarihi & Hızlı Seans Seçimi:</span>': '<span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider"><ThemeIcon icon="clock" fallbackEmoji="⏰" className="w-4 h-4 inline-block mr-1 shrink-0" /> 2. Etkinlik Tarihi & Hızlı Seans Seçimi:</span>',
    '<span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider">🎁 3. Ek Hizmetler & Dahili Paket Seçimi:</span>': '<span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider"><ThemeIcon icon="gift" fallbackEmoji="🎁" className="w-4 h-4 inline-block mr-1 shrink-0" /> 3. Ek Hizmetler & Dahili Paket Seçimi:</span>',
    '<span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider">🏷️ 4. Özel Kampanya & İndirim Kodu:</span>': '<span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider"><ThemeIcon icon="campaign" fallbackEmoji="🏷️" className="w-4 h-4 inline-block mr-1 shrink-0" /> 4. Özel Kampanya & İndirim Kodu:</span>',
    '<span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider">👤 5. Müşteri İletişim, Adres & Fatura Bilgileri:</span>': '<span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider"><ThemeIcon icon="user" fallbackEmoji="👤" className="w-4 h-4 inline-block mr-1 shrink-0" /> 5. Müşteri İletişim, Adres & Fatura Bilgileri:</span>',
    '<span className="text-amber-900 dark:text-amber-300 font-bold block text-[11px] uppercase tracking-wider">💰 6. Finans, Kapora, Ödeme Statüsü & Fatura Kesildi Bilgisi:</span>': '<span className="text-amber-900 dark:text-amber-300 font-bold block text-[11px] uppercase tracking-wider"><ThemeIcon icon="money" fallbackEmoji="💰" className="w-4 h-4 inline-block mr-1 shrink-0" /> 6. Finans, Kapora, Ödeme Statüsü & Fatura Kesildi Bilgisi:</span>',
    '<span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider">📜 7. Düğün & Etkinlik Akış Planlaması:</span>': '<span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider"><ThemeIcon icon="document" fallbackEmoji="📜" className="w-4 h-4 inline-block mr-1 shrink-0" /> 7. Düğün & Etkinlik Akış Planlaması:</span>',
    '<span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider">📝 8. Operasyonel Ek Notlar & Özel İstekler:</span>': '<span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider"><ThemeIcon icon="notes" fallbackEmoji="📝" className="w-4 h-4 inline-block mr-1 shrink-0" /> 8. Operasyonel Ek Notlar & Özel İstekler:</span>',

    # Section Headers & Modal Headers
    '<h4 className="font-bold text-amber-700 dark:text-gold-400">📋 Etkinlik Akış Planlaması': '<h4 className="font-bold text-amber-700 dark:text-gold-400"><ThemeIcon icon="document" fallbackEmoji="📋" className="w-4 h-4 inline-block mr-1 shrink-0" /> Etkinlik Akış Planlaması',
    '<h4 className="font-bold text-xs text-amber-700 dark:text-gold-400">💳 Ödeme ve Kapora Güncelleme</h4>': '<h4 className="font-bold text-xs text-amber-700 dark:text-gold-400"><ThemeIcon icon="card" fallbackEmoji="💳" className="w-4 h-4 inline-block mr-1 shrink-0" /> Ödeme ve Kapora Güncelleme</h4>',
    '<div className="font-bold text-amber-700 dark:text-gold-400">🔑 Üyelik ve Giriş Bilgileriniz:</div>': '<div className="font-bold text-amber-700 dark:text-gold-400"><ThemeIcon icon="key" fallbackEmoji="🔑" className="w-4 h-4 inline-block mr-1 shrink-0" /> Üyelik ve Giriş Bilgileriniz:</div>',
    '<div className="font-bold text-amber-700 dark:text-gold-400">📋 Rezervasyon Fatura ve Ödeme Özeti': '<div className="font-bold text-amber-700 dark:text-gold-400"><ThemeIcon icon="document" fallbackEmoji="📋" className="w-4 h-4 inline-block mr-1 shrink-0" /> Rezervasyon Fatura ve Ödeme Özeti',
    '🏛️ Salon Doluluk & Seans Çakışma Analizi': '<ThemeIcon icon="venue" fallbackEmoji="🏛️" className="w-4 h-4 inline-block mr-1 shrink-0" /> Salon Doluluk & Seans Çakışma Analizi',
    '<span>🔍 Detaylı Filtreleme & Arama Kriterleri</span>': '<span><ThemeIcon icon="search" fallbackEmoji="🔍" className="w-4 h-4 inline-block mr-1 shrink-0" /> Detaylı Filtreleme & Arama Kriterleri</span>',
    '🛡️ Rol Tabanlı Sayfa İzin Matrisi (RBAC Matrix)': '<ThemeIcon icon="shield" fallbackEmoji="🛡️" className="w-5 h-5 inline-block mr-2 shrink-0" /> Rol Tabanlı Sayfa İzin Matrisi (RBAC Matrix)',
    '<span>🚨 Özel Hata & Yönlendirme Sayfaları Canlı Simülasyon Paneli</span>': '<span><ThemeIcon icon="alert" fallbackEmoji="🚨" className="w-5 h-5 inline-block mr-2 text-red-500 shrink-0" /> Özel Hata & Yönlendirme Sayfaları Canlı Simülasyon Paneli</span>',

    # Buttons
    '<button onClick={onAddClick} className="gold-button font-bold px-4 py-2.5 rounded-xl text-xs shadow">➕ Yeni Düğün Salonu Ekle</button>': '<button onClick={onAddClick} className="gold-button font-bold px-4 py-2.5 rounded-xl text-xs shadow flex items-center space-x-1.5"><ThemeIcon icon="plus" fallbackEmoji="➕" className="w-3.5 h-3.5 shrink-0" /><span>Yeni Düğün Salonu Ekle</span></button>',
    '➕ Akış Adımı Ekle': '<ThemeIcon icon="plus" fallbackEmoji="➕" className="w-3.5 h-3.5 inline-block mr-1 shrink-0" /> Akış Adımı Ekle',
    '➕ Bu Tarihe Yeni Rezervasyon Ekle': '<ThemeIcon icon="plus" fallbackEmoji="➕" className="w-3.5 h-3.5 inline-block mr-1 shrink-0" /> Bu Tarihe Yeni Rezervasyon Ekle',
    '<span>➕ Yeni Kullanıcı Rolü Tanımla</span>': '<span><ThemeIcon icon="plus" fallbackEmoji="➕" className="w-4 h-4 inline-block mr-1 shrink-0" /> Yeni Kullanıcı Rolü Tanımla</span>',
    '🗑️ Önbelleği Temizle & Sıfırla': '<ThemeIcon icon="delete" fallbackEmoji="🗑️" className="w-4 h-4 inline-block mr-1 shrink-0" /> Önbelleği Temizle & Sıfırla',
    '<span>💾 Değişiklikleri Kaydet & Tüm Sistemde Uygula ✓</span>': '<span><ThemeIcon icon="document" fallbackEmoji="💾" className="w-4 h-4 inline-block mr-1 shrink-0" /> Değişiklikleri Kaydet & Tüm Sistemde Uygula <ThemeIcon icon="check" fallbackEmoji="✓" className="w-4 h-4 inline-block ml-1 shrink-0" /></span>',
    '<span>⚡ Önbellekleme (Caching Engine) Yönetimi</span>': '<span><ThemeIcon icon="zap" fallbackEmoji="⚡" className="w-4 h-4 inline-block mr-1 shrink-0" /> Önbellekleme (Caching Engine) Yönetimi</span>',

    # Placeholders
    'placeholder="🔍 Ad, Soyad, Telefon veya E-posta ile Hızlı Ara..."': 'placeholder="Ad, Soyad, Telefon veya E-posta ile Hızlı Ara..."',
    'placeholder="🔍 Müşteri Adı, Tel veya Sözleşme Kodu..."': 'placeholder="Müşteri Adı, Tel veya Sözleşme Kodu..."',
    'placeholder="Örn: Muhasebe Sorumlusu 📊"': 'placeholder="Örn: Muhasebe Sorumlusu"',

    # Badges / Small elements
    "badge: '✨ AI Üretimi'": "badge: 'AI Üretimi'",
    "✨ AI Üretimi": "<ThemeIcon icon=\"sparkles\" fallbackEmoji=\"✨\" className=\"w-3.5 h-3.5 inline-block mr-1 shrink-0\" /> AI Üretimi",
    "<span>👤 Profil & Güvenlik Ayarlarını Düzenle</span>": "<span><ThemeIcon icon=\"user\" fallbackEmoji=\"👤\" className=\"w-4 h-4 inline-block mr-1.5 shrink-0\" /> Profil & Güvenlik Ayarlarını Düzenle</span>"
}

for k, v in replacements.items():
    if k in content:
        content = content.replace(k, v)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Replaced exact raw emoji occurrences in index.html successfully.')
