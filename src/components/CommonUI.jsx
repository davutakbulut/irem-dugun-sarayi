import React, { useState, useMemo } from 'react';

export function ToastNotification({ message, isVisible, onClose }) {
  if (!isVisible) return null;
  return (
    <div className="fixed bottom-6 right-6 z-50 animate-bounce bg-slate-900/90 dark:bg-brand-card/95 text-white dark:text-gray-100 px-5 py-3 rounded-2xl shadow-2xl border border-amber-500/50 flex items-center space-x-3 text-xs font-bold backdrop-blur-md">
      <span className="text-lg">✨</span>
      <span>{message}</span>
      <button onClick={onClose} className="ml-2 text-gray-400 hover:text-white font-bold">✕</button>
    </div>
  );
}

export function OptimizedImage({ src, alt, className = '', priority = false, onClick }) {
  const [isLoaded, setIsLoaded] = useState(false);
  const [hasError, setHasError] = useState(false);

  const optimizedSrc = useMemo(() => {
    if (!src) return '';
    if (src.includes('unsplash.com')) {
      return src.includes('auto=format') ? src : `${src}&auto=format&fit=crop&q=80`;
    }
    return src;
  }, [src]);

  return (
    <div className={`relative overflow-hidden bg-slate-200 dark:bg-brand-dark ${className}`} onClick={onClick}>
      {!isLoaded && !hasError && (
        <div className="absolute inset-0 skeleton-shimmer z-10" />
      )}
      {hasError ? (
        <div className="w-full h-full flex items-center justify-center bg-slate-100 dark:bg-brand-card text-slate-400 text-xs font-bold">
          🖼️ Görsel
        </div>
      ) : (
        <img
          src={optimizedSrc}
          alt={alt || 'Görsel'}
          loading={priority ? 'eager' : 'lazy'}
          decoding="async"
          fetchPriority={priority ? 'high' : 'auto'}
          onLoad={() => setIsLoaded(true)}
          onError={() => setHasError(true)}
          className={`w-full h-full object-cover transition-opacity duration-500 ${isLoaded ? 'opacity-100' : 'opacity-0'}`}
        />
      )}
    </div>
  );
}

export function SkeletonCard() {
  return (
    <div className="glass-panel p-4 rounded-3xl space-y-3 border border-slate-200 dark:border-brand-border">
      <div className="h-36 rounded-2xl skeleton-shimmer" />
      <div className="h-4 w-3/4 rounded-lg skeleton-shimmer" />
      <div className="h-3 w-1/2 rounded-lg skeleton-shimmer" />
      <div className="flex justify-between items-center pt-2">
        <div className="h-4 w-20 rounded-lg skeleton-shimmer" />
        <div className="h-6 w-16 rounded-full skeleton-shimmer" />
      </div>
    </div>
  );
}

export function SkeletonTable({ rows = 4 }) {
  return (
    <div className="space-y-2">
      {[...Array(rows)].map((_, i) => (
        <div key={i} className="h-12 w-full rounded-xl skeleton-shimmer border border-slate-200/40" />
      ))}
    </div>
  );
}
