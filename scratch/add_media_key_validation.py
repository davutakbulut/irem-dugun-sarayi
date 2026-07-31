import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update currentRes resolution to explicitly check if selectedResKey / urlKey has a matching reservation
old_current_res = """  const currentRes = useMemo(() => {
    if (!selectedResKey) return userReservations[0] || reservations[0] || null;
    return reservations.find(r => r.mediaKey === selectedResKey || r.id === selectedResKey) || userReservations[0] || reservations[0] || null;
  }, [reservations, userReservations, selectedResKey]);"""

new_current_res = """  // Strict MediaKey / Reference Number Validation
  const currentRes = useMemo(() => {
    if (!selectedResKey) return null;
    return reservations.find(r => r.mediaKey === selectedResKey || r.id === selectedResKey) || null;
  }, [reservations, selectedResKey]);

  // Check whether the URL reference key actually matches a valid active reservation in the database
  const isValidMediaKey = useMemo(() => {
    if (!selectedResKey) return false;
    return !!currentRes;
  }, [selectedResKey, currentRes]);"""

if old_current_res in html:
    html = html.replace(old_current_res, new_current_res)
    print("Replaced currentRes resolution with strict mediaKey validation check!")

# Add invalid key error screen inside MediaComponent return
old_public_mode_start = """  return (
    <div className="w-full space-y-6 animate-fade-in pb-16">
      {/* PUBLIC GUEST MODE HEADER */}
      {isPublicGuestMode ? ("""

new_public_mode_start = """  return (
    <div className="w-full space-y-6 animate-fade-in pb-16">
      {/* INVALID OR EXPIRED MEDIA KEY ERROR SCREEN (If public guest accesses with non-existent Key) */}
      {isPublicGuestMode && selectedResKey && !isValidMediaKey && (
        <div className="glass-panel p-8 rounded-3xl border-2 border-red-500/50 bg-gradient-to-b from-red-500/10 via-slate-900 to-slate-950 text-center space-y-4 shadow-2xl max-w-lg mx-auto my-12">
          <div className="w-16 h-16 rounded-3xl bg-red-500/20 text-red-500 flex items-center justify-center mx-auto border border-red-500/40 shadow-lg">
            <ThemeIcon icon="alert" fallbackEmoji="" className="w-8 h-8 text-red-500 shrink-0" />
          </div>
          <div className="space-y-2">
            <h3 className="font-heading font-black text-xl text-red-500">
              ⚠️ Geçersiz veya Bulunamayan Etkinlik Bağlantısı
            </h3>
            <p className="text-xs text-slate-300 leading-relaxed font-medium">
              Girmeye çalıştığınız medya paylaşım bağlantısı (<span className="font-mono text-amber-400 font-bold">{selectedResKey}</span>) sistemimizde bulunamadı veya saklama süresi dolduğu için kaldırılmıştır.
            </p>
          </div>

          <div className="p-3 rounded-2xl bg-slate-900/80 border border-slate-800 text-[11px] text-slate-400 font-mono">
            Doğru bağlantı ve QR kodu için lütfen düğün sahibi veya salon yönetimi ile iletişime geçiniz.
          </div>
        </div>
      )}

      {/* PUBLIC GUEST MODE HEADER */}
      {isPublicGuestMode && isValidMediaKey ? ("""

if old_public_mode_start in html:
    html = html.replace(old_public_mode_start, new_public_mode_start)
    print("Added Invalid MediaKey Error Screen for public guest mode!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with mediaKey reference verification successfully!")
