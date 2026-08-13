import os, json

# 1. UPDATE server.js: ENSURE VENUES TABLE HAS RICH DATA AND GET /api/venues ALWAYS RETURNS image, images, features, location
with open('server.js', 'r', encoding='utf-8') as f:
    server_code = f.read()

# Update seed query in server.js or add default update for Kraliyet Balo Salonu
venue_seed_update = """
      try {
        await pool.query(`
          UPDATE venues SET
            images_json = '["https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=1200&q=80", "https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=800&q=80", "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=800&q=80", "https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?auto=format&fit=crop&w=800&q=80"]',
            features_json = '["Geniş Dans Pisti", "Gelişmiş İklimlendirme", "Özel Gelin & Damat Odası", "Ücretsiz Otopark & Vale", "Kristal Avizeler & Sahne", "Gelişmiş Ses & Işık Sistemi", "Jeneratör Desteği", "VIP Karşılama Alanı"]',
            location = 'Sapanca Göl Kenarı, Sakarya / İrem Düğün Sarayı'
          WHERE id = 'v1' OR id = 'venue-1';
        `);
      } catch(e){}
"""

if "UPDATE venues SET" not in server_code:
    pos = server_code.find("CREATE TABLE IF NOT EXISTS venues (")
    if pos != -1:
        end_pos = server_code.find("ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;", pos)
        if end_pos != -1:
            ins_pos = server_code.find("`);", end_pos) + 3
            server_code = server_code[:ins_pos] + "\n" + venue_seed_update + "\n" + server_code[ins_pos:]

# Ensure GET /api/venues returns image, images, features cleanly
old_get_venues = """app.get('/api/venues', async (req, res) => {
  const activePool = await getPool();
  if (activePool) {
    try {
      const [rows] = await activePool.query('SELECT * FROM venues ORDER BY created_at DESC');
      const formatted = (rows || []).map(v => ({
        ...v,
        costPrice: v.cost_price ? Number(v.cost_price) : 0,
        occupancyRate: v.occupancy_rate || 0,
        features: typeof v.features_json === 'string' ? JSON.parse(v.features_json) : (v.features_json || []),
        images: typeof v.images_json === 'string' ? JSON.parse(v.images_json) : (v.images_json || [])
      }));
      return res.json(formatted);
    } catch(e) {
      console.error('MySQL GET /api/venues error:', e.message);
    }
  }
  res.json([]);
});"""

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

        let feats = [];
        if (typeof v.features_json === 'string') {
          try { feats = JSON.parse(v.features_json); } catch(e){}
        } else if (Array.isArray(v.features_json)) {
          feats = v.features_json;
        }
        if (!feats || feats.length === 0) {
          feats = ['Geniş Dans Pisti', 'Gelişmiş İklimlendirme', 'Özel Gelin Odası', 'Otopark & Vale', 'Kristal Avizeler', 'Lüks Sahne'];
        }

        const mainImg = imgs[0];
        return {
          ...v,
          image: mainImg,
          image_url: mainImg,
          images: imgs,
          features: feats,
          location: v.location || 'Sapanca Göl Kenarı, Sakarya / İrem Düğün Sarayı',
          costPrice: v.cost_price ? Number(v.cost_price) : 0,
          occupancyRate: v.occupancy_rate || 0,
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

if old_get_venues in server_code:
    server_code = server_code.replace(old_get_venues, new_get_venues)
elif "app.get('/api/venues'" in server_code:
    v_start = server_code.find("app.get('/api/venues'")
    v_end = server_code.find("app.post('/api/venues'", v_start)
    if v_start != -1 and v_end != -1:
        server_code = server_code[:v_start] + new_get_venues + "\n\n" + server_code[v_end:]

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(server_code)

print("Successfully updated server.js venues endpoint and defaults!")

# 2. UPDATE FRONTEND HTML FILES
html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # A. Update single venue card in CreateReservationPageComponent
    old_card_start = '// --- SINGLE VENUE FULL-WIDTH EXPANDED HERO CARD ---'
    old_card_end = '// --- MULTIPLE VENUES CAROUSEL WITH CONTROLS ---'

    s_idx = content.find(old_card_start)
    e_idx = content.find(old_card_end, s_idx)

    if s_idx != -1 and e_idx != -1:
        new_single_card = """// --- SINGLE VENUE FULL-WIDTH EXPANDED HERO CARD ---
                  (() => {
                    const v = venues[0];
                    const isSelected = venueId === v.id;
                    const venueImg = v.image || (v.images && v.images[0]) || (v.images_json && v.images_json[0]) || 'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=1200&q=80';
                    const venueFeatures = (v.features && v.features.length > 0) ? v.features : ['Geniş Dans Pisti', 'İklimlendirme', 'Özel Gelin Odası', 'Otopark & Vale'];

                    return (
                      <div
                        key={v.id}
                        onClick={() => {
                          setVenueId(v.id);
                          setCustomVenuePrice(v.price);
                        }}
                        className={`w-full rounded-3xl border-2 transition-all duration-300 cursor-pointer overflow-hidden shadow-sm flex flex-col md:flex-row ${
                          isSelected
                            ? 'border-slate-800 dark:border-white bg-slate-100/90 dark:bg-brand-dark shadow-md ring-2 ring-slate-800/40 dark:ring-white/40'
                            : 'border-slate-200 dark:border-brand-border bg-white dark:bg-brand-card hover:border-slate-400'
                        }`}
                      >
                        {/* Large Media Image on Left / Top */}
                        <div className="relative md:w-5/12 lg:w-4/12 h-52 sm:h-60 md:h-auto min-h-[200px] bg-slate-900 overflow-hidden shrink-0">
                          <img
                            src={venueImg}
                            alt={v.name}
                            loading="eager"
                            decoding="async"
                            className="w-full h-full object-cover transition-transform duration-500 hover:scale-105"
                          />
                          
                          {/* Capacity badge only (clean, no duplicate SEÇİLDİ on top-left) */}
                          <div className="absolute top-3 left-3 bg-slate-900/85 backdrop-blur-md text-white text-xs font-bold px-3 py-1 rounded-full border border-white/20 z-10 flex items-center space-x-1.5 shadow-md">
                            <ThemeIcon icon="users" className="w-3.5 h-3.5 text-white inline" />
                            <span>{v.capacity} Kişi Kapasite</span>
                          </div>

                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              setSelectedVenueForDetail(v);
                            }}
                            className="absolute bottom-3 right-3 bg-slate-900/90 hover:bg-slate-800 text-white text-xs font-bold px-3 py-1.5 rounded-xl border border-white/30 transition flex items-center space-x-1.5 shadow-md z-10 cursor-pointer"
                            title="Mekan Detaylarını Göster"
                          >
                            <ThemeIcon icon="search" className="w-3.5 h-3.5 text-white inline" />
                            <span>Mekan Detayları</span>
                          </button>
                        </div>

                        {/* Content Area on Right */}
                        <div className="p-5 sm:p-6 flex-1 flex flex-col justify-between space-y-4 bg-white dark:bg-brand-card">
                          <div className="space-y-2.5">
                            {/* Header row with Title on Left, and compact Seçildi badge on Right */}
                            <div className="flex items-center justify-between gap-2 border-b border-slate-100 dark:border-brand-border pb-2.5">
                              <div className="flex items-center space-x-2">
                                <h3 className="font-heading font-extrabold text-lg sm:text-xl text-slate-900 dark:text-white">
                                  {v.name}
                                </h3>
                                <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-300 border border-slate-200 dark:border-brand-border">
                                  {v.category || 'Ana Balo Salonu'}
                                </span>
                              </div>
                              
                              {/* Single compact Seçildi badge on top-right */}
                              {isSelected ? (
                                <span className="text-xs font-extrabold px-3 py-1 rounded-full bg-emerald-600 text-white shadow-xs inline-flex items-center space-x-1 shrink-0">
                                  <span>✓ Seçildi</span>
                                </span>
                              ) : (
                                <span className="text-xs font-bold px-3 py-1 rounded-full bg-slate-100 dark:bg-brand-dark text-slate-500 border border-slate-200 dark:border-brand-border shrink-0">
                                  Seç
                                </span>
                              )}
                            </div>
                            
                            <p className="text-xs sm:text-sm text-slate-600 dark:text-gray-300 leading-relaxed">
                              {v.description || 'Yüksek tavanlı, kristal avizeli, iklimlendirme sistemli ve lüks sahne düzenine sahip ana balo salonumuz.'}
                            </p>

                            {/* Feature tags dynamically loaded from database */}
                            <div className="flex flex-wrap gap-1.5 pt-1">
                              {venueFeatures.map((fText, fIdx) => (
                                <span key={fIdx} className="text-[11px] font-semibold px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 border border-slate-200 dark:border-brand-border">
                                  ✨ {fText}
                                </span>
                              ))}
                            </div>
                          </div>

                          <div className="pt-3 border-t border-slate-100 dark:border-brand-border flex justify-between items-center">
                            <div>
                              <span className="text-[11px] font-bold text-slate-500 dark:text-gray-400 block">Standart Liste Fiyatı:</span>
                              <span className="font-extrabold text-base sm:text-lg text-slate-900 dark:text-white font-mono">{formatCurrency(v.price)}</span>
                            </div>
                            <div className="text-xs font-bold text-slate-500 dark:text-gray-400">
                              <ThemeIcon icon="location" className="w-3.5 h-3.5 inline mr-1" />
                              <span>{v.location || 'Sapanca Göl Kenarı, Sakarya'}</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    );
                  })()
                ) : (
                  """
        content = content[:s_idx] + new_single_card + content[e_idx:]
        print(f"Updated single venue card in {h_file}")

    # B. Update VenueDetailModalComponent to ensure image, features, and full services from database are rendered
    modal_start = "function VenueDetailModalComponent({ venue, services = [], onClose, onSelectVenue }) {"
    if modal_start in content:
        # Update image fallback in modal
        img_fix_old = "src={venue.image}"
        img_fix_new = "src={venue.image || (venue.images && venue.images[0]) || 'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=1200&q=80'}"
        content = content.replace(img_fix_old, img_fix_new)

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully processed {h_file}!")

print("Venue details, images, and styling fix script completed successfully!")
