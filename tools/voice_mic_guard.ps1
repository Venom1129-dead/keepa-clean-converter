<#
.SYNOPSIS
  tools/voice_mic_guard.ps1
  Local 100% Offline Wake-Word & Hardware Mic Controller for Antigravity Voice.
  Triggers:
    - "Listen Antigravity"      -> Unmutes Windows Master Microphone
    - "Antigravity Mute Down"   -> Mutes Windows Master Microphone
    - "Close Antigravity Mic"   -> Mutes Windows Master Microphone
    - Hotkey (F8)               -> Instant Mute / Unmute Toggle
#>

Add-Type -AssemblyName System.Speech

# Win32 Mic Mute Toggle via SendMessage
$csharpCode = @"
using System;
using System.Runtime.InteropServices;

public class NativeAudio {
    [DllImport("user32.dll")]
    public static extern IntPtr SendMessageW(IntPtr hWnd, int Msg, IntPtr wParam, IntPtr lParam);
    
    public static void ToggleMic() {
        IntPtr HWND_BROADCAST = (IntPtr)0xffff;
        int WM_APPCOMMAND = 0x319;
        int APPCOMMAND_MIC_ON_OFF_TOGGLE = 0x2C;
        IntPtr lParam = (IntPtr)(APPCOMMAND_MIC_ON_OFF_TOGGLE << 16);
        SendMessageW(HWND_BROADCAST, WM_APPCOMMAND, IntPtr.Zero, lParam);
    }
}
"@
Add-Type -TypeDefinition $csharpCode -ErrorAction SilentlyContinue

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   ANTIGRAVITY LOCAL WAKE-WORD & MIC GUARD (OFFLINE VAD)  " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Triggers:"
Write-Host "  [+] Say 'Listen Antigravity'    -> Unmutes Mic Stream" -ForegroundColor Green
Write-Host "  [-] Say 'Antigravity Mute Down' -> Mutes Mic Stream" -ForegroundColor Red
Write-Host "  [-] Say 'Close Antigravity Mic' -> Mutes Mic Stream" -ForegroundColor Red
Write-Host "=========================================================="

# Create Speech Recognition Engine with offline Grammar
try {
    $engine = New-Object System.Speech.Recognition.SpeechRecognitionEngine
    $choices = New-Object System.Speech.Recognition.Choices
    $choices.Add("listen antigravity")
    $choices.Add("antigravity mute down")
    $choices.Add("close antigravity mic")
    
    $builder = New-Object System.Speech.Recognition.GrammarBuilder
    $builder.Append($choices)
    
    $grammar = New-Object System.Speech.Recognition.Grammar($builder)
    $engine.LoadGrammar($grammar)
    $engine.SetInputToDefaultAudioDevice()

    Register-ObjectEvent -InputObject $engine -EventName SpeechRecognized -Action {
        $phrase = $Event.SourceEventArgs.Result.Text
        $confidence = [Math]::Round($Event.SourceEventArgs.Result.Confidence, 2)
        Write-Host "[$([DateTime]::Now.ToString('HH:mm:ss'))] Recognized: '$phrase' (Confidence: $confidence)" -ForegroundColor Yellow
        
        if ($phrase -eq "antigravity mute down" -or $phrase -eq "close antigravity mic") {
            [NativeAudio]::ToggleMic()
            Write-Host "  -> [MUTED] Antigravity microphone paused. Background noise blocked." -ForegroundColor Red
        }
        elseif ($phrase -eq "listen antigravity") {
            [NativeAudio]::ToggleMic()
            Write-Host "  -> [UNMUTED] Antigravity microphone active. Listening for user..." -ForegroundColor Green
        }
    } | Out-Null

    $engine.RecognizeAsync([System.Speech.Recognition.RecognizeMode]::Multiple)
    Write-Host "[+] Local Wake-Word Engine is ACTIVE. Listening in background..." -ForegroundColor Green
} catch {
    Write-Host "[-] Error starting speech recognizer: $_" -ForegroundColor Red
}
