import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update VirtualTourPage definition to accept venues prop and use live venues
old_vtour = """    function VirtualTourPage({ navigateTo }) {
      const [activeVenueId, setActiveVenueId] = useState(INITIAL_VENUES[0]?.id || 'v1');
      const [activeHotspot, setActiveHotspot] = useState(null);
      const activeVenue = INITIAL_VENUES.find(v => v.id === activeVenueId) || INITIAL_VENUES[0];

      return (
        <div className="max-w-7xl mx-auto px-4 py-16 text-white space-y-10">
          <div className="text-center space-y-4 max-w-3xl mx-auto">
            <span className="text-xs font-mono font-bold text-[#e2c07d] bg-[#c5a059]/10 px-4 py-1.5 rounded-full border border-[#c5a059]/30 uppercase tracking-widest"><ThemeIcon icon="location" className="w-4 h-4 inline-block shrink-0" /> 3D 360° Canlı Tur</span>
            <h2 className="text-3xl sm:text-5xl font-serif font-extrabold text-white">İnteraktif 360° Balo Salonu Sanal Turu</h2>
            <p className="text-xs sm:text-sm text-slate-300">Tesisimizdeki salonları ve kır bahçemizi 3D panoramik detaylar ve mimari sıcak noktalar (hotspots) ile evinizden inceleyin.</p>
          </div>

          <div className="flex flex-wrap items-center justify-center gap-3 bg-slate-900/80 p-2 rounded-2xl border border-[#c5a059]/30 max-w-4xl mx-auto">
            {INITIAL_VENUES.map(v => ("""

new_vtour = """    function VirtualTourPage({ venues = [], navigateTo }) {
      const liveVenues = (venues && venues.length > 0) ? venues : INITIAL_VENUES;
      const [activeVenueId, setActiveVenueId] = useState(liveVenues[0]?.id || 'v1');
      const [activeHotspot, setActiveHotspot] = useState(null);
      const activeVenue = liveVenues.find(v => v.id === activeVenueId) || liveVenues[0];

      return (
        <div className="max-w-7xl mx-auto px-4 py-16 text-white space-y-10">
          <div className="text-center space-y-4 max-w-3xl mx-auto">
            <span className="text-xs font-mono font-bold text-[#e2c07d] bg-[#c5a059]/10 px-4 py-1.5 rounded-full border border-[#c5a059]/30 uppercase tracking-widest"><ThemeIcon icon="location" className="w-4 h-4 inline-block shrink-0" /> 3D 360° Canlı Tur</span>
            <h2 className="text-3xl sm:text-5xl font-serif font-extrabold text-white">İnteraktif 360° Balo Salonu Sanal Turu</h2>
            <p className="text-xs sm:text-sm text-slate-300">Tesisimizdeki salonları ve kır bahçemizi 3D panoramik detaylar ve mimari sıcak noktalar (hotspots) ile evinizden inceleyin.</p>
          </div>

          <div className="flex flex-wrap items-center justify-center gap-3 bg-slate-900/80 p-2 rounded-2xl border border-[#c5a059]/30 max-w-4xl mx-auto">
            {liveVenues.map(v => ("""

if old_vtour in content:
    content = content.replace(old_vtour, new_vtour)
    print("1. Updated VirtualTourPage to use live database venues.")

# 2. Update VirtualTourPage call site in App component
old_vtour_call = "{currentPublicTab === 'public-virtual-tour' && <VirtualTourPage navigateTo={navigateTo} />}"
new_vtour_call = "{currentPublicTab === 'public-virtual-tour' && <VirtualTourPage venues={venues} navigateTo={navigateTo} />}"

if old_vtour_call in content:
    content = content.replace(old_vtour_call, new_vtour_call)
    print("2. Updated VirtualTourPage call site to pass venues={venues}.")

# 3. Clean remaining 'Demo' strings in UI
content = content.replace('Hızlı Canlı Rol Seçimi & Demo Girişleri:', 'Hızlı Canlı Rol Seçimi & Oturum Seçenekleri:')
content = content.replace('handleDemoLogin', 'handleQuickRoleLogin')
content = content.replace('Demo Giriş', 'Canlı Giriş')

print("3. Cleaned remaining 'Demo' UI terminology across index.html.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
