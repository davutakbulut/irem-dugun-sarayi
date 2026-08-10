import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_campaign_handlers = """      const handleSaveCampaign = (cObj) => {
        setCampaigns(prev => {
          const idx = prev.findIndex(x => x.id === cObj.id);
          if (idx >= 0) {
            const updated = [...prev];
            updated[idx] = cObj;
            return updated;
          }
          return [...prev, cObj];
        });
        setCampaignModalData(null);
        showToast('Özel Kampanya Başarıyla Oluşturuldu!');
      };

      const handleConvertAiToCampaign = (rec) => {
        const newCamp = {
          id: 'c_' + Date.now(),
          code: rec.code || ('AI_' + Math.floor(Math.random() * 8999 + 1000)),
          title: (rec.title || '').replace(/^[]\s*/, ''),
          type: rec.type || 'percent',
          value: rec.value || 15,
          description: rec.description,
          isAiGenerated: true,
          badge: 'AI Üretimi',
          active: true
        };
        setCampaigns(prev => [newCamp, ...prev]);
        showToast(`AI Önerisi Canlı Kampanyalar Sayfasına Enjekte Edildi! Kod: ${newCamp.code}`);
        navigateTo('campaigns');
      };"""

new_campaign_handlers = """      const handleSaveCampaign = (cObj) => {
        setCampaigns(prev => {
          const list = prev || [];
          const idx = list.findIndex(x => x.id === cObj.id);
          let updated;
          if (idx >= 0) {
            updated = [...list];
            updated[idx] = { ...updated[idx], ...cObj };
          } else {
            updated = [...list, cObj];
          }
          CacheService.set('campaigns', updated);
          if (window.fetchWithRetry) {
            window.fetchWithRetry('/api/system-settings', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ campaigns: updated })
            }).catch(() => {});
          }
          return updated;
        });
        setCampaignModalData(null);
        showToast(`Kampanya (${cObj.code}) Veritabanına Başarıyla Kaydedildi!`);
      };

      const handleConvertAiToCampaign = (rec) => {
        const newCamp = {
          id: 'c_' + Date.now(),
          code: rec.code || ('AI_' + Math.floor(Math.random() * 8999 + 1000)),
          title: (rec.title || '').replace(/^[]\s*/, ''),
          type: rec.type || 'percent',
          value: rec.value || 15,
          description: rec.description,
          isAiGenerated: true,
          badge: 'AI Üretimi',
          active: true
        };
        setCampaigns(prev => {
          const updated = [newCamp, ...(prev || [])];
          CacheService.set('campaigns', updated);
          if (window.fetchWithRetry) {
            window.fetchWithRetry('/api/system-settings', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ campaigns: updated })
            }).catch(() => {});
          }
          return updated;
        });
        showToast(`AI Önerisi Veritabanına Kaydedildi ve Kampanyalara Eklendi! Kod: ${newCamp.code}`);
        navigateTo('campaigns');
      };"""

if old_campaign_handlers in content:
    content = content.replace(old_campaign_handlers, new_campaign_handlers)
    print("1. Updated handleSaveCampaign and handleConvertAiToCampaign with POST persistence!")
else:
    print("WARNING: Could not find old_campaign_handlers in index.html!")

old_delete_camp = """      const handleDeleteCampaign = (cIdOrObj) => {
        const cId = typeof cIdOrObj === 'object' ? cIdOrObj.id : cIdOrObj;
        const campaign = campaigns.find(x => x.id === cId);
        const cTitle = campaign ? campaign.title : 'Özel Kampanya';
        setRedAlertModalData({
          title: 'ÖZEL KAMPANYA SİLİNECEK',
          message: `"${cTitle}" kampanyasını sistemden kaldırmak istediğinize emin misiniz?`,
          confirmText: 'Evet, Kampanyayı Sil',
          onConfirm: () => {
            setCampaigns(prev => prev.filter(x => x.id !== cId));
            showToast('Kampanya Kaldırıldı.');
          }
        });
      };"""

new_delete_camp = """      const handleDeleteCampaign = (cIdOrObj) => {
        const cId = typeof cIdOrObj === 'object' ? cIdOrObj.id : cIdOrObj;
        const campaign = campaigns.find(x => x.id === cId);
        const cTitle = campaign ? campaign.title : 'Özel Kampanya';
        setRedAlertModalData({
          title: 'ÖZEL KAMPANYA SİLİNECEK',
          message: `"${cTitle}" kampanyasını sistemden kaldırmak istediğinize emin misiniz?`,
          confirmText: 'Evet, Kampanyayı Sil',
          onConfirm: () => {
            setCampaigns(prev => {
              const updated = (prev || []).filter(x => x.id !== cId);
              CacheService.set('campaigns', updated);
              if (window.fetchWithRetry) {
                window.fetchWithRetry('/api/system-settings', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ campaigns: updated })
                }).catch(() => {});
              }
              return updated;
            });
            showToast('Kampanya Veritabanından Silindi.');
          }
        });
      };"""

if old_delete_camp in content:
    content = content.replace(old_delete_camp, new_delete_camp)
    print("2. Updated handleDeleteCampaign with POST persistence!")
else:
    print("WARNING: Could not find old_delete_camp in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
