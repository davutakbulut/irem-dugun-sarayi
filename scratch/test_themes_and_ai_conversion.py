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

def run_tests():
    ws_url = get_target()
    client = CDPClient(ws_url)

    # 1. Reload page
    client.call("Page.navigate", {"url": "http://localhost:8000/"})
    time.sleep(1.2)

    # Test 1: Theme palettes in Ayarlar > Görünüm
    print("Testing 1. Theme Palettes in Ayarlar > Görünüm ...")
    client.eval_js("window.location.hash = '#/ayarlar/gorunum'; window.dispatchEvent(new Event('hashchange'));")
    time.sleep(0.8)

    t1_res = client.eval_js("""
        const buttons = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('#') || b.innerText.includes('rounded-'));
        const sharpBadges = Array.from(document.querySelectorAll('span')).filter(s => s.innerText.includes('rounded-')).map(s => s.innerText.trim());
        const themeNames = Array.from(document.querySelectorAll('.font-extrabold')).map(e => e.innerText.trim()).filter(t => t.includes('👑') || t.includes('💎') || t.includes('⬛') || t.includes('🪙') || t.includes('⚡') || t.includes('🌲'));

        // Click Obsidian Gold theme button
        const obsidianBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Obsidian'));
        if (obsidianBtn) obsidianBtn.click();

        const goldVar = getComputedStyle(document.documentElement).getPropertyValue('--color-gold').trim();

        return {
            themesFoundCount: themeNames.length,
            themeNamesSample: themeNames,
            sharpBadgesCount: sharpBadges.length,
            sharpBadgesSample: sharpBadges,
            obsidianBtnClicked: !!obsidianBtn,
            activeGoldVarColor: goldVar
        };
    """)
    print("Test 1 Result:", json.dumps(t1_res, indent=2, ensure_ascii=False))

    # Test 2: AI Suggestion Conversion in Raporlar & AI
    print("\nTesting 2. AI Suggestion Conversion in Raporlar & AI ...")
    client.eval_js("window.location.hash = '#/raporlar-ai'; window.dispatchEvent(new Event('hashchange'));")
    time.sleep(0.8)

    t2_res = client.eval_js("""
        const convertBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Tek Tıkla Kampanyaya Dönüştür'));
        if (convertBtn) {
            convertBtn.click();
            return { convertBtnFound: true };
        }
        return { convertBtnFound: false };
    """)
    time.sleep(0.8)

    t2_verify = client.eval_js("""
        const currentHash = window.location.hash;
        const text = document.body.innerText;
        const aiCampaignCard = text.includes('Salı/Çarşamba') || text.includes('AI Fırsat') || text.includes('Doluluk Fırsatı');
        const toast = document.querySelector('.fixed.bottom-5');

        return {
            convertBtnClicked: true,
            currentRoute: currentHash,
            redirectedToCampaigns: currentHash === '#/kampanyalar',
            aiCampaignAddedToState: aiCampaignCard,
            toastText: toast ? toast.innerText : null
        };
    """)
    print("Test 2 Result:", json.dumps(t2_verify, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    run_tests()
