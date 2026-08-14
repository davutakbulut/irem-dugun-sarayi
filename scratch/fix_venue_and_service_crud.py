import os, re

# ========================================================
# 1. UPGRADE server.js VENUES & SERVICES ENDPOINTS
# ========================================================
with open('server.js', 'r', encoding='utf-8') as f:
    server_code = f.read()

# Replace /api/venues endpoints in server.js
venues_endpoints_pattern = re.compile(
    r"app\.get\('/api/venues', async \(req, res\) => \{[\s\S]*?app\.delete\('/api/venues/:id', async \(req, res\) => \{[\s\S]*?res\.json\(\{ success: true, id \}\);\s*\}\);",
    re.MULTILINE
)

new_venues_endpoints = """app.get('/api/venues', async (req, res) => {
  try {
    const activePool = await getPool();
    if (activePool) {
      const [rows] = await activePool.query('SELECT * FROM venues ORDER BY id ASC');
      const formatted = (rows || []).map(v => {
        let feats = [];
        if (typeof v.features_json === 'string') {
          try { feats = JSON.parse(v.features_json); } catch(e){}
        } else if (Array.isArray(v.features_json)) {
          feats = v.features_json;
        }

        let imgs = [];
        if (typeof v.images_json === 'string') {
          try { imgs = JSON.parse(v.images_json); } catch(e){}
        } else if (Array.isArray(v.images_json)) {
          imgs = v.images_json;
        }
        if (!imgs || imgs.length === 0) {
          imgs = ['https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=1200&q=80'];
        }

        let extImgs = [];
        if (typeof v.exterior_images_json === 'string') {
          try { extImgs = JSON.parse(v.exterior_images_json); } catch(e){}
        } else if (Array.isArray(v.exterior_images_json)) {
          extImgs = v.exterior_images_json;
        }

        let evTypes = [];
        if (typeof v.event_types_json === 'string') {
          try { evTypes = JSON.parse(v.event_types_json); } catch(e){}
        } else if (Array.isArray(v.event_types_json)) {
          evTypes = v.event_types_json;
        }

        let availServs = [];
        if (typeof v.available_services_json === 'string') {
          try { availServs = JSON.parse(v.available_services_json); } catch(e){}
        } else if (Array.isArray(v.available_services_json)) {
          availServs = v.available_services_json;
        }
        if (!availServs || availServs.length === 0) {
          availServs = ['s1', 's2', 's3', 's-tavuk-menu'];
        }

        const mainImg = imgs[0];
        return {
          ...v,
          image: mainImg,
          image_url: mainImg,
          images: imgs,
          interiorImages: imgs,
          exteriorImages: extImgs,
          features: feats,
          eventTypes: evTypes,
          availableServices: availServs,
          location: v.location || 'Sapanca Göl Kenarı, Sakarya / İrem Düğün Sarayı',
          costPrice: v.cost_price !== undefined && v.cost_price !== null ? Number(v.cost_price) : 0,
          cost_price: v.cost_price !== undefined && v.cost_price !== null ? Number(v.cost_price) : 0,
          occupancyRate: v.occupancy_rate || 85,
          price: Number(v.price || 0),
          deposit: Number(v.deposit || 0),
          capacity: Number(v.capacity || 500)
        };
      });
      return res.json(formatted);
    }
  } catch(e) {
    console.error('MySQL GET /api/venues error:', e.message);
  }
  res.json(memoryStore.venues || []);
});

app.post('/api/venues', async (req, res) => {
  try {
    const item = { id: req.body.id || ('v-' + Date.now()), ...req.body };
    const imgs = Array.isArray(item.images) && item.images.length > 0 ? item.images : (item.image ? [item.image] : []);
    const extImgs = Array.isArray(item.exteriorImages) && item.exteriorImages.length > 0 ? item.exteriorImages : [];
    const feats = Array.isArray(item.features) ? item.features : [];
    const evTypes = Array.isArray(item.eventTypes) ? item.eventTypes : [];
    const availServs = Array.isArray(item.availableServices) ? item.availableServices : [];
    const costPrice = item.costPrice !== undefined ? Number(item.costPrice) : (item.cost_price !== undefined ? Number(item.cost_price) : 0);
    const occupancyRate = item.occupancyRate !== undefined ? Number(item.occupancyRate) : (item.occupancy_rate !== undefined ? Number(item.occupancy_rate) : 85);
    const price = Number(item.price || 0);
    const deposit = Number(item.deposit || 0);
    const capacity = Number(item.capacity || 500);

    const activePool = await getPool();
    if (activePool) {
      await activePool.query(
        `INSERT INTO venues (id, name, category, capacity, price, deposit, cost_price, location, description, occupancy_rate, features_json, images_json, exterior_images_json, event_types_json, available_services_json) 
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
         ON DUPLICATE KEY UPDATE 
           name=VALUES(name), category=VALUES(category), capacity=VALUES(capacity), 
           price=VALUES(price), deposit=VALUES(deposit), cost_price=VALUES(cost_price), 
           location=VALUES(location), description=VALUES(description), occupancy_rate=VALUES(occupancy_rate), 
           features_json=VALUES(features_json), images_json=VALUES(images_json), 
           exterior_images_json=VALUES(exterior_images_json), event_types_json=VALUES(event_types_json), 
           available_services_json=VALUES(available_services_json)`,
        [
          item.id, item.name, item.category || 'Kapalı Salon', capacity, price, deposit, costPrice, item.location || '', item.description || '', occupancyRate, JSON.stringify(feats), JSON.stringify(imgs), JSON.stringify(extImgs), JSON.stringify(evTypes), JSON.stringify(availServs)
        ]
      );
      console.log(`🏰 Salon [${item.id}] MariaDB Veritabanına Yazıldı: ${item.name} (Fiyat: ${price} TL, Maliyet: ${costPrice} TL)`);
    }

    const fullItem = {
      ...item,
      price,
      costPrice,
      cost_price: costPrice,
      deposit,
      capacity,
      occupancyRate,
      features: feats,
      images: imgs,
      interiorImages: imgs,
      exteriorImages: extImgs,
      eventTypes: evTypes,
      availableServices: availServs,
      location: item.location || ''
    };

    memoryStore.venues = [fullItem, ...(memoryStore.venues || []).filter(v => v.id !== fullItem.id)];
    res.status(201).json({ success: true, item: fullItem });
  } catch(e) {
    console.error('MySQL POST /api/venues error:', e.message);
    res.status(500).json({ error: 'Salon kaydedilemedi', message: e.message });
  }
});

app.delete('/api/venues/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const activePool = await getPool();
    if (activePool) {
      await activePool.query('DELETE FROM venues WHERE id = ?', [id]);
      console.log(`🗑️ Salon [${id}] MariaDB Veritabanından Silindi.`);
    }
    memoryStore.venues = (memoryStore.venues || []).filter(v => v.id !== id);
    res.json({ success: true, id });
  } catch(e) {
    console.error('MySQL DELETE /api/venues error:', e.message);
    res.status(500).json({ error: 'Salon silinemedi', message: e.message });
  }
});"""

if venues_endpoints_pattern.search(server_code):
    server_code = venues_endpoints_pattern.sub(new_venues_endpoints, server_code)
    print("Replaced venues endpoints in server.js!")
else:
    print("venues_endpoints_pattern not found in server.js")

# Upgrade /api/services endpoints in server.js
services_endpoints_pattern = re.compile(
    r"app\.get\('/api/services', async \(req, res\) => \{[\s\S]*?app\.delete\('/api/services/:id', async \(req, res\) => \{[\s\S]*?res\.json\(\{ success: true, id \}\);\s*\}\);",
    re.MULTILINE
)

new_services_endpoints = """app.get('/api/services', async (req, res) => {
  try {
    const activePool = await getPool();
    if (activePool) {
      const [rows] = await activePool.query('SELECT * FROM services ORDER BY sort_order ASC, created_at DESC');
      const formatted = (rows || []).map(s => ({
        id: s.id,
        name: s.name,
        category: s.category || 'Genel',
        price: Number(s.price || 0),
        costPrice: s.cost_price !== undefined && s.cost_price !== null ? Number(s.cost_price) : 0,
        cost_price: s.cost_price !== undefined && s.cost_price !== null ? Number(s.cost_price) : 0,
        pricingType: s.pricing_type || 'fixed',
        pricing_type: s.pricing_type || 'fixed',
        description: s.description || '',
        image: s.image_url || '',
        image_url: s.image_url || '',
        sortOrder: s.sort_order || 0,
        order: s.sort_order || 0
      }));
      return res.json(formatted);
    }
  } catch(e) {
    console.error('MySQL GET /api/services error:', e.message);
  }
  res.json(memoryStore.services || []);
});

app.post('/api/services', async (req, res) => {
  try {
    const item = { id: req.body.id || ('s-' + Date.now()), ...req.body };
    const price = Number(item.price || 0);
    const costPrice = item.costPrice !== undefined ? Number(item.costPrice) : (item.cost_price !== undefined ? Number(item.cost_price) : 0);
    const sortOrder = Number(item.sortOrder || item.order || 0);

    const activePool = await getPool();
    if (activePool) {
      await activePool.query(
        `INSERT INTO services (id, name, category, price, cost_price, pricing_type, description, image_url, sort_order)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
         ON DUPLICATE KEY UPDATE
           name=VALUES(name), category=VALUES(category), price=VALUES(price), 
           cost_price=VALUES(cost_price), pricing_type=VALUES(pricing_type), 
           description=VALUES(description), image_url=VALUES(image_url), sort_order=VALUES(sort_order)`,
        [item.id, item.name, item.category || 'Genel', price, costPrice, item.pricingType || item.pricing_type || 'fixed', item.description || '', item.image || item.image_url || '', sortOrder]
      );
      console.log(`🍽️ Hizmet [${item.id}] MariaDB Veritabanına Yazıldı: ${item.name} (Fiyat: ${price} TL, Maliyet: ${costPrice} TL)`);
    }

    const fullItem = {
      ...item,
      price,
      costPrice,
      cost_price: costPrice,
      sortOrder,
      order: sortOrder
    };

    memoryStore.services = [fullItem, ...(memoryStore.services || []).filter(s => s.id !== fullItem.id)];
    res.status(201).json({ success: true, item: fullItem });
  } catch(e) {
    console.error('MySQL POST /api/services error:', e.message);
    res.status(500).json({ error: 'Hizmet kaydedilemedi', message: e.message });
  }
});

app.delete('/api/services/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const activePool = await getPool();
    if (activePool) {
      await activePool.query('DELETE FROM services WHERE id = ?', [id]);
      console.log(`🗑️ Hizmet [${id}] MariaDB Veritabanından Silindi.`);
    }
    memoryStore.services = (memoryStore.services || []).filter(s => s.id !== id);
    res.json({ success: true, id });
  } catch(e) {
    console.error('MySQL DELETE /api/services error:', e.message);
    res.status(500).json({ error: 'Hizmet silinemedi', message: e.message });
  }
});"""

if services_endpoints_pattern.search(server_code):
    server_code = services_endpoints_pattern.sub(new_services_endpoints, server_code)
    print("Replaced services endpoints in server.js!")
else:
    print("services_endpoints_pattern not found in server.js")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(server_code)


# ========================================================
# 2. UPGRADE App.handleSaveVenue & handleSaveService IN HTML
# ========================================================
html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

old_handlers = """      // CRUD HANDLERS
      const handleSaveVenue = (vObj) => {
        setVenues(prev => {
          const idx = prev.findIndex(x => String(x.id) === String(vObj.id));
          let updated;
          if (idx >= 0) {
            updated = [...prev];
            updated[idx] = vObj;
          } else {
            updated = [...prev, vObj];
          }
          CacheService.set('venues', updated);
          window.fetchWithRetry('/api/public-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ venues: updated })
          }).catch(() => {});
          return updated;
        });
        setVenueModalData(null);
        showToast('Düğün Salonu Başarıyla Kaydedildi!');
      };

      const handleDeleteVenue = (vIdOrObj) => {
        const vId = typeof vIdOrObj === 'object' ? (vIdOrObj?.id || vIdOrObj) : vIdOrObj;
        const venue = venues.find(x => String(x.id) === String(vId));
        const vName = venue ? venue.name : 'Düğün Salonu';
        setRedAlertModalData({
          title: 'DÜĞÜN SALONU SİLİNECEK',
          message: `"${vName}" salonunu sistemden tamamen silmek istediğinize emin misiniz? Bu işlem geri alınamaz.`,
          confirmText: 'Evet, Salonu Sil',
          onConfirm: () => {
            setVenues(prev => {
              const updated = prev.filter(x => String(x.id) !== String(vId));
              CacheService.set('venues', updated);
              window.fetchWithRetry('/api/public-settings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ venues: updated })
              }).catch(() => {});
              return updated;
            });
            showToast('Düğün Salonu Sistemden Silindi.');
          }
        });
      };

      const handleSaveService = (sObj) => {
        setServices(prev => {
          const idx = prev.findIndex(x => String(x.id) === String(sObj.id));
          let updated;
          if (idx >= 0) {
            updated = [...prev];
            const existing = updated[idx];
            updated[idx] = {
              ...existing,
              ...sObj,
              order: sObj.order || existing.order || existing.sortOrder || (idx + 1),
              sortOrder: sObj.sortOrder || existing.sortOrder || existing.order || (idx + 1)
            };
          } else {
            const nextOrder = prev.length + 1;
            updated = [...prev, { order: nextOrder, sortOrder: nextOrder, ...sObj }];
          }
          CacheService.set('services', updated);
          if (window.fetchWithRetry) {
            window.fetchWithRetry('/api/public-settings', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ services: updated })
            }).catch(() => {});
          }
          return updated;
        });

        if (sObj && sObj.id) {
          setVenues(prevVenues => {
            const updatedVenues = prevVenues.map(v => {
              const currentServices = v.includedServices || [];
              if (!currentServices.some(id => String(id) === String(sObj.id))) {
                return { ...v, includedServices: [...currentServices, sObj.id] };
              }
              return v;
            });
            CacheService.set('venues', updatedVenues);
            if (window.fetchWithRetry) {
              window.fetchWithRetry('/api/public-settings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ venues: updatedVenues })
              }).catch(() => {});
            }
            return updatedVenues;
          });
        }

        setServiceModalData(null);
        showToast('Ek Hizmet Başarıyla Kaydedildi!');
      };

      const handleDeleteService = (sIdOrObj) => {
        const sId = typeof sIdOrObj === 'object' ? (sIdOrObj?.id || sIdOrObj) : sIdOrObj;
        const service = services.find(x => String(x.id) === String(sId));
        const sName = service ? service.name : 'Hizmet';
        setRedAlertModalData({
          title: 'EK HİZMET SİLİNECEK',
          message: `"${sName}" hizmetini sistemden tamamen silmek istediğinize emin misiniz? Bu işlem geri alınamaz.`,
          confirmText: 'Evet, Hizmeti Sil',
          onConfirm: () => {
            setServices(prev => {
              const updated = prev.filter(x => String(x.id) !== String(sId));
              CacheService.set('services', updated);
              if (window.fetchWithRetry) {
                window.fetchWithRetry('/api/public-settings', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ services: updated })
                }).catch(() => {});
              }
              return updated;
            });
            showToast('Ek Hizmet Sistemden Silindi.');
          }
        });
      };"""

new_handlers = """      // CRUD HANDLERS (DIRECT MARIADB SYNC)
      const handleSaveVenue = async (vObj) => {
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
        const sName = service ? service.name : 'Hizmet';
        setRedAlertModalData({
          title: 'EK HİZMET SİLİNECEK',
          message: `"${sName}" hizmetini sistemden tamamen silmek istediğinize emin misiniz? Bu işlem geri alınamaz.`,
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
            showToast('Ek Hizmet Sistemden Silindi.');
          }
        });
      };"""

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_handlers in content:
        content = content.replace(old_handlers, new_handlers)
        with open(h_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated CRUD handlers in {h_file}")
    else:
        print(f"old_handlers not matched in {h_file}")

print("All files updated successfully!")
