import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add qrcode and download icons to NordicSvgMap if not present
qrcode_svg = """  qrcode: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><rect x="3" y="3" width="7" height="7" /><rect x="14" y="3" width="7" height="7" /><rect x="3" y="14" width="7" height="7" /><rect x="14" y="14" width="3" height="3" /><rect x="18" y="18" width="3" height="3" /><rect x="18" y="14" width="3" height="3" /><rect x="14" y="18" width="3" height="3" /></svg>,
  download: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>,
  copy: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><rect x="9" y="9" width="13" height="13" rx="2" ry="2" /><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" /></svg>,
  video: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><polygon points="23 7 16 12 23 17 23 7" /><rect x="1" y="5" width="15" height="14" rx="2" ry="2" /></svg>,
  play: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="currentColor" viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3" /></svg>,"""

if "qrcode:" not in html:
    html = html.replace("  media: (props) =>", qrcode_svg + "\n  media: (props) =>")
    print("Added qrcode, download, copy, video, play SVG icons to index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html SVG map successfully!")
