import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Check if QrCodeIcon and JSZip are referenced or needed
print("Reading index.html for media expansion...")

# 1. Update INITIAL_RESERVATIONS to include mediaKey, mediaRetentionDays, and sample mediaFiles (photos & videos)
sample_media_res1 = """        mediaKey: 'MEDIA-8X92M1KP',
        mediaRetentionDays: 30,
        mediaFiles: [
          { id: 'mf1', type: 'image', url: 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=1200&q=80', thumbnail: 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=400&q=80', uploaderName: 'Davetli - Mehmet T.', tableNo: 'Masa 4', timestamp: '2026-08-15 20:14', isGuest: true, uploaderIp: '195.175.22.4' },
          { id: 'mf2', type: 'image', url: 'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&w=1200&q=80', thumbnail: 'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&w=400&q=80', uploaderName: 'Fotoğrafçı - Can S.', tableNo: 'Ana Sahne', timestamp: '2026-08-15 21:05', isGuest: false, uploaderIp: '195.175.22.1' },
          { id: 'mf3', type: 'video', url: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4', thumbnail: 'https://images.unsplash.com/photo-1537633552985-df8429e8048b?auto=format&fit=crop&w=400&q=80', uploaderName: 'Davetli - Elif K.', tableNo: 'Masa 8', timestamp: '2026-08-15 21:30', isGuest: true, uploaderIp: '195.175.22.12' },
          { id: 'mf4', type: 'image', url: 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&w=1200&q=80', thumbnail: 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&w=400&q=80', uploaderName: 'Davetli - Burak A.', tableNo: 'Masa 2', timestamp: '2026-08-15 22:00', isGuest: true, uploaderIp: '195.175.22.18' }
        ],"""

sample_media_res2 = """        mediaKey: 'MEDIA-7K34P9LV',
        mediaRetentionDays: 30,
        mediaFiles: [
          { id: 'mf201', type: 'image', url: 'https://images.unsplash.com/photo-1469371670807-013ccf25f16a?auto=format&fit=crop&w=1200&q=80', thumbnail: 'https://images.unsplash.com/photo-1469371670807-013ccf25f16a?auto=format&fit=crop&w=400&q=80', uploaderName: 'Davetli - Selin Y.', tableNo: 'Masa 1', timestamp: '2026-08-20 19:45', isGuest: true, uploaderIp: '195.175.40.8' },
          { id: 'mf202', type: 'video', url: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4', thumbnail: 'https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=400&q=80', uploaderName: 'Sosyal Medya Sorumlusu', tableNo: 'Balo Giriş', timestamp: '2026-08-20 20:10', isGuest: false, uploaderIp: '195.175.40.1' }
        ],"""

# Insert mediaKey fields into INITIAL_RESERVATIONS in index.html
if "mediaKey: 'MEDIA-8X92M1KP'" not in html:
    html = html.replace("id: 'RES-2026-001',", f"id: 'RES-2026-001',\n{sample_media_res1}")
    html = html.replace("id: 'RES-2026-002',", f"id: 'RES-2026-002',\n{sample_media_res2}")
    print("Added mock media files & mediaKeys to INITIAL_RESERVATIONS!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html initial data successfully!")
