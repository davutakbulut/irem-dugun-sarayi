import os

# 1. UPDATE server.js: Add ALTER TABLE checks for venues and enrich GET /api/venues and POST /api/venues
with open('server.js', 'r', encoding='utf-8') as f:
    server_code = f.read()

# Add table columns alter
venue_columns_alter = """
      // Ensure venues table has all rich columns
      try { await pool.query("ALTER TABLE venues ADD COLUMN IF NOT EXISTS cost_price DECIMAL(12,2) DEFAULT 0.00;"); } catch(e){}
      try { await pool.query("ALTER TABLE venues ADD COLUMN IF NOT EXISTS exterior_images_json LONGTEXT;"); } catch(e){}
      try { await pool.query("ALTER TABLE venues ADD COLUMN IF NOT EXISTS event_types_json LONGTEXT;"); } catch(e){}
      try { await pool.query("ALTER TABLE venues ADD COLUMN IF NOT EXISTS available_services_json LONGTEXT;"); } catch(e){}
      try {
        await pool.query(`
          UPDATE venues SET
            images_json = '["https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=1200&q=80", "https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=800&q=80", "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=800&q=80", "https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?auto=format&fit=crop&w=800&q=80"]',
            exterior_images_json = '["https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?auto=format&fit=crop&w=800&q=80", "https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&w=800&q=80", "https://images.unsplash.com/photo-1527529482837-4698179dc6ce?auto=format&fit=crop&w=800&q=80"]',
            event_types_json = '["Düğün", "Nişan", "Kına", "Kurumsal Etkinlik", "Gala", "Sünnet Düğünü"]',
            available_services_json = '["s1", "s2", "s3", "s-tavuk-menu"]',
            features_json = '["Geniş Dans Pisti", "Gelişmiş İklimlendirme", "Özel Gelin & Damat Odası", "Ücretsiz Otopark & Vale", "Kristal Avizeler & Sahne", "Gelişmiş Ses & Işık Sistemi", "Jeneratör Desteği", "VIP Karşılama Alanı"]',
            location = 'Sapanca Göl Kenarı, Sakarya / İrem Düğün Sarayı'
          WHERE id = 'v1' OR id = 'venue-1';
        `);
      } catch(e){}
"""

# Replace in server.js initialization
if "ALTER TABLE venues ADD COLUMN IF NOT EXISTS exterior_images_json" not in server_code:
    pos = server_code.find("UPDATE venues SET")
    if pos != -1:
        end_pos = server_code.find("} catch(e){}", pos) + 12
        server_code = server_code[:pos-12] + venue_columns_alter + server_code[end_pos:]

# Update GET /api/venues to parse exteriorImages, eventTypes, availableServices
new_get_venues = """app.get('/api/venues', async (req, res) => {
  const activePool = await getPool();
  if (activePool) {
    try {
      const [rows] = await activePool.query('SELECT * FROM venues ORDER BY created_at DESC');
      const formatted = (rows || []).map(v => {
        let imgs = [];
        if (typeof v.images_json === 'string') {
          try { imgs = JSON.parse(v.images_json); } catch(e){}
        } else if (Array.isArray(v.images_json)) {
          imgs = v.images_json;
        }
        if (!imgs || imgs.length === 0) {
          imgs = [
            'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=1200&q=80',
            'https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=800&q=80'
          ];
        }

        let extImgs = [];
        if (typeof v.exterior_images_json === 'string') {
          try { extImgs = JSON.parse(v.exterior_images_json); } catch(e){}
        } else if (Array.isArray(v.exterior_images_json)) {
          extImgs = v.exterior_images_json;
        }
        if (!extImgs || extImgs.length === 0) {
          extImgs = [
            'https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1527529482837-4698179dc6ce?auto=format&fit=crop&w=800&q=80'
          ];
        }

        let feats = [];
        if (typeof v.features_json === 'string') {
          try { feats = JSON.parse(v.features_json); } catch(e){}
        } else if (Array.isArray(v.features_json)) {
          feats = v.features_json;
        }
        if (!feats || feats.length === 0) {
          feats = ['Geniş Dans Pisti', 'Gelişmiş İklimlendirme', 'Özel Gelin Odası', 'Otopark & Vale', 'Kristal Avizeler', 'Lüks Sahne'];
        }

        let evTypes = [];
        if (typeof v.event_types_json === 'string') {
          try { evTypes = JSON.parse(v.event_types_json); } catch(e){}
        } else if (Array.isArray(v.event_types_json)) {
          evTypes = v.event_types_json;
        }
        if (!evTypes || evTypes.length === 0) {
          evTypes = ['Düğün', 'Nişan', 'Kına', 'Kurumsal Etkinlik', 'Gala', 'Sünnet Düğünü'];
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
          costPrice: v.cost_price ? Number(v.cost_price) : 0,
          occupancyRate: v.occupancy_rate || 85,
          price: Number(v.price || 0),
          deposit: Number(v.deposit || 0),
          capacity: Number(v.capacity || 500)
        };
      });
      return res.json(formatted);
    } catch(e) {
      console.error('MySQL GET /api/venues error:', e.message);
    }
  }
  res.json([]);
});"""

new_post_venues = """app.post('/api/venues', async (req, res) => {
  const item = { id: req.body.id || ('v-' + Date.now()), ...req.body };
  const imgs = Array.isArray(item.images) && item.images.length > 0 ? item.images : (item.image ? [item.image] : []);
  const extImgs = Array.isArray(item.exteriorImages) && item.exteriorImages.length > 0 ? item.exteriorImages : [];
  const feats = Array.isArray(item.features) ? item.features : [];
  const evTypes = Array.isArray(item.eventTypes) ? item.eventTypes : [];
  const availServs = Array.isArray(item.availableServices) ? item.availableServices : [];
  const costPrice = item.costPrice !== undefined ? Number(item.costPrice) : (item.cost_price !== undefined ? Number(item.cost_price) : 0);
  const occupancyRate = item.occupancyRate !== undefined ? Number(item.occupancyRate) : (item.occupancy_rate !== undefined ? Number(item.occupancy_rate) : 85);

  if (pool) {
    try {
      await pool.query(
        `INSERT INTO venues (id, name, category, capacity, price, deposit, cost_price, location, description, occupancy_rate, features_json, images_json, exterior_images_json, event_types_json, available_services_json) 
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
         ON DUPLICATE KEY UPDATE 
           name=?, category=?, capacity=?, price=?, deposit=?, cost_price=?, location=?, description=?, occupancy_rate=?, features_json=?, images_json=?, exterior_images_json=?, event_types_json=?, available_services_json=?`,
        [
          item.id, item.name, item.category || 'Kapalı Salon', item.capacity || 500, item.price || 0, item.deposit || 0, costPrice, item.location || '', item.description || '', occupancyRate, JSON.stringify(feats), JSON.stringify(imgs), JSON.stringify(extImgs), JSON.stringify(evTypes), JSON.stringify(availServs),
          item.name, item.category || 'Kapalı Salon', item.capacity || 500, item.price || 0, item.deposit || 0, costPrice, item.location || '', item.description || '', occupancyRate, JSON.stringify(feats), JSON.stringify(imgs), JSON.stringify(extImgs), JSON.stringify(evTypes), JSON.stringify(availServs)
        ]
      );
    } catch(e) {
      console.error('MySQL POST /api/venues error:', e.message);
    }
  }
  res.status(201).json({ success: true, item: { ...item, costPrice, occupancyRate, features: feats, images: imgs, interiorImages: imgs, exteriorImages: extImgs, eventTypes: evTypes, availableServices: availServs, location: item.location || '' } });
});"""

v_get_start = server_code.find("app.get('/api/venues'")
v_del_start = server_code.find("app.delete('/api/venues/:id'")
if v_get_start != -1 and v_del_start != -1:
    server_code = server_code[:v_get_start] + new_get_venues + "\n\n" + new_post_venues + "\n\n" + server_code[v_del_start:]

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(server_code)

print("Updated server.js with complete exterior images, event types, features, and available services!")

# 2. UPDATE VenueModalComponent to include Exterior Images and Occupancy Rate along with Features & Event Types
new_venue_modal_code = """    // --- VENUE MODAL COMPONENT (100% SYNCED WITH MYSQL & VENUE POPUP DETAILS) ---
    function VenueModalComponent({ venue, allServices = [], onClose, onSave }) {
      const [name, setName] = useState(venue?.name || '');
      const [category, setCategory] = useState(venue?.category || 'Kapalı Salon');
      const [capacity, setCapacity] = useState(venue?.capacity || 750);
      const [price, setPrice] = useState(venue?.price || 100000);
      const [costPrice, setCostPrice] = useState(venue?.costPrice !== undefined ? venue.costPrice : Math.round((venue?.price || 100000) * 0.55));
      const [deposit, setDeposit] = useState(venue?.deposit || 15000);
      const [occupancyRate, setOccupancyRate] = useState(venue?.occupancyRate !== undefined ? venue.occupancyRate : 85);
      const [location, setLocation] = useState(venue?.location || 'Sapanca Göl Kenarı, Sakarya / İrem Düğün Sarayı');
      const [description, setDescription] = useState(venue?.description || 'Yüksek tavanlı, kristal avizeli, iklimlendirme sistemli ve lüks sahne düzenine sahip ana balo salonumuz.');
      
      // IMAGES (INTERIOR & COVER)
      const [image, setImage] = useState(venue?.image || venue?.images?.[0] || 'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=1200&q=80');
      const [interiorImages, setInteriorImages] = useState(
        (venue?.interiorImages && venue.interiorImages.length > 0) 
          ? venue.interiorImages 
          : (venue?.images && venue.images.length > 0) ? venue.images : [
            'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=800&q=80'
          ]
      );
      const [newInteriorInput, setNewInteriorInput] = useState('');

      const addInteriorImg = () => {
        const trimmed = newInteriorInput.trim();
        if (trimmed && !interiorImages.includes(trimmed)) {
          setInteriorImages([...interiorImages, trimmed]);
          setNewInteriorInput('');
        }
      };

      const removeInteriorImg = (imgUrl) => {
        setInteriorImages(interiorImages.filter(x => x !== imgUrl));
      };

      // EXTERIOR IMAGES
      const [exteriorImages, setExteriorImages] = useState(
        (venue?.exteriorImages && venue.exteriorImages.length > 0)
          ? venue.exteriorImages
          : [
            'https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1527529482837-4698179dc6ce?auto=format&fit=crop&w=800&q=80'
          ]
      );
      const [newExteriorInput, setNewExteriorInput] = useState('');

      const addExteriorImg = () => {
        const trimmed = newExteriorInput.trim();
        if (trimmed && !exteriorImages.includes(trimmed)) {
          setExteriorImages([...exteriorImages, trimmed]);
          setNewExteriorInput('');
        }
      };

      const removeExteriorImg = (imgUrl) => {
        setExteriorImages(exteriorImages.filter(x => x !== imgUrl));
      };

      // FEATURES / MEKAN ÖZELLİKLERİ ROZETLERİ (Directly shown on reservation card & modal)
      const defaultFeaturesList = ['Geniş Dans Pisti', 'Gelişmiş İklimlendirme', 'Özel Gelin & Damat Odası', 'Ücretsiz Otopark & Vale', 'Kristal Avizeler & Sahne', 'Gelişmiş Ses & Işık Sistemi', 'Jeneratör Desteği', 'VIP Karşılama Alanı'];
      const [features, setFeatures] = useState(
        (venue?.features && venue.features.length > 0) ? venue.features : defaultFeaturesList
      );
      const [newFeatureInput, setNewFeatureInput] = useState('');

      const addFeature = (fText) => {
        const textToAdd = (fText || newFeatureInput).trim();
        if (textToAdd && !features.includes(textToAdd)) {
          setFeatures([...features, textToAdd]);
          if (!fText) setNewFeatureInput('');
        }
      };

      const removeFeature = (fToRemove) => {
        setFeatures(features.filter(f => f !== fToRemove));
      };

      // EVENT TYPES
      const [eventTypes, setEventTypes] = useState(
        (venue?.eventTypes && venue.eventTypes.length > 0) 
          ? venue.eventTypes 
          : ['Düğün', 'Nişan', 'Kına', 'Kurumsal Etkinlik', 'Gala', 'Sünnet Düğünü']
      );
      const [newEventInput, setNewEventInput] = useState('');

      const addEventType = () => {
        const trimmed = newEventInput.trim();
        if (trimmed && !eventTypes.includes(trimmed)) {
          setEventTypes([...eventTypes, trimmed]);
          setNewEventInput('');
        }
      };

      const removeEventType = (typeToRemove) => {
        setEventTypes(eventTypes.filter(t => t !== typeToRemove));
      };
      
      const defaultServicesList = [...(allServices || [])].sort((a, b) => {
        const oA = typeof a.order === 'number' ? a.order : (typeof a.sortOrder === 'number' ? a.sortOrder : 9999);
        const oB = typeof b.order === 'number' ? b.order : (typeof b.sortOrder === 'number' ? b.sortOrder : 9999);
        return oA - oB;
      });

      const [selectedServices, setSelectedServices] = useState(
        venue?.availableServices || ['s1', 's2', 's3', 's-tavuk-menu']
      );

      const toggleService = (srvId) => {
        setSelectedServices(prev => 
          prev.includes(srvId) ? prev.filter(id => id !== srvId) : [...prev, srvId]
        );
      };

      const handleSubmit = (e) => {
        e.preventDefault();
        onSave({
          id: venue?.id || `v-${Date.now()}`,
          name,
          category,
          capacity: Number(capacity),
          price: Number(price),
          costPrice: Number(costPrice),
          deposit: Number(deposit),
          occupancyRate: Number(occupancyRate),
          location,
          description,
          image,
          images: interiorImages.length > 0 ? interiorImages : [image],
          interiorImages: interiorImages.length > 0 ? interiorImages : [image],
          exteriorImages: exteriorImages,
          features: features,
          eventTypes: eventTypes,
          availableServices: selectedServices
        });
      };

      const estimatedProfit = Math.max(0, Number(price) - Number(costPrice));
      const estimatedMargin = Number(price) > 0 ? ((estimatedProfit / Number(price)) * 100).toFixed(1) : 0;

      return (
        <div className="fixed inset-0 z-[999999] bg-black/75 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in">
          <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-2xl w-full p-6 space-y-4 shadow-2xl max-h-[92vh] overflow-y-auto custom-scrollbar">
            <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border">
              <h3 className="text-lg font-bold text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                <ThemeIcon icon="venue" className="w-5 h-5 text-amber-500 inline" />
                <span>{venue ? 'Etkinlik Mekanını Düzenle' : 'Yeni Etkinlik Mekanı Ekle'}</span>
              </h3>
              <button onClick={onClose} className="text-slate-400 hover:text-slate-600 dark:hover:text-white font-bold text-lg cursor-pointer">✕</button>
            </div>
            
            <form onSubmit={handleSubmit} className="space-y-4 text-xs">
              <div>
                <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Etkinlik Mekanı Adı:</label>
                <input type="text" value={name} onChange={e => setName(e.target.value)} required placeholder="Örn: Kraliyet Balo Salonu / Kır Bahçesi" className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold" />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Mekan Kategorisi / Konsepti:</label>
                  <input type="text" value={category} onChange={e => setCategory(e.target.value)} required placeholder="Örn: Kapalı Salon, Balo Salonu, Kır Bahçesi" className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200" />
                </div>
                <div>
                  <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Maksimum Kapasite (Kişi):</label>
                  <input type="number" value={capacity} onChange={e => setCapacity(e.target.value)} required className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold" />
                </div>
              </div>

              <div className="grid grid-cols-4 gap-2">
                <div>
                  <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Satış Fiyatı (TL):</label>
                  <input type="number" value={price} onChange={e => setPrice(e.target.value)} required className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2 text-amber-700 font-bold" />
                </div>
                <div>
                  <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Maliyet (TL):</label>
                  <input type="number" value={costPrice} onChange={e => setCostPrice(e.target.value)} required className="w-full bg-slate-50 dark:bg-brand-dark border border-blue-500/40 rounded-xl p-2 text-blue-600 dark:text-blue-400 font-bold" />
                </div>
                <div>
                  <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Asgari Kapora (TL):</label>
                  <input type="number" value={deposit} onChange={e => setDeposit(e.target.value)} required className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2 text-emerald-600 font-bold" />
                </div>
                <div>
                  <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Doluluk Oranı (%):</label>
                  <input type="number" min="0" max="100" value={occupancyRate} onChange={e => setOccupancyRate(e.target.value)} required className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2 text-blue-600 font-bold" />
                </div>
              </div>

              <div className="p-2.5 bg-slate-100 dark:bg-brand-dark rounded-xl border border-slate-200 dark:border-brand-border flex justify-between items-center text-[11px] font-bold">
                <span className="text-slate-600 dark:text-gray-400">Tahmini Mekan Kârı: <strong className="text-emerald-600 font-mono">{formatCurrency(estimatedProfit)}</strong></span>
                <span className="bg-emerald-500/20 text-emerald-700 dark:text-emerald-300 px-2 py-0.5 rounded-md border border-emerald-500/30">%{estimatedMargin} Kâr Marjı</span>
              </div>

              <div>
                <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Mekan Konumu & Adres:</label>
                <input type="text" value={location} onChange={e => setLocation(e.target.value)} required placeholder="Örn: Sapanca Göl Kenarı, Sakarya / İrem Düğün Sarayı" className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200" />
              </div>

              {/* 🌟 MEKAN ÖZELLİKLERİ VE ROZETLERİ */}
              <div className="border border-amber-500/30 bg-amber-500/5 rounded-2xl p-3.5 space-y-2.5">
                <div className="flex items-center justify-between">
                  <label className="font-extrabold text-slate-900 dark:text-white flex items-center space-x-1.5">
                    <span>✨ Mekan Özellikleri & Rozetleri (Kartta ve Pop-up'ta Görünenler):</span>
                  </label>
                  <span className="text-[10px] text-amber-700 dark:text-gold-400 font-bold">({features.length} Özellik Tanımlı)</span>
                </div>
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={newFeatureInput}
                    onChange={e => setNewFeatureInput(e.target.value)}
                    onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); addFeature(); } }}
                    placeholder="Örn: Helikopter Pisti, Deniz Manzaralı, VIP Lounge (Enter'a basın)"
                    className="flex-1 bg-white dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2 text-slate-800 dark:text-gray-200 text-xs font-bold"
                  />
                  <button type="button" onClick={() => addFeature()} className="gold-button font-bold px-3 py-2 rounded-xl text-xs shrink-0 cursor-pointer">+ Ekle</button>
                </div>
                <div className="flex flex-wrap gap-1.5 pt-1 max-h-28 overflow-y-auto custom-scrollbar">
                  {features.map((feat, fIdx) => (
                    <span key={fIdx} className="inline-flex items-center space-x-1 text-[11px] bg-white dark:bg-brand-card text-slate-800 dark:text-gray-200 font-bold px-2.5 py-1 rounded-lg border border-slate-200 dark:border-brand-border shadow-xs">
                      <span>✨ {feat}</span>
                      <button type="button" onClick={() => removeFeature(feat)} className="hover:text-red-500 text-slate-400 font-extrabold ml-1.5 cursor-pointer">✕</button>
                    </span>
                  ))}
                </div>
              </div>

              {/* 🎯 DÜZENLENEBİLEN ETKİNLİK TÜRLERİ */}
              <div className="border border-slate-200 dark:border-brand-border/60 bg-slate-50/50 dark:bg-brand-dark/30 rounded-2xl p-3.5 space-y-2.5">
                <div className="flex items-center justify-between">
                  <label className="font-extrabold text-slate-900 dark:text-white flex items-center space-x-1.5">
                    <span>🎯 Düzenlenebilen Etkinlik Türleri (Pop-up'ta Görünenler):</span>
                  </label>
                  <span className="text-[10px] text-amber-600 font-bold">({eventTypes.length} Tür Tanımlı)</span>
                </div>
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={newEventInput}
                    onChange={e => setNewEventInput(e.target.value)}
                    onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); addEventType(); } }}
                    placeholder="Örn: Sünnet Düğünü, Mezuniyet, Gala (Enter'a basın)"
                    className="flex-1 bg-white dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2 text-slate-800 dark:text-gray-200 text-xs font-bold"
                  />
                  <button type="button" onClick={addEventType} className="gold-button font-bold px-3 py-2 rounded-xl text-xs shrink-0 cursor-pointer">+ Ekle</button>
                </div>
                <div className="flex flex-wrap gap-1.5 pt-1 max-h-24 overflow-y-auto custom-scrollbar">
                  {eventTypes.map((type, tIdx) => (
                    <span key={tIdx} className="inline-flex items-center space-x-1 text-[11px] bg-amber-500/10 dark:bg-amber-500/20 text-amber-800 dark:text-amber-300 font-bold px-2.5 py-1 rounded-lg border border-amber-500/30">
                      <span>◎ {type}</span>
                      <button type="button" onClick={() => removeEventType(type)} className="hover:text-red-500 font-extrabold ml-1.5 cursor-pointer">✕</button>
                    </span>
                  ))}
                </div>
              </div>

              {/* 🏢 İÇ MEKAN & BALO SALONU GÖRSELLERİ GALERİSİ */}
              <div className="border border-slate-200 dark:border-brand-border/60 bg-slate-50/50 dark:bg-brand-dark/30 rounded-2xl p-3.5 space-y-2.5">
                <div className="flex items-center justify-between">
                  <label className="font-extrabold text-slate-900 dark:text-white flex items-center space-x-1.5">
                    <span>🏢 İç Mekan & Balo Salonu Görselleri ({interiorImages.length}):</span>
                  </label>
                </div>
                <div className="flex gap-2">
                  <input
                    type="url"
                    value={newInteriorInput}
                    onChange={e => setNewInteriorInput(e.target.value)}
                    placeholder="Görsel URL'si yapıştırın (https://...)"
                    className="flex-1 bg-white dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2 text-slate-800 dark:text-gray-200 text-xs"
                  />
                  <button type="button" onClick={addInteriorImg} className="gold-button font-bold px-3 py-2 rounded-xl text-xs shrink-0 cursor-pointer">+ Görsel Ekle</button>
                </div>
                <div className="grid grid-cols-3 sm:grid-cols-4 gap-2 pt-1">
                  {interiorImages.map((imgUrl, idx) => (
                    <div key={idx} className="relative group rounded-xl overflow-hidden h-16 border border-slate-200 dark:border-brand-border">
                      <img src={imgUrl} alt="İç Görsel" className="w-full h-full object-cover" />
                      <button type="button" onClick={() => removeInteriorImg(imgUrl)} className="absolute top-1 right-1 bg-red-600 text-white rounded-full w-5 h-5 flex items-center justify-center text-[10px] font-bold opacity-80 group-hover:opacity-100 cursor-pointer">✕</button>
                    </div>
                  ))}
                </div>
              </div>

              {/* ☀️ DIŞ MEKAN & GÖL MANZARASI GÖRSELLERİ GALERİSİ */}
              <div className="border border-slate-200 dark:border-brand-border/60 bg-slate-50/50 dark:bg-brand-dark/30 rounded-2xl p-3.5 space-y-2.5">
                <div className="flex items-center justify-between">
                  <label className="font-extrabold text-slate-900 dark:text-white flex items-center space-x-1.5">
                    <span>☀️ Dış Mekan & Göl Manzarası Görselleri ({exteriorImages.length}):</span>
                  </label>
                </div>
                <div className="flex gap-2">
                  <input
                    type="url"
                    value={newExteriorInput}
                    onChange={e => setNewExteriorInput(e.target.value)}
                    placeholder="Dış mekan görsel URL'si yapıştırın (https://...)"
                    className="flex-1 bg-white dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2 text-slate-800 dark:text-gray-200 text-xs"
                  />
                  <button type="button" onClick={addExteriorImg} className="gold-button font-bold px-3 py-2 rounded-xl text-xs shrink-0 cursor-pointer">+ Görsel Ekle</button>
                </div>
                <div className="grid grid-cols-3 sm:grid-cols-4 gap-2 pt-1">
                  {exteriorImages.map((imgUrl, idx) => (
                    <div key={idx} className="relative group rounded-xl overflow-hidden h-16 border border-slate-200 dark:border-brand-border">
                      <img src={imgUrl} alt="Dış Görsel" className="w-full h-full object-cover" />
                      <button type="button" onClick={() => removeExteriorImg(imgUrl)} className="absolute top-1 right-1 bg-red-600 text-white rounded-full w-5 h-5 flex items-center justify-center text-[10px] font-bold opacity-80 group-hover:opacity-100 cursor-pointer">✕</button>
                    </div>
                  ))}
                </div>
              </div>

              {/* SEÇİLEBİLİR EK HİZMETLER TANIMLAMA */}
              <div className="border-t border-b border-slate-200 dark:border-brand-border/60 py-3 space-y-2">
                <label className="font-extrabold block text-slate-800 dark:text-gray-100 flex items-center justify-between">
                  <span><ThemeIcon icon="gift" className="w-4 h-4 inline-block text-amber-500 shrink-0" /> Bu Mekanda Sunulabilecek Hizmetler:</span>
                  <span className="text-[10px] text-amber-600 font-bold">({selectedServices.length} Seçili)</span>
                </label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-h-32 overflow-y-auto custom-scrollbar p-2.5 bg-slate-50 dark:bg-brand-dark/60 border border-slate-200 dark:border-brand-border rounded-xl">
                  {defaultServicesList.map(srv => {
                    const isChecked = selectedServices.includes(srv.id);
                    return (
                      <label key={srv.id} className={`flex items-center space-x-2 p-2 rounded-xl cursor-pointer transition-all ${
                        isChecked 
                          ? 'bg-amber-500/10 border border-amber-500/30 text-amber-900 dark:text-amber-300 font-bold' 
                          : 'hover:bg-slate-200/50 dark:hover:bg-brand-card text-slate-700 dark:text-gray-300'
                      }`}>
                        <input
                          type="checkbox"
                          checked={isChecked}
                          onChange={() => toggleService(srv.id)}
                          className="accent-amber-500 rounded w-4 h-4 cursor-pointer"
                        />
                        <span className="text-xs truncate">{srv.name}</span>
                      </label>
                    );
                  })}
                </div>
              </div>

              <ImageDropzoneUploader
                label="Mekan Ana Kapak Görseli (URL veya Dosya)"
                value={image}
                onChange={setImage}
                aspectGuide="1200x800 px (16:9 Geniş)"
                placeholderIcon=""
              />

              <div>
                <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Açıklama & Mekan Tanıtım Metni:</label>
                <textarea value={description} onChange={e => setDescription(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 h-16 text-slate-800 dark:text-gray-200" placeholder="Mekan detayları, teknik altyapı ve imkanlar..." />
              </div>

              <div className="flex justify-end space-x-2 pt-2 border-t border-slate-200 dark:border-brand-border">
                <button type="button" onClick={onClose} className="px-4 py-2 bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-400 rounded-xl font-bold cursor-pointer">İptal</button>
                <button type="submit" className="gold-button font-bold px-5 py-2 rounded-xl cursor-pointer">Mekanı Kaydet ✓</button>
              </div>
            </form>
          </div>
        </div>
      );
    }"""

modal_start_marker = "// --- VENUE MODAL COMPONENT"
modal_end_marker = "// --- SERVICE MODAL COMPONENT ---"

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    s_idx = content.find(modal_start_marker)
    e_idx = content.find(modal_end_marker, s_idx)

    if s_idx != -1 and e_idx != -1:
        content = content[:s_idx] + new_venue_modal_code + "\n\n    " + content[e_idx:]
        with open(h_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated VenueModalComponent in {h_file}")
    else:
        print(f"Markers not found in {h_file}")

print("All files updated successfully!")
