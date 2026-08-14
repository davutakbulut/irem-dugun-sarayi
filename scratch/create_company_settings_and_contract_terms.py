import os

# 1. UPDATE server.js: Add company_settings table and GET / POST endpoints
with open('server.js', 'r', encoding='utf-8') as f:
    server_code = f.read()

company_table_sql = """
      await pool.query(`
        CREATE TABLE IF NOT EXISTS company_settings (
          id VARCHAR(50) PRIMARY KEY,
          company_name VARCHAR(255) NOT NULL DEFAULT 'İrem Düğün Sarayı Ltd. Şti.',
          brand_title VARCHAR(255) DEFAULT 'Organizasyon & Kiralama Şirketi',
          address TEXT,
          tax_office VARCHAR(150) DEFAULT 'Sapanca Vergi Dairesi',
          tax_number VARCHAR(50) DEFAULT '4820192837',
          phone VARCHAR(50) DEFAULT '+90 532 111 2233',
          email VARCHAR(100) DEFAULT 'bilgi@iremdugunsarayi.com',
          website VARCHAR(100) DEFAULT 'https://irem.portegu.com',
          authorized_person VARCHAR(100) DEFAULT 'Davut Akbulut (Genel Müdür)',
          bank_info TEXT,
          contract_title VARCHAR(255) DEFAULT 'DÜĞÜN SALONU KİRALAMA & ETKİNLİK HİZMET SÖZLEŞMESİ',
          contract_terms_full LONGTEXT,
          updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
      `);

      // Seed default company settings if not exists
      try {
        const [exist] = await pool.query("SELECT id FROM company_settings WHERE id = 'default'");
        if (!exist || exist.length === 0) {
          const defaultTerms = `
<h3>BÖLÜM 1: GENEL HÜKÜMLER, TARAFLAR VE REZERVASYON KOŞULLARI</h3>
<p><strong>Madde 1 - Sözleşmenin Tarafları:</strong> İşbu sözleşme, bir tarafta yukarıda bilgileri yer alan Hizmet Veren (İrem Düğün Sarayı Ltd. Şti.) ile diğer tarafta Hizmet Alan (Müşteri/Kiracı) arasında karşılıklı mutabakat ile akdedilmiştir.</p>
<p><strong>Madde 2 - Sözleşmenin Konusu ve Kapsamı:</strong> Hizmet Veren'in mülkiyetinde/işletmesinde bulunan etkinlik salonunun, sözleşmede belirtilen tarih ve saat aralığında, belirlenen davetli kapasitesi ve seçilen ek hizmetler doğrultusunda Hizmet Alan'a tahsis edilmesidir.</p>
<p><strong>Madde 3 - Tarih, Saat Dilimi ve Kapasite:</strong> Etkinlik başlangıç ve bitiş saatleri kesin olup; program aşımı durumunda her ek saat için yürürlükteki ek salon kullanım ücreti tahakkuk ettirilir. Mekan azami kapasitesinin aşılmaması esastır.</p>
<p><strong>Madde 4 - Kapora, Fiyat ve Ödeme Planı:</strong> Rezervasyonun kesinleşmesi için belirlenen asgari kapora tutarı sözleşme anında tahsil edilir. Kalan bakiye, en geç etkinlik tarihinden 7 (yedi) iş günü öncesine kadar Hizmet Veren'in banka hesabına veya kasasına eksiksiz ödenmelidir.</p>

<div class="page-break" style="page-break-before: always; margin-top: 30px;"></div>

<h3>BÖLÜM 2: HİZMET DETAYLARI, İPTAL VE DEĞİŞİKLİK ŞARTLARI</h3>
<p><strong>Madde 5 - Catering ve Menü Standartları:</strong> Seçilen yemekli/kokteyl menüler profesyonel hijyen ve kalite standartlarında servis edilir. Menü tadımı ve kişi sayısı revizyonları etkinlikten en geç 10 gün önce yazılı olarak bildirilmelidir.</p>
<p><strong>Madde 6 - Fotoğraf, Video ve Müzik Hizmetleri:</strong> Etkinlik süresince ses ve ışık sistemleri uzman teknik personelce yönetilir. 4K video ve fotoğraf teslimatları organizasyon bitiminden itibaren azami 20 iş günü içinde dijital/albüm olarak teslim edilir.</p>
<p><strong>Madde 7 - Rezervasyon İptali ve Kapora İade Koşulları:</strong> Hizmet Alan tarafından etkinlik tarihine 60 günden fazla süre kala yapılan iptallerde kaporanın %50'si iade edilir. 60 günden az kalan iptallerde kapora iadesi yapılmaz; ancak karşılıklı mutabakatla sezon içi müsait başka bir tarihe devir hakkı tanınabilir.</p>
<p><strong>Madde 8 - Tarih Değişikliği ve Seans Revizyonu:</strong> Tarih erteleme talepleri en geç 30 gün öncesinden yazılı yapılmalıdır. Yeni seçilecek tarihteki güncel fiyat farkı Hizmet Alan tarafından karşılanır.</p>

<div class="page-break" style="page-break-before: always; margin-top: 30px;"></div>

<h3>BÖLÜM 3: TESİS KULLANIM KURALLARI, MÜCBİR SEBEPLER VE YETKİLİ MAHKEME</h3>
<p><strong>Madde 9 - Tesis Güvenliği ve Demirbaş Sorumluluğu:</strong> Hizmet Alan ve davetlileri tesis genel ahlak ve huzur kurallarına uymakla yükümlüdür. Mekan demirbaşlarına, ses-ışık donanımına kasti verilecek zararlar Hizmet Alan tarafından tazmin edilir.</p>
<p><strong>Madde 10 - Mücbir Sebepler (Force Majeure):</strong> Deprem, sel, yangın, salgın hastalık, resmi makamlarca getirilen sokağa çıkma yasakları veya yasal kısıtlamalar gibi tarafların iradesi dışındaki durumlarda etkinlik ileri bir tarihe ertelenir; taraflar birbirine tazminat yükümlülüğü getirmez.</p>
<p><strong>Madde 11 - Kişisel Verilerin Korunması (KVKK):</strong> Hizmet Alan'ın paylaştığı iletişim ve fatura verileri 6698 sayılı KVKK kapsamında yalnızca organizasyon ve yasal muhasebe süreçleri için işlenir.</p>
<p><strong>Madde 12 - Yetkili Mahkeme ve İcra Daireleri:</strong> İşbu 12 maddeden ve 3 sayfadan ibaret sözleşmenin uygulanmasından doğabilecek her türlü ihtilafta Sakarya Mahkemeleri ve İcra Daireleri yetkilidir.</p>
          `;

          await pool.query(`
            INSERT INTO company_settings (
              id, company_name, brand_title, address, tax_office, tax_number, phone, email, website, authorized_person, bank_info, contract_title, contract_terms_full
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
          `, [
            'default',
            'İrem Düğün Sarayı Ltd. Şti.',
            'Organizasyon & Kiralama Şirketi | Sapanca Göl Kenarı, Sakarya',
            'Sapanca Göl Kenarı No: 45, Sapanca / Sakarya',
            'Sapanca Vergi Dairesi',
            '4820192837',
            '+90 532 111 2233',
            'bilgi@iremdugunsarayi.com',
            'https://irem.portegu.com',
            'Davut Akbulut (Genel Müdür)',
            'Garanti BBVA - TR12 0006 2000 0001 2345 6789 01 (Alıcı: İrem Düğün Sarayı Ltd. Şti.)',
            'DÜĞÜN SALONU KİRALAMA & ETKİNLİK SÖZLEŞMESİ',
            defaultTerms.trim()
          ]);
        }
      } catch(e){}
"""

# Insert table creation into server.js
if "CREATE TABLE IF NOT EXISTS company_settings" not in server_code:
    pos = server_code.find("CREATE TABLE IF NOT EXISTS venues (")
    if pos != -1:
        server_code = server_code[:pos] + company_table_sql + "\n\n        " + server_code[pos:]

# Add Endpoints GET /api/company-settings & POST /api/company-settings
company_endpoints = """
// -------------------------------------------------------------
// 12. ŞİRKET BİLGİLERİ VE RESMİ SÖZLEŞME METİNLERİ ENDPOINTS
// -------------------------------------------------------------
app.get('/api/company-settings', async (req, res) => {
  const activePool = await getPool();
  if (activePool) {
    try {
      const [rows] = await activePool.query("SELECT * FROM company_settings WHERE id = 'default'");
      if (rows && rows.length > 0) {
        return res.json(rows[0]);
      }
    } catch(e) {
      console.error('MySQL GET /api/company-settings error:', e.message);
    }
  }
  res.json({
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
  });
});

app.post('/api/company-settings', async (req, res) => {
  const activePool = await getPool();
  const data = req.body || {};
  const item = {
    id: 'default',
    company_name: data.company_name || data.companyName || 'İrem Düğün Sarayı Ltd. Şti.',
    brand_title: data.brand_title || data.brandTitle || 'Organizasyon & Kiralama Şirketi | Sapanca Göl Kenarı, Sakarya',
    address: data.address || 'Sapanca Göl Kenarı No: 45, Sapanca / Sakarya',
    tax_office: data.tax_office || data.taxOffice || 'Sapanca Vergi Dairesi',
    tax_number: data.tax_number || data.taxNumber || '4820192837',
    phone: data.phone || '+90 532 111 2233',
    email: data.email || 'bilgi@iremdugunsarayi.com',
    website: data.website || 'https://irem.portegu.com',
    authorized_person: data.authorized_person || data.authorizedPerson || 'Davut Akbulut',
    bank_info: data.bank_info || data.bankInfo || '',
    contract_title: data.contract_title || data.contractTitle || 'DÜĞÜN SALONU KİRALAMA & ETKİNLİK SÖZLEŞMESİ',
    contract_terms_full: data.contract_terms_full || data.contractTermsFull || ''
  };

  if (activePool) {
    try {
      await activePool.query(`
        INSERT INTO company_settings (
          id, company_name, brand_title, address, tax_office, tax_number, phone, email, website, authorized_person, bank_info, contract_title, contract_terms_full
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON DUPLICATE KEY UPDATE
          company_name=?, brand_title=?, address=?, tax_office=?, tax_number=?, phone=?, email=?, website=?, authorized_person=?, bank_info=?, contract_title=?, contract_terms_full=?
      `, [
        item.id, item.company_name, item.brand_title, item.address, item.tax_office, item.tax_number, item.phone, item.email, item.website, item.authorized_person, item.bank_info, item.contract_title, item.contract_terms_full,
        item.company_name, item.brand_title, item.address, item.tax_office, item.tax_number, item.phone, item.email, item.website, item.authorized_person, item.bank_info, item.contract_title, item.contract_terms_full
      ]);
    } catch(e) {
      console.error('MySQL POST /api/company-settings error:', e.message);
    }
  }
  res.json({ success: true, item });
});
"""

if "app.get('/api/company-settings'" not in server_code:
    pos = server_code.find("app.get('/api/backup'")
    if pos != -1:
        server_code = server_code[:pos] + company_endpoints + "\n\n" + server_code[pos:]
    else:
        server_code += "\n\n" + company_endpoints

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(server_code)

print("Updated server.js with company settings table & endpoints successfully!")
