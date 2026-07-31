import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update Video Thumbnail rendering in Gallery Grid (replace img with HTML5 video tag for live video frame poster)
old_grid_video = """                    {item.type === 'video' ? (
                      <div className="w-full h-full relative bg-slate-950 flex items-center justify-center">
                        <img src={item.thumbnail} alt="Video Önizleme" className="w-full h-full object-cover opacity-60 group-hover:opacity-80 transition" />
                        <div className="absolute w-10 h-10 rounded-full bg-amber-500 text-slate-950 flex items-center justify-center shadow-lg group-hover:scale-110 transition">
                          <ThemeIcon icon="play" fallbackEmoji="" className="w-5 h-5 ml-0.5 shrink-0" />
                        </div>
                        <span className="absolute top-2 left-2 px-2 py-0.5 rounded-md bg-slate-900/80 text-white font-mono text-[9px] font-bold">
                          VIDEO
                        </span>
                      </div>
                    ) : ("""

new_grid_video = """                    {item.type === 'video' ? (
                      <div className="w-full h-full relative bg-slate-950 flex items-center justify-center overflow-hidden">
                        <video
                          src={item.url}
                          preload="metadata"
                          muted
                          playsInline
                          className="w-full h-full object-cover opacity-70 group-hover:opacity-90 group-hover:scale-105 transition duration-300 pointer-events-none"
                        />
                        <div className="absolute w-12 h-12 rounded-full bg-amber-500/90 text-slate-950 flex items-center justify-center shadow-2xl group-hover:scale-110 transition backdrop-blur-xs">
                          <ThemeIcon icon="play" fallbackEmoji="▶" className="w-6 h-6 ml-0.5 shrink-0 text-slate-950" />
                        </div>
                        <span className="absolute top-2 left-2 px-2 py-0.5 rounded-md bg-slate-900/90 border border-amber-500/40 text-amber-400 font-mono text-[9px] font-black tracking-widest shadow-md">
                          ▶ VİDEO
                        </span>
                      </div>
                    ) : ("""

if old_grid_video in html:
    html = html.replace(old_grid_video, new_grid_video)
    print("Updated Gallery Grid Video Thumbnail rendering!")

# Update Lightbox Video Modal Controls
old_lightbox_video = """            {mediaList[lightboxIndex].type === 'video' ? (
              <video
                src={mediaList[lightboxIndex].url}
                controls
                autoPlay
                className="max-w-full max-h-[70vh] rounded-2xl border border-white/20 shadow-2xl"
              />
            ) : ("""

new_lightbox_video = """            {mediaList[lightboxIndex].type === 'video' ? (
              <div className="w-full flex flex-col items-center">
                <video
                  src={mediaList[lightboxIndex].url}
                  controls
                  autoPlay
                  playsInline
                  className="max-w-full max-h-[70vh] rounded-2xl border-2 border-amber-500/40 shadow-2xl bg-black"
                />
              </div>
            ) : ("""

if old_lightbox_video in html:
    html = html.replace(old_lightbox_video, new_lightbox_video)
    print("Updated Lightbox Video Player rendering!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html video preview enhancements successfully!")
