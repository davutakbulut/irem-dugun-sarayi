import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update companySettings initialization in App with CacheService
    old_state_init = "const [companySettings, setCompanySettings] = useState(DEFAULT_COMPANY_SETTINGS);"
    new_state_init = "const [companySettings, setCompanySettings] = useState(() => CacheService.get('company_settings', DEFAULT_COMPANY_SETTINGS));"

    if old_state_init in content:
        content = content.replace(old_state_init, new_state_init)
        print(f"Updated companySettings init with CacheService in {h_file}")

    # 2. Update fetch in App to store in CacheService
    old_fetch = """        fetchWithRetry('/api/company-settings')
          .then(r => r.json())
          .then(data => { if (data && data.company_name) setCompanySettings(data); })
          .catch(e => console.error('Company settings fetch error:', e));"""

    new_fetch = """        fetchWithRetry('/api/company-settings')
          .then(r => r.json())
          .then(data => {
            if (data && data.company_name) {
              setCompanySettings(data);
              CacheService.set('company_settings', data);
            }
          })
          .catch(e => console.error('Company settings fetch error:', e));"""

    if old_fetch in content:
        content = content.replace(old_fetch, new_fetch)
        print(f"Updated companySettings fetch cache setter in {h_file}")

    # 3. Update onSave callback in router to update CacheService
    old_save_route = """                          const json = await res.json();
                          if (json.success && json.item) {
                            setCompanySettings(json.item);
                            showToast('Şirket Bilgileri ve Sözleşme Şablonu Başarıyla Kaydedildi!');
                          }"""

    new_save_route = """                          const json = await res.json();
                          if (json.success && json.item) {
                            setCompanySettings(json.item);
                            CacheService.set('company_settings', json.item);
                            showToast('Şirket Bilgileri ve Sözleşme Şablonu Başarıyla Kaydedildi!');
                          }"""

    if old_save_route in content:
        content = content.replace(old_save_route, new_save_route)
        print(f"Updated onSave cache setter in {h_file}")

    # 4. Add useEffect sync inside CompanySettingsComponent
    old_comp_start = """    // --- COMPANY SETTINGS & CONTRACT TERMS COMPONENT ---
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
      const [contractTerms, setContractTerms] = useState(companySettings?.contract_terms_full || DEFAULT_COMPANY_SETTINGS.contract_terms_full);"""

    new_comp_start = """    // --- COMPANY SETTINGS & CONTRACT TERMS COMPONENT ---
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

      // Keep form fields synced when companySettings loads or updates from MySQL
      useEffect(() => {
        if (companySettings) {
          if (companySettings.company_name !== undefined) setCompanyName(companySettings.company_name);
          if (companySettings.brand_title !== undefined) setBrandTitle(companySettings.brand_title);
          if (companySettings.address !== undefined) setAddress(companySettings.address);
          if (companySettings.tax_office !== undefined) setTaxOffice(companySettings.tax_office);
          if (companySettings.tax_number !== undefined) setTaxNumber(companySettings.tax_number);
          if (companySettings.phone !== undefined) setPhone(companySettings.phone);
          if (companySettings.email !== undefined) setEmail(companySettings.email);
          if (companySettings.website !== undefined) setWebsite(companySettings.website);
          if (companySettings.authorized_person !== undefined) setAuthorizedPerson(companySettings.authorized_person);
          if (companySettings.bank_info !== undefined) setBankInfo(companySettings.bank_info);
          if (companySettings.contract_title !== undefined) setContractTitle(companySettings.contract_title);
          if (companySettings.contract_terms_full !== undefined) setContractTerms(companySettings.contract_terms_full);
        }
      }, [companySettings]);"""

    if old_comp_start in content:
        content = content.replace(old_comp_start, new_comp_start)
        print(f"Added useEffect sync to CompanySettingsComponent in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully processed {h_file}!")

print("All HTML files updated for perfect Company Settings state synchronization!")
