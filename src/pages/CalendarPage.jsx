import React, { useState, useEffect, useRef } from 'react';
import { DayDetailModalComponent } from '../components/Modals.jsx';
import { createPortal } from 'react-dom';
import { ThemeIcon } from '../components/ThemeIcon.jsx';

export function CalendarComponent({ reservations = [], draftReservations = [], venues = [], onResClick, onReschedule, onCreateNewForDate, navigateTo }) {
      const [draggedResId, setDraggedResId] = useState(null);
      const [selectedDayData, setSelectedDayData] = useState(null);
      const [currentDate, setCurrentDate] = useState(new Date(2026, 7, 1)); // August 2026 default

      const year = currentDate.getFullYear();
      const month = currentDate.getMonth();

      const daysInMonth = new Date(year, month + 1, 0).getDate();
      const firstDayIndex = (new Date(year, month, 1).getDay() + 6) % 7;

      const monthName = currentDate.toLocaleDateString('tr-TR', { month: 'long', year: 'numeric' });

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

          <div className="flex justify-between items-center flex-wrap gap-3">
            <div>
              <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">İnteraktif Takvim & Saat Çakışma Denetleyicisi</h2>
              <p className="text-xs text-slate-500 dark:text-gray-400">Günün üzerine tıklayarak tüm salon doluluklarını inceleyin veya sürükleyip bırakın</p>
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={handlePrevMonth}
                className="px-3 py-1.5 bg-slate-100 dark:bg-brand-card hover:bg-slate-200 dark:hover:bg-brand-border rounded-xl font-bold text-xs text-slate-700 dark:text-gray-200 transition border border-slate-200 dark:border-brand-border"
              >
                ← Önceki Ay
              </button>
              <button
                onClick={handleToday}
                className="px-3 py-1.5 gold-button font-bold text-xs rounded-xl shadow transition"
              >
                Bugün
              </button>
              <button
                onClick={handleNextMonth}
                className="px-3 py-1.5 bg-slate-100 dark:bg-brand-card hover:bg-slate-200 dark:hover:bg-brand-border rounded-xl font-bold text-xs text-slate-700 dark:text-gray-200 transition border border-slate-200 dark:border-brand-border"
              >
                Sonraki Ay →
              </button>
            </div>
          </div>

          <div className="glass-panel p-6 rounded-3xl space-y-4 shadow-sm">
            <div className="flex items-center justify-between border-b border-slate-200 dark:border-brand-border pb-3">
              <h3 className="font-bold text-lg text-amber-700 dark:text-gold-400 capitalize">📅 {monthName}</h3>
              <div className="flex items-center space-x-3 text-xs">
                <span className="text-amber-700 dark:text-gold-400 font-bold bg-amber-500/10 px-3 py-1 rounded-full border border-amber-500/30">
                  👑 Onaylı Rezervasyonlar
                </span>
                <span className="text-amber-600 dark:text-amber-400 font-bold bg-amber-500/10 px-3 py-1 rounded-full border border-dashed border-amber-500/40">
                  ⏳ Yarım Kalmış Taslaklar
                </span>
              </div>
            </div>

            <div className="grid grid-cols-7 gap-2 text-center text-xs">
              {['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'].map(d => (
                <div key={d} className="font-bold text-slate-500 dark:text-gray-400 p-2 bg-slate-100 dark:bg-brand-card rounded-lg">{d}</div>
              ))}

              {/* Offset Blank Cells */}
              {Array.from({ length: firstDayIndex }).map((_, i) => (
                <div key={`blank-${i}`} className="min-h-[90px] p-2 rounded-xl bg-slate-50/50 dark:bg-brand-dark/20 opacity-30 border border-transparent"></div>
              ))}

              {/* Dynamic Days in Month */}
              {Array.from({ length: daysInMonth }, (_, i) => i + 1).map(day => {
                const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
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
                    onClick={() => setSelectedDayData({ dateStr, dayNumber: day, reservations: dayRes, drafts: dayDrafts })}
                    className={`min-h-[95px] p-2 rounded-xl border text-left flex flex-col justify-between transition cursor-pointer hover:shadow-md ${
                      totalCount > 0 ? 'bg-amber-50/80 dark:bg-brand-card border-amber-500/40 hover:border-amber-500' : 'bg-white dark:bg-brand-dark/40 border-slate-200 dark:border-brand-border/30 hover:border-emerald-500'
                    }`}
                  >
                    <div className="flex justify-between items-center mb-1">
                      <span className="font-bold text-xs text-slate-700 dark:text-gray-300">{day}</span>
                      {totalCount > 0 && (
                        <div className="flex items-center space-x-1">
                          {dayRes.length > 0 && (
                            <span className="text-[9px] font-bold text-amber-700 dark:text-gold-400 bg-amber-500/10 px-1.5 py-0.2 rounded border border-amber-500/20">
                              {dayRes.length} Etkinlik
                            </span>
                          )}
                          {dayDrafts.length > 0 && (
                            <span className="text-[9px] font-bold text-amber-600 dark:text-amber-400 bg-amber-500/10 px-1.5 py-0.2 rounded border border-dashed border-amber-500/40">
                              ⏳ {dayDrafts.length} Taslak
                            </span>
                          )}
                        </div>
                      )}
                    </div>
                    <div className="space-y-1">
                      {dayRes.map(r => (
                        <div
                          key={r.id}
                          draggable={true}
                          onDragStart={() => setDraggedResId(r.id)}
                          onClick={(e) => {
                            e.stopPropagation();
                            onResClick(r);
                          }}
                          className="bg-amber-500/20 text-amber-900 dark:text-gold-300 p-1 rounded text-[9px] font-bold truncate border border-amber-500/40 cursor-grab active:cursor-grabbing hover:bg-amber-500 hover:text-white transition"
                        >
                          ⋮⋮ {(r.customerName || 'Etkinlik').split(' ')[0]} ({r.timeSlot ? r.timeSlot.split('-')[0] : ''})
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
                          className="bg-amber-500/10 text-amber-700 dark:text-gold-400 p-1 rounded text-[9px] font-bold truncate border border-dashed border-amber-500/50 hover:bg-amber-500 hover:text-white transition cursor-pointer flex items-center space-x-1"
                        >
                          <span>⏳</span>
                          <span className="truncate">{(d.customerName || 'Taslak').split(' ')[0]} (Taslak)</span>
                        </div>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      );
    }

    // --- CAMPAIGNS COMPONENT ---
