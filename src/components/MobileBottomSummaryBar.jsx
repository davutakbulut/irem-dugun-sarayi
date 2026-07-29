import React, { useState, useEffect } from 'react';
import { formatCurrency } from '../utils/formatters';

export function MobileBottomSummaryBar() {
  const [data, setData] = useState(null);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    window.updateMobileReservationSummary = (summaryData) => {
      setData(summaryData);
    };
    return () => {
      delete window.updateMobileReservationSummary;
    };
  }, []);

  if (!data) return null;

  const { remaining = 0, isFullyPaid = false, calculations = {}, isInvoiced = false, paymentStatus = 'Bekliyor', hasDeposit = false, hasConflict = false, onSubmit } = data;

  return (
    <>
      {/* BACKGROUND BACKDROP (Arkaya çok az karartı) */}
      {isOpen && (
        <div
          onClick={() => setIsOpen(false)}
          className="fixed inset-0 z-[8888] bg-black/25 backdrop-blur-[2px] transition-opacity duration-300 sm:hidden"
          aria-hidden="true"
        />
      )}

      {/* MOBILE BOTTOM-UP SLIDING SUMMARY DRAWER */}
      <div
        className={`fixed left-0 right-0 z-[8889] bg-white dark:bg-brand-card border-t-2 border-amber-500/40 rounded-t-3xl shadow-[0_-10px_40px_rgba(0,0,0,0.3)] transition-all duration-300 transform ease-in-out sm:hidden ${
          isOpen ? 'translate-y-0 bottom-16 max-h-[80vh] overflow-y-auto p-5 space-y-4' : 'translate-y-full bottom-16 p-0 max-h-0 pointer-events-none opacity-0'
        }`}
      >
        <div className="flex justify-between items-center border-b border-slate-200 dark:border-brand-border pb-3">
          <div className="flex items-center space-x-2">
            <span className="text-lg">📜</span>
            <h4 className="font-heading font-extrabold text-sm text-slate-800 dark:text-gray-100">
              Canlı Hesaplama & Sözleşme Kartı
            </h4>
          </div>
          <button
            onClick={() => setIsOpen(false)}
            className="w-7 h-7 rounded-full bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-300 flex items-center justify-center font-bold text-xs"
          >
            ✕
          </button>
        </div>

        {/* Detailed Breakdown */}
        {calculations && (
          <div className="space-y-2 text-xs">
            <div className="flex justify-between text-slate-600 dark:text-gray-300">
              <span>Salon Kiralama Fiyatı:</span>
              <span className="font-mono font-bold text-slate-800 dark:text-gray-100">{formatCurrency(calculations.venuePrice)}</span>
            </div>
            
            {calculations.serviceBreakdown && calculations.serviceBreakdown.length > 0 && (
              <div className="pl-2 border-l-2 border-amber-500/30 space-y-1">
                <div className="text-[11px] font-bold text-slate-500">Seçilen Ek Hizmetler ({calculations.serviceBreakdown.length}):</div>
                {calculations.serviceBreakdown.map(sb => (
                  <div key={sb.id} className="flex justify-between text-[11px] text-slate-600 dark:text-gray-400">
                    <span>• {sb.name} ({sb.quantity} adet)</span>
                    <span className="font-mono">{formatCurrency(sb.total)}</span>
                  </div>
                ))}
              </div>
            )}

            <div className="flex justify-between font-bold text-slate-700 dark:text-gray-200 pt-1 border-t border-slate-100 dark:border-brand-border">
              <span>Ara Toplam:</span>
              <span className="font-mono">{formatCurrency(calculations.subtotal)}</span>
            </div>

            {calculations.discount > 0 && (
              <div className="flex justify-between text-amber-600 dark:text-gold-400 font-bold">
                <span>Kampanya İndirimi:</span>
                <span className="font-mono">-{formatCurrency(calculations.discount)}</span>
              </div>
            )}

            {isInvoiced && (
              <div className="flex justify-between text-slate-600 dark:text-gray-300">
                <span>KDV (%20):</span>
                <span className="font-mono">{formatCurrency(calculations.vat)}</span>
              </div>
            )}

            <div className="flex justify-between font-extrabold text-sm text-slate-900 dark:text-white pt-2 border-t border-slate-200 dark:border-brand-border">
              <span>Genel Toplam Tutarı:</span>
              <span className="font-mono text-amber-800 dark:text-gold-400">{formatCurrency(calculations.grandTotal)}</span>
            </div>

            {hasDeposit && (
              <div className="flex justify-between text-emerald-600 dark:text-emerald-400 font-bold pt-1">
                <span>Tahsil Edilen Kapora ({paymentStatus}):</span>
                <span className="font-mono">-{formatCurrency(calculations.dep)}</span>
              </div>
            )}

            <div className={`flex justify-between font-extrabold text-sm p-3 rounded-2xl border mt-2 ${
              isFullyPaid
                ? 'bg-emerald-500/10 border-emerald-500/40 text-emerald-700 dark:text-emerald-300'
                : 'bg-red-500/10 border-red-500/30 text-red-600 dark:text-red-400'
            }`}>
              <span>Kalan Ödenecek Net Bakiye:</span>
              <span className="font-mono text-base">
                {isFullyPaid ? '0 ₺ (Ödendi ✓)' : formatCurrency(remaining)}
              </span>
            </div>
          </div>
        )}
      </div>

      {/* FIXED BOTTOM BAR ON MOBILE (Mobilde Ekranın En Altına Sabit Bar) */}
      <div className="fixed bottom-0 left-0 right-0 z-[8890] bg-slate-900/95 dark:bg-brand-card/95 border-t border-amber-500/40 p-2.5 sm:hidden shadow-[0_-5px_25px_rgba(0,0,0,0.4)] backdrop-blur-xl flex items-center justify-between gap-2">
        
        {/* Left Side: Toggle Details + Expanded Remaining Balance */}
        <div className="flex items-center space-x-2 shrink-0">
          <button
            type="button"
            onClick={() => setIsOpen(!isOpen)}
            className="bg-slate-800 dark:bg-brand-dark hover:bg-slate-700 text-amber-800 dark:text-gold-400 font-bold px-2.5 py-1.5 rounded-xl border border-amber-500/30 text-xs flex items-center space-x-1 shadow transition active:scale-95 shrink-0"
            title="Döküm Detaylarını Aç/Kapat"
          >
            <span>{isOpen ? '▼' : '▲'}</span>
            <span>Detaylar</span>
          </button>

          <div className="flex flex-col text-left">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider leading-none">
              Kalan Toplam:
            </span>
            <span className="font-mono font-extrabold text-base text-gold-400 leading-tight">
              {isFullyPaid ? '0 ₺ (Ödendi)' : formatCurrency(remaining)}
            </span>
          </div>
        </div>

        {/* Right Side: Icon-Enhanced Compact Create Button */}
        <button
          type="button"
          disabled={hasConflict}
          onClick={() => {
            if (onSubmit) onSubmit();
          }}
          className={`gold-button font-extrabold px-3 py-2 rounded-xl text-xs shadow-lg flex items-center space-x-1.5 shrink-0 ${
            hasConflict ? 'opacity-50 cursor-not-allowed' : 'active:scale-95'
          }`}
        >
          <svg className="w-4 h-4 text-amber-950 inline shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
          <span className="whitespace-nowrap">Rezervasyonu Oluştur</span>
        </button>
      </div>
    </>
  );
}
