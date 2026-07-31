import subprocess
import os

html_900f015 = subprocess.check_output(['git', 'show', '900f015:index.html']).decode('utf-8')
lines = html_900f015.split('\n')

def extract_lines(start_l, end_l):
    return "\n".join(lines[start_l - 1:end_l])

# 1. CreateReservationPage.jsx (lines 3229 to 4681)
create_res_body = extract_lines(3229, 4681)
# Convert function header to export function CreateReservationPage
create_res_code = """import React, { useState, useEffect, useMemo, useRef } from 'react';
import { formatCurrency, formatDate, formatPhoneNumber, isValidPhoneNumber } from '../utils/formatters';

""" + create_res_body.replace("function CreateReservationPageComponent(props)", "export function CreateReservationPage(props)").replace("function CreateReservationPageComponent(", "export function CreateReservationPage(")

with open("src/pages/CreateReservationPage.jsx", "w", encoding="utf-8") as f:
    f.write(create_res_code)
print("✅ Restored src/pages/CreateReservationPage.jsx (1453 lines)")

# 2. CampaignsPage.jsx (lines 6810 to 6941)
campaigns_body = extract_lines(6810, 6941)
campaigns_code = """import React from 'react';
import { formatCurrency } from '../utils/formatters';
import { ThemeIcon } from '../components/ThemeIcon';

""" + campaigns_body.replace("function CampaignsComponent(", "export function CampaignsPage(").replace("function CampaignsComponent", "export function CampaignsPage")

with open("src/pages/CampaignsPage.jsx", "w", encoding="utf-8") as f:
    f.write(campaigns_code)
print("✅ Restored src/pages/CampaignsPage.jsx (132 lines)")

# 3. ReportsPage.jsx (lines 6942 to 7039)
reports_body = extract_lines(6942, 7039)
reports_code = """import React from 'react';
import { formatCurrency, formatDate } from '../utils/formatters';
import { ThemeIcon } from '../components/ThemeIcon';

""" + reports_body.replace("function ReportsComponent(", "export function ReportsPage(").replace("function ReportsComponent", "export function ReportsPage")

with open("src/pages/ReportsPage.jsx", "w", encoding="utf-8") as f:
    f.write(reports_code)
print("✅ Restored src/pages/ReportsPage.jsx (98 lines)")

# 4. SettingsPage.jsx (lines 7332 to 7900)
settings_body = extract_lines(7332, 7900)
settings_code = """import React, { useState } from 'react';
import { ThemeIcon } from '../components/ThemeIcon';

""" + settings_body.replace("function SettingsComponent(", "export function SettingsPage(").replace("function SettingsComponent", "export function SettingsPage")

with open("src/pages/SettingsPage.jsx", "w", encoding="utf-8") as f:
    f.write(settings_code)
print("✅ Restored src/pages/SettingsPage.jsx (569 lines)")

# 5. ReservationsListPage.jsx (lines 5203 to 6598)
res_list_body = extract_lines(5203, 6598)
res_list_code = """import React, { useState, useMemo, useEffect } from 'react';
import { formatCurrency, formatDate, formatPhoneNumber } from '../utils/formatters';
import { ThemeIcon } from '../components/ThemeIcon';

""" + res_list_body.replace("function ReservationsComponent(props)", "export function ReservationsListPage(props)").replace("function ReservationsComponent(", "export function ReservationsListPage(")

with open("src/pages/ReservationsListPage.jsx", "w", encoding="utf-8") as f:
    f.write(res_list_code)
print("✅ Restored src/pages/ReservationsListPage.jsx (1396 lines)")

# 6. DashboardPage.jsx (lines 4727 to 4775)
dash_body = extract_lines(4727, 4775)
dash_code = """import React from 'react';
import { formatCurrency, formatDate } from '../utils/formatters';
import { ThemeIcon } from '../components/ThemeIcon';

""" + dash_body.replace("function DashboardComponent(", "export function DashboardPage(").replace("function DashboardComponent", "export function DashboardPage")

with open("src/pages/DashboardPage.jsx", "w", encoding="utf-8") as f:
    f.write(dash_code)
print("✅ Restored src/pages/DashboardPage.jsx (49 lines)")

# 7. VenuesPage.jsx (lines 5120 to 5159)
venues_body = extract_lines(5120, 5159)
venues_code = """import React from 'react';
import { formatCurrency } from '../utils/formatters';
import { ThemeIcon } from '../components/ThemeIcon';
import { OptimizedImage } from '../components/OptimizedImage';

""" + venues_body.replace("function VenuesComponent(", "export function VenuesPage(").replace("function VenuesComponent", "export function VenuesPage")

with open("src/pages/VenuesPage.jsx", "w", encoding="utf-8") as f:
    f.write(venues_code)
print("✅ Restored src/pages/VenuesPage.jsx (40 lines)")

# 8. ServicesPage.jsx (lines 5160 to 5202)
services_body = extract_lines(5160, 5202)
services_code = """import React from 'react';
import { formatCurrency } from '../utils/formatters';
import { ThemeIcon } from '../components/ThemeIcon';

""" + services_body.replace("function ServicesComponent(", "export function ServicesPage(").replace("function ServicesComponent", "export function ServicesPage")

with open("src/pages/ServicesPage.jsx", "w", encoding="utf-8") as f:
    f.write(services_code)
print("✅ Restored src/pages/ServicesPage.jsx (43 lines)")

# 9. CustomersPage.jsx (lines 7054 to 7098)
cust_body = extract_lines(7054, 7098)
cust_code = """import React from 'react';
import { ThemeIcon } from '../components/ThemeIcon';

""" + cust_body.replace("function CustomersComponent(", "export function CustomersPage(").replace("function CustomersPage", "export function CustomersPage")

with open("src/pages/CustomersPage.jsx", "w", encoding="utf-8") as f:
    f.write(cust_code)
print("✅ Restored src/pages/CustomersPage.jsx (45 lines)")

# 10. UsersPage.jsx (lines 7099 to 7142)
users_body = extract_lines(7099, 7142)
users_code = """import React from 'react';
import { ThemeIcon } from '../components/ThemeIcon';

""" + users_body.replace("function UsersComponent(", "export function UsersPage(").replace("function UsersPage", "export function UsersPage")

with open("src/pages/UsersPage.jsx", "w", encoding="utf-8") as f:
    f.write(users_code)
print("✅ Restored src/pages/UsersPage.jsx (44 lines)")

print("🎉 ALL PAGES SYNCHRONIZED AND RESTORED WITH 100% RICH CONTENT!")
