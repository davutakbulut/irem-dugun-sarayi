import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update VenueModalComponent call in App component to pass allServices={services}
old_venue_modal = """          {venueModalData && (
            <VenueModalComponent
              venue={venueModalData === 'new' ? null : venueModalData}
              onClose={() => setVenueModalData(null)}
              onSave={handleSaveVenue}
            />
          )}"""

new_venue_modal = """          {venueModalData && (
            <VenueModalComponent
              venue={venueModalData === 'new' ? null : venueModalData}
              allServices={services}
              onClose={() => setVenueModalData(null)}
              onSave={handleSaveVenue}
            />
          )}"""

if old_venue_modal in content:
    content = content.replace(old_venue_modal, new_venue_modal)
    print("1. Passed allServices={services} prop to VenueModalComponent in App component.")
else:
    print("WARNING: Could not find old_venue_modal in index.html!")

# 2. Update defaultServicesList in VenueModalComponent to dynamically sort and list all database services
old_service_list_code = """      const defaultServicesList = allServices.length > 0 ? allServices : [
        { id: 's1', name: 'Gurme Yemek Servisi (Et Menü)' },
        { id: 's2', name: 'Fotoğraf & 4K Video Paketi' },
        { id: 's3', name: 'Canlı Müzik Orkestrası & DJ' },
        { id: 's4', name: 'Masa & Sahne Süsleme' },
        { id: 's5', name: 'Volkan, Konfeti & Işık Şovu' }
      ];"""

new_service_list_code = """      const defaultServicesList = [...(allServices || [])].sort((a, b) => {
        const oA = typeof a.order === 'number' ? a.order : (typeof a.sortOrder === 'number' ? a.sortOrder : 9999);
        const oB = typeof b.order === 'number' ? b.order : (typeof b.sortOrder === 'number' ? b.sortOrder : 9999);
        return oA - oB;
      });"""

if old_service_list_code in content:
    content = content.replace(old_service_list_code, new_service_list_code)
    print("2. Updated VenueModalComponent to pull 100% of extra services dynamically from database.")
else:
    print("WARNING: Could not find old_service_list_code in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
