with open('server.js', 'r', encoding='utf-8') as f:
    code = f.read()

target = "try { await pool.query(\"ALTER TABLE reservations ADD COLUMN IF NOT EXISTS details_json LONGTEXT\"); } catch(e){}"
addition = """try { await pool.query("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS details_json LONGTEXT"); } catch(e){}
      try { await pool.query("ALTER TABLE services ADD COLUMN IF NOT EXISTS cost_price DECIMAL(12,2) DEFAULT 0"); } catch(e){}
      try { await pool.query("ALTER TABLE services MODIFY COLUMN pricing_type VARCHAR(50) DEFAULT 'fixed'"); } catch(e){}"""

if target in code and "ALTER TABLE services ADD COLUMN IF NOT EXISTS cost_price" not in code:
    code = code.replace(target, addition)
    with open('server.js', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Added ALTER TABLE services into initMysql in server.js")
else:
    print("Already exists or target not found")
