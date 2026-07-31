import sys

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if 'function CreateReservationPageComponent({' in line:
        start_idx = i
    if 'function CustomerFormModal({' in line:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    comp_lines = lines[start_idx:end_idx]
    comp_text = "".join(comp_lines).strip()
    
    header = "import React, { useState, useEffect, useRef } from 'react';\nimport { createPortal } from 'react-dom';\nimport { ThemeIcon } from '../components/ThemeIcon.jsx';\n\nexport "
    
    with open('src/pages/CreateReservationPage.jsx', 'w', encoding='utf-8') as f:
        f.write(header + comp_text + "\n")
    print(f"Successfully synced CreateReservationPageComponent (lines {start_idx+1}-{end_idx}) into src/pages/CreateReservationPage.jsx!")
else:
    print(f"Could not locate start ({start_idx}) or end ({end_idx})!")
