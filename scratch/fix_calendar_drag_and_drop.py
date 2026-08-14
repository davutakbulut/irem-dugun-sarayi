import os, re

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix handleRescheduleReservation in App to update all date fields and sync to MySQL
    old_reschedule_fn = """      const handleRescheduleReservation = (resId, newDate) => {
        setReservations(prev => prev.map(r => r.id === resId ? { ...r, date: newDate, dateFormatted: newDate } : r));
        setSelectedResForDetail(prev => (prev && prev.id === resId ? { ...prev, date: newDate, dateFormatted: newDate } : prev));
        showToast(`Rezervasyon Tarihi ${formatDate(newDate)} Olarak Değiştirildi!`);
      };"""

    new_reschedule_fn = """      const handleRescheduleReservation = (resId, newDate) => {
        const targetRes = (reservations || []).find(r => r.id === resId);
        if (!targetRes) return;
        const updatedRes = {
          ...targetRes,
          date: newDate,
          eventDate: newDate,
          startDate: newDate,
          endDate: newDate,
          dateFormatted: newDate
        };
        handleUpdateReservation(updatedRes);
        setSelectedResForDetail(prev => (prev && prev.id === resId ? updatedRes : prev));
        showToast(`Rezervasyon Tarihi ${formatDate(newDate)} Olarak Değiştirildi ve Kaydedildi!`);
      };"""

    if old_reschedule_fn in content:
        content = content.replace(old_reschedule_fn, new_reschedule_fn)
        print(f"Updated handleRescheduleReservation in {h_file}")

    # 2. Fix Drag and Drop in CalendarComponent
    # In CalendarComponent, add dragOverDate state and robust HTML5 drag/drop events
    old_calendar_cell = """                return (
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
                  >"""

    new_calendar_cell = """                const isDragOver = dragOverDate === dateStr;
                return (
                  <div
                    key={day}
                    onDragOver={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      e.dataTransfer.dropEffect = 'move';
                    }}
                    onDragEnter={(e) => {
                      e.preventDefault();
                      setDragOverDate(dateStr);
                    }}
                    onDragLeave={() => setDragOverDate(null)}
                    onDrop={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      const resId = e.dataTransfer.getData('text/plain') || draggedResId;
                      if (resId && onReschedule) {
                        onReschedule(resId, dateStr);
                      }
                      setDraggedResId(null);
                      setDragOverDate(null);
                    }}
                    onClick={() => setSelectedDayData({ dateStr, dayNumber: day, reservations: dayRes, drafts: dayDrafts })}
                    className={`min-h-[95px] p-2 rounded-xl border text-left flex flex-col justify-between transition cursor-pointer hover:shadow-md ${
                      isDragOver
                        ? 'bg-amber-100/90 dark:bg-amber-900/60 border-2 border-amber-500 scale-[1.03] shadow-lg ring-2 ring-amber-400'
                        : totalCount > 0
                        ? 'bg-amber-50/80 dark:bg-brand-card border-amber-500/40 hover:border-amber-500'
                        : 'bg-white dark:bg-brand-dark/40 border-slate-200 dark:border-brand-border/30 hover:border-emerald-500'
                    }`}
                  >"""

    if old_calendar_cell in content:
        content = content.replace(old_calendar_cell, new_calendar_cell)
        print(f"Updated calendar cell drop handler in {h_file}")

    # Fix onDragStart in CalendarComponent
    old_drag_start_calendar = """                        <div
                          key={r.id}
                          draggable={true}
                          onDragStart={() => setDraggedResId(r.id)}"""

    new_drag_start_calendar = """                        <div
                          key={r.id}
                          draggable={true}
                          onDragStart={(e) => {
                            e.stopPropagation();
                            e.dataTransfer.setData('text/plain', r.id);
                            e.dataTransfer.effectAllowed = 'move';
                            setDraggedResId(r.id);
                          }}
                          onDragEnd={() => {
                            setDraggedResId(null);
                            setDragOverDate(null);
                          }}"""

    if old_drag_start_calendar in content:
        content = content.replace(old_drag_start_calendar, new_drag_start_calendar)
        print(f"Updated onDragStart in CalendarComponent in {h_file}")

    # Ensure CalendarComponent has const [dragOverDate, setDragOverDate] = useState(null);
    if "function CalendarComponent(" in content and "const [dragOverDate, setDragOverDate]" not in content:
        content = content.replace(
            "const [draggedResId, setDraggedResId] = useState(null);",
            "const [draggedResId, setDraggedResId] = useState(null);\n      const [dragOverDate, setDragOverDate] = useState(null);"
        )
        print(f"Added dragOverDate state in CalendarComponent in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully processed {h_file}!")

print("Calendar Drag & Drop synchronization completed across all files!")
