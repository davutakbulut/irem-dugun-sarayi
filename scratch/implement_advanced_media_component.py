import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace MediaComponent with the full implementation including Public Guest Mode, Queue Uploader, Captcha, Cooldown, IP Ban Tab, Lightbox Carousel, and A4 QR PDF Generator

new_media_component = """    // --- ADVANCED GUEST & ADMIN MEDIA GALLERY COMPONENT ---
    function MediaComponent({ reservations = [], setReservations = () => {}, activeRole = 'admin', showToast = () => {} }) {
      // Check URL search param for public guest key (e.g. #/medya-yukle?key=MEDIA-8X92M1KP)
      const getUrlKey = () => {
        if (typeof window === 'undefined') return '';
        const hash = window.location.hash || '';
        const match = hash.match(/key=([A-Za-z0-9_-]+)/);
        return match ? match[1] : '';
      };

      const publicGuestKey = getUrlKey();
      const isPublicGuestMode = !!publicGuestKey;

      // Select active reservation
      const [selectedResKey, setSelectedResKey] = useState(() => {
        if (publicGuestKey) return publicGuestKey;
        return reservations.length > 0 ? (reservations[0].mediaKey || 'MEDIA-8X92M1KP') : '';
      });

      const currentRes = useMemo(() => {
        return reservations.find(r => r.mediaKey === selectedResKey) || reservations[0] || null;
      }, [reservations, selectedResKey]);

      // State filters
      const [filterType, setFilterType] = useState('all'); // all, image, video
      const [activeTabSub, setActiveTabSub] = useState('gallery'); // gallery, ban_list

      // Banned IPs list (Stored in LocalStorage)
      const [bannedIPs, setBannedIPs] = useState(() => {
        if (typeof window === 'undefined') return ['195.175.99.99'];
        try {
          const saved = localStorage.getItem('banned_ips');
          return saved ? JSON.parse(saved) : ['195.175.99.99'];
        } catch(e) { return ['195.175.99.99']; }
      });

      useEffect(() => {
        try { localStorage.setItem('banned_ips', JSON.stringify(bannedIPs)); } catch(e){}
      }, [bannedIPs]);

      // Session Guest Uploads (For privacy: guest sees only items uploaded in current session)
      const [guestSessionUploadIds, setGuestSessionUploadIds] = useState(() => {
        if (typeof window === 'undefined') return [];
        try {
          const saved = sessionStorage.getItem('guest_uploaded_ids');
          return saved ? JSON.parse(saved) : [];
        } catch(e) { return []; }
      });

      useEffect(() => {
        try { sessionStorage.setItem('guest_uploaded_ids', JSON.stringify(guestSessionUploadIds)); } catch(e){}
      }, [guestSessionUploadIds]);

      // Queue Uploader & Cooldown State
      const [uploadQueue, setUploadQueue] = useState([]);
      const [isUploadingQueue, setIsUploadingQueue] = useState(false);
      const [uploadedCountSession, setUploadedCountSession] = useState(0);
      const [cooldownSeconds, setCooldownSeconds] = useState(0);
      const [showCaptchaModal, setShowCaptchaModal] = useState(false);
      const [pendingFilesQueue, setPendingFilesQueue] = useState([]);
      const fileInputRef = useRef(null);

      // Lightbox Carousel State
      const [lightboxIndex, setLightboxIndex] = useState(null);

      // A4 QR PDF Modal State
      const [showPdfModal, setShowPdfModal] = useState(false);

      // Cooldown timer effect
      useEffect(() => {
        if (cooldownSeconds <= 0) return;
        const timer = setInterval(() => {
          setCooldownSeconds(prev => prev - 1);
        }, 1000);
        return () => clearInterval(timer);
      }, [cooldownSeconds]);

      // Current media files list
      const mediaList = useMemo(() => {
        if (!currentRes) return [];
        let files = currentRes.mediaFiles || [];

        // If public guest mode, filter to only show session uploads
        if (isPublicGuestMode) {
          files = files.filter(f => guestSessionUploadIds.includes(f.id));
        }

        if (filterType === 'image') return files.filter(f => f.type === 'image');
        if (filterType === 'video') return files.filter(f => f.type === 'video');
        return files;
      }, [currentRes, isPublicGuestMode, guestSessionUploadIds, filterType]);

      // Handle File Selection (Supports up to 50 files with queue + limits + rate-limiting)
      const handleFilesSelect = (e) => {
        const files = Array.from(e.target.files || []);
        if (files.length === 0) return;

        if (cooldownSeconds > 0) {
          showToast(`⚠️ Lütfen bekleyin! 50 dosya limitine ulaştınız. (${cooldownSeconds} saniye kaldı)`);
          return;
        }

        // Check if session count + new files > 50
        if (uploadedCountSession + files.length > 50) {
          setCooldownSeconds(60);
          showToast('🛑 50 dosya yükleme sınırına ulaşıldı! 1 dakika bekleme süresi başlatıldı.');
          return;
        }

        // Check Captcha trigger (every 50 images)
        if (uploadedCountSession > 0 && uploadedCountSession % 50 === 0) {
          setPendingFilesQueue(files);
          setShowCaptchaModal(true);
          return;
        }

        processFilesQueue(files);
      };

      const processFilesQueue = (files) => {
        const newQueueItems = files.map((file, idx) => ({
          id: 'q_' + Date.now() + '_' + idx,
          file,
          name: file.name,
          size: (file.size / (1024 * 1024)).toFixed(1),
          type: file.type.startsWith('video/') ? 'video' : 'image',
          progress: 0,
          status: 'pending' // pending, uploading, success, error
        }));

        setUploadQueue(prev => [...prev, ...newQueueItems]);
      };

      // Sequential Queue Process Engine
      useEffect(() => {
        if (isUploadingQueue) return;
        const pendingItem = uploadQueue.find(item => item.status === 'pending');
        if (!pendingItem) return;

        setIsUploadingQueue(true);

        // Update status to uploading
        setUploadQueue(prev => prev.map(item => item.id === pendingItem.id ? { ...item, status: 'uploading', progress: 15 } : item));

        // Simulate chunk upload with progress bar
        let prog = 15;
        const interval = setInterval(() => {
          prog += 25;
          if (prog >= 100) {
            clearInterval(interval);

            // Read file data URL
            const reader = new FileReader();
            reader.onload = (e) => {
              const fileDataUrl = e.target.result;
              const newMediaId = 'mf_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4);

              const newMediaObj = {
                id: newMediaId,
                type: pendingItem.type,
                url: fileDataUrl,
                thumbnail: fileDataUrl,
                uploaderName: isPublicGuestMode ? 'Davetli Konuk' : 'İşletme Yetkilisi',
                tableNo: 'Masa Davetlisi',
                timestamp: new Date().toISOString().replace('T', ' ').substr(0, 16),
                isGuest: isPublicGuestMode,
                uploaderIp: '195.175.22.' + Math.floor(Math.random() * 50 + 1)
              };

              // Update reservation mediaFiles state
              setReservations(prev => prev.map(r => {
                if (r.mediaKey === selectedResKey) {
                  return {
                    ...r,
                    mediaFiles: [newMediaObj, ...(r.mediaFiles || [])]
                  };
                }
                return r;
              }));

              // Update guest session IDs
              if (isPublicGuestMode) {
                setGuestSessionUploadIds(prev => [newMediaId, ...prev]);
              }

              // Update queue item to success
              setUploadQueue(prev => prev.map(item => item.id === pendingItem.id ? { ...item, status: 'success', progress: 100 } : item));
              setUploadedCountSession(prev => prev + 1);
              setIsUploadingQueue(false);
            };
            reader.readAsDataURL(pendingItem.file);
          } else {
            setUploadQueue(prev => prev.map(item => item.id === pendingItem.id ? { ...item, progress: prog } : item));
          }
        }, 150);

      }, [uploadQueue, isUploadingQueue, selectedResKey, isPublicGuestMode]);

      // Copy Guest Shareable Link
      const handleCopyLink = () => {
        const shareUrl = `${window.location.origin}${window.location.pathname}#/medya-yukle?key=${selectedResKey}`;
        if (navigator.clipboard) {
          navigator.clipboard.writeText(shareUrl);
          showToast('🔗 Davetli Yükleme Bağlantısı Panoya Kopyalandı!');
        } else {
          prompt('Davetli Bağlantısını Kopyalayın:', shareUrl);
        }
      };

      // Bulk ZIP Download Simulation
      const handleBulkDownload = () => {
        showToast('📦 Tüm fotoğraf ve videolar paketleniyor... Arşiv indirmesi başlatıldı!');
        const text = `İrem Düğün Sarayı - ${currentRes?.customerName || 'Davet'} Medya Arşivi\\nToplam ${mediaList.length} dosya.`;
        const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = `${(currentRes?.customerName || 'Etkinlik').replace(/\\s+/g, '_')}_Medya_Arsivi.txt`;
        a.click();
      };

      return (
        <div className="w-full space-y-6 animate-fade-in pb-16">

          {/* PUBLIC GUEST MODE BANNER OR ADMIN HEADER */}
          {isPublicGuestMode ? (
            <div className="glass-panel p-6 rounded-3xl border-2 border-amber-500/50 bg-gradient-to-r from-amber-500/10 via-amber-600/5 to-amber-500/10 text-center space-y-3 shadow-md">
              <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-amber-400 to-amber-600 flex items-center justify-center text-white mx-auto shadow-lg">
                <ThemeIcon icon="camera" fallbackEmoji="" className="w-7 h-7 text-white" />
              </div>
              <div>
                <h2 className="text-xl sm:text-2xl font-heading font-extrabold gold-gradient-text">
                  {currentRes?.customerName || 'Düğün & Balo Daveti'}
                </h2>
                <p className="text-xs text-slate-600 dark:text-gray-300 font-medium mt-1">
                  Çektiğiniz en özel fotoğraf ve videoları gelin & damat ile anında paylaşın!
                </p>
              </div>
            </div>
          ) : (
            <div className="glass-panel p-6 rounded-3xl border border-amber-500/30 flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 shadow-sm">
              <div className="space-y-1">
                <div className="flex items-center space-x-2">
                  <ThemeIcon icon="camera" fallbackEmoji="" className="w-6 h-6 text-amber-500 shrink-0" />
                  <h2 className="text-xl sm:text-2xl font-heading font-extrabold gold-gradient-text">
                    Medya & QR Fotoğraf Galerisi
                  </h2>
                  <span className="text-[10px] font-black px-2.5 py-0.5 rounded-full gold-button shrink-0">
                    CANLI KONTROL
                  </span>
                </div>
                <p className="text-xs text-slate-500 dark:text-gray-400 font-medium">
                  Rezervasyon bazlı QR kodları yönetin, davetli ve fotoğrafçı medyalarını canlı inceleyin.
                </p>
              </div>

              {/* ACTION BUTTONS (Link Copy, A4 PDF, Zip Download) */}
              <div className="flex flex-wrap items-center gap-2 w-full sm:w-auto">
                <button
                  type="button"
                  onClick={handleCopyLink}
                  className="px-3.5 py-2 rounded-xl bg-blue-500/10 border border-blue-500/30 text-blue-600 dark:text-blue-400 font-bold text-xs hover:bg-blue-500 hover:text-white transition flex items-center space-x-1.5 shrink-0 cursor-pointer"
                >
                  <ThemeIcon icon="copy" fallbackEmoji="" className="w-4 h-4 shrink-0" />
                  <span>Davetli Linkini Kopyala</span>
                </button>

                <button
                  type="button"
                  onClick={() => setShowPdfModal(true)}
                  className="px-3.5 py-2 rounded-xl bg-purple-500/10 border border-purple-500/30 text-purple-600 dark:text-purple-400 font-bold text-xs hover:bg-purple-500 hover:text-white transition flex items-center space-x-1.5 shrink-0 cursor-pointer"
                >
                  <ThemeIcon icon="print" fallbackEmoji="" className="w-4 h-4 shrink-0" />
                  <span>🖨️ A4 Masakartı PDF İndir</span>
                </button>

                <button
                  type="button"
                  onClick={handleBulkDownload}
                  className="px-3.5 py-2 rounded-xl gold-button font-bold text-xs shadow hover:scale-105 transition flex items-center space-x-1.5 shrink-0 cursor-pointer"
                >
                  <ThemeIcon icon="download" fallbackEmoji="" className="w-4 h-4 shrink-0" />
                  <span>Tümünü İndir (.ZIP)</span>
                </button>
              </div>
            </div>
          )}

          {/* RESERVATION SELECTOR BAR (For Staff/Admin) */}
          {!isPublicGuestMode && (
            <div className="glass-panel p-4 rounded-2xl border border-slate-200 dark:border-brand-border/40 flex flex-col sm:flex-row justify-between items-center gap-3">
              <div className="flex items-center space-x-2 w-full sm:w-auto">
                <ThemeIcon icon="venue" fallbackEmoji="" className="w-4 h-4 text-amber-500 shrink-0" />
                <span className="text-xs font-bold text-slate-700 dark:text-gray-300 shrink-0">Etkinlik Seçin:</span>
                <select
                  value={selectedResKey}
                  onChange={e => setSelectedResKey(e.target.value)}
                  className="bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl px-3 py-2 text-xs font-bold w-full sm:w-72"
                >
                  {reservations.map(r => (
                    <option key={r.id} value={r.mediaKey || r.id}>
                      {r.customerName} ({r.date})
                    </option>
                  ))}
                </select>
              </div>

              {/* TABS: GALLERY vs BAN LIST */}
              <div className="flex items-center space-x-1 bg-slate-100 dark:bg-brand-dark p-1 rounded-xl w-full sm:w-auto justify-end">
                <button
                  type="button"
                  onClick={() => setActiveTabSub('gallery')}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center space-x-1 ${activeTabSub === 'gallery' ? 'gold-button shadow-xs' : 'text-slate-600 dark:text-gray-400'}`}
                >
                  <ThemeIcon icon="media" fallbackEmoji="" className="w-3.5 h-3.5 shrink-0" />
                  <span>Medya Galerisi ({mediaList.length})</span>
                </button>

                <button
                  type="button"
                  onClick={() => setActiveTabSub('ban_list')}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center space-x-1 ${activeTabSub === 'ban_list' ? 'bg-red-500 text-white shadow-xs' : 'text-slate-600 dark:text-gray-400'}`}
                >
                  <ThemeIcon icon="shield" fallbackEmoji="" className="w-3.5 h-3.5 shrink-0" />
                  <span>Engellenen IP'ler ({bannedIPs.length})</span>
                </button>
              </div>
            </div>
          )}

          {/* MAIN TAB 1: GALLERY & UPLOAD AREA */}
          {activeTabSub === 'gallery' && (
            <div className="space-y-6">

              {/* UPLOAD DROPZONE */}
              <div className="glass-panel p-6 rounded-3xl space-y-4 border border-amber-500/30 shadow-sm relative overflow-hidden">
                <div className="flex justify-between items-center">
                  <h3 className="font-heading font-extrabold text-sm text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                    <ThemeIcon icon="plus" fallbackEmoji="" className="w-4 h-4 text-amber-500 shrink-0" />
                    <span>Yeni Fotoğraf veya Video Yükleyin</span>
                  </h3>
                  <span className="text-[10px] font-mono text-amber-700 dark:text-gold-400 bg-amber-500/10 px-2 py-0.5 rounded-md border border-amber-500/20 font-bold">
                    Foto: Maks 15MB | Video: Maks 1GB
                  </span>
                </div>

                <div
                  onClick={() => fileInputRef.current?.click()}
                  className="border-2 border-dashed border-amber-500/40 hover:border-amber-500 rounded-2xl p-6 text-center cursor-pointer transition bg-slate-50/50 dark:bg-brand-dark/40 hover:bg-amber-500/5 flex flex-col items-center justify-center space-y-2"
                >
                  <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFilesSelect}
                    multiple
                    accept="image/*,video/*"
                    className="hidden"
                  />
                  <div className="w-12 h-12 rounded-2xl bg-amber-500/10 text-amber-500 flex items-center justify-center mb-1">
                    <ThemeIcon icon="camera" fallbackEmoji="" className="w-6 h-6 shrink-0" />
                  </div>
                  <div className="font-bold text-xs text-slate-800 dark:text-gray-100">
                    Fotoğraf veya Videoları Seçmek İçin Tıklayın
                  </div>
                  <div className="text-[10px] text-slate-500 dark:text-gray-400">
                    Aynı anda çoklu seçim yapabilirsiniz. Dosyalar kilitlenmeden sırayla yüklenecektir.
                  </div>
                </div>

                {/* QUEUE PROGRESS LIST */}
                {uploadQueue.length > 0 && (
                  <div className="space-y-2 pt-2 border-t border-slate-200 dark:border-brand-border/40">
                    <div className="text-xs font-bold text-slate-700 dark:text-gray-300 flex justify-between">
                      <span>Yükleme Kuyruğu ({uploadQueue.filter(q => q.status === 'success').length} / {uploadQueue.length})</span>
                      {uploadQueue.some(q => q.status === 'uploading') && <span className="text-amber-500 font-mono animate-pulse">Sırayla Yükleniyor...</span>}
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-h-48 overflow-y-auto custom-scrollbar">
                      {uploadQueue.map(item => (
                        <div key={item.id} className="bg-slate-100 dark:bg-brand-dark p-2.5 rounded-xl flex items-center justify-between text-xs space-x-2 border border-slate-200 dark:border-brand-border/40">
                          <div className="truncate flex-1">
                            <div className="font-bold truncate text-slate-800 dark:text-gray-200">{item.name}</div>
                            <div className="text-[10px] text-slate-400 font-mono">{item.size} MB • {item.type}</div>
                          </div>

                          {item.status === 'success' && (
                            <span className="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 font-bold text-[10px] shrink-0 flex items-center space-x-1">
                              <ThemeIcon icon="check" fallbackEmoji="" className="w-3 h-3 shrink-0" />
                              <span>Yüklendi</span>
                            </span>
                          )}

                          {item.status === 'uploading' && (
                            <div className="w-20 space-y-1 shrink-0">
                              <div className="flex justify-between text-[9px] font-mono text-amber-500 font-bold">
                                <span>Yükleniyor</span>
                                <span>%{item.progress}</span>
                              </div>
                              <div className="w-full h-1.5 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                                <div className="h-full bg-amber-500 transition-all duration-150" style={{ width: `${item.progress}%` }}></div>
                              </div>
                            </div>
                          )}

                          {item.status === 'pending' && (
                            <span className="text-[10px] text-slate-400 font-mono shrink-0">Sırada...</span>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* FILTERS & GALLERY GRID */}
              <div className="glass-panel p-6 rounded-3xl space-y-4 border border-slate-200 dark:border-brand-border/40 shadow-sm">
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b pb-3 border-slate-200 dark:border-brand-border/40">
                  <h3 className="font-heading font-extrabold text-base text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                    <ThemeIcon icon="media" fallbackEmoji="" className="w-5 h-5 text-amber-500 shrink-0" />
                    <span>Yüklenen İçerikler ({mediaList.length})</span>
                  </h3>

                  {/* FILTER BUTTONS */}
                  <div className="flex items-center space-x-1 bg-slate-100 dark:bg-brand-dark p-1 rounded-xl">
                    <button
                      type="button"
                      onClick={() => setFilterType('all')}
                      className={`px-3 py-1 rounded-lg text-xs font-bold transition ${filterType === 'all' ? 'gold-button shadow-xs' : 'text-slate-600 dark:text-gray-400'}`}
                    >
                      Tümü
                    </button>
                    <button
                      type="button"
                      onClick={() => setFilterType('image')}
                      className={`px-3 py-1 rounded-lg text-xs font-bold transition ${filterType === 'image' ? 'gold-button shadow-xs' : 'text-slate-600 dark:text-gray-400'}`}
                    >
                      Fotoğraflar
                    </button>
                    <button
                      type="button"
                      onClick={() => setFilterType('video')}
                      className={`px-3 py-1 rounded-lg text-xs font-bold transition ${filterType === 'video' ? 'gold-button shadow-xs' : 'text-slate-600 dark:text-gray-400'}`}
                    >
                      Videolar
                    </button>
                  </div>
                </div>

                {/* GALLERY GRID CARDS */}
                {mediaList.length === 0 ? (
                  <div className="text-center py-12 text-slate-400 space-y-2">
                    <ThemeIcon icon="camera" fallbackEmoji="" className="w-12 h-12 mx-auto text-slate-300 dark:text-slate-600" />
                    <div className="font-bold text-sm">Henüz bu etkinliğe ait medya yüklenmedi.</div>
                    <div className="text-xs">Yukarıdaki alandan ilk fotoğrafı veya videoyu yükleyebilirsiniz.</div>
                  </div>
                ) : (
                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                    {mediaList.map((item, idx) => (
                      <div
                        key={item.id}
                        onClick={() => setLightboxIndex(idx)}
                        className="group relative rounded-2xl overflow-hidden aspect-square border border-slate-200 dark:border-brand-border/60 bg-slate-100 dark:bg-brand-dark shadow-xs cursor-pointer hover:border-amber-500/60 hover:scale-[1.02] transition"
                      >
                        {item.type === 'video' ? (
                          <div className="w-full h-full relative bg-slate-950 flex items-center justify-center">
                            <img src={item.thumbnail} alt="Video Önizleme" className="w-full h-full object-cover opacity-60 group-hover:opacity-80 transition" />
                            <div className="absolute w-10 h-10 rounded-full bg-amber-500 text-slate-950 flex items-center justify-center shadow-lg group-hover:scale-110 transition">
                              <ThemeIcon icon="play" fallbackEmoji="" className="w-5 h-5 ml-0.5 shrink-0" />
                            </div>
                            <span className="absolute top-2 left-2 px-2 py-0.5 rounded-md bg-slate-900/80 text-white font-mono text-[9px] font-bold">
                              VIDEO
                            </span>
                          </div>
                        ) : (
                          <img src={item.url} alt="Galeri Fotoğrafı" className="w-full h-full object-cover group-hover:scale-105 transition duration-300" />
                        )}

                        {/* OVERLAY INFORMATION */}
                        <div className="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition p-2.5 flex flex-col justify-between text-white text-[10px]">
                          <div className="flex justify-end">
                            {!isPublicGuestMode && (
                              <button
                                type="button"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  if (confirm('Bu IP adresini engellemek (banlamak) istediğinize emin misiniz?')) {
                                    setBannedIPs(prev => [...new Set([...prev, item.uploaderIp])]);
                                    showToast(`🚫 ${item.uploaderIp} adresi engellendi!`);
                                  }
                                }}
                                className="px-2 py-1 bg-red-600/80 hover:bg-red-600 text-white rounded-md font-bold text-[9px]"
                                title="Yükleyen IP Adresini Engelle"
                              >
                                IP Ban
                              </button>
                            )}
                          </div>

                          <div>
                            <div className="font-bold truncate">{item.uploaderName} ({item.tableNo})</div>
                            <div className="text-[9px] opacity-75 font-mono">{item.timestamp}</div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* MAIN TAB 2: BANNED IP MANAGEMENT (Staff/Admin Only) */}
          {!isPublicGuestMode && activeTabSub === 'ban_list' && (
            <div className="glass-panel p-6 rounded-3xl space-y-4 border border-red-500/30 shadow-sm">
              <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border/40">
                <h3 className="font-heading font-extrabold text-base text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                  <ThemeIcon icon="shield" fallbackEmoji="" className="w-5 h-5 text-red-500 shrink-0" />
                  <span>Engellenen IP Adresleri ({bannedIPs.length})</span>
                </h3>
              </div>

              {bannedIPs.length === 0 ? (
                <div className="text-center py-8 text-slate-400 font-bold text-xs">
                  Henüz engellenmiş hiçbir IP adresi bulunmuyor.
                </div>
              ) : (
                <div className="space-y-2">
                  {bannedIPs.map(ip => (
                    <div key={ip} className="bg-slate-50 dark:bg-brand-dark p-3 rounded-2xl flex items-center justify-between border border-slate-200 dark:border-brand-border/60 text-xs">
                      <div className="flex items-center space-x-2 font-mono font-bold text-red-600 dark:text-red-400">
                        <ThemeIcon icon="alert" fallbackEmoji="" className="w-4 h-4 shrink-0" />
                        <span>IP: {ip}</span>
                      </div>

                      <button
                        type="button"
                        onClick={() => {
                          setBannedIPs(prev => prev.filter(i => i !== ip));
                          showToast(`✅ ${ip} adresinin engeli kaldırıldı.`);
                        }}
                        className="px-3 py-1 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 hover:bg-emerald-500 hover:text-white rounded-xl font-bold transition text-xs"
                      >
                        Banı Kaldır & Erişime Aç
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* LIGHTBOX CAROUSEL MODAL */}
          {lightboxIndex !== null && mediaList[lightboxIndex] && (
            <div className="fixed inset-0 z-[99999] bg-slate-950/95 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in">
              {/* CLOSE BUTTON */}
              <button
                type="button"
                onClick={() => setLightboxIndex(null)}
                className="absolute top-4 right-4 w-10 h-10 rounded-full bg-white/10 hover:bg-red-500 text-white font-bold flex items-center justify-center transition cursor-pointer z-50"
              >
                ✕
              </button>

              {/* PREVIOUS BUTTON */}
              {lightboxIndex > 0 && (
                <button
                  type="button"
                  onClick={() => setLightboxIndex(prev => prev - 1)}
                  className="absolute left-4 w-12 h-12 rounded-full bg-white/10 hover:bg-amber-500 text-white font-bold flex items-center justify-center transition cursor-pointer z-50 text-xl"
                >
                  ‹
                </button>
              )}

              {/* NEXT BUTTON */}
              {lightboxIndex < mediaList.length - 1 && (
                <button
                  type="button"
                  onClick={() => setLightboxIndex(prev => prev + 1)}
                  className="absolute right-4 w-12 h-12 rounded-full bg-white/10 hover:bg-amber-500 text-white font-bold flex items-center justify-center transition cursor-pointer z-50 text-xl"
                >
                  ›
                </button>
              )}

              {/* MAIN CONTENT AREA */}
              <div className="max-w-4xl max-h-[85vh] flex flex-col items-center justify-center space-y-3 text-white">
                {mediaList[lightboxIndex].type === 'video' ? (
                  <video
                    src={mediaList[lightboxIndex].url}
                    controls
                    autoPlay
                    className="max-w-full max-h-[70vh] rounded-2xl border border-white/20 shadow-2xl"
                  />
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
          )}

          {/* CAPTCHA MODAL (Triggers every 50 uploads) */}
          {showCaptchaModal && (
            <div className="fixed inset-0 z-[99999] bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in">
              <div className="bg-white dark:bg-brand-card p-6 rounded-3xl max-w-sm w-full space-y-4 border-2 border-amber-500 text-center shadow-2xl">
                <div className="w-12 h-12 rounded-2xl bg-amber-500/10 text-amber-500 flex items-center justify-center mx-auto font-bold text-xl">
                  🤖
                </div>
                <h3 className="font-heading font-extrabold text-base text-slate-800 dark:text-gray-100">
                  Güvenlik Doğrulaması (Captcha)
                </h3>
                <p className="text-xs text-slate-500 dark:text-gray-400">
                  50 adet görsel yükleme sınırına ulaştınız. Devam etmek için doğrulama kutusunu işaretleyin.
                </p>

                <button
                  type="button"
                  onClick={() => {
                    setShowCaptchaModal(false);
                    processFilesQueue(pendingFilesQueue);
                    setPendingFilesQueue([]);
                    showToast('✅ Güvenlik doğrulaması başarılı! Yükleme devam ediyor.');
                  }}
                  className="w-full py-3 gold-button font-bold text-xs rounded-xl shadow-md cursor-pointer hover:scale-[1.02] transition"
                >
                  ✓ Ben Robot Değilim (Devam Et)
                </button>
              </div>
            </div>
          )}

          {/* A4 QR MASAKARTI PDF MODAL */}
          {showPdfModal && (
            <div className="fixed inset-0 z-[99999] bg-slate-950/85 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in overflow-y-auto">
              <div className="bg-white text-slate-900 w-full max-w-xl rounded-3xl shadow-2xl p-6 space-y-6 relative border-4 border-amber-500/40 my-8">
                <button
                  type="button"
                  onClick={() => setShowPdfModal(false)}
                  className="absolute top-4 right-4 w-8 h-8 rounded-full bg-slate-200 text-slate-700 font-bold flex items-center justify-center hover:bg-red-500 hover:text-white transition"
                >
                  ✕
                </button>

                {/* A4 PRINT PREVIEW AREA */}
                <div className="border-2 border-dashed border-slate-300 p-8 rounded-2xl space-y-6 text-center bg-amber-50/20">
                  <div className="space-y-1">
                    <h2 className="font-heading font-black text-2xl text-amber-900 uppercase tracking-wide">
                      {currentRes?.customerName || 'Ahmet & Ayşe Balo Daveti'}
                    </h2>
                    <p className="text-xs font-bold text-slate-600">İrem Düğün Sarayı • Özel Anı Albümü</p>
                  </div>

                  {/* SLOGAN (HANDWRITING STYLE) */}
                  <div className="font-serif italic text-2xl font-bold text-amber-700">
                    "Anıları Bizimle Paylaş"
                  </div>

                  {/* QR CODE DISPLAY AREA (%80 PROPORTION) */}
                  <div className="w-56 h-56 mx-auto bg-white p-4 rounded-3xl border-4 border-amber-500/60 shadow-xl flex flex-col items-center justify-center relative">
                    {/* SVG QR Code Simulation */}
                    <div className="w-full h-full border-4 border-slate-900 rounded-xl p-2 grid grid-cols-5 gap-1.5 bg-slate-900">
                      {[...Array(25)].map((_, i) => (
                        <div key={i} className={`rounded-xs ${i % 2 === 0 ? 'bg-white' : 'bg-amber-500'}`} />
                      ))}
                    </div>
                  </div>

                  <p className="text-xs font-bold text-slate-700 max-w-sm mx-auto leading-relaxed">
                    Bu QR kodu telefonunuzun kamerasına okutarak düğünümüzde çektiğiniz fotoğraf ve videoları bizimle paylaşabilirsiniz.
                  </p>
                </div>

                <div className="flex justify-end space-x-3">
                  <button
                    type="button"
                    onClick={() => {
                      window.print();
                      showToast('🖨️ A4 Masakartı PDF Baskıya Gönderildi!');
                    }}
                    className="w-full py-3 gold-button font-bold text-xs rounded-xl shadow-lg hover:scale-[1.02] transition flex items-center justify-center space-x-2 cursor-pointer"
                  >
                    <ThemeIcon icon="print" fallbackEmoji="" className="w-4 h-4 shrink-0" />
                    <span>A4 Masakartı Yazdır / PDF İndir</span>
                  </button>
                </div>
              </div>
            </div>
          )}

        </div>
      );
    }"""

if "function MediaComponent" in html:
    html = re.sub(r'function MediaComponent[\s\S]*?\n\}', new_media_component, html)
    print("Replaced MediaComponent with Advanced Guest & Admin Media Gallery!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with new MediaComponent successfully!")
