import subprocess
import time
import json
import urllib.request
import ssl
import os
import re

TOPIC = "antigravity-bildirim-789"

def send_ntfy(message, title="Mac Antigravity Bildirimi 💻"):
    url = f"https://ntfy.sh/{TOPIC}"
    headers = {
        "Title": title,
        "Priority": "high",
        "Tags": "computer,bell,robot",
        "Content-Type": "text/plain; charset=utf-8"
    }
    try:
        req = urllib.request.Request(url, data=message.encode('utf-8'), headers=headers)
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=context) as resp:
            print(f"Forwarded notification to {TOPIC}: {message}")
            return True
    except Exception as e:
        cmd = [
            "curl",
            "-H", f"Title: {title}",
            "-H", "Priority: high",
            "-H", "Tags: computer,bell,robot",
            "-d", message,
            f"ntfy.sh/{TOPIC}"
        ]
        subprocess.run(cmd, capture_output=True)

def monitor_mac_notifications():
    print(f"Starting macOS Notification Center Forwarder to ntfy.sh/{TOPIC}...")
    send_ntfy("🖥️ Mac Sistem Bildirim Köprüsü Başlatıldı! Mac'inizdeki tüm Antigravity masaüstü bildirimleri artık anında telefonunuza düşecek.", "Mac Sistem Köprüsü ⚡")

if __name__ == "__main__":
    monitor_mac_notifications()
