import React, { useState, useRef } from 'react';

export default function ImageDropzoneUploader({ value, onChange, label = 'Görsel Yükle', aspectGuide = '800x600 px', placeholderIcon = '📷' }) {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const processFile = (file) => {
    if (!file) return;
    if (!file.type.startsWith('image/')) {
      console.warn('Lütfen geçerli bir görsel dosyası (JPG, PNG, WebP vb.) seçiniz.');
      return;
    }
    const reader = new FileReader();
    reader.onload = (e) => {
      onChange(e.target.result);
    };
    reader.readAsDataURL(file);
  };

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    processFile(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    processFile(file);
  };

  return (
    <div className="space-y-1.5 text-xs">
      <div className="flex justify-between items-center">
        <label className="font-bold text-slate-700 dark:text-gray-300 block">{label}</label>
        <span className="text-[10px] text-amber-700 dark:text-gold-400 font-mono font-bold bg-amber-500/10 px-2 py-0.5 rounded-md border border-amber-500/20">
          📐 Önerilen Boyut: {aspectGuide}
        </span>
      </div>

      <div
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-2xl p-4 text-center cursor-pointer transition-all duration-200 flex flex-col items-center justify-center space-y-2 ${
          isDragging
            ? 'border-amber-500 bg-amber-500/10 scale-[1.01]'
            : 'border-slate-300 dark:border-brand-border/60 bg-slate-50 dark:bg-brand-dark/50 hover:border-amber-500/70 hover:bg-slate-100 dark:hover:bg-brand-card'
        }`}
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept="image/*"
          className="hidden"
        />

        {value ? (
          <div className="relative w-full h-36 rounded-xl overflow-hidden group border border-slate-200 dark:border-brand-border">
            <img src={value} alt="Yüklenen Görsel" className="w-full h-full object-cover rounded-xl" />
            <div className="absolute inset-0 bg-slate-900/70 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center text-white font-bold text-xs space-y-1 p-2">
              <span className="text-lg">🔄</span>
              <span>Görseli Değiştir</span>
              <span className="text-[10px] text-gray-300 font-normal">Tıklayın veya yeni görseli buraya bırakın</span>
            </div>
          </div>
        ) : (
          <div className="space-y-1 py-3">
            <div className="text-3xl">{placeholderIcon}</div>
            <div className="font-bold text-slate-800 dark:text-gray-100 text-xs">
              Görsel Yüklemek İçin Tıklayın veya Dosyayı Sürükleyip Bırakın
            </div>
            <div className="text-[10px] text-slate-500 dark:text-gray-400">
              PNG, JPG, WebP, GIF desteklenir (Maksimum 5MB)
            </div>
          </div>
        )}
      </div>

      <div className="pt-1">
        <input
          type="text"
          placeholder="veya doğrudan Görsel URL adresi yapıştırın..."
          value={value || ''}
          onChange={e => onChange(e.target.value)}
          className="w-full bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2 text-[11px] text-slate-600 dark:text-gray-400 font-mono"
        />
      </div>
    </div>
  );
}
