import React from 'react';

export function NotificationPopup({ alertModal, onClose }) {
  if (!alertModal || !alertModal.isOpen) return null;

  return (
    <div className="fixed top-4 right-4 sm:top-6 sm:right-6 z-[999999] max-w-md w-[calc(100vw-2rem)] animate-slide-down sm:animate-slide-left pointer-events-auto">
      <div className="bg-white/95 dark:bg-slate-900/95 border-2 border-red-500/70 rounded-2xl p-4 sm:p-5 shadow-[0_20px_50px_rgba(239,68,68,0.35)] backdrop-blur-xl flex items-start space-x-3.5 relative border-l-8 border-l-red-600">
        
        {/* Red Pulse Warning Icon */}
        <div className="w-10 h-10 rounded-xl bg-red-500/20 text-red-600 dark:text-red-400 flex items-center justify-center text-xl font-bold shrink-0 border border-red-500/30 animate-pulse mt-0.5">
          ⚠️
        </div>

        {/* Content Area */}
        <div className="flex-1 space-y-1 pr-6 text-left">
          <h4 className="font-heading font-extrabold text-sm sm:text-base text-slate-900 dark:text-white flex items-center space-x-1.5">
            <span>{alertModal.title}</span>
          </h4>
          <p className="text-xs text-slate-600 dark:text-gray-300 leading-relaxed font-semibold">
            {alertModal.message}
          </p>
          
          {/* Action Button */}
          <div className="pt-2">
            <button
              onClick={onClose}
              className="px-4 py-1.5 rounded-xl bg-red-600 hover:bg-red-500 text-white font-bold text-xs shadow-md transition hover:scale-[1.02] active:scale-[0.98] inline-flex items-center space-x-1"
            >
              <span>Anladım, Düzelt ✓</span>
            </button>
          </div>
        </div>

        {/* Close X Button */}
        <button
          onClick={onClose}
          className="absolute top-3 right-3 text-slate-400 hover:text-slate-700 dark:hover:text-white transition p-1"
          aria-label="Kapat"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
      </div>
    </div>
  );
}
