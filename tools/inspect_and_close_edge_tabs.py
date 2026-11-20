import sys
import os
import time

log_file = r"C:\Users\myven\Downloads\antigravity ai income\00_Brain\proofs\tab_cleanup_log.txt"

def log(msg):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%X')}] {msg}\n")
    print(msg)

try:
    import uiautomation as auto
    log("uiautomation imported successfully.")
except ImportError:
    log("uiautomation not installed. Trying ctypes or UIAutomationClient...")
    auto = None

if auto:
    edge_window = auto.WindowControl(searchDepth=1, ClassName="Chrome_WidgetWin_1")
    if edge_window.Exists(maxSearchSeconds=3):
        log(f"Found Edge Window: '{edge_window.Name}'")
        tabs = edge_window.GetChildren()
        log(f"Root child count: {len(tabs)}")
    else:
        log("No Edge window found via uiautomation.")
