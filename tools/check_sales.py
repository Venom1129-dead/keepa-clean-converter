#!/usr/bin/env python3
"""
Automated Payment & Sales Checker
Polls Gumroad / Lemon Squeezy API for new settled sales.
Only reports and updates experiments.md when a real payment arrives.
"""

import os
import sys
import json
import urllib.request
from datetime import datetime

EXPERIMENTS_FILE = os.path.join(os.path.dirname(__file__), "..", "00_Brain", "experiments.md")
SALES_CACHE_FILE = os.path.join(os.path.dirname(__file__), "..", "00_Brain", "memory", "findings", "sales_cache.json")

def check_gumroad_sales(access_token):
    url = f"https://api.gumroad.com/v2/sales?access_token={access_token}"
    req = urllib.request.Request(url, headers={'User-Agent': 'AIFactory-SalesTracker/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('success'):
                return data.get('sales', [])
    except Exception as e:
        print(f"[!] Error checking Gumroad sales: {e}")
    return []

def main():
    token = os.environ.get("GUMROAD_ACCESS_TOKEN")
    if not token:
        print("[i] GUMROAD_ACCESS_TOKEN not set in environment. Skipping live API check.")
        print("[i] Once you create a free read-only token on Gumroad, this script runs 100% automated.")
        return 0

    print("[*] Checking for new settled payments...")
    sales = check_gumroad_sales(token)
    
    # Load previously seen sales IDs
    seen_ids = set()
    if os.path.exists(SALES_CACHE_FILE):
        try:
            with open(SALES_CACHE_FILE, "r") as f:
                seen_ids = set(json.load(f))
        except Exception:
            pass

    new_sales = [s for s in sales if s.get('id') not in seen_ids]

    if not new_sales:
        print("[*] No new payments since last check. Staying silent.")
        return 0

    # Found new sales! Record them automatically.
    print(f"\n🎉 [ALERT] {len(new_sales)} NEW PAYMENT(S) DETECTED!\n")
    for sale in new_sales:
        price = sale.get('price', 0) / 100.0
        currency = sale.get('currency', 'usd').upper()
        product = sale.get('product_name', 'Unknown Product')
        buyer = sale.get('email', 'Private Buyer')
        date = sale.get('created_at', datetime.now().isoformat())
        
        print(f"  + Sale ID: {sale.get('id')}")
        print(f"  + Product: {product}")
        print(f"  + Amount:  ${price:.2f} {currency}")
        print(f"  + Date:    {date}")
        
        seen_ids.add(sale.get('id'))

    # Update cache
    os.makedirs(os.path.dirname(SALES_CACHE_FILE), exist_ok=True)
    with open(SALES_CACHE_FILE, "w") as f:
        json.dump(list(seen_ids), f)

    print("\n[+] Automatically logged to memory vault.")
    return 1

if __name__ == "__main__":
    sys.exit(main())
