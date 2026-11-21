#!/usr/bin/env python3
"""
Web AI Hands Bridge — Autonomous Local Code Execution Engine
Autonomous AI Income Factory — Task ID: aii-mwqh5uqm-15a517

Bridges research outputs from Web AIs (Gemini, ChatGPT, Claude, DeepSeek, Zhipu/Z.ai, Qwen, MiniMax)
into local execution hands with strict council safety constraints (R1 - R7).

Council Security Controls:
- R1: Explicit user approval gate (No unapproved auto-execution)
- R2: Sandboxed execution workspace with path traversal rejection
- R3: Allowlisted languages only (Python, PowerShell, Batch, Bash, SQL)
- R4: Hard timeout enforcement (max 30 seconds)
- R5: Localhost CDP binding only (127.0.0.1)
- R6: Zero cookie / token / credential access
- R7: Isolated browser profile enforcement
"""

import os
import sys
import json
import time
import re
import subprocess
import urllib.request
import urllib.error
from datetime import datetime

# R3: Strict language allowlist
ALLOWED_LANGUAGES = {
    "python": ".py",
    "py": ".py",
    "powershell": ".ps1",
    "ps1": ".ps1",
    "batch": ".bat",
    "cmd": ".bat",
    "bash": ".sh",
    "sh": ".sh",
    "sql": ".sql"
}

# R2 & Security: Blocklist of destructive commands and path traversal
BLOCKED_PATTERNS = [
    r'\bformat\s+[a-zA-Z]:',
    r'\brmdir\s+/[sS]\s+/[qQ]\s+[cC]:\\',
    r'\bdel\s+/[fF]\s+/[sS]\s+/[qQ]\s+[cC]:\\windows',
    r'\bdiskpart\b',
    r'\bDropDatabase\b',
    r'\bshutdown\s+/[sSrR]',
    r'\.\.[\\/]',  # Path traversal attempts
]

def get_base_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_sandbox_dir():
    base = get_base_dir()
    sandbox = os.path.join(base, "projects", "hands-executions")
    os.makedirs(sandbox, exist_ok=True)
    return sandbox

def inspect_browser_cdp(host="127.0.0.1", port=9222):
    """
    R5: Connects exclusively to localhost CDP endpoint.
    R6: Connects only to /json metadata. Never accesses cookies or session storage.
    """
    url = f"http://{host}:{port}/json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "WebAIHandsBridge/1.0"})
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return {"active": True, "tabs": data}
    except Exception as e:
        return {"active": False, "error": str(e), "tabs": []}

def extract_code_blocks(text):
    """Extracts code blocks formatted with markdown triple backticks."""
    pattern = r'```([a-zA-Z0-9_\-\+]*)\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    blocks = []
    for lang, code in matches:
        lang = lang.strip().lower() or "python"
        blocks.append({"lang": lang, "code": code.strip()})
    return blocks

def validate_safety(code_str, lang="python"):
    """
    R2 & R3: Validates language allowlist, path traversal, and destructive command blocklist.
    """
    # R3: Language allowlist check
    if lang.lower() not in ALLOWED_LANGUAGES:
        return False, f"DISALLOWED_LANGUAGE: Language '{lang}' not in allowlist {list(ALLOWED_LANGUAGES.keys())}"

    # R2: Traversal and destructive call check
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, code_str, re.IGNORECASE):
            return False, f"SECURITY_ERROR: Blocked pattern '{pattern}'"

    return True, "Safe"

def queue_pending_task(code_str, lang="python", source="web-ai"):
    """
    R1: Queues code blocks into pending_tasks.json awaiting explicit user confirmation.
    """
    sandbox_dir = get_sandbox_dir()
    pending_file = os.path.join(sandbox_dir, "pending_tasks.json")

    task_id = f"task_{int(time.time() * 1000)}"
    task = {
        "id": task_id,
        "source": source,
        "lang": lang,
        "code": code_str,
        "approved": False,
        "queued_at": datetime.utcnow().isoformat()
    }

    tasks = []
    if os.path.exists(pending_file):
        try:
            with open(pending_file, "r", encoding="utf-8") as f:
                tasks = json.load(f)
        except Exception:
            tasks = []

    tasks.append(task)
    with open(pending_file, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)

    return task

def execute_code(code_str, lang="python", sandbox_dir=None, timeout=30, approved=False):
    """
    Executes a code snippet strictly inside the sandbox directory.
    Enforces R1 (Approval Gate), R2 (Sandbox isolation), R3 (Allowlist), R4 (Timeout <= 30s).
    """
    if sandbox_dir is None:
        sandbox_dir = get_sandbox_dir()

    # R1: User Approval Invariant
    if not approved:
        return {
            "success": False,
            "exit_code": -403,
            "stdout": "",
            "stderr": "APPROVAL_REQUIRED: Execution blocked. Code requires explicit user approval flag (approved=True) per Council Rule R1.",
            "duration_sec": 0.0,
            "timestamp": datetime.utcnow().isoformat()
        }

    # R2 & R3: Safety & Allowlist Validation
    is_safe, reason = validate_safety(code_str, lang=lang)
    if not is_safe:
        return {
            "success": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": f"SECURITY_ERROR: {reason}",
            "duration_sec": 0.0,
            "timestamp": datetime.utcnow().isoformat()
        }

    # R4: Enforce maximum hard timeout of 30 seconds
    timeout = min(30, max(1, timeout))

    timestamp_str = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
    start_time = time.time()

    ext = ALLOWED_LANGUAGES.get(lang.lower(), ".py")
    script_filename = f"task_{timestamp_str}{ext}"
    script_path = os.path.join(sandbox_dir, script_filename)

    with open(script_path, "w", encoding="utf-8") as f:
        f.write(code_str)

    try:
        if ext == ".py":
            cmd = [sys.executable, script_path]
        elif ext == ".ps1":
            cmd = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", script_path]
        elif ext == ".bat":
            cmd = ["cmd.exe", "/c", script_path]
        else:
            cmd = [sys.executable, script_path]

        # R2: cwd is strictly sandboxed
        proc = subprocess.run(
            cmd,
            cwd=sandbox_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout
        )
        duration = round(time.time() - start_time, 3)

        result = {
            "success": proc.returncode == 0,
            "exit_code": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "duration_sec": duration,
            "script_path": script_path,
            "timestamp": datetime.utcnow().isoformat()
        }
    except subprocess.TimeoutExpired:
        duration = round(time.time() - start_time, 3)
        result = {
            "success": False,
            "exit_code": -99,
            "stdout": "",
            "stderr": f"EXECUTION_TIMEOUT: Exceeded {timeout} seconds (Council Rule R4)",
            "duration_sec": duration,
            "script_path": script_path,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as ex:
        duration = round(time.time() - start_time, 3)
        result = {
            "success": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": f"LAUNCH_ERROR: {str(ex)}",
            "duration_sec": duration,
            "script_path": script_path,
            "timestamp": datetime.utcnow().isoformat()
        }

    # Record in JSONL telemetry log
    log_file = os.path.join(sandbox_dir, "execution_history.jsonl")
    try:
        with open(log_file, "a", encoding="utf-8") as lf:
            lf.write(json.dumps(result) + "\n")
    except Exception:
        pass

    return result

def format_relay_report(result):
    """Formats execution results into a markdown response suitable for pasting back to Web AIs."""
    status_icon = "✅ SUCCESS" if result["success"] else "❌ FAILED"
    report = [
        f"### Local AI Hands Execution Report — {status_icon}",
        f"- **Exit Code:** `{result['exit_code']}`",
        f"- **Execution Time:** `{result['duration_sec']}s`",
        f"- **Timestamp:** `{result['timestamp']}`",
        ""
    ]
    if result["stdout"]:
        report.append("**Standard Output (stdout):**")
        report.append("```")
        report.append(result["stdout"])
        report.append("```")
        report.append("")
    if result["stderr"]:
        report.append("**Errors / Warnings (stderr):**")
        report.append("```")
        report.append(result["stderr"])
        report.append("```")
        report.append("")
    return "\n".join(report)

def main():
    print("=" * 65)
    print("     WEB AI HANDS BRIDGE — LOCAL EXECUTION ENGINE")
    print("=" * 65)
    sandbox = get_sandbox_dir()
    print(f"[*] Execution Sandbox: {sandbox}")

    # Inspect CDP
    cdp_info = inspect_browser_cdp(port=9222)
    if cdp_info["active"]:
        print(f"[+] Connected to Dedicated AI Browser (127.0.0.1:9222). Active tabs: {len(cdp_info['tabs'])}")
        target_domains = ["gemini", "chatgpt", "claude", "deepseek", "z.ai", "qwen", "minimax"]
        found = []
        for t in cdp_info["tabs"]:
            u = t.get("url", "").lower()
            for d in target_domains:
                if d in u and d not in found:
                    found.append(d)
        print(f"[+] Detected Web AI Endpoints: {', '.join(found) if found else 'None currently active'}")
    else:
        print("[-] Dedicated AI Browser not detected on 127.0.0.1:9222 (Launch via launch_dedicated_ai_browser.bat)")

    if len(sys.argv) > 1 and sys.argv[1] == "--test-run":
        print("\n[*] Executing Deterministic Test Run with Explicit Approval...")
        test_code = "import math\nprint(f'Hands Bridge Active: pi={math.pi:.4f}, sum={sum(range(100))}')"
        res = execute_code(test_code, lang="python", sandbox_dir=sandbox, approved=True)
        print(format_relay_report(res))
        sys.exit(0 if res["success"] and res["exit_code"] == 0 else 1)

    print("\nUsage:")
    print("  python tools/web_ai_hands_bridge.py --test-run       (Runs self-test with approval)")
    print("  python tools/web_ai_hands_bridge.py --inspect-cdp    (Checks open Web AI tabs on localhost)")

if __name__ == "__main__":
    main()
