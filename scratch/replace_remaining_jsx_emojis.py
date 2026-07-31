import re

file_path = '/Users/davutakbulut/.gemini/antigravity/scratch/irem_dugun_sarayi/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    # Buttons & Inputs
    'Salonu Kaydet ✓': 'Salonu Kaydet <ThemeIcon icon="check" fallbackEmoji="✓" className="w-3.5 h-3.5 inline-block ml-1" />',
    'Hizmeti Kaydet ✓': 'Hizmeti Kaydet <ThemeIcon icon="check" fallbackEmoji="✓" className="w-3.5 h-3.5 inline-block ml-1" />',
    'Kampanyayı Kaydet ✓': 'Kampanyayı Kaydet <ThemeIcon icon="check" fallbackEmoji="✓" className="w-3.5 h-3.5 inline-block ml-1" />',
    'Kullanıcıyı Kaydet ✓': 'Kullanıcıyı Kaydet <ThemeIcon icon="check" fallbackEmoji="✓" className="w-3.5 h-3.5 inline-block ml-1" />',
    'Değişiklikleri Kaydet ✓': 'Değişiklikleri Kaydet <ThemeIcon icon="check" fallbackEmoji="✓" className="w-3.5 h-3.5 inline-block ml-1" />',
    'Filtreleri Temizle ↺': 'Filtreleri Temizle <ThemeIcon icon="refresh" fallbackEmoji="↺" className="w-3.5 h-3.5 inline-block ml-1" />',
    'Seç & Doldur ✓': 'Seç & Doldur <ThemeIcon icon="check" fallbackEmoji="✓" className="w-3.5 h-3.5 inline-block ml-1" />',

    # Notifications & Modals
    '<span className="text-xl">✉️</span>': '<ThemeIcon icon="email" fallbackEmoji="✉️" className="w-5 h-5 shrink-0 text-amber-500" />',
    '<p className="text-[10px] text-emerald-600 dark:text-emerald-400 font-bold">✓ Müşteri E-Posta Adresine Başarıyla İletildi</p>': '<p className="text-[10px] text-emerald-600 dark:text-emerald-400 font-bold"><ThemeIcon icon="check" fallbackEmoji="✓" className="w-3 h-3 inline-block mr-1" /> Müşteri E-Posta Adresine Başarıyla İletildi</p>',
    '<span className="bg-white/90 dark:bg-slate-900/90 text-slate-800 dark:text-white text-xs font-bold px-3 py-1.5 rounded-xl shadow-lg border border-amber-500/30">🔍 Detay İncele</span>': '<span className="bg-white/90 dark:bg-slate-900/90 text-slate-800 dark:text-white text-xs font-bold px-3 py-1.5 rounded-xl shadow-lg border border-amber-500/30 flex items-center space-x-1"><ThemeIcon icon="search" fallbackEmoji="🔍" className="w-3.5 h-3.5 shrink-0" /><span>Detay İncele</span></span>',

    # Inspector & Day details
    '🕒 {formatDate(selectedDayInspector.dateStr)}': '<ThemeIcon icon="clock" fallbackEmoji="🕒" className="w-4 h-4 inline-block mr-1" /> {formatDate(selectedDayInspector.dateStr)}',
    '💡 <strong>Saat Akış Çizelgesi:</strong>': '<ThemeIcon icon="idea" fallbackEmoji="💡" className="w-4 h-4 inline-block mr-1 text-amber-500" /> <strong>Saat Akış Çizelgesi:</strong>',
    '<span className="font-bold block text-slate-700 dark:text-gray-200">⏱️ Günlük Zaman Çizelgesi': '<span className="font-bold block text-slate-700 dark:text-gray-200"><ThemeIcon icon="clock" fallbackEmoji="⏱️" className="w-4 h-4 inline-block mr-1" /> Günlük Zaman Çizelgesi',
    '<span className="font-bold block text-slate-700 dark:text-gray-200">📋 Günlük Etkinlik Kartları': '<span className="font-bold block text-slate-700 dark:text-gray-200"><ThemeIcon icon="document" fallbackEmoji="📋" className="w-4 h-4 inline-block mr-1" /> Günlük Etkinlik Kartları',
    '👁️ Detay Önizle': '<ThemeIcon icon="preview" fallbackEmoji="👁️" className="w-3.5 h-3.5 inline-block mr-1" /> Detay Önizle',
    '✏️ Rezervasyonu Düzenle': '<ThemeIcon icon="edit" fallbackEmoji="✏️" className="w-3.5 h-3.5 inline-block mr-1" /> Rezervasyonu Düzenle',
    '✏️ Rezervasyon Tüm Bilgilerini Düzenle': '<ThemeIcon icon="edit" fallbackEmoji="✏️" className="w-3.5 h-3.5 inline-block mr-1" /> Rezervasyon Tüm Bilgilerini Düzenle',

    # Reservation Preview labels
    '<span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider">👤 Müşteri İletişim Bilgileri:</span>': '<span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider"><ThemeIcon icon="user" fallbackEmoji="👤" className="w-4 h-4 inline-block mr-1 shrink-0" /> Müşteri İletişim Bilgileri:</span>',
    '<div>📞 Birincil Tel:': '<div><ThemeIcon icon="phone" fallbackEmoji="📞" className="w-4 h-4 inline-block mr-1 shrink-0" /> Birincil Tel:',
    '<div>📱 İkinci Tel:': '<div><ThemeIcon icon="phone" fallbackEmoji="📱" className="w-4 h-4 inline-block mr-1 shrink-0" /> İkinci Tel:',
    '<div>✉️ E-Posta:': '<div><ThemeIcon icon="email" fallbackEmoji="✉️" className="w-4 h-4 inline-block mr-1 shrink-0" /> E-Posta:',
    '<span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider">🏰 Etkinlik & Salon Detayı:</span>': '<span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider"><ThemeIcon icon="venue" fallbackEmoji="🏰" className="w-4 h-4 inline-block mr-1 shrink-0" /> Etkinlik & Salon Detayı:</span>',
    '<div>📅 Tarih:': '<div><ThemeIcon icon="calendar" fallbackEmoji="📅" className="w-4 h-4 inline-block mr-1 shrink-0" /> Tarih:',
    '<div>⏰ Saat Aralığı:': '<div><ThemeIcon icon="clock" fallbackEmoji="⏰" className="w-4 h-4 inline-block mr-1 shrink-0" /> Saat Aralığı:',
    '<div>👥 Davetli Sayısı:': '<div><ThemeIcon icon="user" fallbackEmoji="👥" className="w-4 h-4 inline-block mr-1 shrink-0" /> Davetli Sayısı:',
    '<span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider">📜 Organizasyon & Zaman Akış Programı:</span>': '<span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider"><ThemeIcon icon="document" fallbackEmoji="📜" className="w-4 h-4 inline-block mr-1 shrink-0" /> Organizasyon & Zaman Akış Programı:</span>',
    '<span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider">🎁 Verilen Hizmetler & Dahili Paketler:</span>': '<span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider"><ThemeIcon icon="gift" fallbackEmoji="🎁" className="w-4 h-4 inline-block mr-1 shrink-0" /> Verilen Hizmetler & Dahili Paketler:</span>',
    '<span className="text-amber-900 dark:text-amber-300 font-bold block text-[11px] uppercase tracking-wider">💰 Detaylı Ödeme Durumları & Finansal Döküm:</span>': '<span className="text-amber-900 dark:text-amber-300 font-bold block text-[11px] uppercase tracking-wider"><ThemeIcon icon="money" fallbackEmoji="💰" className="w-4 h-4 inline-block mr-1 shrink-0" /> Detaylı Ödeme Durumları & Finansal Döküm:</span>',
    '<span className="font-bold block text-slate-800 dark:text-gray-200">💳 Gerçekleşen Ödemeler Geçmişi:</span>': '<span className="font-bold block text-slate-800 dark:text-gray-200"><ThemeIcon icon="card" fallbackEmoji="💳" className="w-4 h-4 inline-block mr-1 shrink-0" /> Gerçekleşen Ödemeler Geçmişi:</span>',
    '<span>✓ 1. Ödeme (Kapora Tahsilatı):</span>': '<span><ThemeIcon icon="check" fallbackEmoji="✓" className="w-3.5 h-3.5 inline-block mr-1 shrink-0" /> 1. Ödeme (Kapora Tahsilatı):</span>',
    '<span>✓ 2. Ödeme (Kalan Bakiye Tahsilatı):</span>': '<span><ThemeIcon icon="check" fallbackEmoji="✓" className="w-3.5 h-3.5 inline-block mr-1 shrink-0" /> 2. Ödeme (Kalan Bakiye Tahsilatı):</span>',
    '<span>⏳ 2. Ödeme (Kalan Bakiye Tahsilatı):</span>': '<span><ThemeIcon icon="clock" fallbackEmoji="⏳" className="w-3.5 h-3.5 inline-block mr-1 shrink-0" /> 2. Ödeme (Kalan Bakiye Tahsilatı):</span>',
    '<span className="text-slate-400 font-bold block">📝 Operasyonel Notlar & Özel İstekler:</span>': '<span className="text-slate-400 font-bold block"><ThemeIcon icon="notes" fallbackEmoji="📝" className="w-4 h-4 inline-block mr-1 shrink-0" /> Operasyonel Notlar & Özel İstekler:</span>',

    # Form Selections
    '☀️ Gündüz (12-17)': '<ThemeIcon icon="sun" fallbackEmoji="☀️" className="w-4 h-4 inline-block mr-1" /> Gündüz (12-17)',
    '🌙 Gece (18-23)': '<ThemeIcon icon="moon" fallbackEmoji="🌙" className="w-4 h-4 inline-block mr-1" /> Gece (18-23)',
    '<span className="text-slate-800 dark:text-gray-200">📄 Faturası Kesildi mi?</span>': '<span className="text-slate-800 dark:text-gray-200"><ThemeIcon icon="print" fallbackEmoji="📄" className="w-4 h-4 inline-block mr-1" /> Faturası Kesildi mi?</span>',
    '⚠️ Müşteri adı ve telefonu zorunludur!': '<ThemeIcon icon="alert" fallbackEmoji="⚠️" className="w-4 h-4 inline-block mr-1 text-red-500" /> Müşteri adı ve telefonu zorunludur!',
    '💾 Değişiklikleri Kaydet': '<ThemeIcon icon="document" fallbackEmoji="💾" className="w-4 h-4 inline-block mr-1" /> Değişiklikleri Kaydet',

    # DayDetailModal
    ": '✅ TAMAMEN MÜSAİT'}": ": <><ThemeIcon icon=\"check\" fallbackEmoji=\"✅\" className=\"w-4 h-4 inline-block mr-1 text-emerald-500\" /> TAMAMEN MÜSAİT</>}",
    '<span>⏰ Seans:': '<span><ThemeIcon icon="clock" fallbackEmoji="⏰" className="w-3.5 h-3.5 inline-block mr-1" /> Seans:',
    '<span>• 👥 {r.guestCount} Davetli</span>': '<span>• <ThemeIcon icon="user" fallbackEmoji="👥" className="w-3.5 h-3.5 inline-block mx-1" /> {r.guestCount} Davetli</span>',
    '<span className="text-xs text-amber-700 dark:text-gold-400">Detay 🔍</span>': '<span className="text-xs text-amber-700 dark:text-gold-400 flex items-center space-x-1"><span>Detay</span> <ThemeIcon icon="search" fallbackEmoji="🔍" className="w-3.5 h-3.5 inline-block" /></span>',
    '💡 Bu salon için {formattedDate} tarihinde henüz hiç rezervasyon yapılmamıştır. Gündüz veya Gece seansı hemen rezerve edilebilir!': '<><ThemeIcon icon="idea" fallbackEmoji="💡" className="w-4 h-4 inline-block mr-1 text-amber-500" /> Bu salon için {formattedDate} tarihinde henüz hiç rezervasyon yapılmamıştır. Gündüz veya Gece seansı hemen rezerve edilebilir!</>',
    '💡 Günün üzerine tıklayarak tüm salon doluluklarını inceleyebilir veya kartı sürükleyerek başka güne taşıyabilirsiniz.': '<><ThemeIcon icon="idea" fallbackEmoji="💡" className="w-4 h-4 inline-block mr-1 text-amber-500" /> Günün üzerine tıklayarak tüm salon doluluklarını inceleyebilir veya kartı sürükleyerek başka güne taşıyabilirsiniz.</>',

    # Settings
    '<label className="font-bold text-slate-800 dark:text-gray-200 block mb-1">🔔 Otomatik Bildirim Tercihleri:</label>': '<label className="font-bold text-slate-800 dark:text-gray-200 block mb-1"><ThemeIcon icon="bell" fallbackEmoji="🔔" className="w-4 h-4 inline-block mr-1 text-amber-500" /> Otomatik Bildirim Tercihleri:</label>',
    "{isCacheEnabled ? 'AÇIK ✓' : 'KAPALI ✕'}": "{isCacheEnabled ? <><ThemeIcon icon=\"check\" fallbackEmoji=\"✓\" className=\"w-3.5 h-3.5 inline-block ml-1 text-emerald-500\" /> AÇIK</> : <><ThemeIcon icon=\"close\" fallbackEmoji=\"✕\" className=\"w-3.5 h-3.5 inline-block ml-1 text-red-500\" /> KAPALI</>}",
    "{netProfit >= 0 ? '✓ Pozitif Bakiye' : '⚠ Negatif Bakiye'}": "{netProfit >= 0 ? <><ThemeIcon icon=\"check\" fallbackEmoji=\"✓\" className=\"w-4 h-4 inline-block mr-1 text-emerald-500\" /> Pozitif Bakiye</> : <><ThemeIcon icon=\"warning\" fallbackEmoji=\"⚠\" className=\"w-4 h-4 inline-block mr-1 text-red-500\" /> Negatif Bakiye</>}"
}

for k, v in replacements.items():
    if k in content:
        content = content.replace(k, v)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Replaced remaining JSX emojis successfully.')
