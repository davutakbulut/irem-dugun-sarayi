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

    def reload_page(self):
        self.msg_id += 1
        cmd_id = self.msg_id
        req = {
            "id": cmd_id,
            "method": "Page.reload",
            "params": {"ignoreCache": True}
        }
        self.send_frame(json.dumps(req))
        time.sleep(2)

def test_home_navigation_and_f5():
    ws_url, page_id = get_websocket_url()
    cdp = SimpleCDP(ws_url)
    print("=== ANASAYFA GEÇİŞİ VE BEYAZ EKRAN/F5 YENİLEME TESTİ ===")
    
    # 1. Load #/yeni-rezervasyon
    cdp.execute_js("window.location.hash = '#/yeni-rezervasyon'")
    time.sleep(1.5)
    
    url_1 = cdp.execute_js("window.location.href")
    print(f"1. Sayfa Yüklendi: {url_1}")
    
    # 2. Click 'Anasayfa / İstatistikler' sidebar link
    print("2. Sol menüdeki 'Anasayfa / İstatistikler' linkine tıklanıyor...")
    cdp.execute_js("""
    (() => {
      const links = Array.from(document.querySelectorAll('a'));
      const homeLink = links.find(l => l.innerText.includes('Anasayfa / İstatistikler') || l.href.includes('anasayfa'));
      if (homeLink) homeLink.click();
    })()
    """)
    time.sleep(1.5)
    
    url_2 = cdp.execute_js("window.location.href")
    body_home = cdp.execute_js("document.body.innerText")
    
    is_blank_1 = len(body_home.strip()) < 50
    has_home_content = "Genel İstatistikler" in body_home or "Balo Salonu" in body_home or "Toplam Ciro" in body_home or "İrem Düğün Sarayı" in body_home
    
    print(f"   - Geçiş Yapılan URL: {url_2}")
    print(f"   - Beyaz Ekran Kontrolü: {'❌ BEYAZ EKRAN VAR' if is_blank_1 else '✅ BEYAZ EKRAN DEĞİL (Sorunsuz İçerik)'}")
    print(f"   - Anasayfa Bileşenleri Yüklendi Mi?: {'✅ EVET (İstatistikler ve Grafikler Yüklendi)' if has_home_content else '❌ HAYIR'}")

    # 3. Test F5 / Reload on Homepage
    print("\n3. F5 (Sayfa Yenileme) testi gerçekleştiriliyor...")
    cdp.reload_page()
    time.sleep(2)
    
    url_after_f5 = cdp.execute_js("window.location.href")
    body_after_f5 = cdp.execute_js("document.body.innerText")
    
    is_blank_f5 = len(body_after_f5.strip()) < 50
    has_home_f5 = "Genel İstatistikler" in body_after_f5 or "Balo Salonu" in body_after_f5 or "İrem Düğün Sarayı" in body_after_f5
    
    print(f"   - F5 Sonrası URL: {url_after_f5}")
    print(f"   - F5 Sonrası Beyaz Ekran Kontrolü: {'❌ BEYAZ EKRAN VAR' if is_blank_f5 else '✅ BEYAZ EKRAN OLUŞMADI (Sorunsuz Yüklendi)'}")
    print(f"   - F5 Sonrası Anasayfa Yüklenme Durumu: {'✅ TAM BAŞARILI' if has_home_f5 else '❌ BAŞARISIZ'}")

    # 4. Test '← Rezervasyon Listesine Dön' Button
    print("\n4. '#/yeni-rezervasyon' sayfasındaki '← Rezervasyon Listesine Dön' butonu test ediliyor...")
    cdp.execute_js("window.location.hash = '#/yeni-rezervasyon'")
    time.sleep(1.5)
    
    cdp.execute_js("""
    (() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const cancelBtn = btns.find(b => b.innerText.includes('Rezervasyon Listesine Dön'));
      if (cancelBtn) cancelBtn.click();
    })()
    """)
    time.sleep(1.5)
    
    url_res = cdp.execute_js("window.location.href")
    body_res = cdp.execute_js("document.body.innerText")
    has_res_content = "Rezervasyonlar" in body_res or "Tüm Rezervasyonlar" in body_res or "Sözleşme Detayı" in body_res
    
    print(f"   - Buton Sonrası URL: {url_res}")
    print(f"   - Rezervasyon Listesi Yüklendi Mi?: {'✅ EVET (Rezervasyonlar Ekranı Yüklendi)' if has_res_content else '❌ HAYIR'}")

    results = {
        "nav_url": url_2,
        "is_blank_on_nav": is_blank_1,
        "home_content_loaded": has_home_content,
        "f5_url": url_after_f5,
        "is_blank_on_f5": is_blank_f5,
        "f5_home_loaded": has_home_f5,
        "return_button_success": has_res_content
    }
    return results

if __name__ == "__main__":
    test_home_navigation_and_f5()
