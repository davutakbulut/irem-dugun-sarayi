import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

old_state_line = """    function CalendarComponent({ reservations = [], draftReservations = [], venues = [], onResClick, onReschedule, onCreateNewForDate, navigateTo }) {
      const [draggedResId, setDraggedResId] = useState(null);"""

new_state_line = """    function CalendarComponent({ reservations = [], draftReservations = [], venues = [], onResClick, onReschedule, onCreateNewForDate, navigateTo }) {
      const [draggedResId, setDraggedResId] = useState(null);
      const [dragOverDate, setDragOverDate] = useState(null);"""

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_state_line in content:
        content = content.replace(old_state_line, new_state_line)
        with open(h_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added dragOverDate state in {h_file}")
    else:
        print(f"old_state_line not found in {h_file}")

print("CalendarComponent dragOverDate state fixed across all files!")
