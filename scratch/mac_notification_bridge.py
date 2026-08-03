import os
import sys
import time
import subprocess
import json
import urllib.request
import ssl

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
            print(f"Sent notification to {TOPIC}: {message}")
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

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "Mac Antigravity bildirim köprüsü aktif!"
    title_arg = sys.argv[2] if len(sys.argv) > 2 else "Mac Antigravity Sistem Bildirimi 💻"
    send_ntfy(msg, title=title_arg)
