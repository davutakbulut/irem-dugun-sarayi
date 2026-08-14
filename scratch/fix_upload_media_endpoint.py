with open('server.js', 'r', encoding='utf-8') as f:
    code = f.read()

old_block = """    let matchFound = false;
    memoryStore.reservations = memoryStore.reservations.map(r => {
      const isMatch = r.id === resId || r.mediaKey === resId || r.id === safeResId || r.mediaKey === safeMediaKey;
      if (isMatch) {
        matchFound = true;
        const existingList = r.mediaFiles || [];
        return {
          ...r,
          mediaFiles: [newMediaObj, ...existingList]
        };
      }
      return r;
    });

    if (pool) {
      try {
        const [targetRows] = await pool.query('SELECT id, media_json FROM reservations WHERE id = ? OR id = ?', [resId || safeResId, safeResId]);
        if (targetRows && targetRows.length > 0) {
          const currentMedia = targetRows[0].media_json ? (typeof targetRows[0].media_json === 'string' ? JSON.parse(targetRows[0].media_json) : targetRows[0].media_json) : [];
          const updatedMedia = [newMediaObj, ...currentMedia];
          await pool.query('UPDATE reservations SET media_json = ? WHERE id = ?', [JSON.stringify(updatedMedia), targetRows[0].id]);
          console.log(`💾 Rezervasyon [${targetRows[0].id}] Medyası MariaDB Veritabanına Yazıldı!`);
        }

        await pool.query(
          'INSERT INTO media (id, title, category, url, file_size) VALUES (?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE title=?, url=?',
          [newMediaObj.id, cleanFileName, safeResId, fileUrl, newMediaObj.fileSize, cleanFileName, fileUrl]
        );
      } catch (dbErr) {
        console.error('MySQL upload-media update error:', dbErr.message);
      }
    }"""

new_block = """    const safeMediaKey = (req.body.mediaKey || '').replace(/[^a-zA-Z0-9_-]/g, '_');
    let matchFound = false;
    memoryStore.reservations = memoryStore.reservations.map(r => {
      const isMatch = r.id === resId || r.mediaKey === resId || r.id === safeResId || (safeMediaKey && r.mediaKey === safeMediaKey);
      if (isMatch) {
        matchFound = true;
        const existingList = r.mediaFiles || [];
        return {
          ...r,
          mediaFiles: [newMediaObj, ...existingList]
        };
      }
      return r;
    });

    const activePool = await getPool();
    if (activePool) {
      try {
        const [targetRows] = await activePool.query('SELECT id, media_json FROM reservations WHERE id = ? OR id = ?', [resId || safeResId, safeResId]);
        if (targetRows && targetRows.length > 0) {
          const currentMedia = targetRows[0].media_json ? (typeof targetRows[0].media_json === 'string' ? JSON.parse(targetRows[0].media_json) : targetRows[0].media_json) : [];
          const updatedMedia = [newMediaObj, ...currentMedia];
          await activePool.query('UPDATE reservations SET media_json = ? WHERE id = ?', [JSON.stringify(updatedMedia), targetRows[0].id]);
          console.log(`💾 Rezervasyon [${targetRows[0].id}] Medyası MariaDB Veritabanına Yazıldı!`);
        }

        await activePool.query(
          'INSERT INTO media (id, title, category, url, file_size) VALUES (?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE title=?, url=?',
          [newMediaObj.id, cleanFileName, safeResId, fileUrl, newMediaObj.fileSize, cleanFileName, fileUrl]
        );
      } catch (dbErr) {
        console.error('MySQL upload-media update error:', dbErr.message);
      }
    }"""

if old_block in code:
    code = code.replace(old_block, new_block)
    with open('server.js', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Fixed upload-media safeMediaKey and activePool error in server.js!")
else:
    print("old_block not found in server.js")
