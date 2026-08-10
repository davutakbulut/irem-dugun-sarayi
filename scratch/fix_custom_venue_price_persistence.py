import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the harmful useEffect([venueId]) that overwrote customVenuePrice
old_venue_id_effect = """      // Update customVenuePrice when venueId changes
      useEffect(() => {
        const v = venues.find(x => x.id === venueId);
        if (v) setCustomVenuePrice(v.price);
      }, [venueId]);"""

if old_venue_id_effect in content:
    content = content.replace(old_venue_id_effect, "// Update customVenuePrice when venueId changes (Handled explicitly on user venue click, not passive useEffect)")
    print("1. Removed passive useEffect([venueId]) that reset customVenuePrice!")
else:
    print("WARNING: Could not find old_venue_id_effect in index.html!")

# 2. Fix editingResFromUrl initialization of customVenuePrice
old_init = """setCustomVenuePrice(editingResFromUrl.venuePrice || editingResFromUrl.customVenuePrice || venues[0]?.price || 0);"""
new_init = """setCustomVenuePrice(editingResFromUrl.venuePrice !== undefined ? editingResFromUrl.venuePrice : (editingResFromUrl.customVenuePrice !== undefined ? editingResFromUrl.customVenuePrice : (venues.find(v => v.id === editingResFromUrl.venueId)?.price || 0)));"""

if old_init in content:
    content = content.replace(old_init, new_init)
    print("2. Fixed editingResFromUrl customVenuePrice initialization.")

# 3. Add customVenuePrice to newRes in handleSubmit
old_new_res = """          venuePrice: calculations.vPrice,
          subtotal: calculations.sub,"""

new_new_res = """          venuePrice: calculations.vPrice,
          customVenuePrice: calculations.vPrice,
          customDiscountAmount: customDiscountAmount,
          dipDiscountType: dipDiscountType,
          subtotal: calculations.sub,"""

if old_new_res in content:
    content = content.replace(old_new_res, new_new_res)
    print("3. Added customVenuePrice, customDiscountAmount, dipDiscountType to newRes object in handleSubmit.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
