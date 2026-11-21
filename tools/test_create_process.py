import ctypes
from ctypes import wintypes
import os

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

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
si.lpDesktop = "WinSta0\\default"
pi = PROCESS_INFORMATION()

chrome_path = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
profile_dir = os.path.expandvars(r"%LOCALAPPDATA%\AIIncome_Dedicated_Browser")
urls = [
    "https://gumroad.com/settings/payouts",
    "https://gumroad.com/products/new",
    "https://www.paypal.com/signin",
    "https://kdp.amazon.com/",
    "https://printify.com/app/dashboard",
    "https://gemini.google.com/app",
    "https://chatgpt.com/",
    "https://claude.ai/new",
    "https://chat.deepseek.com/",
    "https://chat.z.ai/",
    "https://chat.qwen.ai/",
    "https://agent.minimax.io/"
]
cmd = f'"{chrome_path}" --user-data-dir="{profile_dir}" {" ".join(urls)}'

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
print(f"CreateProcessW Result: {res} | PID: {pi.dwProcessId} | Error: {err}")
