#!/usr/bin/env python3
"""Cloud Fleet Worker: stdlib-only claim/execute/commit runner for the repo-hosted JSON task queue.

Reads cloud_queue/allowlist.json and cloud_queue/tasks/*.json, claims the oldest
pending task by committing status=running BEFORE executing, runs the allowlisted
argv verbatim with subprocess.run(list, shell=False), writes a capped result JSON,
then commits the result and the terminal task status. All git operations use
explicit paths under cloud_queue/ only. No secrets, no shell, no free-form commands.
"""
import glob
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE_DIR = os.path.join(ROOT, "cloud_queue")
ALLOWLIST_PATH = os.path.join(QUEUE_DIR, "allowlist.json")
TASKS_DIR = os.path.join(QUEUE_DIR, "tasks")
RESULTS_DIR = os.path.join(QUEUE_DIR, "results")
LEASE_MINUTES = 20
OUTPUT_CAP = 20000
GIT_NAME = "CloudFleetAgent[bot]"
GIT_EMAIL = "cloud-agent@users.noreply.github.com"
VALID_ROLES = ("worker", "reviewer", "coordinator")


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(value):
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def load_json(path, label):
    """Load JSON, failing loud on any malformed input (no state change)."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError) as exc:
        raise SystemExit("FATAL: malformed %s %s: %s" % (label, path, exc))


def save_json_atomic(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")
    os.replace(tmp, path)


def validate_allowlist(allowlist):
    if not isinstance(allowlist, dict) or allowlist.get("schema_version") != 1:
        raise SystemExit("FATAL: allowlist schema_version must be 1")
    entries = allowlist.get("entries")
    if not isinstance(entries, dict) or not entries:
        raise SystemExit("FATAL: allowlist entries must be a non-empty object")
    for cid, entry in entries.items():
        if not isinstance(entry, dict):
            raise SystemExit("FATAL: allowlist entry %s not an object" % cid)
        if entry.get("role") not in ("worker", "reviewer"):
            raise SystemExit("FATAL: allowlist entry %s bad role" % cid)
        argv = entry.get("argv")
        if not isinstance(argv, list) or not argv or not all(isinstance(a, str) for a in argv):
            raise SystemExit("FATAL: allowlist entry %s bad argv" % cid)
        if not isinstance(entry.get("timeout_seconds"), int) or entry["timeout_seconds"] <= 0:
            raise SystemExit("FATAL: allowlist entry %s bad timeout" % cid)
        if entry.get("cwd") != ".":
            raise SystemExit("FATAL: allowlist entry %s bad cwd" % cid)
        expected = entry.get("expected_exit_codes")
        if not isinstance(expected, list) or not all(isinstance(c, int) for c in expected):
            raise SystemExit("FATAL: allowlist entry %s bad expected_exit_codes" % cid)
    return entries


def validate_task(task, path):
    if not isinstance(task, dict) or task.get("schema_version") != 1:
        raise SystemExit("FATAL: task %s bad schema_version" % path)
    tid = task.get("id")
    base = os.path.basename(path)[:-5]
    if not isinstance(tid, str) or tid != base or not (3 <= len(tid) <= 64):
        raise SystemExit("FATAL: task %s id/filename mismatch" % path)
    if task.get("role") not in VALID_ROLES:
        raise SystemExit("FATAL: task %s bad role" % path)
    if not isinstance(task.get("command_id"), str):
        raise SystemExit("FATAL: task %s bad command_id" % path)
    if task.get("status") not in ("pending", "running", "done", "failed"):
        raise SystemExit("FATAL: task %s bad status" % path)
    if not isinstance(task.get("history"), list):
        raise SystemExit("FATAL: task %s bad history" % path)
    if not isinstance(task.get("attempts"), int):
        raise SystemExit("FATAL: task %s bad attempts" % path)


def load_tasks():
    tasks = []
    for path in sorted(glob.glob(os.path.join(TASKS_DIR, "*.json"))):
        task = load_json(path, "task")
        validate_task(task, path)
        tasks.append((path, task))
    return tasks


def append_history(task, event, by):
    hist = task.setdefault("history", [])
    hist.append({"at": now_iso(), "event": event, "by": by})
    del hist[:-500]


def run_git(args, check=True):
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=check)


def set_git_identity():
    run_git(["git", "config", "user.name", GIT_NAME])
    run_git(["git", "config", "user.email", GIT_EMAIL])


def commit_and_push(paths, message):
    """Explicit-path add, commit, rebase, push. Return True on success."""
    set_git_identity()
    run_git(["git", "add", "--"] + paths)
    commit = run_git(["git", "commit", "-m", message], check=False)
    if commit.returncode != 0 and "nothing to commit" not in (commit.stdout + commit.stderr):
        print("GIT_COMMIT_FAIL: " + commit.stderr.strip(), file=sys.stderr)
        return False
    pull = run_git(["git", "pull", "--rebase", "origin", "main"], check=False)
    if pull.returncode != 0:
        print("GIT_PULL_FAIL: " + pull.stderr.strip(), file=sys.stderr)
        return False
    push = run_git(["git", "push", "origin", "HEAD:main"], check=False)
    if push.returncode != 0:
        print("GIT_PUSH_FAIL: " + push.stderr.strip(), file=sys.stderr)
        return False
    return True


def rel(path):
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def reclaim_stale(tasks, run_id):
    """Reset running tasks whose lease >20 min to pending; commit+push that change."""
    changed = []
    threshold = datetime.now(timezone.utc) - timedelta(minutes=LEASE_MINUTES)
    for path, task in tasks:
        if task.get("status") != "running":
            continue
        claimed = task.get("claimed_at")
        if not claimed:
            continue
        try:
            if parse_iso(claimed) > threshold:
                continue
        except (ValueError, TypeError):
            continue
        task["status"] = "pending"
        task["claimed_at"] = None
        task["claimed_by"] = None
        task["attempts"] = task.get("attempts", 0) + 1
        task["updated_at"] = now_iso()
        append_history(task, "stale-lease-reclaim", run_id)
        save_json_atomic(path, task)
        changed.append(rel(path))
    if changed:
        if not commit_and_push(changed, "queue: reclaim stale leases"):
            raise SystemExit("FATAL: failed to push stale-lease reclaim")


def main():
    run_id = os.environ.get("GITHUB_RUN_ID", "local")
    if not os.environ.get("GITHUB_TOKEN"):
        print("FATAL: GITHUB_TOKEN not set", file=sys.stderr)
        sys.exit(1)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    allowlist = load_json(ALLOWLIST_PATH, "allowlist")
    entries = validate_allowlist(allowlist)
    tasks = load_tasks()

    reclaim_stale(tasks, run_id)

    pending = [(p, t) for p, t in tasks if t.get("status") == "pending"]
    if not pending:
        print("NO_PENDING_TASKS")
        return 0
    pending.sort(key=lambda pt: pt[1].get("created_at", ""))
    task_path, task = pending[0]
    task_id = task["id"]

    cmd_id = task["command_id"]
    if cmd_id not in entries:
        print("REJECTED unknown command_id: %s" % cmd_id, file=sys.stderr)
        return 0
    entry = entries[cmd_id]
    if entry["role"] != task["role"] or task["role"] == "coordinator":
        print("REJECTED role mismatch for %s" % task_id, file=sys.stderr)
        return 0

    ts = now_iso()
    task["status"] = "running"
    task["claimed_at"] = ts
    task["claimed_by"] = run_id
    task["updated_at"] = ts
    append_history(task, "claimed", run_id)
    save_json_atomic(task_path, task)

    if not commit_and_push([rel(task_path)], "queue: claim %s" % task_id):
        print("CLAIM_LOST %s" % task_id)
        return 0

    started_at = now_iso()
    start_dt = datetime.now(timezone.utc)
    try:
        proc = subprocess.run(
            entry["argv"],
            cwd=os.path.join(ROOT, entry["cwd"]),
            capture_output=True,
            text=True,
            timeout=entry["timeout_seconds"],
            shell=False,
        )
        exit_code = proc.returncode
        stdout, stderr = proc.stdout or "", proc.stderr or ""
    except subprocess.TimeoutExpired as exc:
        exit_code = 124
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = "TIMEOUT after %ss" % entry["timeout_seconds"]
    except OSError as exc:
        exit_code = 127
        stdout, stderr = "", "EXEC_ERROR %s" % exc

    finished_at = now_iso()
    duration_ms = int((datetime.now(timezone.utc) - start_dt).total_seconds() * 1000)
    terminal = "done" if exit_code == 0 else "failed"
    out_trunc = len(stdout) > OUTPUT_CAP
    err_trunc = len(stderr) > OUTPUT_CAP
    commit_sha = run_git(["git", "rev-parse", "HEAD"], check=False).stdout.strip()

    result = {
        "schema_version": 1,
        "task_id": task_id,
        "role": task["role"],
        "command_id": cmd_id,
        "argv": list(entry["argv"]),
        "status": terminal,
        "exit_code": exit_code,
        "stdout": stdout[:OUTPUT_CAP],
        "stderr": stderr[:OUTPUT_CAP],
        "stdout_truncated": out_trunc,
        "stderr_truncated": err_trunc,
        "started_at": started_at,
        "finished_at": finished_at,
        "duration_ms": duration_ms,
        "github_run_id": str(run_id),
        "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT", "1"),
        "commit_sha": commit_sha,
    }
    result_path = os.path.join(RESULTS_DIR, task_id + ".json")
    save_json_atomic(result_path, result)

    task["status"] = terminal
    task["finished_at"] = finished_at
    task["updated_at"] = finished_at
    task["result_path"] = "cloud_queue/results/%s.json" % task_id
    task["attempts"] = task.get("attempts", 0) + 1
    append_history(task, terminal, run_id)
    save_json_atomic(task_path, task)

    rel_task = rel(task_path)
    rel_result = rel(result_path)
    ok = False
    for _ in range(2):
        if commit_and_push([rel_task, rel_result], "queue: result %s %s" % (task_id, terminal)):
            ok = True
            break
    if not ok:
        print("FATAL: could not commit result for %s" % task_id, file=sys.stderr)
        return 1

    print("TASK_%s %s %d" % (terminal.upper(), task_id, exit_code))
    return 0


if __name__ == "__main__":
    sys.exit(main())
