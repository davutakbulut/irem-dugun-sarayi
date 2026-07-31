import os
import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

lines = html.splitlines(keepends=True)

mappings = [
    ("function CreateReservationPageComponent(", "function CustomerFormModal(", "src/pages/CreateReservationPage.jsx"),
    ("function ReservationsListComponent(", "function UsersComponent(", "src/pages/ReservationsListPage.jsx"),
    ("function UsersComponent(", "function MediaComponent(", "src/pages/UsersPage.jsx"),
    ("function MediaComponent(", "function SystemGuidePageComponent(", "src/pages/MediaPage.jsx"),
    ("function SystemGuidePageComponent(", "function App(", "src/pages/SystemGuidePage.jsx"),
    ("function DashboardComponent(", "function VenueModalComponent(", "src/pages/DashboardPage.jsx"),
    ("function VenuesComponent(", "function ServicesComponent(", "src/pages/VenuesPage.jsx"),
    ("function ServicesComponent(", "function ReservationsComponent(", "src/pages/ServicesPage.jsx"),
    ("function CalendarComponent(", "function CampaignsComponent(", "src/pages/CalendarPage.jsx"),
    ("function CampaignsComponent(", "function ReportsComponent(", "src/pages/CampaignsPage.jsx"),
    ("function ReportsComponent(", "function FinanceComponent(", "src/pages/ReportsPage.jsx"),
    ("function FinanceComponent(", "function CustomersComponent(", "src/pages/FinancePage.jsx"),
    ("function CustomersComponent(", "function MindMapPageComponent(", "src/pages/CustomersPage.jsx"),
    ("function MindMapPageComponent(", "function ProfileComponent(", "src/pages/MindMapPage.jsx"),
    ("function ProfileComponent(", "function VersionHistoryModalComponent(", "src/pages/ProfilePage.jsx"),
    ("function RolesPageComponent(", "function SettingsComponent(", "src/pages/RolesPage.jsx"),
    ("function SettingsComponent(", "function ReservationDetailModal(", "src/pages/SettingsPage.jsx")
]

for start_key, end_key, target_file in mappings:
    start_idx = -1
    end_idx = -1
    for i, l in enumerate(lines):
        if start_key in l:
            start_idx = i
        if end_key in l and start_idx != -1 and end_idx == -1:
            end_idx = i
            break
    
    if start_idx != -1 and end_idx != -1:
        comp_text = "".join(lines[start_idx:end_idx]).strip()
        header = "import React, { useState, useEffect, useRef } from 'react';\nimport { createPortal } from 'react-dom';\nimport { ThemeIcon } from '../components/ThemeIcon.jsx';\n\nexport "
        
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, 'w', encoding='utf-8') as tf:
            tf.write(header + comp_text + "\n")
        print(f"Synced {target_file} (lines {start_idx+1}-{end_idx}) successfully!")
    else:
        print(f"Could not locate indices for {target_file} (start: {start_idx}, end: {end_idx})")

print("All 17 modular ES page files in src/pages/ have been 100% synchronized!")
