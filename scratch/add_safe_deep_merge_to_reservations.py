with open('server.js', 'r', encoding='utf-8') as f:
    code = f.read()

old_post_block = """app.post('/api/reservations', async (req, res) => {
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

  const activePool = await getPool();"""

new_post_block = """app.post('/api/reservations', async (req, res) => {
  let item = { ...req.body };
  if (!item.id || item.id.startsWith('RES-DRAFT-')) {
    item.id = `RES-${new Date().getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`;
  }
  item.status = 'CONFIRMED';
  item.isDraft = false;
  item.paymentStatus = item.paymentStatus || 'Kapora Alındı';

  const activePool = await getPool();
  
  // SAFE DEEP-MERGE: Preserve existing payments, customExpenses, mediaFiles, notesHistory
  if (activePool && item.id) {
    try {
      const [existingRows] = await activePool.query('SELECT details_json, media_json, selected_services_json, flow_plan_json FROM reservations WHERE id = ?', [item.id]);
      if (existingRows && existingRows.length > 0) {
        let existingDetails = {};
        if (existingRows[0].details_json) {
          try { existingDetails = typeof existingRows[0].details_json === 'string' ? JSON.parse(existingRows[0].details_json) : existingRows[0].details_json; } catch(e){}
        }
        item = {
          ...existingDetails,
          ...item,
          customExpenses: item.customExpenses !== undefined ? item.customExpenses : (existingDetails.customExpenses || []),
          payments: item.payments !== undefined ? item.payments : (existingDetails.payments || []),
          mediaFiles: (item.mediaFiles && item.mediaFiles.length > 0) ? item.mediaFiles : (existingDetails.mediaFiles || []),
          notesHistory: item.notesHistory !== undefined ? item.notesHistory : (existingDetails.notesHistory || []),
          flowPlan: item.flowPlan !== undefined ? item.flowPlan : (existingDetails.flowPlan || []),
          selectedServices: item.selectedServices !== undefined ? item.selectedServices : (existingDetails.selectedServices || [])
        };
      }
    } catch(e) {
      console.warn('Deep-merge query warning:', e.message);
    }
  }

  const detailsJsonStr = JSON.stringify(item);
  const selectedServicesJsonStr = JSON.stringify(item.selectedServices || []);
  const flowPlanJsonStr = JSON.stringify(item.flowPlan || []);"""

if old_post_block in code:
    code = code.replace(old_post_block, new_post_block)
    with open('server.js', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Added safe deep-merge to POST /api/reservations in server.js!")
else:
    print("old_post_block not found in server.js")
