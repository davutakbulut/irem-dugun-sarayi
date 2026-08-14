import os

# Script to inject CompanySettingsComponent, navigation tab, and updated handlePrintInvoice into all HTML files
html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add company-settings to TAB_LABELS and TAB_PERMISSIONS
    if "'company-settings':" not in content:
        content = content.replace(
            "'settings': 'Genel Ayarlar & Rol Yönetimi',",
            "'company-settings': 'Şirket Bilgileri & Sözleşme Şablonu',\n      'settings': 'Genel Ayarlar & Rol Yönetimi',"
        )
        content = content.replace(
            "'settings': ['admin'],",
            "'company-settings': ['admin'],\n      'settings': ['admin'],"
        )
        print(f"Added company-settings tab label & permission in {h_file}")

    # 2. Add sidebar menu item under SİSTEM AYARLARI
    if "{ id: 'company-settings'" not in content:
        old_menu_pos = "{ id: 'settings', label: 'Genel Sistem Ayarları'"
        new_menu_pos = "{ id: 'company-settings', label: 'Şirket & Sözleşme Şablonu', icon: 'document', fallbackEmoji: '', badge: 'RESMİ' },\n                        { id: 'settings', label: 'Genel Sistem Ayarları'"
        if old_menu_pos in content:
            content = content.replace(old_menu_pos, new_menu_pos)
            print(f"Added company-settings to sidebar menu in {h_file}")

    # 3. Add default company settings and state in App component
    if "const [companySettings, setCompanySettings]" not in content:
        # Define default
        default_company_def = """
    const DEFAULT_COMPANY_SETTINGS = {
      id: 'default',
      company_name: 'İrem Düğün Sarayı Ltd. Şti.',
      brand_title: 'Organizasyon & Kiralama Şirketi | Sapanca Göl Kenarı, Sakarya',
      address: 'Sapanca Göl Kenarı No: 45, Sapanca / Sakarya',
      tax_office: 'Sapanca Vergi Dairesi',
      tax_number: '4820192837',
      phone: '+90 532 111 2233',
      email: 'bilgi@iremdugunsarayi.com',
      website: 'https://irem.portegu.com',
      authorized_person: 'Davut Akbulut (Genel Müdür)',
      bank_info: 'Garanti BBVA - TR12 0006 2000 0001 2345 6789 01 (Alıcı: İrem Düğün Sarayı Ltd. Şti.)',
      contract_title: 'DÜĞÜN SALONU KİRALAMA & ETKİNLİK SÖZLEŞMESİ',
      contract_terms_full: `
<h3>BÖLÜM 1: GENEL HÜKÜMLER, TARAFLAR VE REZERVASYON KOŞULLARI</h3>
<p><strong>Madde 1 - Sözleşmenin Tarafları:</strong> İşbu sözleşme, bir tarafta Hizmet Veren (İrem Düğün Sarayı Ltd. Şti.) ile diğer tarafta Hizmet Alan (Müşteri/Kiracı) arasında akdedilmiştir.</p>
<p><strong>Madde 2 - Sözleşmenin Konusu ve Kapsamı:</strong> Hizmet Veren'in mülkiyetinde bulunan etkinlik salonunun, sözleşmede belirtilen tarih ve saat aralığında, belirlenen davetli kapasitesi ve seçilen ek hizmetler doğrultusunda tahsis edilmesidir.</p>
<p><strong>Madde 3 - Tarih, Saat Dilimi ve Kapasite:</strong> Etkinlik başlangıç ve bitiş saatleri kesin olup program aşımı durumunda ek salon kullanım ücreti tahakkuk ettirilir. Mekan azami kapasitesinin aşılmaması esastır.</p>
<p><strong>Madde 4 - Kapora, Fiyat ve Ödeme Planı:</strong> Rezervasyonun kesinleşmesi için belirlenen asgari kapora tutarı sözleşme anında tahsil edilir. Kalan bakiye en geç etkinlik tarihinden 7 gün öncesine kadar eksiksiz ödenmelidir.</p>

<div class="page-break" style="page-break-before: always; margin-top: 30px;"></div>

<h3>BÖLÜM 2: HİZMET DETAYLARI, İPTAL VE DEĞİŞİKLİK ŞARTLARI</h3>
<p><strong>Madde 5 - Catering ve Menü Standartları:</strong> Seçilen yemekli/kokteyl menüler profesyonel hijyen ve kalite standartlarında servis edilir. Menü tadımı ve kişi sayısı revizyonları etkinlikten en geç 10 gün önce yazılı olarak bildirilmelidir.</p>
<p><strong>Madde 6 - Fotoğraf, Video ve Müzik Hizmetleri:</strong> Etkinlik süresince ses ve ışık sistemleri uzman teknik personelce yönetilir. 4K video ve fotoğraf teslimatları organizasyon bitiminden itibaren azami 20 iş günü içinde dijital/albüm olarak teslim edilir.</p>
<p><strong>Madde 7 - Rezervasyon İptali ve Kapora İade Koşulları:</strong> Hizmet Alan tarafından etkinlik tarihine 60 günden fazla süre kala yapılan iptallerde kaporanın %50'si iade edilir. 60 günden az kalan iptallerde kapora iadesi yapılmaz; ancak karşılıklı mutabakatla müsait başka bir tarihe devir hakkı tanınabilir.</p>
<p><strong>Madde 8 - Tarih Değişikliği ve Seans Revizyonu:</strong> Tarih erteleme talepleri en geç 30 gün öncesinden yazılı yapılmalıdır. Yeni seçilecek tarihteki güncel fiyat farkı Hizmet Alan tarafından karşılanır.</p>

<div class="page-break" style="page-break-before: always; margin-top: 30px;"></div>

<h3>BÖLÜM 3: TESİS KULLANIM KURALLARI, MÜCBİR SEBEPLER VE YETKİLİ MAHKEME</h3>
<p><strong>Madde 9 - Tesis Güvenliği ve Demirbaş Sorumluluğu:</strong> Hizmet Alan ve davetlileri tesis genel ahlak ve huzur kurallarına uymakla yükümlüdür. Mekan demirbaşlarına verilecek zararlar Hizmet Alan tarafından tazmin edilir.</p>
<p><strong>Madde 10 - Mücbir Sebepler:</strong> Doğal afet, salgın hastalık veya yasal kısıtlamalar gibi tarafların iradesi dışındaki durumlarda etkinlik ileri bir tarihe ertelenir; taraflar birbirine tazminat yükümlülüğü getirmez.</p>
<p><strong>Madde 11 - Kişisel Verilerin Korunması (KVKK):</strong> Hizmet Alan'ın paylaştığı veriler 6698 sayılı KVKK kapsamında yalnızca organizasyon ve muhasebe süreçleri için işlenir.</p>
<p><strong>Madde 12 - Yetkili Mahkeme:</strong> İşbu sözleşmenin uygulanmasından doğabilecek ihtilaflarda Sakarya Mahkemeleri ve İcra Daireleri yetkilidir.</p>
`
    };
"""
        content = content.replace("const TAB_LABELS = {", default_company_def + "\n    const TAB_LABELS = {")
        
        # Add state inside App
        content = content.replace(
            "const [currentUserState, setCurrentUserState] = useState(",
            "const [companySettings, setCompanySettings] = useState(DEFAULT_COMPANY_SETTINGS);\n      const [currentUserState, setCurrentUserState] = useState("
        )

        # Add fetch in App useEffect
        fetch_call = """
        fetchWithRetry('/api/company-settings')
          .then(r => r.json())
          .then(data => { if (data && data.company_name) setCompanySettings(data); })
          .catch(e => console.error('Company settings fetch error:', e));
"""
        app_fetch_anchor = "fetchWithRetry('/api/users')"
        if app_fetch_anchor in content:
            content = content.replace(app_fetch_anchor, fetch_call + "\n        " + app_fetch_anchor)

        print(f"Added companySettings state and fetch in {h_file}")

    # 4. Update handlePrintInvoice to dynamically use companySettings and append the 3-page contract clauses
    old_handle_print = """      // Print Invoice Helper
      const handlePrintInvoice = (res) => {
        const venue = venues.find(v => v.id === res.venueId);
        const printWin = window.open('', '_blank');
        printWin.document.write(`
          <!DOCTYPE html>
          <html>
          <head>
            <title>İrem Düğün Sarayı - Resmi Sözleşme & Fatura (${res.id})</title>
            <style>
              body { font-family: 'Segoe UI', Arial, sans-serif; padding: 40px; color: #1e293b; line-height: 1.5; }
              .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #d97706; padding-bottom: 20px; }
              .logo { font-size: 24px; font-weight: bold; color: #b45309; }
              .title { font-size: 18px; font-weight: bold; text-align: center; margin: 30px 0 10px 0; color: #0f172a; text-transform: uppercase; }
              .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 25px; }
              .card { background: #f8fafc; border: 1px solid #cbd5e1; padding: 15px; border-radius: 8px; font-size: 13px; }
              table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 13px; }
              th, td { border: 1px solid #cbd5e1; padding: 10px; text-align: left; }
              th { background: #f1f5f9; font-weight: bold; }
              .totals { margin-top: 20px; text-align: right; font-size: 14px; }
              .totals div { margin-bottom: 5px; }
              .grand-total { font-size: 18px; font-weight: bold; color: #b45309; }
              .signatures { display: flex; justify-content: space-between; margin-top: 50px; font-size: 13px; }
              .sig-box { border-top: 1px solid #94a3b8; width: 200px; text-align: center; padding-top: 8px; }
            </style>
          



</head>
          <body>
            <div class="header">
              <div>
                <div class="logo"><ThemeIcon icon="crown" className="w-4 h-4 inline-block shrink-0" /> İREM DÜĞÜN SARAYI</div>
                <div style="font-size: 12px; color: #64748b;">Organizasyon & Kiralama Şirketi | Sapanca Göl Kenarı, Sakarya</div>
              </div>
              <div style="text-align: right;">
                <div style="font-size: 16px; font-weight: bold;">SÖZLEŞME & FATURA</div>
                <div style="font-size: 12px; color: #64748b;">Belge No: <strong>${res.id}</strong></div>
                <div style="font-size: 12px; color: #64748b;">Tarih: ${new Date().toLocaleDateString('tr-TR')}</div>
              </div>
            </div>

            <div class="title">DÜĞÜN SALONU KİRALAMA & ETKİNLİK SÖZLEŞMESİ</div>

            <div class="grid">
              <div class="card">
                <strong>ŞİRKET BİLGİLERİ (Hizmet Veren):</strong><br>
                İrem Düğün Sarayı Ltd. Şti.<br>
                Sapanca Göl Kenarı No: 45, Sakarya<br>
                Sapanca Vergi Dairesi | VKN: 4820192837<br>
                Tel: +90 532 111 2233
              </div>"""

    new_handle_print = """      // Print Invoice Helper (100% Dynamic with Database Company Settings & 3-Page Contract Clauses)
      const handlePrintInvoice = (res) => {
        const venue = venues.find(v => v.id === res.venueId);
        const comp = companySettings || DEFAULT_COMPANY_SETTINGS;
        const printWin = window.open('', '_blank');
        printWin.document.write(`
          <!DOCTYPE html>
          <html>
          <head>
            <title>${comp.company_name} - Resmi Sözleşme & Fatura (${res.id})</title>
            <style>
              body { font-family: 'Segoe UI', Arial, sans-serif; padding: 40px; color: #1e293b; line-height: 1.5; }
              .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #d97706; padding-bottom: 20px; }
              .logo { font-size: 24px; font-weight: bold; color: #b45309; }
              .title { font-size: 18px; font-weight: bold; text-align: center; margin: 30px 0 10px 0; color: #0f172a; text-transform: uppercase; }
              .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 25px; }
              .card { background: #f8fafc; border: 1px solid #cbd5e1; padding: 15px; border-radius: 8px; font-size: 13px; }
              table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 13px; }
              th, td { border: 1px solid #cbd5e1; padding: 10px; text-align: left; }
              th { background: #f1f5f9; font-weight: bold; }
              .totals { margin-top: 20px; text-align: right; font-size: 14px; }
              .totals div { margin-bottom: 5px; }
              .grand-total { font-size: 18px; font-weight: bold; color: #b45309; }
              .signatures { display: flex; justify-content: space-between; margin-top: 40px; font-size: 13px; }
              .sig-box { border-top: 1px solid #94a3b8; width: 220px; text-align: center; padding-top: 8px; font-weight: bold; }
              .contract-terms-box { margin-top: 30px; font-size: 12px; color: #334155; line-height: 1.7; }
              .contract-terms-box h3 { color: #0f172a; font-size: 14px; border-bottom: 1px solid #e2e8f0; padding-bottom: 5px; margin-top: 20px; }
              @media print {
                body { padding: 20px; }
                .page-break { page-break-before: always; }
                button { display: none; }
              }
            </style>
          </head>
          <body>
            <div class="header">
              <div>
                <div class="logo">👑 ${comp.company_name}</div>
                <div style="font-size: 12px; color: #64748b;">${comp.brand_title}</div>
              </div>
              <div style="text-align: right;">
                <div style="font-size: 16px; font-weight: bold;">SÖZLEŞME & FATURA</div>
                <div style="font-size: 12px; color: #64748b;">Belge No: <strong>${res.id}</strong></div>
                <div style="font-size: 12px; color: #64748b;">Tarih: ${new Date().toLocaleDateString('tr-TR')}</div>
              </div>
            </div>

            <div class="title">${comp.contract_title || 'DÜĞÜN SALONU KİRALAMA & ETKİNLİK SÖZLEŞMESİ'}</div>

            <div class="grid">
              <div class="card">
                <strong>ŞİRKET BİLGİLERİ (Hizmet Veren):</strong><br>
                ${comp.company_name}<br>
                ${comp.address}<br>
                ${comp.tax_office} | VKN: ${comp.tax_number}<br>
                Tel: ${comp.phone} | ${comp.email}
              </div>"""

    if old_handle_print in content:
        content = content.replace(old_handle_print, new_handle_print)
        print(f"Updated handlePrintInvoice header in {h_file}")

    # Add contract terms to end of document.write before </body>
    old_doc_end = """            <div class="signatures">
              <div class="sig-box">İrem Düğün Sarayı Yetkilisi<br>(İmza & Kaşe)</div>
              <div class="sig-box">Müşteri / Kiracı<br>(İmza)</div>
            </div>
          </body>
          </html>
        `);
        printWin.document.close();"""

    new_doc_end = """            <div class="signatures">
              <div class="sig-box">${comp.company_name}<br>Hizmet Veren (İmza & Kaşe)</div>
              <div class="sig-box">${res.customerName}<br>Hizmet Alan / Kiracı (İmza)</div>
            </div>

            <!-- RESMİ 3 SAYFALIK SÖZLEŞME HÜKÜMLERİ VE MADDELERİ -->
            <div class="contract-terms-box">
              <div class="page-break" style="page-break-before: always; margin-top: 40px; padding-top: 20px; border-top: 2px solid #d97706;"></div>
              <div style="text-align: center; font-weight: bold; font-size: 16px; margin-bottom: 20px; color: #b45309; text-transform: uppercase;">
                ${comp.contract_title || 'DÜĞÜN SALONU KİRALAMA & ETKİNLİK HİZMET SÖZLEŞMESİ'} GENEL HÜKÜMLERİ
              </div>
              <div>
                ${comp.contract_terms_full || ''}
              </div>
              <div class="signatures" style="margin-top: 50px;">
                <div class="sig-box">${comp.company_name}<br>Hizmet Veren (İmza & Kaşe)</div>
                <div class="sig-box">${res.customerName}<br>Hizmet Alan (Okudum, Onayladım)</div>
              </div>
            </div>

          </body>
          </html>
        `);
        printWin.document.close();"""

    if old_doc_end in content:
        content = content.replace(old_doc_end, new_doc_end)
        print(f"Appended contract terms to handlePrintInvoice in {h_file}")

    # 5. Add CompanySettingsComponent in activeTab render
    company_comp_route = """
                  {activeTab === 'company-settings' && (
                    <CompanySettingsComponent
                      companySettings={companySettings}
                      onSave={async (updated) => {
                        try {
                          const res = await fetchWithRetry('/api/company-settings', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(updated)
                          });
                          const json = await res.json();
                          if (json.success && json.item) {
                            setCompanySettings(json.item);
                            showToast('Şirket Bilgileri ve Sözleşme Şablonu Başarıyla Kaydedildi!');
                          }
                        } catch(e) {
                          showToast('Kaydetme hatası: ' + e.message);
                        }
                      }}
                    />
                  )}
    """
    if "activeTab === 'company-settings'" not in content:
        content = content.replace("{activeTab === 'settings' && (", company_comp_route + "\n                  {activeTab === 'settings' && (")
        print(f"Added company-settings route in {h_file}")

    # 6. Inject the CompanySettingsComponent React code
    company_comp_def = """
    // --- COMPANY SETTINGS & CONTRACT TERMS COMPONENT ---
    function CompanySettingsComponent({ companySettings, onSave }) {
      const [activeSubTab, setActiveSubTab] = useState('company'); // 'company' | 'contract' | 'preview'
      
      const [companyName, setCompanyName] = useState(companySettings?.company_name || 'İrem Düğün Sarayı Ltd. Şti.');
      const [brandTitle, setBrandTitle] = useState(companySettings?.brand_title || 'Organizasyon & Kiralama Şirketi | Sapanca Göl Kenarı, Sakarya');
      const [address, setAddress] = useState(companySettings?.address || 'Sapanca Göl Kenarı No: 45, Sapanca / Sakarya');
      const [taxOffice, setTaxOffice] = useState(companySettings?.tax_office || 'Sapanca Vergi Dairesi');
      const [taxNumber, setTaxNumber] = useState(companySettings?.tax_number || '4820192837');
      const [phone, setPhone] = useState(companySettings?.phone || '+90 532 111 2233');
      const [email, setEmail] = useState(companySettings?.email || 'bilgi@iremdugunsarayi.com');
      const [website, setWebsite] = useState(companySettings?.website || 'https://irem.portegu.com');
      const [authorizedPerson, setAuthorizedPerson] = useState(companySettings?.authorized_person || 'Davut Akbulut (Genel Müdür)');
      const [bankInfo, setBankInfo] = useState(companySettings?.bank_info || 'Garanti BBVA - TR12 0006 2000 0001 2345 6789 01');
      const [contractTitle, setContractTitle] = useState(companySettings?.contract_title || 'DÜĞÜN SALONU KİRALAMA & ETKİNLİK SÖZLEŞMESİ');
      const [contractTerms, setContractTerms] = useState(companySettings?.contract_terms_full || DEFAULT_COMPANY_SETTINGS.contract_terms_full);

      const [isSaving, setIsSaving] = useState(false);

      const handleSubmit = async (e) => {
        if (e) e.preventDefault();
        setIsSaving(true);
        try {
          await onSave({
            company_name: companyName,
            brand_title: brandTitle,
            address: address,
            tax_office: taxOffice,
            tax_number: taxNumber,
            phone: phone,
            email: email,
            website: website,
            authorized_person: authorizedPerson,
            bank_info: bankInfo,
            contract_title: contractTitle,
            contract_terms_full: contractTerms
          });
        } finally {
          setIsSaving(false);
        }
      };

      const handleResetDefaults = () => {
        if (confirm('Sözleşme maddelerini varsayılan 3 sayfalık resmi şablona sıfırlamak istediğinize emin misiniz?')) {
          setContractTerms(DEFAULT_COMPANY_SETTINGS.contract_terms_full);
        }
      };

      return (
        <div className="space-y-6 animate-fade-in">
          {/* HEADER */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-200 dark:border-brand-border/40">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-500 shrink-0">
                <ThemeIcon icon="document" className="w-6 h-6" />
              </div>
              <div>
                <h2 className="text-2xl font-heading font-extrabold text-slate-900 dark:text-gray-100 gold-gradient-text">
                  Şirket Bilgileri & Sözleşme Şablonu
                </h2>
                <p className="text-xs text-slate-500 dark:text-gray-400">
                  Resmi fatura başlığı, şirket iletişim bilgileri ve 3 sayfalık etkinlik sözleşmesi maddelerini yönetin.
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <button
                type="button"
                onClick={handleSubmit}
                disabled={isSaving}
                className="gold-button font-bold px-5 py-2.5 rounded-xl text-xs shadow-lg flex items-center space-x-2 cursor-pointer hover:scale-105 transition"
              >
                <span>💾</span>
                <span>{isSaving ? 'Kaydediliyor...' : 'Değişiklikleri Veritabanına Kaydet ✓'}</span>
              </button>
            </div>
          </div>

          {/* SUB-TABS NAVIGATION */}
          <div className="flex space-x-2 border-b border-slate-200 dark:border-brand-border pb-2 overflow-x-auto custom-scrollbar">
            <button
              type="button"
              onClick={() => setActiveSubTab('company')}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-2 shrink-0 ${
                activeSubTab === 'company'
                  ? 'bg-amber-500 text-slate-950 shadow-sm'
                  : 'text-slate-600 dark:text-gray-400 hover:bg-slate-100 dark:hover:bg-brand-dark'
              }`}
            >
              <span>🏢</span>
              <span>Şirket & Fatura Bilgileri</span>
            </button>

            <button
              type="button"
              onClick={() => setActiveSubTab('contract')}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-2 shrink-0 ${
                activeSubTab === 'contract'
                  ? 'bg-amber-500 text-slate-950 shadow-sm'
                  : 'text-slate-600 dark:text-gray-400 hover:bg-slate-100 dark:hover:bg-brand-dark'
              }`}
            >
              <span>📜</span>
              <span>3 Sayfalık Resmi Sözleşme Maddeleri</span>
            </button>

            <button
              type="button"
              onClick={() => setActiveSubTab('preview')}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-2 shrink-0 ${
                activeSubTab === 'preview'
                  ? 'bg-amber-500 text-slate-950 shadow-sm'
                  : 'text-slate-600 dark:text-gray-400 hover:bg-slate-100 dark:hover:bg-brand-dark'
              }`}
            >
              <span>👁️</span>
              <span>Canlı Sözleşme Ön İzlemesi</span>
            </button>
          </div>

          {/* TAB 1: ŞİRKET BİLGİLERİ */}
          {activeSubTab === 'company' && (
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="glass-panel p-6 rounded-3xl space-y-4 border border-slate-200 dark:border-brand-border shadow-sm">
                <h3 className="font-heading font-bold text-base text-slate-900 dark:text-gray-100 flex items-center space-x-2 border-b border-slate-100 dark:border-brand-border/40 pb-2">
                  <span>🏢 Şirket Resmi Kimlik & İletişim Bilgileri (Hizmet Veren)</span>
                </h3>
                <p className="text-xs text-slate-500 dark:text-gray-400">
                  Bu bilgiler tüm sözleşmelerin sol üst köşesindeki "ŞİRKET BİLGİLERİ" kutusunda ve fatura başlığında dinamik olarak gösterilir.
                </p>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
                  <div>
                    <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Şirket Resmi Ünvanı:</label>
                    <input
                      type="text"
                      value={companyName}
                      onChange={e => setCompanyName(e.target.value)}
                      required
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-900 dark:text-white font-bold"
                    />
                  </div>

                  <div>
                    <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Marka / Tesis Başlığı:</label>
                    <input
                      type="text"
                      value={brandTitle}
                      onChange={e => setBrandTitle(e.target.value)}
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-900 dark:text-white"
                    />
                  </div>

                  <div className="sm:col-span-2">
                    <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Şirket Resmi Adresi:</label>
                    <input
                      type="text"
                      value={address}
                      onChange={e => setAddress(e.target.value)}
                      required
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-900 dark:text-white"
                    />
                  </div>

                  <div>
                    <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Bağlı Olunan Vergi Dairesi:</label>
                    <input
                      type="text"
                      value={taxOffice}
                      onChange={e => setTaxOffice(e.target.value)}
                      required
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-900 dark:text-white"
                    />
                  </div>

                  <div>
                    <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Vergi Kimlik No (VKN / Mersis):</label>
                    <input
                      type="text"
                      value={taxNumber}
                      onChange={e => setTaxNumber(e.target.value)}
                      required
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-900 dark:text-white font-mono font-bold"
                    />
                  </div>

                  <div>
                    <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Resmi İletişim Telefonu:</label>
                    <input
                      type="text"
                      value={phone}
                      onChange={e => setPhone(e.target.value)}
                      required
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-900 dark:text-white font-bold"
                    />
                  </div>

                  <div>
                    <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Kurumsal E-Posta Adresi:</label>
                    <input
                      type="email"
                      value={email}
                      onChange={e => setEmail(e.target.value)}
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-900 dark:text-white"
                    />
                  </div>

                  <div>
                    <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Şirket Yetkilisi / Temsilci:</label>
                    <input
                      type="text"
                      value={authorizedPerson}
                      onChange={e => setAuthorizedPerson(e.target.value)}
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-900 dark:text-white"
                    />
                  </div>

                  <div>
                    <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Resmi Web Sitesi URL:</label>
                    <input
                      type="url"
                      value={website}
                      onChange={e => setWebsite(e.target.value)}
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-900 dark:text-white"
                    />
                  </div>

                  <div className="sm:col-span-2">
                    <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Banka & IBAN Bilgileri (Ödeme Bilgisi):</label>
                    <input
                      type="text"
                      value={bankInfo}
                      onChange={e => setBankInfo(e.target.value)}
                      placeholder="Örn: Garanti BBVA - TR12 0006 2000 0001 2345 6789 01"
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-900 dark:text-white font-mono"
                    />
                  </div>
                </div>

                <div className="pt-3 border-t border-slate-100 dark:border-brand-border/40 flex justify-end">
                  <button
                    type="submit"
                    disabled={isSaving}
                    className="gold-button font-bold px-6 py-2.5 rounded-xl text-xs shadow"
                  >
                    {isSaving ? 'Kaydediliyor...' : 'Şirket Bilgilerini Kaydet ✓'}
                  </button>
                </div>
              </div>
            </form>
          )}

          {/* TAB 2: SÖZLEŞME MADDELERİ EDİTÖRÜ */}
          {activeSubTab === 'contract' && (
            <div className="space-y-4">
              <div className="glass-panel p-6 rounded-3xl space-y-4 border border-slate-200 dark:border-brand-border shadow-sm">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 dark:border-brand-border/40 pb-3">
                  <div>
                    <h3 className="font-heading font-bold text-base text-slate-900 dark:text-gray-100 flex items-center space-x-2">
                      <span>📜 3 Sayfalık Resmi Hukuki Sözleşme Maddeleri Şablonu</span>
                    </h3>
                    <p className="text-xs text-slate-500 dark:text-gray-400 mt-0.5">
                      Sözleşme PDF'inin sonuna otomatik olarak eklenecek hukuki maddeleri ve şartları düzenleyin.
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={handleResetDefaults}
                    className="px-3 py-1.5 rounded-xl bg-amber-500/10 text-amber-700 dark:text-gold-400 border border-amber-500/30 font-bold text-xs hover:bg-amber-500/20 transition self-start sm:self-auto cursor-pointer"
                  >
                    🔄 Varsayılan Şablonu Geri Yükle
                  </button>
                </div>

                <div className="space-y-3 text-xs">
                  <div>
                    <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Sözleşme Ana Başlığı:</label>
                    <input
                      type="text"
                      value={contractTitle}
                      onChange={e => setContractTitle(e.target.value)}
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-900 dark:text-white font-bold"
                    />
                  </div>

                  <div>
                    <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">
                      Sözleşme Maddeleri Metni (HTML / Paragraflar Desteklenir):
                    </label>
                    <div className="text-[11px] text-slate-500 dark:text-gray-400 mb-1">
                      İpucu: Sayfa geçişleri için <code>&lt;div class="page-break" style="page-break-before: always;"&gt;&lt;/div&gt;</code> kullanabilirsiniz.
                    </div>
                    <textarea
                      value={contractTerms}
                      onChange={e => setContractTerms(e.target.value)}
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-2xl p-4 h-96 text-slate-800 dark:text-gray-200 font-mono text-xs leading-relaxed"
                      placeholder="Sözleşme maddeleri..."
                    />
                  </div>
                </div>

                <div className="pt-3 border-t border-slate-100 dark:border-brand-border/40 flex justify-end space-x-2">
                  <button
                    type="button"
                    onClick={() => setActiveSubTab('preview')}
                    className="px-4 py-2 bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-200 rounded-xl font-bold text-xs"
                  >
                    Ön İzlemeye Geç 👁️
                  </button>
                  <button
                    type="button"
                    onClick={handleSubmit}
                    disabled={isSaving}
                    className="gold-button font-bold px-6 py-2 rounded-xl text-xs shadow"
                  >
                    {isSaving ? 'Kaydediliyor...' : 'Sözleşme Şablonunu Kaydet ✓'}
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* TAB 3: CANLI ÖN İZLEME */}
          {activeSubTab === 'preview' && (
            <div className="space-y-4">
              <div className="glass-panel p-6 sm:p-8 rounded-3xl space-y-6 border border-slate-200 dark:border-brand-border shadow-md bg-white text-slate-900 max-w-4xl mx-auto">
                <div className="flex justify-between items-center border-b-2 border-amber-600 pb-4">
                  <div>
                    <h2 className="text-xl font-bold text-amber-700">👑 {companyName}</h2>
                    <p className="text-xs text-slate-500">{brandTitle}</p>
                  </div>
                  <div className="text-right text-xs text-slate-500">
                    <span className="font-bold block text-slate-800">RESMİ SÖZLEŞME & FATURA</span>
                    <span>Tarih: {new Date().toLocaleDateString('tr-TR')}</span>
                  </div>
                </div>

                <h3 className="text-center font-bold text-base text-slate-900 tracking-wide uppercase">
                  {contractTitle}
                </h3>

                <div className="grid grid-cols-2 gap-4 text-xs bg-slate-50 p-4 rounded-xl border border-slate-200">
                  <div>
                    <strong className="text-amber-800">ŞİRKET BİLGİLERİ (Hizmet Veren):</strong><br />
                    {companyName}<br />
                    {address}<br />
                    {taxOffice} | VKN: {taxNumber}<br />
                    Tel: {phone} | {email}
                  </div>
                  <div>
                    <strong className="text-slate-800">MÜŞTERİ BİLGİLERİ (Hizmet Alan):</strong><br />
                    Ahmet & Ayşe Yılmaz<br />
                    Tel: 0532 999 8877<br />
                    E-posta: ornek_musteri@gmail.com<br />
                    Bireysel (TC No: 12345678901)
                  </div>
                </div>

                {/* DYNAMIC CONTRACT CLAUSES PREVIEW */}
                <div className="border-t border-slate-200 pt-4 text-xs leading-relaxed space-y-3 text-slate-700">
                  <div dangerouslySetInnerHTML={{ __html: contractTerms }} />
                </div>

                {/* SIGNATURES */}
                <div className="flex justify-between pt-8 border-t border-slate-200 text-xs">
                  <div className="w-52 border-t border-slate-400 text-center pt-2 font-bold">
                    {companyName}<br /><span className="text-[11px] font-normal text-slate-500">Hizmet Veren (İmza & Kaşe)</span>
                  </div>
                  <div className="w-52 border-t border-slate-400 text-center pt-2 font-bold">
                    Ahmet Yılmaz<br /><span className="text-[11px] font-normal text-slate-500">Hizmet Alan (Okudum, Onayladım)</span>
                  </div>
                </div>

              </div>
            </div>
          )}

        </div>
      );
    }
"""
    if "function CompanySettingsComponent" not in content:
        content = content.replace(
            "// --- VENUE MODAL COMPONENT",
            company_comp_def + "\n\n    // --- VENUE MODAL COMPONENT"
        )
        print(f"Injected CompanySettingsComponent into {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully processed {h_file}!")

print("All HTML files updated with Company Settings and Contract Terms management!")
