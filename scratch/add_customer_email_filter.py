with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update MediaComponent signature and add userReservations filtering
old_sig = "function MediaComponent({ reservations = [], setReservations = () => {}, activeRole = 'admin', showToast = () => {} }) {"
new_sig = "function MediaComponent({ reservations = [], setReservations = () => {}, activeRole = 'admin', currentUserState = null, showToast = () => {} }) {"

if old_sig in html:
    html = html.replace(old_sig, new_sig)

old_selected_key = "  const [selectedResKey, setSelectedResKey] = useState(() => {"
new_filtered_res = """  const userReservations = useMemo(() => {
    if (activeRole === 'customer') {
      return reservations.filter(r => {
        const matchesEmail = currentUserState?.email && r.customerEmail && r.customerEmail.toLowerCase() === currentUserState.email.toLowerCase();
        const matchesId = currentUserState?.id && r.customerId === currentUserState.id;
        return matchesEmail || matchesId;
      });
    }
    return reservations;
  }, [reservations, activeRole, currentUserState]);

  const [selectedResKey, setSelectedResKey] = useState(() => {"""

if "const userReservations = useMemo" not in html:
    html = html.replace(old_selected_key, new_filtered_res)

# Replace reservations list references in MediaComponent
html = html.replace("Kayıtlı Düğün ve Balo Albümleri ({reservations.length})", "Kayıtlı Düğün ve Balo Albümleri ({userReservations.length})")
html = html.replace("reservations.map(r => {", "userReservations.map(r => {")
html = html.replace("reservations.map(r => (\n                <option", "userReservations.map(r => (\n                <option")

# Update App invocation of MediaComponent to pass currentUserState
old_app_inv = "<MediaComponent reservations={reservations} setReservations={setReservations} activeRole={activeRole} showToast={showToast} />"
new_app_inv = "<MediaComponent reservations={reservations} setReservations={setReservations} activeRole={activeRole} currentUserState={currentUserState} showToast={showToast} />"

if old_app_inv in html:
    html = html.replace(old_app_inv, new_app_inv)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Enforced customer email reservation filter in MediaComponent successfully!")
