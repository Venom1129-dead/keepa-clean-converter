<#
.SYNOPSIS
  tools/voice_mic_guard.ps1
  Local 100% Offline Wake-Word & Hardware Mic Controller for Antigravity Voice.
  Triggers:
    - "Antigravity Listen Up"  -> Unmutes Windows Master Microphone
    - "Antigravity Mute Down"  -> Mutes Windows Master Microphone
    - "Antigravity Mode Down"  -> Mutes Windows Master Microphone
    - Fallbacks: "Listen Antigravity", "Close Antigravity Mic"
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
Write-Host "Active Voice Triggers:"
Write-Host "  [+] 'Antigravity Listen Up'  -> UNMUTE Mic (Wake Up)" -ForegroundColor Green
Write-Host "  [-] 'Antigravity Mute Down'  -> MUTE Mic (Sleep)" -ForegroundColor Red
Write-Host "  [-] 'Antigravity Mode Down'  -> MUTE Mic (Sleep)" -ForegroundColor Red
Write-Host "=========================================================="

try {
    $engine = New-Object System.Speech.Recognition.SpeechRecognitionEngine
    
    # Exact triggers configured per user specifications
    $choices = New-Object System.Speech.Recognition.Choices
    $choices.Add("antigravity listen up")
    $choices.Add("antigravity listen")
    $choices.Add("listen antigravity")
    $choices.Add("antigravity mute down")
    $choices.Add("antigravity mode down")
    $choices.Add("close antigravity mic")
    
    $builder = New-Object System.Speech.Recognition.GrammarBuilder
    $builder.Append($choices)
    
    $grammar = New-Object System.Speech.Recognition.Grammar($builder)
    $engine.LoadGrammar($grammar)
    $engine.SetInputToDefaultAudioDevice()

    Register-ObjectEvent -InputObject $engine -EventName SpeechRecognized -Action {
        $phrase = $Event.SourceEventArgs.Result.Text.ToLower()
        $confidence = [Math]::Round($Event.SourceEventArgs.Result.Confidence, 2)
        Write-Host "[$([DateTime]::Now.ToString('HH:mm:ss'))] Recognized: '$phrase' (Confidence: $confidence)" -ForegroundColor Yellow
        
        # Mute / Sleep Commands
        if ($phrase -eq "antigravity mute down" -or $phrase -eq "antigravity mode down" -or $phrase -eq "close antigravity mic") {
            [NativeAudio]::ToggleMic()
            Write-Host "  -> [MUTED] Microphone stream paused. Background noise blocked." -ForegroundColor Red
        }
        # Unmute / Wake-Up Commands
        elseif ($phrase -eq "antigravity listen up" -or $phrase -eq "antigravity listen" -or $phrase -eq "listen antigravity") {
            [NativeAudio]::ToggleMic()
            Write-Host "  -> [UNMUTED] Microphone active. Antigravity listening..." -ForegroundColor Green
        }
    } | Out-Null

    $engine.RecognizeAsync([System.Speech.Recognition.RecognizeMode]::Multiple)
    Write-Host "[+] Local Wake-Word Engine is ACTIVE. Listening in background..." -ForegroundColor Green
    
    # Keep session active
    while ($true) {
        Start-Sleep -Seconds 3600
    }
} catch {
    Write-Host "[-] Error starting speech recognizer: $_" -ForegroundColor Red
}
