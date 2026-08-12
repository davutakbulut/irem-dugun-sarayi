import os

# 1. FIX server.js /api/roles ENDPOINT TO RETURN DICTIONARY/MAP OBJECT OR ARRAY ACCORDING TO FRONTEND Standard
with open('server.js', 'r', encoding='utf-8') as f:
    server_code = f.read()

old_get_roles = """app.get('/api/roles', async (req, res) => {
  if (pool) {
    try {
      const [rows] = await pool.query('SELECT * FROM roles');
      const formatted = (rows || []).map(r => ({
        ...r,
        permissions: r.permissions_json ? (typeof r.permissions_json === 'string' ? JSON.parse(r.permissions_json) : r.permissions_json) : []
      }));
      return res.json(formatted);
    } catch(e) {
      console.error('MySQL GET /api/roles error:', e.message);
    }
  }
  res.json([]);
});"""

new_get_roles = """app.get('/api/roles', async (req, res) => {
  if (pool) {
    try {
      const [rows] = await pool.query('SELECT * FROM roles');
      const mapObj = {};
      (rows || []).forEach(r => {
        if (r.id) mapObj[r.id] = r.name || r.id;
      });
      if (Object.keys(mapObj).length > 0) {
        return res.json(mapObj);
      }
    } catch(e) {
      console.error('MySQL GET /api/roles error:', e.message);
    }
  }
  res.json({
    admin: 'Sistem Yöneticisi',
    satisci: 'Satış Danışmanı',
    sosyal_medyaci: 'Sosyal Medya Sorumlusu',
    musteri: 'Müşteri Portalı'
  });
});"""

if old_get_roles in server_code:
    server_code = server_code.replace(old_get_roles, new_get_roles)
    with open('server.js', 'w', encoding='utf-8') as f:
        f.write(server_code)
    print("Successfully updated /api/roles in server.js!")

# 2. UPDATE FRONTEND FETCH & COMPONENT ROLES HANDLERS ACROSS ALL HTML FILES
files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for f_path in files:
    if not os.path.exists(f_path):
        continue
    with open(f_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Safely convert roles data if array is received from backend
    old_fetch_roles = """            // Fetch Roles
            fetchFn('/api/roles')
              .then(res => res.json())
              .then(data => {
                if (Array.isArray(data)) {
                  lastSyncedRolesRef.current = JSON.stringify(data);
                  setRolesState(data);
                }
              })
              .catch(() => {});"""

    new_fetch_roles = """            // Fetch Roles
            fetchFn('/api/roles')
              .then(res => res.json())
              .then(data => {
                if (data && typeof data === 'object') {
                  let roleObj = data;
                  if (Array.isArray(data)) {
                    roleObj = {};
                    data.forEach(r => {
                      if (r && r.id) roleObj[r.id] = r.name || r.id;
                    });
                  }
                  lastSyncedRolesRef.current = JSON.stringify(roleObj);
                  setRolesState(roleObj);
                }
              })
              .catch(() => {});"""

    if old_fetch_roles in content:
        content = content.replace(old_fetch_roles, new_fetch_roles)

    # Safely convert public settings roles data if array is received
    old_ps_roles = """                  if (Array.isArray(data.roles) && data.roles.length > 0) {
                    lastSyncedRolesRef.current = JSON.stringify(data.roles);
                    setRolesState(data.roles);
                  }"""

    new_ps_roles = """                  if (data.roles && typeof data.roles === 'object') {
                    let roleObj = data.roles;
                    if (Array.isArray(data.roles)) {
                      roleObj = {};
                      data.roles.forEach(r => {
                        if (r && r.id) roleObj[r.id] = r.name || r.id;
                      });
                    }
                    lastSyncedRolesRef.current = JSON.stringify(roleObj);
                    setRolesState(roleObj);
                  }"""

    if old_ps_roles in content:
        content = content.replace(old_ps_roles, new_ps_roles)

    with open(f_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully updated role handling in {f_path}!")

print("Role object invariant fix finished!")
