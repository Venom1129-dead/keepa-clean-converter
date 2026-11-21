import sqlite3
import json
import os

userprofile = os.environ.get("USERPROFILE") or os.path.expandvars(r"%USERPROFILE%")
appdata = os.environ.get("APPDATA") or os.path.expandvars(r"%APPDATA%")

db_path = os.path.join(userprofile, ".gemini", "antigravity", "conversation_summaries.db")
storage_path = os.path.join(appdata, "Antigravity", "app_storage.json")

target_project_id = "95da692f-9cfa-4e50-b740-3a7f0c2ab8cc"
workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Normalize file URI
target_workspace = json.dumps([f"file:///{workspace_dir.replace(os.sep, '/')}"])
convo_id = "4a1fb3a7-40ff-4262-818e-2d1d613341b9"

# 1. Update conversation_summaries.db
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE conversation_summaries SET project_id = ?, workspace_uris = ? WHERE conversation_id = ?",
        (target_project_id, target_workspace, convo_id)
    )
    conn.commit()
    print(f"Updated rows in conversation_summaries: {cursor.rowcount}")

    cursor.execute(
        "SELECT conversation_id, project_id, workspace_uris, title FROM conversation_summaries WHERE conversation_id = ?",
        (convo_id,)
    )
    print("Verified in DB:", cursor.fetchone())
    conn.close()

# 2. Update app_storage.json
if os.path.exists(storage_path):
    with open(storage_path, "r", encoding="utf-8") as f:
        storage = json.load(f)

    storage["new-convo-last-selected-project"] = target_project_id
    storage["new-convo-magic-workspace-selected"] = True
    storage["lastCreatedProjectId"] = target_project_id

    with open(storage_path, "w", encoding="utf-8") as f:
        json.dump(storage, f, indent=2)

    print(f"[+] app_storage.json locked default project to '{target_project_id}' (antigravity ai income).")
