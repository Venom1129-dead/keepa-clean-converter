import ctypes
import os
import time
from ctypes import wintypes

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

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

si = STARTUPINFOW()
si.cb = ctypes.sizeof(si)
si.lpDesktop = "WinSta0\\Default"
pi = PROCESS_INFORMATION()

chrome_path = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
profile_dir = os.path.expandvars(r"%LOCALAPPDATA%\AIIncome_Dedicated_Browser")
cmd = f'"{chrome_path}" --user-data-dir="{profile_dir}" https://gumroad.com/settings/payouts'

res = kernel32.CreateProcessW(
    None,
    cmd,
    None,
    None,
    False,
    0,
    None,
    None,
    ctypes.byref(si),
    ctypes.byref(pi)
)
err = ctypes.get_last_error()
print(f"CreateProcess Chrome: {res}, PID: {pi.dwProcessId}, Err: {err}")

time.sleep(3)
exit_code = wintypes.DWORD()
kernel32.GetExitCodeProcess(pi.hProcess, ctypes.byref(exit_code))
print(f"Exit code after 3s: {exit_code.value} (STILL_ACTIVE is 259)")

# Check windows on Default
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
        if "Chrome" in buff.value or "Gumroad" in buff.value:
            wins.append((pid.value, buff.value))
    return True

if hDesk:
    user32.EnumDesktopWindows(hDesk, WNDENUMPROC(win_cb), 0)
    print("Matching windows on Default desktop:", wins)
