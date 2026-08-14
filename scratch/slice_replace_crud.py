import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

new_code = """const handleSaveVenue = async (vObj) => {
        try {
          const fetchFn = window.fetchWithRetry || fetch;
          const resp = await fetchFn('/api/venues', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(vObj)
          });
          const data = await resp.json();
          const savedItem = (data && data.item) ? data.item : vObj;

          setVenues(prev => {
            const idx = prev.findIndex(x => String(x.id) === String(savedItem.id));
            let updated;
            if (idx >= 0) {
              updated = [...prev];
              updated[idx] = savedItem;
            } else {
              updated = [...prev, savedItem];
            }
            CacheService.set('venues', updated);
            return updated;
          });
        } catch(err) {
          console.error('Save venue error:', err);
        }
        setVenueModalData(null);
        showToast('Düğün Salonu ve Maliyetleri Başarıyla Kaydedildi!');
      };

      const handleDeleteVenue = (vIdOrObj) => {
        const vId = typeof vIdOrObj === 'object' ? (vIdOrObj?.id || vIdOrObj) : vIdOrObj;
        const venue = venues.find(x => String(x.id) === String(vId));
        const vName = venue ? venue.name : 'Düğün Salonu';
        setRedAlertModalData({
          title: 'DÜĞÜN SALONU SİLİNECEK',
          message: `"${vName}" salonunu sistemden tamamen silmek istediğinize emin misiniz? Bu işlem geri alınamaz.`,
          confirmText: 'Evet, Salonu Sil',
          onConfirm: async () => {
            try {
              const fetchFn = window.fetchWithRetry || fetch;
              await fetchFn(`/api/venues/${vId}`, { method: 'DELETE' });
            } catch(e) {}

            setVenues(prev => {
              const updated = prev.filter(x => String(x.id) !== String(vId));
              CacheService.set('venues', updated);
              return updated;
            });
            showToast('Düğün Salonu Sistemden Silindi.');
          }
        });
      };

      const handleSaveService = async (sObj) => {
        try {
          const fetchFn = window.fetchWithRetry || fetch;
          const resp = await fetchFn('/api/services', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(sObj)
          });
          const data = await resp.json();
          const savedItem = (data && data.item) ? data.item : sObj;

          setServices(prev => {
            const idx = prev.findIndex(x => String(x.id) === String(savedItem.id));
            let updated;
            if (idx >= 0) {
              updated = [...prev];
              updated[idx] = savedItem;
            } else {
              updated = [...prev, savedItem];
            }
            CacheService.set('services', updated);
            return updated;
          });
        } catch(err) {
          console.error('Save service error:', err);
        }

        setServiceModalData(null);
        showToast('Ek Hizmet ve Maliyeti Başarıyla Kaydedildi!');
      };

      const handleDeleteService = (sIdOrObj) => {
        const sId = typeof sIdOrObj === 'object' ? (sIdOrObj?.id || sIdOrObj) : sIdOrObj;
        const service = services.find(x => String(x.id) === String(sId));
        const sName = service ? service.name : 'Ek Hizmet';
        setRedAlertModalData({
          title: 'EK HİZMET SİLİNECEK',
          message: `"${sName}" ek hizmet kartını silmek istediğinize emin misiniz?`,
          confirmText: 'Evet, Hizmeti Sil',
          onConfirm: async () => {
            try {
              const fetchFn = window.fetchWithRetry || fetch;
              await fetchFn(`/api/services/${sId}`, { method: 'DELETE' });
            } catch(e) {}

            setServices(prev => {
              const updated = prev.filter(x => String(x.id) !== String(sId));
              CacheService.set('services', updated);
              return updated;
            });
            showToast('Ek Hizmet Başarıyla Silindi.');
          }
        });
      };

      """

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    start_str = "const handleSaveVenue = (vObj) => {"
    end_str = "const handleReorderServices = (newServicesList) => {"

    start_idx = content.find(start_str)
    end_idx = content.find(end_str)

    if start_idx != -1 and end_idx != -1:
        content = content[:start_idx] + new_code + content[end_idx:]
        with open(h_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully replaced CRUD handlers in {h_file}")
    else:
        print(f"Indices not found in {h_file}: start={start_idx}, end={end_idx}")

print("All HTML files updated!")
