import ctypes
import os
import subprocess
import urllib.request
import json

user32 = ctypes.windll.user32
WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

# Check tasklist
out = subprocess.check_output(['tasklist', '/fi', 'imagename eq chrome.exe', '/fo', 'csv'], text=True)
pids = []
for line in out.strip().splitlines()[1:]:
    parts = line.split(',')
    if len(parts) >= 2:
        pid = parts[1].strip('"')
        try:
            pids.append(int(pid))
        except:
            pass
print(f"Total chrome.exe processes running: {len(pids)}, PIDs: {pids[:10]}")

# Check windows on Default desktop
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

chrome_wins = [w for w in wins if w[1] in pids]
print(f"Windows on Default belonging to Chrome PIDs: {len(chrome_wins)}")
for w in chrome_wins:
    print(f"  HWND: {w[0]} | PID: {w[1]} | Title: {w[2]}")
    # Force bring to top & restore
    user32.ShowWindow(w[0], 9) # SW_RESTORE
    user32.ShowWindow(w[0], 3) # SW_MAXIMIZE
    user32.SetForegroundWindow(w[0])
    user32.BringWindowToTop(w[0])

# Check CDP tabs
try:
    with urllib.request.urlopen("http://127.0.0.1:9222/json/list", timeout=3) as resp:
        tabs = json.loads(resp.read().decode("utf-8"))
        print(f"\nCDP verified! Total active browser tabs: {len(tabs)}")
        for i, t in enumerate(tabs):
            print(f"  Tab {i+1}: {t.get('title')} ({t.get('url')})")
except Exception as e:
    print("CDP query failed:", e)
