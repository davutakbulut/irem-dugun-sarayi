import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add const releases = [...dynamicReleases, ...staticReleases]; right after staticReleases array
old_static_end = """        {
          version: 'v0.0.1',
          date: '27 Temmuz 2026',
          title: 'İrem Düğün Sarayı İlk Sürüm Yayını',
          color: 'bg-slate-400',
          changes: [
            'Temel rezervasyon oluşturma formu, müşteri CRM kayıtları ve salon kapasite tanımları kuruldu.'
          ]
        }
      ];"""

new_static_end = """        {
          version: 'v0.0.1',
          date: '27 Temmuz 2026',
          title: 'İrem Düğün Sarayı İlk Sürüm Yayını',
          color: 'bg-slate-400',
          changes: [
            'Temel rezervasyon oluşturma formu, müşteri CRM kayıtları ve salon kapasite tanımları kuruldu.'
          ]
        }
      ];

      const releases = [...dynamicReleases, ...staticReleases];"""

if old_static_end in html and "const releases = [...dynamicReleases, ...staticReleases];" not in html:
    html = html.replace(old_static_end, new_static_end)
    print("Added const releases = [...dynamicReleases, ...staticReleases]; to VersionHistoryModalComponent!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html releases array fix successfully!")
