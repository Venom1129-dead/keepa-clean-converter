Add-Type @"
using System;
using System.Runtime.InteropServices;

public class DesktopLauncher {
    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
    public struct STARTUPINFO {
        public Int32 cb;
        public string lpReserved;
        public string lpDesktop;
        public string lpTitle;
        public Int32 dwX;
        public Int32 dwY;
        public Int32 dwXSize;
        public Int32 dwYSize;
        public Int32 dwXCountChars;
        public Int32 dwYCountChars;
        public Int32 dwFillAttribute;
        public Int32 dwFlags;
        public Int16 wShowWindow;
        public Int16 cbReserved2;
        public IntPtr lpReserved2;
        public IntPtr hStdInput;
        public IntPtr hStdOutput;
        public IntPtr hStdError;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct PROCESS_INFORMATION {
        public IntPtr hProcess;
        public IntPtr hThread;
        public Int32 dwProcessId;
        public Int32 dwThreadId;
    }

    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
    public static extern bool CreateProcess(
        string lpApplicationName,
        string lpCommandLine,
        IntPtr lpProcessAttributes,
        IntPtr lpThreadAttributes,
        bool bInheritHandles,
        uint dwCreationFlags,
        IntPtr lpEnvironment,
        string lpCurrentDirectory,
        ref STARTUPINFO lpStartupInfo,
        out PROCESS_INFORMATION lpProcessInformation
    );
}
"@

$chrome = "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
$profile = "$env:LOCALAPPDATA\AIIncome_Dedicated_Browser"
$urls = @(
    "https://gumroad.com/settings/payouts",
    "https://gumroad.com/products/new",
    "https://www.paypal.com/signin",
    "https://kdp.amazon.com/",
    "https://printify.com/app/dashboard",
    "https://gemini.google.com/app",
    "https://chatgpt.com/",
    "https://claude.ai/new",
    "https://chat.deepseek.com/",
    "https://chat.z.ai/",
    "https://chat.qwen.ai/",
    "https://agent.minimax.io/"
)
$urlStr = ($urls -join " ")
$cmd = "`"$chrome`" --user-data-dir=`"$profile`" $urlStr"

$si = New-Object DesktopLauncher+STARTUPINFO
$si.cb = [System.Runtime.InteropServices.Marshal]::SizeOf($si)
$si.lpDesktop = "WinSta0\default"
$pi = New-Object DesktopLauncher+PROCESS_INFORMATION

$res = [DesktopLauncher]::CreateProcess($chrome, $cmd, [IntPtr]::Zero, [IntPtr]::Zero, $false, 0, [IntPtr]::Zero, $null, [ref]$si, [ref]$pi)
$err = [System.Runtime.InteropServices.Marshal]::GetLastWin32Error()

Write-Host "CreateProcess Success: $res | ProcessId: $($pi.dwProcessId) | Win32Error: $err"
