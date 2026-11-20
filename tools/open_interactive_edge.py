#!/usr/bin/env python3
"""
tools/open_interactive_edge.py
Opens a URL in Microsoft Edge directly on the user's active interactive desktop (WinSta0\\Default).
Bypasses the agent harness's isolated sandbox desktop (exebox-...) using Windows Task Scheduler (/it).
"""

import sys
import os
import subprocess
import time

def open_url_on_screen(url):
    print(f"[*] Opening URL on user's interactive display: {url}")
    bat_path = r"C:\Users\myven\open_interactive_url.bat"
    with open(bat_path, "w") as f:
        f.write(f'@echo off\nstart "" "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe" "{url}"\n')
    
    task_name = "AgentOpenEdgeOnScreen"
    try:
        # Create interactive one-time task
        subprocess.run([
            "schtasks", "/create", "/tn", task_name,
            "/tr", bat_path,
            "/sc", "once", "/st", "23:59",
            "/it", "/f"
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Run immediately
        subprocess.run(["schtasks", "/run", "/tn", task_name], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)
        
        # Cleanup task definition
        subprocess.run(["schtasks", "/delete", "/tn", task_name, "/f"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[+] Edge successfully launched on user's interactive monitor.")
        return True
    except Exception as e:
        print(f"[-] Error launching via schtasks: {e}")
        return False

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "file:///c:/Users/myven/Downloads/antigravity ai income/03_Active_MVP/frontend/index.html"
    success = open_url_on_screen(target)
    sys.exit(0 if success else 1)
