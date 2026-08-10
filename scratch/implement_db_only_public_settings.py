import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = "      const [publicTheme, setPublicTheme] = useState("
end_marker = "      return (\n        <div className=\"w-full space-y-6 animate-fade-in pb-16\">"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_code = """      const [publicTheme, setPublicTheme] = useState('dark-gold');
      const [publicBadge, setPublicBadge] = useState('✨ Sapanca Göl Kenarı Lüks Düğün Tesisleri');
      const [publicTitle, setPublicTitle] = useState('Hayalinizdeki Düğün İrem Düğün Sarayı\'nda Unutulmaz Oluyor');
      const [publicSubtitle, setPublicSubtitle] = useState('4 farklı balo salonu, açık hava kır bahçesi, kristal avizeler ve VIP ikram menüleriyle hayatınızın en özel gününe ev sahipliği yapıyoruz.');

      // PURE DATABASE FETCH (NO COOKIE / NO CACHE)
      useEffect(() => {
        const fetchPublicSettingsFromDB = async () => {
          try {
            const fetchFn = window.fetchWithRetry || fetch;
            const res = await fetchFn('/api/public-settings');
            if (res.ok) {
              const data = await res.json();
              if (data.publicTheme) setPublicTheme(data.publicTheme);
              if (data.heroBadgeText) setPublicBadge(data.heroBadgeText);
              if (data.heroTitle) setPublicTitle(data.heroTitle);
              if (data.heroSubtitle) setPublicSubtitle(data.heroSubtitle);
            }
          } catch(e) {}
        };
        fetchPublicSettingsFromDB();
      }, []);

      const handleSavePublicSettings = async () => {
        const payload = {
          publicTheme: 'dark-gold',
          heroBadgeText: publicBadge,
          heroTitle: publicTitle,
          heroSubtitle: publicSubtitle,
          updatedAt: new Date().toISOString()
        };
        try {
          const fetchFn = window.fetchWithRetry || fetch;
          const res = await fetchFn('/api/public-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
          if (res.ok) {
            if (showToast) showToast('Ön Yüz Ayarları Veritabanına Başarıyla Kaydedildi & Yayınlandı! ✓');
          } else {
            if (showToast) showToast('Veritabanına kaydedilirken bir yanıt uyarısı oluştu.');
          }
        } catch (e) {
          if (showToast) showToast('Veritabanı bağlantı hatası oluştu!');
        }
      };

"""
    content = content[:start_idx] + new_code + content[end_idx:]
    print("Replaced SettingsComponent state logic successfully!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
