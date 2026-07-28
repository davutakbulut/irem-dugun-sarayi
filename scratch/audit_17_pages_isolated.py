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

def test_17_pages_isolated():
    ws_url = get_target()
    client = CDPClient(ws_url)

    results = []

    def reset_and_navigate(hash_slug):
        client.call("Page.navigate", {"url": f"http://localhost:8000/#/{hash_slug}"})
        time.sleep(0.8)
        client.eval_js("localStorage.removeItem('tab_permissions');")
        # Ensure Admin active
        client.eval_js("""
            const adminBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Admin'));
            if (adminBtn) adminBtn.click();
        """)
        time.sleep(0.3)

    # 1. Dashboard
    reset_and_navigate('anasayfa')
    r1 = client.eval_js("""
        const text = document.body.innerText;
        return {
            page: '1. /#/anasayfa (Dashboard)',
            passed: text.includes('Kır Bahçesi') || text.includes('Salon') || text.includes('Ciro') || text.includes('Hoş Geldiniz'),
            ciroCard: text.includes('Ciro') || text.includes('₺') || text.includes('TL'),
            activeResCard: text.includes('Rezervasyon'),
            kaparoCard: text.includes('Kaparo') || text.includes('Tahsilat'),
            bakiyeCard: text.includes('Bakiye') || text.includes('Kalan')
        };
    """)
    print("1. Dashboard:", r1)
    results.append(r1)

    # 2. Create Reservation
    reset_and_navigate('yeni-rezervasyon')
    r2 = client.eval_js("""
        const text = document.body.innerText;
        const selects = document.querySelectorAll('select');
        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
        return {
            page: '2. /#/yeni-rezervasyon (Create Reservation)',
            passed: selects.length > 0 && (text.includes('Toplam') || text.includes('Fiyat') || text.includes('₺')),
            venueSelectFound: selects.length > 0,
            checkboxesCount: checkboxes.length,
            liveCalculation: text.includes('Toplam') || text.includes('₺')
        };
    """)
    print("2. Create Res:", r2)
    results.append(r2)

    # 3. Venues
    reset_and_navigate('dugun-salonlari')
    client.eval_js("""
        const addBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Yeni Düğün Salonu Ekle'));
        if (addBtn) addBtn.click();
    """)
    time.sleep(0.4)
    r3 = client.eval_js("""
        const modal = document.querySelector('.fixed, [role="dialog"]');
        const badge = modal ? Array.from(modal.querySelectorAll('span, div')).find(el => el.innerText && el.innerText.includes('1200x800')) : null;
        const editBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Düzenle'));
        const deleteBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Sil'));
        return {
            page: '3. /#/dugun-salonlari (Venues)',
            passed: !!modal && !!badge && editBtns.length > 0 && deleteBtns.length > 0,
            modalOpened: !!modal,
            badge1200x800Found: !!badge,
            editBtnsCount: editBtns.length,
            deleteBtnsCount: deleteBtns.length
        };
    """)
    print("3. Venues:", r3)
    results.append(r3)

    # 4. Services
    reset_and_navigate('ek-hizmetler')
    client.eval_js("""
        const addBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Yeni Ek Hizmet Ekle'));
        if (addBtn) addBtn.click();
    """)
    time.sleep(0.4)
    r4 = client.eval_js("""
        const modal = document.querySelector('.fixed, [role="dialog"]');
        const badge = modal ? Array.from(modal.querySelectorAll('span, div')).find(el => el.innerText && el.innerText.includes('600x400')) : null;
        const editBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Düzenle'));
        const deleteBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Sil'));
        return {
            page: '4. /#/ek-hizmetler (Services)',
            passed: !!modal && !!badge && editBtns.length > 0 && deleteBtns.length > 0,
            modalOpened: !!modal,
            badge600x400Found: !!badge,
            editBtnsCount: editBtns.length,
            deleteBtnsCount: deleteBtns.length
        };
    """)
    print("4. Services:", r4)
    results.append(r4)

    # 5. Reservations
    reset_and_navigate('rezervasyonlar')
    r5 = client.eval_js("""
        const searchInput = document.querySelector('input[type="text"], input[placeholder*="Ara"]');
        const detailBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Detay') || b.innerText.includes('İncele'));

        if (detailBtns.length > 0) detailBtns[0].click();
        const modal = document.querySelector('.fixed, [role="dialog"]');
        const modalText = modal ? modal.innerText : '';

        return {
            page: '5. /#/rezervasyonlar (Reservations)',
            passed: !!searchInput && detailBtns.length > 0 && !!modal,
            hasSearchInput: !!searchInput,
            detailBtnsCount: detailBtns.length,
            detailModalOpened: !!modal,
            hasPrintInvoiceAction: modalText.includes('Fatura') || modalText.includes('Yazdır'),
            hasEmailPreviewAction: modalText.includes('E-Posta') || modalText.includes('E-posta') || modalText.includes('Gönder')
        };
    """)
    print("5. Reservations:", r5)
    results.append(r5)

    # 6. Calendar
    reset_and_navigate('takvim')
    r6 = client.eval_js("""
        const text = document.body.innerText;
        const draggables = document.querySelectorAll('[draggable="true"]');
        const days = document.querySelectorAll('.grid > div');
        return {
            page: '6. /#/takvim (Calendar)',
            passed: days.length > 10 && text.includes('Takvim'),
            hasAugustGrid: text.includes('Ağustos') || text.includes('2026') || text.includes('Takvim'),
            daysGridCount: days.length,
            draggableCardsCount: draggables.length
        };
    """)
    print("6. Calendar:", r6)
    results.append(r6)

    # 7. Campaigns
    reset_and_navigate('kampanyalar')
    client.eval_js("""
        const addBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Yeni Özel Kampanya Ekle'));
        if (addBtn) addBtn.click();
    """)
    time.sleep(0.4)
    r7 = client.eval_js("""
        const modal = document.querySelector('.fixed, [role="dialog"]');
        const editBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Düzenle'));
        const deleteBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Sil'));
        return {
            page: '7. /#/kampanyalar (Campaigns)',
            passed: !!modal && editBtns.length > 0 && deleteBtns.length > 0,
            modalOpened: !!modal,
            editBtnsCount: editBtns.length,
            deleteBtnsCount: deleteBtns.length
        };
    """)
    print("7. Campaigns:", r7)
    results.append(r7)

    # 8. Finance
    reset_and_navigate('finans')
    r8 = client.eval_js("""
        const text = document.body.innerText;
        return {
            page: '8. /#/finans (Finance)',
            passed: text.includes('Finans') || text.includes('Muhasebe') || text.includes('Ciro'),
            hasCiro: text.includes('Ciro') || text.includes('Gelir'),
            hasKaparo: text.includes('Kaparo') || text.includes('Tahsilat'),
            hasBakiye: text.includes('Bakiye') || text.includes('Kalan')
        };
    """)
    print("8. Finance:", r8)
    results.append(r8)

    # 9. Customers
    reset_and_navigate('musteri-rehberi')
    r9 = client.eval_js("""
        const waLinks = Array.from(document.querySelectorAll('a')).filter(a => a.href && a.href.includes('wa.me'));
        const addBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Yeni Müşteri Ekle'));
        const deleteBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Sil'));
        return {
            page: '9. /#/musteri-rehberi (Customers)',
            passed: waLinks.length > 0 && !!addBtn && deleteBtns.length > 0,
            whatsappLinksCount: waLinks.length,
            hasAddCustomerBtn: !!addBtn,
            deleteBtnsCount: deleteBtns.length
        };
    """)
    print("9. Customers:", r9)
    results.append(r9)

    # 10. Users
    reset_and_navigate('kullanici-yonetimi')
    client.eval_js("""
        const addBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Yeni Kullanıcı Tanımla'));
        if (addBtn) addBtn.click();
    """)
    time.sleep(0.4)
    r10 = client.eval_js("""
        const modal = document.querySelector('.fixed, [role="dialog"]');
        const badge = modal ? Array.from(modal.querySelectorAll('span, div')).find(el => el.innerText && el.innerText.includes('400x400')) : null;
        const roleBadges = Array.from(document.querySelectorAll('span')).filter(s => s.innerText && (s.innerText.includes('admin') || s.innerText.includes('satisci') || s.innerText.includes('sosyal')));

        return {
            page: '10. /#/kullanici-yonetimi (Users)',
            passed: !!modal && !!badge && roleBadges.length > 0,
            modalOpened: !!modal,
            badge400x400Found: !!badge,
            roleBadgesCount: roleBadges.length
        };
    """)
    print("10. Users:", r10)
    results.append(r10)

    # 11. Reports & AI
    reset_and_navigate('raporlar-ai')
    r11 = client.eval_js("""
        const text = document.body.innerText;
        const actionBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Kampanya Oluştur') || b.innerText.includes('Paket Oluştur'));
        return {
            page: '11. /#/raporlar-ai (AI Reports)',
            passed: actionBtns.length > 0 && (text.includes('Rapor') || text.includes('Yapay Zeka')),
            hasAiRecommendations: text.includes('Rapor') || text.includes('Yapay Zeka'),
            actionBtnsCount: actionBtns.length
        };
    """)
    print("11. Reports:", r11)
    results.append(r11)

    # 12. Media Gallery
    reset_and_navigate('medya-yukle')
    r12 = client.eval_js("""
        const badge = Array.from(document.querySelectorAll('span, div')).find(el => el.innerText && el.innerText.includes('1920x1080'));
        const fileInput = document.querySelector('input[type="file"]');
        return {
            page: '12. /#/medya-yukle (Media Gallery)',
            passed: !!badge && !!fileInput,
            badge1920x1080Found: !!badge,
            hasFileInput: !!fileInput
        };
    """)
    print("12. Media:", r12)
    results.append(r12)

    # 13. Profile
    reset_and_navigate('profil')
    r13 = client.eval_js("""
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
    print("13. Profile:", r13)
    results.append(r13)

    # 14. Theme Settings
    reset_and_navigate('ayarlar/gorunum')
    r14 = client.eval_js("""
        const colorBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Gold') || b.innerText.includes('Emerald') || b.innerText.includes('Sapphire') || b.innerText.includes('Rose') || b.innerText.includes('Violet'));
        return {
            page: '14. /#/ayarlar/gorunum (Appearance Settings)',
            passed: colorBtns.length >= 5,
            colorPaletteBtnsCount: colorBtns.length
        };
    """)
    print("14. Theme:", r14)
    results.append(r14)

    # 15. Cache Settings
    reset_and_navigate('ayarlar/onbellek')
    r15 = client.eval_js("""
        const text = document.body.innerText;
        return {
            page: '15. /#/ayarlar/onbellek (Cache Performance)',
            passed: text.includes('Önbellek') || text.includes('Cache'),
            hasCacheText: text.includes('Önbellek') || text.includes('Cache')
        };
    """)
    print("15. Cache:", r15)
    results.append(r15)

    # 16. RBAC Permissions Matrix
    reset_and_navigate('ayarlar/rol-izinleri')
    r16 = client.eval_js("""
        const table = document.querySelector('table');
        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
        return {
            page: '16. /#/ayarlar/rol-izinleri (RBAC Matrix)',
            passed: !!table && checkboxes.length > 5,
            matrixTableFound: !!table,
            checkboxesCount: checkboxes.length
        };
    """)
    print("16. RBAC:", r16)
    results.append(r16)

    # 17. 403 Security Guard
    reset_and_navigate('anasayfa')
    client.eval_js("""
        const musteriBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Müşteri'));
        if (musteriBtn) musteriBtn.click();
    """)
    time.sleep(0.3)
    client.eval_js("window.location.hash = '#/kullanici-yonetimi'; window.dispatchEvent(new Event('hashchange'));")
    time.sleep(0.4)

    r17 = client.eval_js("""
        const text = document.body.innerText;
        const has403 = text.includes('Yetkisiz') || text.includes('Erişim Engellendi') || text.includes('403') || text.includes('İzin');
        const goHomeBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Anasayfa') || b.innerText.includes('Dön'));

        // Restore Admin
        const adminBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Admin'));
        if (adminBtn) adminBtn.click();

        return {
            page: '17. 403 Güvenlik Duvarı Guard',
            passed: has403 && !!goHomeBtn,
            unauthorizedScreenTriggered: has403,
            hasGoHomeButton: !!goHomeBtn
        };
    """)
    print("17. 403 Guard:", r17)
    results.append(r17)

    print("\n================ ISOLATED 17 PAGES AUDIT SUMMARY ================")
    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    test_17_pages_isolated()
