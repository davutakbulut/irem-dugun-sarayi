const mysql = require('mysql2/promise');
async function run() {
  const pool = mysql.createPool({
    host: process.env.DB_HOST || '213.159.6.158',
    user: process.env.DB_USER || 'irem_user',
    password: process.env.DB_PASSWORD || 'Irem_2026!Db',
    database: process.env.DB_NAME || 'irem_dugun_sarayi',
    waitForConnections: true,
    connectionLimit: 5
  });
  try {
    const [res] = await pool.query("DELETE FROM reservations WHERE id LIKE 'RES-DRAFT-%' OR customer_name = 'İsimsiz Müşteri' OR notes LIKE '%AUTO_SAVE%'");
    console.log('Cleaned draft reservations count:', res.affectedRows);
  } catch(e) {
    console.error('Error cleaning drafts:', e.message);
  } finally {
    await pool.end();
  }
}
run();
