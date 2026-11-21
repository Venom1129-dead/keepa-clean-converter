$logFile = "$env:USERPROFILE\Downloads\antigravity ai income\00_Brain\proofs\tab_cleanup_log.txt"
"`nExecuting Precise Tab Cleanup at $(Get-Date)" | Out-File $logFile -Append

Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes

$root = [System.Windows.Automation.AutomationElement]::RootElement
$condition = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ClassNameProperty, "Chrome_WidgetWin_1")
$windows = $root.FindAll([System.Windows.Automation.TreeScope]::Children, $condition)

foreach ($win in $windows) {
    if ($win.Current.Name -like "*Microsoft?Edge*" -or $win.Current.Name -like "*Edge*") {
        "Target Edge Window found: '$($win.Current.Name)'" | Out-File $logFile -Append
        
        $tabCond = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ControlTypeProperty, [System.Windows.Automation.ControlType]::TabItem)
        $tabs = $win.FindAll([System.Windows.Automation.TreeScope]::Descendants, $tabCond)
        
        # Track how many audit tabs we see so we keep only the last/active one
        $auditTabCount = 0
        foreach ($t in $tabs) {
            if ($t.Current.Name -like "*Data Integrity Audit*") {
                $auditTabCount++
            }
        }
        
        $seenAuditCount = 0
        foreach ($tab in $tabs) {
            $name = $tab.Current.Name
            $shouldClose = $false
            
            # Rule 1: Never close user's personal Google Doc
            if ($name -like "*AI income - Google Docs*") {
                "  PRESERVE: User document '$name'" | Out-File $logFile -Append
                continue
            }
            
            # Rule 2: Close Device Activation
            if ($name -like "*Device Activation*") {
                $shouldClose = $true
                "  CLOSE TARGET: Finished authentication tab '$name'" | Out-File $logFile -Append
            }
            # Rule 3: Close stale Keepa Converter test tabs
            elseif ($name -like "*Keepa Clean Excel Converter*") {
                $shouldClose = $true
                "  CLOSE TARGET: Unneeded Keepa tab '$name'" | Out-File $logFile -Append
            }
            # Rule 4: Close old duplicate Audit tabs, keeping the most recent one
            elseif ($name -like "*Data Integrity Audit*") {
                $seenAuditCount++
                if ($seenAuditCount -lt $auditTabCount) {
                    $shouldClose = $true
                    "  CLOSE TARGET: Stale comparison tab ($seenAuditCount of $auditTabCount) '$name'" | Out-File $logFile -Append
                } else {
                    "  PRESERVE: Active audit viewer on screen '$name'" | Out-File $logFile -Append
                }
            }
            
            if ($shouldClose) {
                # Find Close tab button
                $btnCond = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ControlTypeProperty, [System.Windows.Automation.ControlType]::Button)
                $buttons = $tab.FindAll([System.Windows.Automation.TreeScope]::Children, $btnCond)
                $closed = $false
                foreach ($btn in $buttons) {
                    if ($btn.Current.Name -eq "Close tab" -or $btn.Current.Name -like "*Close*") {
                        try {
                            $pattern = $btn.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
                            $pattern.Invoke()
                            "    -> Successfully invoked Close tab button on '$name'" | Out-File $logFile -Append
                            $closed = $true
                            Start-Sleep -Milliseconds 400
                            break
                        } catch {
                            "    -> Failed invoking Close tab: $_" | Out-File $logFile -Append
                        }
                    }
                }
                if (-not $closed) {
                    "    -> Could not find 'Close tab' button on '$name'" | Out-File $logFile -Append
                }
            }
        }
    }
}
