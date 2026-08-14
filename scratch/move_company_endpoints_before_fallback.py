with open('server.js', 'r', encoding='utf-8') as f:
    code = f.read()

marker_start = "// -------------------------------------------------------------\n// 12. ŞİRKET BİLGİLERİ VE RESMİ SÖZLEŞME METİNLERİ ENDPOINTS"
idx_start = code.find(marker_start)

if idx_start != -1:
    endpoints_block = code[idx_start:]
    code_without = code[:idx_start].strip()
    
    # Find insert position: before HTML Rota Yönlendirmeleri
    insert_marker = "// HTML Rota Yönlendirmeleri"
    ins_idx = code_without.find(insert_marker)
    if ins_idx != -1:
        new_code = code_without[:ins_idx] + endpoints_block + "\n\n" + code_without[ins_idx:]
        with open('server.js', 'w', encoding='utf-8') as f:
            f.write(new_code)
        print("Moved company endpoints before 404 fallback handler successfully!")
