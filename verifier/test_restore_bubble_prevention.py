import json
import os
import sys

def get_workspace_root():
    """Dynamically finds the workspace root by looking for tools directory."""
    d = os.path.dirname(os.path.abspath(__file__))
    while d and os.path.dirname(d) != d:
        if os.path.exists(os.path.join(d, "tools")):
            return d
        d = os.path.dirname(d)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def test_launcher_scripts():
    """Verify anti-bubble flags exist in launcher batch files."""
    workspace_dir = get_workspace_root()
    bat_path = os.path.join(workspace_dir, "tools", "launch_dedicated_ai_browser.bat")
    desktop_bat = os.path.expandvars(r"%USERPROFILE%\Desktop\Launch_Dedicated_AI_Browser.bat")

    required_flags = [
        "--disable-session-crashed-bubble",
        "--hide-crash-restore-bubble",
        "--noerrdialogs",
        "patch_chrome_preferences.py"
    ]

    for p in [bat_path, desktop_bat]:
        assert os.path.exists(p), f"Launcher batch file missing: {p}"
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        for flag in required_flags:
            assert flag in content, f"Required flag/command '{flag}' missing in {p}"
    print("[PASS] Test 1: All launcher batch files contain mandatory anti-bubble flags & pre-sanitization.")

def test_scope_guard():
    """Verify patch_chrome_preferences.py enforces strict council scope-guard."""
    workspace_dir = get_workspace_root()
    sys.path.insert(0, os.path.join(workspace_dir, "tools"))
    from patch_chrome_preferences import sanitize_chrome_profile, get_dedicated_browser_dir

    # Must raise ValueError when illegal directory outside AIIncome_Dedicated_Browser is passed
    illegal_dir = os.path.abspath(r"C:\Users\Public\BadProfile")
    raised = False
    try:
        sanitize_chrome_profile(target_dir=illegal_dir)
    except ValueError as e:
        raised = True
        assert "[SECURITY VIOLATION]" in str(e)

    assert raised, "Security violation: sanitize_chrome_profile did not block unauthorized profile path!"
    print("[PASS] Test 2: Council Scope-Guard successfully blocked unauthorized directory modification.")

def test_preferences_sanitization():
    """Verify sanitize_chrome_profile writes exit_type=Normal and exited_cleanly=true."""
    workspace_dir = get_workspace_root()
    sys.path.insert(0, os.path.join(workspace_dir, "tools"))
    from patch_chrome_preferences import sanitize_chrome_profile, get_dedicated_browser_dir

    dedicated_dir = get_dedicated_browser_dir()
    res = sanitize_chrome_profile()
    assert res is True, "sanitize_chrome_profile did not return True"

    # Check Preferences
    pref_path = os.path.join(dedicated_dir, "Default", "Preferences")
    assert os.path.exists(pref_path), f"Preferences file missing at {pref_path}"
    with open(pref_path, "r", encoding="utf-8") as f:
        prefs = json.load(f)
    assert prefs.get("profile", {}).get("exit_type") == "Normal", "profile.exit_type is not 'Normal'"
    assert prefs.get("profile", {}).get("exited_cleanly") is True, "profile.exited_cleanly is not True"

    # Check Local State
    local_state_path = os.path.join(dedicated_dir, "Local State")
    assert os.path.exists(local_state_path), f"Local State missing at {local_state_path}"
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = json.load(f)
    assert local_state.get("user_experience_metrics", {}).get("stability", {}).get("exited_cleanly") is True, (
        "user_experience_metrics.stability.exited_cleanly is not True"
    )
    print("[PASS] Test 3: Dedicated profile Preferences & Local State verified cleanly sanitized.")

def test_dismiss_script_filters():
    """Verify dismiss_restore_popup.py filters strictly by Chrome PID and title."""
    workspace_dir = get_workspace_root()
    dismiss_path = os.path.join(workspace_dir, "tools", "dismiss_restore_popup.py")
    assert os.path.exists(dismiss_path), f"Missing dismiss script: {dismiss_path}"
    with open(dismiss_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "get_chrome_pids()" in content, "Missing Chrome PID filter in dismiss script"
    assert "Restore pages" in content, "Missing Restore pages title filter in dismiss script"
    assert "WM_CLOSE" in content, "Missing WM_CLOSE signal in dismiss script"
    print("[PASS] Test 4: Restore bubble dismiss script verified with strict Council filter guards.")

def main():
    print("=== Running Restore Bubble Prevention Verifier ===")
    test_launcher_scripts()
    test_scope_guard()
    test_preferences_sanitization()
    test_dismiss_script_filters()
    print("\n[VERIFIED COMPLETE] All 4 tests passed. Exit Code 0.")
    sys.exit(0)

if __name__ == "__main__":
    main()
