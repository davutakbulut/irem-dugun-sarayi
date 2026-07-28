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

def run_17_pages_click_audit():
    ws_url = get_target()
    client = CDPClient(ws_url)

    # Initial setup & switch to Admin role
    client.call("Page.navigate", {"url": "http://localhost:8000/"})
    time.sleep(1.0)
    client.eval_js("localStorage.removeItem('tab_permissions');")

    # Ensure Admin role active
    client.eval_js("""
        const adminBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Admin'));
        if (adminBtn) adminBtn.click();
    """)
    time.sleep(0.3)

    results = []

    def navigate_by_click_or_reload(slug):
        client.call("Page.navigate", {"url": f"http://localhost:8000/#/{slug}"})
        time.sleep(0.8)

    # 1. Anasayfa (Dashboard)
    print("1. Anasayfa (Dashboard)...")
    navigate_by_click_or_reload('anasayfa')
    r1 = client.eval_js("""
        const text = document.body.innerText;
        return {
            page: '1. /#/anasayfa',
            passed: text.includes('Kır Bahçesi') || text.includes('Salon') || text.includes('İstatistik') || text.includes('Ciro') || text.includes('Hoş Geldiniz'),
            ciroCard: text.includes('Ciro') || text.includes('₺') || text.includes('TL'),
            resCountCard: text.includes('Rezervasyon'),
            kaparoCard: text.includes('Kaparo') || text.includes('Tahsilat'),
            bakiyeCard: text.includes('Bakiye') || text.includes('Kalan')
        };
    """)
    print("R1:", r1)
    results.append(r1)

    # 2. Yeni Rezervasyon
    print("2. Yeni Rezervasyon...")
    navigate_by_click_or_reload('yeni-rezervasyon')
    r2 = client.eval_js("""
        const text = document.body.innerText;
        const selects = document.querySelectorAll('select');
        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
        return {
            page: '2. /#/yeni-rezervasyon',
            passed: selects.length > 0 && text.includes('Rezervasyon'),
            selectsCount: selects.length,
            checkboxesCount: checkboxes.length,
            hasCalculation: text.includes('Toplam') || text.includes('₺') || text.includes('TL')
        };
    """)
    print("R2:", r2)
    results.append(r2)

    # 3. Düğün Salonları
    print("3. Düğün Salonları...")
    navigate_by_click_or_reload('dugun-salonlari')
    client.eval_js("""
        const addBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Yeni Düğün Salonu Ekle'));
        if (addBtn) addBtn.click();
    """)
    time.sleep(0.5)

    r3 = client.eval_js("""
        const modal = document.querySelector('.fixed, [role="dialog"]');
        const badge = modal ? Array.from(modal.querySelectorAll('span, div')).find(el => el.innerText && el.innerText.includes('1200x800')) : null;
        const editBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Düzenle'));
        const deleteBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Sil'));

        const cancelBtn = modal ? Array.from(modal.querySelectorAll('button')).find(b => b.innerText.includes('İptal')) : null;
        if (cancelBtn) cancelBtn.click();

        return {
            page: '3. /#/dugun-salonlari',
            passed: !!modal && !!badge && editBtns.length > 0 && deleteBtns.length > 0,
            modalOpened: !!modal,
            badge1200x800Found: !!badge,
            editBtnsCount: editBtns.length,
            deleteBtnsCount: deleteBtns.length
        };
    """)
    print("R3:", r3)
    results.append(r3)

    # 4. Ek Hizmetler
    print("4. Ek Hizmetler...")
    navigate_by_click_or_reload('ek-hizmetler')
    client.eval_js("""
        const addBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Yeni Ek Hizmet Ekle'));
        if (addBtn) addBtn.click();
    """)
    time.sleep(0.5)

    r4 = client.eval_js("""
        const modal = document.querySelector('.fixed, [role="dialog"]');
        const badge = modal ? Array.from(modal.querySelectorAll('span, div')).find(el => el.innerText && el.innerText.includes('600x400')) : null;
        const editBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Düzenle'));
        const deleteBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Sil'));

        const cancelBtn = modal ? Array.from(modal.querySelectorAll('button')).find(b => b.innerText.includes('İptal')) : null;
        if (cancelBtn) cancelBtn.click();

        return {
            page: '4. /#/ek-hizmetler',
            passed: !!modal && !!badge && editBtns.length > 0 && deleteBtns.length > 0,
            modalOpened: !!modal,
            badge600x400Found: !!badge,
            editBtnsCount: editBtns.length,
            deleteBtnsCount: deleteBtns.length
        };
    """)
    print("R4:", r4)
    results.append(r4)

    # 5. Rezervasyonlar
    print("5. Rezervasyonlar...")
    navigate_by_click_or_reload('rezervasyonlar')
    r5 = client.eval_js("""
        const text = document.body.innerText;
        const searchInput = document.querySelector('input[type="text"], input[placeholder*="Ara"]');
        const statusSelect = document.querySelector('select');
        const detailBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Detay') || b.innerText.includes('İncele'));

        if (detailBtns.length > 0) detailBtns[0].click();
        
        const modal = document.querySelector('.fixed, [role="dialog"]');
        const modalText = modal ? modal.innerText : '';

        const closeBtn = document.querySelector('.fixed button');
        if (closeBtn) closeBtn.click();

        return {
            page: '5. /#/rezervasyonlar',
            passed: !!searchInput && detailBtns.length > 0,
            hasSearchInput: !!searchInput,
            detailBtnsCount: detailBtns.length,
            modalOpened: !!modal,
            hasInvoiceBtn: modalText.includes('Fatura') || modalText.includes('Yazdır'),
            hasEmailBtn: modalText.includes('E-Posta') || modalText.includes('E-posta') || modalText.includes('Gönder')
        };
    """)
    print("R5:", r5)
    results.append(r5)

    # 6. Takvim
    print("6. Takvim...")
    navigate_by_click_or_reload('takvim')
    r6 = client.eval_js("""
        const text = document.body.innerText;
        const draggables = document.querySelectorAll('[draggable="true"]');
        const gridDays = document.querySelectorAll('.grid > div');
        return {
            page: '6. /#/takvim',
            passed: gridDays.length > 10 && text.includes('Takvim'),
            hasAugustGrid: text.includes('Ağustos') || text.includes('2026') || text.includes('Takvim'),
            gridDaysCount: gridDays.length,
            draggableCardsCount: draggables.length
        };
    """)
    print("R6:", r6)
    results.append(r6)

    # 7. Kampanyalar
    print("7. Kampanyalar...")
    navigate_by_click_or_reload('kampanyalar')
    client.eval_js("""
        const addBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Yeni Özel Kampanya Ekle'));
        if (addBtn) addBtn.click();
    """)
    time.sleep(0.5)

    r7 = client.eval_js("""
        const modal = document.querySelector('.fixed, [role="dialog"]');
        const editBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Düzenle'));
        const deleteBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Sil'));

        const cancelBtn = modal ? Array.from(modal.querySelectorAll('button')).find(b => b.innerText.includes('İptal')) : null;
        if (cancelBtn) cancelBtn.click();

        return {
            page: '7. /#/kampanyalar',
            passed: !!modal && editBtns.length > 0 && deleteBtns.length > 0,
            modalOpened: !!modal,
            editBtnsCount: editBtns.length,
            deleteBtnsCount: deleteBtns.length
        };
    """)
    print("R7:", r7)
    results.append(r7)

    # 8. Finans
    print("8. Finans...")
    navigate_by_click_or_reload('finans')
    r8 = client.eval_js("""
        const text = document.body.innerText;
        return {
            page: '8. /#/finans',
            passed: text.includes('Finans') || text.includes('Muhasebe') || text.includes('Ciro'),
            hasCiro: text.includes('Ciro') || text.includes('Gelir'),
            hasKaparo: text.includes('Kaparo') || text.includes('Tahsilat'),
            hasBakiye: text.includes('Bakiye') || text.includes('Kalan')
        };
    """)
    print("R8:", r8)
    results.append(r8)

    # 9. Müşteri Rehberi
    print("9. Müşteri Rehberi...")
    navigate_by_click_or_reload('musteri-rehberi')
    r9 = client.eval_js("""
        const text = document.body.innerText;
        const waLinks = Array.from(document.querySelectorAll('a')).filter(a => a.href && a.href.includes('wa.me'));
        const addBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Yeni Müşteri Ekle'));
        const deleteBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Sil'));

        return {
            page: '9. /#/musteri-rehberi',
            passed: waLinks.length > 0 && !!addBtn && deleteBtns.length > 0,
            whatsappLinksCount: waLinks.length,
            hasAddCustomerBtn: !!addBtn,
            deleteBtnsCount: deleteBtns.length
        };
    """)
    print("R9:", r9)
    results.append(r9)

    # 10. Kullanıcı Yönetimi
    print("10. Kullanıcı Yönetimi...")
    navigate_by_click_or_reload('kullanici-yonetimi')
    client.eval_js("""
        const addBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Yeni Kullanıcı Tanımla'));
        if (addBtn) addBtn.click();
    """)
    time.sleep(0.5)

    r10 = client.eval_js("""
        const modal = document.querySelector('.fixed, [role="dialog"]');
        const badge = modal ? Array.from(modal.querySelectorAll('span, div')).find(el => el.innerText && el.innerText.includes('400x400')) : null;
        const roleBadges = Array.from(document.querySelectorAll('span')).filter(s => s.innerText && (s.innerText.includes('admin') || s.innerText.includes('satisci') || s.innerText.includes('sosyal')));

        const cancelBtn = modal ? Array.from(modal.querySelectorAll('button')).find(b => b.innerText.includes('İptal')) : null;
        if (cancelBtn) cancelBtn.click();

        return {
            page: '10. /#/kullanici-yonetimi',
            passed: !!modal && !!badge && roleBadges.length > 0,
            modalOpened: !!modal,
            badge400x400Found: !!badge,
            roleBadgesCount: roleBadges.length
        };
    """)
    print("R10:", r10)
    results.append(r10)

    # 11. Raporlar & AI
    print("11. Raporlar & AI...")
    navigate_by_click_or_reload('raporlar-ai')
    r11 = client.eval_js("""
        const text = document.body.innerText;
        const actionBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Kampanya Oluştur') || b.innerText.includes('Paket Oluştur'));
        return {
            page: '11. /#/raporlar-ai',
            passed: actionBtns.length > 0 && (text.includes('Rapor') || text.includes('Yapay Zeka')),
            hasAiRecommendations: text.includes('Rapor') || text.includes('Yapay Zeka'),
            actionBtnsCount: actionBtns.length
        };
    """)
    print("R11:", r11)
    results.append(r11)

    # 12. Medya Galerisi
    print("12. Medya Galerisi...")
    navigate_by_click_or_reload('medya-yukle')
    r12 = client.eval_js("""
        const badge = Array.from(document.querySelectorAll('span, div')).find(el => el.innerText && el.innerText.includes('1920x1080'));
        const fileInput = document.querySelector('input[type="file"]');
        return {
            page: '12. /#/medya-yukle',
            passed: !!badge && !!fileInput,
            badge1920x1080Found: !!badge,
            hasFileInput: !!fileInput
        };
    """)
    print("R12:", r12)
    results.append(r12)

    # 13. Profil
    print("13. Profil...")
    navigate_by_click_or_reload('profil')
    r13 = client.eval_js("""
        const form = document.querySelector('form');
        const badge = Array.from(document.querySelectorAll('span, div')).find(el => el.innerText && el.innerText.includes('400x400'));
        const nameInput = document.querySelector('form input[type="text"]');
        const emailInput = document.querySelector('form input[type="email"]');
        const passInput = document.querySelector('form input[type="password"]');
        const roleSelect = document.querySelector('form select');

        return {
            page: '13. /#/profil',
            passed: !!form && !!badge && !!nameInput && !!emailInput && !!passInput && !!roleSelect,
            formFound: !!form,
            badge400x400Found: !!badge,
            hasNameInput: !!nameInput,
            hasEmailInput: !!emailInput,
            hasPasswordInput: !!passInput,
            hasRoleSelect: !!roleSelect
        };
    """)
    print("R13:", r13)
    results.append(r13)

    # 14. Görünüm & Tema
    print("14. Görünüm & Tema...")
    navigate_by_click_or_reload('ayarlar/gorunum')
    r14 = client.eval_js("""
        const colorBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Gold') || b.innerText.includes('Emerald') || b.innerText.includes('Sapphire') || b.innerText.includes('Rose') || b.innerText.includes('Violet'));
        return {
            page: '14. /#/ayarlar/gorunum',
            passed: colorBtns.length >= 5,
            colorPaletteButtonsCount: colorBtns.length
        };
    """)
    print("R14:", r14)
    results.append(r14)

    # 15. Önbellek & Performans
    print("15. Önbellek & Performans...")
    navigate_by_click_or_reload('ayarlar/onbellek')
    r15 = client.eval_js("""
        const text = document.body.innerText;
        return {
            page: '15. /#/ayarlar/onbellek',
            passed: text.includes('Önbellek') || text.includes('Cache'),
            hasCacheText: text.includes('Önbellek') || text.includes('Cache')
        };
    """)
    print("R15:", r15)
    results.append(r15)

    # 16. Rol & İzin Yönetimi
    print("16. Rol & İzin Yönetimi...")
    navigate_by_click_or_reload('ayarlar/rol-izinleri')
    r16 = client.eval_js("""
        const table = document.querySelector('table');
        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
        return {
            page: '16. /#/ayarlar/rol-izinleri',
            passed: !!table && checkboxes.length > 5,
            matrixTableFound: !!table,
            checkboxesCount: checkboxes.length
        };
    """)
    print("R16:", r16)
    results.append(r16)

    # 17. 403 Güvenlik Duvarı
    print("17. 403 Güvenlik Duvarı Guard...")
    client.eval_js("""
        const musteriBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Müşteri'));
        if (musteriBtn) musteriBtn.click();
    """)
    time.sleep(0.3)
    navigate_by_click_or_reload('kullanici-yonetimi')
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
    print("R17:", r17)
    results.append(r17)

    print("\n=== FINAL 17 PAGES AUDIT REPORT ===")
    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    run_17_pages_click_audit()
