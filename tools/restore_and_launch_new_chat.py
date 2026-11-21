import ctypes
import os
import subprocess
import time
from ctypes import wintypes

user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

SW_RESTORE = 9
SW_SHOW = 5
SW_SHOWMAXIMIZED = 3

VK_SHIFT = 0x10
VK_CONTROL = 0x11
VK_MENU = 0x12 # Alt
VK_L = 0x4C
VK_V = 0x56
VK_RETURN = 0x0D
KEYEVENTF_KEYUP = 0x0002

def press_key_combination(keys):
    """Sends keydown for all keys, then keyup in reverse order."""
    for k in keys:
        user32.keybd_event(k, 0, 0, 0)
        time.sleep(0.05)
    time.sleep(0.1)
    for k in reversed(keys):
        user32.keybd_event(k, 0, KEYEVENTF_KEYUP, 0)
        time.sleep(0.05)

def main():
    print("=== EXECUTING PHYSICAL DESKTOP NEW CHAT LAUNCHER ===")
    hDesk = user32.OpenDesktopW("Default", 0, False, 0x01FF)
    if not hDesk:
        print("[!] Failed to open Default desktop.")
        return False

    res_desk = user32.SetThreadDesktop(hDesk)
    print(f"[*] SetThreadDesktop to Default: {res_desk}")

    # Set prompt to clipboard via powershell
    prompt_text = "Read HANDOFF.md and continue as Chief Coordinator under AGENTS.md. Gumroad payment method is active. Guide me through publishing the first products."
    subprocess.run(["powershell", "-NoProfile", "-Command", f"Set-Clipboard -Value @'\n{prompt_text}\n'@"], check=True)
    print("[+] Master prompt copied to Windows clipboard.")

    # Find the Antigravity window
    hwnd = 132726
    # Restore and bring to foreground
    user32.ShowWindow(hwnd, SW_RESTORE)
    user32.ShowWindow(hwnd, SW_SHOWMAXIMIZED)
    user32.SetForegroundWindow(hwnd)
    user32.BringWindowToTop(hwnd)
    time.sleep(0.8)

    rect = (ctypes.c_long * 4)()
    user32.GetWindowRect(hwnd, rect)
    print(f"[+] Antigravity window restored to foreground. Rect: {rect[:]}")

    # Step 1: Send Ctrl + Shift + L (antigravity.startNewConversation)
    print("[*] Sending Ctrl + Shift + L (New Conversation)...")
    press_key_combination([VK_CONTROL, VK_SHIFT, VK_L])
    time.sleep(1.0)

    # Step 2: Send Ctrl + V (Paste prompt)
    print("[*] Sending Ctrl + V (Paste prompt)...")
    press_key_combination([VK_CONTROL, VK_V])
    time.sleep(0.5)

    # Step 3: Send Enter (Submit)
    print("[*] Sending Enter (Submit)...")
    press_key_combination([VK_RETURN])
    time.sleep(0.5)

    print("[SUCCESS] New chat initiated on the physical screen with prompt submitted!")
    return True

if __name__ == "__main__":
    main()
