# QUEUE_SPEC — Cloud Fleet Task Queue

Version 1. Repo-hosted JSON task queue drained by a GitHub Actions runner
(`cloud_queue/worker.py`). Tasks are command_ids resolved through a strict
allowlist — never free-form prompts or shell strings. No LLM keys, no secrets,
no task-supplied environment variables, no `shell=True`.

## Layout on `main`

```
cloud_queue/
  QUEUE_SPEC.md              # this spec, human-readable
  allowlist.json             # versioned command allowlist
  worker.py                  # stdlib-only claim/execute/commit worker
  tasks/<task_id>.json       # one task per file, status stored in-file
  results/<task_id>.json     # one result per processed task
  results/.gitkeep           # directory anchor
.github/workflows/cloud_fleet_worker.yml   # NEW, web UI only
```

## Identity and IDs

- `task_id`: `^[a-z0-9][a-z0-9-]{2,63}$`, lowercase kebab-case; filename is `<task_id>.json`.
- Timestamps: ISO-8601 UTC with `Z` suffix (e.g. `2026-11-24T18:42:00Z`).
- `schema_version`: integer, currently `1`. Unknown versions are rejected (fail loud).

## Task file schema (`cloud_queue/tasks/<task_id>.json`)

```json
{
  "schema_version": 1,
  "id": "selftest-0001",
  "role": "reviewer",
  "command_id": "reviewer.verify_converter",
  "status": "pending",
  "result_path": "cloud_queue/results/selftest-0001.json",
  "requested_by": "local-orchestrator",
  "note": "E2E smoke test: deterministic read-only verifier",
  "created_at": "2026-11-24T18:40:00Z",
  "updated_at": "2026-11-24T18:40:00Z",
  "claimed_at": null,
  "claimed_by": null,
  "finished_at": null,
  "attempts": 0,
  "history": [
    {"at": "2026-11-24T18:40:00Z", "event": "created", "by": "local-orchestrator"}
  ]
}
```

Rules:
- `role` ∈ `worker` | `reviewer` | `coordinator`. `coordinator` is reserved for built-in claim/serialization logic (no coordinator command entries accepted in v1).
- `command_id` must exist in the allowlist **and** its entry's `role` must equal the task's `role`.
- `note` and `requested_by` are descriptive only — never interpolated into a command, env var, or path.
- `history` is append-only, capped at 500 entries; true attempt count kept in `attempts`.
- Invalid/malformed JSON → fail loud, no state change, no commit.
- Saves are atomic (write temp + `os.replace`).

## Allowlist schema (`cloud_queue/allowlist.json`)

Three entries, verbatim:

```json
{
  "schema_version": 1,
  "entries": {
    "reviewer.verify_converter": {
      "role": "reviewer",
      "argv": ["python", "03_Active_MVP/verifier/test_converter.py"],
      "cwd": ".",
      "timeout_seconds": 120,
      "writes": [],
      "expected_exit_codes": [0]
    },
    "reviewer.verify_merch_intel": {
      "role": "reviewer",
      "argv": ["python", "01_Research/verifier/test_community_merch_intel.py"],
      "cwd": ".",
      "timeout_seconds": 120,
      "writes": [],
      "expected_exit_codes": [0]
    },
    "worker.generate_mvp18_svgs": {
      "role": "worker",
      "argv": ["python", "tools/generate_mvp18_svgs.py"],
      "cwd": ".",
      "timeout_seconds": 300,
      "writes": ["03_Active_MVP_18/svg/*.svg"],
      "expected_exit_codes": [0]
    }
  }
}
```

Rules:
- `argv` is a literal JSON array of strings; entries are chosen from scripts already on `main`.
- No shell, no glob expansion by worker, no `sh -c`, no user-supplied arguments.
- `writes` is documentation + review guard only; generator entry not enabled in E2E.
- Adding an entry requires a reviewed Contents API commit; tasks can never add entries.

## Result file schema (`cloud_queue/results/<task_id>.json`)

```json
{
  "schema_version": 1,
  "task_id": "selftest-0001",
  "role": "reviewer",
  "command_id": "reviewer.verify_converter",
  "argv": ["python", "03_Active_MVP/verifier/test_converter.py"],
  "status": "done",
  "exit_code": 0,
  "stdout": "=== RUNNING VERIFIER SANITY CHECKS === ... ALL SANITY TESTS PASSED",
  "stderr": "",
  "stdout_truncated": false,
  "stderr_truncated": false,
  "started_at": "2026-11-24T18:42:10Z",
  "finished_at": "2026-11-24T18:42:11Z",
  "duration_ms": 340,
  "github_run_id": "12345678",
  "github_run_attempt": "1",
  "commit_sha": "<sha at execution time>"
}
```

Rules: stdout/stderr capped at 20,000 chars each with `*_truncated` flag; status mirrors task's terminal status; atomic write; committed with task update in one commit.

## State machine and claim/commit protocol

```
pending --claim(commit status=running)--> running --exit 0--> done
                                             \--exit !=0--> failed
running --claimed_at older than 20 min--> pending (attempts++, history note)
```

1. Runner checks out `main`; worker resolves repo root from `__file__`.
2. Load + validate allowlist and all task files; fail loud on any malformed input.
3. If no `pending` task: print `NO_PENDING_TASKS`, exit 0, no commit.
4. Reclaim any `running` task whose `claimed_at` exceeds `lease_minutes` (default 20): reset to `pending`, increment `attempts`, append history, then commit+push that change.
5. Select oldest `pending` by `created_at` (FIFO). Set `status=running`, `claimed_at`, `claimed_by=$GITHUB_RUN_ID`, append history; commit only that task file; `git pull --rebase origin main`; `git push origin HEAD:main`. On push failure print `CLAIM_LOST` and exit 0 without executing.
6. Execute: `subprocess.run(argv, cwd=root, capture_output=True, text=True, timeout=entry.timeout_seconds, shell=False)` using the allowlist vector verbatim. No task field enters argv, cwd, or env.
7. Write result file; update task to `done`/`failed` with `finished_at`, `result_path`, `attempts`, history.
8. `git add -- cloud_queue/tasks/<id>.json cloud_queue/results/<id>.json`; commit `queue: result <id> <status>`; `git pull --rebase origin main`; push. Retry once on push failure; fail loud if still failing.
9. Print `TASK_DONE <id> <exit_code>` / `TASK_FAILED <id> <exit_code>`; exit 0 after processed task.

Git identity is set inside the worker before each commit. Only `cloud_queue/**` paths ever added. GITHUB_TOKEN pushes do not re-trigger workflows.

## Roles

- `worker` — executes allowlisted generator commands that may write declared outputs.
- `reviewer` — executes allowlisted read-only verifiers/checkers; v1 E2E uses this role.
- `coordinator` — not a command role; implemented by concurrency group + claim-by-commit + lease reclaim. `coordinator` tasks rejected in v1.

## Workflow contract (web-UI-created file)

- Name: `Cloud Fleet Worker`; `on.schedule`: `2,12,22,32,42,52 * * * *`; `on.workflow_dispatch`; `permissions.contents: write`.
- `concurrency: {group: cloud-fleet-queue, cancel-in-progress: false}`; `timeout-minutes: 10`; `runs-on: ubuntu-latest`.
- Steps: `actions/checkout@v4` → `actions/setup-python@v5` (3.11) → `python cloud_queue/worker.py`. Worker owns all git commits/pushes.
- Never references `01_Research/**`, `.github/workflows/**`, final-product dirs, or secrets.
