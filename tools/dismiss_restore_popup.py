#!/usr/bin/env python3
"""
Chrome Crash Restore Bubble Desktop Window Dismissal Guard
Autonomous AI Income Factory — Task ID: aii-mwqjg030-b779d2

Strict Council Constraints Implemented:
1. Matches ONLY windows belonging to chrome.exe / msedge.exe processes.
2. Matches ONLY window titles containing "Restore pages" or "Restore".
3. Sends WM_CLOSE (0x0010) strictly to matched windows; never sends arbitrary keys/clicks.
4. Defaults to safe one-shot scan (--once).
"""

import sys
import os
import argparse
import ctypes
from ctypes import wintypes
import subprocess

WM_CLOSE = 0x0010
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

# Win32 Function Prototypes
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

def get_chrome_pids():
    """Returns a set of active process IDs for chrome.exe and msedge.exe."""
    pids = set()
    try:
        # Use tasklist for fast PID lookup
        cmd = ["tasklist", "/FO", "CSV", "/NH"]
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
        for line in out.splitlines():
            line = line.strip()
            if not line:
                continue
            parts = [p.strip('"') for p in line.split('","')]
            if len(parts) >= 2:
                pname = parts[0].lower()
                if pname in ("chrome.exe", "msedge.exe"):
                    try:
                        pids.add(int(parts[1]))
                    except ValueError:
                        pass
    except Exception:
        pass
    return pids

def get_process_name_by_pid(pid):
    """Retrieves process image base name safely via QueryFullProcessImageNameW."""
    h_process = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not h_process:
        return ""
    try:
        buf = ctypes.create_unicode_buffer(1024)
        size = wintypes.DWORD(1024)
        if kernel32.QueryFullProcessImageNameW(h_process, 0, buf, ctypes.byref(size)):
            full_path = buf.value
            return os.path.basename(full_path).lower()
        return ""
    finally:
        kernel32.CloseHandle(h_process)

def get_window_title(hwnd):
    """Retrieves window text safely."""
    length = user32.GetWindowTextLengthW(hwnd)
    if length == 0:
        return ""
    buf = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buf, length + 1)
    return buf.value

def is_target_restore_window(title, proc_name):
    """
    Strict Council Match Filter:
    Must match process = chrome.exe or msedge.exe AND title contains 'Restore pages' or 'Restore'.
    """
    valid_procs = ("chrome.exe", "msedge.exe")
    if proc_name not in valid_procs:
        return False

    title_lower = title.lower()
    if "restore pages" in title_lower or "restore session" in title_lower:
        return True

    return False

def dismiss_restore_bubbles():
    """
    Enumerates top-level windows on WinSta0\\Default and dismisses any active Chrome restore bubbles.
    """
    dismissed = []
    chrome_pids = get_chrome_pids()

    def enum_windows_callback(hwnd, lparam):
        if not user32.IsWindowVisible(hwnd):
            return True

        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        if pid.value == 0:
            return True

        # Check against Chrome/Edge PID list
        if chrome_pids and pid.value not in chrome_pids:
            return True

        proc_name = get_process_name_by_pid(pid.value)
        title = get_window_title(hwnd)

        if is_target_restore_window(title, proc_name):
            print(f"[*] Found Chrome Restore Bubble: HWND={hwnd}, Title='{title}', Process='{proc_name}' (PID={pid.value})")
            user32.PostMessageW(hwnd, WM_CLOSE, 0, 0)
            dismissed.append({"hwnd": hwnd, "title": title, "pid": pid.value})

        return True

    cb = WNDENUMPROC(enum_windows_callback)
    user32.EnumWindows(cb, 0)
    return dismissed

def main():
    parser = argparse.ArgumentParser(description="Safely dismiss Chrome 'Restore pages?' crash bubbles on desktop.")
    parser.add_argument("--once", action="store_true", default=True, help="Perform a single desktop scan (default: True)")
    args = parser.parse_args()

    print("=" * 65)
    print(" CHROME CRASH BUBBLE DISMISSAL GUARD — DESKTOP WINDOW AUDIT")
    print("=" * 65)

    dismissed = dismiss_restore_bubbles()
    if dismissed:
        print(f"[+] Successfully dismissed {len(dismissed)} active Chrome restore bubble(s).")
    else:
        print("[+] Desktop clean: Zero Chrome restore crash bubbles detected.")

    sys.exit(0)

if __name__ == "__main__":
    main()
