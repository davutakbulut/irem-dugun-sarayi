import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace Lightbox Modal rendering in index.html with ReactDOM.createPortal directly targeting document.body
old_lightbox_block = """      {/* LIGHTBOX CAROUSEL MODAL */}
      {lightboxIndex !== null && mediaList[lightboxIndex] && (
        <div className="fixed inset-0 z-[99999] bg-slate-950/95 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in">
          <button
            type="button"
            onClick={() => setLightboxIndex(null)}
            className="absolute top-4 right-4 w-10 h-10 rounded-full bg-white/10 hover:bg-red-500 text-white font-bold flex items-center justify-center transition cursor-pointer z-50"
          >
            ✕
          </button>

          {lightboxIndex > 0 && (
            <button
              type="button"
              onClick={() => setLightboxIndex(prev => prev - 1)}
              className="absolute left-4 w-12 h-12 rounded-full bg-white/10 hover:bg-amber-500 text-white font-bold flex items-center justify-center transition cursor-pointer z-50 text-xl"
            >
              ‹
            </button>
          )}

          {lightboxIndex < mediaList.length - 1 && (
            <button
              type="button"
              onClick={() => setLightboxIndex(prev => prev + 1)}
              className="absolute right-4 w-12 h-12 rounded-full bg-white/10 hover:bg-amber-500 text-white font-bold flex items-center justify-center transition cursor-pointer z-50 text-xl"
            >
              ›
            </button>
          )}

          <div className="max-w-4xl max-h-[85vh] flex flex-col items-center justify-center space-y-3 text-white">
            {mediaList[lightboxIndex].type === 'video' ? (
              <div className="w-full flex flex-col items-center">
                <video
                  src={mediaList[lightboxIndex].url}
                  controls
                  autoPlay
                  preload="auto"
                  playsInline
                  className="max-w-full max-h-[70vh] rounded-2xl border-2 border-amber-500/40 shadow-2xl bg-black"
                />
              </div>
            ) : (
              <img
                src={mediaList[lightboxIndex].url}
                alt="Büyük Görsel"
                className="max-w-full max-h-[70vh] object-contain rounded-2xl border border-white/20 shadow-2xl"
              />
            )}

            <div className="text-center space-y-1">
              <div className="font-bold text-sm">{mediaList[lightboxIndex].uploaderName} ({mediaList[lightboxIndex].tableNo})</div>
              <div className="text-xs text-gray-400 font-mono">{mediaList[lightboxIndex].timestamp} • {lightboxIndex + 1} / {mediaList.length}</div>
            </div>
          </div>
        </div>
      )}"""

new_lightbox_block = """      {/* LIGHTBOX CAROUSEL MODAL (REACT PORTAL DIRECTLY TO DOCUMENT.BODY) */}
      {lightboxIndex !== null && mediaList[lightboxIndex] && typeof ReactDOM !== 'undefined' && ReactDOM.createPortal(
        <div className="fixed inset-0 w-screen h-screen z-[999999] bg-slate-950/98 backdrop-blur-xl flex items-center justify-center p-4 sm:p-8 animate-fade-in pointer-events-auto">
          {/* TOP-RIGHT PHYSICAL SCREEN CLOSE (X) BUTTON */}
          <button
            type="button"
            onClick={() => setLightboxIndex(null)}
            className="fixed top-4 right-4 sm:top-6 sm:right-6 w-12 h-12 rounded-full bg-red-600 hover:bg-red-500 hover:scale-110 text-white font-extrabold text-2xl shadow-2xl flex items-center justify-center transition cursor-pointer z-[1000000] border-2 border-white/30"
            title="Kapat (ESC)"
            aria-label="Kapat"
          >
            ✕
          </button>

          {/* FAR-LEFT PHYSICAL SCREEN PREVIOUS BUTTON */}
          {lightboxIndex > 0 && (
            <button
              type="button"
              onClick={() => setLightboxIndex(prev => prev - 1)}
              className="fixed left-3 sm:left-6 top-1/2 -translate-y-1/2 w-14 h-14 rounded-full gold-button text-slate-950 font-black text-3xl shadow-2xl flex items-center justify-center transition cursor-pointer hover:scale-115 z-[1000000] border-2 border-white/40"
              title="Önceki İçerik (Sol Ok)"
              aria-label="Önceki"
            >
              ‹
            </button>
          )}

          {/* FAR-RIGHT PHYSICAL SCREEN NEXT BUTTON */}
          {lightboxIndex < mediaList.length - 1 && (
            <button
              type="button"
              onClick={() => setLightboxIndex(prev => prev + 1)}
              className="fixed right-3 sm:right-6 top-1/2 -translate-y-1/2 w-14 h-14 rounded-full gold-button text-slate-950 font-black text-3xl shadow-2xl flex items-center justify-center transition cursor-pointer hover:scale-115 z-[1000000] border-2 border-white/40"
              title="Sonraki İçerik (Sağ Ok)"
              aria-label="Sonraki"
            >
              ›
            </button>
          )}

          {/* CENTERED FULLSCREEN MEDIA CONTAINER */}
          <div className="w-full max-w-5xl max-h-[90vh] flex flex-col items-center justify-center space-y-4 text-white pointer-events-auto">
            {mediaList[lightboxIndex].type === 'video' ? (
              <div className="w-full flex flex-col items-center justify-center">
                <video
                  src={mediaList[lightboxIndex].url}
                  controls
                  autoPlay
                  preload="auto"
                  playsInline
                  className="max-w-full max-h-[75vh] rounded-3xl border-2 border-amber-500/50 shadow-[0_0_50px_rgba(217,119,6,0.3)] bg-black"
                />
              </div>
            ) : (
              <img
                src={mediaList[lightboxIndex].url}
                alt="Büyük Görsel"
                className="max-w-full max-h-[75vh] object-contain rounded-3xl border-2 border-white/20 shadow-[0_0_50px_rgba(0,0,0,0.8)]"
              />
            )}

            {/* CAPTION & METADATA BAR */}
            <div className="text-center space-y-1 bg-slate-900/90 border border-white/10 px-6 py-2.5 rounded-2xl shadow-xl backdrop-blur-md">
              <div className="font-heading font-extrabold text-sm sm:text-base text-amber-400">
                {mediaList[lightboxIndex].uploaderName} • <span className="text-slate-300 font-normal">{mediaList[lightboxIndex].tableNo}</span>
              </div>
              <div className="text-xs text-gray-400 font-mono">
                {mediaList[lightboxIndex].timestamp} • <span className="text-amber-400 font-bold">{lightboxIndex + 1} / {mediaList.length}</span>
              </div>
            </div>
          </div>
        </div>,
        document.body
      )}"""

if old_lightbox_block in html:
    html = html.replace(old_lightbox_block, new_lightbox_block)
    print("Replaced Lightbox Modal in index.html with ReactDOM.createPortal directly to document.body!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html ReactDOM.createPortal portal successfully!")
