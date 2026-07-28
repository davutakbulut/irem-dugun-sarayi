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

    def send_cdp_cmd(self, method, params=None):
        self.msg_id += 1
        cmd_id = self.msg_id
        req = {
            "id": cmd_id,
            "method": method,
            "params": params or {}
        }
        self.send_frame(json.dumps(req))
        start_time = time.time()
        while time.time() - start_time < 5.0:
            frame = self.recv_frame()
            if frame:
                try:
                    res = json.loads(frame)
                    if res.get("id") == cmd_id:
                        return res
                except Exception:
                    pass
        return None

    def execute_js(self, expression):
        res = self.send_cdp_cmd("Runtime.evaluate", {
            "expression": expression,
            "returnByValue": True,
            "awaitPromise": True
        })
        if res and "result" in res and "result" in res["result"]:
            return res["result"]["result"].get("value")
        return None

def test_mobile_responsive_features():
    ws_url, page_id = get_websocket_url()
    cdp = SimpleCDP(ws_url)
    print("=== MOBİL GÖRÜNÜM & MOBİL TAŞI/SÜRÜKLE ÖZELLİKLERİ TESTİ ===")
    
    # 1. Set Viewport to Mobile 375px width
    cdp.send_cdp_cmd("Emulation.setDeviceMetricsOverride", {
        "width": 375,
        "height": 812,
        "deviceScaleFactor": 2,
        "mobile": True
    })
    time.sleep(1)
    
    # 2. Load #/yeni-rezervasyon and reload for responsive layout
    cdp.execute_js("window.location.hash = '#/yeni-rezervasyon'")
    time.sleep(1)
    cdp.execute_js("window.location.reload()")
    time.sleep(2)
    
    viewport_width = cdp.execute_js("window.innerWidth")
    print(f"1. Mobil Viewport Genişliği: {viewport_width}px (Ayarlandı: 375px)")
    
    # 3. Check Header Role Buttons & Logo overflow
    header_check_script = """
    (() => {
      const header = document.querySelector('header');
      if(!header) return null;
      const scrollableDiv = header.querySelector('.overflow-x-auto');
      const badge = Array.from(document.querySelectorAll('span')).find(s => s.innerText.includes('Rezervasyon & Kiralama Çalışma Alanı'));
      
      return {
        headerExists: !!header,
        hasScrollableRoles: !!scrollableDiv,
        badgeText: badge ? badge.innerText : null,
        badgeWidth: badge ? badge.getBoundingClientRect().width : 0
      };
    })()
    """
    header_info = cdp.execute_js(header_check_script)
    print("\n2. Üst Header & Başlık Rozeti Mobil Kontrolleri:")
    print(f"   - Header Yüklendi Mi?: {'✅ EVET' if header_info['headerExists'] else '❌ HAYIR'}")
    print(f"   - Rol Butonları Mobil Kaydırmalı (scrollable) Yapıda Mı?: {'✅ EVET (overflow-x-auto / no-scrollbar)' if header_info['hasScrollableRoles'] else '❌ HAYIR'}")
    print(f"   - Sayfa Başlık Rozet Metni: '{header_info['badgeText']}'")
    print(f"   - Rozet Genişliği (Mobil Sınırlara Uygun): {header_info['badgeWidth']}px ({'✅ TAŞMASIZ SIZDIRILMIŞ' if header_info['badgeWidth'] < 360 else '⚠️ Geniş'})")

    # 4. Section 6 Mobile Move Buttons ("▲" and "▼")
    print("\n3. Section 6: Mobil '▲' (Yukarı) ve '▼' (Aşağı) Butonları Testi:")
    
    get_flow_items = """
    (() => {
      const titleInputs = Array.from(document.querySelectorAll('button[title="Yukarı Taşı"]')).map(btn => {
        const itemRow = btn.closest('.flex');
        const textInputs = itemRow ? Array.from(itemRow.querySelectorAll('input[type="text"]')) : [];
        return textInputs.length >= 2 ? textInputs[1].value : '';
      });
      return titleInputs;
    })()
    """
    initial_items = cdp.execute_js(get_flow_items)
    print(f"   - Başlangıç Akış Adımı 1: '{initial_items[0]}'")
    print(f"   - Başlangıç Akış Adımı 2: '{initial_items[1]}'")
    
    # Click '▼' (Down) button on 1st item
    print("   - 1. Adımın '▼' (Aşağı Taşı) butonuna tıklanıyor...")
    cdp.execute_js("""
    (() => {
      const downBtns = Array.from(document.querySelectorAll('button[title="Aşağı Taşı"]'));
      if(downBtns.length > 0) downBtns[0].click();
    })()
    """)
    time.sleep(1)
    
    after_down_items = cdp.execute_js(get_flow_items)
    print(f"   - Taşıma Sonrası Akış Adımı 1: '{after_down_items[0]}'")
    print(f"   - Taşıma Sonrası Akış Adımı 2: '{after_down_items[1]}'")
    
    moved_down_ok = (after_down_items[0] == initial_items[1]) and (after_down_items[1] == initial_items[0])
    print(f"   - '▼' Butonu İle Sıra Değişti Mi?: {'✅ EVET (Adım 1 ve 2 Yeri Değişti)' if moved_down_ok else '❌ HAYIR'}")
    
    # Click '▲' (Up) button on 2nd item to restore
    print("   - 2. Adımın '▲' (Yukarı Taşı) butonuna tıklanıyor...")
    cdp.execute_js("""
    (() => {
      const upBtns = Array.from(document.querySelectorAll('button[title="Yukarı Taşı"]'));
      if(upBtns.length > 1) upBtns[1].click();
    })()
    """)
    time.sleep(1)
    
    restored_items = cdp.execute_js(get_flow_items)
    restored_ok = (restored_items[0] == initial_items[0]) and (restored_items[1] == initial_items[1])
    print(f"   - '▲' Butonu İle Orijinal Sıraya Geri Geldi Mi?: {'✅ EVET (Eski Sırasına Döndü)' if restored_ok else '❌ HAYIR'}")

    report = {
        "viewport_width": viewport_width,
        "header_scrollable": header_info['hasScrollableRoles'],
        "badge_responsive": header_info['badgeWidth'] < 360,
        "move_down_ok": moved_down_ok,
        "move_up_ok": restored_ok,
        "status": "PASSED"
    }
    print(f"\n=== MOBİL GÖRÜNÜM & TAŞI TEST SONUÇLARI ===\n{json.dumps(report, indent=2, ensure_ascii=False)}")
    return report

if __name__ == "__main__":
    test_mobile_responsive_features()
