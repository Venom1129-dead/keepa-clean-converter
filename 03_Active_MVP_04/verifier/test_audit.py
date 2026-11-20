#!/usr/bin/env python3
"""
verifier/test_audit.py
Deterministic verification tests for On-Page SEO & Schema Extension audit engine.
"""

import sys
import re
import json
import os

def audit_html(html_content):
    audit = {
        "title": None,
        "title_length": 0,
        "description": None,
        "canonical": None,
        "robots": None,
        "og_title": None,
        "h1_count": 0,
        "h1_tags": [],
        "h2_count": 0,
        "json_ld_schemas": [],
        "warnings": []
    }

    # Title
    t_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
    if t_match:
        audit["title"] = t_match.group(1).strip()
        audit["title_length"] = len(audit["title"])
        if audit["title_length"] > 60:
            audit["warnings"].append("Title exceeds 60 characters (may truncate in Google SERPs)")

    # Description
    d_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html_content, re.IGNORECASE)
    if d_match:
        audit["description"] = d_match.group(1).strip()
    else:
        audit["warnings"].append("Missing meta description")

    # Canonical
    c_match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', html_content, re.IGNORECASE)
    if c_match:
        audit["canonical"] = c_match.group(1).strip()

    # Headings
    h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', html_content, re.IGNORECASE | re.DOTALL)
    audit["h1_count"] = len(h1s)
    audit["h1_tags"] = [h.strip() for h in h1s]
    if audit["h1_count"] > 1:
        audit["warnings"].append(f"Multiple H1 tags detected ({audit['h1_count']}). Google prefers a single primary H1.")
    elif audit["h1_count"] == 0:
        audit["warnings"].append("Missing H1 heading tag")

    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', html_content, re.IGNORECASE | re.DOTALL)
    audit["h2_count"] = len(h2s)

    # JSON-LD
    json_ld_scripts = re.findall(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', html_content, re.IGNORECASE | re.DOTALL)
    for s in json_ld_scripts:
        try:
            parsed = json.loads(s.strip())
            audit["json_ld_schemas"].append(parsed)
        except json.JSONDecodeError:
            audit["warnings"].append("Malformed JSON-LD schema script detected")

    return audit

def test_seo_auditor():
    fixture_path = os.path.join(os.path.dirname(__file__), "test_page.html")
    with open(fixture_path, "r", encoding="utf-8") as f:
        content = f.read()

    res = audit_html(content)
    print(f"[+] Title: '{res['title']}' ({res['title_length']} chars)")
    print(f"[+] Meta Description: '{res['description'][:40]}...'")
    print(f"[+] Canonical URL: {res['canonical']}")
    print(f"[+] H1 Count: {res['h1_count']} | H2 Count: {res['h2_count']}")
    print(f"[+] Detected Schemas: {len(res['json_ld_schemas'])} ([{res['json_ld_schemas'][0].get('@type')}])")
    print(f"[+] Flagged Warnings: {res['warnings']}")

    # Assertions
    assert res["title"] == "Best Wireless Headphones 2026 - Ultimate Buyer's Guide"
    assert res["canonical"] == "https://example.com/headphones-guide"
    assert res["h1_count"] == 2, "Must detect exactly 2 H1 tags"
    assert any("Multiple H1 tags detected" in w for w in res["warnings"]), "Must flag multiple H1s warning"
    assert len(res["json_ld_schemas"]) == 1
    assert res["json_ld_schemas"][0]["@type"] == "Product"
    assert res["json_ld_schemas"][0]["offers"]["price"] == "199.99"
    print("\n[PASS] All deterministic SEO audit assertions verified.")

if __name__ == "__main__":
    print("=== RUNNING TECHNICAL SEO AUDIT ENGINE TESTS ===")
    try:
        test_seo_auditor()
        print("\n=== ALL TESTS PASSED: AUDIT ENGINE SOUND (EXIT 0) ===")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[FAIL] Assertion failed: {e}")
        sys.exit(1)
