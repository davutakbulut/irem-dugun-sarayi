import React, { useState } from 'react';
import { ImageDropzoneUploader } from '../components/ImageDropzoneUploader';

export function MediaPage({ reservations = [], showToast = () => {} }) {
  const [mediaUrl, setMediaUrl] = useState('');

  return (
    <div className="space-y-6 max-w-2xl mx-auto">
      <div className="text-center">
        <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Medya & Fotoğraf Galerisi Yükleyici</h2>
        <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">Düğün salonları, organizasyon galerileri veya müşteri albümleri için yüksek çözünürlüklü görsel yükleyin.</p>
      </div>

      <div className="glass-panel p-6 rounded-3xl space-y-4 shadow-sm border border-slate-200 dark:border-brand-border">
        <ImageDropzoneUploader
          label="Galeri Fotoğrafı Yükle"
          value={mediaUrl}
          onChange={(url) => {
            setMediaUrl(url);
            showToast('📸 Medya Görseli Başarıyla Yüklendi ve Önizlemeye Alındı!');
          }}
          aspectGuide="1920x1080 px (Full HD Galeri Görseli)"
          placeholderIcon="📸"
        />
      </div>
    </div>
  );
}
