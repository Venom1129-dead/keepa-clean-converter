#!/usr/bin/env python3
"""
Edge Browser Controller & Verifier with Screenshot Proof
Uses Chrome DevTools Protocol (CDP) on port 9222.
"""

import sys
import os
import json
import time
import base64
import urllib.request
import subprocess

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 9222
PROOF_DIR = os.path.join(os.path.dirname(__file__), "..", "00_Brain", "proofs")
os.makedirs(PROOF_DIR, exist_ok=True)

def is_port_open():
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=1) as resp:
            return resp.status == 200
    except Exception:
        return False

def ensure_edge():
    if is_port_open():
        return True
    print(f"[*] Starting Edge with remote debugging on port {PORT}...")
    subprocess.Popen([
        EDGE_PATH,
        f"--remote-debugging-port={PORT}",
        "--remote-allow-origins=*",
        "--no-first-run",
        "--no-default-browser-check"
    ])
    for _ in range(15):
        time.sleep(1)
        if is_port_open():
            print("[+] Edge connected on port 9222!")
            return True
    return False

def main():
    target_url = sys.argv[1] if len(sys.argv) > 1 else "about:blank"
    if not ensure_edge():
        print(f"[-] Could not establish CDP connection to Edge on port {PORT}.")
        sys.exit(1)

    # Query active tabs or create a new tab
    try:
        # Create or navigate tab
        encoded_url = urllib.parse.quote(target_url, safe=':/?&=#._')
        put_url = f"http://127.0.0.1:{PORT}/json/new?{encoded_url}"
        req = urllib.request.Request(put_url, method='PUT')
        with urllib.request.urlopen(req, timeout=5) as resp:
            tab = json.loads(resp.read().decode())
        
        tab_id = tab.get('id')
        print(f"[+] Opened tab in Edge:")
        print(f"    - Title: {tab.get('title')}")
        print(f"    - URL:   {tab.get('url')}")
        print(f"    - ID:    {tab_id}")

        # Wait 2 seconds for render
        time.sleep(2)

        # Connect WebSocket to capture screenshot proof
        ws_url = tab.get('webSocketDebuggerUrl')
        if ws_url:
            try:
                import websocket
                ws = websocket.create_connection(ws_url, timeout=5)
                # Send Page.captureScreenshot
                cmd = json.dumps({"id": 1, "method": "Page.captureScreenshot", "params": {"format": "png"}})
                ws.send(cmd)
                res = json.loads(ws.recv())
                img_data = res.get('result', {}).get('data')
                if img_data:
                    proof_file = os.path.join(PROOF_DIR, f"edge_proof_{int(time.time())}.png")
                    with open(proof_file, "wb") as f:
                        f.write(base64.b64decode(img_data))
                    print(f"[+] SCREENSHOT PROOF CAPTURED:")
                    print(f"    {proof_file}")
                ws.close()
            except ImportError:
                print("[i] websocket-client not installed for CDP screenshot capture. Run: pip install websocket-client")
            except Exception as e:
                print(f"[!] Screenshot capture error: {e}")

    except Exception as e:
        print(f"[-] Error controlling Edge: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
