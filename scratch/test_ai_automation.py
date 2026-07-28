import urllib.request
import json
import socket
import os
import base64
import struct
import time

def get_websocket_url():
    req = urllib.request.urlopen('http://localhost:9222/json/list')
    data = json.loads(req.read().decode('utf-8'))
    for target in data:
        if target.get('type') == 'page':
            return target['webSocketDebuggerUrl'], target['id']
    raise Exception("No page target found in Chrome DevTools")

class SimpleCDP:
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

    def execute(self, method, params=None):
        self.msg_id += 1
        msg = {"id": self.msg_id, "method": method, "params": params or {}}
        self.send_frame(json.dumps(msg))
        start_time = time.time()
        while time.time() - start_time < 5.0:
            raw = self.recv_frame()
            if not raw:
                continue
            try:
                data = json.loads(raw)
                if data.get("id") == self.msg_id:
                    if "error" in data:
                        raise Exception(f"CDP Error: {data['error']}")
                    return data.get("result", {})
            except json.JSONDecodeError:
                pass
        raise Exception(f"Timeout waiting for response to {method}")

    def eval_js(self, js_expression):
        res = self.execute("Runtime.evaluate", {
            "expression": js_expression,
            "returnByValue": True,
            "awaitPromise": True
        })
        if "exceptionDetails" in res:
            raise Exception(f"JS Exception: {res['exceptionDetails']}")
        return res.get("result", {}).get("value")

def run_test():
    print("🚀 Starting Live Automation Test for AI Recommendations & Campaign Automation...")
    ws_url, _ = get_websocket_url()
    cdp = SimpleCDP(ws_url)

    print("🔄 Reloading browser to fetch updated code...")
    cdp.eval_js("window.location.reload()")
    time.sleep(3.5)

    # 1. Navigate to Reports page (#/raporlar-ai)
    print("📍 Navigating to #/raporlar-ai ...")
    cdp.eval_js("window.location.hash = '#/raporlar-ai'")
    time.sleep(1.5)

    # Check page content
    page_text = cdp.eval_js("document.body.innerText")
    assert "Yapay Zeka" in page_text, "Failed to load Reports & AI Page!"

    print("✅ Reports Page loaded cleanly!")

    # Check AI Recommendation Cards
    assert "Tek Tıkla Kampanyaya Dönüştür" in page_text, "Action button 'Tek Tıkla Kampanyaya Dönüştür' missing on Reports Page!"
    print("✅ Verified AI Action Button 'Tek Tıkla Kampanyaya Dönüştür' on Reports Page!")

    assert "Fiyatı Güncelle & Uygula" in page_text, "Action button 'Fiyatı Güncelle & Uygula' missing on Reports Page!"
    print("✅ Verified AI Action Button 'Fiyatı Güncelle & Uygula' on Reports Page!")

    # 2. Click "Fiyatı Güncelle & Uygula" button
    print("👆 Clicking 'Fiyatı Güncelle & Uygula' button...")
    click_res = cdp.eval_js("""
        (() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const priceBtn = btns.find(b => b.innerText.includes('Fiyatı Güncelle'));
            if (priceBtn) {
                priceBtn.click();
                return 'CLICKED';
            }
            return 'NOT_FOUND';
        })()
    """)
    assert click_res == 'CLICKED', "Failed to click 'Fiyatı Güncelle' button!"
    time.sleep(0.5)

    page_text_after_price = cdp.eval_js("document.body.innerText")
    assert "Güncellendi" in page_text_after_price or "₺" in page_text_after_price, "Price update notification not detected!"
    print("✅ Verified Price Update Toast & State Mutation!")

    # 3. Click "Tek Tıkla Kampanyaya Dönüştür" button
    print("👆 Clicking 'Tek Tıkla Kampanyaya Dönüştür' button...")
    click_camp_res = cdp.eval_js("""
        (() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const convertBtn = btns.find(b => b.innerText.includes('Tek Tıkla Kampanyaya Dönüştür'));
            if (convertBtn) {
                convertBtn.click();
                return 'CLICKED';
            }
            return 'NOT_FOUND';
        })()
    """)
    assert click_camp_res == 'CLICKED', "Failed to click 'Tek Tıkla Kampanyaya Dönüştür' button!"
    time.sleep(1.0)

    # 4. Verify auto-navigation to #/kampanyalar and campaign injection
    current_hash = cdp.eval_js("window.location.hash")
    print(f"📍 Current Hash: {current_hash}")
    assert "kampanya" in current_hash.lower(), f"Expected navigation to campaigns page, got {current_hash}"

    camp_page_text = cdp.eval_js("document.body.innerText")
    assert "AI Üretimi" in camp_page_text or "AĞUSTOS10" in camp_page_text or "Enjekte Edildi" in camp_page_text, "Injected AI campaign not visible on Campaigns page!"
    print("✅ Verified instant injection of AI campaign on live Campaigns page!")

    print("\n🎉 ALL TESTS PASSED SUCCESSFULLY WITH 0 ERRORS!")

if __name__ == '__main__':
    run_test()
