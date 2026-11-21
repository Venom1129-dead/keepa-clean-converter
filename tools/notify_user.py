import sys
import subprocess
import os

def notify_user(title, message):
    """
    Delivers a high-volume, crystal-clear audio announcement + on-screen visual dialog.
    - SAPI Volume: 100 (Maximum)
    - Voice: Microsoft Zira (Clear high-treble enunciation)
    - Rate: -1 (Crisp, deliberate pace)
    - Chime: Double alert tone
    - Visual: Top-most Windows alert popup
    """
    ps_script = f"""
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing

    # Play loud attention alert chime
    try {{
        [System.Console]::Beep(900, 150)
        [System.Console]::Beep(1300, 300)
    }} catch {{}}

    # Clear High-Volume Voice Announcement
    try {{
        $voice = New-Object -ComObject SAPI.SpVoice
        $voice.Volume = 100
        $voice.Rate = -1
        $voices = $voice.GetVoices()
        for ($i=0; $i -lt $voices.Count; $i++) {{
            if ($voices.Item($i).GetDescription() -match "Zira") {{
                $voice.Voice = $voices.Item($i)
                break
            }}
        }}
        $voice.Speak("{message}")
    }} catch {{}}

    # Top-most Visual Popup on Screen
    try {{
        [System.Windows.Forms.MessageBox]::Show("{message}", "{title}", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)
    }} catch {{}}
    """
    try:
        subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script], check=True)
        print(f"[NOTIFIED] Title: {title} | Message: {message}")
    except Exception as e:
        print(f"[NOTIFICATION ERROR] {e}")

if __name__ == "__main__":
    title = sys.argv[1] if len(sys.argv) > 1 else "Autonomous AI Income Milestone"
    msg = sys.argv[2] if len(sys.argv) > 2 else "All multi-agent deliverables verified and complete."
    notify_user(title, msg)
