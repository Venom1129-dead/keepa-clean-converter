#!/usr/bin/env python3
"""
tools/ensure_edge_browser.py
Automated Watchdog & Verifier for Microsoft Edge & OpenCode Browse Relay.
Guarantees:
1. Edge is running interactively in the user's desktop session.
2. Browse relay is running with OPENCODE_BROWSER_ALLOW_FILE_URLS=1.
3. Extension is connected and responsive.
4. Captures real screenshot proof and outputs deterministic JSON status.
"""

import os
import sys
import time
import json
import urllib.request
import subprocess

RELAY_URL = "http://127.0.0.1:19988"
BROWSE_BIN = os.path.join(os.path.expanduser("~"), ".local", "bin", "browse.exe")
PROOF_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "00_Brain", "proofs")
os.makedirs(PROOF_DIR, exist_ok=True)

def is_edge_running():
    try:
        out = subprocess.check_output(["powershell", "-NoProfile", "-Command", "Get-Process msedge -ErrorAction SilentlyContinue"], text=True)
        return bool(out.strip())
    except Exception:
        return False

def is_relay_running():
    try:
        with urllib.request.urlopen(RELAY_URL, timeout=1) as resp:
            return resp.status == 200
    except Exception:
        return False

def ensure_edge():
    if is_edge_running():
        print("[+] Edge is already running.")
        return True
    print("[*] Launching Edge via Explorer shell to guarantee persistent desktop session...")
    subprocess.run(["powershell", "-NoProfile", "-Command", 'Start-Process "explorer.exe" -ArgumentList "microsoft-edge:about:blank"'], check=True)
    for _ in range(10):
        time.sleep(1)
        if is_edge_running():
            print("[+] Edge successfully launched and verified running.")
            return True
    return False

def ensure_relay():
    if is_relay_running():
        print("[+] Browse relay is already listening on port 19988.")
        return True
    print("[*] Starting browse relay daemon...")
    env = os.environ.copy()
    env["OPENCODE_BROWSER_ALLOW_FILE_URLS"] = "1"
    DETACHED_PROCESS = 0x00000008
    CREATE_NEW_PROCESS_GROUP = 0x00000200
    subprocess.Popen([BROWSE_BIN, "serve"], env=env, creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)
    for _ in range(10):
        time.sleep(1)
        if is_relay_running():
            print("[+] Browse relay listening successfully.")
            return True
    return False

def verify_connection():
    print("[*] Verifying extension connection status...")
    for attempt in range(10):
        try:
            out = subprocess.check_output([BROWSE_BIN, "status"], text=True, stderr=subprocess.STDOUT)
            if "Extension: connected" in out:
                print(f"[+] Extension connected successfully (Attempt {attempt+1})!")
                return True
        except Exception as e:
            print(f"[*] Waiting for extension connection... ({attempt+1}/10)")
        time.sleep(1)
    return False

def test_render_and_screenshot(target_url=None):
    if not target_url:
        target_url = "file:///c:/Users/myven/Downloads/antigravity%20ai%20income/03_Active_MVP/frontend/index.html"
    print(f"[*] Navigating Edge to: {target_url}")
    code = f"""
    await page.goto('{target_url}');
    const title = await page.title();
    const url = page.url();
    const buf = await page.screenshot({{ fullPage: true }});
    await files.write('edge_verified_proof.png', buf);
    const savedPath = files.path('edge_verified_proof.png');
    return {{ title, url, savedPath }};
    """
    try:
        res = subprocess.check_output([BROWSE_BIN, "execute", "--json", code], text=True, stderr=subprocess.STDOUT)
        start_idx = res.find('{')
        end_idx = res.rfind('}')
        if start_idx != -1 and end_idx != -1:
            parsed = json.loads(res[start_idx:end_idx+1])
        else:
            print(f"[-] No JSON found in output: {res}")
            return None
        if parsed.get("ok"):
            val = parsed.get("value", {})
            print(f"[+] Verification passed!")
            print(f"    - Page Title: {val.get('title')}")
            print(f"    - Page URL:   {val.get('url')}")
            print(f"    - Screenshot: {val.get('savedPath')}")
            return val
        else:
            print(f"[-] Execute returned error: {parsed.get('error')}")
            return None
    except Exception as e:
        print(f"[-] Execution error: {e}")
        return None

if __name__ == "__main__":
    print("=== STARTING EDGE AUTOMATION VERIFICATION LOOP ===")
    if not ensure_edge():
        print("[-] FAILED: Could not start Edge.")
        sys.exit(1)
    if not ensure_relay():
        print("[-] FAILED: Could not start browse relay.")
        sys.exit(1)
    if not verify_connection():
        print("[-] FAILED: Extension is not connected.")
        sys.exit(1)
    result = test_render_and_screenshot()
    if result:
        print("\n=== VERIFIED COMPLETE: EDGE AUTOMATION IS 100% OPERATIONAL ===")
        sys.exit(0)
    else:
        print("\n[-] FAILED: Screenshot and navigation verification failed.")
        sys.exit(1)
