with open('server.js', 'r', encoding='utf-8') as f:
    code = f.read()

old_endpoints = """// -------------------------------------------------------------
// 6. GİDERLER ENDPOINTS (/api/expenses)
// -------------------------------------------------------------
app.get('/api/expenses', async (req, res) => {
  if (pool) {
    try {
      const [rows] = await pool.query('SELECT * FROM expenses ORDER BY date DESC');
      const formatted = (rows || []).map(r => ({
        ...r,
        amount: Number(r.amount || 0),
        date: r.date ? (r.date instanceof Date ? r.date.toISOString().split('T')[0] : String(r.date).split('T')[0]) : ''
      }));
      return res.json(formatted);
    } catch(e) {
      console.error('MySQL GET /api/expenses error:', e.message);
    }
  }
  res.json([]);
});

app.post('/api/expenses', async (req, res) => {
  const item = { id: req.body.id || ('exp-' + Date.now()), ...req.body };
  if (pool) {
    try {
      await pool.query(
        'INSERT INTO expenses (id, title, category, amount, date, description, type) VALUES (?, ?, ?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE title=?, category=?, amount=?, date=?, description=?, type=?',
        [item.id, item.title, item.category || 'Genel', item.amount || 0, item.date || new Date().toISOString().split('T')[0], item.description || '', item.type || 'expense', item.title, item.category || 'Genel', item.amount || 0, item.date || new Date().toISOString().split('T')[0], item.description || '', item.type || 'expense']
      );
    } catch(e) {
      console.error('MySQL POST /api/expenses error:', e.message);
    }
  }
  res.status(201).json({ success: true, item });
});

app.delete('/api/expenses/:id', async (req, res) => {
  const { id } = req.params;
  if (pool) {
    try {
      await pool.query('DELETE FROM expenses WHERE id = ?', [id]);
    } catch(e) {
      console.error('MySQL DELETE /api/expenses error:', e.message);
    }
  }
  res.json({ success: true, id });
});"""

new_endpoints = """// -------------------------------------------------------------
// 6. GİDERLER ENDPOINTS (/api/expenses)
// -------------------------------------------------------------
app.get('/api/expenses', async (req, res) => {
  try {
    const activePool = await getPool();
    if (activePool) {
      const [rows] = await activePool.query('SELECT * FROM expenses ORDER BY date DESC, created_at DESC');
      const formatted = (rows || []).map(r => ({
        ...r,
        amount: Number(r.amount || 0),
        date: r.date ? (typeof r.date === 'string' ? r.date.split('T')[0] : (r.date instanceof Date ? `${r.date.getFullYear()}-${String(r.date.getMonth()+1).padStart(2,'0')}-${String(r.date.getDate()).padStart(2,'0')}` : String(r.date).split('T')[0])) : ''
      }));
      return res.json(formatted);
    }
  } catch(e) {
    console.error('MySQL GET /api/expenses error:', e.message);
  }
  res.json(memoryStore.expenses || []);
});

app.post('/api/expenses', async (req, res) => {
  try {
    const item = { id: req.body.id || ('exp-' + Date.now()), ...req.body };
    const cleanDate = item.date || new Date().toISOString().split('T')[0];
    const activePool = await getPool();
    if (activePool) {
      await activePool.query(
        `INSERT INTO expenses (id, title, category, amount, date, description, type)
         VALUES (?, ?, ?, ?, ?, ?, ?)
         ON DUPLICATE KEY UPDATE title=VALUES(title), category=VALUES(category), amount=VALUES(amount), date=VALUES(date), description=VALUES(description), type=VALUES(type)`,
        [item.id, item.title, item.category || 'Genel', Number(item.amount || 0), cleanDate, item.description || '', item.type || 'expense']
      );
      console.log(`💾 Gider [${item.id}] MariaDB Veritabanına Yazıldı: ${item.title} (${item.amount} TL)`);
    }
    
    // Update memoryStore
    memoryStore.expenses = [item, ...(memoryStore.expenses || []).filter(e => e.id !== item.id)];
    res.status(201).json({ success: true, item });
  } catch(e) {
    console.error('MySQL POST /api/expenses error:', e.message);
    res.status(500).json({ error: 'Gider kaydedilemedi', message: e.message });
  }
});

app.delete('/api/expenses/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const activePool = await getPool();
    if (activePool) {
      await activePool.query('DELETE FROM expenses WHERE id = ?', [id]);
      console.log(`🗑️ Gider [${id}] MariaDB Veritabanından Silindi.`);
    }
    memoryStore.expenses = (memoryStore.expenses || []).filter(e => e.id !== id);
    res.json({ success: true, id });
  } catch(e) {
    console.error('MySQL DELETE /api/expenses error:', e.message);
    res.status(500).json({ error: 'Gider silinemedi', message: e.message });
  }
});"""

if old_endpoints in code:
    code = code.replace(old_endpoints, new_endpoints)
    with open('server.js', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Upgraded /api/expenses in server.js!")
else:
    print("old_endpoints not found in server.js")
