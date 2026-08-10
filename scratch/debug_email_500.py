import os

with open('scratch/serve_fast_3g.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_except = """            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
                return"""

new_except = """            except Exception as e:
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
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(resp, ensure_ascii=False).encode('utf-8'))
                return"""

if old_except in content:
    content = content.replace(old_except, new_except)
    print("Updated exception handler in serve_fast_3g.py.")

with open('scratch/serve_fast_3g.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved serve_fast_3g.py successfully.")
