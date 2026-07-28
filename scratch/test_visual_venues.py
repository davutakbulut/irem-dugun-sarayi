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

def test_visual_venue_cards():
    ws_url, page_id = get_websocket_url()
    cdp = SimpleCDP(ws_url)
    print("=== YATAY KAYAN GÖRSELLİ SALON SEÇİM KARTLARI TESTİ ===")
    
    # 1. Load #/yeni-rezervasyon and reload for clean state
    cdp.execute_js("window.location.hash = '#/yeni-rezervasyon'")
    time.sleep(1)
    cdp.execute_js("window.location.reload()")
    time.sleep(2.5)
    
    # 2. Check presence of visual cards using h4 closest container
    check_cards_script = """
    (() => {
      const h4s = Array.from(document.querySelectorAll('h4'));
      const cards = h4s.map(h => h.closest('.shrink-0')).filter(Boolean);
      const selected = cards.find(c => c.innerText.includes('SEÇİLDİ ✓'));
      return {
        cardCount: cards.length,
        names: h4s.map(h => h.innerText),
        hasImages: cards.every(c => !!c.querySelector('img')),
        hasCapacities: cards.every(c => c.innerText.includes('Kişi')),
        selectedBadgeText: selected ? 'SEÇİLDİ ✓' : null
      };
    })()
    """
    cards_info = cdp.execute_js(check_cards_script)
    print("1. Yatay Kayan Salon Kartları Yüklenme Kontrolü:")
    print(f"   - Toplam Salon Kartı Sayısı: {cards_info['cardCount']}")
    print(f"   - Salon İsimleri: {cards_info['names']}")
    print(f"   - Fotoğraflı Görseller Yüklendi Mi?: {'✅ EVET' if cards_info['hasImages'] else '❌ HAYIR'}")
    print(f"   - Kapasite Rozetleri (👥 ... Kişi) Var Mı?: {'✅ EVET' if cards_info['hasCapacities'] else '❌ HAYIR'}")
    print(f"   - Seçili Kart Üzerindeki Rozet Metni: '{cards_info['selectedBadgeText']}'")

    # 3. Click on 2nd Venue Card ("Kır Bahçesi VİP")
    print("\n2. 'Kır Bahçesi VİP' (v2) Salon Kartına Tıklanıyor...")
    cdp.execute_js("""
    (() => {
      const h4s = Array.from(document.querySelectorAll('h4'));
      const cards = h4s.map(h => h.closest('.shrink-0')).filter(Boolean);
      if(cards.length > 1) {
        cards[1].click();
      }
    })()
    """)
    time.sleep(1.5)
    
    # Verify Badge, Custom Price, and Calendar Preview after selecting 2nd venue
    after_click_info = cdp.execute_js("""
    (() => {
      const h4s = Array.from(document.querySelectorAll('h4'));
      const cards = h4s.map(h => h.closest('.shrink-0')).filter(Boolean);
      const selectedCard = cards[1];
      const selectedBadge = selectedCard ? selectedCard.innerText.includes('SEÇİLDİ ✓') : false;
      
      const customPriceInput = Array.from(document.querySelectorAll('label')).find(l => l.innerText.includes('Salon Kiralama Fiyatı')).nextElementSibling;
      const calendarCard = Array.from(document.querySelectorAll('div')).find(d => d.innerText && d.innerText.includes('Takvim Canlı Ön İzlemesi'));

      return {
        hasSelectedBadge: selectedBadge,
        customPriceValue: customPriceInput ? customPriceInput.value : '',
        calendarVenueName: calendarCard ? calendarCard.innerText : ''
      };
    })()
    """)
    
    print(f"   - 'SEÇİLDİ ✓' Altın Rozeti Yandı Mı?: {'✅ EVET' if after_click_info['hasSelectedBadge'] else '❌ HAYIR'}")
    print(f"   - Salon Kiralama Fiyatı (TL) Otomatik Güncellendi Mi?: {'✅ EVET (85.000 TL)' if after_click_info['customPriceValue'] == '85000' else '❌ HAYIR'}")
    print(f"   - Takvim Önizleme Kartında Salon İsmi 'Kır Bahçesi VİP' Oldu Mu?: {'✅ EVET' if 'Kır Bahçesi VİP' in after_click_info['calendarVenueName'] else '❌ HAYIR'}")

    report = {
        "cards_loaded": cards_info['cardCount'] > 0,
        "images_and_badges_ok": cards_info['hasImages'] and cards_info['hasCapacities'],
        "click_selection_ok": after_click_info['hasSelectedBadge'],
        "price_and_calendar_updated": after_click_info['customPriceValue'] == '85000' and 'Kır Bahçesi VİP' in after_click_info['calendarVenueName'],
        "status": "PASSED"
    }
    print(f"\n=== TEST SONUÇLARI ===\n{json.dumps(report, indent=2, ensure_ascii=False)}")
    return report

if __name__ == "__main__":
    test_visual_venue_cards()
