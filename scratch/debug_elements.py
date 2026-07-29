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
        if target.get('type') == 'page' and 'localhost:8000' in target.get('url', ''):
            return target['webSocketDebuggerUrl'], target['id']
    for target in data:
        if target.get('type') == 'page':
            return target['webSocketDebuggerUrl'], target['id']
    raise Exception("No page target found")

class SimpleCDP:
    def __init__(self, ws_url):
        host_port = ws_url.replace('ws://', '').split('/')[0]
        host, port = host_port.split(':')
        self.path = '/' + '/'.join(ws_url.replace('ws://', '').split('/')[1:])
        self.sock = socket.create_connection((host, int(port)), timeout=2.0)
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

    def recv_frame(self, timeout=0.5):
        self.sock.settimeout(timeout)
        try:
            buf = bytearray()
            while len(buf) < 2:
                chunk = self.sock.recv(2 - len(buf))
                if not chunk: return None
                buf.extend(chunk)
            payload_len = buf[1] & 0x7F
            if payload_len == 126:
                payload_len = struct.unpack("!H", self.sock.recv(2))[0]
            elif payload_len == 127:
                payload_len = struct.unpack("!Q", self.sock.recv(8))[0]
            if buf[1] & 0x80:
                mask_key = self.sock.recv(4)
            payload = bytearray()
            while len(payload) < payload_len:
                chunk = self.sock.recv(payload_len - len(payload))
                if not chunk: break
                payload.extend(chunk)
            if buf[1] & 0x80:
                payload = bytearray(b ^ mask_key[i % 4] for i, b in enumerate(payload))
            return payload.decode('utf-8', errors='ignore')
        except Exception:
            return None

    def send_cdp_cmd(self, method, params=None):
        self.msg_id += 1
        cmd_id = self.msg_id
        req = {"id": cmd_id, "method": method, "params": params or {}}
        self.send_frame(json.dumps(req))
        start_time = time.time()
        while time.time() - start_time < 5.0:
            frame = self.recv_frame(timeout=0.2)
            if frame:
                try:
                    res = json.loads(frame)
                    if res.get("id") == cmd_id:
                        return res
                except Exception:
                    pass
        return None

    def eval_js(self, js_code):
        wrapped = f"(function() {{\n{js_code}\n}})()"
        res = self.send_cdp_cmd("Runtime.evaluate", {
            "expression": wrapped,
            "returnByValue": True,
            "awaitPromise": True
        })
        if res and "result" in res:
            if "result" in res["result"]:
                return res["result"]["result"].get("value")
            if "exceptionDetails" in res["result"]:
                print("JS ERR:", res["result"]["exceptionDetails"])
        return None

def debug():
    ws_url, _ = get_websocket_url()
    cdp = SimpleCDP(ws_url)
    cdp.send_cdp_cmd("Emulation.setDeviceMetricsOverride", {
        "width": 390,
        "height": 844,
        "deviceScaleFactor": 3,
        "mobile": True
    })
    
    print("Navigating via Page.navigate...")
    cdp.send_cdp_cmd("Page.navigate", {"url": "http://localhost:8000/#/rezervasyon-olustur"})
    
    print("Waiting for React mount...")
    mounted = False
    for i in range(15):
        time.sleep(1)
        root_children = cdp.eval_js("return document.getElementById('root') ? document.getElementById('root').children.length : 0;")
        text_len = cdp.eval_js("return document.body.innerText ? document.body.innerText.length : 0;")
        print(f"[{i+1}s] root children: {root_children}, text length: {text_len}")
        if root_children and root_children > 0 and text_len and text_len > 100:
            mounted = True
            break
            
    print("REACT MOUNTED:", mounted)
    if mounted:
        matches = cdp.eval_js("""
          const result = [];
          document.querySelectorAll('*').forEach(el => {
            if (el.innerText && (el.innerText.includes('Detaylar') || el.innerText.includes('Net Bakiye'))) {
              const rect = el.getBoundingClientRect();
              const style = window.getComputedStyle(el);
              result.push({
                tag: el.tagName,
                className: el.className,
                position: style.position,
                display: style.display,
                bottom: style.bottom,
                rectBottom: rect.bottom,
                textSnippet: el.innerText.substring(0, 50).replace(/\\s+/g, ' ')
              });
            }
          });
          return result;
        """)
        print("MATCHES FOUND:", json.dumps(matches, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    debug()
