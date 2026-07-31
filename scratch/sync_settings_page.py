import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos_start = html.find('function SettingsComponent(')
pos_end = html.find('function ReservationDetailModal(', pos_start)

if pos_start != -1 and pos_end != -1:
    settings_code = html[pos_start:pos_end].strip()
    
    settings_code = settings_code.replace('function SettingsComponent(', 'export function SettingsPage(')
    settings_code = settings_code.replace('function SettingsComponent', 'export function SettingsPage')
    
    header_imports = """import React, { useState, useEffect } from 'react';
import { ThemeIcon } from '../components/ThemeIcon';
import { TAB_PERMISSIONS } from '../constants/initialData';
import { Page404Component, Page301Component, Page403Component, Page500Component } from './ErrorPages';

"""
    full_code = header_imports + settings_code + "\n"
    
    with open('src/pages/SettingsPage.jsx', 'w', encoding='utf-8') as sf:
        sf.write(full_code)
    print("Successfully updated src/pages/SettingsPage.jsx to match 767-line index.html version!")
else:
    print("Error: positions not found!", pos_start, pos_end)
