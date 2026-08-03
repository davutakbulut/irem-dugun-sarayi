const fs = require('fs');
const path = require('path');

const dbPath = path.join(__dirname, '../scratch/db_system_settings.json');

const ROLE_NAMES = {
  'admin': 'Admin (Yönetici)',
  'satisci': 'Satış Temsilcisi',
  'sosyal_medyaci': 'Sosyal Medya',
  'musteri': 'Müşteri'
};

const TAB_PERMISSIONS = {
  'dashboard': ['admin', 'satisci', 'sosyal_medyaci', 'musteri'],
  'create-reservation': ['admin', 'satisci'],
  'venues': ['admin', 'satisci'],
  'services': ['admin', 'satisci'],
  'reservations': ['admin', 'satisci'],
  'calendar': ['admin', 'satisci'],
  'campaigns': ['admin'],
  'finance': ['admin'],
  'customers': ['admin', 'satisci'],
  'users': ['admin'],
  'roles': ['admin'],
  'reports': ['admin'],
  'media': ['admin', 'sosyal_medyaci', 'musteri'],
  'profile': ['admin', 'satisci', 'sosyal_medyaci', 'musteri'],
  'mind-map': ['admin'],
  'settings': ['admin'],
  'settings-appearance': ['admin'],
  'settings-performance': ['admin'],
  'settings-rbac': ['admin'],
  'settings-indexing': ['admin'],
  'settings-errors': ['admin'],
  'system-guide': ['admin', 'satisci', 'sosyal_medyaci', 'musteri'],
  'simulasyon-404': ['admin', 'satisci', 'sosyal_medyaci', 'musteri'],
  'simulasyon-301': ['admin', 'satisci', 'sosyal_medyaci', 'musteri'],
  'simulasyon-403': ['admin', 'satisci', 'sosyal_medyaci', 'musteri'],
  'simulasyon-500': ['admin', 'satisci', 'sosyal_medyaci', 'musteri']
};

const INITIAL_USERS = [
  { id: 'u1', name: 'İrem Yılmaz (Admin)', email: 'admin@iremdugunsarayi.com', role: 'admin', avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80' },
  { id: 'u2', name: 'Canan Güneş (Satış Müdürü)', email: 'satis@iremdugunsarayi.com', role: 'satisci', avatar: 'https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=200&q=80' },
  { id: 'u3', name: 'Murat Arslan (Sosyal Medya)', email: 'sosyal@iremdugunsarayi.com', role: 'sosyal_medyaci', avatar: 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=200&q=80' },
  { id: 'u4', name: 'Ahmet Yılmaz (Müşteri)', email: 'ahmet.yilmaz@example.com', role: 'musteri', avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80' }
];

let db = {};
if (fs.existsSync(dbPath)) {
  try {
    db = JSON.parse(fs.readFileSync(dbPath, 'utf8'));
  } catch(e) {}
}

if (!db.roles) db.roles = ROLE_NAMES;
if (!db.tabPermissions) db.tabPermissions = TAB_PERMISSIONS;
if (!db.users || !db.users.length) db.users = INITIAL_USERS;

fs.writeFileSync(dbPath, JSON.stringify(db, null, 2), 'utf8');
console.log('✅ BACKEND DB ROLES, TAB PERMISSIONS & USERS SYNCED SUCCESSFUL!');
