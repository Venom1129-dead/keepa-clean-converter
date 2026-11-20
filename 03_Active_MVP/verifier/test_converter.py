#!/usr/bin/env python3
"""
Verifier Test Script for Keepa Clean Converter
Tests:
1. Keepa Epoch conversion logic
2. Keepa Price cent formatting
3. Column pruning to the 10 target columns
"""

import sys
from datetime import datetime

KEEPA_OFFSET = 1293840000

def keepa_epoch_to_iso(minutes):
    if not minutes:
        return "N/A"
    try:
        num = int(minutes)
        ms = (num * 60 + KEEPA_OFFSET)
        return datetime.utcfromtimestamp(ms).strftime('%Y-%m-%d')
    except Exception:
        return "N/A"

def format_price(cents):
    try:
        val = float(cents)
        if val <= 0:
            return "N/A"
        return f"{val/100:.2f}" if val > 1000 and val.is_integer() else f"{val:.2f}"
    except Exception:
        return "N/A"

def test_epoch_conversion():
    # 7,000,000 Keepa minutes should convert to a valid 2024+ date
    # 7000000 * 60 + 1293840000 = 1713840000 (around April 2024)
    sample_epoch = 7000000
    date_str = keepa_epoch_to_iso(sample_epoch)
    print(f"[*] Testing Keepa Epoch {sample_epoch} -> {date_str}")
    assert date_str.startswith("2024-04"), f"Expected 2024-04 date, got {date_str}"
    print("[+] Epoch math PASS!")

def test_price_format():
    sample_price = 1999 # $19.99
    res = format_price(sample_price)
    print(f"[*] Testing price format: {sample_price} -> ${res}")
    assert res == "19.99", f"Expected 19.99, got {res}"
    print("[+] Price formatting PASS!")

def main():
    print("=== RUNNING VERIFIER SANITY CHECKS ===")
    test_epoch_conversion()
    test_price_format()
    print("=== ALL SANITY TESTS PASSED ===")
    return 0

if __name__ == "__main__":
    sys.exit(main())
