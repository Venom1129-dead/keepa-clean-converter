#!/usr/bin/env python3
"""
Automated Edge Remote Debugging Fixer & Verifier
Uses isolated debug profile to bypass Windows Edge Startup Boost conflict.
Guarantees port 9222 is active, loads URL, and captures screenshot proof.
"""

import sys
import os
import time
import json
import base64
import urllib.request
import urllib.parse
import subprocess

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 9222
DEBUG_PROFILE = os.path.join(os.path.expanduser("~"), ".edge-debug-profile")
PROOF_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "00_Brain", "proofs")
os.makedirs(DEBUG_PROFILE, exist_ok=True)
os.makedirs(PROOF_DIR, exist_ok=True)

def is_port_listening():
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=1) as resp:
            return resp.status == 200
    except Exception:
        return False

def ensure_edge():
    if is_port_listening():
        print(f"[+] Edge CDP is ALREADY listening on port {PORT}.")
        return True

    print(f"[*] Starting Edge with isolated debug profile on port {PORT}...")
    DETACHED_PROCESS = 0x00000008
    CREATE_NEW_PROCESS_GROUP = 0x00000200

    subprocess.Popen([
        EDGE_PATH,
        f"--remote-debugging-port={PORT}",
        "--remote-allow-origins=*",
        f"--user-data-dir={DEBUG_PROFILE}",
        "--no-first-run",
        "--no-default-browser-check",
        "about:blank"
    ], creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)

    for i in range(15):
        time.sleep(1)
        if is_port_listening():
            print(f"[+] Edge CDP successfully listening on port {PORT} (Attempt {i+1})!")
            return True
        print(f"[*] Waiting for port {PORT}... ({i+1}/15)")

    return False

def open_url_and_capture_proof(url):
    print(f"[*] Opening URL in Edge: {url}")
    try:
        # Create new tab with URL
        encoded = urllib.parse.quote(url, safe=':/?&=#._')
        put_url = f"http://127.0.0.1:{PORT}/json/new?{encoded}"
        req = urllib.request.Request(put_url, method='PUT')
        with urllib.request.urlopen(req, timeout=5) as resp:
            tab = json.loads(resp.read().decode())
        
        tab_id = tab['id']
        ws_url = tab.get('webSocketDebuggerUrl')
        print(f"[+] Tab created successfully:")
        print(f"    - ID:    {tab_id}")
        print(f"    - Title: {tab.get('title')}")
        print(f"    - URL:   {tab.get('url')}")

        # Allow 3 seconds for DOM to render
        print("[*] Waiting for DOM render...")
        time.sleep(3)

        # Connect WebSocket to verify and capture screenshot
        if not ws_url:
            print("[-] No webSocketDebuggerUrl found.")
            return None

        import websocket
        ws = websocket.create_connection(ws_url, timeout=10)
        
        # 1. Query document title from DOM
        ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate", "params": {"expression": "document.title"}}))
        title_res = json.loads(ws.recv())
        doc_title = title_res.get('result', {}).get('result', {}).get('value', 'Unknown')
        print(f"[+] Verified Document Title via DOM: '{doc_title}'")

        # 2. Capture Screenshot
        ws.send(json.dumps({"id": 2, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
        screen_res = json.loads(ws.recv())
        ws.close()

        img_b64 = screen_res.get('result', {}).get('data')
        if not img_b64:
            print("[-] No image data returned in captureScreenshot.")
            return None

        timestamp = int(time.time())
        proof_path = os.path.join(PROOF_DIR, f"edge_render_proof_{timestamp}.png")
        with open(proof_path, "wb") as f:
            f.write(base64.b64decode(img_b64))

        file_size = os.path.getsize(proof_path)
        print(f"[+] REAL SCREENSHOT PROOF CAPTURED & SAVED:")
        print(f"    - File: {proof_path}")
        print(f"    - Size: {file_size:,} bytes")
        return proof_path

    except Exception as e:
        print(f"[-] Error controlling Edge via CDP: {e}")
        return None

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "file:///c:/Users/myven/Downloads/antigravity ai income/03_Active_MVP/frontend/index.html"
    
    if not ensure_edge():
        print("[-] Loop failed: Could not bind Edge to port 9222.")
        sys.exit(1)

    proof = open_url_and_capture_proof(target)
    if proof and os.path.exists(proof) and os.path.getsize(proof) > 1000:
        print("\n=== VERIFICATION COMPLETE: EDGE IS RUNNING, RENDERING, AND CAPTURED WITH PROOF ===")
        sys.exit(0)
    else:
        print("\n[-] Verification failed: Could not capture screenshot proof.")
        sys.exit(1)
