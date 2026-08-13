with open('server.js', 'r', encoding='utf-8') as f:
    code = f.read()

bad_sql_block = """        CREATE TABLE IF NOT EXISTS users (
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
        try { await pool.query("ALTER TABLE users ADD COLUMN IF NOT EXISTS notify_sms TINYINT(1) DEFAULT 0"); } catch(e){}
      `);"""

good_sql_block = """        CREATE TABLE IF NOT EXISTS users (
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
      `);

      try { await pool.query("ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR(50)"); } catch(e){}
      try { await pool.query("ALTER TABLE users ADD COLUMN IF NOT EXISTS notify_whatsapp TINYINT(1) DEFAULT 1"); } catch(e){}
      try { await pool.query("ALTER TABLE users ADD COLUMN IF NOT EXISTS notify_email TINYINT(1) DEFAULT 1"); } catch(e){}
      try { await pool.query("ALTER TABLE users ADD COLUMN IF NOT EXISTS notify_sms TINYINT(1) DEFAULT 0"); } catch(e){}"""

if bad_sql_block in code:
    code = code.replace(bad_sql_block, good_sql_block)
    with open('server.js', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Successfully fixed SQL syntax in server.js!")
else:
    print("bad_sql_block not found!")
