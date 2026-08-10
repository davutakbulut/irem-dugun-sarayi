import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_scroll_indicator = """            {/* Scroll Down Indicator */}
            <div 
              onClick={() => window.scrollTo({ top: window.innerHeight - 70, behavior: 'smooth' })}
              className="absolute bottom-8 left-1/2 -translate-x-1/2 z-10 text-white/80 animate-bounce flex flex-col items-center cursor-pointer group"
            >
              <span className="text-[10px] font-extrabold tracking-widest uppercase mb-1 group-hover:text-amber-300 transition-colors">AŞAĞI KAYDIRIN</span>
              <span className="text-2xl">↓</span>
            </div>"""

new_scroll_indicator = """            {/* Scroll Down Indicator */}
            <div 
              onClick={() => window.scrollTo({ top: window.innerHeight - 70, behavior: 'smooth' })}
              className="absolute bottom-8 sm:bottom-10 left-0 right-0 z-20 text-white/90 animate-bounce flex flex-col items-center justify-center text-center cursor-pointer group pointer-events-auto mx-auto w-full px-4"
            >
              <span className="text-[10px] sm:text-xs font-black tracking-[0.25em] uppercase mb-1 group-hover:text-amber-300 transition-colors text-center w-full block drop-shadow-md">AŞAĞI KAYDIRIN</span>
              <span className="text-2xl font-bold leading-none drop-shadow-md">↓</span>
            </div>"""

if old_scroll_indicator in content:
    content = content.replace(old_scroll_indicator, new_scroll_indicator, 1)
    print("Fixed scroll down indicator centering for mobile view!")
else:
    print("WARNING: Could not find old_scroll_indicator in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
