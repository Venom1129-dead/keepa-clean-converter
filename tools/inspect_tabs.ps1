$logFile = "$env:USERPROFILE\Downloads\antigravity ai income\00_Brain\proofs\tab_cleanup_log.txt"
"Starting Tab Inspection at $(Get-Date)" | Out-File $logFile

Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes

$root = [System.Windows.Automation.AutomationElement]::RootElement
$condition = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ClassNameProperty, "Chrome_WidgetWin_1")
$windows = $root.FindAll([System.Windows.Automation.TreeScope]::Children, $condition)

"Found $($windows.Count) Chrome_WidgetWin_1 windows" | Out-File $logFile -Append

foreach ($win in $windows) {
    "Window: '$($win.Current.Name)' (ProcessId: $($win.Current.ProcessId))" | Out-File $logFile -Append
    
    # Find TabItems
    $tabCond = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ControlTypeProperty, [System.Windows.Automation.ControlType]::TabItem)
    $tabs = $win.FindAll([System.Windows.Automation.TreeScope]::Descendants, $tabCond)
    "  Found $($tabs.Count) TabItems" | Out-File $logFile -Append
    
    foreach ($tab in $tabs) {
        "    Tab: '$($tab.Current.Name)'" | Out-File $logFile -Append
        
        # Check if tab has a Close button
        # In Edge/Chrome, the close button is often named "Close tab" or a child Button
        $btnCond = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ControlTypeProperty, [System.Windows.Automation.ControlType]::Button)
        $buttons = $tab.FindAll([System.Windows.Automation.TreeScope]::Children, $btnCond)
        foreach ($btn in $buttons) {
            "      Button: '$($btn.Current.Name)'" | Out-File $logFile -Append
        }
    }
}
