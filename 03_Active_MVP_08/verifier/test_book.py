#!/usr/bin/env python3
"""
03_Active_MVP_08/verifier/test_book.py
Deterministic verification tests for "How To Do Things Faster" Ebook & Template Vault.
"""

import os
import sys

BASE_DIR = os.path.dirname(__file__)
BOOK_PATH = os.path.join(BASE_DIR, "..", "book", "book_full.md")
HTML_PATH = os.path.join(BASE_DIR, "..", "book", "index.html")
TEMPLATES_DIR = os.path.join(BASE_DIR, "..", "templates")

def test_book_content():
    assert os.path.exists(BOOK_PATH), f"Book markdown must exist at {BOOK_PATH}"
    with open(BOOK_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    words = len(content.split())
    print(f"[+] Book Full Markdown: {len(content)} characters, {words} words")

    # Assertions
    assert words >= 1000, f"Guide must contain substantial content (found {words} words)"
    assert "Chapter 1:" in content, "Must contain Chapter 1"
    assert "Chapter 2:" in content, "Must contain Chapter 2"
    assert "Chapter 3:" in content, "Must contain Chapter 3"
    assert "Chapter 4:" in content, "Must contain Chapter 4"
    assert "Chapter 5:" in content, "Must contain Chapter 5"
    assert "The Shareholder Shift" in content, "Must explain Shareholder Mindset"
    assert "GitHub Pages" in content, "Must detail zero-cost hosting"

def test_templates_presence():
    assert os.path.exists(TEMPLATES_DIR), f"Templates directory must exist at {TEMPLATES_DIR}"
    templates = [f for f in os.listdir(TEMPLATES_DIR) if f.endswith(".md")]
    print(f"[+] Found {len(templates)} turnkey templates: {templates}")
    assert len(templates) >= 4, f"Must provide at least 4 templates (found {len(templates)})"

    for t in templates:
        p = os.path.join(TEMPLATES_DIR, t)
        size = os.path.getsize(p)
        assert size > 200, f"Template {t} must be non-empty (size: {size} bytes)"

def test_web_reader():
    assert os.path.exists(HTML_PATH), f"Web reader HTML must exist at {HTML_PATH}"
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()
    assert "reading-progress-bar" in html, "Web reader must have reading progress bar"
    assert "btn-copy" in html, "Web reader must have copy template buttons"

if __name__ == "__main__":
    print("=== RUNNING EBOOK & TEMPLATE VAULT VERIFIER ===")
    try:
        test_book_content()
        test_templates_presence()
        test_web_reader()
        print("\n=== ALL EBOOK VERIFICATIONS PASSED (EXIT CODE 0) ===")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[FAIL] Assertion failed: {e}")
        sys.exit(1)
