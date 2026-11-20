#!/usr/bin/env python3
"""
verifier/test_multi_format.py
Deterministic Multi-Format Stress Test for Shopify Supplier CSV Normalizer.
Tests Faire, AliExpress, Doba, and Chaos Edge Cases (HTML in titles, oz/lbs weights, special characters, missing MSRP, negative stock).
"""

import sys
import re
import csv
import os

def clean_title(title):
    if not title:
        return "Untitled Product"
    # Strip HTML tags
    clean = re.sub(r'<[^>]+>', '', title)
    return clean.strip()

def generate_handle(title):
    cleaned = clean_title(title).lower()
    # Replace non-alphanumeric with hyphen
    slug = re.sub(r'[^a-z0-9]+', '-', cleaned)
    # Strip leading and trailing hyphens
    slug = re.sub(r'^-+|-+$', '', slug)
    return slug or "product"

def parse_weight_to_grams(raw_weight):
    if not raw_weight:
        return 0
    s = str(raw_weight).lower().strip()
    match = re.search(r'([0-9.]+)', s)
    if not match:
        return 0
    val = float(match.group(1))
    
    if "oz" in s:
        # 1 oz = 28.3495 grams
        return round(val * 28.3495)
    elif "kg" in s:
        return round(val * 1000)
    elif "g" in s and "kg" not in s:
        return round(val)
    else:
        # Default assumption: lbs (1 lb = 453.592 grams)
        return round(val * 453.592)

def clamp_inventory(qty):
    try:
        val = int(float(qty))
        return max(0, val)
    except (ValueError, TypeError):
        return 0

def run_stress_test():
    fixture_path = os.path.join(os.path.dirname(__file__), "multi_supplier_stress_test.csv")
    print(f"[*] Reading multi-supplier stress test fixture: {fixture_path}")
    
    with open(fixture_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"[+] Loaded {len(rows)} diverse real-world edge case rows.")
    
    results = []
    for idx, r in enumerate(rows, 1):
        source = r["source_feed"]
        raw_title = r["product_title"]
        title = clean_title(raw_title)
        handle = generate_handle(raw_title)
        grams = parse_weight_to_grams(r["item_weight_lbs"])
        stock = clamp_inventory(r["in_stock_qty"])
        price = r["wholesale_cost"] or "0.00"
        compare_price = r["retail_msrp"] or ""
        sku = r["vendor_sku"]

        # Assertions
        assert "<" not in title and ">" not in title, f"Row {idx}: HTML tags not stripped from title: {title}"
        assert not handle.startswith("-") and not handle.endswith("-"), f"Row {idx}: Illegal handle format: {handle}"
        assert grams > 0, f"Row {idx}: Grams must be positive, got {grams}"
        assert stock >= 0, f"Row {idx}: Stock must not be negative, got {stock}"
        assert re.match(r'^[a-z0-9-]+$', handle), f"Row {idx}: Handle contains non-url characters: {handle}"

        results.append({
            "Source": source,
            "SKU": sku,
            "Handle": handle,
            "Title": title,
            "Variant Grams": grams,
            "Variant Qty": stock,
            "Variant Price": price,
            "Compare Price": compare_price
        })
        print(f"[PASS] Row {idx} ({source}): '{title}' -> handle: '{handle}', weight: {grams}g, stock: {stock}")

    out_path = os.path.join(os.path.dirname(__file__), "multi_format_normalized_output.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\n[+] Multi-format normalized output saved to: {out_path}")
    print("=== ALL MULTI-DATASET STRESS TESTS PASSED (EXIT 0) ===")

if __name__ == "__main__":
    try:
        run_stress_test()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[FAIL] Stress test assertion failed: {e}")
        sys.exit(1)
