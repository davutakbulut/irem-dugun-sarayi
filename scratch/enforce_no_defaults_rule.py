import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace DEFAULT_COMPANY_SETTINGS with an empty structure
    old_default_company_marker = "const DEFAULT_COMPANY_SETTINGS = {"
    if old_default_company_marker in content:
        # Find ending of DEFAULT_COMPANY_SETTINGS
        start_idx = content.find(old_default_company_marker)
        end_idx = content.find("};\n    const TAB_LABELS = {")
        if start_idx != -1 and end_idx != -1:
            empty_def = """const DEFAULT_COMPANY_SETTINGS = {
      id: 'default',
      company_name: '',
      brand_title: '',
      address: '',
      tax_office: '',
      tax_number: '',
      phone: '',
      email: '',
      website: '',
      authorized_person: '',
      bank_info: '',
      contract_title: '',
      contract_terms_full: ''
    };"""
            content = content[:start_idx] + empty_def + content[end_idx + 2:]
            print(f"Purged hardcoded defaults from DEFAULT_COMPANY_SETTINGS in {h_file}")

    # 2. In CompanySettingsComponent, default initial state to empty strings
    old_comp_state_block = """      const [companyName, setCompanyName] = useState(companySettings?.company_name || 'İrem Düğün Sarayı Ltd. Şti.');
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

    new_comp_state_block = """      const [companyName, setCompanyName] = useState(companySettings?.company_name || '');
      const [brandTitle, setBrandTitle] = useState(companySettings?.brand_title || '');
      const [address, setAddress] = useState(companySettings?.address || '');
      const [taxOffice, setTaxOffice] = useState(companySettings?.tax_office || '');
      const [taxNumber, setTaxNumber] = useState(companySettings?.tax_number || '');
      const [phone, setPhone] = useState(companySettings?.phone || '');
      const [email, setEmail] = useState(companySettings?.email || '');
      const [website, setWebsite] = useState(companySettings?.website || '');
      const [authorizedPerson, setAuthorizedPerson] = useState(companySettings?.authorized_person || '');
      const [bankInfo, setBankInfo] = useState(companySettings?.bank_info || '');
      const [contractTitle, setContractTitle] = useState(companySettings?.contract_title || '');
      const [contractTerms, setContractTerms] = useState(companySettings?.contract_terms_full || '');"""

    if old_comp_state_block in content:
        content = content.replace(old_comp_state_block, new_comp_state_block)
        print(f"Replaced initial form state fallbacks with clean database-bound empty state in {h_file}")

    # 3. In handlePrintInvoice, use comp fields directly without fake fallback strings
    old_handle_print_fallback = """        const comp = companySettings || (typeof DEFAULT_COMPANY_SETTINGS !== 'undefined' ? DEFAULT_COMPANY_SETTINGS : {
          company_name: 'İrem Düğün Sarayı Ltd. Şti.',
          brand_title: 'Organizasyon & Kiralama Şirketi | Sapanca Göl Kenarı, Sakarya',
          address: 'Sapanca Göl Kenarı No: 45, Sapanca / Sakarya',
          tax_office: 'Sapanca Vergi Dairesi',
          tax_number: '4820192837',
          phone: '+90 532 111 2233',
          email: 'bilgi@iremdugunsarayi.com',
          contract_title: 'DÜĞÜN SALONU KİRALAMA & ETKİNLİK SÖZLEŞMESİ',
          contract_terms_full: ''
        });"""

    new_handle_print_fallback = """        const comp = companySettings || {
          company_name: '',
          brand_title: '',
          address: '',
          tax_office: '',
          tax_number: '',
          phone: '',
          email: '',
          contract_title: '',
          contract_terms_full: ''
        };"""

    if old_handle_print_fallback in content:
        content = content.replace(old_handle_print_fallback, new_handle_print_fallback)
        print(f"Removed hardcoded print fallback in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully processed {h_file}!")

# Also clean up server.js to not return static fake strings when table is empty
with open('server.js', 'r', encoding='utf-8') as f:
    server_code = f.read()

old_server_default = """  res.json({
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
    bank_info: 'Garanti BBVA - TR12 0006 2000 0001 2345 6789 01',
    contract_title: 'DÜĞÜN SALONU KİRALAMA & ETKİNLİK SÖZLEŞMESİ',
    contract_terms_full: ''
  });"""

new_server_default = """  res.json({
    id: 'default',
    company_name: '',
    brand_title: '',
    address: '',
    tax_office: '',
    tax_number: '',
    phone: '',
    email: '',
    website: '',
    authorized_person: '',
    bank_info: '',
    contract_title: '',
    contract_terms_full: ''
  });"""

if old_server_default in server_code:
    server_code = server_code.replace(old_server_default, new_server_default)
    with open('server.js', 'w', encoding='utf-8') as f:
        f.write(server_code)
    print("Cleaned server.js fallback defaults!")

print("All default values eliminated. 100% strict database hydration rule applied!")
