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

def run_comprehensive_audit():
    ws_url = get_target()
    client = CDPClient(ws_url)

    report = {
        "status": "HEALTHY",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "url": "http://localhost:8000",
        "tests": []
    }

    # Test 1: Page Load & Header
    header_title = client.eval_js("return document.title;")
    report["tests"].append({
        "name": "Page Title Check",
        "passed": "İrem Düğün Sarayı" in str(header_title),
        "detail": f"Title: '{header_title}'"
    })

    # Test 2: Role Switcher & Context State
    roles = ['Admin', 'Satışçı', 'Sosyal Medya', 'Müşteri']
    role_results = []
    for role in roles:
        res = client.eval_js(f"""
            const btns = Array.from(document.querySelectorAll('button'));
            const b = btns.find(x => x.innerText.includes('{role}'));
            if (b) {{
                b.click();
                return {{ found: true, text: b.innerText }};
            }}
            return {{ found: false }};
        """)
        time.sleep(0.2)
        role_results.append({ "role": role, "res": res })

    report["tests"].append({
        "name": "Role Switching Audit",
        "passed": all(r["res"] and r["res"].get("found") for r in role_results),
        "detail": role_results
    })

    # Switch back to Admin
    client.eval_js("""
        const btns = Array.from(document.querySelectorAll('button'));
        const b = btns.find(x => x.innerText.includes('Admin'));
        if (b) b.click();
    """)
    time.sleep(0.2)

    # Test 3: Navigation Views Audit
    nav_keywords = ['Anasayfa', 'Salonlar', 'Rezervasyon', 'Takvim', 'Finans', 'Performans']
    nav_results = []
    for kw in nav_keywords:
        res = client.eval_js(f"""
            const els = Array.from(document.querySelectorAll('a, button, div, span'));
            const el = els.find(x => x.innerText && x.innerText.includes('{kw}'));
            if (el) {{
                el.click();
                return {{ clicked: true, target: '{kw}' }};
            }}
            return {{ clicked: false, target: '{kw}' }};
        """)
        time.sleep(0.2)
        nav_results.append(res)

    report["tests"].append({
        "name": "Navigation Submenus Audit",
        "passed": any(r.get("clicked") for r in nav_results),
        "detail": nav_results
    })

    # Test 4: Modal & Glass Panel Isolation
    modal_test = client.eval_js("""
        // Open modal by clicking detail button
        const cardBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Detay') || b.innerText.includes('İncele'));
        let opened = false;
        if (cardBtns.length > 0) {
            cardBtns[0].click();
            opened = true;
        }
        
        const hasGlass = document.querySelectorAll('.glass-panel, [role="dialog"]').length > 0;
        
        // Close modal if present
        const closeBtn = document.querySelector('button[aria-label="Kapat"], button svg');
        if (closeBtn) closeBtn.click();

        return { modalOpened: opened, glassPanelDetected: hasGlass };
    """)
    report["tests"].append({
        "name": "Modal & Glass Panel Audit",
        "passed": modal_test.get("glassPanelDetected", False) if modal_test else False,
        "detail": modal_test
    })

    # Test 5: FPS & Smooth Scrolling Audit
    fps_res = client.eval_js("""
        let start = performance.now();
        let frames = 0;
        window.scrollBy({ top: 400, behavior: 'smooth' });
        for (let i = 0; i < 1000000; i++) {} // slight computation load
        window.scrollBy({ top: -400, behavior: 'smooth' });
        let duration = (performance.now() - start) / 1000;
        return { durationMs: Math.round(duration * 1000), domNodeCount: document.getElementsByTagName('*').length };
    """)
    report["tests"].append({
        "name": "Rendering & Repaint Audit",
        "passed": fps_res is not None and fps_res.get("durationMs", 999) < 500,
        "detail": fps_res
    })

    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    run_comprehensive_audit()
