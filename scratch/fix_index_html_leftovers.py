import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Clean CreateReservationPageComponent section
start_marker = "    // --- 2. YENİ REZERVASYON OLUŞTUR (MODULAR CREATE RESERVATION PAGE) ---"
end_marker = "    // --- CUSTOMER FORM MODAL ---"

pos_start = content.find(start_marker)
pos_end = content.find(end_marker)

print(f"CreateReservation: pos_start={pos_start}, pos_end={pos_end}")
if pos_start != -1 and pos_end != -1:
    clean_create_res = """    // --- 2. YENİ REZERVASYON OLUŞTUR (MODULAR CREATE RESERVATION PAGE) ---
    function CreateReservationPageComponent(props) {
      return <CreateReservationPage {...props} />;
    }

"""
    content = content[:pos_start] + clean_create_res + content[pos_end:]

# 2. Clean ReservationsComponent section
res_start_marker = "    // --- 5. REZERVASYONLARIM & MASTER TAKVİM (MODULAR RESERVATIONS LIST PAGE) ---"
res_end_marker = "    function DayDetailModalComponent"

pos_res_start = content.find(res_start_marker)
pos_res_end = content.find(res_end_marker)

print(f"ReservationsComponent: pos_res_start={pos_res_start}, pos_res_end={pos_res_end}")
if pos_res_start != -1 and pos_res_end != -1:
    clean_res_comp = """    // --- 5. REZERVASYONLARIM & MASTER TAKVİM (MODULAR RESERVATIONS LIST PAGE) ---
    function ReservationsComponent(props) {
      return <ReservationsListPage {...props} />;
    }

    """
    content = content[:pos_res_start] + clean_res_comp + content[pos_res_end:]

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Cleaned index.html successfully!")
