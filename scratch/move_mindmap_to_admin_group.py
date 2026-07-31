import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Sidebar menu: remove mind-map from ANA PANOLAR and add to YÖNETİM & AYARLAR
old_sidebar_anapanolar = """                      title: 'ANA PANOLAR',
                      icon: 'chart',
                      fallbackEmoji: '📌',
                      items: [
                        { id: 'dashboard', label: 'Anasayfa / İstatistikler', icon: 'chart', fallbackEmoji: '📊' },
                        { id: 'mind-map', label: 'Zihin Haritası (MindMap)', icon: 'sparkles', fallbackEmoji: '🧠', badge: 'YENİ' },
                        { id: 'create-reservation', label: 'Yeni Rezervasyon', icon: 'sparkles', fallbackEmoji: '✨', badge: 'YENİ' }
                      ]"""

new_sidebar_anapanolar = """                      title: 'ANA PANOLAR',
                      icon: 'chart',
                      fallbackEmoji: '📌',
                      items: [
                        { id: 'dashboard', label: 'Anasayfa / İstatistikler', icon: 'chart', fallbackEmoji: '📊' },
                        { id: 'create-reservation', label: 'Yeni Rezervasyon', icon: 'sparkles', fallbackEmoji: '✨', badge: 'YENİ' }
                      ]"""

if old_sidebar_anapanolar in html:
    html = html.replace(old_sidebar_anapanolar, new_sidebar_anapanolar)
    print("Removed mind-map from ANA PANOLAR in Sidebar")

old_sidebar_yonetim = """                      title: 'YÖNETİM & AYARLAR',
                      icon: 'settings',
                      fallbackEmoji: '⚙️',
                      items: [
                        { id: 'roles', label: 'Rol Yönetimi & İzinler', icon: 'shield', fallbackEmoji: '🛡️', badge: 'YENİ' },
                        { id: 'users', label: 'Kullanıcı Yönetimi', icon: 'user', fallbackEmoji: '👥' },
                        { id: 'settings', label: 'Sistem Ayarları', icon: 'settings', fallbackEmoji: '⚙️' }
                      ]"""

new_sidebar_yonetim = """                      title: 'YÖNETİM & AYARLAR',
                      icon: 'settings',
                      fallbackEmoji: '⚙️',
                      items: [
                        { id: 'mind-map', label: 'Zihin Haritası (MindMap)', icon: 'sparkles', fallbackEmoji: '🧠', badge: 'YENİ' },
                        { id: 'roles', label: 'Rol Yönetimi & İzinler', icon: 'shield', fallbackEmoji: '🛡️', badge: 'YENİ' },
                        { id: 'users', label: 'Kullanıcı Yönetimi', icon: 'user', fallbackEmoji: '👥' },
                        { id: 'settings', label: 'Sistem Ayarları', icon: 'settings', fallbackEmoji: '⚙️' }
                      ]"""

if old_sidebar_yonetim in html:
    html = html.replace(old_sidebar_yonetim, new_sidebar_yonetim)
    print("Added mind-map under YÖNETİM & AYARLAR in Sidebar")


# 2. Update Topbar Mega Menu (HorizontalNavbarComponent)
old_topbar_admin_items = """          title: 'Yönetim & Ayarlar',
          icon: 'settings',
          fallbackEmoji: '⚙️',
          showcaseTitle: 'Personel Yetkileri & Sistem Ayarları',
          showcaseDesc: 'RBAC rol matrisi ile personel yetkilerini denetleyin, 5 kurumsal tema ve performans önbelleğini yönetin.',
          showcaseImg: 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=600&q=80',
          items: [
            { id: 'roles', label: 'Rol Yönetimi (Sistem Rolleri)', desc: 'Rol ekleme, düzenleme, silme ve yetki kısıtlama paneli', icon: 'shield', fallbackEmoji: '🛡️', badge: 'ADMIN' },"""

new_topbar_admin_items = """          title: 'Yönetim & Ayarlar',
          icon: 'settings',
          fallbackEmoji: '⚙️',
          showcaseTitle: 'Personel Yetkileri & Sistem Ayarları',
          showcaseDesc: 'RBAC rol matrisi ile personel yetkilerini denetleyin, 5 kurumsal tema ve performans önbelleğini yönetin.',
          showcaseImg: 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=600&q=80',
          items: [
            { id: 'mind-map', label: 'Zihin Haritası (MindMap)', desc: 'İnteraktif sistem zihin haritası ve veri akış topolojisi', icon: 'sparkles', fallbackEmoji: '🧠', badge: 'ADMIN' },
            { id: 'roles', label: 'Rol Yönetimi (Sistem Rolleri)', desc: 'Rol ekleme, düzenleme, silme ve yetki kısıtlama paneli', icon: 'shield', fallbackEmoji: '🛡️', badge: 'ADMIN' },"""

if old_topbar_admin_items in html:
    html = html.replace(old_topbar_admin_items, new_topbar_admin_items)
    print("Added mind-map under Yönetim & Ayarlar in Topbar Mega Menu")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html successfully!")
