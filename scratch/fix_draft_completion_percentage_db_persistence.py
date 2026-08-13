import os, re

with open('server.js', 'r', encoding='utf-8') as f:
    server_code = f.read()

# Add server-side calculateFormCompletion function if needed
completion_calc_fn = """const calculateFormCompletionServer = (f) => {
  if (!f || typeof f !== 'object') return 0;
  let score = 0;
  if (f.newCustName || f.customerName || f.selectedCustomerId) score += 15;
  if (f.newCustPhone || f.customerPhone) score += 10;
  if (f.startDate || f.eventDate) score += 15;
  if (f.startTime && f.endTime) score += 10;
  if (f.venueId) score += 25;
  if (Array.isArray(f.selectedServices) && f.selectedServices.length > 0) score += 15;
  if (Number(f.depositPaid) > 0 || Number(f.totalAmount) > 0) score += 10;
  return Math.min(score, 100);
};
"""

if "calculateFormCompletionServer" not in server_code:
    # Insert right before GET /api/draft-reservations
    insert_pos = server_code.find("app.get('/api/draft-reservations'")
    if insert_pos != -1:
        server_code = server_code[:insert_pos] + completion_calc_fn + "\n" + server_code[insert_pos:]

# Update GET /api/draft-reservations returning object mapping
old_get_map = """        return {
          id: r.id,
          refKey: parsedNotesData?.refKey || r.id,
          isDraft: true,
          formData: parsedNotesData?.formData || null,
          venueId: r.venue_id || 'v1',
          customerId: r.customer_id || '',
          customerName: r.customer_name || 'Taslak Müşteri',
          customerEmail: r.customer_email || '',
          customerPhone: r.customer_phone || '',
          date: rawDate,
          eventDate: rawDate,
          startDate: rawDate,
          endDate: rawDate,
          timeSlot: r.time_slot || '19:00 - 23:00',
          guestCount: String(r.guest_count || 0),
          venuePrice: Number(r.venue_price || 0),
          subtotal: Number(r.subtotal || 0),
          totalAmount: Number(r.total_amount || 0),
          depositPaid: Number(r.deposit_paid || 0),
          notes: r.notes || '',
          status: 'DRAFT',
          paymentStatus: 'Taslak'
        };"""

new_get_map = """        const fData = parsedNotesData?.formData || null;
        const compPercentage = parsedNotesData?.completionPercentage !== undefined 
          ? parsedNotesData.completionPercentage 
          : calculateFormCompletionServer(fData);

        return {
          id: r.id,
          refKey: parsedNotesData?.refKey || r.id,
          isDraft: true,
          formData: fData,
          completionPercentage: compPercentage,
          customerInfo: parsedNotesData?.customerInfo || {
            name: r.customer_name || 'Taslak Müşteri',
            phone: r.customer_phone || '-',
            date: rawDate
          },
          accessLogs: parsedNotesData?.accessLogs || [],
          updatedAt: parsedNotesData?.updatedAt || r.created_at || new Date().toISOString(),
          venueId: r.venue_id || 'v1',
          customerId: r.customer_id || '',
          customerName: r.customer_name || 'Taslak Müşteri',
          customerEmail: r.customer_email || '',
          customerPhone: r.customer_phone || '',
          date: rawDate,
          eventDate: rawDate,
          startDate: rawDate,
          endDate: rawDate,
          timeSlot: r.time_slot || '19:00 - 23:00',
          guestCount: String(r.guest_count || 0),
          venuePrice: Number(r.venue_price || 0),
          subtotal: Number(r.subtotal || 0),
          totalAmount: Number(r.total_amount || 0),
          depositPaid: Number(r.deposit_paid || 0),
          notes: r.notes || '',
          status: 'DRAFT',
          paymentStatus: 'Taslak'
        };"""

if old_get_map in server_code:
    server_code = server_code.replace(old_get_map, new_get_map)
    print("Successfully updated GET /api/draft-reservations mapping!")

# Update POST /api/draft-reservations notesContent building
old_notes_content = "const notesContent = JSON.stringify({ refKey: draft.refKey || draftId, formData: f });"
new_notes_content = """const compPerc = draft.completionPercentage !== undefined ? draft.completionPercentage : calculateFormCompletionServer(f);
        const notesContent = JSON.stringify({
          refKey: draft.refKey || draftId,
          formData: f,
          completionPercentage: compPerc,
          customerInfo: draft.customerInfo || { name: custName, phone: custPhone, date: eventDate },
          accessLogs: draft.accessLogs || [],
          updatedAt: draft.updatedAt || new Date().toISOString()
        });"""

if old_notes_content in server_code:
    server_code = server_code.replace(old_notes_content, new_notes_content)
    print("Successfully updated POST /api/draft-reservations notesContent!")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(server_code)

print("Draft completion percentage persistence fix completed!")
