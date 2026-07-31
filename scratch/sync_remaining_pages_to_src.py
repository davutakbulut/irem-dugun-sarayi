import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

def extract_and_export(comp_name, page_name, next_marker, extra_imports=""):
    p_start = html.find(f'function {comp_name}(')
    if p_start == -1:
        p_start = html.find(f'const {comp_name} =')
    
    p_end = html.find(next_marker, p_start)
    if p_start != -1 and p_end != -1:
        code = html[p_start:p_end].strip()
        code = code.replace(f'function {comp_name}(', f'export function {page_name}(')
        code = code.replace(f'function {comp_name}', f'export function {page_name}')
        
        full_code = f"import React, {{ useState, useMemo, useEffect }} from 'react';\nimport {{ ThemeIcon }} from '../components/ThemeIcon';\n{extra_imports}\n\n" + code + "\n"
        
        with open(f'src/pages/{page_name}.jsx', 'w', encoding='utf-8') as f:
            f.write(full_code)
        print(f"Successfully synced src/pages/{page_name}.jsx ({len(full_code.splitlines())} lines)")
    else:
        print(f"Error extracting {comp_name}", p_start, p_end)

extract_and_export('FinanceComponent', 'FinancePage', '// --- CUSTOMERS COMPONENT ---', "import { formatCurrency } from '../utils/formatters';")
extract_and_export('ReportsComponent', 'ReportsPage', '// --- FINANCE COMPONENT ---')
extract_and_export('VenuesComponent', 'VenuesPage', '// --- SERVICES COMPONENT ---', "import { VenueDetailModalComponent } from '../components/Modals';")
extract_and_export('ServicesComponent', 'ServicesPage', '// --- UNIFIED RESERVATIONS')

