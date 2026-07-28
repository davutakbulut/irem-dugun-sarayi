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
        header.append(0x81) # FIN + text opcode
        
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

def run_tests():
    ws_url, page_id = get_websocket_url()
    cdp = SimpleCDP(ws_url)
    print("=== İREM DÜĞÜN SARAYI CANLI TARAYICI EKRAN VE İŞLEVSELLİK TESTİ ===")
    
    # 1. Page load & Role verification
    cdp.execute_js("window.location.hash = '#/yeni-rezervasyon'")
    time.sleep(1)
    
    url = cdp.execute_js("window.location.href")
    print(f"[TEST 1] Yüklenen URL: {url}")
    
    # Check sections presence
    body_text = cdp.execute_js("document.body.innerText")
    
    sections = [
        ("1. Salon & Kiralama Tarih/Saat Seçimi", "1. Salon Seçimi"),
        ("2. Müşteri İletişim & Otomatik Üyelik Kartı", "2. Otomatik Üyelik Oluşturma / Müşteri Bilgileri"),
        ("3. Alınan Ek Hizmetler & Hizmet Bazlı Kişi/Adet Sayıları", "3. Hizmet Kişi Sayıları"),
        ("4. Ödeme, Kapora & İndirim Kodu Bilgileri", "4. Kapora / Finans"),
        ("5. Fatura Bilgileri (Resmi Belge Düzenleme)", "5. Fatura Bilgileri (TC/VKN)"),
        ("6. Organizasyon & Etkinlik Akış Planlaması", "6. Akış Planlaması"),
        ("Takvim Canlı Ön İzlemesi", "7. Canlı Takvim Önizleme Kartı & Operasyonel Notlar")
    ]
    
    print("\n[TEST 2] 7 Ana Bölümün Yüklenme Doğrulaması:")
    sections_status = {}
    for title_check, name in sections:
        present = title_check in body_text
        sections_status[name] = present
        status_icon = "✅ EKSİKSİZ YÜKLENDİ" if present else "❌ EKSİK"
        print(f"  - {name}: {status_icon}")
        
    # Check TC / VKN and Auto membership elements specifically
    tc_present = "TC Kimlik No" in body_text or "Vergi Kimlik No (VKN)" in body_text
    print(f"  - Fatura detayları (TC / VKN alanları): {'✅ DOĞRULANDI' if tc_present else '❌ EKSİK'}")

    # 3. Test Collision Detection with conflicting date
    print("\n[TEST 3] Çakışan Tarih Seçim Uyarısı & Kaydet Buton Durumu Testi:")
    # Set date to existing reservation date '2026-08-15' (RES-2026-001 has date 2026-08-15, time 19:00-23:00, venue v1)
    script_set_collision = """
    (() => {
      // Find date input and set to 2026-08-15
      const inputs = Array.from(document.querySelectorAll('input[type="date"]'));
      if(inputs.length > 0) {
        let nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
        nativeSetter.call(inputs[0], '2026-08-15');
        inputs[0].dispatchEvent(new Event('input', { bubbles: true }));
        inputs[0].dispatchEvent(new Event('change', { bubbles: true }));
      }
      // Also ensure venue is v1
      const selects = Array.from(document.querySelectorAll('select'));
      if(selects.length > 0) {
        let nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLSelectElement.prototype, "value").set;
        nativeSetter.call(selects[0], 'v1');
        selects[0].dispatchEvent(new Event('change', { bubbles: true }));
      }
      return true;
    })()
    """
    cdp.execute_js(script_set_collision)
    time.sleep(1)
    
    body_after_collision = cdp.execute_js("document.body.innerText")
    has_collision_alert = "ÇAKIŞMA UYARISI" in body_after_collision and "BU SAAT DİLİMİ DOLUDUR" in body_after_collision
    print(f"  - Çakışma Uyarısı (⚠️ ÇAKIŞMA UYARISI / BU SAAT DİLİMİ DOLUDUR): {'✅ AKTİF UYARI VERDİ' if has_collision_alert else '❌ UYARI VERMEDİ'}")
    
    is_button_disabled = cdp.execute_js("""
    (() => {
      const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Rezervasyonu ve Sözleşmeyi Kaydet'));
      return btn ? btn.disabled : null;
    })()
    """)
    print(f"  - Kaydet Butonu Devre Dışı (Disabled) Durumu: {'✅ KİLİTLİ (disabled=true)' if is_button_disabled else '❌ KİLİTLİ DEĞİL'}")

    # 4. Test non-conflicting date & Successful Form Submission
    print("\n[TEST 4] Çakışmayan Tarih Seçimi & 'Rezervasyonu ve Sözleşmeyi Kaydet' İşlevsellik Testi:")
    script_set_valid = """
    (() => {
      const inputs = Array.from(document.querySelectorAll('input[type="date"]'));
      if(inputs.length > 0) {
        let nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
        nativeSetter.call(inputs[0], '2026-11-20');
        inputs[0].dispatchEvent(new Event('input', { bubbles: true }));
        inputs[0].dispatchEvent(new Event('change', { bubbles: true }));
      }
      return true;
    })()
    """
    cdp.execute_js(script_set_valid)
    time.sleep(1)
    
    body_after_valid = cdp.execute_js("document.body.innerText")
    has_available_status = "BU SAAT DİLİMİ MÜSAİTTİR" in body_after_valid
    print(f"  - Saat Dilimi Müsait Durumu (✅ BU SAAT DİLİMİ MÜSAİTTİR): {'✅ MÜSAİT OLARAK GÜNCELLENDİ' if has_available_status else '❌ GÜNCELLENMEDİ'}")
    
    is_button_enabled = cdp.execute_js("""
    (() => {
      const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Rezervasyonu ve Sözleşmeyi Kaydet'));
      return btn ? !btn.disabled : false;
    })()
    """)
    print(f"  - Kaydet Butonu Etkinlik (Enabled) Durumu: {'✅ TIKLANABİLİR (enabled=true)' if is_button_enabled else '❌ TIKLANAMAZ'}")
    
    # Click Save Reservation Button
    cdp.execute_js("""
    (() => {
      const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Rezervasyonu ve Sözleşmeyi Kaydet'));
      if (btn) btn.click();
    })()
    """)
    time.sleep(1.5)
    
    url_after_save = cdp.execute_js("window.location.href")
    print(f"  - Kaydetme Sonrası Yönlendirilen URL: {url_after_save}")
    submission_successful = '#/rezervasyonlar' in url_after_save
    print(f"  - Rezervasyon & Sözleşme Kaydetme Butonu İşlevselliği: {'✅ BAŞARIYLA ÇALIŞTI (Rezervasyonlar listesine yönlendirildi)' if submission_successful else '❌ BAŞARISIZ'}")
    
    report = {
        "url": url,
        "sections": sections_status,
        "collision_alert": has_collision_alert,
        "button_disabled_on_collision": is_button_disabled,
        "valid_slot_available": has_available_status,
        "button_enabled_on_valid": is_button_enabled,
        "save_and_redirect_success": submission_successful
    }
    
    return report

if __name__ == "__main__":
    res = run_tests()
    print("\n=== TEST SONUÇLARI ÖZETİ ===")
    print(json.dumps(res, indent=2, ensure_ascii=False))
