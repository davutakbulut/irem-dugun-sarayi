import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

v150_entry = """const releases = [
        {
          version: 'v1.5.0 (Yol Haritası)',
          tag: 'YAKINDA GELECEK',
          date: 'Ağustos 2026 (Planlanan)',
          title: '🚀 Excel/PDF Dışa Aktarma, Otomatik Mesajlaşma & Çoklu Dil Mimarisi',
          color: 'bg-indigo-500',
          changes: [
            '📊 Excel & PDF Rapor İndirme: Finansal raporlar ve rezervasyon listelerini tek tıkla Excel (.xlsx) ve PDF formatında indirme.',
            '💬 Otomatik SMS & WhatsApp Entegrasyonu: Rezervasyon onaylandığında müşteriye otomatik bildirim mesajı iletimi.',
            '🌐 Çoklu Dil Desteği (TR / EN): Uluslararası organizasyonlar için Türkçe ve İngilizce arayüz dil seçeneği.'
          ]
        },
        {
          version: 'v1.4.0',"""

html = html.replace("const releases = [\n        {\n          version: 'v1.4.0',", v150_entry)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Added v1.5.0 Roadmap release entry to index.html successfully!")
