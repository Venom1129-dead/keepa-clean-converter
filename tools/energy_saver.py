import ctypes
import os
import subprocess
import sys
import json
from ctypes import wintypes

psapi = ctypes.WinDLL('psapi', use_last_error=True)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

PROCESS_SET_QUOTA = 0x0100
PROCESS_QUERY_INFORMATION = 0x0400
IDLE_PRIORITY_CLASS = 0x00000040
BELOW_NORMAL_PRIORITY_CLASS = 0x00004000

def get_process_pids(image_name):
    """Finds PIDs for a given process image name."""
    pids = []
    try:
        out = subprocess.check_output(
            ["tasklist", "/fi", f"imagename eq {image_name}", "/fo", "csv"],
            text=True,
            stderr=subprocess.DEVNULL
        )
        for line in out.strip().splitlines()[1:]:
            parts = line.split(",")
            if len(parts) >= 2:
                pid_str = parts[1].strip('"')
                try:
                    pids.append(int(pid_str))
                except ValueError:
                    pass
    except Exception:
        pass
    return pids

def optimize_process_memory_and_priority(pid, priority_class=BELOW_NORMAL_PRIORITY_CLASS):
    """Purges unused working set pages and lowers CPU scheduling priority."""
    h_proc = kernel32.OpenProcess(PROCESS_SET_QUOTA | PROCESS_QUERY_INFORMATION | 0x0200, False, pid)
    if not h_proc:
        return False
    try:
        # Set CPU priority to BelowNormal so it never starves Windows desktop
        kernel32.SetPriorityClass(h_proc, priority_class)
        # Flush working set (reclaim RAM back to Windows)
        psapi.EmptyWorkingSet(h_proc)
        return True
    finally:
        kernel32.CloseHandle(h_proc)

def run_energy_saver():
    print("=== AUTONOMOUS PC ENERGY & RESOURCE SAVER ROUTINE ===")
    reclaimed_pids = 0

    # 1. Optimize Chrome dedicated browser processes
    chrome_pids = get_process_pids("chrome.exe")
    print(f"[*] Found {len(chrome_pids)} Chrome processes. Purging idle RAM and lowering CPU priority...")
    for pid in chrome_pids:
        if optimize_process_memory_and_priority(pid):
            reclaimed_pids += 1

    # 2. Optimize background Edge processes
    edge_pids = get_process_pids("msedge.exe")
    print(f"[*] Found {len(edge_pids)} Edge processes. Purging idle RAM and lowering CPU priority...")
    for pid in edge_pids:
        if optimize_process_memory_and_priority(pid):
            reclaimed_pids += 1

    # 3. Dismiss any restore bubbles
    workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dismiss_script = os.path.join(workspace_dir, "tools", "dismiss_restore_popup.py")
    if os.path.exists(dismiss_script):
        try:
            subprocess.run([sys.executable, dismiss_script], capture_output=True)
        except Exception:
            pass

    # 4. Check battery and memory status
    print("\n[*] Measuring System Power & Reclaimed State:")
    try:
        cmd = """
        $os = Get-CimInstance Win32_OperatingSystem
        $freeRamMB = [math]::Round($os.FreePhysicalMemory / 1024, 2)
        $totalRamMB = [math]::Round($os.TotalVisibleMemorySize / 1024, 2)
        $usedRamMB = $totalRamMB - $freeRamMB
        $pct = [math]::Round(($usedRamMB / $totalRamMB) * 100, 1)

        $battery = Get-CimInstance Win32_Battery -ErrorAction SilentlyContinue
        $pwr = if ($battery) { "Battery $($battery.EstimatedChargeRemaining)%" } else { "AC Power" }

        Write-Output "RAM: Used ${usedRamMB}MB / ${totalRamMB}MB (${pct}%) | Free: ${freeRamMB}MB | Power: $pwr"
        """
        res = subprocess.check_output(["powershell", "-NoProfile", "-Command", cmd], text=True)
        print(f"    {res.strip()}")
    except Exception as e:
        print(f"    Memory check note: {e}")

    print(f"[+] Successfully optimized {reclaimed_pids} browser processes to prevent PC freezing.")
    print("=== ENERGY SAVER RUN COMPLETE ===")
    return True

if __name__ == "__main__":
    run_energy_saver()
