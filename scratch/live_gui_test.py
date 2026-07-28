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

def run_live_gui_test():
    ws_url, page_id = get_websocket_url()
    cdp = SimpleCDP(ws_url)
    print("=== CANLI GÖRÜNÜR PENCERE TARAYICI OTOMASYON TESTİ BAŞLIYOR ===")
    
    # 1. Bring window to front / navigate to #/yeni-rezervasyon
    cdp.execute_js("window.focus()")
    cdp.execute_js("window.location.hash = '#/yeni-rezervasyon'")
    time.sleep(2)
    print("1. Chrome penceresinde http://localhost:3000/#/yeni-rezervasyon canlı olarak açıldı.")
    
    # 2. Click 'Otomatik Yeni Üyelik Oluştur' button
    cdp.execute_js("""
    (() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const newCustBtn = btns.find(b => b.innerText.includes('Otomatik Yeni Üyelik'));
      if (newCustBtn) newCustBtn.click();
    })()
    """)
    time.sleep(1.5)
    print("2. 'Otomatik Yeni Üyelik Oluştur' butonuna canlı olarak tıklandı.")
    
    # 3. Fill New Customer details visually
    cdp.execute_js("""
    (() => {
      const inputs = Array.from(document.querySelectorAll('input'));
      // Name
      const nameInput = inputs.find(i => i.placeholder && i.placeholder.includes('Mehmet Yılmaz'));
      if (nameInput) {
        let nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
        nativeSetter.call(nameInput, 'Zeynep & Emre Kaya (Canlı Test)');
        nameInput.dispatchEvent(new Event('input', { bubbles: true }));
      }
      // Email
      const emailInput = inputs.find(i => i.type === 'email');
      if (emailInput) {
        let nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
        nativeSetter.call(emailInput, 'zeynep.kaya@example.com');
        emailInput.dispatchEvent(new Event('input', { bubbles: true }));
      }
      // Phone
      const phoneInput = inputs.find(i => i.placeholder && i.placeholder.includes('532 000'));
      if (phoneInput) {
        let nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
        nativeSetter.call(phoneInput, '+90 532 999 8877');
        phoneInput.dispatchEvent(new Event('input', { bubbles: true }));
      }
    })()
    """)
    time.sleep(2)
    print("3. Yeni Müşteri Adı, E-posta ve Telefon alanları görünür şekilde dolduruldu.")
    
    # 4. Trigger Conflict Date (2026-08-15)
    print("4. Çakışan tarih (2026-08-15) seçiliyor ve ekrandaki canlı uyarı kartı bekleniyor...")
    cdp.execute_js("""
    (() => {
      const inputs = Array.from(document.querySelectorAll('input[type="date"]'));
      if(inputs.length > 0) {
        let nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
        nativeSetter.call(inputs[0], '2026-08-15');
        inputs[0].dispatchEvent(new Event('input', { bubbles: true }));
        inputs[0].dispatchEvent(new Event('change', { bubbles: true }));
      }
    })()
    """)
    time.sleep(3)
    
    # 5. Set Non-conflicting Date (2026-10-25)
    print("5. Müsait tarih (2026-10-25) seçiliyor ve yeşil onay kartı görünür yapılıyor...")
    cdp.execute_js("""
    (() => {
      const inputs = Array.from(document.querySelectorAll('input[type="date"]'));
      if(inputs.length > 0) {
        let nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
        nativeSetter.call(inputs[0], '2026-10-25');
        inputs[0].dispatchEvent(new Event('input', { bubbles: true }));
        inputs[0].dispatchEvent(new Event('change', { bubbles: true }));
      }
    })()
    """)
    time.sleep(2)
    
    # 6. Apply Promo Code 'IREM2026'
    print("6. Referans İndirim Kodu 'IREM2026' seçiliyor...")
    cdp.execute_js("""
    (() => {
      const selects = Array.from(document.querySelectorAll('select'));
      const campSelect = selects.find(s => Array.from(s.options).some(o => o.value === 'IREM2026'));
      if(campSelect) {
        let nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLSelectElement.prototype, "value").set;
        nativeSetter.call(campSelect, 'IREM2026');
        campSelect.dispatchEvent(new Event('change', { bubbles: true }));
      }
    })()
    """)
    time.sleep(2)
    
    # 7. Click 'Rezervasyonu ve Sözleşmeyi Kaydet' button
    print("7. 'Rezervasyonu ve Sözleşmeyi Kaydet' butonuna canlı görünür pencerede tıklanıyor...")
    cdp.execute_js("""
    (() => {
      const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Rezervasyonu ve Sözleşmeyi Kaydet'));
      if (btn) btn.click();
    })()
    """)
    time.sleep(2.5)
    
    current_url = cdp.execute_js("window.location.href")
    print(f"8. Canlı Test Tamamlandı. Yönlendirilen Ekran: {current_url}")
    return current_url

if __name__ == "__main__":
    run_live_gui_test()
