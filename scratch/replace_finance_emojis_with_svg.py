import os, re

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace Star emoji in KPI card
    content = content.replace(
        '<span className="text-amber-500 text-lg font-bold">★</span>',
        '<ThemeIcon icon="star" className="w-5 h-5 text-amber-500 shrink-0" />'
    )

    # 2. Replace Inflow/Outflow arrow emojis
    content = content.replace(
        '<span className="text-emerald-500 text-lg font-bold">↗</span>',
        '<svg className="w-5 h-5 text-emerald-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M7 17L17 7M17 7H7M17 7V17" /></svg>'
    )
    content = content.replace(
        '<span className="text-red-500 text-lg font-bold">↘</span>',
        '<svg className="w-5 h-5 text-red-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M7 7l10 10M17 17H7M17 17V7" /></svg>'
    )

    content = content.replace(
        '<span className="text-red-500">↘</span>',
        '<svg className="w-4 h-4 text-red-500 shrink-0 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M7 7l10 10M17 17H7M17 17V7" /></svg>'
    )
    content = content.replace(
        '<span className="text-emerald-500">↗</span>',
        '<svg className="w-4 h-4 text-emerald-500 shrink-0 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M7 17L17 7M17 7H7M17 7V17" /></svg>'
    )

    # 3. Replace Accordion breakdown item icons
    content = content.replace(
        '<span>🏰</span><span>Mekan & Salon Maliyeti</span>',
        '<ThemeIcon icon="venue" className="w-4 h-4 text-amber-500 shrink-0 inline-block mr-1.5" /><span>Mekan & Salon Maliyeti</span>'
    )
    content = content.replace(
        '<span>🍽️</span><span>Seçili Ek Hizmetler',
        '<ThemeIcon icon="gift" className="w-4 h-4 text-amber-500 shrink-0 inline-block mr-1.5" /><span>Seçili Ek Hizmetler'
    )
    content = content.replace(
        '<span>📑</span><span>Düğüne Özel Giderler',
        '<ThemeIcon icon="notes" className="w-4 h-4 text-amber-500 shrink-0 inline-block mr-1.5" /><span>Düğüne Özel Giderler'
    )

    # 4. Replace 🗑️ Sil button in Kasa Table
    content = content.replace(
        '🗑️ Sil',
        'Sil'
    )

    # 5. Clean Select Options for Categories in the Modal
    content = content.replace('📷 Dış Çekim & Plato Kiralama Geliri', 'Dış Çekim & Plato Kiralama Geliri')
    content = content.replace('☕ Kafeterya & Mutfak Günlük Satış', 'Kafeterya & Mutfak Günlük Satış Geliri')
    content = content.replace('🔊 Ses & Işık Ekipman Dış Kiralama', 'Ses & Işık Ekipman Dış Kiralama')
    content = content.replace('🏷️ Sponsorluk & Reklam Geliri', 'Sponsorluk & Reklam Geliri')
    content = content.replace('📦 Eski Ekipman / Hurda Satış Geliri', 'Eski Ekipman / Hurda Satış Geliri')
    content = content.replace('💵 Diğer Muhtelif Kasa Geliri', 'Diğer Muhtelif Kasa Geliri')

    content = content.replace('💡 Faturalar & Enerji (Elektrik, Su, Doğalgaz, Fiber İnternet)', 'Faturalar & Enerji (Elektrik, Su, Doğalgaz, İnternet)')
    content = content.replace('🍽️ Yemek & Mutfak & İkram Alımları', 'Yemek & Mutfak & İkram Alımları')
    content = content.replace('☕ Keyfi & Temsil Ağırlama (Kahve, Yemek vb.)', 'Keyfi & Temsil Ağırlama (Kahve, Yemek vb.)')
    content = content.replace('👥 Personel Maaş, Yevmiye & SGK', 'Personel Maaş, Yevmiye & SGK')
    content = content.replace('🌸 Dekorasyon, Çiçek & Sahne Süsleme', 'Dekorasyon, Çiçek & Sahne Süsleme')
    content = content.replace('🔊 Ekipman, Ses, Işık & Bakım Onarım', 'Ekipman, Ses, Işık & Bakım Onarım')
    content = content.replace('📑 Ofis, Kırtasiye & Sarf Malzeme', 'Ofis, Kırtasiye & Sarf Malzeme')
    content = content.replace('⚖️ Vergi, Harç & Muhasebe Ödemeleri', 'Vergi, Harç & Muhasebe Ödemeleri')
    content = content.replace('📦 Diğer Genel İşletme Giderleri', 'Diğer Genel İşletme Giderleri')

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Replaced emojis with SVG icons in {h_file}")

print("All finance page emojis converted to crisp SVG icons!")
