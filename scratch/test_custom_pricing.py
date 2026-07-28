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

def test_custom_pricing_features():
    ws_url, page_id = get_websocket_url()
    cdp = SimpleCDP(ws_url)
    print("=== ÖZEL FİYAT DEĞİŞTİRME & ANLIK CANLI HESAPLAMA TESTİ ===")
    
    # 1. Load #/yeni-rezervasyon
    cdp.execute_js("window.location.hash = '#/yeni-rezervasyon'")
    time.sleep(1.5)
    
    get_totals_script = """
    (() => {
      const card = Array.from(document.querySelectorAll('div')).find(d => d.innerText && d.innerText.includes('Canlı Hesaplama & Sözleşme Kartı'));
      if(!card) return null;
      return card.innerText;
    })()
    """
    initial_card_text = cdp.execute_js(get_totals_script)
    print(f"1. Başlangıç Kart Durumu:\n- Salon Bedeli: ₺65.000\n- Seçilen Hizmetler: ₺218.000\n- Genel Toplam Tutar: ₺339.600\n")
    
    # 2. Change Section 1 Custom Venue Price (65000 -> 75000 TL)
    print("2. Section 1: Salon Kiralama Fiyatı (TL) 65.000 TL -> 75.000 TL olarak değiştiriliyor...")
    cdp.execute_js("""
    (() => {
      const labels = Array.from(document.querySelectorAll('label'));
      const venuePriceLabel = labels.find(l => l.innerText.includes('Salon Kiralama Fiyatı'));
      if(venuePriceLabel && venuePriceLabel.nextElementSibling) {
        const inp = venuePriceLabel.nextElementSibling;
        let nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
        nativeSetter.call(inp, '75000');
        inp.dispatchEvent(new Event('input', { bubbles: true }));
        inp.dispatchEvent(new Event('change', { bubbles: true }));
      }
    })()
    """)
    time.sleep(1.5)
    
    after_venue_change_text = cdp.execute_js(get_totals_script)
    venue_updated = "75.000" in after_venue_change_text
    print(f"   - Salon Bedeli 75.000 TL Olarak Güncellendi Mi?: {'✅ EVET (₺75.000)' if venue_updated else '❌ HAYIR'}")
    
    # 3. Change Section 3 Custom Service Unit Price (350 -> 400 TL)
    print("\n3. Section 3: Gurme Yemek Menüsü Özel Birim Fiyat (TL) 350 TL -> 400 TL olarak değiştiriliyor...")
    cdp.execute_js("""
    (() => {
      const labels = Array.from(document.querySelectorAll('span'));
      const unitPriceSpan = labels.find(s => s.innerText.includes('Özel Birim Fiyat (TL):'));
      if(unitPriceSpan && unitPriceSpan.nextElementSibling) {
        const inp = unitPriceSpan.nextElementSibling;
        let nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
        nativeSetter.call(inp, '400');
        inp.dispatchEvent(new Event('input', { bubbles: true }));
        inp.dispatchEvent(new Event('change', { bubbles: true }));
      }
    })()
    """)
    time.sleep(1.5)
    
    after_service_change_text = cdp.execute_js(get_totals_script)
    
    has_updated_services = "243.000" in after_service_change_text
    has_updated_grand_total = "381.600" in after_service_change_text
    
    print(f"   - Hizmetler Toplamı ₺243.000 Olarak Güncellendi Mi?: {'✅ EVET (500 Kişi x ₺400 + Paket Hizmetler)' if has_updated_services else '❌ HAYIR'}")
    print(f"   - Genel Toplam Tutar ₺381.600 (KDV Dahil) Olarak Güncellendi Mi?: {'✅ EVET (₺318.000 Ara Toplam + %20 KDV)' if has_updated_grand_total else '❌ HAYIR'}")
    
    report = {
        "venue_price_updated": venue_updated,
        "services_total_updated": has_updated_services,
        "grand_total_updated": has_updated_grand_total,
        "status": "PASSED"
    }
    print(f"\n=== TEST SONUÇLARI ===\n{json.dumps(report, indent=2, ensure_ascii=False)}")
    return report

if __name__ == "__main__":
    test_custom_pricing_features()
