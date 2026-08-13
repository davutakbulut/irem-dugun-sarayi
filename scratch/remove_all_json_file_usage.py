import os, glob

# 1. REMOVE readDbFile and saveDbFile from server.js
with open('server.js', 'r', encoding='utf-8') as f:
    server_code = f.read()

# Replace readDbFile & saveDbFile definition
old_helpers = """// JSON DB Dosyaları Okuma/Yazma Yardımcıları
const readDbFile = (fileName, fallback) => {
  try {
    const filePath = path.join(__dirname, 'scratch', fileName);
    if (fs.existsSync(filePath)) {
      const data = fs.readFileSync(filePath, 'utf8');
      const parsed = JSON.parse(data);
      if (parsed) return parsed;
    }
  } catch(e) {
    console.error('Error loading ' + fileName + ':', e.message);
  }
  return fallback;
};

const saveDbFile = (fileName, data) => {
  // Disksel JSON yerel dosya kaydı kapalı - Veriler %100 canlı MySQL/MariaDB veritabanında saklanır.
};"""

new_helpers = """// DISKSEL JSON YEREL DOSYA KULLANIMI TAMAMEN KALDIRILDI
// Tüm sistem verileri %100 CANLI MySQL / MariaDB veritabanından okunur ve veritabanına yazılır."""

if old_helpers in server_code:
    server_code = server_code.replace(old_helpers, new_helpers)

# Remove any saveDbFile(...) calls
server_code = server_code.replace("saveDbFile('db_reservations.json', memoryStore.reservations);", "// %100 MySQL Veritabanına kaydedilir")
server_code = server_code.replace("saveDbFile('db_media.json', memoryStore.media);", "// %100 MySQL Veritabanına kaydedilir")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(server_code)

print("Successfully cleaned up JSON file helpers from server.js!")

# 2. DELETE ALL scratch/db_*.json files
json_files = glob.glob('scratch/db_*.json') + glob.glob('scratch/*.json')
deleted_count = 0
for jf in json_files:
    if os.path.exists(jf):
        try:
            os.remove(jf)
            deleted_count += 1
            print(f"Deleted JSON file: {jf}")
        except Exception as e:
            print(f"Error deleting {jf}: {e}")

print(f"Deleted {deleted_count} JSON database files from scratch directory.")
