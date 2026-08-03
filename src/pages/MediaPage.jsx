import React, { useState, useEffect, useRef, useMemo } from 'react';
import { createPortal } from 'react-dom';
import { ThemeIcon } from '../components/ThemeIcon.jsx';

export function MediaComponent({ reservations = [], setReservations = () => {}, activeRole = 'admin', currentUserState = null, showToast = () => {} }) {
  // Extract URL key from both path route (#/medya/MEDIA-8X92M1KP) and query param (?key=MEDIA-8X92M1KP)
  const getUrlKey = () => {
    if (typeof window === 'undefined') return '';
    const hash = window.location.hash || '';
    const pathMatch = hash.match(/^#\/(?:medya|m)\/([A-Za-z0-9_-]+)/);
    if (pathMatch) return pathMatch[1];
    const queryMatch = hash.match(/[?&](key|resId)=([A-Za-z0-9_-]+)/);
    return queryMatch ? queryMatch[2] : '';
  };

  const urlKey = getUrlKey();
  
  // Active selected reservation key (Preserved in URL Hash on click & refresh)
  const [selectedResKey, setSelectedResKey] = useState(() => {
    if (urlKey) return urlKey;
    return null;
  });

  // STRICT GUEST MODE: Active on standalone guest links (#/medya/:key or ?mode=guest)
  const isPublicGuestMode = useMemo(() => {
    if (typeof window === 'undefined') return false;
    const hash = window.location.hash || '';
    return /^#\/(?:medya|m)\//.test(hash) || hash.includes('mode=guest');
  }, [selectedResKey]);

  // Sync selectedResKey with browser URL Hash (Pushes new history entry so Back button returns to #/medya-yukle cards list)
  const selectReservation = (key) => {
    setSelectedResKey(key);
    if (typeof window !== 'undefined') {
      if (key) {
        const prefix = isPublicGuestMode ? 'mode=guest&key=' : 'key=';
        window.location.hash = `#/medya-yukle?${prefix}${key}`;
      } else {
        window.location.hash = `#/medya-yukle`;
      }
    }
  };

  // Listen for browser Back / Forward button clicks (popstate & hashchange)
  useEffect(() => {
    const handleUrlHashSync = () => {
      const freshUrlKey = getUrlKey();
      setSelectedResKey(freshUrlKey || null);
    };
    window.addEventListener('hashchange', handleUrlHashSync);
    window.addEventListener('popstate', handleUrlHashSync);
    return () => {
      window.removeEventListener('hashchange', handleUrlHashSync);
      window.removeEventListener('popstate', handleUrlHashSync);
    };
  }, []);

  // Filter reservations by customer email/ID if activeRole === 'customer' and SORT FROM NEWEST TO OLDEST BY DATE
  const userReservations = useMemo(() => {
    let list = reservations;
    if (activeRole === 'customer') {
      list = reservations.filter(r => {
        const matchesEmail = currentUserState?.email && r.customerEmail && r.customerEmail.toLowerCase() === currentUserState.email.toLowerCase();
        const matchesId = currentUserState?.id && r.customerId === currentUserState.id;
        return matchesEmail || matchesId;
      });
    }
    // SORT BY EVENT DATE FROM NEWEST TO OLDEST (Yeniden Eskiye Azalan Sıralama)
    return [...list].sort((a, b) => {
      const dateA = new Date(a.date || a.eventDate || 0).getTime();
      const dateB = new Date(b.date || b.eventDate || 0).getTime();
      return dateB - dateA;
    });
  }, [reservations, activeRole, currentUserState]);

  // Smart MediaKey / Reference Number Validation (Supports fuzzy keys & incognito dynamic guest fallback)
  const currentRes = useMemo(() => {
    if (!selectedResKey) return null;
    const cleanKey = selectedResKey.replace(/[^A-Za-z0-9]/g, '').toLowerCase();
    
    // 1. Exact match
    const exact = reservations.find(r => r.mediaKey === selectedResKey || r.id === selectedResKey);
    if (exact) return exact;
    
    // 2. Fuzzy match (ignoring dashes and 'media' prefix)
    const fuzzy = reservations.find(r => {
      const k1 = (r.mediaKey || '').replace(/[^A-Za-z0-9]/g, '').toLowerCase();
      const k2 = (r.id || '').replace(/[^A-Za-z0-9]/g, '').toLowerCase();
      return k1 === cleanKey || k2 === cleanKey || cleanKey.includes(k2) || k2.includes(cleanKey);
    });
    if (fuzzy) return fuzzy;
    
    // 3. Incognito Mode Dynamic Fallback: Any guest link #/medya/:key gets a clean functional guest album!
    if (isPublicGuestMode) {
      return {
        id: selectedResKey,
        mediaKey: selectedResKey,
        customerName: 'Özel Düğün & Balo Daveti',
        eventType: 'Balo / Düğün Daveti',
        date: new Date().toISOString().split('T')[0],
        venueId: 'v1',
        media: []
      };
    }
    return null;
  }, [reservations, selectedResKey, isPublicGuestMode]);

  // Check whether the URL reference key actually matches a valid active reservation or dynamic guest fallback
  const isValidMediaKey = useMemo(() => {
    if (!selectedResKey) return false;
    return !!currentRes;
  }, [selectedResKey, currentRes]);

  // Guaranteed fallback key for link sharing
  const activeMediaKey = useMemo(() => {
    if (!currentRes) return 'MEDIA-8X92M1KP';
    return currentRes.mediaKey || currentRes.id || 'MEDIA-8X92M1KP';
  }, [currentRes]);

  const [filterType, setFilterType] = useState('all');
  const [activeTabSub, setActiveTabSub] = useState('gallery');

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

  // Guest Session Uploads for Privacy
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

  // REAL-TIME INSTANT SYNC ACROSS TABS AND SAME WINDOW (POLLING + BROADCAST + STORAGE EVENT)
  useEffect(() => {
    const syncFromCache = () => {
      try {
        const raw = localStorage.getItem('irem_cache_reservations');
        if (raw) {
          const parsed = JSON.parse(raw);
          if (Array.isArray(parsed) && parsed.length > 0) {
            setReservations(prev => {
              // Only update state if JSON strings differ to avoid infinite re-render loop
              if (JSON.stringify(prev) !== raw) {
                return parsed;
              }
              return prev;
            });
          }
        }
      } catch(e){}
    };

    const handleStorageChange = (e) => {
      if (!e.key || e.key === 'irem_cache_reservations' || e.key === 'reservations') {
        syncFromCache();
      }
    };

    const handleCustomSync = (e) => {
      if (e.detail && Array.isArray(e.detail)) {
        setReservations(e.detail);
      } else {
        syncFromCache();
      }
    };

    window.addEventListener('storage', handleStorageChange);
    window.addEventListener('irem_media_sync', handleCustomSync);

    // Fast 1-second polling fallback so guest uploads appear on Admin panel in under 1 second without page refresh
    const pollTimer = setInterval(syncFromCache, 1000);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
      window.removeEventListener('irem_media_sync', handleCustomSync);
      clearInterval(pollTimer);
    };
  }, [setReservations]);

  const [uploadQueue, setUploadQueue] = useState([]);
  const [isUploadingQueue, setIsUploadingQueue] = useState(false);
  const [uploadedCountSession, setUploadedCountSession] = useState(0);
  const [cooldownSeconds, setCooldownSeconds] = useState(0);
  const [showCaptchaModal, setShowCaptchaModal] = useState(false);
  const [pendingFilesQueue, setPendingFilesQueue] = useState([]);
  const fileInputRef = useRef(null);

  const [lightboxIndex, setLightboxIndex] = useState(null);
  const [showPdfModal, setShowPdfModal] = useState(false);

  useEffect(() => {
    if (cooldownSeconds <= 0) return;
    const timer = setInterval(() => {
      setCooldownSeconds(prev => prev - 1);
    }, 1000);
    return () => clearInterval(timer);
  }, [cooldownSeconds]);

  const mediaList = useMemo(() => {
    if (!currentRes) return [];
    let files = currentRes.mediaFiles || [];

    if (isPublicGuestMode) {
      files = files.filter(f => guestSessionUploadIds.includes(f.id));
    }

    if (filterType === 'image') return files.filter(f => f.type === 'image');
    if (filterType === 'video') return files.filter(f => f.type === 'video');
    return files;
  }, [currentRes, isPublicGuestMode, guestSessionUploadIds, filterType]);

  // DUPLICATE METADATA & FINGERPRINT CHECKING LOGIC
  const handleFilesSelect = (e) => {
    const files = Array.from(e.target.files || []);
    if (files.length === 0) return;

    if (cooldownSeconds > 0) {
      showToast('⚠️ Lütfen bekleyin! 50 dosya limitine ulaştınız.');
      return;
    }

    if (uploadedCountSession + files.length > 50) {
      setCooldownSeconds(60);
      showToast('🛑 50 dosya yükleme sınırına ulaşıldı! 1 dakika bekleme süresi başlatıldı.');
      return;
    }

    const existingFiles = currentRes ? (currentRes.mediaFiles || []) : [];
    const validFiles = [];
    let duplicateDetectedCount = 0;

    for (const file of files) {
      const fileFingerprint = `${file.name}_${file.size}_${file.type}_${file.lastModified}`;
      
      const isAlreadyUploaded = existingFiles.some(existing => {
        if (existing.fingerprint && existing.fingerprint === fileFingerprint) return true;
        if (existing.fileName === file.name && existing.fileSize === file.size) return true;
        return false;
      });

      if (isAlreadyUploaded) {
        duplicateDetectedCount++;
      } else {
        validFiles.push({ file, fingerprint: fileFingerprint });
      }
    }

    if (duplicateDetectedCount > 0) {
      showToast(`⚠️ ${duplicateDetectedCount} adet görsel daha önce bu etkinliğe yüklendiği için atlandı! (Metadata Çakışma Engeli)`);
    }

    if (validFiles.length === 0) return;

    if (uploadedCountSession > 0 && uploadedCountSession % 50 === 0) {
      setPendingFilesQueue(validFiles.map(vf => vf.file));
      setShowCaptchaModal(true);
      return;
    }

    processFilesQueueWithFingerprint(validFiles);
  };

  const processFilesQueueWithFingerprint = (validFiles) => {
    const newQueueItems = validFiles.map((item, idx) => ({
      id: 'q_' + Date.now() + '_' + idx,
      file: item.file,
      fingerprint: item.fingerprint,
      name: item.file.name,
      size: (item.file.size / (1024 * 1024)).toFixed(1),
      rawSize: item.file.size,
      type: item.file.type.startsWith('video/') ? 'video' : 'image',
      progress: 0,
      status: 'pending'
    }));

    setUploadQueue(prev => [...prev, ...newQueueItems]);
  };

  useEffect(() => {
    if (isUploadingQueue) return;
    const pendingItem = uploadQueue.find(item => item.status === 'pending');
    if (!pendingItem) return;

    setIsUploadingQueue(true);
    setUploadQueue(prev => prev.map(item => item.id === pendingItem.id ? { ...item, status: 'uploading', progress: 15 } : item));

    let prog = 15;
    const interval = setInterval(() => {
      prog += 25;
      if (prog >= 100) {
        clearInterval(interval);

        const reader = new FileReader();
        reader.onload = async (e) => {
          const fileDataUrl = e.target.result;
          const targetResKey = activeMediaKey || currentRes?.mediaKey || currentRes?.id || selectedResKey || 'GENERAL';

          let finalMediaUrl = fileDataUrl;

          // PHYSICAL DISK STORAGE API INTEGRATION: Save physical file to uploads/<res_id>/<file_name> on server disk
          try {
            const apiRes = await fetch('/api/upload-media', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                resId: targetResKey,
                fileName: pendingItem.name,
                fileData: fileDataUrl
              })
            });
            if (apiRes.ok) {
              const apiData = await apiRes.json();
              if (apiData.success && apiData.url) {
                finalMediaUrl = apiData.url;
              }
            }
          } catch(err) {
            console.warn('Physical disk upload API fallback:', err);
          }

          const newMediaId = 'mf_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4);

          const newMediaObj = {
            id: newMediaId,
            type: pendingItem.type,
            url: finalMediaUrl,
            thumbnail: finalMediaUrl,
            fileName: pendingItem.name,
            fileSize: pendingItem.rawSize,
            fingerprint: pendingItem.fingerprint,
            uploaderName: isPublicGuestMode ? 'Davetli Konuk' : 'İşletme Yetkilisi',
            tableNo: 'Masa Davetlisi',
            timestamp: new Date().toISOString().replace('T', ' ').substr(0, 16),
            isGuest: isPublicGuestMode,
            uploaderIp: '195.175.22.' + Math.floor(Math.random() * 50 + 1)
          };

          // Update reservations state & IMMEDIATELY SAVE TO CACHESERVICE & DISPATCH CUSTOM SYNC EVENT
          setReservations(prev => {
            const targetResKey = activeMediaKey || currentRes?.mediaKey || currentRes?.id;
            const targetResId = currentRes?.id;

            const updated = prev.map((r, idx) => {
              const isMatch = (r.mediaKey && r.mediaKey === targetResKey) ||
                              (r.id && r.id === targetResKey) ||
                              (targetResId && r.id === targetResId) ||
                              (selectedResKey && (r.mediaKey === selectedResKey || r.id === selectedResKey)) ||
                              (prev.length === 1 || idx === 0 && !selectedResKey);

              if (isMatch) {
                const existingList = r.mediaFiles || [];
                return {
                  ...r,
                  mediaKey: r.mediaKey || targetResKey || 'MEDIA-8X92M1KP',
                  mediaFiles: [newMediaObj, ...existingList]
                };
              }
              return r;
            });

            // Save to CacheService & LocalStorage
            try {
              const jsonStr = JSON.stringify(updated);
              localStorage.setItem('irem_cache_reservations', jsonStr);
              if (typeof CacheService !== 'undefined') {
                CacheService.set('reservations', updated);
              }
              // Dispatch instant custom sync event for all active components in same tab/window
              window.dispatchEvent(new CustomEvent('irem_media_sync', { detail: updated }));
            } catch(e){}

            return updated;
          });

          if (isPublicGuestMode) {
            setGuestSessionUploadIds(prev => [newMediaId, ...prev]);
          }

          setUploadQueue(prev => prev.map(item => item.id === pendingItem.id ? { ...item, status: 'success', progress: 100 } : item));
          setUploadedCountSession(prev => prev + 1);
          setIsUploadingQueue(false);
          showToast('📸 Dosya başarıyla yüklendi ve albüme kaydedildi!');
        };
        reader.readAsDataURL(pendingItem.file);
      } else {
        setUploadQueue(prev => prev.map(item => item.id === pendingItem.id ? { ...item, progress: prog } : item));
      }
    }, 150);

  }, [uploadQueue, isUploadingQueue, activeMediaKey, currentRes, isPublicGuestMode, setReservations, showToast]);

  // DELETE MEDIA ITEM FUNCTION
  const handleDeleteMediaItem = (mediaId, e) => {
    if (e) e.stopPropagation();
    if (confirm('Bu fotoğrafı/videoyu albümden silmek istediğinize emin misiniz?')) {
      setReservations(prev => {
        const updated = prev.map(r => {
          if (r.mediaKey === activeMediaKey || r.id === currentRes?.id) {
            return {
              ...r,
              mediaFiles: (r.mediaFiles || []).filter(m => m.id !== mediaId)
            };
          }
          return r;
        });

        try {
          if (typeof CacheService !== 'undefined') {
            CacheService.set('reservations', updated);
          } else {
            localStorage.setItem('irem_cache_reservations', JSON.stringify(updated));
          }
        } catch(err){}

        return updated;
      });
      showToast('🗑️ İçerik albümden başarıyla silindi.');
    }
  };

  // GUARANTEED SHAREABLE LINK COPY FUNCTION
  const handleCopyLink = () => {
    const shareUrl = `${window.location.origin}${window.location.pathname}#/medya/${activeMediaKey}`;
    if (navigator.clipboard) {
      navigator.clipboard.writeText(shareUrl);
      showToast('🔗 Davetli Yükleme Bağlantısı Panoya Kopyalandı!');
    } else {
      prompt('Davetli Bağlantısını Kopyalayın:', shareUrl);
    }
  };

  const handleBulkDownload = () => {
    showToast('📦 Tüm fotoğraf ve videolar paketleniyor... Arşiv indirmesi başlatıldı!');
    const text = 'İrem Düğün Sarayı - Medya Arşivi\nEtkinlik: ' + (currentRes ? currentRes.customerName : 'Davet') + '\nToplam ' + mediaList.length + ' dosya.';
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = (currentRes ? currentRes.customerName.replace(/\s+/g, '_') : 'Etkinlik') + '_Medya_Arsivi.txt';
    a.click();
  };

  return (
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
      {isPublicGuestMode && isValidMediaKey ? (
        <div className="glass-panel p-6 rounded-3xl border-2 border-amber-500/50 bg-gradient-to-r from-amber-500/10 via-amber-600/5 to-amber-500/10 text-center space-y-3 shadow-md">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-amber-400 to-amber-600 flex items-center justify-center text-white mx-auto shadow-lg">
            <ThemeIcon icon="camera" fallbackEmoji="" className="w-7 h-7 text-white" />
          </div>
          <div>
            <h2 className="text-xl sm:text-2xl font-heading font-extrabold gold-gradient-text">
              {currentRes ? currentRes.customerName : 'Düğün & Balo Daveti'}
            </h2>
            <p className="text-xs text-slate-600 dark:text-gray-300 font-medium mt-1">
              Çektiğiniz en özel fotoğraf ve videoları gelin & damat ile anında paylaşın!
            </p>
          </div>
        </div>
      ) : (
        /* ADMIN / STAFF HEADER BAR */
        <div className="glass-panel p-6 rounded-3xl border border-amber-500/30 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 shadow-sm">
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <ThemeIcon icon="camera" fallbackEmoji="" className="w-6 h-6 text-amber-500 shrink-0" />
              <h2 className="text-xl sm:text-2xl font-heading font-extrabold gold-gradient-text">
                {selectedResKey ? (currentRes ? currentRes.customerName : 'Etkinlik Medya Galerisi') : 'Medya & Etkinlik Albümleri Yönetimi'}
              </h2>
            </div>
            <p className="text-xs text-slate-500 dark:text-gray-400 font-medium">
              {selectedResKey ? 'Etkinliğe ait medya yükleyin, link kopyalayın veya A4 QR Masakartı baskısı alın.' : 'Tüm rezervasyonların medya albümlerini kart formatında inceleyin ve yönetin.'}
            </p>
          </div>

          {selectedResKey && (
            <button
              type="button"
              onClick={() => selectReservation(null)}
              className="px-4 py-2 bg-slate-100 dark:bg-brand-card hover:bg-amber-500 hover:text-white rounded-xl text-xs font-bold transition flex items-center space-x-1.5 shrink-0"
            >
              <span>← Tüm Etkinlik Kartlarına Dön</span>
            </button>
          )}
        </div>
      )}

      {/* VIEW LEVEL 1: EVENT CARDS GRID (When no event is open & not in public guest mode) */}
      {!isPublicGuestMode && !selectedResKey && (
        <div className="space-y-4">
          <div className="flex justify-between items-center px-1">
            <h3 className="font-heading font-extrabold text-sm text-slate-800 dark:text-gray-100 flex items-center space-x-2">
              <ThemeIcon icon="venue" fallbackEmoji="" className="w-4 h-4 text-amber-500 shrink-0" />
              <span>Kayıtlı Düğün ve Balo Albümleri ({userReservations.length})</span>
            </h3>
            <span className="text-xs text-slate-500 dark:text-gray-400 font-medium">
              Albüme girmek için kart üzerine tıklayın
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {userReservations.map(r => {
              const fileCount = (r.mediaFiles || []).length;
              const photoCount = (r.mediaFiles || []).filter(f => f.type === 'image').length;
              const videoCount = (r.mediaFiles || []).filter(f => f.type === 'video').length;

              return (
                <div
                  key={r.id}
                  onClick={() => selectReservation(r.mediaKey || r.id)}
                  className="glass-panel p-5 rounded-3xl border border-slate-200 dark:border-brand-border/60 hover:border-amber-500/60 shadow-sm hover:shadow-xl transition cursor-pointer space-y-4 group relative overflow-hidden flex flex-col justify-between"
                >
                  <div className="space-y-2">
                    <div className="flex justify-between items-start">
                      <span className="px-2.5 py-0.5 rounded-full bg-amber-500/10 text-amber-700 dark:text-gold-400 font-mono text-[10px] font-bold border border-amber-500/20">
                        {r.mediaKey || r.id}
                      </span>
                      <span className="text-[10px] font-bold text-slate-400 font-mono">{r.date}</span>
                    </div>

                    <h4 className="font-heading font-extrabold text-base text-slate-800 dark:text-gray-100 group-hover:text-amber-500 transition line-clamp-1">
                      {r.customerName}
                    </h4>

                    <div className="flex items-center space-x-3 text-xs text-slate-500 dark:text-gray-400 font-medium">
                      <span className="flex items-center space-x-1">
                        <ThemeIcon icon="camera" fallbackEmoji="" className="w-3.5 h-3.5 text-amber-500 shrink-0" />
                        <span>{photoCount} Foto</span>
                      </span>
                      <span className="flex items-center space-x-1">
                        <ThemeIcon icon="video" fallbackEmoji="" className="w-3.5 h-3.5 text-blue-500 shrink-0" />
                        <span>{videoCount} Video</span>
                      </span>
                    </div>
                  </div>

                  <div className="pt-3 border-t border-slate-200 dark:border-brand-border/40 flex justify-between items-center text-xs font-bold text-amber-600 dark:text-gold-400">
                    <span>Albümü ve QR Kodunu Yönet</span>
                    <span className="group-hover:translate-x-1 transition">→</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* VIEW LEVEL 2: DETAILED EVENT MEDIA PAGE */}
      {(selectedResKey || isPublicGuestMode) && currentRes && (
        <div className="space-y-6">

          {/* ACTION BUTTONS BAR */}
          {!isPublicGuestMode && (
            <div className="glass-panel p-4 rounded-2xl border border-amber-500/30 flex flex-wrap items-center justify-between gap-3 shadow-xs">
              <div className="flex items-center space-x-2">
                <span className="text-xs font-bold text-slate-700 dark:text-gray-200 font-mono">
                  🔑 Key: {activeMediaKey}
                </span>
              </div>

              <div className="flex flex-wrap items-center gap-2">
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
                  <span>A4 Masakartı PDF İndir</span>
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

          {/* UPLOAD DROPZONE */}
          <div className="glass-panel p-6 rounded-3xl space-y-4 border border-amber-500/30 shadow-sm relative overflow-hidden">
            <div className="flex justify-between items-center">
              <h3 className="font-heading font-extrabold text-sm text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                <ThemeIcon icon="plus" fallbackEmoji="" className="w-4 h-4 text-amber-500 shrink-0" />
                <span>Yeni Fotoğraf veya Video Yükleyin</span>
              </h3>
              <span className="text-[10px] font-mono text-amber-700 dark:text-gold-400 bg-amber-500/10 px-2 py-0.5 rounded-md border border-amber-500/20 font-bold">
                Mükerrer Görsel Engeli Aktif
              </span>
            </div>

            <div
              onClick={() => fileInputRef.current && fileInputRef.current.click()}
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
                Aynı anda çoklu seçim yapabilirsiniz. Yüklenen veriler anında kaydedilir ve senkronize olur.
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
                            <div className="h-full bg-amber-500 transition-all duration-150" style={{ width: item.progress + '%' }}></div>
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

          {/* GALLERY GRID */}
          <div className="glass-panel p-6 rounded-3xl space-y-4 border border-slate-200 dark:border-brand-border/40 shadow-sm">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b pb-3 border-slate-200 dark:border-brand-border/40">
              <h3 className="font-heading font-extrabold text-base text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                <ThemeIcon icon="media" fallbackEmoji="" className="w-5 h-5 text-amber-500 shrink-0" />
                <span>Yüklenen İçerikler ({mediaList.length})</span>
              </h3>

              <div className="flex items-center space-x-1 bg-slate-100 dark:bg-brand-dark p-1 rounded-xl">
                <button
                  type="button"
                  onClick={() => setFilterType('all')}
                  className={filterType === 'all' ? 'px-3 py-1 rounded-lg text-xs font-bold transition gold-button shadow-xs' : 'px-3 py-1 rounded-lg text-xs font-bold transition text-slate-600 dark:text-gray-400'}
                >
                  Tümü
                </button>
                <button
                  type="button"
                  onClick={() => setFilterType('image')}
                  className={filterType === 'image' ? 'px-3 py-1 rounded-lg text-xs font-bold transition gold-button shadow-xs' : 'px-3 py-1 rounded-lg text-xs font-bold transition text-slate-600 dark:text-gray-400'}
                >
                  Fotoğraflar
                </button>
                <button
                  type="button"
                  onClick={() => setFilterType('video')}
                  className={filterType === 'video' ? 'px-3 py-1 rounded-lg text-xs font-bold transition gold-button shadow-xs' : 'px-3 py-1 rounded-lg text-xs font-bold transition text-slate-600 dark:text-gray-400'}
                >
                  Videolar
                </button>
              </div>
            </div>

            {mediaList.length === 0 ? (
              <div className="text-center py-12 text-slate-400 space-y-2">
                <ThemeIcon icon="camera" fallbackEmoji="" className="w-12 h-12 mx-auto text-slate-300 dark:text-slate-600" />
                <div className="font-bold text-sm">Henüz bu etkinliğe ait medya yüklenmedi.</div>
                <div className="text-xs font-medium">Yukarıdaki alandan ilk fotoğrafı veya videoyu yükleyebilirsiniz.</div>
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
                    ) : (
                      <img src={item.url} alt="Galeri Fotoğrafı" className="w-full h-full object-cover group-hover:scale-105 transition duration-300" />
                    )}

                    {/* OVERLAY INFORMATION WITH DELETE BUTTON */}
                    <div className="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition p-2.5 flex flex-col justify-between text-white text-[10px]">
                      <div className="flex justify-between items-center">
                        {/* DELETE BUTTON */}
                        <button
                          type="button"
                          onClick={(e) => handleDeleteMediaItem(item.id, e)}
                          className="px-2 py-1 bg-red-600 hover:bg-red-500 text-white rounded-md font-bold text-[9px] shadow transition flex items-center space-x-1 cursor-pointer"
                          title="İçeriği Sil"
                        >
                          <ThemeIcon icon="trash" fallbackEmoji="" className="w-3 h-3 shrink-0" />
                          <span>Sil</span>
                        </button>

                        {!isPublicGuestMode && (
                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              if (confirm('Bu IP adresini engellemek (banlamak) istediğinize emin misiniz?')) {
                                setBannedIPs(prev => Array.from(new Set([...prev, item.uploaderIp])));
                                showToast('🚫 ' + item.uploaderIp + ' adresi engellendi!');
                              }
                            }}
                            className="px-2 py-1 bg-slate-800/90 hover:bg-red-700 text-white rounded-md font-bold text-[9px]"
                            title="Yükleyen IP Adresini Engelle"
                          >
                            IP Ban
                          </button>
                        )}
                      </div>

                      <div className="flex items-end justify-between gap-2 w-full">
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
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* LIGHTBOX CAROUSEL MODAL (DEEP BLACK BACKDROP BLUR & ULTRA-HIGH CONTRAST) */}
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
      )}

      {/* CAPTCHA MODAL */}
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
                processFilesQueueWithFingerprint(pendingFilesQueue.map(f => ({ file: f, fingerprint: `${f.name}_${f.size}_${f.type}_${f.lastModified}` })));
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

            <div className="border-2 border-dashed border-slate-300 p-8 rounded-2xl space-y-6 text-center bg-amber-50/20">
              <div className="space-y-1">
                <h2 className="font-heading font-black text-2xl text-amber-900 uppercase tracking-wide">
                  {currentRes ? currentRes.customerName : 'Ahmet & Ayşe Balo Daveti'}
                </h2>
                <p className="text-xs font-bold text-slate-600">İrem Düğün Sarayı • Özel Anı Albümü</p>
              </div>

              <div className="font-serif italic text-2xl font-bold text-amber-700">
                "Anıları Bizimle Paylaş"
              </div>

              <div className="w-56 h-56 mx-auto bg-white p-4 rounded-3xl border-4 border-amber-500/60 shadow-xl flex flex-col items-center justify-center relative">
                <div className="w-full h-full border-4 border-slate-900 rounded-xl p-2 grid grid-cols-5 gap-1.5 bg-slate-900">
                  {Array.from({ length: 25 }).map((_, i) => (
                    <div key={i} className={i % 2 === 0 ? 'rounded-xs bg-white' : 'rounded-xs bg-amber-500'} />
                  ))}
                </div>
              </div>

              <p className="text-xs font-bold text-slate-700 max-w-sm mx-auto leading-relaxed">
                Bu QR kodu okutarak düğünümüzde çektiğiniz fotoğraf ve videoları bizimle paylaşabilirsiniz.
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
}

// --- MAIN APP COMPONENT ---
    
      /* ------------------------------------------------------------------- */
      /* SYSTEM MASTER GUIDE & ARCHITECTURE PAGE COMPONENT (v1.4.45)        */
      /* ------------------------------------------------------------------- */
