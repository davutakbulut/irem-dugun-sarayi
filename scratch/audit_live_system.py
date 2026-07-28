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
        res = self.call("Runtime.evaluate", {"expression": js_code, "returnByValue": True, "awaitPromise": True})
        if res and "result" in res and "result" in res["result"]:
            return res["result"]["result"].get("value")
        return None

def audit():
    ws_url = get_target()
    print("Connecting to target:", ws_url)
    client = CDPClient(ws_url)
    
    # 1. Page Title & URL
    title = client.eval_js("document.title")
    print(f"[AUDIT 1] Page Title: {title}")
    
    # 2. Check React root mounted
    root_children = client.eval_js("document.getElementById('root').children.length")
    print(f"[AUDIT 2] React Root Children Count: {root_children}")
    
    # 3. Collect UI Elements
    buttons = client.eval_js("Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean)")
    print(f"[AUDIT 3] Found {len(buttons)} interactive buttons:")
    print("  Buttons sample:", buttons[:10])
    
    # 4. Check Navigation Tabs & Active View
    nav_tabs = client.eval_js("Array.from(document.querySelectorAll('nav a, nav button, header button')).map(el => el.innerText.trim()).filter(Boolean)")
    print(f"[AUDIT 4] Navigation items: {nav_tabs}")
    
    # 5. Check Modals
    client.eval_js("""
      // Try to click first detail/venue button to trigger modal
      const detailBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Detay') || b.innerText.includes('İncele') || b.innerText.includes('Düzenle'));
      if (detailBtns.length > 0) detailBtns[0].click();
    """)
    time.sleep(1)
    
    modal_present = client.eval_js("document.querySelectorAll('.fixed, [role=\"dialog\"], .glass-panel').length > 0")
    print(f"[AUDIT 5] Modal / Glass panel visible after click: {modal_present}")
    
    # Close modal if open
    client.eval_js("""
      const closeBtn = document.querySelector('button[aria-label=\"Kapat\"], button svg, .fixed button');
      if (closeBtn) closeBtn.click();
    """)
    time.sleep(0.5)
    
    # 6. Scroll Performance & Repaint Audit
    scroll_res = client.eval_js("""
      (async () => {
        let fpsSamples = [];
        let lastTime = performance.now();
        let frameCount = 0;

        const countFrame = (now) => {
          frameCount++;
          if (now - lastTime >= 100) {
            fpsSamples.push((frameCount * 1000) / (now - lastTime));
            frameCount = 0;
            lastTime = now;
          }
        };

        let rafId;
        const measure = (now) => {
          countFrame(now);
          rafId = requestAnimationFrame(measure);
        };
        rafId = requestAnimationFrame(measure);

        // Perform smooth scrolling sequence
        for (let i = 0; i < 5; i++) {
          window.scrollBy({ top: 300, behavior: 'smooth' });
          await new Promise(r => setTimeout(r, 100));
        }
        for (let i = 0; i < 5; i++) {
          window.scrollBy({ top: -300, behavior: 'smooth' });
          await new Promise(r => setTimeout(r, 100));
        }

        cancelAnimationFrame(rafId);
        const avgFps = fpsSamples.reduce((a, b) => a + b, 0) / (fpsSamples.length || 1);
        return { avgFps: Math.round(avgFps), sampleCount: fpsSamples.length };
      })()
    """)
    print(f"[AUDIT 6] Scroll Performance: {scroll_res}")
    
    # 7. Check Console Errors
    console_errors = client.eval_js("window.__console_errors || []")
    print(f"[AUDIT 7] Console Errors Recorded: {console_errors}")
    
    # 8. Memory & DOM stats
    dom_count = client.eval_js("document.getElementsByTagName('*').length")
    print(f"[AUDIT 8] Total DOM Nodes: {dom_count}")

if __name__ == '__main__':
    audit()
