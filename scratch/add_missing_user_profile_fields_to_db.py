import os, re

# 1. UPDATE server.js SCHEMA & API ENDPOINTS
with open('server.js', 'r', encoding='utf-8') as f:
    server_code = f.read()

# Update CREATE TABLE users schema
old_users_schema = """        CREATE TABLE IF NOT EXISTS users (
          id VARCHAR(50) PRIMARY KEY,
          name VARCHAR(150) NOT NULL,
          email VARCHAR(150),
          password_hash VARCHAR(255),
          role VARCHAR(50) DEFAULT 'admin',
          avatar TEXT,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"""

new_users_schema = """        CREATE TABLE IF NOT EXISTS users (
          id VARCHAR(50) PRIMARY KEY,
          name VARCHAR(150) NOT NULL,
          email VARCHAR(150),
          phone VARCHAR(50),
          password_hash VARCHAR(255),
          role VARCHAR(50) DEFAULT 'admin',
          avatar LONGTEXT,
          notify_whatsapp TINYINT(1) DEFAULT 1,
          notify_email TINYINT(1) DEFAULT 1,
          notify_sms TINYINT(1) DEFAULT 0,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

        try { await pool.query("ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR(50)"); } catch(e){}
        try { await pool.query("ALTER TABLE users ADD COLUMN IF NOT EXISTS notify_whatsapp TINYINT(1) DEFAULT 1"); } catch(e){}
        try { await pool.query("ALTER TABLE users ADD COLUMN IF NOT EXISTS notify_email TINYINT(1) DEFAULT 1"); } catch(e){}
        try { await pool.query("ALTER TABLE users ADD COLUMN IF NOT EXISTS notify_sms TINYINT(1) DEFAULT 0"); } catch(e){}"""

if old_users_schema in server_code:
    server_code = server_code.replace(old_users_schema, new_users_schema)

# Update GET /api/users
old_get_users = "const [rows] = await pool.query('SELECT id, name, email, role, avatar, created_at FROM users ORDER BY created_at DESC');"
new_get_users = "const [rows] = await pool.query('SELECT id, name, email, phone, role, avatar, notify_whatsapp AS notifyWhatsapp, notify_email AS notifyEmail, notify_sms AS notifySms, created_at FROM users ORDER BY created_at DESC');"

if old_get_users in server_code:
    server_code = server_code.replace(old_get_users, new_get_users)

# Update POST /api/users
old_post_users = """app.post('/api/users', async (req, res) => {
  const item = { id: req.body.id || ('u_' + Date.now()), ...req.body };
  if (pool) {
    try {
      await pool.query(
        'INSERT INTO users (id, name, email, password_hash, role, avatar) VALUES (?, ?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE name=?, email=?, role=?, avatar=?',
        [item.id, item.name, item.email, item.password || '123456', item.role || 'admin', item.avatar || '', item.name, item.email, item.role || 'admin', item.avatar || '']
      );
    } catch(e) {
      console.error('MySQL POST /api/users error:', e.message);
    }
  }
  res.status(201).json({ success: true, item });
});"""

new_post_users = """app.post('/api/users', async (req, res) => {
  const item = { id: req.body.id || ('u_' + Date.now()), ...req.body };
  if (pool) {
    try {
      await pool.query(
        `INSERT INTO users (id, name, email, phone, password_hash, role, avatar, notify_whatsapp, notify_email, notify_sms) 
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
         ON DUPLICATE KEY UPDATE name=?, email=?, phone=?, role=?, avatar=?, notify_whatsapp=?, notify_email=?, notify_sms=?`,
        [
          item.id, item.name, item.email || '', item.phone || '', item.password || '123456', item.role || 'admin', item.avatar || '',
          item.notifyWhatsapp ? 1 : 0, item.notifyEmail ? 1 : 0, item.notifySms ? 1 : 0,
          item.name, item.email || '', item.phone || '', item.role || 'admin', item.avatar || '',
          item.notifyWhatsapp ? 1 : 0, item.notifyEmail ? 1 : 0, item.notifySms ? 1 : 0
        ]
      );
    } catch(e) {
      console.error('MySQL POST /api/users error:', e.message);
    }
  }
  res.status(201).json({ success: true, item });
});"""

if old_post_users in server_code:
    server_code = server_code.replace(old_post_users, new_post_users)

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(server_code)

print("Successfully updated server.js with missing user fields (phone, notifyWhatsapp, notifyEmail, notifySms)!")

# 2. UPDATE ProfileComponent IN HTML FILES
html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update ProfileComponent notify states & payload
    old_profile_states = """      const [notifyWhatsapp, setNotifyWhatsapp] = useState(true);
      const [notifyEmail, setNotifyEmail] = useState(true);
      const [notifySms, setNotifySms] = useState(false);"""

    new_profile_states = """      const [notifyWhatsapp, setNotifyWhatsapp] = useState(currentUser?.notifyWhatsapp !== undefined ? currentUser.notifyWhatsapp : true);
      const [notifyEmail, setNotifyEmail] = useState(currentUser?.notifyEmail !== undefined ? currentUser.notifyEmail : true);
      const [notifySms, setNotifySms] = useState(currentUser?.notifySms !== undefined ? currentUser.notifySms : false);"""

    old_profile_payload = """        const profilePayload = {
          name,
          email,
          phone,
          avatar,
          role: selectedRole
        };"""

    new_profile_payload = """        const profilePayload = {
          name,
          email,
          phone,
          avatar,
          role: selectedRole,
          notifyWhatsapp,
          notifyEmail,
          notifySms
        };"""

    if old_profile_states in content:
        content = content.replace(old_profile_states, new_profile_states)

    if old_profile_payload in content:
        content = content.replace(old_profile_payload, new_profile_payload)

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully updated {h_file}!")

print("All missing user profile fields added to database and synchronized!")
