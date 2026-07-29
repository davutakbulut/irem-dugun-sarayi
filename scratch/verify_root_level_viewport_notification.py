with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check 1: Root App level globalAlert state and window.showGlobalAlert helper registered
has_root_helper = 'window.showGlobalAlert = (title, message, targetInputId = null)' in content
print(f"[CHECK 1] Root App level window.showGlobalAlert helper registered: {has_root_helper}")

# Check 2: Notification rendered at root App return level with z-[999999]
has_root_popup_render = 'z-[999999] max-w-md w-full animate-slide-left' in content
print(f"[CHECK 2] Root App level viewport popup rendered (z-[999999]): {has_root_popup_render}")

# Check 3: showAlertModal delegates to window.showGlobalAlert
has_delegation = 'if (window.showGlobalAlert)' in content and 'window.showGlobalAlert(title, message, targetInputId)' in content
print(f"[CHECK 3] Page components delegate alerts to root window.showGlobalAlert: {has_delegation}")

if has_root_helper and has_root_popup_render and has_delegation:
    print("\n✅ ALL ROOT LEVEL VIEWPORT NOTIFICATION CHECKS PASSED 100%!")
else:
    print("\n❌ SOME CHECKS FAILED!")
