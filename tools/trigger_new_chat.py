import subprocess
import os
import sys

desktop_bat = os.path.expandvars(r"%USERPROFILE%\Desktop\START_NEW_CHAT.bat")
task_name = "TriggerAntigravityNewChat"

create_cmd = [
    "schtasks", "/create",
    "/tn", task_name,
    "/tr", f'cmd.exe /c "{desktop_bat}"',
    "/sc", "ONCE",
    "/st", "23:59",
    "/f",
    "/it"
]
res1 = subprocess.run(create_cmd, capture_output=True, text=True)
print("schtasks /create:", res1.stdout.strip() or res1.stderr.strip())

run_cmd = ["schtasks", "/run", "/tn", task_name]
res2 = subprocess.run(run_cmd, capture_output=True, text=True)
print("schtasks /run:", res2.stdout.strip() or res2.stderr.strip())
