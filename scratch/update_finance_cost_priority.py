import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

old_calc_chunk = """          const vObj = (venues || []).find(v => v.id === r.venueId);
          const venueCost = r.venueCost !== undefined ? Number(r.venueCost) : Number(vObj?.costPrice || Math.round((r.venuePrice || 60000) * 0.55));

          const servicesCost = (r.selectedServices || []).reduce((sum, s) => {
            const sObj = (services || []).find(srv => srv.id === s.serviceId);
            const uCost = s.costPrice !== undefined ? Number(s.costPrice) : (sObj?.costPrice !== undefined ? Number(sObj.costPrice) : Math.round(Number(s.unitPrice || 250) * 0.6));
            return sum + (uCost * Number(s.quantity || 1));
          }, 0);"""

new_calc_chunk = """          const vObj = (venues || []).find(v => v.id === r.venueId);
          // 1. ÖNCELİK: Mekan Kartına Tanımlı Gerçek Maliyet Bedeli
          const venueCost = (vObj && vObj.costPrice !== undefined && Number(vObj.costPrice) > 0)
            ? Number(vObj.costPrice)
            : (r.venueCost !== undefined && Number(r.venueCost) > 0
                ? Number(r.venueCost)
                : Math.round(Number(r.venuePrice || r.customVenuePrice || 60000) * 0.55));

          // 1. ÖNCELİK: Ek Hizmet Kartına Tanımlı Gerçek Birim Maliyeti
          const servicesCost = (r.selectedServices || []).reduce((sum, s) => {
            const sObj = (services || []).find(srv => srv.id === s.serviceId);
            const uCost = (sObj && sObj.costPrice !== undefined && Number(sObj.costPrice) > 0)
              ? Number(sObj.costPrice)
              : (s.costPrice !== undefined && Number(s.costPrice) > 0
                  ? Number(s.costPrice)
                  : Math.round(Number(s.unitPrice || s.price || 250) * 0.6));
            return sum + (uCost * Number(s.quantity || 1));
          }, 0);"""

old_expanded_chunk = """                                                const sObj = (services || []).find(srv => srv.id === s.serviceId);
                                                const sName = s.name || sObj?.name || `Hizmet (${s.serviceId})`;
                                                const sQty = Number(s.quantity || 1);
                                                const sCost = s.costPrice !== undefined ? Number(s.costPrice) : (sObj?.costPrice !== undefined ? Number(sObj.costPrice) : Math.round(Number(s.unitPrice || 250) * 0.6));"""

new_expanded_chunk = """                                                const sObj = (services || []).find(srv => srv.id === s.serviceId);
                                                const sName = s.name || sObj?.name || `Hizmet (${s.serviceId})`;
                                                const sQty = Number(s.quantity || 1);
                                                const sCost = (sObj && sObj.costPrice !== undefined && Number(sObj.costPrice) > 0)
                                                  ? Number(sObj.costPrice)
                                                  : (s.costPrice !== undefined && Number(s.costPrice) > 0
                                                      ? Number(s.costPrice)
                                                      : Math.round(Number(s.unitPrice || s.price || 250) * 0.6));"""

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_calc_chunk in content:
        content = content.replace(old_calc_chunk, new_calc_chunk)
        print(f"Updated cost calculation priority in {h_file}")
    else:
        print(f"old_calc_chunk not found in {h_file}")

    if old_expanded_chunk in content:
        content = content.replace(old_expanded_chunk, new_expanded_chunk)
        print(f"Updated expanded row item cost in {h_file}")
    else:
        print(f"old_expanded_chunk not found in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Priority cost rules successfully updated across all files!")
