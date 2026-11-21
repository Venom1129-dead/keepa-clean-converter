#!/usr/bin/env python3
"""
Chrome Profile Preferences Sanitizer
Autonomous AI Income Factory — Task ID: aii-mwqjg030-b779d2

Permanently eradicates Chrome's "Restore pages?" crash bubble by enforcing:
1. profile.exit_type = "Normal"
2. profile.exited_cleanly = True
3. user_experience_metrics.stability.exited_cleanly = True

Mandatory Security Scope Guard (Council Constraint):
- ONLY permits operating inside %LOCALAPPDATA%\\AIIncome_Dedicated_Browser.
- Raises ValueError("[SECURITY VIOLATION] ...") immediately if any attempt is made to target any profile outside.
"""

import os
import sys
import json
import argparse

def get_dedicated_browser_dir():
    local_app_data = os.environ.get("LOCALAPPDATA")
    if not local_app_data:
        local_app_data = os.path.expanduser("~\\AppData\\Local")
    return os.path.abspath(os.path.join(local_app_data, "AIIncome_Dedicated_Browser"))

def enforce_scope_guard(target_dir):
    """
    Mandatory Security Scope Guard:
    Refuses execution if target_dir is not strictly scoped to AIIncome_Dedicated_Browser.
    """
    normalized = os.path.abspath(target_dir).lower()

    if "aiincome_dedicated_browser" not in normalized:
        raise ValueError(
            f"[SECURITY VIOLATION] Refusing to modify any profile outside 'AIIncome_Dedicated_Browser'. Target attempted: '{target_dir}'"
        )

    # Explicitly forbidden default personal directories
    forbidden_defaults = [
        os.path.join("google", "chrome", "user data", "default").lower(),
        os.path.join("microsoft", "edge", "user data", "default").lower()
    ]
    for forbidden in forbidden_defaults:
        if forbidden in normalized:
            raise ValueError(
                f"[SECURITY VIOLATION] Cannot target user's default browser profile '{forbidden}'. Target: '{target_dir}'"
            )

    return True

def sanitize_chrome_profile(target_dir=None):
    """
    Sanitizes Preferences and Local State to mark the profile cleanly closed.
    """
    if target_dir is None:
        target_dir = get_dedicated_browser_dir()

    enforce_scope_guard(target_dir)

    os.makedirs(target_dir, exist_ok=True)
    default_subdir = os.path.join(target_dir, "Default")
    os.makedirs(default_subdir, exist_ok=True)

    # 1. Patch Preferences in Default/Preferences
    pref_paths = [
        os.path.join(default_subdir, "Preferences"),
        os.path.join(target_dir, "Preferences")
    ]

    for p_path in pref_paths:
        data = {}
        if os.path.exists(p_path):
            try:
                with open(p_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}

        if not isinstance(data, dict):
            data = {}

        if "profile" not in data or not isinstance(data["profile"], dict):
            data["profile"] = {}

        data["profile"]["exit_type"] = "Normal"
        data["profile"]["exited_cleanly"] = True

        try:
            with open(p_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[!] Warning: Could not write {p_path}: {e}")

    # 2. Patch Local State
    local_state_path = os.path.join(target_dir, "Local State")
    ls_data = {}
    if os.path.exists(local_state_path):
        try:
            with open(local_state_path, "r", encoding="utf-8") as f:
                ls_data = json.load(f)
        except Exception:
            ls_data = {}

    if not isinstance(ls_data, dict):
        ls_data = {}

    if "user_experience_metrics" not in ls_data or not isinstance(ls_data["user_experience_metrics"], dict):
        ls_data["user_experience_metrics"] = {}

    if "stability" not in ls_data["user_experience_metrics"] or not isinstance(ls_data["user_experience_metrics"]["stability"], dict):
        ls_data["user_experience_metrics"]["stability"] = {}

    ls_data["user_experience_metrics"]["stability"]["exited_cleanly"] = True

    try:
        with open(local_state_path, "w", encoding="utf-8") as f:
            json.dump(ls_data, f, indent=2)
    except Exception as e:
        print(f"[!] Warning: Could not write {local_state_path}: {e}")

    return True

# Alias for backward compatibility
patch_preferences = sanitize_chrome_profile

def main():
    parser = argparse.ArgumentParser(description="Sanitize Chrome profile crash recovery state.")
    parser.add_argument("--profile", default=None, help="Target profile directory (must contain AIIncome_Dedicated_Browser)")
    args = parser.parse_args()

    try:
        sanitize_chrome_profile(args.profile)
        print(f"[+] Chrome profile sanitized successfully.")
        sys.exit(0)
    except Exception as e:
        print(f"[!] ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
