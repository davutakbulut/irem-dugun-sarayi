import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update reader.onload inside MediaComponent to call /api/upload-media API and save physical file to disk
old_reader = """        const reader = new FileReader();
        reader.onload = (e) => {
          const fileDataUrl = e.target.result;
          const newMediaId = 'mf_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4);

          const newMediaObj = {
            id: newMediaId,
            type: pendingItem.type,
            url: fileDataUrl,
            thumbnail: fileDataUrl,
            fileName: pendingItem.name,
            fileSize: pendingItem.rawSize,
            fingerprint: pendingItem.fingerprint,
            uploaderName: isPublicGuestMode ? 'Davetli Konuk' : 'İşletme Yetkilisi',
            tableNo: 'Masa Davetlisi',
            timestamp: new Date().toISOString().replace('T', ' ').substr(0, 16),
            isGuest: isPublicGuestMode,
            uploaderIp: '195.175.22.' + Math.floor(Math.random() * 50 + 1)
          };"""

new_reader = """        const reader = new FileReader();
        reader.onload = async (e) => {
          const fileDataUrl = e.target.result;
          const targetResKey = activeMediaKey || currentRes?.mediaKey || currentRes?.id || selectedResKey || 'GENERAL';

          let finalMediaUrl = fileDataUrl;

          // PHYSICAL DISK STORAGE API INTEGRATION: Save physical file to uploads/<res_id>/<file_name> on server disk
          try {
            const apiRes = await fetch('/api/upload-media', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                resId: targetResKey,
                fileName: pendingItem.name,
                fileData: fileDataUrl
              })
            });
            if (apiRes.ok) {
              const apiData = await apiRes.json();
              if (apiData.success && apiData.url) {
                finalMediaUrl = apiData.url;
              }
            }
          } catch(err) {
            console.warn('Physical disk upload API fallback:', err);
          }

          const newMediaId = 'mf_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4);

          const newMediaObj = {
            id: newMediaId,
            type: pendingItem.type,
            url: finalMediaUrl,
            thumbnail: finalMediaUrl,
            fileName: pendingItem.name,
            fileSize: pendingItem.rawSize,
            fingerprint: pendingItem.fingerprint,
            uploaderName: isPublicGuestMode ? 'Davetli Konuk' : 'İşletme Yetkilisi',
            tableNo: 'Masa Davetlisi',
            timestamp: new Date().toISOString().replace('T', ' ').substr(0, 16),
            isGuest: isPublicGuestMode,
            uploaderIp: '195.175.22.' + Math.floor(Math.random() * 50 + 1)
          };"""

if old_reader in html:
    html = html.replace(old_reader, new_reader)
    print("Integrated Physical Disk Upload API into MediaComponent!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html disk upload integration successfully!")
