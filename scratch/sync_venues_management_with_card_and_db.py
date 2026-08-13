import os

# 1. UPDATE server.js: Ensure POST /api/venues accepts and stores cost_price, location, features, images, etc.
with open('server.js', 'r', encoding='utf-8') as f:
    server_code = f.read()

new_post_venues = """app.post('/api/venues', async (req, res) => {
  const item = { id: req.body.id || ('v-' + Date.now()), ...req.body };
  const imgs = Array.isArray(item.images) && item.images.length > 0 ? item.images : (item.image ? [item.image] : []);
  const feats = Array.isArray(item.features) ? item.features : [];
  const costPrice = item.costPrice !== undefined ? Number(item.costPrice) : (item.cost_price !== undefined ? Number(item.cost_price) : 0);

  if (pool) {
    try {
      await pool.query(
        `INSERT INTO venues (id, name, category, capacity, price, deposit, cost_price, location, description, features_json, images_json) 
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
         ON DUPLICATE KEY UPDATE 
           name=?, category=?, capacity=?, price=?, deposit=?, cost_price=?, location=?, description=?, features_json=?, images_json=?`,
        [
          item.id, item.name, item.category || 'Kapalı Salon', item.capacity || 500, item.price || 0, item.deposit || 0, costPrice, item.location || '', item.description || '', JSON.stringify(feats), JSON.stringify(imgs),
          item.name, item.category || 'Kapalı Salon', item.capacity || 500, item.price || 0, item.deposit || 0, costPrice, item.location || '', item.description || '', JSON.stringify(feats), JSON.stringify(imgs)
        ]
      );
    } catch(e) {
      console.error('MySQL POST /api/venues error:', e.message);
    }
  }
  res.status(201).json({ success: true, item: { ...item, costPrice, features: feats, images: imgs, location: item.location || '' } });
});"""

v_start = server_code.find("app.post('/api/venues'")
if v_start != -1:
    v_end = server_code.find("app.delete('/api/venues/:id'", v_start)
    if v_end != -1:
        server_code = server_code[:v_start] + new_post_venues + "\n\n" + server_code[v_end:]
        with open('server.js', 'w', encoding='utf-8') as f:
            f.write(server_code)
        print("Updated server.js POST /api/venues successfully!")

# 2. UPDATE VenueModalComponent in all HTML files
html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

new_venue_modal_code = """    // --- VENUE MODAL COMPONENT (100% SYNCED WITH MYSQL & VENUE CARD) ---
    function VenueModalComponent({ venue, allServices = [], onClose, onSave }) {
      const [name, setName] = useState(venue?.name || '');
      const [category, setCategory] = useState(venue?.category || 'Kapalı Salon');
      const [capacity, setCapacity] = useState(venue?.capacity || 750);
      const [price, setPrice] = useState(venue?.price || 100000);
      const [costPrice, setCostPrice] = useState(venue?.costPrice !== undefined ? venue.costPrice : Math.round((venue?.price || 100000) * 0.55));
      const [deposit, setDeposit] = useState(venue?.deposit || 15000);
      const [location, setLocation] = useState(venue?.location || 'Sapanca Göl Kenarı, Sakarya / İrem Düğün Sarayı');
      const [description, setDescription] = useState(venue?.description || 'Yüksek tavanlı, kristal avizeli, iklimlendirme sistemli ve lüks sahne düzenine sahip ana balo salonumuz.');
      const [image, setImage] = useState(venue?.image || venue?.images?.[0] || 'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=1200&q=80');

      // FEATURES / MEKAN ÖZELLİKLERİ ROZETLERİ (Directly shown on reservation card)
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
        venue?.eventTypes || ['Düğün', 'Nişan', 'Kına', 'Kurumsal Etkinlik', 'Gala', 'Sünnet Düğünü']
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
          location,
          description,
          image,
          images: venue?.images && venue.images.length > 1 ? [image, ...venue.images.slice(1)] : [image],
          features: features,
          occupancyRate: venue?.occupancyRate || 85,
          eventTypes: eventTypes,
          availableServices: selectedServices
        });
      };

      const estimatedProfit = Math.max(0, Number(price) - Number(costPrice));
      const estimatedMargin = Number(price) > 0 ? ((estimatedProfit / Number(price)) * 100).toFixed(1) : 0;

      return (
        <div className="fixed inset-0 z-[999999] bg-black/75 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-xl w-full p-6 space-y-4 shadow-2xl max-h-[92vh] overflow-y-auto custom-scrollbar">
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

              <div className="grid grid-cols-3 gap-2">
                <div>
                  <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Satış Fiyatı (TL):</label>
                  <input type="number" value={price} onChange={e => setPrice(e.target.value)} required className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2 text-amber-700 font-bold" />
                </div>
                <div>
                  <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Maliyet Fiyatı (TL):</label>
                  <input type="number" value={costPrice} onChange={e => setCostPrice(e.target.value)} required className="w-full bg-slate-50 dark:bg-brand-dark border border-blue-500/40 rounded-xl p-2 text-blue-600 dark:text-blue-400 font-bold" />
                </div>
                <div>
                  <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Asgari Kapora (TL):</label>
                  <input type="number" value={deposit} onChange={e => setDeposit(e.target.value)} required className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2 text-emerald-600 font-bold" />
                </div>
              </div>

              <div>
                <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Mekan Konumu & Adres:</label>
                <input type="text" value={location} onChange={e => setLocation(e.target.value)} required placeholder="Örn: Sapanca Göl Kenarı, Sakarya / İrem Düğün Sarayı" className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200" />
              </div>

              {/* 🌟 MEKAN ÖZELLİKLERİ VE ROZETLERİ (KARTTA VE REZERVASYONDA GÖZÜKEN ALAN) */}
              <div className="border border-amber-500/30 bg-amber-500/5 rounded-2xl p-3.5 space-y-2.5">
                <div className="flex items-center justify-between">
                  <label className="font-extrabold text-slate-900 dark:text-white flex items-center space-x-1.5">
                    <span>✨ Mekan Özellikleri & Rozetleri (Kartta Görünen Alan):</span>
                  </label>
                  <span className="text-[10px] text-amber-700 dark:text-gold-400 font-bold">({features.length} Özellik Tanımlı)</span>
                </div>
                <p className="text-[11px] text-slate-500 dark:text-gray-400">
                  Rezervasyon sayfasındaki mekan kartında ve detay pop-up penceresinde listelenecek özellikleri ekleyin veya silin:
                </p>

                <div className="flex gap-2">
                  <input
                    type="text"
                    value={newFeatureInput}
                    onChange={e => setNewFeatureInput(e.target.value)}
                    onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); addFeature(); } }}
                    placeholder="Örn: Helikopter Pisti, Deniz Manzaralı, VIP Lounge (Enter'a basın)"
                    className="flex-1 bg-white dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2 text-slate-800 dark:text-gray-200 text-xs font-bold"
                  />
                  <button
                    type="button"
                    onClick={() => addFeature()}
                    className="gold-button font-bold px-3 py-2 rounded-xl text-xs shrink-0 cursor-pointer"
                  >
                    + Özellik Ekle
                  </button>
                </div>

                {/* FEATURE TAGS LIST */}
                <div className="flex flex-wrap gap-1.5 pt-1 max-h-32 overflow-y-auto custom-scrollbar">
                  {features.map((feat, fIdx) => (
                    <span key={fIdx} className="inline-flex items-center space-x-1 text-[11px] bg-white dark:bg-brand-card text-slate-800 dark:text-gray-200 font-bold px-2.5 py-1 rounded-lg border border-slate-200 dark:border-brand-border shadow-xs">
                      <span>✨ {feat}</span>
                      <button type="button" onClick={() => removeFeature(feat)} className="hover:text-red-500 text-slate-400 font-extrabold ml-1.5 cursor-pointer">✕</button>
                    </span>
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
                label="Mekan Kapak Görseli (URL veya Dosya)"
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

modal_start_marker = "// --- VENUE MODAL COMPONENT ---"
modal_end_marker = "// --- SERVICE MODAL COMPONENT ---"

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    s_idx = content.find(modal_start_marker)
    if s_idx == -1:
        s_idx = content.find("function VenueModalComponent({")
        if s_idx != -1:
            # backtrack to comment if any
            pass
    e_idx = content.find(modal_end_marker, s_idx)

    if s_idx != -1 and e_idx != -1:
        content = content[:s_idx] + new_venue_modal_code + "\n\n    " + content[e_idx:]
        with open(h_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated VenueModalComponent in {h_file}")
    else:
        print(f"Markers not found in {h_file}: s_idx={s_idx}, e_idx={e_idx}")

print("All venue management components synchronized with database and card layout!")
