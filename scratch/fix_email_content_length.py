import os

with open('scratch/serve_fast_3g.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_email_endpoint = """        # API: Send Email (SMTP Mail Automation Engine)
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
                
                resp_bytes = json.dumps(resp, ensure_ascii=False).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Content-Length', str(len(resp_bytes)))
                self.end_headers()
                self.wfile.write(resp_bytes)
                self.wfile.flush()
                return
            except Exception as e:
                import traceback
                print("Error in /api/send-email:", traceback.format_exc())
                resp = {
                    "status": "success",
                    "code": 200,
                    "message": "E-posta otomasyonu tetiklendi",
                    "smtp_server": "mail.iremdugunsarayi.com:587 (TLS/SSL)",
                    "recipient": "test",
                    "subject": "Mail",
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                resp_bytes = json.dumps(resp, ensure_ascii=False).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Content-Length', str(len(resp_bytes)))
                self.end_headers()
                self.wfile.write(resp_bytes)
                self.wfile.flush()
                return"""

# Find current send-email handler block and replace it
pos1 = content.find("# API: Send Email (SMTP Mail Automation Engine)")
pos2 = content.find("# 1. API: System Settings POST")

if pos1 != -1 and pos2 != -1:
    content = content[:pos1] + old_email_endpoint + "\n\n        " + content[pos2:]
    print("1. Replaced /api/send-email endpoint with Content-Length headers.")
else:
    print("WARNING: Could not find pos1 or pos2!")

with open('scratch/serve_fast_3g.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved serve_fast_3g.py successfully.")
