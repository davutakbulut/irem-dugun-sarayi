import React, { useState } from 'react';
import { ThemeIcon } from '../components/ThemeIcon';
import { DayDetailModalComponent } from '../components/Modals';

export function CalendarPage({ reservations = [], draftReservations = [], venues = [], onResClick, onReschedule, onCreateNewForDate, navigateTo }) {
  const [currentDate, setCurrentDate] = useState(new Date(2026, 7, 1)); // August 2026 default
  const [draggedResId, setDraggedResId] = useState(null);
  const [selectedDayData, setSelectedDayData] = useState(null);

  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();
  const monthNames = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"];
  
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const firstDayIndex = (new Date(year, month, 1).getDay() + 6) % 7; // Monday start

  const handlePrevMonth = () => {
    setCurrentDate(new Date(year, month - 1, 1));
  };

  const handleNextMonth = () => {
    setCurrentDate(new Date(year, month + 1, 1));
  };

  const handleToday = () => {
    setCurrentDate(new Date());
  };

  return (
    <div className="space-y-6">
      {/* DAY DETAIL INSPECTOR MODAL */}
      {selectedDayData && (
        <DayDetailModalComponent
          dayData={selectedDayData}
          venues={venues}
          onResClick={onResClick}
          navigateTo={navigateTo}
          onCreateNewForDay={(dateStr) => {
            if (onCreateNewForDate) onCreateNewForDate(dateStr);
          }}
          onClose={() => setSelectedDayData(null)}
        />
      )}

      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">İnteraktif Takvim & Saat Çakışma Denetleyicisi</h2>
          <p className="text-xs text-slate-500 dark:text-gray-400 font-medium">Salon doluluklarını inceleyin veya sürükle-bırak ile tarihleri değiştirin.</p>
        </div>
        <div className="flex items-center space-x-2 bg-white dark:bg-brand-card p-1.5 rounded-2xl border border-slate-200 dark:border-brand-border shadow-sm">
          <button onClick={handlePrevMonth} className="px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-brand-dark hover:bg-amber-500/10 text-xs font-bold transition flex items-center space-x-1">
            <span>← Önceki Ay</span>
          </button>
          <button onClick={handleToday} className="px-3 py-1.5 rounded-xl gold-button text-xs font-bold shadow-xs">
            <span>Bugün</span>
          </button>
          <button onClick={handleNextMonth} className="px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-brand-dark hover:bg-amber-500/10 text-xs font-bold transition flex items-center space-x-1">
            <span>Sonraki Ay →</span>
          </button>
        </div>
      </div>

      <div className="glass-panel p-6 rounded-3xl space-y-4 shadow-sm">
        <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border">
          <h3 className="font-bold text-lg text-amber-700 dark:text-gold-400 flex items-center space-x-2">
            <ThemeIcon icon="calendar" fallbackEmoji="📅" className="w-5 h-5 shrink-0" />
            <span>{monthNames[month]} {year}</span>
          </h3>
          <div className="flex items-center space-x-2 text-xs">
            <span className="text-amber-700 dark:text-gold-400 font-bold bg-amber-500/10 px-3 py-1 rounded-full border border-amber-500/30">
              👑 {reservations.filter(r => r.date && r.date.startsWith(`${year}-${(month + 1).toString().padStart(2, '0')}`)).length} Onaylı Etkinlik
            </span>
            <span className="text-amber-600 dark:text-amber-400 font-bold bg-amber-500/10 px-3 py-1 rounded-full border border-dashed border-amber-500/40">
              ⏳ Yarım Kalmış Taslaklar
            </span>
          </div>
        </div>

        <div className="grid grid-cols-7 gap-2 text-center text-xs">
          {['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'].map(d => (
            <div key={d} className="font-bold text-slate-500 dark:text-gray-400 p-2 bg-slate-100 dark:bg-brand-card rounded-xl uppercase tracking-wider text-[11px]">{d}</div>
          ))}

          {/* Padding Cells for First Day Offset */}
          {Array.from({ length: firstDayIndex }).map((_, i) => (
            <div key={`pad-${i}`} className="min-h-[100px] p-2 bg-slate-50/40 dark:bg-brand-dark/20 rounded-2xl border border-dashed border-slate-200/50 dark:border-brand-border/20 opacity-30"></div>
          ))}

          {/* Dynamic Month Days */}
          {Array.from({ length: daysInMonth }, (_, i) => i + 1).map(day => {
            const dateStr = `${year}-${(month + 1).toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
            const dayRes = reservations.filter(r => r.date === dateStr || r.eventDate === dateStr || r.startDate === dateStr);
            const dayDrafts = (draftReservations || []).filter(d => (d.startDate === dateStr || d.eventDate === dateStr || d.date === dateStr) && d.customerName);
            const totalCount = dayRes.length + dayDrafts.length;

            return (
              <div
                key={day}
                onDragOver={e => e.preventDefault()}
                onDrop={e => {
                  e.preventDefault();
                  if (draggedResId && onReschedule) {
                    onReschedule(draggedResId, dateStr);
                    setDraggedResId(null);
                  }
                }}
                onClick={() => setSelectedDayData({ day, dateStr, reservations: dayRes, drafts: dayDrafts })}
                className={`min-h-[100px] p-2 bg-white dark:bg-brand-card rounded-2xl border transition-all cursor-pointer hover:border-amber-500/60 shadow-2xs flex flex-col justify-between ${totalCount > 0 ? 'border-amber-500/40' : 'border-slate-200 dark:border-brand-border/40'}`}
              >
                <div className="flex justify-between items-center">
                  <span className={`font-bold text-xs ${totalCount > 0 ? 'text-amber-800 dark:text-gold-400 font-extrabold' : 'text-slate-600 dark:text-gray-400'}`}>{day}</span>
                  {totalCount > 0 && <span className="w-2 h-2 rounded-full bg-amber-500 animate-pulse"></span>}
                </div>
                <div className="space-y-1 my-1 overflow-y-auto max-h-[60px] custom-scrollbar">
                  {dayRes.map(r => (
                    <div
                      key={r.id}
                      draggable
                      onDragStart={() => setDraggedResId(r.id)}
                      onClick={(e) => { e.stopPropagation(); onResClick(r); }}
                      className="p-1 rounded bg-amber-500/10 hover:bg-amber-500/20 text-[10px] text-amber-800 dark:text-gold-300 font-bold truncate border border-amber-500/30 transition shadow-2xs"
                    >
                      {r.customerName}
                    </div>
                  ))}
                  {dayDrafts.map(d => (
                    <div
                      key={d.refKey}
                      onClick={(e) => {
                        e.stopPropagation();
                        if (navigateTo) navigateTo('create-reservation', { ref: d.refKey });
                      }}
                      title="Taslağı tamamlamak için tıklayın"
                      className="p-1 rounded bg-amber-500/10 hover:bg-amber-500/20 text-[10px] text-amber-700 dark:text-gold-400 font-bold truncate border border-dashed border-amber-500/50 transition cursor-pointer flex items-center space-x-1"
                    >
                      <span>⏳</span>
                      <span className="truncate">{(d.customerName || 'Taslak').split(' ')[0]}</span>
                    </div>
                  ))}
                </div>
                <div className="text-[9px] text-slate-400 text-right font-medium">
                  {totalCount > 0 ? `${dayRes.length} Etkinlik, ${dayDrafts.length} Taslak` : 'Boş'}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
