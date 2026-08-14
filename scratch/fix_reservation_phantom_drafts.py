import os

# 1. UPDATE server.js: Exclude drafts and auto-delete phantom drafts on boot
with open('server.js', 'r', encoding='utf-8') as f:
    server_code = f.read()

# In table init, add cleanup for phantom drafts
clean_sql = """
      // Purge any phantom / auto-saved draft rows from real reservations
      try {
        await pool.query("DELETE FROM reservations WHERE id LIKE 'RES-DRAFT-%' OR customer_name = 'İsimsiz Müşteri' OR notes LIKE '%AUTO_SAVE%'");
      } catch(e){}
"""

if "Purge any phantom / auto-saved draft rows" not in server_code:
    pos = server_code.find("console.log('⚡ MariaDB Verileri Belleğe Senkronize Edildi!');")
    if pos != -1:
        server_code = server_code[:pos] + clean_sql + "\n      " + server_code[pos:]

# In GET /api/reservations, filter out drafts
old_get_res_query = "const [rows] = await activePool.query('SELECT * FROM reservations ORDER BY date ASC');"
new_get_res_query = "const [rows] = await activePool.query(\"SELECT * FROM reservations WHERE id NOT LIKE 'RES-DRAFT-%' AND customer_name != 'İsimsiz Müşteri' AND (is_draft = 0 OR is_draft IS NULL) ORDER BY date ASC\");"

if old_get_res_query in server_code:
    server_code = server_code.replace(old_get_res_query, new_get_res_query)

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(server_code)

print("Updated server.js to exclude and purge phantom drafts!")

# 2. UPDATE HTML files:
html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace hardcoded 2026-08-25 with dynamic todayDateStr in CreateReservationPageComponent
    old_start_date_init = "const [startDate, setStartDate] = useState(prefilledDate || '2026-08-25');"
    new_start_date_init = "const [startDate, setStartDate] = useState(prefilledDate || todayDateStr);"

    old_end_date_init = "const [endDate, setEndDate] = useState(prefilledDate || '2026-08-25');"
    new_end_date_init = "const [endDate, setEndDate] = useState(prefilledDate || todayDateStr);"

    content = content.replace(old_start_date_init, new_start_date_init)
    content = content.replace(old_end_date_init, new_end_date_init)

    # In collision check, ignore any draft reservation
    old_conflict_check = """          if (editingResFromUrl && (r.id === editingResFromUrl.id || r.mediaKey === editingResFromUrl.mediaKey || (editingResFromUrl.refKey && r.refKey === editingResFromUrl.refKey))) {
            return false;
          }
          if (activeRefKey && r.refKey === activeRefKey) {
            return false;
          }"""

    new_conflict_check = """          if (r.id && r.id.startsWith('RES-DRAFT-')) return false;
          if (r.isDraft || r.status === 'DRAFT' || r.customerName === 'İsimsiz Müşteri') return false;
          if (editingResFromUrl && (r.id === editingResFromUrl.id || r.mediaKey === editingResFromUrl.mediaKey || (editingResFromUrl.refKey && r.refKey === editingResFromUrl.refKey))) {
            return false;
          }
          if (activeRefKey && r.refKey === activeRefKey) {
            return false;
          }"""

    if old_conflict_check in content:
        content = content.replace(old_conflict_check, new_conflict_check)
        print(f"Updated conflict check in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully processed {h_file}!")

print("Reservation collision logic and phantom draft elimination completed!")
