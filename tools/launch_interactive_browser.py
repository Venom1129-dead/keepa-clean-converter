import ctypes
import json
import os
import subprocess
import sys
import time
import urllib.request
from ctypes import wintypes

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

SW_RESTORE = 9
SW_SHOW = 5
SW_SHOWMAXIMIZED = 3

class STARTUPINFOW(ctypes.Structure):
    _fields_ = [
        ('cb', wintypes.DWORD),
        ('lpReserved', wintypes.LPWSTR),
        ('lpDesktop', wintypes.LPWSTR),
        ('lpTitle', wintypes.LPWSTR),
        ('dwX', wintypes.DWORD),
        ('dwY', wintypes.DWORD),
        ('dwXSize', wintypes.DWORD),
        ('dwYSize', wintypes.DWORD),
        ('dwXCountChars', wintypes.DWORD),
        ('dwYCountChars', wintypes.DWORD),
        ('dwFillAttribute', wintypes.DWORD),
        ('dwFlags', wintypes.DWORD),
        ('wShowWindow', wintypes.WORD),
        ('cbReserved2', wintypes.WORD),
        ('lpReserved2', ctypes.POINTER(wintypes.BYTE)),
        ('hStdInput', wintypes.HANDLE),
        ('hStdOutput', wintypes.HANDLE),
        ('hStdError', wintypes.HANDLE),
    ]

class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ('hProcess', wintypes.HANDLE),
        ('hThread', wintypes.HANDLE),
        ('dwProcessId', wintypes.DWORD),
        ('dwThreadId', wintypes.DWORD),
    ]

def get_windows_on_default_desktop():
    """Returns list of (hwnd, pid, title) for all windows on WinSta0\\Default."""
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    hDesk = user32.OpenDesktopW("Default", 0, False, 0x01FF)
    wins = []
    def win_cb(hwnd, lparam):
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            pid = ctypes.c_ulong()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            wins.append((hwnd, pid.value, buff.value))
        return True

    if hDesk:
        user32.EnumDesktopWindows(hDesk, WNDENUMPROC(win_cb), 0)
        user32.CloseDesktop(hDesk)
    return wins

def find_browser_windows_on_default():
    """Finds Chrome or Edge windows on Default desktop."""
    all_wins = get_windows_on_default_desktop()
    browser_wins = []
    keywords = ["Chrome", "Edge", "Gumroad", "PayPal", "Printify", "Gemini", "ChatGPT", "Claude", "DeepSeek"]
    for hwnd, pid, title in all_wins:
        if any(k.lower() in title.lower() for k in keywords):
            browser_wins.append((hwnd, pid, title))
    return browser_wins

def bring_window_to_front(hwnd):
    """Brings the target window to the foreground and un-minimizes it."""
    try:
        user32.ShowWindow(hwnd, SW_RESTORE)
        user32.SetForegroundWindow(hwnd)
        user32.BringWindowToTop(hwnd)
        return True
    except Exception as e:
        print(f"Error bringing window to front: {e}")
        return False

def launch_via_task_scheduler(bat_path):
    """Registers and executes an interactive task via Task Scheduler."""
    task_name = "AIIncome_Dedicated_AI_Browser"
    print(f"[*] Registering Task Scheduler task '{task_name}' for interactive launch...")
    
    # Create the task
    create_cmd = [
        "schtasks", "/create",
        "/tn", task_name,
        "/tr", f'cmd.exe /c "{bat_path}"',
        "/sc", "ONCE",
        "/st", "23:59",
        "/f",
        "/it"
    ]
    res = subprocess.run(create_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[!] Warning: schtasks /create returned code {res.returncode}: {res.stderr.strip()}")
    else:
        print(f"[+] Task '{task_name}' successfully created.")

    # Run the task
    run_cmd = ["schtasks", "/run", "/tn", task_name]
    res_run = subprocess.run(run_cmd, capture_output=True, text=True)
    print(f"[*] schtasks /run output: {res_run.stdout.strip()}")
    return res_run.returncode == 0

def launch_via_create_process(bat_path):
    """Fallback: Launches batch file via CreateProcessW specifying WinSta0\\Default."""
    print("[*] Launching via Win32 CreateProcessW on WinSta0\\Default...")
    si = STARTUPINFOW()
    si.cb = ctypes.sizeof(si)
    si.lpDesktop = "WinSta0\\Default"
    si.dwFlags = 1 # STARTF_USESHOWWINDOW
    si.wShowWindow = SW_SHOW
    pi = PROCESS_INFORMATION()

    cmd = f'cmd.exe /c "{bat_path}"'
    # CREATE_BREAKAWAY_FROM_JOB (0x01000000) | CREATE_NEW_PROCESS_GROUP (0x00000200)
    flags = 0x01000000 | 0x00000200

    res = kernel32.CreateProcessW(
        None, cmd, None, None, False, flags, None, None, ctypes.byref(si), ctypes.byref(pi)
    )
    if not res:
        err = ctypes.get_last_error()
        print(f"[!] CreateProcessW failed with error {err}")
        return False
    print(f"[+] CreateProcessW succeeded. PID: {pi.dwProcessId}")
    return True

def verify_and_focus(max_wait_seconds=15):
    """Loop verifying window appears on Default desktop and brings it to front."""
    print(f"[*] Entering verification loop (up to {max_wait_seconds}s)...")
    start_time = time.time()
    while time.time() - start_time < max_wait_seconds:
        browser_wins = find_browser_windows_on_default()
        if browser_wins:
            print(f"[+] Verified {len(browser_wins)} browser window(s) on interactive desktop 'Default':")
            for hwnd, pid, title in browser_wins:
                print(f"    - HWND: {hwnd} | PID: {pid} | Title: {title}")
                bring_window_to_front(hwnd)
            return True
        time.sleep(1)
    return False

def verify_cdp_tabs():
    """Checks remote debugging port 9222 to verify tabs."""
    try:
        req = urllib.request.Request("http://127.0.0.1:9222/json/list")
        with urllib.request.urlopen(req, timeout=3) as resp:
            tabs = json.loads(resp.read().decode("utf-8"))
            print(f"[+] CDP Remote Debugging Active. Total tabs loaded: {len(tabs)}")
            for t in tabs[:5]:
                print(f"    - Tab: {t.get('title', '')} ({t.get('url', '')})")
            return len(tabs) > 0
    except Exception as e:
        print(f"[*] CDP port 9222 check: {e}")
        return False

def main():
    workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bat_path = os.path.join(workspace_dir, "tools", "launch_dedicated_ai_browser.bat")
    desktop_bat = os.path.expandvars(r"%USERPROFILE%\Desktop\Launch_Dedicated_AI_Browser.bat")

    target_bat = bat_path if os.path.exists(bat_path) else desktop_bat
    print(f"[*] Target launcher script: {target_bat}")

    # Step 0: Pre-sanitize profile to eliminate crash bubbles
    patch_script = os.path.join(workspace_dir, "tools", "patch_chrome_preferences.py")
    if os.path.exists(patch_script):
        try:
            subprocess.run([sys.executable, patch_script], check=True, capture_output=True)
            print("[+] Profile pre-sanitization verified (exit_type=Normal).")
        except Exception as e:
            print(f"[*] Warning: patch_chrome_preferences failed: {e}")

    # Step 1: Launch via Task Scheduler
    launched = launch_via_task_scheduler(target_bat)

    # Step 2: Verification loop on Default desktop
    verified = verify_and_focus(max_wait_seconds=12)

    if not verified:
        print("[!] Task Scheduler launch did not yield visible window in time. Trying CreateProcessW fallback...")
        launch_via_create_process(target_bat)
        verified = verify_and_focus(max_wait_seconds=10)

    # Step 3: Dismiss any residual restore bubble
    dismiss_script = os.path.join(workspace_dir, "tools", "dismiss_restore_popup.py")
    if os.path.exists(dismiss_script):
        try:
            subprocess.run([sys.executable, dismiss_script], check=False, capture_output=True)
        except Exception:
            pass

    # Step 4: Check CDP tabs
    time.sleep(2)
    verify_cdp_tabs()

    if verified:
        print("\n[SUCCESS] Dedicated AI Browser is physically active and visible on the user's monitor (WinSta0\\Default).")
        sys.exit(0)
    else:
        print("\n[FAILURE] Browser window not detected on Default desktop.")
        sys.exit(1)

if __name__ == "__main__":
    main()
