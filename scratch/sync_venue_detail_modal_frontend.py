import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

old_detail_images = """      const interiorImages = venue.images && venue.images.length > 0 ? venue.images : [
        (venue.image ? venue.image.replace('w=800', 'w=450&q=65') : 'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=450&q=65'),
        'https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=450&q=65',
        'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=450&q=65'
      ];

      const exteriorImages = [
        'https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?auto=format&fit=crop&w=450&q=65',
        'https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&w=450&q=65',
        'https://images.unsplash.com/photo-1527529482837-4698179dc6ce?auto=format&fit=crop&w=450&q=65'
      ];

      // DYNAMIC EVENT TYPES FROM VENUE RECORD
      const dynamicEventTypes = (venue.eventTypes && venue.eventTypes.length > 0)
        ? venue.eventTypes
        : ['Düğün', 'Nişan', 'Kurumsal Kokteyl'];

      // DYNAMIC AVAILABLE SERVICES MATCHING THIS VENUE'S UNIQUE SERVICE IDS
      const defaultServicesList = (typeof INITIAL_SERVICES !== 'undefined' ? INITIAL_SERVICES : []);
      const allServices = (services && services.length > 0) ? services : defaultServicesList;
      
      const venueServiceIds = venue.availableServices || [];
      const dynamicVenueServices = venueServiceIds.length > 0
        ? allServices.filter(s => venueServiceIds.includes(s.id))
        : allServices.slice(0, 4);"""

new_detail_images = """      const interiorImages = (venue.interiorImages && venue.interiorImages.length > 0)
        ? venue.interiorImages
        : (venue.images && venue.images.length > 0 ? venue.images : [
            (venue.image ? venue.image.replace('w=800', 'w=450&q=65') : 'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=450&q=65'),
            'https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=450&q=65',
            'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=450&q=65'
          ]);

      const exteriorImages = (venue.exteriorImages && venue.exteriorImages.length > 0)
        ? venue.exteriorImages
        : [
            'https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?auto=format&fit=crop&w=450&q=65',
            'https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&w=450&q=65',
            'https://images.unsplash.com/photo-1527529482837-4698179dc6ce?auto=format&fit=crop&w=450&q=65'
          ];

      // DYNAMIC EVENT TYPES FROM VENUE RECORD
      const dynamicEventTypes = (venue.eventTypes && venue.eventTypes.length > 0)
        ? venue.eventTypes
        : ['Düğün', 'Nişan', 'Kına', 'Kurumsal Etkinlik', 'Gala', 'Sünnet Düğünü'];

      // DYNAMIC AVAILABLE SERVICES MATCHING THIS VENUE'S UNIQUE SERVICE IDS
      const defaultServicesList = (typeof INITIAL_SERVICES !== 'undefined' ? INITIAL_SERVICES : []);
      const allServices = (services && services.length > 0) ? services : defaultServicesList;
      
      const venueServiceIds = venue.availableServices || [];
      const dynamicVenueServices = venueServiceIds.length > 0
        ? allServices.filter(s => venueServiceIds.includes(s.id))
        : allServices;"""

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_detail_images in content:
        content = content.replace(old_detail_images, new_detail_images)
        with open(h_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated VenueDetailModalComponent in {h_file}")
    else:
        print(f"old_detail_images not found in {h_file}")

print("All HTML files updated!")
