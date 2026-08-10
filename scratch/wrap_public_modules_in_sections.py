import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = "    // 4. MODULAR PAGE BLOCKS (INDEPENDENT FAULT ISOLATED PUBLIC SECTIONS)"
end_marker = "    function HallsPage({ navigateTo }) {"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

print(f"start_idx: {start_idx}, end_idx: {end_idx}")

if start_idx != -1 and end_idx != -1:
    sections_code = """    // 4. MODULAR PAGE BLOCKS (INDEPENDENT FAULT ISOLATED PUBLIC SECTIONS & STANDALONE HTML5 SECTIONS)
    function PublicHeroBlock({ onOpenLeadModal }) {
      return (
        <section id="section-hero" className="w-full relative min-h-screen">
          <div className="relative w-full h-screen min-h-[100vh] overflow-hidden flex items-center justify-center">
            <video
              autoPlay
              loop
              muted
              playsInline
              className="absolute inset-0 w-full h-full object-cover scale-105 pointer-events-none"
              src="https://cdn.creafolks.com/svadba-davet/9e9fee9d-dc11-4bd5-bc7a-4614de2d7e2b.mp4"
            />
            <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-black/40 to-black/70 backdrop-blur-[0.5px]" />

            <div className="relative z-10 text-center text-white px-4 max-w-4xl space-y-6 animate-fade-in">
              <div className="w-14 h-14 sm:w-16 sm:h-16 mx-auto rounded-full bg-white/10 backdrop-blur-md border border-white/30 flex items-center justify-center text-2xl text-amber-300 shadow-2xl animate-pulse">
                <ThemeIcon icon="crown" className="w-7 h-7 sm:w-8 sm:h-8 text-amber-300 shrink-0" />
              </div>

              <div className="space-y-3">
                <h1 className="text-3xl sm:text-6xl md:text-7xl font-serif font-extrabold tracking-widest uppercase text-white drop-shadow-[0_10px_35px_rgba(0,0,0,0.8)]">
                  İREM DÜĞÜN SARAYI
                </h1>
                <p className="text-base sm:text-2xl md:text-3xl font-serif italic text-amber-200/95 font-light tracking-wide drop-shadow-md">
                  Türkiye'nin & Sakarya'nın Düğün Mekanları
                </p>
              </div>

              <p className="text-xs sm:text-base text-slate-200/90 max-w-2xl mx-auto leading-relaxed font-medium drop-shadow-sm hidden sm:block">
                Sapanca Göl kıyısında 4 farklı saray konseptli balo salonumuz ve kır bahçemiz ile hayallerinizdeki düğünü taçlandırıyoruz.
              </p>

              <div className="pt-6 flex flex-wrap justify-center gap-4">
                <button 
                  onClick={onOpenLeadModal} 
                  className="bg-[#B89B5E] hover:bg-[#a3874e] text-white font-extrabold px-8 py-4 rounded-full text-xs shadow-2xl transition-all duration-300 hover:scale-105 flex items-center space-x-2.5 cursor-pointer uppercase tracking-wider"
                >
                  <span><ThemeIcon icon="crown" className="w-4 h-4 inline-block shrink-0" /></span>
                  <span>ÜCRETSİZ FİYAT TEKLİFİ ALIN</span>
                </button>
                <a 
                  href="https://wa.me/905471440054" 
                  target="_blank" 
                  rel="noreferrer" 
                  className="bg-white/20 hover:bg-white/30 text-white backdrop-blur-md border border-white/40 font-extrabold px-8 py-4 rounded-full text-xs shadow-xl transition-all duration-300 hover:scale-105 flex items-center space-x-2.5 uppercase tracking-wider"
                >
                  <span><ThemeIcon icon="chat" className="w-4 h-4 inline-block shrink-0 text-emerald-400" /></span>
                  <span>WHATSAPP İLETİŞİM</span>
                </a>
              </div>
            </div>

            <div 
              onClick={() => window.scrollTo({ top: window.innerHeight - 70, behavior: 'smooth' })}
              className="absolute bottom-8 sm:bottom-10 left-0 right-0 z-20 text-white/90 animate-bounce flex flex-col items-center justify-center text-center cursor-pointer group pointer-events-auto mx-auto w-full px-4"
            >
              <span className="text-[10px] sm:text-xs font-black tracking-[0.25em] uppercase mb-1 group-hover:text-amber-300 transition-colors text-center w-full block drop-shadow-md">AŞAĞI KAYDIRIN</span>
              <span className="text-2xl font-bold leading-none drop-shadow-md">↓</span>
            </div>
          </div>
        </section>
      );
    }

    function PublicWelcomeBlock({ navigateTo }) {
      return (
        <section id="section-welcome" className="w-full py-20 bg-white">
          <div className="max-w-7xl mx-auto px-4 grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div className="relative rounded-3xl overflow-hidden shadow-2xl border-4 border-amber-100">
              <img src="https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80" alt="İrem Düğün Sarayı" className="w-full h-[420px] object-cover" />
            </div>
            <div className="space-y-6">
              <span className="text-xs font-bold text-[#B89B5E] tracking-widest uppercase border-b-2 border-[#B89B5E] pb-1">İrem Düğün Sarayı Sakarya</span>
              <h2 className="text-3xl sm:text-4xl font-serif font-extrabold text-slate-900 leading-snug">İrem Düğün Sarayı’na Hoşgeldiniz...</h2>
              <p className="text-slate-600 text-sm leading-relaxed">
                İrem Düğün Sarayı, Sapanca Gölünün kıyısında konumlanan; şıklığı, konforu ve profesyonel hizmet anlayışını bir araya getiren seçkin bir davet ve organizasyon merkezidir. En özel anlarınızı unutulmaz kılmak için tasarlanan mekanımız, tamamı göl manzarasına sahip üç farklı salon seçeneği ile her davete eşsiz bir atmosfer sunar.
              </p>
              <p className="text-slate-600 text-sm leading-relaxed">
                Düğün, nişan, kına gecesi, sünnet, özel kutlamalar ve kurumsal davetler için farklı konsept alternatifleri sunan İrem Düğün Sarayı; otel konseptinden kır düğününe kadar uzanan geniş organizasyon yelpazesiyle hayallerinizi gerçeğe dönüştürür.
              </p>
              <div className="pt-2">
                <a href="/salonlar" onClick={(e) => { e.preventDefault(); if (navigateTo) navigateTo('/salonlar'); }} className="inline-block bg-[#B89B5E] hover:bg-[#a3874e] text-white font-bold px-8 py-3.5 rounded-full text-xs shadow-md transition">
                  Salonlarımızı İnceleyin →
                </a>
              </div>
            </div>
          </div>
        </section>
      );
    }

    function PublicServicesBlock() {
      const services = [
        { title: 'Düğün Salonu', desc: 'Hayalinizdeki düğün için şık, konforlu ve özenle tasarlanmış salonlarımızı keşfedebilirsiniz.' },
        { title: 'Nişan Organizasyonu', desc: 'Nişan organizasyonlarınız için zarif detaylarla hazırlanmış özel salonlarımızı inceleyebilirsiniz.' },
        { title: 'Sünnet Düğünü', desc: 'Sünnet düğünleri için ferah, modern ve ailelere uygun salon seçeneklerimizi keşfedebilirsiniz.' },
        { title: 'Kır Düğünü', desc: 'Doğayla iç içe, romantik ve unutulmaz kır düğünleri için özel alanlarımızı inceleyebilirsiniz.' },
        { title: 'Dönemsel Organizasyonlar', desc: 'Özel günler ve sezonluk organizasyonlar için profesyonelce hazırlanmış salonlarımızı keşfedebilirsiniz.' },
        { title: 'Mezuniyet Kutlaması', desc: 'Mezuniyet gecelerinizi unutulmaz kılacak geniş ve özenle hazırlanmış salonlarımızı inceleyebilirsiniz.' },
        { title: 'Kurumsal Organizasyon', desc: 'Toplantı, davet ve kurumsal etkinlikler için prestijli ve fonksiyonel salonlarımızı inceleyebilirsiniz.' },
      ];

      return (
        <section id="section-services" className="w-full bg-[#faf8f5] py-20 px-4 border-y border-amber-200/50">
          <div className="max-w-7xl mx-auto space-y-12">
            <div className="text-center space-y-3">
              <span className="text-xs font-bold text-[#B89B5E] tracking-widest uppercase">Ayrıcalıklı Konseptler</span>
              <h2 className="text-3xl font-serif font-extrabold text-slate-900">Organizasyon Hizmetlerimiz</h2>
              <p className="text-xs text-slate-500 max-w-xl mx-auto">Her davet türüne özel olarak dizayn edilmiş lüks salon ve organizasyon seçenekleri.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {services.map((item, idx) => (
                <div key={idx} className="bg-white p-8 rounded-3xl border border-amber-100 shadow-sm hover:shadow-xl transition-all duration-300 text-center space-y-4 hover:-translate-y-1">
                  <div className="w-14 h-14 mx-auto rounded-full bg-[#faf8f5] border border-amber-200 flex items-center justify-center text-[#B89B5E] text-2xl shadow-inner"><ThemeIcon icon="crown" className="w-4 h-4 inline-block shrink-0" /></div>
                  <h3 className="font-serif font-bold text-xl text-slate-900">{item.title}</h3>
                  <p className="text-xs text-slate-600 leading-relaxed">{item.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>
      );
    }

    function PublicHallsBlock({ navigateTo, onOpenLeadModal }) {
      const halls = [
        { name: 'Saray Balo', cap: '750 Kişi', desc: 'Geniş salonu ve göz alıcı dekorasyonuyla Saray Balo, lüks ve estetiği bir arada sunar. Özel günlerinizi prestijli ve şık bir atmosferde gerçekleştirmenizi sağlar.', img: 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=600&q=80' },
        { name: 'Safir Salon', cap: '500 Kişi', desc: 'Modern mimarisi ve şık tasarımıyla Safir Salon, zarif davetler için özel olarak hazırlanmıştır. Konforlu yapısı ve manzarasıyla kusursuz bir düğün deneyimi sunar.', img: 'https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=600&q=80' },
        { name: 'Kır Bahçesi', cap: '1000+ Kişi', desc: 'Göl manzarası ve ferah alanlarıyla Kır Bahçesi, açık hava konseptini şıklıkla buluşturur. Doğayla iç içe, keyifli ve unutulmaz davetler için ideal bir mekândır.', img: 'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&w=600&q=80' },
      ];

      return (
        <section id="section-halls" className="w-full py-20 bg-white">
          <div className="max-w-7xl mx-auto px-4 space-y-12">
            <div className="text-center space-y-3">
              <span className="text-xs font-bold text-[#B89B5E] tracking-widest uppercase">İrem Düğün Sarayı</span>
              <h2 className="text-3xl sm:text-5xl font-serif font-extrabold text-slate-900">Sakarya Düğün Salonları</h2>
              <p className="text-xs text-slate-500 max-w-xl mx-auto">Sapanca Gölünün kıyısında kolonsuz yüksek tavan ferahlığıyla tasarlanmış balo salonlarımız.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {halls.map((hall, idx) => (
                <div key={idx} className="bg-white rounded-3xl overflow-hidden border border-amber-100 shadow-md hover:shadow-2xl transition duration-300 space-y-5 p-6 flex flex-col justify-between">
                  <div className="space-y-4">
                    <div className="relative h-60 rounded-2xl overflow-hidden shadow-sm">
                      <img src={hall.img} alt={hall.name} className="w-full h-full object-cover" />
                      <div className="absolute top-3 right-3 bg-white/95 backdrop-blur-md text-[#B89B5E] font-bold text-xs px-3.5 py-1.5 rounded-full shadow border border-amber-200">
                        <ThemeIcon icon="users" className="w-4 h-4 inline-block shrink-0" /> {hall.cap}
                      </div>
                    </div>
                    <h3 className="font-serif font-bold text-2xl text-slate-900">{hall.name}</h3>
                    <p className="text-xs text-slate-600 leading-relaxed">{hall.desc}</p>
                  </div>

                  <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
                    <a href="/360-tur" onClick={(e) => { e.preventDefault(); if (navigateTo) navigateTo('/360-tur'); }} className="text-xs font-bold text-[#B89B5E] hover:underline flex items-center space-x-1">
                      <span><ThemeIcon icon="location" className="w-4 h-4 inline-block shrink-0" /></span><span>360° İnceleyin</span>
                    </a>
                    <button onClick={onOpenLeadModal} className="bg-[#B89B5E] hover:bg-[#a3874e] text-white px-5 py-2.5 rounded-full text-xs font-bold shadow transition cursor-pointer">
                      Teklif Alın
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      );
    }

    function PublicMenusBlock() {
      return (
        <section id="section-menus" className="w-full bg-[#faf8f5] py-20 px-4 border-y border-amber-200/50">
          <div className="max-w-7xl mx-auto space-y-10">
            <div className="text-center space-y-2">
              <span className="text-xs font-bold text-[#B89B5E] tracking-widest uppercase">Zengin Davet İkramları</span>
              <h2 className="text-3xl font-serif font-extrabold text-slate-900">Menülerimiz & VIP Lezzetler</h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="bg-white p-6 rounded-3xl border border-amber-100 shadow-sm space-y-3">
                <div className="text-[#B89B5E] font-bold text-sm flex items-center space-x-2">
                  <span><ThemeIcon icon="gift" className="w-4 h-4 inline-block shrink-0" /></span><span>Ordövr Tabağı</span>
                </div>
                <p className="text-xs text-slate-600 leading-relaxed">Zengin Türk ordövr tabağı, dana füme et şöleni, ezme, humus ve gurme peynir çeşitleri.</p>
              </div>
              <div className="bg-white p-6 rounded-3xl border border-amber-100 shadow-sm space-y-3">
                <div className="text-[#B89B5E] font-bold text-sm flex items-center space-x-2">
                  <span><ThemeIcon icon="gift" className="w-4 h-4 inline-block shrink-0" /></span><span>Ara Sıcaklar</span>
                </div>
                <p className="text-xs text-slate-600 leading-relaxed">Sıcak Paçanga böreği, fıstıklı içli köfte ve sebzeli krep ikramları.</p>
              </div>
              <div className="bg-white p-6 rounded-3xl border border-amber-100 shadow-sm space-y-3">
                <div className="text-[#B89B5E] font-bold text-sm flex items-center space-x-2">
                  <span><ThemeIcon icon="gift" className="w-4 h-4 inline-block shrink-0" /></span><span>Ana Yemek</span>
                </div>
                <p className="text-xs text-slate-600 leading-relaxed">Ağır ateşte pişmiş Kuzu Tandır veya Özel Soslu Dana Antrikot, iç pilav ile.</p>
              </div>
              <div className="bg-white p-6 rounded-3xl border border-amber-100 shadow-sm space-y-3">
                <div className="text-[#B89B5E] font-bold text-sm flex items-center space-x-2">
                  <span><ThemeIcon icon="gift" className="w-4 h-4 inline-block shrink-0" /></span><span>Düğün Pastası</span>
                </div>
                <p className="text-xs text-slate-600 leading-relaxed">5 Katlı şov düğün pastası, mevsim meyveleri tabağı ve meşrubat servisi.</p>
              </div>
            </div>
          </div>
        </section>
      );
    }

    function PublicTestimonialsBlock() {
      return (
        <section id="section-testimonials" className="w-full py-20 px-4 bg-white">
          <div className="max-w-7xl mx-auto space-y-10">
            <div className="text-center space-y-2">
              <div className="text-amber-500 text-sm font-bold"><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /> (643 Doğrulanmış Değerlendirme)</div>
              <h2 className="text-3xl font-serif font-extrabold text-slate-900">Müşteri Yorumları</h2>
              <p className="text-xs text-slate-500">Google ve Düğün.com üzerinden gelen gerçek çift deneyimleri.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="bg-white border border-amber-100 p-8 rounded-3xl space-y-4 shadow-sm hover:shadow-md transition">
                <div className="flex items-center space-x-1 text-amber-500 text-sm"><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /></div>
                <p className="text-xs text-slate-600 leading-relaxed font-serif italic">"Sapanca göl kenarındaki Saray Balo salonunda 600 kişilik düğünümüz gerçekleşti. Yemek kalitesi ve garson ilgisi harikaydı!"</p>
                <div className="flex items-center justify-between pt-3 border-t border-slate-100 text-[11px]">
                  <span className="font-bold text-slate-900">Ahmet & Zeynep Y.</span>
                  <span className="text-emerald-600 font-bold">Google Doğrulanmış</span>
                </div>
              </div>

              <div className="bg-white border border-amber-100 p-8 rounded-3xl space-y-4 shadow-sm hover:shadow-md transition">
                <div className="flex items-center space-x-1 text-amber-500 text-sm"><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /></div>
                <p className="text-xs text-slate-600 leading-relaxed font-serif italic">"Kır bahçesindeki nişan organizasyonumuz masal gibiydi. Işıklandırma ve ses sistemleri son teknolojiydi. Emeği geçen herkese teşekkürler."</p>
                <div className="flex items-center justify-between pt-3 border-t border-slate-100 text-[11px]">
                  <span className="font-bold text-slate-900">Burak & Selin K.</span>
                  <span className="text-emerald-600 font-bold">Düğün.com Doğrulanmış</span>
                </div>
              </div>

              <div className="bg-white border border-amber-100 p-8 rounded-3xl space-y-4 shadow-sm hover:shadow-md transition">
                <div className="flex items-center space-x-1 text-amber-500 text-sm"><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /><ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" /></div>
                <p className="text-xs text-slate-600 leading-relaxed font-serif italic">"Safir Salon'da yapılan sünnet organizasyonumuzda organizasyon koordinatörünün planlaması sayesinde sıfır aksamayla harika bir gece geçirdik."</p>
                <div className="flex items-center justify-between pt-3 border-t border-slate-100 text-[11px]">
                  <span className="font-bold text-slate-900">Murat & Elif D.</span>
                  <span className="text-emerald-600 font-bold">Google Doğrulanmış</span>
                </div>
              </div>
            </div>
          </div>
        </section>
      );
    }

    // 5. MAIN HOMEPAGE ASSEMBLY WITH ISOLATED INDEPENDENT SECTIONS
    function HomePage({ navigateTo }) {
      const [isLeadModalOpen, setIsLeadModalOpen] = useState(false);

      return (
        <div className="w-full bg-white flex flex-col">
          <BlockErrorBoundary blockName="Video Hero Header">
            <PublicHeroBlock onOpenLeadModal={() => setIsLeadModalOpen(true)} />
          </BlockErrorBoundary>

          <BlockErrorBoundary blockName="Hoşgeldiniz Alanı">
            <PublicWelcomeBlock navigateTo={navigateTo} />
          </BlockErrorBoundary>

          <BlockErrorBoundary blockName="Organizasyon Hizmetleri">
            <PublicServicesBlock />
          </BlockErrorBoundary>

          <BlockErrorBoundary blockName="Salonlarımız">
            <PublicHallsBlock navigateTo={navigateTo} onOpenLeadModal={() => setIsLeadModalOpen(true)} />
          </BlockErrorBoundary>

          <BlockErrorBoundary blockName="Catering & VIP Menüler">
            <PublicMenusBlock />
          </BlockErrorBoundary>

          <BlockErrorBoundary blockName="Müşteri Yorumları">
            <PublicTestimonialsBlock />
          </BlockErrorBoundary>

          <LeadModal isOpen={isLeadModalOpen} onClose={() => setIsLeadModalOpen(false)} />
        </div>
      );
    }

"""
    content = content[:start_idx] + sections_code + content[end_idx:]
    print("Successfully wrapped all public module blocks into independent HTML5 section containers!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
