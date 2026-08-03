import sys
import json
import urllib.request
import urllib.parse
import ssl

def sanitize_header(val):
    return urllib.parse.quote(str(val), safe=" :!?,.()-/_")

def send_ntfy_notification(message, title="Irem Dugun Sarayi 🏰", priority="high", tags="party,tada,robot", topic="antigravity-bildirim-789"):
    url = f"https://ntfy.sh/{topic}"
    headers = {
        "Title": sanitize_header(title),
        "Priority": priority,
        "Tags": tags,
        "Content-Type": "text/plain; charset=utf-8"
    }
    
    try:
        req = urllib.request.Request(url, data=message.encode('utf-8'), headers=headers)
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=context) as resp:
            res_text = resp.read().decode('utf-8')
            print("ntfy.sh Notification Sent successfully via urllib:", res_text)
            return True
    except Exception as e:
        print("urllib notification exception:", e)
        return False

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "🎉 Antigravity işlemi başarıyla tamamlandı!"
    title_arg = sys.argv[2] if len(sys.argv) > 2 else "Irem Dugun Sarayi 🏰"
    send_ntfy_notification(msg, title=title_arg)
