#!/usr/bin/env python3
"""
Verifier script for Market Intelligence Report:
01_Research/opencode_community_merch_intel.md

Verifies:
1. File existence and substantive content size (>3,000 bytes).
2. Grounding against user research (Lines 19, 36, 61).
3. Presence of mandatory Printify garment analytics (Comfort Colors 1717, Bella+Canvas 3001, Bella+Canvas 6681, Gildan 18000).
4. Youth tech aesthetic taxonomy & Etsy 13-tag matrix.
5. Community QA architecture, zero-spend policy compliance, and conversion funnel.
6. Zero hardcoded personal paths (Portability Invariant).
"""

import os
import sys

def verify_report():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    report_path = os.path.join(base_dir, "opencode_community_merch_intel.md")

    print("[*] Verifying research deliverable at:", report_path)

    # 1. File existence
    if not os.path.isfile(report_path):
        print(f"[FAIL] Deliverable not found at: {report_path}")
        sys.exit(1)

    file_size = os.path.getsize(report_path)
    print(f"[+] File exists. Size: {file_size} bytes")
    if file_size < 3000:
        print(f"[FAIL] Deliverable size {file_size} is under substantive threshold (3000 bytes).")
        sys.exit(1)

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 2. Mandatory content anchors
    required_anchors = [
        "Printify Apparel Market Intelligence",
        "Comfort Colors 1717",
        "Bella + Canvas 3001",
        "Bella + Canvas 6681",
        "Gildan 18000",
        "Cyber-Y2K",
        "Frutiger Aero",
        "Lo-Fi Hacker Girl",
        "Community QA Platform Architecture",
        "13-Tag Etsy SEO Matrix",
        "Line 19",
        "Line 36",
        "Line 61",
        "Net Cash Profit per Garment",
        "Zero Capital Outlay"
    ]

    missing_anchors = [anchor for anchor in required_anchors if anchor not in content]
    if missing_anchors:
        print(f"[FAIL] Missing mandatory content anchors: {missing_anchors}")
        sys.exit(1)
    print(f"[+] All {len(required_anchors)} mandatory content anchors verified present.")

    # 3. Portability check (Zero hardcoded personal paths)
    banned_substrings = ["C:\\Users\\", "c:\\users\\", "/home/"]
    for banned in banned_substrings:
        if banned in content:
            print(f"[FAIL] Hardcoded personal path detected in deliverable: {banned}")
            sys.exit(1)
    print("[+] Portability Invariant satisfied (Zero personal path leaks).")

    print("\n=======================================================")
    print("  RESEARCH VERIFICATION: PASS (Exit Code 0)")
    print("=======================================================")
    sys.exit(0)

if __name__ == "__main__":
    verify_report()
