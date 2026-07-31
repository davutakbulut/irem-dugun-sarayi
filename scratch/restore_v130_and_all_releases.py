import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the releases array in VersionHistoryModalComponent with the full list including both v1.4.0 and v1.3.0
old_releases_pattern = r'const releases = \[[\s\S]*?\];'

new_releases_code = """const releases = [
        {
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
          tag: 'ÖNCEKİ SÜRÜM',
          date: '30 Temmuz 2026',
          title: 'Dinamik Sürüm Yönetimi & Sub-Header Mimarisi',
          color: 'bg-teal-500',
          changes: [
            'Ana header ile menü arasında bağımsız Rol & Canlı Sistem Sub-Header barı kuruldu.',
            'Git commit analizine dayalı Semantik Sürümleme (Semantic Versioning) motoru entegre edildi.',
            'Düğün.com stili Mega Menü çekmecesi (full-width hover drawer) tamamlandı.'
          ]
        },
        {
          version: 'v1.2.0',
          date: '30 Temmuz 2026',
          title: 'Çift Navigasyon Mimarisi & Düzen Değiştirici',
          color: 'bg-amber-500',
          changes: [
            'Ayarlar > Görünüm sekmesine Dikey Sol Menü / Yatay Üst Menü kartları eklendi.',
            'Seçilen menü yerleşiminin LocalStorage önbelleği ile kalıcılığı sağlandı.'
          ]
        },
        {
          version: 'v1.1.0',
          date: '29 Temmuz 2026',
          title: 'RBAC Rol Bazlı Sayfa & İstatistik Kısıtlamaları',
          color: 'bg-blue-500',
          changes: [
            'Ciro ve finansal grafikler strictly Admin rolüne kısıtlandı.',
            'Satışçı, Sosyal Medyacı ve Müşteri için özelleştirilmiş özel ana sayfa panoları geliştirildi.'
          ]
        },
        {
          version: 'v1.0.0',
          date: '29 Temmuz 2026',
          title: 'Modüler Sayfa Mimarisi & 5 Kurumsal Tema',
          color: 'bg-purple-500',
          changes: [
            '11 ana sayfa bileşeni ES modülleri halinde src/pages/ dizinine ayrıştırıldı.',
            'Nordic Light Zero Emoji direktifi ve SVG ThemeIcon mimarisi devreye alındı.',
            '5 kurumsal tema (Classic Gold, Elite Luxury, Sapphire, Emerald, Nordic) yayına alındı.'
          ]
        },
        {
          version: 'v0.1.0',
          date: '28 Temmuz 2026',
          title: 'Dinamik Düğün Takvimi & Hatasız Modallar',
          color: 'bg-slate-500',
          changes: [
            'Düğün takvimine Ay/Yıl navigasyon araçları ve dinamik gün matrisi yerleştirildi.',
            'Gelişmiş Fatura dökümü ve WhatsApp rezervasyon bildirimleri entegre edildi.'
          ]
        },
        {
          version: 'v0.0.1',
          date: '27 Temmuz 2026',
          title: 'İrem Düğün Sarayı İlk Sürüm Yayını',
          color: 'bg-slate-400',
          changes: [
            'Temel rezervasyon oluşturma formu, müşteri CRM kayıtları ve salon kapasite tanımları kuruldu.'
          ]
        }
      ];"""

if re.search(old_releases_pattern, html):
    html = re.sub(old_releases_pattern, new_releases_code, html)
    print("Restored v1.3.0 and complete version history log successfully!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html successfully!")
