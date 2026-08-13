import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

old_section_start = '{/* VISUAL HORIZONTAL SCROLLABLE VENUE CAROUSEL WITH ARROW CONTROLS */}'
old_section_end = '<div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs pt-1">'

new_section = """{/* VISUAL VENUE SELECTION: EXPANDED SINGLE HERO CARD IF 1 VENUE, CAROUSEL/GRID IF MULTIPLE */}
                {venues.length === 0 ? (
                  <div className="p-6 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-800 dark:text-gold-400 text-xs font-bold text-center space-y-2.5 w-full">
                    <div><ThemeIcon icon="warning" className="w-4 h-4 inline-block text-amber-500 shrink-0" /> Sistemde henüz tanımlı bir etkinlik mekanı bulunmamaktadır.</div>
                    <button
                      type="button"
                      onClick={() => navigateTo && navigateTo('dugun-salonlari')}
                      className="gold-button px-4 py-2 rounded-xl font-extrabold shadow hover:scale-105 transition cursor-pointer inline-flex items-center space-x-2"
                    >
                      <span><ThemeIcon icon="venue" className="w-4 h-4 inline-block shrink-0" /> Yeni Düğün Salonu Ekle</span>
                    </button>
                  </div>
                ) : venues.length === 1 ? (
                  // --- SINGLE VENUE FULL-WIDTH EXPANDED HERO CARD ---
                  (() => {
                    const v = venues[0];
                    const isSelected = venueId === v.id;
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
                        <div className="relative md:w-5/12 lg:w-4/12 h-48 sm:h-56 md:h-auto min-h-[180px] bg-slate-200 dark:bg-brand-dark overflow-hidden shrink-0">
                          <OptimizedImage src={v.image} alt={v.name} className="w-full h-full object-cover" priority={true} />
                          
                          <div className="absolute top-3 right-3 bg-slate-900/85 backdrop-blur-md text-white text-xs font-bold px-3 py-1 rounded-full border border-white/20 z-10 flex items-center space-x-1.5 shadow-md">
                            <ThemeIcon icon="users" className="w-3.5 h-3.5 text-white inline" />
                            <span>{v.capacity} Kişi Kapasite</span>
                          </div>
                          
                          {isSelected && (
                            <div className="absolute top-3 left-3 gold-button text-xs font-extrabold px-3 py-1 rounded-full shadow-lg z-10 flex items-center space-x-1">
                              <span>✓ SEÇİLDİ</span>
                            </div>
                          )}

                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              setSelectedVenueForDetail(v);
                            }}
                            className="absolute bottom-3 right-3 bg-slate-900/90 hover:bg-slate-800 text-white text-xs font-bold px-3 py-1.5 rounded-xl border border-white/30 transition flex items-center space-x-1.5 shadow-md z-10"
                            title="Mekan Detaylarını Göster"
                          >
                            <ThemeIcon icon="search" className="w-3.5 h-3.5 text-white inline" />
                            <span>Mekan Detayları</span>
                          </button>
                        </div>

                        {/* Content Area on Right */}
                        <div className="p-5 sm:p-6 flex-1 flex flex-col justify-between space-y-4 bg-white dark:bg-brand-card">
                          <div className="space-y-2.5">
                            <div className="flex flex-wrap items-center justify-between gap-2">
                              <h3 className="font-heading font-extrabold text-lg sm:text-xl text-slate-900 dark:text-white flex items-center space-x-2">
                                <span>{v.name}</span>
                              </h3>
                              <span className="text-xs font-bold px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30">
                                Ana Balo Salonu
                              </span>
                            </div>
                            
                            <p className="text-xs sm:text-sm text-slate-600 dark:text-gray-300 leading-relaxed">
                              {v.description || 'Yüksek tavanlı, kristal avizeli, iklimlendirme sistemli ve geniş dans pistine sahip ana salon.'}
                            </p>

                            {/* Feature tags */}
                            <div className="flex flex-wrap gap-1.5 pt-1">
                              <span className="text-[11px] font-semibold px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 border border-slate-200 dark:border-brand-border">
                                ✨ Geniş Dans Pisti
                              </span>
                              <span className="text-[11px] font-semibold px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 border border-slate-200 dark:border-brand-border">
                                ❄️ İklimlendirme
                              </span>
                              <span className="text-[11px] font-semibold px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 border border-slate-200 dark:border-brand-border">
                                👰 Özel Gelin Odası
                              </span>
                              <span className="text-[11px] font-semibold px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 border border-slate-200 dark:border-brand-border">
                                🚗 Otopark & Vale
                              </span>
                            </div>
                          </div>

                          <div className="pt-3 border-t border-slate-100 dark:border-brand-border flex flex-wrap justify-between items-center gap-2">
                            <div>
                              <span className="text-[11px] font-bold text-slate-500 dark:text-gray-400 block">Standart Liste Fiyatı:</span>
                              <span className="font-extrabold text-base sm:text-lg text-slate-900 dark:text-white font-mono">{formatCurrency(v.price)}</span>
                            </div>
                            <div className="text-right">
                              <span className="text-xs font-extrabold text-emerald-600 dark:text-emerald-400 flex items-center space-x-1">
                                <span>✓ Rezervasyon için Seçildi</span>
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                    );
                  })()
                ) : (
                  // --- MULTIPLE VENUES CAROUSEL WITH CONTROLS ---
                  <div className="space-y-2">
                    <div className="flex justify-between items-center pb-1">
                      <span className="text-xs font-bold text-slate-500">Mevcut Salonlar ({venues.length} Adet):</span>
                      <div className="flex items-center space-x-1.5">
                        <button
                          type="button"
                          onClick={scrollVenueCarouselLeft}
                          className="w-7 h-7 rounded-full border border-amber-500/40 bg-white dark:bg-brand-card text-amber-800 dark:text-gold-400 hover:bg-amber-500 hover:text-white font-bold text-xs shadow flex items-center justify-center transition active:scale-95 cursor-pointer"
                          title="Sola Kaydır"
                          aria-label="Etkinlik Mekanlarını Sola Kaydır"
                        >
                          ❮
                        </button>
                        <button
                          type="button"
                          onClick={scrollVenueCarouselRight}
                          className="w-7 h-7 rounded-full border border-amber-500/40 bg-white dark:bg-brand-card text-amber-800 dark:text-gold-400 hover:bg-amber-500 hover:text-white font-bold text-xs shadow flex items-center justify-center transition active:scale-95 cursor-pointer"
                          title="Sağa Kaydır"
                          aria-label="Etkinlik Mekanlarını Sağa Kaydır"
                        >
                          ❯
                        </button>
                      </div>
                    </div>

                    <div ref={venueCarouselRef} className="flex overflow-x-auto gap-3.5 pb-3 pt-1 no-scrollbar snap-x snap-mandatory scroll-smooth px-1">
                      {venues.map(v => {
                        const isSelected = venueId === v.id;
                        return (
                          <div
                            key={v.id}
                            onClick={() => {
                              setVenueId(v.id);
                              setCustomVenuePrice(v.price);
                            }}
                            className={`shrink-0 w-64 sm:w-68 rounded-2xl border-2 transition-all duration-300 cursor-pointer overflow-hidden snap-start flex flex-col justify-between shadow-sm ${
                              isSelected
                                ? 'border-slate-800 dark:border-white bg-slate-100/80 dark:bg-brand-dark shadow-md ring-2 ring-slate-800/40 dark:ring-white/40'
                                : 'border-slate-200 dark:border-brand-border bg-white dark:bg-brand-card hover:border-slate-400'
                            }`}
                          >
                            <div className="relative h-32 sm:h-36 w-full bg-slate-200 dark:bg-brand-dark overflow-hidden shrink-0">
                              <OptimizedImage src={v.image} alt={v.name} className="w-full h-full object-cover" priority={isSelected} />
                              
                              <div className="absolute top-2 right-2 bg-slate-900/80 backdrop-blur-md text-white text-[10px] font-bold px-2 py-0.5 rounded-full border border-white/20 z-10 flex items-center space-x-1">
                                <ThemeIcon icon="users" className="w-3 h-3 text-white inline" />
                                <span>{v.capacity} Kişi</span>
                              </div>
                              
                              {isSelected && (
                                <div className="absolute top-2 left-2 gold-button text-[11px] font-extrabold px-2.5 py-0.5 rounded-full shadow z-10">
                                  SEÇİLDİ ✓
                                </div>
                              )}

                              <button
                                type="button"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  setSelectedVenueForDetail(v);
                                }}
                                className="absolute bottom-2 right-2 bg-slate-900/90 hover:bg-slate-800 text-white text-[10px] font-bold px-2.5 py-1 rounded-lg border border-white/30 transition flex items-center space-x-1 shadow z-10"
                                title="Mekan Detaylarını Göster"
                              >
                                <ThemeIcon icon="search" className="w-3.5 h-3.5 text-white inline" />
                                <span>Mekan Detayları</span>
                              </button>
                            </div>

                            <div className="p-3 space-y-1.5 flex-1 flex flex-col justify-between bg-white dark:bg-brand-card">
                              <div>
                                <h4 className="font-heading font-extrabold text-xs sm:text-sm text-slate-800 dark:text-gray-100 leading-tight">
                                  {v.name}
                                </h4>
                                <p className="text-[10px] text-slate-500 dark:text-gray-400 line-clamp-1 mt-1">{v.description}</p>
                              </div>

                              <div className="pt-2 border-t border-slate-100 dark:border-brand-border flex justify-between items-center text-xs">
                                <span className="text-[10px] font-bold text-slate-500">Liste Fiyatı:</span>
                                <span className="font-extrabold text-xs text-slate-800 dark:text-gray-200">{formatCurrency(v.price)}</span>
                              </div>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}

                """

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    s_pos = content.find(old_section_start)
    e_pos = content.find(old_section_end, s_pos)

    if s_pos != -1 and e_pos != -1:
        content = content[:s_pos] + new_section + content[e_pos:]
        with open(h_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully updated venue selection layout in {h_file}!")
    else:
        print(f"Markers not found in {h_file}")

print("Venue selection layout update complete!")
