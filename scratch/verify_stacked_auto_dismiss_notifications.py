with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check 1: globalAlerts array state and 3.5s auto-dismiss timer
has_stacked_state = 'const [globalAlerts, setGlobalAlerts] = useState([]);' in content and 'setTimeout(() => {' in content and '3500);' in content
print(f"[CHECK 1] Stacked globalAlerts queue state & 3.5s timer: {has_stacked_state}")

# Check 2: Vertical stack layout (flex flex-col space-y-3)
has_vertical_stack = 'flex flex-col space-y-3 pointer-events-none' in content
print(f"[CHECK 2] Vertical stack container (flex-col space-y-3): {has_vertical_stack}")

# Check 3: Mapping globalAlerts cards
has_card_mapping = 'globalAlerts.map((alert) => (' in content
print(f"[CHECK 3] Stacked cards rendering via globalAlerts.map: {has_card_mapping}")

if has_stacked_state and has_vertical_stack and has_card_mapping:
    print("\n✅ ALL STACKED AUTO-DISMISS NOTIFICATION QUEUE CHECKS PASSED 100%!")
else:
    print("\n❌ SOME CHECKS FAILED!")
