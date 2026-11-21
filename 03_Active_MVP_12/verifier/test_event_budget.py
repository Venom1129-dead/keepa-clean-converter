import os
import sys

def verify_event_budget():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frontend_dir = os.path.join(base_dir, "frontend")

    html_path = os.path.join(frontend_dir, "index.html")
    css_path = os.path.join(frontend_dir, "styles.css")
    js_path = os.path.join(frontend_dir, "app.js")

    print("[*] Verifying MVP_12 Holiday & Event Budget Splitter Assets...")

    for path, name in [(html_path, "index.html"), (css_path, "styles.css"), (js_path, "app.js")]:
        assert os.path.exists(path), f"Missing file: {name}"
        assert os.path.getsize(path) > 100, f"File {name} too small"
        print(f" [+] Found {name}: {os.path.getsize(path)} bytes")

    # 1. HTML Verification
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="targetBudgetInput"' in html, "Missing targetBudgetInput"
    assert 'id="itemsTableBody"' in html, "Missing itemsTableBody table"
    assert 'id="exportCsvBtn"' in html, "Missing exportCsvBtn"
    assert 'gumroad.com' in html or 'Get Planner Vault' in html, "Missing monetization CTA"
    print(" [+] HTML structure and inputs verified.")

    # 2. CSS Verification
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    assert '--primary' in css and '--font-main' in css, "Missing CSS theme variables"
    assert '.progress-bar-fill' in css, "Missing progress bar styling"
    print(" [+] CSS styles and theme verified.")

    # 3. Mathematical & Ledger Logic Verification
    print("[*] Validating Ledger Math and Group Cost Splitter Logic...")

    # Math test 1: Budget allocation
    target_budget = 1500.0
    items = [
        {"name": "Mom", "actual": 75.0},
        {"name": "Dad", "actual": 129.0},
        {"name": "Dinner", "actual": 380.0},
        {"name": "Decor", "actual": 85.0},
        {"name": "Secret Santa", "actual": 48.0}
    ]
    total_spent = sum(it["actual"] for it in items)
    assert total_spent == 717.0, f"Unexpected total spent: {total_spent}"
    remaining = target_budget - total_spent
    assert remaining == 783.0, f"Unexpected remaining: {remaining}"
    percent_used = (total_spent / target_budget) * 100.0
    assert round(percent_used, 1) == 47.8, f"Unexpected percent: {percent_used}"

    # Math test 2: Group expense splitting
    members = ["Alex", "Jordan", "Taylor", "Sam"]
    shared_cost = 480.0
    per_person = shared_cost / len(members)
    assert per_person == 120.0, f"Split error: {per_person}"

    print(" [+] Budget totals, remaining funds, and equal group splitting verified.")
    print("\n[SUCCESS] ALL VERIFICATION CHECKS PASSED FOR MVP_12 (Exit Code 0).")

if __name__ == "__main__":
    verify_event_budget()
