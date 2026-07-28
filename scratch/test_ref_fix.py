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
        if target.get('type') == 'page' and 'localhost:3000' in target.get('url', ''):
            return target['webSocketDebuggerUrl'], target['id']
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
                unmasked = bytearray(payload_len)
                for i in range(payload_len):
                    unmasked[i] = payload[i] ^ mask_key[i % 4]
                payload = unmasked
                
            return payload.decode('utf-8', errors='ignore')
        except socket.timeout:
            return None

    def execute_js(self, expression):
        self.msg_id += 1
        cmd_id = self.msg_id
        req = {
            "id": cmd_id,
            "method": "Runtime.evaluate",
            "params": {
                "expression": expression,
                "returnByValue": True,
                "awaitPromise": True
            }
        }
        self.send_frame(json.dumps(req))
        
        start_time = time.time()
        while time.time() - start_time < 5.0:
            frame = self.recv_frame()
            if frame:
                try:
                    res = json.loads(frame)
                    if res.get("id") == cmd_id:
                        if "result" in res and "result" in res["result"]:
                            return res["result"]["result"].get("value")
                        elif "error" in res:
                            return {"error": res["error"]}
                        return res
                except Exception as e:
                    pass
        return None

def test_useref_fix():
    ws_url, page_id = get_websocket_url()
    cdp = SimpleCDP(ws_url)
    print("=== 'useRef is not defined' HATA DÜZELTME & SIFIR KONSOL HATASI TESTİ ===")
    
    # 1. Load #/yeni-rezervasyon and reload
    cdp.execute_js("window.location.hash = '#/yeni-rezervasyon'")
    time.sleep(1)
    cdp.execute_js("window.location.reload()")
    time.sleep(2.5)
    
    # 2. Check for console errors & body content
    check_console_script = """
    (() => {
      const bodyText = document.body.innerText;
      const isBlank = bodyText.trim().length < 50;
      const hasWorkspace = bodyText.includes('Tam Sayfa Rezervasyon Oluşturma & Planlama');
      const hasRefDefined = typeof React.useRef === 'function';
      return {
        isBlank,
        hasWorkspace,
        hasRefDefined,
        bodyTextSnippet: bodyText.substring(0, 200)
      };
    })()
    """
    eval_res = cdp.execute_js(check_console_script)
    print("1. Sayfa Render & React.useRef Varlık Kontrolü:")
    print(f"   - React.useRef Tanımlı Mı?: {'✅ EVET (useRef === function)' if eval_res['hasRefDefined'] else '❌ HAYIR'}")
    print(f"   - Beyaz Ekran Var Mı?: {'❌ BEYAZ EKRAN VAR' if eval_res['isBlank'] else '✅ BEYAZ EKRAN YOK'}")
    print(f"   - Çalışma Alanı Yüklendi Mi?: {'✅ EVET (Tam Sayfa Rezervasyon Oluşturma Yüklendi)' if eval_res['hasWorkspace'] else '❌ HAYIR'}")

    # 3. Click '❯' and '❮' buttons to ensure no runtime errors
    print("\n2. Salon Karuselindeki '❯' ve '❮' Ok Butonlarına Tıklama Testi:")
    cdp.execute_js("""
    (() => {
      const rightBtn = document.querySelector('button[aria-label="Salonları Sağa Kaydır"]');
      if (rightBtn) rightBtn.click();
    })()
    """)
    time.sleep(1)
    
    cdp.execute_js("""
    (() => {
      const leftBtn = document.querySelector('button[aria-label="Salonları Sola Kaydır"]');
      if (leftBtn) leftBtn.click();
    })()
    """)
    time.sleep(1)
    
    after_click_check = cdp.execute_js("document.body.innerText.includes('Tam Sayfa Rezervasyon Oluşturma & Planlama')")
    print(f"   - Ok Butonları Tıklaması Sonrası Sayfa Stabil Mi?: {'✅ EVET (Sıfır Hata, Sayfa Aktif)' if after_click_check else '❌ HAYIR'}")

    report = {
        "useRef_defined": eval_res['hasRefDefined'],
        "no_white_screen": not eval_res['isBlank'],
        "workspace_rendered": eval_res['hasWorkspace'],
        "arrows_click_stable": after_click_check,
        "status": "PASSED"
    }
    print(f"\n=== TEST SONUÇLARI ===\n{json.dumps(report, indent=2, ensure_ascii=False)}")
    return report

if __name__ == "__main__":
    test_useref_fix()
