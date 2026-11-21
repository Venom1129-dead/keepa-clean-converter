import ctypes
import subprocess

user32 = ctypes.windll.user32
WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
hDesk = user32.OpenDesktopW("Default", 0, False, 0x01FF)

wins = []
def win_cb(hwnd, lparam):
    pid = ctypes.c_ulong()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    length = user32.GetWindowTextLengthW(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buff, length + 1)
    rect = (ctypes.c_long * 4)()
    user32.GetWindowRect(hwnd, rect)
    w = rect[2] - rect[0]
    h = rect[3] - rect[1]
    vis = user32.IsWindowVisible(hwnd)
    wins.append((hwnd, pid.value, buff.value, w, h, vis))
    return True

if hDesk:
    user32.EnumDesktopWindows(hDesk, WNDENUMPROC(win_cb), 0)

out = subprocess.check_output(["tasklist", "/fi", "imagename eq Antigravity.exe", "/fo", "csv"], text=True)
pids = set()
for line in out.strip().splitlines()[1:]:
    parts = line.split(",")
    if len(parts) >= 2:
        try:
            pids.add(int(parts[1].strip('"')))
        except ValueError:
            pass

print(f"Antigravity PIDs: {pids}")
antigravity_wins = [w for w in wins if w[1] in pids]
print(f"Windows belonging to Antigravity: {len(antigravity_wins)}")
for w in antigravity_wins:
    print(f"  HWND {w[0]} | PID {w[1]} | Visible={w[5]} | Size: {w[3]}x{w[4]} | Title: '{w[2]}'")
