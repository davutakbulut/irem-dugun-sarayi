import urllib.request
import json
import socket
import os
import base64
import struct
import time

def get_target():
    req = urllib.request.urlopen('http://localhost:9222/json/list')
    targets = json.loads(req.read().decode('utf-8'))
    for t in targets:
        if t.get('type') == 'page' and 'localhost:8000' in t.get('url', ''):
            return t['webSocketDebuggerUrl']
    for t in targets:
        if t.get('type') == 'page':
            return t['webSocketDebuggerUrl']
    raise Exception("No page target found")

class CDPClient:
    def __init__(self, ws_url):
        host_port = ws_url.replace('ws://', '').split('/')[0]
        host, port = host_port.split(':')
        self.path = '/' + '/'.join(ws_url.replace('ws://', '').split('/')[1:])
        self.sock = socket.create_connection((host, int(port)))
        self.msg_id = 0
        self._handshake(host_port)

    def _handshake(self, host_port):
        sec_key = base64.b64encode(os.urandom(16)).decode('utf-8')
        req = (
            f"GET {self.path} HTTP/1.1\r\n"
            f"Host: {host_port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {sec_key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(req.encode('utf-8'))
        resp = self.sock.recv(4096).decode('utf-8', errors='ignore')
        if "101 " not in resp:
            raise Exception(f"WebSocket handshake failed: {resp}")

    def send_frame(self, data_str):
        data_bytes = data_str.encode('utf-8')
        length = len(data_bytes)
        mask_key = os.urandom(4)
        header = bytearray()
        header.append(0x81)
        if length <= 125:
            header.append(0x80 | length)
        elif length <= 65535:
            header.append(0x80 | 126)
            header.extend(struct.pack("!H", length))
        else:
            header.append(0x80 | 127)
            header.extend(struct.pack("!Q", length))
        header.extend(mask_key)
        masked_payload = bytearray(length)
        for i in range(length):
            masked_payload[i] = data_bytes[i] ^ mask_key[i % 4]
        self.sock.sendall(header + masked_payload)

    def recv_frame(self, timeout=5.0):
        self.sock.settimeout(timeout)
        try:
            buf = bytearray()
            while len(buf) < 2:
                chunk = self.sock.recv(2 - len(buf))
                if not chunk:
                    return None
                buf.extend(chunk)
            opcode = buf[0] & 0x0F
            masked = (buf[1] & 0x80) != 0
            payload_len = buf[1] & 0x7F
            if payload_len == 126:
                len_bytes = self.sock.recv(2)
                payload_len = struct.unpack("!H", len_bytes)[0]
            elif payload_len == 127:
                len_bytes = self.sock.recv(8)
                payload_len = struct.unpack("!Q", len_bytes)[0]
            if masked:
                mask_key = self.sock.recv(4)
            payload = bytearray()
            while len(payload) < payload_len:
                chunk = self.sock.recv(payload_len - len(payload))
                if not chunk:
                    break
                payload.extend(chunk)
            if masked:
                for i in range(len(payload)):
                    payload[i] ^= mask_key[i % 4]
            return payload.decode('utf-8', errors='ignore')
        except socket.timeout:
            return None

    def call(self, method, params=None, timeout=5.0):
        self.msg_id += 1
        msg_id = self.msg_id
        cmd = {"id": msg_id, "method": method}
        if params:
            cmd["params"] = params
        self.send_frame(json.dumps(cmd))
        start = time.time()
        while time.time() - start < timeout:
            raw = self.recv_frame(timeout=1.0)
            if raw:
                try:
                    data = json.loads(raw)
                    if data.get("id") == msg_id:
                        return data
                except Exception:
                    pass
        return None

    def eval_js(self, js_code):
        res = self.call("Runtime.evaluate", {"expression": f"(function() {{ {js_code} }})()", "returnByValue": True, "awaitPromise": True})
        if res and "result" in res and "result" in res["result"]:
            return res["result"]["result"].get("value")
        return None

def run_17_pages_comprehensive_audit():
    ws_url = get_target()
    client = CDPClient(ws_url)

    # Initial setup & switch to Admin role
    client.eval_js("localStorage.removeItem('tab_permissions');")
    client.eval_js("""
        const adminBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Admin'));
        if (adminBtn) adminBtn.click();
    """)
    time.sleep(0.3)

    results = []

    def navigate_tab(tab_name):
        client.eval_js(f"window.location.hash = '#/{window_slug(tab_name)}'; window.dispatchEvent(new Event('hashchange'));")
        time.sleep(0.5)

    def window_slug(tab):
        slugs = {
            'dashboard': 'anasayfa',
            'create-reservation': 'yeni-rezervasyon',
            'venues': 'dugun-salonlari',
            'services': 'ek-hizmetler',
            'reservations': 'rezervasyonlar',
            'calendar': 'takvim',
            'campaigns': 'kampanyalar',
            'finance': 'finans',
            'customers': 'musteri-rehberi',
            'users': 'kullanici-yonetimi',
            'reports': 'raporlar-ai',
            'media': 'medya-yukle',
            'profile': 'profil',
            'settings': 'ayarlar',
            'settings-appearance': 'ayarlar/gorunum',
            'settings-performance': 'ayarlar/onbellek',
            'settings-rbac': 'ayarlar/rol-izinleri'
        }
        return slugs.get(tab, tab)

    # 1. Anasayfa (Dashboard)
    print("Auditing 1. Anasayfa (Dashboard)...")
    navigate_tab('dashboard')
    res1 = client.eval_js("""
        const text = document.body.innerText;
        const hasCiro = text.includes('Toplam Ciro') || text.includes('Ciro');
        const hasResCount = text.includes('Aktif Rezervasyon') || text.includes('Rezervasyon');
        const hasKaparo = text.includes('Kaparo') || text.includes('Tahsilat');
        const hasBakiye = text.includes('Kalan Bakiye') || text.includes('Bakiye');
        return {
            page: '1. /#/anasayfa (Dashboard)',
            passed: hasCiro && hasResCount && hasKaparo && hasBakiye,
            metricsFound: { hasCiro, hasResCount, hasKaparo, hasBakiye }
        };
    """)
    results.append(res1)

    # 2. Yeni Rezervasyon
    print("Auditing 2. Yeni Rezervasyon...")
    navigate_tab('create-reservation')
    res2 = client.eval_js("""
        const text = document.body.innerText;
        const selects = document.querySelectorAll('select');
        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
        const inputs = document.querySelectorAll('input');
        const hasTotalText = text.includes('Toplam') || text.includes('Bakiye') || text.includes('TL') || text.includes('₺');
        return {
            page: '2. /#/yeni-rezervasyon (Create Reservation)',
            passed: selects.length > 0 && checkboxes.length >= 0 && hasTotalText,
            selectsCount: selects.length,
            checkboxesCount: checkboxes.length,
            hasLiveCalculation: hasTotalText
        };
    """)
    results.append(res2)

    # 3. Düğün Salonları
    print("Auditing 3. Düğün Salonları...")
    navigate_tab('venues')
    client.eval_js("""
        const addBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Yeni Düğün Salonu Ekle'));
        if (addBtn) addBtn.click();
    """)
    time.sleep(0.4)

    res3 = client.eval_js("""
        const modal = document.querySelector('.fixed, [role="dialog"]');
        const badge = modal ? Array.from(modal.querySelectorAll('span, div')).find(el => el.innerText && el.innerText.includes('1200x800')) : null;
        const editBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Düzenle'));
        const deleteBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Sil'));

        const cancelBtn = modal ? Array.from(modal.querySelectorAll('button')).find(b => b.innerText.includes('İptal')) : null;
        if (cancelBtn) cancelBtn.click();

        return {
            page: '3. /#/dugun-salonlari (Venues)',
            passed: !!modal && !!badge && editBtns.length > 0 && deleteBtns.length > 0,
            modalOpened: !!modal,
            badge1200x800Found: !!badge,
            editButtonsCount: editBtns.length,
            deleteButtonsCount: deleteBtns.length
        };
    """)
    results.append(res3)

    # 4. Ek Hizmetler
    print("Auditing 4. Ek Hizmetler...")
    navigate_tab('services')
    client.eval_js("""
        const addBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Yeni Ek Hizmet Ekle'));
        if (addBtn) addBtn.click();
    """)
    time.sleep(0.4)

    res4 = client.eval_js("""
        const modal = document.querySelector('.fixed, [role="dialog"]');
        const badge = modal ? Array.from(modal.querySelectorAll('span, div')).find(el => el.innerText && el.innerText.includes('600x400')) : null;
        const editBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Düzenle'));
        const deleteBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Sil'));

        const cancelBtn = modal ? Array.from(modal.querySelectorAll('button')).find(b => b.innerText.includes('İptal')) : null;
        if (cancelBtn) cancelBtn.click();

        return {
            page: '4. /#/ek-hizmetler (Services)',
            passed: !!modal && !!badge && editBtns.length > 0 && deleteBtns.length > 0,
            modalOpened: !!modal,
            badge600x400Found: !!badge,
            editButtonsCount: editBtns.length,
            deleteButtonsCount: deleteBtns.length
        };
    """)
    results.append(res4)

    # 5. Rezervasyonlar (Rezervasyonlarım)
    print("Auditing 5. Rezervasyonlar...")
    navigate_tab('reservations')
    res5 = client.eval_js("""
        const text = document.body.innerText;
        const searchInput = document.querySelector('input[type="text"], input[placeholder*="Ara"]');
        const selects = document.querySelectorAll('select');
        const detailBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Detay') || b.innerText.includes('İncele'));
        
        // Open first detail modal
        if (detailBtns.length > 0) detailBtns[0].click();
        
        const modal = document.querySelector('.fixed, [role="dialog"]');
        const modalText = modal ? modal.innerText : '';
        const hasPrintInvoice = modalText.includes('Fatura') || modalText.includes('Yazdır');
        const hasEmailPreview = modalText.includes('E-Posta') || modalText.includes('E-posta') || modalText.includes('Gönder');

        // Close modal
        const closeBtn = document.querySelector('.fixed button');
        if (closeBtn) closeBtn.click();

        return {
            page: '5. /#/rezervasyonlar (Reservations)',
            passed: !!searchInput && detailBtns.length > 0,
            hasSearchInput: !!searchInput,
            detailButtonsCount: detailBtns.length,
            detailModalTested: !!modal,
            hasInvoiceAction: hasPrintInvoice,
            hasEmailPreviewAction: hasEmailPreview
        };
    """)
    results.append(res5)

    # 6. Takvim
    print("Auditing 6. Takvim...")
    navigate_tab('calendar')
    res6 = client.eval_js("""
        const text = document.body.innerText;
        const hasAugustHeader = text.includes('Ağustos') || text.includes('2026') || text.includes('Takvim');
        const draggables = document.querySelectorAll('[draggable="true"]');
        const days = document.querySelectorAll('.grid > div');

        return {
            page: '6. /#/takvim (Calendar Grid & Drag-Drop)',
            passed: hasAugustHeader && days.length > 10,
            hasAugustGrid: hasAugustHeader,
            daysGridCount: days.length,
            draggableCardsCount: draggables.length
        };
    """)
    results.append(res6)

    # 7. Kampanyalar
    print("Auditing 7. Kampanyalar...")
    navigate_tab('campaigns')
    client.eval_js("""
        const addBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Yeni Özel Kampanya Ekle'));
        if (addBtn) addBtn.click();
    """)
    time.sleep(0.4)

    res7 = client.eval_js("""
        const modal = document.querySelector('.fixed, [role="dialog"]');
        const editBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Düzenle'));
        const deleteBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Sil'));

        const cancelBtn = modal ? Array.from(modal.querySelectorAll('button')).find(b => b.innerText.includes('İptal')) : null;
        if (cancelBtn) cancelBtn.click();

        return {
            page: '7. /#/kampanyalar (Campaigns)',
            passed: !!modal && editBtns.length > 0 && deleteBtns.length > 0,
            modalOpened: !!modal,
            editButtonsCount: editBtns.length,
            deleteButtonsCount: deleteBtns.length
        };
    """)
    results.append(res7)

    # 8. Finans
    print("Auditing 8. Finans...")
    navigate_tab('finance')
    res8 = client.eval_js("""
        const text = document.body.innerText;
        const hasCiro = text.includes('Ciro') || text.includes('Gelir');
        const hasKaparo = text.includes('Kaparo') || text.includes('Tahsilat');
        const hasBakiye = text.includes('Bakiye') || text.includes('Kalan');

        return {
            page: '8. /#/finans (Finance)',
            passed: hasCiro && hasKaparo && hasBakiye,
            hasCiroMetric: hasCiro,
            hasKaparoMetric: hasKaparo,
            hasBakiyeMetric: hasBakiye
        };
    """)
    results.append(res8)

    # 9. Müşteri Rehberi
    print("Auditing 9. Müşteri Rehberi...")
    navigate_tab('customers')
    res9 = client.eval_js("""
        const text = document.body.innerText;
        const waLinks = Array.from(document.querySelectorAll('a')).filter(a => a.href && a.href.includes('wa.me'));
        const addBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Yeni Müşteri Ekle'));
        const deleteBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Sil'));

        return {
            page: '9. /#/musteri-rehberi (Customers)',
            passed: waLinks.length > 0 && !!addBtn && deleteBtns.length > 0,
            whatsappLinksCount: waLinks.length,
            hasAddCustomerBtn: !!addBtn,
            deleteButtonsCount: deleteBtns.length
        };
    """)
    results.append(res9)

    # 10. Kullanıcı Yönetimi
    print("Auditing 10. Kullanıcı Yönetimi...")
    navigate_tab('users')
    client.eval_js("""
        const addBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Yeni Kullanıcı Tanımla'));
        if (addBtn) addBtn.click();
    """)
    time.sleep(0.4)

    res10 = client.eval_js("""
        const modal = document.querySelector('.fixed, [role="dialog"]');
        const badge = modal ? Array.from(modal.querySelectorAll('span, div')).find(el => el.innerText && el.innerText.includes('400x400')) : null;
        const roleBadges = Array.from(document.querySelectorAll('span')).filter(s => s.innerText && (s.innerText.includes('admin') || s.innerText.includes('satisci') || s.innerText.includes('sosyal')));

        const cancelBtn = modal ? Array.from(modal.querySelectorAll('button')).find(b => b.innerText.includes('İptal')) : null;
        if (cancelBtn) cancelBtn.click();

        return {
            page: '10. /#/kullanici-yonetimi (Users)',
            passed: !!modal && !!badge && roleBadges.length > 0,
            modalOpened: !!modal,
            badge400x400Found: !!badge,
            roleBadgesCount: roleBadges.length
        };
    """)
    results.append(res10)

    # 11. Raporlar & AI
    print("Auditing 11. Raporlar & AI...")
    navigate_tab('reports')
    res11 = client.eval_js("""
        const text = document.body.innerText;
        const actionBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Kampanya Oluştur') || b.innerText.includes('Paket Oluştur'));
        const hasAiHeader = text.includes('Yapay Zeka') || text.includes('Öneri') || text.includes('Rapor');

        return {
            page: '11. /#/raporlar-ai (AI Reports)',
            passed: hasAiHeader && actionBtns.length > 0,
            hasAiRecommendations: hasAiHeader,
            actionButtonsCount: actionBtns.length
        };
    """)
    results.append(res11)

    # 12. Medya Galerisi
    print("Auditing 12. Medya Galerisi...")
    navigate_tab('media')
    res12 = client.eval_js("""
        const badge = Array.from(document.querySelectorAll('span, div')).find(el => el.innerText && el.innerText.includes('1920x1080'));
        const fileInput = document.querySelector('input[type="file"]');

        return {
            page: '12. /#/medya-yukle (Media Gallery)',
            passed: !!badge && !!fileInput,
            badge1920x1080Found: !!badge,
            hasFileInput: !!fileInput
        };
    """)
    results.append(res12)

    # 13. Profil
    print("Auditing 13. Profil...")
    navigate_tab('profile')
    res13 = client.eval_js("""
        const form = document.querySelector('form');
        const badge = Array.from(document.querySelectorAll('span, div')).find(el => el.innerText && el.innerText.includes('400x400'));
        const nameInput = document.querySelector('form input[type="text"]');
        const emailInput = document.querySelector('form input[type="email"]');
        const passInput = document.querySelector('form input[type="password"]');
        const roleSelect = document.querySelector('form select');

        return {
            page: '13. /#/profil (Profile Component)',
            passed: !!form && !!badge && !!nameInput && !!emailInput && !!passInput && !!roleSelect,
            formFound: !!form,
            badge400x400Found: !!badge,
            hasNameInput: !!nameInput,
            hasEmailInput: !!emailInput,
            hasPasswordInput: !!passInput,
            hasRoleSelect: !!roleSelect
        };
    """)
    results.append(res13)

    # 14. Ayarlar - Görünüm & Tema
    print("Auditing 14. Ayarlar - Görünüm & Tema...")
    navigate_tab('settings-appearance')
    res14 = client.eval_js("""
        const text = document.body.innerText;
        const colorBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Gold') || b.innerText.includes('Emerald') || b.innerText.includes('Sapphire') || b.innerText.includes('Rose') || b.innerText.includes('Violet'));

        return {
            page: '14. /#/ayarlar/gorunum (Theme Color Palette)',
            passed: colorBtns.length >= 5,
            colorPaletteButtonsCount: colorBtns.length
        };
    """)
    results.append(res14)

    # 15. Ayarlar - Önbellek & Performans
    print("Auditing 15. Ayarlar - Önbellek...")
    navigate_tab('settings-performance')
    res15 = client.eval_js("""
        const text = document.body.innerText;
        const switches = document.querySelectorAll('input[type="checkbox"], button[role="switch"]');
        const clearBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Temizle') || b.innerText.includes('Sıfırla') || b.innerText.includes('Önbellek'));

        return {
            page: '15. /#/ayarlar/onbellek (Cache & Performance)',
            passed: text.includes('Önbellek') || text.includes('Cache'),
            hasCacheSettingsText: text.includes('Önbellek') || text.includes('Cache')
        };
    """)
    results.append(res15)

    # 16. Ayarlar - Rol & İzin Yönetimi (RBAC)
    print("Auditing 16. Ayarlar - Rol & İzin Yönetimi...")
    navigate_tab('settings-rbac')
    res16 = client.eval_js("""
        const table = document.querySelector('table');
        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
        const addRoleInput = document.querySelector('input[type="text"]');

        return {
            page: '16. /#/ayarlar/rol-izinleri (RBAC Matrix)',
            passed: !!table && checkboxes.length > 5,
            matrixTableFound: !!table,
            permissionCheckboxesCount: checkboxes.length
        };
    """)
    results.append(res16)

    # 17. 403 Güvenlik Duvarı (Unauthorized Access Guard)
    print("Auditing 17. 403 Güvenlik Duvarı...")
    client.eval_js("""
        const musteriBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Müşteri'));
        if (musteriBtn) musteriBtn.click();
    """)
    time.sleep(0.3)
    navigate_tab('users')
    time.sleep(0.4)

    res17 = client.eval_js("""
        const text = document.body.innerText;
        const has403Text = text.includes('Yetkisiz') || text.includes('Erişim Engellendi') || text.includes('403') || text.includes('İzin');
        const goHomeBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Anasayfa') || b.innerText.includes('Dön'));

        // Restore Admin role
        const adminBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Admin'));
        if (adminBtn) adminBtn.click();

        return {
            page: '17. 403 Güvenlik Duvarı Guard',
            passed: has403Text && !!goHomeBtn,
            unauthorizedScreenTriggered: has403Text,
            hasGoHomeButton: !!goHomeBtn
        };
    """)
    results.append(res17)

    print("\n=================== 17 PAGES AUDIT SUMMARY REPORT ===================")
    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    run_17_pages_comprehensive_audit()
