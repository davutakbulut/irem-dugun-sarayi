import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Gallery Card Overlay to add Download button at bottom-right
old_card_bottom = """                      <div>
                        <div className="font-bold truncate">{item.uploaderName} ({item.tableNo})</div>
                        <div className="text-[9px] opacity-75 font-mono">{item.timestamp}</div>
                      </div>"""

new_card_bottom = """                      <div className="flex items-end justify-between gap-2 w-full">
                        <div className="min-w-0">
                          <div className="font-bold truncate">{item.uploaderName} ({item.tableNo})</div>
                          <div className="text-[9px] opacity-75 font-mono">{item.timestamp}</div>
                        </div>
                        <a
                          href={item.url}
                          download={item.fileName || 'medya_icerigi'}
                          onClick={(e) => e.stopPropagation()}
                          className="px-2 py-1 bg-amber-500 hover:bg-amber-400 text-slate-950 rounded-md font-extrabold text-[9px] shadow-lg transition flex items-center space-x-1 shrink-0 cursor-pointer hover:scale-105"
                          title="Cihaza İndir"
                        >
                          <ThemeIcon icon="download" fallbackEmoji="⬇️" className="w-3 h-3 shrink-0 text-slate-950" />
                          <span>İndir</span>
                        </a>
                      </div>"""

if old_card_bottom in html:
    html = html.replace(old_card_bottom, new_card_bottom)
    print("Added Download button to Gallery Card Overlay!")

# 2. Update Fullscreen Lightbox Portal Modal to add fixed Download button at bottom-right of screen
old_lightbox_close = """          {/* TOP-RIGHT PHYSICAL SCREEN CLOSE (X) BUTTON */}
          <button
            type="button"
            onClick={() => setLightboxIndex(null)}
            className="fixed top-4 right-4 sm:top-6 sm:right-6 w-12 h-12 rounded-full bg-red-600 hover:bg-red-500 hover:scale-110 text-white font-extrabold text-2xl shadow-2xl flex items-center justify-center transition cursor-pointer z-[1000000] border-2 border-white/30"
            title="Kapat (ESC)"
            aria-label="Kapat"
          >
            ✕
          </button>"""

new_lightbox_close = """          {/* TOP-RIGHT PHYSICAL SCREEN CLOSE (X) BUTTON */}
          <button
            type="button"
            onClick={() => setLightboxIndex(null)}
            className="fixed top-4 right-4 sm:top-6 sm:right-6 w-12 h-12 rounded-full bg-red-600 hover:bg-red-500 hover:scale-110 text-white font-extrabold text-2xl shadow-2xl flex items-center justify-center transition cursor-pointer z-[1000000] border-2 border-white/30"
            title="Kapat (ESC)"
            aria-label="Kapat"
          >
            ✕
          </button>

          {/* BOTTOM-RIGHT PHYSICAL SCREEN DOWNLOAD BUTTON */}
          <a
            href={mediaList[lightboxIndex].url}
            download={mediaList[lightboxIndex].fileName || 'medya_icerigi'}
            onClick={(e) => e.stopPropagation()}
            className="fixed bottom-4 right-4 sm:bottom-6 sm:right-6 gold-button text-slate-950 font-black text-xs sm:text-sm px-4 py-2.5 rounded-2xl shadow-2xl hover:scale-110 transition flex items-center space-x-2 z-[1000000] border-2 border-white/40 cursor-pointer"
            title="İçeriği Cihazınıza İndirin"
          >
            <ThemeIcon icon="download" fallbackEmoji="⬇️" className="w-4 h-4 shrink-0 text-slate-950" />
            <span>İndir</span>
          </a>"""

if old_lightbox_close in html:
    html = html.replace(old_lightbox_close, new_lightbox_close)
    print("Added fixed Download button to Lightbox Modal bottom-right!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html download buttons successfully!")
