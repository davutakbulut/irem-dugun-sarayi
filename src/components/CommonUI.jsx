import React, { useState, useMemo } from 'react';
export { OptimizedImage } from './OptimizedImage.jsx';

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

export function WhatsAppButton({ phone, customerName = '', text = 'WhatsApp İle Mesaj At', className = '' }) {
  const cleanPhone = (phone || '').replace(/[^0-9]/g, '');
  const encodedText = encodeURIComponent(`Merhabalar ${customerName ? customerName + ' ' : ''}İrem Düğün Sarayı'ndan sizlere ulaşıyorum.`);
  const href = `https://wa.me/${cleanPhone}?text=${encodedText}`;

  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className={`bg-[#25D366] hover:bg-[#20BA5A] text-white font-extrabold px-3.5 py-2 rounded-xl text-xs inline-flex items-center space-x-2 shadow-md shadow-emerald-500/20 hover:shadow-lg hover:shadow-emerald-500/30 transition-all duration-200 transform hover:-translate-y-0.5 border border-emerald-400/30 active:scale-95 ${className}`}
    >
      <svg className="w-4 h-4 fill-white text-white shrink-0" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12.012 2c-5.506 0-9.969 4.463-9.969 9.969 0 1.758.459 3.473 1.332 4.989l-1.416 5.176 5.297-1.389c1.464.798 3.119 1.218 4.756 1.218 5.506 0 9.969-4.463 9.969-9.969s-4.463-9.994-9.969-9.994zm5.829 14.157c-.247.695-1.436 1.341-1.968 1.386-.532.045-1.214.218-3.957-.919-3.308-1.365-5.422-4.733-5.586-4.952-.164-.218-1.341-1.782-1.341-3.401 0-1.619.845-2.415 1.146-2.742.301-.327.655-.409.873-.409.218 0 .436.009.627.018.2.009.473-.073.746.573.273.646.928 2.264 1.009 2.428.082.164.136.355.027.573-.109.218-.164.355-.327.546-.164.191-.345.427-.491.573-.164.164-.336.345-.145.673.191.327.855 1.401 1.837 2.274 1.264 1.128 2.328 1.482 2.655 1.646.327.164.518.136.709-.082.191-.218.818-.955 1.036-1.282.218-.327.436-.273.736-.164.3.109 1.909.901 2.236 1.064.327.164.545.245.627.382.082.137.082.846-.164 1.541z" />
      </svg>
      <span>{text}</span>
    </a>
  );
}

