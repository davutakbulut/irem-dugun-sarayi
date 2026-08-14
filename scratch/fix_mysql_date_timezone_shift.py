import os

with open('server.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add dateStrings: true to mysql.createPool
old_pool_opts = """      const testPool = mysql.createPool({
        host: host,
        port: (process.env.DB_PORT || process.env.MYSQL_PORT) ? Number(process.env.DB_PORT || process.env.MYSQL_PORT) : 3306,
        user: 'kullaniciadi_irem_dugun_db',
        password: 'Akblt_157',
        database: 'irem_dugun_db',
        waitForConnections: true,
        connectionLimit: 10,
        queueLimit: 0,
        connectTimeout: 5000
      });"""

new_pool_opts = """      const testPool = mysql.createPool({
        host: host,
        port: (process.env.DB_PORT || process.env.MYSQL_PORT) ? Number(process.env.DB_PORT || process.env.MYSQL_PORT) : 3306,
        user: 'kullaniciadi_irem_dugun_db',
        password: 'Akblt_157',
        database: 'irem_dugun_db',
        dateStrings: true,
        waitForConnections: true,
        connectionLimit: 10,
        queueLimit: 0,
        connectTimeout: 5000
      });"""

if old_pool_opts in code:
    code = code.replace(old_pool_opts, new_pool_opts)
    print("Added dateStrings: true to mysql.createPool in server.js")

# 2. Fix date parsing helper in GET /api/reservations
old_date_parse = """        const rawDate = r.event_date ? (r.event_date instanceof Date ? r.event_date.toISOString().split('T')[0] : String(r.event_date).split('T')[0]) : '';
        const rawEndDate = r.end_date ? (r.end_date instanceof Date ? r.end_date.toISOString().split('T')[0] : String(r.end_date).split('T')[0]) : rawDate;"""

new_date_parse = """        const formatMySqlDate = (d) => {
          if (!d) return '';
          if (typeof d === 'string') return d.split('T')[0];
          if (d instanceof Date) {
            const yr = d.getFullYear();
            const mo = String(d.getMonth() + 1).padStart(2, '0');
            const day = String(d.getDate()).padStart(2, '0');
            return `${yr}-${mo}-${day}`;
          }
          return String(d).split('T')[0];
        };
        const rawDate = formatMySqlDate(r.event_date);
        const rawEndDate = formatMySqlDate(r.end_date) || rawDate;"""

if old_date_parse in code:
    code = code.replace(old_date_parse, new_date_parse)
    print("Updated date formatting helper in GET /api/reservations in server.js")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved server.js with precise date timezone handling!")
