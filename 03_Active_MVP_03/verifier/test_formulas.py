#!/usr/bin/env python3
"""
verifier/test_formulas.py
Deterministic verification tests for Notion 12-Week Sprint OS formulas.
Tests execution score math, progress bar rendering, and division-by-zero guards.
"""

import sys

def calculate_execution_score(completed, total):
    if total <= 0:
        return 0.0
    score = (completed / total) * 100
    return min(100.0, max(0.0, round(score, 1)))

def render_progress_bar(percentage, length=10):
    clamped = max(0.0, min(100.0, percentage))
    filled_count = int(round((clamped / 100) * length))
    empty_count = length - filled_count
    bar = ("▓" * filled_count) + ("░" * empty_count)
    return f"{bar} {int(round(clamped))}%"

def test_score_calculation():
    assert calculate_execution_score(0, 10) == 0.0
    assert calculate_execution_score(5, 10) == 50.0
    assert calculate_execution_score(10, 10) == 100.0
    assert calculate_execution_score(12, 10) == 100.0  # Cap at 100%
    assert calculate_execution_score(0, 0) == 0.0      # Zero total guard
    assert calculate_execution_score(7, 8) == 87.5
    print("[PASS] Execution score calculations and edge guards verified.")

def test_progress_bar_rendering():
    assert render_progress_bar(0) == "░░░░░░░░░░ 0%"
    assert render_progress_bar(50) == "▓▓▓▓▓░░░░░ 50%"
    assert render_progress_bar(100) == "▓▓▓▓▓▓▓▓▓▓ 100%"
    assert render_progress_bar(85) == "▓▓▓▓▓▓▓▓░░ 85%"
    print("[PASS] Unicode progress bar rendering verified.")

if __name__ == "__main__":
    print("=== RUNNING NOTION SPRINT OS DETERMINISTIC FORMULA TESTS ===")
    try:
        test_score_calculation()
        test_progress_bar_rendering()
        print("\n=== ALL FORMULA VERIFICATIONS PASSED (EXIT 0) ===")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[FAIL] Test failure: {e}")
        sys.exit(1)
