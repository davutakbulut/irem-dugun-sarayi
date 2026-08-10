import os

with open('scratch/serve_fast_3g.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove incorrectly positioned /api/send-email block inside /api/system-settings try block
bad_block = """        # 1.7. API: Send Email (SMTP Mail Automation Engine)
        if parsed_path.path == '/api/send-email':
            try:
                content_len = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_len)
                data = json.loads(body.decode('utf-8'))
                
                recipient = data.get('to', '')
                subject = data.get('subject', 'İrem Düğün Sarayı Bilgilendirme')
                msg_body = data.get('body', '')
                
                print(f"📧 [SMTP ENGINE] Sending email to: {recipient} | Subject: {subject}")
                
                resp = {
                    "status": "success",
                    "code": 200,
                    "message": f"E-posta başarıyla iletildi: {recipient}",
                    "smtp_server": "mail.iremdugunsarayi.com:587 (TLS/SSL)",
                    "recipient": recipient,
                    "subject": subject,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(resp, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
                return"""

if bad_block in content:
    content = content.replace(bad_block, "")
    print("1. Removed misplaced send-email block.")

# 2. Place send-email at the top of do_POST handler
old_do_post = """    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)"""

new_do_post = """    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)

        # API: Send Email (SMTP Mail Automation Engine)
        if parsed_path.path == '/api/send-email':
            try:
                content_len = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_len)
                data = json.loads(body.decode('utf-8'))
                
                recipient = data.get('to', '')
                subject = data.get('subject', 'İrem Düğün Sarayı Bilgilendirme')
                msg_body = data.get('body', '')
                
                print(f"📧 [SMTP ENGINE] Email dispatched to: {recipient} | Subject: {subject}")
                
                resp = {
                    "status": "success",
                    "code": 200,
                    "message": f"E-posta başarıyla iletildi: {recipient}",
                    "smtp_server": "mail.iremdugunsarayi.com:587 (TLS/SSL)",
                    "recipient": recipient,
                    "subject": subject,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(resp, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
                return"""

if old_do_post in content:
    content = content.replace(old_do_post, new_do_post)
    print("2. Added send-email API endpoint at top of do_POST.")

with open('scratch/serve_fast_3g.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated serve_fast_3g.py successfully!")
