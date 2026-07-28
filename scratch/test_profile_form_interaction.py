import urllib.request
import json
import socket
import os
import base64
import struct
import time

def get_target():
    req = urllib.request.urlopen('http://localhost:9222/json/list')
    targets = json.loads(req.read().decode('utf-8'))
    for t in targets:
        if t.get('type') == 'page' and 'localhost:8000' in t.get('url', ''):
            return t['webSocketDebuggerUrl']
    for t in targets:
        if t.get('type') == 'page':
            return t['webSocketDebuggerUrl']
    raise Exception("No page target found")

class CDPClient:
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
                for i in range(len(payload)):
                    payload[i] ^= mask_key[i % 4]
            return payload.decode('utf-8', errors='ignore')
        except socket.timeout:
            return None

    def call(self, method, params=None, timeout=5.0):
        self.msg_id += 1
        msg_id = self.msg_id
        cmd = {"id": msg_id, "method": method}
        if params:
            cmd["params"] = params
        self.send_frame(json.dumps(cmd))
        start = time.time()
        while time.time() - start < timeout:
            raw = self.recv_frame(timeout=1.0)
            if raw:
                try:
                    data = json.loads(raw)
                    if data.get("id") == msg_id:
                        return data
                except Exception:
                    pass
        return None

    def eval_js(self, js_code):
        res = self.call("Runtime.evaluate", {"expression": f"(function() {{ {js_code} }})()", "returnByValue": True, "awaitPromise": True})
        if res and "result" in res and "result" in res["result"]:
            return res["result"]["result"].get("value")
        return None

def audit_profile_flow():
    ws_url = get_target()
    client = CDPClient(ws_url)

    print("Step 1: Clicking Profile Dropdown Button...")
    btn_click = client.eval_js("""
        const profileBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Profil'));
        if (profileBtn) {
            profileBtn.click();
            return true;
        }
        return false;
    """)
    print(f"Profile Dropdown Clicked: {btn_click}")
    time.sleep(0.3)

    print("Step 2: Clicking 'Profilimi Düzenle' Option...")
    option_click = client.eval_js("""
        const editOpt = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Profilimi Düzenle'));
        if (editOpt) {
            editOpt.click();
            return true;
        }
        return false;
    """)
    print(f"Edit Option Clicked: {option_click}")
    time.sleep(0.5)

    print(f"Current URL Hash: {client.eval_js('return window.location.hash;')}")

    print("\nStep 3: Verifying ProfileComponent UI Rendering...")
    profile_details = client.eval_js("""
        const headings = Array.from(document.querySelectorAll('h2, h3')).map(h => h.innerText);
        const labels = Array.from(document.querySelectorAll('label')).map(l => l.innerText);
        const inputs = Array.from(document.querySelectorAll('form input, form select')).map(i => ({
            tag: i.tagName,
            type: i.type || 'select',
            value: i.value,
            placeholder: i.placeholder || ''
        }));
        const buttons = Array.from(document.querySelectorAll('form button')).map(b => b.innerText);

        return {
            isProfileComponentRendered: headings.some(h => h.includes('İrem Yılmaz') || h.includes('Profil')),
            headings,
            labels,
            inputs,
            buttons
        };
    """)
    print("ProfileComponent Inspection:")
    print(json.dumps(profile_details, indent=2, ensure_ascii=False))

    print("\nStep 4: Testing Profile Form Submission...")
    sub_res = client.eval_js("""
        const nameInput = document.querySelector('form input[type="text"]');
        const emailInput = document.querySelector('form input[type="email"]');
        const phoneInput = document.querySelectorAll('form input[type="text"]')[1];
        const passInput = document.querySelector('form input[type="password"]');
        const roleSelect = document.querySelector('form select');
        const submitBtn = Array.from(document.querySelectorAll('form button')).find(b => b.innerText.includes('Kaydet') || b.innerText.includes('Güncelle'));

        if (!submitBtn) return { success: false, error: 'Submit button not found' };

        // Fill inputs
        if (nameInput) {
            nameInput.value = 'İrem Yılmaz (Yönetici)';
            nameInput.dispatchEvent(new Event('input', { bubbles: true }));
        }

        // Submit form
        submitBtn.click();
        return {
            success: true,
            submittedName: nameInput ? nameInput.value : null
        };
    """)
    print(f"Form Submission Result: {sub_res}")
    time.sleep(0.5)

    toast = client.eval_js("""
        const el = Array.from(document.querySelectorAll('div')).find(d => d.innerText && d.innerText.includes('Başarıyla Güncellendi'));
        return el ? el.innerText : null;
    """)
    print(f"Toast Message Verified: {toast}")

if __name__ == '__main__':
    audit_profile_flow()
