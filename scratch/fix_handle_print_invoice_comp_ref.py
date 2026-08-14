import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

old_fn_start = """      // Print Invoice Helper
      const handlePrintInvoice = (res) => {
        const venue = venues.find(v => v.id === res.venueId);
        const printWin = window.open('', '_blank');"""

new_fn_start = """      // Print Invoice Helper (100% Dynamic with Database Company Settings & 3-Page Contract Clauses)
      const handlePrintInvoice = (res) => {
        const venue = venues.find(v => v.id === res.venueId);
        const comp = companySettings || (typeof DEFAULT_COMPANY_SETTINGS !== 'undefined' ? DEFAULT_COMPANY_SETTINGS : {
          company_name: 'İrem Düğün Sarayı Ltd. Şti.',
          brand_title: 'Organizasyon & Kiralama Şirketi | Sapanca Göl Kenarı, Sakarya',
          address: 'Sapanca Göl Kenarı No: 45, Sapanca / Sakarya',
          tax_office: 'Sapanca Vergi Dairesi',
          tax_number: '4820192837',
          phone: '+90 532 111 2233',
          email: 'bilgi@iremdugunsarayi.com',
          contract_title: 'DÜĞÜN SALONU KİRALAMA & ETKİNLİK SÖZLEŞMESİ',
          contract_terms_full: ''
        });
        const printWin = window.open('', '_blank');"""

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Also update header inside document.write if needed
    if old_fn_start in content:
        content = content.replace(old_fn_start, new_fn_start)
        print(f"Fixed comp ref in {h_file}")

    # Also make sure company details in the top card use comp
    old_comp_card = """            <div class="grid">
              <div class="card">
                <strong>ŞİRKET BİLGİLERİ (Hizmet Veren):</strong><br>
                İrem Düğün Sarayı Ltd. Şti.<br>
                Sapanca Göl Kenarı No: 45, Sakarya<br>
                Sapanca Vergi Dairesi | VKN: 4820192837<br>
                Tel: +90 532 111 2233
              </div>"""

    new_comp_card = """            <div class="grid">
              <div class="card">
                <strong>ŞİRKET BİLGİLERİ (Hizmet Veren):</strong><br>
                ${comp.company_name}<br>
                ${comp.address}<br>
                ${comp.tax_office} | VKN: ${comp.tax_number}<br>
                Tel: ${comp.phone} | ${comp.email}
              </div>"""

    if old_comp_card in content:
        content = content.replace(old_comp_card, new_comp_card)
        print(f"Updated company card in {h_file}")

    # Also update logo & brand in header
    old_logo_hdr = """            <div class="header">
              <div>
                <div class="logo"><ThemeIcon icon="crown" className="w-4 h-4 inline-block shrink-0" /> İREM DÜĞÜN SARAYI</div>
                <div style="font-size: 12px; color: #64748b;">Organizasyon & Kiralama Şirketi | Sapanca Göl Kenarı, Sakarya</div>
              </div>"""

    new_logo_hdr = """            <div class="header">
              <div>
                <div class="logo">👑 ${comp.company_name}</div>
                <div style="font-size: 12px; color: #64748b;">${comp.brand_title}</div>
              </div>"""

    if old_logo_hdr in content:
        content = content.replace(old_logo_hdr, new_logo_hdr)
        print(f"Updated logo header in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully processed {h_file}!")

print("All HTML files fixed for handlePrintInvoice!")
