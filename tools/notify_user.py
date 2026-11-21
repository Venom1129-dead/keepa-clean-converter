import sys
import subprocess
import os

def notify_user(title, message):
    ps_script = f"""
    Add-Type -AssemblyName System.Windows.Forms
    [System.Media.SystemSounds]::Asterisk.Play()
    try {{
        $voice = New-Object -ComObject SAPI.SpVoice
        $voice.Rate = 1
        $voice.Speak("{message}")
    }} catch {{}}
    """
    try:
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], check=True)
        print(f"[NOTIFIED] Title: {title} | Message: {message}")
    except Exception as e:
        print(f"[NOTIFICATION ERROR] {e}")

if __name__ == "__main__":
    title = sys.argv[1] if len(sys.argv) > 1 else "Autonomous AI Income Milestone"
    msg = sys.argv[2] if len(sys.argv) > 2 else "All multi-agent deliverables verified and complete."
    notify_user(title, msg)
