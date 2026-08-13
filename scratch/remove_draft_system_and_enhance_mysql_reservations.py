import os, re

# 1. UPDATE server.js: ALTER TABLE, API ENDPOINTS, AND ELIMINATE DRAFT ENDPOINTS
with open('server.js', 'r', encoding='utf-8') as f:
    server_code = f.read()

# Add ALTER TABLE column additions for reservations in server.js
alter_queries = """
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS secondary_phone VARCHAR(50)"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS end_date DATE"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS start_time VARCHAR(20)"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS end_time VARCHAR(20)"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS custom_venue_price DECIMAL(12,2)"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS referrer_name VARCHAR(150)"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS dip_discount_type VARCHAR(50)"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS tc_no VARCHAR(20)"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS vkn_no VARCHAR(20)"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS tax_office VARCHAR(150)"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS invoice_address TEXT"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS flow_plan_json LONGTEXT"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS selected_services_json LONGTEXT"); } catch(e){}
      try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS details_json LONGTEXT"); } catch(e){}
      try { await pool.query("UPDATE reservations SET status = 'CONFIRMED' WHERE status = 'DRAFT'"); } catch(e){}
"""

# Insert ALTER queries right after CREATE TABLE reservations block
create_res_pos = server_code.find("CREATE TABLE IF NOT EXISTS reservations (")
if create_res_pos != -1:
    create_res_end = server_code.find("ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;", create_res_pos)
    if create_res_end != -1:
        insert_pos = server_code.find("`);", create_res_end) + 3
        if alter_queries.strip() not in server_code:
            server_code = server_code[:insert_pos] + "\n" + alter_queries + "\n" + server_code[insert_pos:]

# Update GET /api/reservations
new_get_reservations = """app.get('/api/reservations', async (req, res) => {
  try {
    const activePool = await getPool();
    if (activePool) {
      const [rows] = await activePool.query("SELECT * FROM reservations ORDER BY created_at DESC");
      const formatted = (rows || []).map(r => {
        let detailsObj = {};
        if (r.details_json) {
          try { detailsObj = JSON.parse(r.details_json); } catch(e){}
        }
        let selectedServicesArr = [];
        if (r.selected_services_json) {
          try { selectedServicesArr = JSON.parse(r.selected_services_json); } catch(e){}
        }
        let flowPlanArr = [];
        if (r.flow_plan_json) {
          try { flowPlanArr = JSON.parse(r.flow_plan_json); } catch(e){}
        }
        let parsedMedia = [];
        if (r.media_json) {
          try { parsedMedia = JSON.parse(r.media_json); } catch(e){}
        }

        const rawDate = r.event_date ? (r.event_date instanceof Date ? r.event_date.toISOString().split('T')[0] : String(r.event_date).split('T')[0]) : '';
        const rawEndDate = r.end_date ? (r.end_date instanceof Date ? r.end_date.toISOString().split('T')[0] : String(r.end_date).split('T')[0]) : rawDate;

        return {
          ...detailsObj,
          id: r.id,
          venueId: r.venue_id || detailsObj.venueId || 'v1',
          customerId: r.customer_id || detailsObj.customerId || '',
          customerName: r.customer_name || detailsObj.customerName || 'Misafir',
          customerEmail: r.customer_email || detailsObj.customerEmail || '',
          customerPhone: r.customer_phone || detailsObj.customerPhone || '',
          secondaryPhone: r.secondary_phone || detailsObj.secondaryPhone || '',
          date: rawDate,
          eventDate: rawDate,
          startDate: rawDate,
          endDate: rawEndDate,
          startTime: r.start_time || detailsObj.startTime || '18:00',
          endTime: r.end_time || detailsObj.endTime || '23:00',
          timeSlot: r.time_slot || detailsObj.timeSlot || '18:00 - 23:00',
          guestCount: String(r.guest_count || detailsObj.guestCount || 0),
          venuePrice: Number(r.venue_price || detailsObj.venuePrice || 0),
          customVenuePrice: Number(r.custom_venue_price || detailsObj.customVenuePrice || r.venue_price || 0),
          subtotal: Number(r.subtotal || detailsObj.subtotal || 0),
          referrerName: r.referrer_name || detailsObj.referrerName || '',
          campaignCode: r.campaign_code || detailsObj.campaignCode || '',
          discountAmount: Number(r.discount_amount || detailsObj.discountAmount || 0),
          dipDiscountType: r.dip_discount_type || detailsObj.dipDiscountType || 'amount',
          vatAmount: Number(r.vat_amount || detailsObj.vatAmount || 0),
          totalAmount: Number(r.total_amount || detailsObj.totalAmount || 0),
          depositPaid: Number(r.deposit_paid || detailsObj.depositPaid || 0),
          remainingBalance: Number(r.remaining_balance || detailsObj.remainingBalance || 0),
          paymentStatus: r.payment_status || 'Kapora Alındı',
          isInvoiced: Boolean(r.is_invoiced),
          invoiceType: r.invoice_type || detailsObj.invoiceType || 'individual',
          tcNo: r.tc_no || detailsObj.tcNo || '',
          vknNo: r.vkn_no || detailsObj.vknNo || '',
          taxOffice: r.tax_office || detailsObj.taxOffice || '',
          invoiceAddress: r.invoice_address || detailsObj.invoiceAddress || '',
          notes: r.notes || detailsObj.notes || '',
          selectedServices: selectedServicesArr.length > 0 ? selectedServicesArr : (detailsObj.selectedServices || []),
          flowPlan: flowPlanArr.length > 0 ? flowPlanArr : (detailsObj.flowPlan || []),
          createdBy: detailsObj.createdBy || { name: 'Sistem Yöneticisi' },
          mediaFiles: parsedMedia.length > 0 ? parsedMedia : (detailsObj.mediaFiles || []),
          status: r.status === 'DRAFT' ? 'CONFIRMED' : (r.status || 'CONFIRMED'),
          isDraft: false
        };
      });
      return res.json(formatted);
    }
    return res.json(memoryStore.reservations || []);
  } catch(e) {
    console.error('MySQL GET /api/reservations error:', e.message);
    return res.status(500).json({ error: e.message, poolActive: !!pool });
  }
});"""

get_res_start = server_code.find("app.get('/api/reservations',")
if get_res_start != -1:
    get_res_end = server_code.find("app.post('/api/reservations',", get_res_start)
    if get_res_end != -1:
        server_code = server_code[:get_res_start] + new_get_reservations + "\n\n" + server_code[get_res_end:]

# Update POST /api/reservations
new_post_reservations = """app.post('/api/reservations', async (req, res) => {
  const item = { ...req.body };
  if (!item.id || item.id.startsWith('RES-DRAFT-')) {
    item.id = `RES-${new Date().getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`;
  }
  item.status = 'CONFIRMED';
  item.isDraft = false;
  item.paymentStatus = item.paymentStatus || 'Kapora Alındı';

  const detailsJsonStr = JSON.stringify(item);
  const selectedServicesJsonStr = JSON.stringify(item.selectedServices || []);
  const flowPlanJsonStr = JSON.stringify(item.flowPlan || []);

  const activePool = await getPool();
  
  if (activePool) {
    try {
      const custId = item.customerId || (`cust-` + Date.now());
      if (item.customerName) {
        await activePool.query(
          `INSERT INTO customers (id, name, email, phone, address, tax_type, tc_no, vkn_no, tax_office)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
           ON DUPLICATE KEY UPDATE name=VALUES(name), phone=VALUES(phone), email=VALUES(email), address=VALUES(address)`,
          [custId, item.customerName, item.customerEmail || '', item.customerPhone || '', item.invoiceAddress || '', item.invoiceType || 'individual', item.tcNo || '', item.vknNo || '', item.taxOffice || '']
        );
      }

      const eventDate = item.eventDate || item.startDate || item.date || new Date().toISOString().split('T')[0];
      const endDate = item.endDate || eventDate;
      const startTime = item.startTime || '18:00';
      const endTime = item.endTime || '23:00';
      const timeSlot = item.timeSlot || `${startTime} - ${endTime}`;

      await activePool.query(
        `INSERT INTO reservations (
          id, venue_id, customer_id, customer_name, customer_email, customer_phone, secondary_phone,
          event_date, end_date, start_time, end_time, time_slot, guest_count,
          venue_price, custom_venue_price, subtotal, referrer_name, campaign_code,
          discount_amount, dip_discount_type, vat_amount, total_amount, deposit_paid, remaining_balance,
          payment_status, is_invoiced, invoice_type, tc_no, vkn_no, tax_office, invoice_address,
          notes, flow_plan_json, selected_services_json, details_json, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'CONFIRMED')
        ON DUPLICATE KEY UPDATE
          venue_id=VALUES(venue_id), customer_name=VALUES(customer_name), customer_email=VALUES(customer_email),
          customer_phone=VALUES(customer_phone), secondary_phone=VALUES(secondary_phone),
          event_date=VALUES(event_date), end_date=VALUES(end_date), start_time=VALUES(start_time), end_time=VALUES(end_time),
          time_slot=VALUES(time_slot), guest_count=VALUES(guest_count), venue_price=VALUES(venue_price),
          custom_venue_price=VALUES(custom_venue_price), subtotal=VALUES(subtotal), referrer_name=VALUES(referrer_name),
          campaign_code=VALUES(campaign_code), discount_amount=VALUES(discount_amount), dip_discount_type=VALUES(dip_discount_type),
          vat_amount=VALUES(vat_amount), total_amount=VALUES(total_amount), deposit_paid=VALUES(deposit_paid),
          remaining_balance=VALUES(remaining_balance), payment_status=VALUES(payment_status), is_invoiced=VALUES(is_invoiced),
          invoice_type=VALUES(invoice_type), tc_no=VALUES(tc_no), vkn_no=VALUES(vkn_no), tax_office=VALUES(tax_office),
          invoice_address=VALUES(invoice_address), notes=VALUES(notes), flow_plan_json=VALUES(flow_plan_json),
          selected_services_json=VALUES(selected_services_json), details_json=VALUES(details_json), status='CONFIRMED'`,
        [
          item.id, item.venueId || 'v1', custId, item.customerName || '', item.customerEmail || '', item.customerPhone || '', item.secondaryPhone || '',
          eventDate, endDate, startTime, endTime, timeSlot, Number(item.guestCount || 0),
          Number(item.venuePrice || 0), Number(item.customVenuePrice || item.venuePrice || 0), Number(item.subtotal || 0),
          item.referrerName || '', item.campaignCode || '', Number(item.discountAmount || 0), item.dipDiscountType || 'amount',
          Number(item.vatAmount || 0), Number(item.totalAmount || 0), Number(item.depositPaid || 0), Number(item.remainingBalance || 0),
          item.paymentStatus || 'Kapora Alındı', item.isInvoiced ? 1 : 0, item.invoiceType || 'individual',
          item.tcNo || '', item.vknNo || '', item.taxOffice || '', item.invoiceAddress || '',
          item.notes || '', flowPlanJsonStr, selectedServicesJsonStr, detailsJsonStr
        ]
      );
    } catch(e) {
      console.error('MySQL POST /api/reservations error:', e.message);
    }
  }

  const idx = memoryStore.reservations.findIndex(r => r.id === item.id);
  if (idx >= 0) {
    memoryStore.reservations[idx] = { ...memoryStore.reservations[idx], ...item };
  } else {
    memoryStore.reservations.unshift(item);
  }

  res.status(201).json({ success: true, id: item.id, item });
});"""

post_res_start = server_code.find("app.post('/api/reservations',")
if post_res_start != -1:
    post_res_end = server_code.find("const deleteDraftReservationHandler", post_res_start)
    if post_res_end == -1:
        post_res_end = server_code.find("app.delete('/api/reservations/:id'", post_res_start)
    if post_res_end != -1:
        server_code = server_code[:post_res_start] + new_post_reservations + "\n\n" + server_code[post_res_end:]

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(server_code)

print("Successfully updated server.js reservations API & schema!")

# 2. UPDATE FRONTEND HTML FILES TO REMOVE DRAFT PANEL AND DRAFT OPTION
html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove DRAFT PANEL block in ReservationListComponent
    dp_start = "{/* DRAFT / UNCOMPLETED RESERVATIONS DEDICATED PANEL (TOP OF PAGE) */}"
    if dp_start in content:
        p_start = content.find(dp_start)
        # Find ending of panel div
        p_end = content.find("</div>\n          </div>\n\n          {/* SEARCH, VENUE & DATE FILTERS BAR */}", p_start)
        if p_end == -1:
            p_end = content.find("{/* SEARCH, VENUE & DATE FILTERS BAR */}", p_start)
        if p_start != -1 and p_end != -1:
            content = content[:p_start] + content[p_end:]
            print(f"Successfully removed Draft Panel from {h_file}!")

    # Remove DRAFT option from filter dropdown in ReservationListComponent
    draft_opt_str = '<option value="DRAFT">'
    if draft_opt_str in content:
        o_start = content.find(draft_opt_str)
        o_end = content.find("</option>", o_start)
        if o_start != -1 and o_end != -1:
            content = content[:o_start] + content[o_end + 9:]
            print(f"Successfully removed Draft Option from dropdown in {h_file}!")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Draft removal updated for {h_file}!")

print("All draft removal and comprehensive database saving updates completed!")
