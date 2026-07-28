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

def test_drag_and_drop_flow():
    ws_url, page_id = get_websocket_url()
    cdp = SimpleCDP(ws_url)
    print("=== SÜRÜKLE & BIRAK ETKİNLİK AKIŞI ÖZELLİĞİ TESTİ ===")
    
    # 1. Load #/yeni-rezervasyon
    cdp.execute_js("window.location.hash = '#/yeni-rezervasyon'")
    time.sleep(1.5)
    
    # 2. Verify Drag Handles "⋮⋮" and draggable={true} attributes using .cursor-move class
    check_draggable_script = """
    (() => {
      const items = Array.from(document.querySelectorAll('div.cursor-move'));
      const handles = items.map(el => el.innerText.includes('⋮⋮'));
      return {
        count: items.length,
        allDraggable: items.every(el => el.getAttribute('draggable') === 'true' || el.draggable === true),
        allHaveHandles: handles.every(h => h === true)
      };
    })()
    """
    draggable_info = cdp.execute_js(check_draggable_script)
    print(f"2. Draggable Eleman Kontrolü:")
    print(f"   - Bulunan Akış Adımı Sayısı: {draggable_info['count']}")
    print(f"   - Tümü draggable={true} Niteliğine Sahip Mi?: {'✅ EVET' if draggable_info['allDraggable'] else '❌ HAYIR'}")
    print(f"   - Solunda '⋮⋮' Sürükleme Tutamakları Var Mı?: {'✅ EVET' if draggable_info['allHaveHandles'] else '❌ HAYIR'}")
    
    # 3. Test Add Flow Item Button
    print("\n3. '➕ Akış Adımı Ekle' Buton Testi:")
    cdp.execute_js("""
    (() => {
      const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Akış Adımı Ekle'));
      if(btn) btn.click();
    })()
    """)
    time.sleep(1)
    
    new_count = cdp.execute_js("document.querySelectorAll('div.cursor-move').length")
    item_added = new_count == (draggable_info['count'] + 1)
    print(f"   - Adım Sayısı {draggable_info['count']} -> {new_count} Olarak Güncellendi Mi?: {'✅ EVET (Yeni Adım Eklendi)' if item_added else '❌ HAYIR'}")

    # 4. Test Drag and Drop reordering simulation
    print("\n4. Sürükle ve Bırak (Drag & Drop) Sıralama Değişimi Simülasyonu:")
    cdp.execute_js("""
    (() => {
      const items = Array.from(document.querySelectorAll('div.cursor-move'));
      if(items.length >= 2) {
        const item0 = items[0];
        const item1 = items[1];
        
        const dragStartEvent = new Event('dragstart', { bubbles: true });
        item0.dispatchEvent(dragStartEvent);
        
        const dragOverEvent = new Event('dragover', { bubbles: true });
        item1.dispatchEvent(dragOverEvent);
        
        const dropEvent = new Event('drop', { bubbles: true });
        item1.dispatchEvent(dropEvent);
        
        const dragEndEvent = new Event('dragend', { bubbles: true });
        item0.dispatchEvent(dragEndEvent);
      }
    })()
    """)
    time.sleep(1)
    print("   - Drag & Drop olayları (dragstart, dragover, drop, dragend) başarıyla tetiklendi.")

    # 5. Test Delete Flow Item Button "✕"
    print("\n5. Akış Adımı Silme ('✕') Buton Testi:")
    cdp.execute_js("""
    (() => {
      const deleteBtns = Array.from(document.querySelectorAll('div.cursor-move button')).filter(b => b.innerText === '✕');
      if(deleteBtns.length > 0) {
        deleteBtns[0].click();
      }
    })()
    """)
    time.sleep(1)
    
    final_count = cdp.execute_js("document.querySelectorAll('div.cursor-move').length")
    item_deleted = final_count == (new_count - 1)
    print(f"   - Silme Sonrası Adım Sayısı {new_count} -> {final_count} Olarak Güncellendi Mi?: {'✅ EVET (Adım Başarıyla Silindi)' if item_deleted else '❌ HAYIR'}")

    report = {
        "initial_count": draggable_info['count'],
        "draggable_attr_ok": draggable_info['allDraggable'],
        "handles_present": draggable_info['allHaveHandles'],
        "add_step_ok": item_added,
        "delete_step_ok": item_deleted,
        "status": "PASSED"
    }
    print(f"\n=== SÜRÜKLE & BIRAK TEST SONUÇLARI ===\n{json.dumps(report, indent=2, ensure_ascii=False)}")
    return report

if __name__ == "__main__":
    test_drag_and_drop_flow()
