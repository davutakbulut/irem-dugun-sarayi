import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Expand NordicSvgMap with all missing icons and enforce 100% SVG rendering in ThemeIcon
old_theme_icon = """    function ThemeIcon({ icon, fallbackEmoji, activeTheme, className = "w-4 h-4" }) {
      const domTheme = typeof document !== 'undefined' ? document.documentElement.getAttribute('data-ui-theme') : null;
      const rawTheme = activeTheme || domTheme || 'gold';

      const isVectorTheme = domTheme === 'nordic-light' || rawTheme === 'nordic-light' || domTheme === 'apple' || rawTheme === 'apple';

      const SvgComponent = NordicSvgMap[icon];
      if (SvgComponent) {
        return <SvgComponent className={className} />;
      }

      if (isVectorTheme) {
        return (
          <svg className={className || "w-4 h-4 inline-block shrink-0"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
            <path strokeLinecap="round" strokeLinejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
      }

      if (ThemeConceptEmojis[icon] && ThemeConceptEmojis[icon][rawTheme]) {
        return <span className="inline-block emoji-fallback">{ThemeConceptEmojis[icon][rawTheme]}</span>;
      }
      return <span className="inline-block emoji-fallback">{fallbackEmoji}</span>;
    }"""

new_theme_icon = """    function ThemeIcon({ icon, fallbackEmoji, activeTheme, className = "w-4 h-4" }) {
      const SvgComponent = NordicSvgMap[icon];
      if (SvgComponent) {
        return <SvgComponent className={className} />;
      }
      return (
        <svg className={className || "w-4 h-4 inline-block shrink-0"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
          <path strokeLinecap="round" strokeLinejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      );
    }"""

if old_theme_icon in content:
    content = content.replace(old_theme_icon, new_theme_icon)
    print("1. Enforced 100% SVG rendering in ThemeIcon (Zero Emoji Fallback).")
else:
    print("WARNING: Could not find old_theme_icon exact match in index.html!")

# 2. Add extra icon keys to NordicSvgMap
extra_nordic_svgs = """      users: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" /></svg>,
      mobile: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><rect x="5" y="2" width="14" height="20" rx="2" ry="2" /><line x1="12" y1="18" x2="12.01" y2="18" /></svg>,
      file: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M13 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V9z" /><polyline points="13 2 13 9 20 9" /></svg>,
      tag: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" /></svg>,
      info: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><circle cx="12" cy="12" r="10" /><line x1="12" y1="16" x2="12" y2="12" /><line x1="12" y1="8" x2="12.01" y2="8" /></svg>,"""

nordic_map_target = "    const NordicSvgMap = {"
if nordic_map_target in content:
    content = content.replace(nordic_map_target, nordic_map_target + "\n" + extra_nordic_svgs)
    print("2. Added users, mobile, file, tag, info SVG definitions to NordicSvgMap.")

# 3. Replace all inline hardcoded text emojis with ThemeIcon SVG elements
emoji_replacements = [
    ("🏰", '<ThemeIcon icon="venue" className="w-4 h-4 inline-block shrink-0" />'),
    ("🛠️", '<ThemeIcon icon="settings" className="w-4 h-4 inline-block shrink-0" />'),
    ("🛠", '<ThemeIcon icon="settings" className="w-4 h-4 inline-block shrink-0" />'),
    ("📝", '<ThemeIcon icon="document" className="w-4 h-4 inline-block shrink-0" />'),
    ("💰", '<ThemeIcon icon="money" className="w-4 h-4 inline-block shrink-0" />'),
    ("👥", '<ThemeIcon icon="users" className="w-4 h-4 inline-block shrink-0" />'),
    ("👤", '<ThemeIcon icon="user" className="w-4 h-4 inline-block shrink-0" />'),
    ("👑", '<ThemeIcon icon="crown" className="w-4 h-4 inline-block shrink-0" />'),
    ("📄", '<ThemeIcon icon="document" className="w-4 h-4 inline-block shrink-0" />'),
    ("📜", '<ThemeIcon icon="flow" className="w-4 h-4 inline-block shrink-0" />'),
    ("📅", '<ThemeIcon icon="calendar" className="w-4 h-4 inline-block shrink-0" />'),
    ("🗓️", '<ThemeIcon icon="calendar" className="w-4 h-4 inline-block shrink-0" />'),
    ("🗓", '<ThemeIcon icon="calendar" className="w-4 h-4 inline-block shrink-0" />'),
    ("📆", '<ThemeIcon icon="calendar" className="w-4 h-4 inline-block shrink-0" />'),
    ("📌", '<ThemeIcon icon="location" className="w-4 h-4 inline-block shrink-0" />'),
    ("📍", '<ThemeIcon icon="location" className="w-4 h-4 inline-block shrink-0" />'),
    ("⚡", '<ThemeIcon icon="zap" className="w-4 h-4 inline-block shrink-0" />'),
    ("🔒", '<ThemeIcon icon="lock" className="w-4 h-4 inline-block shrink-0" />'),
    ("🔐", '<ThemeIcon icon="lock" className="w-4 h-4 inline-block shrink-0" />'),
    ("🔑", '<ThemeIcon icon="key" className="w-4 h-4 inline-block shrink-0" />'),
    ("✅", '<ThemeIcon icon="check-circle" className="w-4 h-4 inline-block shrink-0" />'),
    ("✔️", '<ThemeIcon icon="check" className="w-4 h-4 inline-block shrink-0" />'),
    ("☑️", '<ThemeIcon icon="check-circle" className="w-4 h-4 inline-block shrink-0" />'),
    ("❌", '<ThemeIcon icon="x-circle" className="w-4 h-4 inline-block shrink-0" />'),
    ("✖️", '<ThemeIcon icon="close" className="w-4 h-4 inline-block shrink-0" />'),
    ("🚫", '<ThemeIcon icon="warning" className="w-4 h-4 inline-block shrink-0" />'),
    ("🛑", '<ThemeIcon icon="warning" className="w-4 h-4 inline-block shrink-0" />'),
    ("⭐", '<ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" />'),
    ("★", '<ThemeIcon icon="star" className="w-4 h-4 inline-block shrink-0" />'),
    ("🎯", '<ThemeIcon icon="target" className="w-4 h-4 inline-block shrink-0" />'),
    ("🏷️", '<ThemeIcon icon="campaign" className="w-4 h-4 inline-block shrink-0" />'),
    ("🏷", '<ThemeIcon icon="campaign" className="w-4 h-4 inline-block shrink-0" />'),
    ("📞", '<ThemeIcon icon="phone" className="w-4 h-4 inline-block shrink-0" />'),
    ("📱", '<ThemeIcon icon="mobile" className="w-4 h-4 inline-block shrink-0" />'),
    ("✉️", '<ThemeIcon icon="email" className="w-4 h-4 inline-block shrink-0" />'),
    ("✉", '<ThemeIcon icon="email" className="w-4 h-4 inline-block shrink-0" />'),
    ("📩", '<ThemeIcon icon="email" className="w-4 h-4 inline-block shrink-0" />'),
    ("⏰", '<ThemeIcon icon="clock" className="w-4 h-4 inline-block shrink-0" />'),
    ("⏳", '<ThemeIcon icon="clock" className="w-4 h-4 inline-block shrink-0" />'),
    ("⏱️", '<ThemeIcon icon="clock" className="w-4 h-4 inline-block shrink-0" />'),
    ("📸", '<ThemeIcon icon="camera" className="w-4 h-4 inline-block shrink-0" />'),
    ("📷", '<ThemeIcon icon="camera" className="w-4 h-4 inline-block shrink-0" />'),
    ("🎉", '<ThemeIcon icon="celebrate" className="w-4 h-4 inline-block shrink-0" />'),
    ("🥂", '<ThemeIcon icon="celebrate" className="w-4 h-4 inline-block shrink-0" />'),
    ("🎁", '<ThemeIcon icon="gift" className="w-4 h-4 inline-block shrink-0" />'),
    ("💼", '<ThemeIcon icon="briefcase" className="w-4 h-4 inline-block shrink-0" />'),
    ("🏢", '<ThemeIcon icon="building" className="w-4 h-4 inline-block shrink-0" />'),
    ("🏛️", '<ThemeIcon icon="building" className="w-4 h-4 inline-block shrink-0" />'),
    ("🏛", '<ThemeIcon icon="building" className="w-4 h-4 inline-block shrink-0" />'),
    ("🧹", '<ThemeIcon icon="trash" className="w-4 h-4 inline-block shrink-0" />'),
    ("🗑️", '<ThemeIcon icon="trash" className="w-4 h-4 inline-block shrink-0" />'),
    ("🗑", '<ThemeIcon icon="trash" className="w-4 h-4 inline-block shrink-0" />'),
    ("🔧", '<ThemeIcon icon="settings" className="w-4 h-4 inline-block shrink-0" />'),
    ("⚙️", '<ThemeIcon icon="settings" className="w-4 h-4 inline-block shrink-0" />'),
    ("⚙", '<ThemeIcon icon="settings" className="w-4 h-4 inline-block shrink-0" />'),
    ("💡", '<ThemeIcon icon="idea" className="w-4 h-4 inline-block shrink-0" />'),
    ("🚀", '<ThemeIcon icon="rocket" className="w-4 h-4 inline-block shrink-0" />'),
    ("🛡️", '<ThemeIcon icon="shield" className="w-4 h-4 inline-block shrink-0" />'),
    ("🛡", '<ThemeIcon icon="shield" className="w-4 h-4 inline-block shrink-0" />'),
    ("💬", '<ThemeIcon icon="chat" className="w-4 h-4 inline-block shrink-0" />'),
    ("🧾", '<ThemeIcon icon="document" className="w-4 h-4 inline-block shrink-0" />'),
    ("💳", '<ThemeIcon icon="card" className="w-4 h-4 inline-block shrink-0" />'),
    ("⚠️", '<ThemeIcon icon="warning" className="w-4 h-4 inline-block text-amber-500 shrink-0" />'),
    ("⚠", '<ThemeIcon icon="warning" className="w-4 h-4 inline-block text-amber-500 shrink-0" />'),
    ("🚨", '<ThemeIcon icon="warning" className="w-4 h-4 inline-block text-red-500 shrink-0" />'),
    ("🔍", '<ThemeIcon icon="search" className="w-4 h-4 inline-block shrink-0" />'),
    ("✨", '<ThemeIcon icon="sparkles" className="w-4 h-4 inline-block text-amber-500 shrink-0" />'),
    ("📊", '<ThemeIcon icon="chart" className="w-4 h-4 inline-block shrink-0" />'),
    ("📈", '<ThemeIcon icon="chart" className="w-4 h-4 inline-block shrink-0" />'),
    ("📉", '<ThemeIcon icon="chart" className="w-4 h-4 inline-block shrink-0" />'),
    ("🎨", '<ThemeIcon icon="paint" className="w-4 h-4 inline-block shrink-0" />'),
    ("📐", '<ThemeIcon icon="ruler" className="w-4 h-4 inline-block shrink-0" />'),
    ("📂", '<ThemeIcon icon="flow" className="w-4 h-4 inline-block shrink-0" />'),
    ("📁", '<ThemeIcon icon="flow" className="w-4 h-4 inline-block shrink-0" />'),
    ("📦", '<ThemeIcon icon="gift" className="w-4 h-4 inline-block shrink-0" />'),
    ("🔄", '<ThemeIcon icon="refresh" className="w-4 h-4 inline-block shrink-0" />'),
    ("👁️", '<ThemeIcon icon="eye" className="w-4 h-4 inline-block shrink-0" />'),
    ("👁", '<ThemeIcon icon="eye" className="w-4 h-4 inline-block shrink-0" />'),
    ("✏️", '<ThemeIcon icon="edit" className="w-4 h-4 inline-block shrink-0" />'),
    ("✏", '<ThemeIcon icon="edit" className="w-4 h-4 inline-block shrink-0" />'),
    ("➕", '<ThemeIcon icon="plus" className="w-4 h-4 inline-block shrink-0" />'),
    ("🔔", '<ThemeIcon icon="bell" className="w-4 h-4 inline-block shrink-0" />'),
    ("🚪", '<ThemeIcon icon="door" className="w-4 h-4 inline-block shrink-0" />'),
    ("🌐", '<ThemeIcon icon="location" className="w-4 h-4 inline-block shrink-0" />'),
    ("💎", '<ThemeIcon icon="diamond" className="w-4 h-4 inline-block shrink-0" />'),
    ("🌿", '<ThemeIcon icon="leaf" className="w-4 h-4 inline-block shrink-0" />'),
    ("🍃", '<ThemeIcon icon="leaf" className="w-4 h-4 inline-block shrink-0" />'),
    ("🌸", '<ThemeIcon icon="sparkles" className="w-4 h-4 inline-block shrink-0" />'),
    ("🧠", '<ThemeIcon icon="brain" className="w-4 h-4 inline-block shrink-0" />'),
    ("🔽", '<span className="inline-block text-xs">▼</span>')
]

# We must skip comments, ThemeConceptEmojis definition lines, or log strings where emojis are inside quotes in ThemeConceptEmojis map
# Let's replace emojis carefully outside JS dictionary strings
lines = content.split('\n')
new_lines = []

in_emoji_map = False

for line_no, line in enumerate(lines, 1):
    if "const ThemeConceptEmojis = {" in line:
        in_emoji_map = True
    if in_emoji_map and "};" in line:
        in_emoji_map = False
        new_lines.append(line)
        continue
    if in_emoji_map:
        new_lines.append(line)
        continue
    
    # Don't replace in console.log statements
    if "console.log" in line or "console.warn" in line or "console.error" in line:
        new_lines.append(line)
        continue
        
    line_replaced = line
    for emoji, replacement in emoji_replacements:
        if emoji in line_replaced:
            # If inside fallbackEmoji="..."
            if f'fallbackEmoji="{emoji}"' in line_replaced:
                line_replaced = line_replaced.replace(f'fallbackEmoji="{emoji}"', 'fallbackEmoji=""')
            elif f"fallbackEmoji='{emoji}'" in line_replaced:
                line_replaced = line_replaced.replace(f"fallbackEmoji='{emoji}'", "fallbackEmoji=''")
            else:
                line_replaced = line_replaced.replace(emoji, replacement)
    new_lines.append(line_replaced)

new_content = '\n'.join(new_lines)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Replaced all hardcoded emojis across index.html with clean SVG components and synced yonetim.html and dist/index.html!")
