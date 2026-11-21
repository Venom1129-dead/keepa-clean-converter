$w = New-Object -ComObject WScript.Shell
Get-ChildItem "$env:USERPROFILE\Desktop\*.lnk" | ForEach-Object {
    $s = $w.CreateShortcut($_.FullName)
    Write-Host "$($_.Name) => $($s.TargetPath) $($s.Arguments)"
}
