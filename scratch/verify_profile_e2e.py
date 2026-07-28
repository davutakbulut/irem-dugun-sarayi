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

def verify_full_profile():
    ws_url = get_target()
    client = CDPClient(ws_url)

    report = {
        "test_name": "Profile Route & Component Verification",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "steps": []
    }

    # Step 1: Open Dropdown
    s1 = client.eval_js("""
        const profileBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Profil'));
        if (profileBtn) {
            profileBtn.click();
            return { clicked: true };
        }
        return { clicked: false };
    """)
    time.sleep(0.3)
    report["steps"].append({ "step": 1, "description": "Profil Dropdown Click", "result": s1 })

    # Step 2: Click 'Profilimi Düzenle'
    s2 = client.eval_js("""
        const editOpt = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Profilimi Düzenle'));
        if (editOpt) {
            editOpt.click();
            return { clicked: true, hash: window.location.hash };
        }
        return { clicked: false };
    """)
    time.sleep(0.5)
    report["steps"].append({ "step": 2, "description": "Profilimi Düzenle Option Click & Hash Change", "result": s2 })

    # Step 3: Audit ProfileComponent Form Fields
    s3 = client.eval_js("""
        const form = document.querySelector('form');
        if (!form) return { rendered: false };

        const nameInput = document.querySelector('form input[type="text"]');
        const emailInput = document.querySelector('form input[type="email"]');
        const phoneInput = document.querySelectorAll('form input[type="text"]')[1];
        const avatarInput = document.querySelectorAll('form input[type="text"]')[2];
        const passInput = document.querySelector('form input[type="password"]');
        const roleSelect = document.querySelector('form select');
        const submitBtn = Array.from(document.querySelectorAll('form button')).find(b => b.innerText.includes('Kaydet') || b.innerText.includes('Güncelle'));

        return {
            rendered: true,
            initialData: {
                name: nameInput ? nameInput.value : null,
                email: emailInput ? emailInput.value : null,
                phone: phoneInput ? phoneInput.value : null,
                avatar: avatarInput ? avatarInput.value : null,
                passwordPlaceholder: passInput ? passInput.placeholder : null,
                selectedRole: roleSelect ? roleSelect.value : null,
                roleOptionsCount: roleSelect ? roleSelect.options.length : 0,
                hasSubmitButton: !!submitBtn
            }
        };
    """)
    report["steps"].append({ "step": 3, "description": "ProfileComponent Form Inspection", "result": s3 })

    # Step 4: Perform Form Edit & Submit Test
    s4 = client.eval_js("""
        const nameInput = document.querySelector('form input[type="text"]');
        const emailInput = document.querySelector('form input[type="email"]');
        const phoneInput = document.querySelectorAll('form input[type="text"]')[1];
        const passInput = document.querySelector('form input[type="password"]');
        const roleSelect = document.querySelector('form select');
        const submitBtn = Array.from(document.querySelectorAll('form button')).find(b => b.innerText.includes('Kaydet') || b.innerText.includes('Güncelle'));

        if (!submitBtn) return { success: false, reason: 'Submit button missing' };

        // 1. Update Name
        nameInput.value = 'İrem Yılmaz (Başkan)';
        nameInput.dispatchEvent(new Event('input', { bubbles: true }));

        // 2. Update Email
        emailInput.value = 'irem.yilmaz@iremdugunsarayi.com';
        emailInput.dispatchEvent(new Event('input', { bubbles: true }));

        // 3. Update Phone
        phoneInput.value = '+90 532 999 8877';
        phoneInput.dispatchEvent(new Event('input', { bubbles: true }));

        // 4. Update Password
        passInput.value = 'YeniGuvenliSifre2026!';
        passInput.dispatchEvent(new Event('input', { bubbles: true }));

        // 5. Submit
        submitBtn.click();

        return {
            success: true,
            newValues: {
                name: nameInput.value,
                email: emailInput.value,
                phone: phoneInput.value
            }
        };
    """)
    time.sleep(0.5)
    report["steps"].append({ "step": 4, "description": "Form Modification & Submission", "result": s4 })

    # Step 5: Verify Toast Notification & Header State Update
    s5 = client.eval_js("""
        const toastEl = document.querySelector('[role="status"]');
        const headerName = document.querySelector('h2');
        return {
            toastMessage: toastEl ? toastEl.innerText : null,
            updatedHeaderName: headerName ? headerName.innerText : null
        };
    """)
    report["steps"].append({ "step": 5, "description": "Toast Alert & Dynamic Header Verification", "result": s5 })

    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    verify_full_profile()
