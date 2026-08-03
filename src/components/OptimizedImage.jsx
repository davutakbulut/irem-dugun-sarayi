import React, { useState, useMemo } from 'react';

export function OptimizedImage({ src, alt, className = '', priority = false, onClick }) {
  const [isLoaded, setIsLoaded] = useState(false);
  const [hasError, setHasError] = useState(false);

  // WebP Optimization & Mobile 3G Low-Bandwidth Compression
  const optimizedSrc = useMemo(() => {
    if (!src) return '';
    if (src.includes('images.unsplash.com')) {
      if (src.includes('w=')) return src;
      return `${src}&auto=format&fit=crop&w=600&q=60`;
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
