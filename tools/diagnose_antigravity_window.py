import ctypes
import os
import subprocess

user32 = ctypes.windll.user32
WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

# Get Antigravity PIDs
out = subprocess.check_output(["tasklist", "/fi", "imagename eq Antigravity.exe", "/fo", "csv"], text=True)
pids = set()
for line in out.strip().splitlines()[1:]:
    parts = line.split(",")
    if len(parts) >= 2:
        try:
            pids.add(int(parts[1].strip('"')))
        except:
            pass

print("Antigravity PIDs:", pids)

hDesk = user32.OpenDesktopW("Default", 0, False, 0x01FF)
wins = []
def enum_cb(hwnd, lparam):
    pid = ctypes.c_ulong()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    if pid.value in pids:
        length = user32.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        rect = (ctypes.c_long * 4)()
        user32.GetWindowRect(hwnd, rect)
        vis = user32.IsWindowVisible(hwnd)
        wins.append((hwnd, pid.value, vis, rect[:], buff.value))
    return True

if hDesk:
    user32.EnumDesktopWindows(hDesk, WNDENUMPROC(enum_cb), 0)

print(f"Total windows found for Antigravity: {len(wins)}")
for w in wins:
    print(f"  HWND {w[0]} | PID {w[1]} | Vis={w[2]} | Rect={w[3]} | Title='{w[4]}'")
