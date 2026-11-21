Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName Microsoft.VisualBasic

$prompt = "Read HANDOFF.md and continue as Chief Coordinator under AGENTS.md. Gumroad payment method is active. Guide me through publishing the first products."

# 1. Put prompt into Windows clipboard
Set-Clipboard -Value $prompt
Write-Host "[+] Clipboard loaded with master resume prompt."

# 2. Activate Antigravity Window
$wshell = New-Object -ComObject WScript.Shell
$activated = $wshell.AppActivate("Antigravity")
if (-not $activated) {
    $activated = $wshell.AppActivate("Google Antigravity")
}
Write-Host "[*] Window activation result: $activated"

Start-Sleep -Milliseconds 400

# 3. Send Ctrl+Shift+L (antigravity.startNewConversation registered keybinding)
[System.Windows.Forms.SendKeys]::SendWait("^+l")
Start-Sleep -Milliseconds 600

# 4. Paste the prompt via Ctrl+V
[System.Windows.Forms.SendKeys]::SendWait("^v")
Start-Sleep -Milliseconds 400

# 5. Submit via Enter
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
Write-Host "[SUCCESS] Sent New Conversation keystroke and submitted prompt."
