import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update userReservations sorting in MediaComponent
old_user_res = """  // Filter reservations by customer email/ID if activeRole === 'customer'
  const userReservations = useMemo(() => {
    if (activeRole === 'customer') {
      return reservations.filter(r => {
        const matchesEmail = currentUserState?.email && r.customerEmail && r.customerEmail.toLowerCase() === currentUserState.email.toLowerCase();
        const matchesId = currentUserState?.id && r.customerId === currentUserState.id;
        return matchesEmail || matchesId;
      });
    }
    return reservations;
  }, [reservations, activeRole, currentUserState]);"""

new_user_res = """  // Filter reservations by customer email/ID if activeRole === 'customer' and SORT FROM NEWEST TO OLDEST BY DATE
  const userReservations = useMemo(() => {
    let list = reservations;
    if (activeRole === 'customer') {
      list = reservations.filter(r => {
        const matchesEmail = currentUserState?.email && r.customerEmail && r.customerEmail.toLowerCase() === currentUserState.email.toLowerCase();
        const matchesId = currentUserState?.id && r.customerId === currentUserState.id;
        return matchesEmail || matchesId;
      });
    }
    // SORT BY EVENT DATE FROM NEWEST TO OLDEST (Yeniden Eskiye Azalan Sıralama)
    return [...list].sort((a, b) => {
      const dateA = new Date(a.date || a.eventDate || 0).getTime();
      const dateB = new Date(b.date || b.eventDate || 0).getTime();
      return dateB - dateA;
    });
  }, [reservations, activeRole, currentUserState]);"""

if old_user_res in html:
    html = html.replace(old_user_res, new_user_res)
    print("Updated MediaComponent userReservations to sort newest to oldest!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html sorting successfully!")
