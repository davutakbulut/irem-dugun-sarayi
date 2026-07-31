import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace version text strings across index.html
html = html.replace('v1.3.0', 'v1.4.0')
html = html.replace('Canlı Sistem v1.3.0', 'Canlı Sistem v1.4.0')
html = html.replace('v1.3.0 (Canlı)', 'v1.4.0 (Kararlı Canlı Sürüm)')

# Insert v1.4.0 entry into releases array in VersionHistoryModalComponent
v140_entry = """        {
          version: 'v1.4.0',
          tag: 'KARARLI CANLI SÜRÜM',
          date: '31 Temmuz 2026',
          title: '🛡️ Müstakil Rol Yönetimi, 3G Hız Performansı & Nordic Taç Logosu',
          color: 'bg-emerald-500',
          changes: [
            'Rol Yönetimi Sistem Ayarlarından ayrılıp bağımsız #/roller sayfasına dönüştürüldü.',
            'Zihin Haritası ve Rol Yönetimi bağlantıları YÖNETİM & AYARLAR menü grubu altına alındı.',
            '5 Kritik Form Doğrulama Kuralı (Negatif kişi/fiyat engeli, mükerrer kupon engeli, geçmiş tarihli rezervasyon engeli) tamamlandı.',
            'Babel ön derlemesi ve Gzip sıkıştırma ile 3G LCP yükleme süresi <2.5s seviyesine indirildi.',
            'Header logosuna Sarı Taç Logo rozeti uygulandı ve ham emojiler temaya özel SVG ikonlarla değiştirildi.'
          ]
        },
        {
          version: 'v1.3.0',
          tag: 'ÖNCEKİ SÜRÜM',"""

html = html.replace("""        {
          version: 'v1.3.0',
          tag: 'GÜNCEL SÜRÜM',""", v140_entry)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Bumped system version to v1.4.0 in index.html successfully!")
