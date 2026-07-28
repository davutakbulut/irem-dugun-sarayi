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

def test_6_new_updates():
    ws_url, page_id = get_websocket_url()
    cdp = SimpleCDP(ws_url)
    print("=== YENİ 6 GÜNCELLEME OTOMASYON TESTİ ===")
    
    # Wait for DOM to render
    for _ in range(10):
        body_len = cdp.execute_js("document.body.innerText.length")
        if body_len and body_len > 100:
            break
        time.sleep(1)
        
    cdp.execute_js("window.location.hash = '#/yeni-rezervasyon'")
    time.sleep(1)
    
    # Update 1: 4 Venues Check
    check_venues_script = """
    (() => {
      const headings = Array.from(document.querySelectorAll('h4')).map(h => h.innerText);
      const images = Array.from(document.querySelectorAll('img')).map(i => i.src).filter(s => s.includes('unsplash'));
      return {
        venueNames: headings,
        count: headings.length,
        has4Venues: headings.length === 4,
        allImagesValid: images.length >= 4
      };
    })()
    """
    v_res = cdp.execute_js(check_venues_script)
    print("1. 4 Salon Kapak Görselleri Kontrolü:")
    print(f"   - Yüklenen Salon Sayısı: {v_res['count']}")
    print(f"   - Salon İsimleri: {v_res['venueNames']}")
    print(f"   - Yüksek Çözünürlüklü Görseller Render Oldu Mu?: {'✅ EVET' if v_res['allImagesValid'] else '❌ HAYIR'}")

    # Update 2: Start/End Date & Time + Calendar Preview
    check_dateTime_script = """
    (() => {
      const dates = Array.from(document.querySelectorAll('input[type="date"]')).map(i => i.value);
      const times = Array.from(document.querySelectorAll('input[type="time"]')).map(i => i.value);
      const calendarText = document.body.innerText.includes('Canlı Takvim & Çakışma Önizlemesi');
      return {
        startDate: dates[0] || '',
        endDate: dates[1] || '',
        startTime: times[0] || '',
        endTime: times[1] || '',
        hasCalendarPreview: calendarText
      };
    })()
    """
    dt_res = cdp.execute_js(check_dateTime_script)
    print("\n2. Etkinlik Başlangıç / Bitiş (Tarih & Saat) ve Canlı Takvim Kontrolü:")
    print(f"   - Başlangıç: {dt_res['startDate']} {dt_res['startTime']}")
    print(f"   - Bitiş: {dt_res['endDate']} {dt_res['endTime']}")
    print(f"   - Canlı Takvim Önizleme Kartı Çalışıyor Mu?: {'✅ EVET' if dt_res['hasCalendarPreview'] else '❌ HAYIR'}")

    # Update 3: Section 2 Auto-Membership Default & Searchable Combobox
    check_section2_script = """
    (() => {
      const bodyText = document.body.innerText;
      const autoNewMemberMsg = bodyText.includes('Bu kişi için sistemde otomatik olarak yeni üye ve müşteri kartı oluşturulacaktır.');
      const btns = Array.from(document.querySelectorAll('button'));
      const existingBtn = btns.find(b => b.innerText.includes('Müşteri Rehberinden Seç'));
      return {
        autoNewMemberDefault: autoNewMemberMsg,
        hasExistingBtn: !!existingBtn
      };
    })()
    """
    s2_res = cdp.execute_js(check_section2_script)
    print("\n3. Section 2 Otomatik Üyelik Varsayılan ve Combobox Kontrolü:")
    print(f"   - 'Otomatik Yeni Üyelik Oluştur' Varsayılan Seçili Mi?: {'✅ EVET' if s2_res['autoNewMemberDefault'] else '❌ HAYIR'}")
    
    # Click 'Müşteri Rehberinden Seç' to test Searchable Combobox
    cdp.execute_js("""
    (() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const existingBtn = btns.find(b => b.innerText.includes('Müşteri Rehberinden Seç'));
      if (existingBtn) existingBtn.click();
    })()
    """)
    time.sleep(1)
    
    search_combobox_res = cdp.execute_js("""
    (() => {
      const searchInput = document.querySelector('input[placeholder*="Ad, Soyad, Telefon"]');
      return !!searchInput;
    })()
    """)
    print(f"   - Searchable Combobox Arama Inputu Açıldı Mı?: {'✅ EVET' if search_combobox_res else '❌ HAYIR'}")

    # Switch back to 'new' mode
    cdp.execute_js("""
    (() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const newBtn = btns.find(b => b.innerText.includes('Otomatik Yeni Üyelik Oluştur'));
      if (newBtn) newBtn.click();
    })()
    """)
    time.sleep(0.5)

    # Update 4: Section 3 Unchecked Paid Badge ("Ödenmedi")
    check_section3_script = """
    (() => {
      const bodyText = document.body.innerText;
      const hasOdenmediBadge = bodyText.includes('Ödenmedi');
      return hasOdenmediBadge;
    })()
    """
    s3_res = cdp.execute_js(check_section3_script)
    print("\n4. Section 3 Tiklenmeyen Hizmette Gri 'Ödenmedi' Rozeti Kontrolü:")
    print(f"   - Gri 'Ödenmedi' Rozeti Görüntülendi Mi?: {'✅ EVET' if s3_res else '❌ HAYIR'}")

    # Update 5: Section 4 Referrer Name Input
    check_section4_script = """
    (() => {
      const input = document.querySelector('input[placeholder*="Ahmet Yılmaz (Organizasyon Koçu"]');
      return !!input;
    })()
    """
    s4_res = cdp.execute_js(check_section4_script)
    print("\n5. Section 4 'Referans / Aracılık Eden (İsim Soyisim)' Input Kontrolü:")
    print(f"   - Referans Input Alanı Eklendi Mi?: {'✅ EVET' if s4_res else '❌ HAYIR'}")

    # Update 6: Section 5 Faturalı İşlem Default Unchecked
    check_section5_script = """
    (() => {
      const invoices = Array.from(document.querySelectorAll('input[type="checkbox"]'));
      const invoiceCb = invoices.find(i => i.parentElement && i.parentElement.innerText.includes('Faturalı İşlem'));
      return {
        hasInvoiceCb: !!invoiceCb,
        isUncheckedByDefault: invoiceCb ? !invoiceCb.checked : false
      };
    })()
    """
    s5_res = cdp.execute_js(check_section5_script)
    print("\n6. Section 5 Faturalı İşlem Kutusu Kontrolü:")
    print(f"   - Faturalı İşlem Kutusu Var Mı?: {'✅ EVET' if s5_res['hasInvoiceCb'] else '❌ HAYIR'}")
    print(f"   - Varsayılanlarak Tiksiz (Unchecked) Geldi Mi?: {'✅ EVET' if s5_res['isUncheckedByDefault'] else '❌ HAYIR'}")

    all_passed = all([
        v_res['has4Venues'],
        dt_res['hasCalendarPreview'],
        s2_res['autoNewMemberDefault'],
        search_combobox_res,
        s3_res,
        s4_res,
        s5_res['isUncheckedByDefault']
    ])

    report = {
        "venues_4_ok": v_res['has4Venues'],
        "datetime_calendar_ok": dt_res['hasCalendarPreview'],
        "section2_auto_member_and_combobox_ok": s2_res['autoNewMemberDefault'] and search_combobox_res,
        "section3_unpaid_badge_ok": s3_res,
        "section4_referrer_input_ok": s4_res,
        "section5_invoice_unchecked_ok": s5_res['isUncheckedByDefault'],
        "status": "PASSED" if all_passed else "FAILED"
    }
    print(f"\n=== TEST SONUÇLARI ===\n{json.dumps(report, indent=2, ensure_ascii=False)}")
    return report

if __name__ == "__main__":
    test_6_new_updates()
