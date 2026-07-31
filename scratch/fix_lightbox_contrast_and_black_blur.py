import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace Lightbox Modal in index.html with deep black backdrop blur and ultra-high contrast gold/white elements
old_lightbox = """      {/* LIGHTBOX CAROUSEL MODAL (REACT PORTAL DIRECTLY TO DOCUMENT.BODY) */}
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
          </a>

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

new_lightbox = """      {/* LIGHTBOX CAROUSEL MODAL (DEEP BLACK BACKDROP BLUR & ULTRA-HIGH CONTRAST) */}
      {lightboxIndex !== null && mediaList[lightboxIndex] && typeof ReactDOM !== 'undefined' && ReactDOM.createPortal(
        <div className="fixed inset-0 w-screen h-screen z-[999999] bg-black/92 backdrop-blur-2xl flex items-center justify-center p-4 sm:p-8 animate-fade-in pointer-events-auto">
          {/* TOP-RIGHT PHYSICAL SCREEN CLOSE (X) BUTTON */}
          <button
            type="button"
            onClick={() => setLightboxIndex(null)}
            className="fixed top-4 right-4 sm:top-6 sm:right-6 w-12 h-12 rounded-full bg-red-600 hover:bg-red-500 hover:scale-110 text-white font-black text-2xl shadow-2xl flex items-center justify-center transition cursor-pointer z-[1000000] border-2 border-white"
            title="Kapat (ESC)"
            aria-label="Kapat"
          >
            ✕
          </button>

          {/* BOTTOM-RIGHT PHYSICAL SCREEN DOWNLOAD BUTTON (BRIGHT GOLD ON DEEP BLACK) */}
          <a
            href={mediaList[lightboxIndex].url}
            download={mediaList[lightboxIndex].fileName || 'medya_icerigi'}
            onClick={(e) => e.stopPropagation()}
            className="fixed bottom-4 right-4 sm:bottom-6 sm:right-6 bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 hover:to-amber-400 text-slate-950 font-black text-xs sm:text-sm px-5 py-3 rounded-2xl shadow-[0_10px_30px_rgba(245,158,11,0.6)] hover:scale-110 transition flex items-center space-x-2 z-[1000000] border-2 border-white cursor-pointer"
            title="İçeriği Cihazınıza İndirin"
          >
            <ThemeIcon icon="download" fallbackEmoji="⬇️" className="w-4 h-4 shrink-0 text-slate-950 font-bold" />
            <span className="tracking-wide">İNDİR</span>
          </a>

          {/* FAR-LEFT PHYSICAL SCREEN PREVIOUS BUTTON */}
          {lightboxIndex > 0 && (
            <button
              type="button"
              onClick={() => setLightboxIndex(prev => prev - 1)}
              className="fixed left-3 sm:left-6 top-1/2 -translate-y-1/2 w-14 h-14 rounded-full bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 hover:to-amber-400 text-slate-950 font-black text-3xl shadow-[0_10px_30px_rgba(245,158,11,0.5)] flex items-center justify-center transition cursor-pointer hover:scale-115 z-[1000000] border-2 border-white"
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
              className="fixed right-3 sm:right-6 top-1/2 -translate-y-1/2 w-14 h-14 rounded-full bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 hover:to-amber-400 text-slate-950 font-black text-3xl shadow-[0_10px_30px_rgba(245,158,11,0.5)] flex items-center justify-center transition cursor-pointer hover:scale-115 z-[1000000] border-2 border-white"
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
                  className="max-w-full max-h-[75vh] rounded-3xl border-2 border-amber-500/60 shadow-[0_0_50px_rgba(245,158,11,0.4)] bg-black"
                />
              </div>
            ) : (
              <img
                src={mediaList[lightboxIndex].url}
                alt="Büyük Görsel"
                className="max-w-full max-h-[75vh] object-contain rounded-3xl border-2 border-white/30 shadow-[0_0_60px_rgba(0,0,0,0.9)]"
              />
            )}

            {/* CAPTION & METADATA BAR (CRYSTAL CLEAR HIGH CONTRAST) */}
            <div className="text-center space-y-1 bg-slate-900/95 border-2 border-amber-500/50 px-6 py-3 rounded-2xl shadow-2xl backdrop-blur-md">
              <div className="font-heading font-black text-base sm:text-lg text-amber-400 tracking-wide">
                {mediaList[lightboxIndex].uploaderName} <span className="text-white font-medium">• {mediaList[lightboxIndex].tableNo}</span>
              </div>
              <div className="text-xs text-slate-300 font-mono font-bold">
                {mediaList[lightboxIndex].timestamp} • <span className="text-amber-400 font-black">{lightboxIndex + 1} / {mediaList.length}</span>
              </div>
            </div>
          </div>
        </div>,
        document.body
      )}"""

if old_lightbox in html:
    html = html.replace(old_lightbox, new_lightbox)
    print("Fixed Lightbox Modal backdrop to deep black & updated buttons/texts to ultra-high contrast!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html black backdrop blur & contrast fix successfully!")
