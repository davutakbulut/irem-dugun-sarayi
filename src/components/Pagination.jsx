import React from 'react';
import { ThemeIcon } from './ThemeIcon';

export function Pagination({
  currentPage = 1,
  totalItems = 0,
  pageSize = 10,
  onPageChange,
  onPageSizeChange,
  pageSizeOptions = [10, 20, 50, 100],
  className = ''
}) {
  const totalPages = Math.ceil(totalItems / pageSize) || 1;

  if (totalItems === 0) return null;

  const startItem = (currentPage - 1) * pageSize + 1;
  const endItem = Math.min(currentPage * pageSize, totalItems);

  // Generate page numbers with ellipsis for large page counts
  const getPageNumbers = () => {
    const pages = [];
    const maxVisible = 5;

    if (totalPages <= maxVisible) {
      for (let i = 1; i <= totalPages; i++) pages.push(i);
    } else {
      pages.push(1);
      if (currentPage > 3) pages.push('...');
      
      const start = Math.max(2, currentPage - 1);
      const end = Math.min(totalPages - 1, currentPage + 1);

      for (let i = start; i <= end; i++) {
        if (!pages.includes(i)) pages.push(i);
      }

      if (currentPage < totalPages - 2) pages.push('...');
      if (!pages.includes(totalPages)) pages.push(totalPages);
    }
    return pages;
  };

  return (
    <div className={`flex flex-col sm:flex-row items-center justify-between gap-4 py-4 px-2 border-t border-slate-200/80 dark:border-brand-border/60 ${className}`}>
      {/* LEFT: SUMMARY & PAGE SIZE SELECTOR */}
      <div className="flex flex-wrap items-center gap-3 text-xs text-slate-600 dark:text-gray-300 font-bold">
        <span>
          Toplam <strong className="text-slate-900 dark:text-white font-extrabold">{totalItems}</strong> kayıttan{' '}
          <span className="text-amber-600 dark:text-amber-400 font-black">{startItem}-{endItem}</span> arası gösteriliyor
        </span>

        {onPageSizeChange && (
          <div className="flex items-center space-x-1.5 ml-0 sm:ml-2">
            <span className="text-slate-400 dark:text-slate-500 font-normal">Sayfa Başı:</span>
            <select
              value={pageSize}
              onChange={(e) => {
                onPageSizeChange(Number(e.target.value));
                if (onPageChange) onPageChange(1);
              }}
              className="bg-slate-100 dark:bg-brand-dark text-slate-800 dark:text-gray-100 text-xs font-bold px-2 py-1 rounded-lg border border-slate-300 dark:border-brand-border outline-none focus:ring-2 focus:ring-amber-500/40 cursor-pointer"
            >
              {pageSizeOptions.map((opt) => (
                <option key={opt} value={opt}>
                  {opt} Adet
                </option>
              ))}
            </select>
          </div>
        )}
      </div>

      {/* RIGHT: NAVIGATION BUTTONS */}
      {totalPages > 1 && (
        <div className="flex items-center space-x-1">
          {/* FIRST PAGE */}
          <button
            type="button"
            disabled={currentPage === 1}
            onClick={() => onPageChange(1)}
            className="p-1.5 rounded-lg border border-slate-200 dark:border-brand-border bg-white dark:bg-brand-card text-slate-700 dark:text-gray-200 hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-30 disabled:cursor-not-allowed transition cursor-pointer"
            title="İlk Sayfa"
          >
            ⏮
          </button>

          {/* PREVIOUS PAGE */}
          <button
            type="button"
            disabled={currentPage === 1}
            onClick={() => onPageChange(currentPage - 1)}
            className="px-2.5 py-1.5 rounded-lg border border-slate-200 dark:border-brand-border bg-white dark:bg-brand-card text-slate-700 dark:text-gray-200 hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-30 disabled:cursor-not-allowed transition text-xs font-bold cursor-pointer"
            title="Önceki Sayfa"
          >
            ◄ Önceki
          </button>

          {/* PAGE NUMBERS */}
          <div className="flex items-center space-x-1 mx-1">
            {getPageNumbers().map((num, i) => {
              if (num === '...') {
                return (
                  <span key={`dots-${i}`} className="px-1 text-slate-400 text-xs font-bold">
                    ...
                  </span>
                );
              }
              const isActive = num === currentPage;
              return (
                <button
                  key={num}
                  type="button"
                  onClick={() => onPageChange(num)}
                  className={`w-8 h-8 rounded-lg text-xs font-extrabold transition cursor-pointer flex items-center justify-center ${
                    isActive
                      ? 'gold-button text-slate-950 shadow-sm scale-105 ring-2 ring-amber-500/30'
                      : 'bg-slate-100 dark:bg-brand-card text-slate-700 dark:text-gray-300 hover:bg-slate-200 dark:hover:bg-slate-800 border border-slate-200 dark:border-brand-border'
                  }`}
                >
                  {num}
                </button>
              );
            })}
          </div>

          {/* NEXT PAGE */}
          <button
            type="button"
            disabled={currentPage === totalPages}
            onClick={() => onPageChange(currentPage + 1)}
            className="px-2.5 py-1.5 rounded-lg border border-slate-200 dark:border-brand-border bg-white dark:bg-brand-card text-slate-700 dark:text-gray-200 hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-30 disabled:cursor-not-allowed transition text-xs font-bold cursor-pointer"
            title="Sonraki Sayfa"
          >
            Sonraki ►
          </button>

          {/* LAST PAGE */}
          <button
            type="button"
            disabled={currentPage === totalPages}
            onClick={() => onPageChange(totalPages)}
            className="p-1.5 rounded-lg border border-slate-200 dark:border-brand-border bg-white dark:bg-brand-card text-slate-700 dark:text-gray-200 hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-30 disabled:cursor-not-allowed transition cursor-pointer"
            title="Son Sayfa"
          >
            ⏭
          </button>
        </div>
      )}
    </div>
  );
}
