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

    def wait_for_dom(self, max_seconds=4.0):
        start = time.time()
        while time.time() - start < max_seconds:
            mounted = self.eval_js("return document.getElementById('root') && document.getElementById('root').children.length > 0 && document.body.innerText.length > 50;")
            if mounted:
                return True
            time.sleep(0.3)
        return False

def audit_17_pages_proper_wait():
    ws_url = get_target()
    client = CDPClient(ws_url)

    # Initial page reload
    client.call("Page.navigate", {"url": "http://localhost:8000/"})
    client.wait_for_dom()
    client.eval_js("localStorage.removeItem('tab_permissions');")

    pages = [
        {"id": 1, "title": "1. Anasayfa (Dashboard)", "slug": "anasayfa"},
        {"id": 2, "title": "2. Yeni Rezervasyon", "slug": "yeni-rezervasyon"},
        {"id": 3, "title": "3. Düğün Salonları", "slug": "dugun-salonlari", "modalBtn": "Yeni Düğün Salonu Ekle", "badge": "1200x800"},
        {"id": 4, "title": "4. Ek Hizmetler", "slug": "ek-hizmetler", "modalBtn": "Yeni Ek Hizmet Ekle", "badge": "600x400"},
        {"id": 5, "title": "5. Rezervasyonlar", "slug": "rezervasyonlar"},
        {"id": 6, "title": "6. Takvim", "slug": "takvim"},
        {"id": 7, "title": "7. Kampanyalar", "slug": "kampanyalar", "modalBtn": "Yeni Özel Kampanya Ekle"},
        {"id": 8, "title": "8. Finans", "slug": "finans"},
        {"id": 9, "title": "9. Müşteri Rehberi", "slug": "musteri-rehberi"},
        {"id": 10, "title": "10. Kullanıcı Yönetimi", "slug": "kullanici-yonetimi", "modalBtn": "Yeni Kullanıcı Tanımla", "badge": "400x400"},
        {"id": 11, "title": "11. Raporlar & AI Öneri", "slug": "raporlar-ai"},
        {"id": 12, "title": "12. Medya Galerisi", "slug": "medya-yukle", "badge": "1920x1080"},
        {"id": 13, "title": "13. Profil", "slug": "profil", "badge": "400x400"},
        {"id": 14, "title": "14. Görünüm & Tema", "slug": "ayarlar/gorunum"},
        {"id": 15, "title": "15. Önbellek & Performans", "slug": "ayarlar/onbellek"},
        {"id": 16, "title": "16. Rol & İzin Yönetimi (RBAC)", "slug": "ayarlar/rol-izinleri"},
        {"id": 17, "title": "17. 403 Güvenlik Duvarı Guard", "slug": "kullanici-yonetimi", "guardTest": True}
    ]

    report = []

    for p in pages:
        print(f"Testing {p['title']} ...")
        
        if p.get("guardTest"):
            client.eval_js("""
                const mBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Müşteri'));
                if (mBtn) mBtn.click();
            """)
            time.sleep(0.3)

        client.eval_js(f"window.location.hash = '#/{p['slug']}'; window.dispatchEvent(new Event('hashchange'));")
        time.sleep(0.5)

        if p.get("modalBtn"):
            client.eval_js(f"""
                const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes("{p['modalBtn']}"));
                if (btn) btn.click();
            """)
            time.sleep(0.4)

        eval_code = """
            const text = document.body.innerText;
            const modal = document.querySelector('.fixed, [role="dialog"]');
            const fileInput = document.querySelector('input[type="file"]');
            const badgeEl = Array.from(document.querySelectorAll('span, div')).find(el => el.innerText && el.innerText.includes('""" + (p.get("badge") or "XYZ_NONE") + """'));
            
            return {
                title: '""" + p['title'] + """',
                textSnippet: text.substring(0, 150).replace(/\\n/g, ' '),
                domNodesCount: document.getElementsByTagName('*').length,
                modalOpened: !!modal,
                fileInputFound: !!fileInput,
                badgeFound: !!badgeEl
            };
        """

        res = client.eval_js(eval_code)
        
        # Close modal if opened
        if p.get("modalBtn"):
            client.eval_js("""
                const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('İptal') || b.innerText.includes('✕'));
                if (cancelBtn) cancelBtn.click();
            """)
            time.sleep(0.3)

        # Restore Admin if guard test ran
        if p.get("guardTest"):
            client.eval_js("""
                const aBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Admin'));
                if (aBtn) aBtn.click();
            """)

        print(res)
        report.append(res)

    print("\n=== FINAL 17 PAGES PROPER AUDIT REPORT ===")
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    audit_17_pages_proper_wait()
