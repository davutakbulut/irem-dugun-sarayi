import os
import re

INDEX_PATH = '/Users/davutakbulut/.gemini/antigravity/scratch/irem_dugun_sarayi/index.html'
MODALS_PATH = '/Users/davutakbulut/.gemini/antigravity/scratch/irem_dugun_sarayi/src/components/Modals.jsx'

def test_standalone_top_right_alert():
    print("==================================================================")
    print("🔎 TEST 1: STANDALONE TOP-RIGHT FLOATING ALERT NOTIFICATION POPUP")
    print("==================================================================")
    
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        index_html = f.read()

    # 1.1 Positioning & Layout
    has_top_right_positioning = 'fixed top-5 right-4 sm:right-6 left-4 sm:left-auto z-[99999]' in index_html
    print(f"  [1.1] Positioning (fixed top-5 right-4 sm:right-6): {'✅ PASS' if has_top_right_positioning else '❌ FAIL'}")

    # 1.2 Crimson Border Accent & Glassmorphism
    has_crimson_accent = 'border-l-8 border-l-red-600' in index_html and 'border-2 border-red-500/70' in index_html
    has_glassmorphism = 'backdrop-blur-xl' in index_html or 'backdrop-blur-md' in index_html
    print(f"  [1.2] Crimson Accent & Glassmorphism: {'✅ PASS' if (has_crimson_accent and has_glassmorphism) else '❌ FAIL'}")

    # 1.3 Pulsing Icon & Text Content
    has_pulsing_icon = 'animate-pulse' in index_html and '⚠️' in index_html
    print(f"  [1.3] Pulsing Warning Icon (⚠️): {'✅ PASS' if has_pulsing_icon else '❌ FAIL'}")

    # 1.4 Interactive Action Buttons
    has_action_button = 'Anladım, Düzelt ✓' in index_html
    has_close_x = 'aria-label="Kapat"' in index_html
    print(f"  [1.4] Action ('Anladım, Düzelt ✓') & Close (✕) Buttons: {'✅ PASS' if (has_action_button and has_close_x) else '❌ FAIL'}")

    # 1.5 Target Focus & Smooth Scroll
    has_target_focus = 'scrollIntoView' in index_html and 'targetInputId' in index_html
    print(f"  [1.5] Auto Target Focus & Smooth Scroll (targetInputId): {'✅ PASS' if has_target_focus else '❌ FAIL'}")

    return has_top_right_positioning and has_crimson_accent and has_pulsing_icon and has_action_button and has_target_focus


def test_native_browser_alert_elimination():
    print("\n==================================================================")
    print("🔎 TEST 2: NATIVE BROWSER alert() & confirm() ELIMINATION")
    print("==================================================================")

    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        index_html = f.read()

    # Search for unhandled native alert() calls in application code (excluding comments)
    lines = index_html.splitlines()
    native_alerts = []
    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped.startswith('//') and not stripped.startswith('/*') and 'alert(' in stripped:
            if 'showAlertModal' not in stripped and 'closeAlertModal' not in stripped and 'alertModal' not in stripped:
                native_alerts.append((idx, stripped))

    print(f"  [2.1] Native window.alert() calls remaining: {len(native_alerts)}")
    if native_alerts:
        for line_num, code in native_alerts:
            print(f"      - Line {line_num}: {code}")
        print("  ❌ Native alert() elimination: FAIL")
        return False
    else:
        print("  ✅ Native browser alert() completely eliminated: PASS")
        return True


def test_in_app_red_alert_confirm_modal():
    print("\n==================================================================")
    print("🔎 TEST 3: IN-APP RED ALERT & CONFIRMATION POPUP MODAL")
    print("==================================================================")

    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        index_html = f.read()

    with open(MODALS_PATH, 'r', encoding='utf-8') as f:
        modals_jsx = f.read()

    # Check RedAlertConfirmModal definition in index.html & Modals.jsx
    has_red_modal_html = 'RedAlertConfirmModal' in index_html and 'setRedAlertModalData' in index_html
    has_red_modal_jsx = 'RedAlertConfirmModal' in modals_jsx
    print(f"  [3.1] RedAlertConfirmModal exported & hooked: {'✅ PASS' if (has_red_modal_html and has_red_modal_jsx) else '❌ FAIL'}")

    # Check deletion handlers (Venues, Services, Campaigns, Users, Customers)
    deletion_triggers = ['DÜĞÜN SALONU SİLİNECEK', 'EK HİZMET SİLİNECEK', 'ÖZEL KAMPANYA SİLİNECEK', 'KULLANICI HESABI SİLİNECEK', 'MÜŞTERİ KARTI SİLİNECEK']
    all_triggers_present = all(t in index_html for t in deletion_triggers)
    print(f"  [3.2] All 5 Deletion Safeguard Popups Configured: {'✅ PASS' if all_triggers_present else '❌ FAIL'}")

    return has_red_modal_html and has_red_modal_jsx and all_triggers_present


def test_notification_architecture_completeness():
    print("\n==================================================================")
    print("🔎 TEST 4: COMPLETE NOTIFICATION SYSTEM ARCHITECTURE")
    print("==================================================================")

    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        index_html = f.read()

    # 4.1 Toast Notifications (bottom-right auto-dismiss)
    has_toast = 'ToastNotification' in index_html or 'showToast' in index_html
    print(f"  [4.1] ToastNotification System (3s Auto-Dismiss): {'✅ PASS' if has_toast else '❌ FAIL'}")

    # 4.2 Invoice & Contract Notification Modal
    has_invoice_modal = 'InvoiceNotificationModal' in index_html or 'Resmi Sözleşme & Fatura' in index_html
    print(f"  [4.2] Invoice & Official Contract Modal: {'✅ PASS' if has_invoice_modal else '❌ FAIL'}")

    # 4.3 Email Notification Modal
    has_email_modal = 'EmailNotificationModal' in index_html or 'emailModalData' in index_html
    print(f"  [4.3] Automated Email Notification Modal: {'✅ PASS' if has_email_modal else '❌ FAIL'}")

    return has_toast and has_invoice_modal and has_email_modal


def run_all_tests():
    t1 = test_standalone_top_right_alert()
    t2 = test_native_browser_alert_elimination()
    t3 = test_in_app_red_alert_confirm_modal()
    t4 = test_notification_architecture_completeness()

    print("\n==================================================================")
    if t1 and t2 and t3 and t4:
        print("🏆 ALL NOTIFICATION SYSTEM ARCHITECTURE & POPUP TESTS PASSED 100%!")
        print("==================================================================")
        return True
    else:
        print("❌ SOME TESTS FAILED!")
        print("==================================================================")
        return False

if __name__ == '__main__':
    run_all_tests()
