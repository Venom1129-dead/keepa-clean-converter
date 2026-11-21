import os
import sys

def verify_pc_audit():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frontend_dir = os.path.join(base_dir, "frontend")

    html_path = os.path.join(frontend_dir, "index.html")
    css_path = os.path.join(frontend_dir, "styles.css")
    js_path = os.path.join(frontend_dir, "app.js")

    print("[*] Verifying MVP_13 PC Hardening & Privacy Audit Hub Assets...")

    for path, name in [(html_path, "index.html"), (css_path, "styles.css"), (js_path, "app.js")]:
        assert os.path.exists(path), f"Missing file: {name}"
        assert os.path.getsize(path) > 100, f"File {name} too small"
        print(f" [+] Found {name}: {os.path.getsize(path)} bytes")

    # 1. HTML Verification
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="scoreNumber"' in html, "Missing scoreNumber element"
    assert 'id="auditChecklist"' in html, "Missing auditChecklist container"
    assert 'id="copyRemediationBtn"' in html, "Missing copyRemediationBtn button"
    assert 'adguard.com' in html and 'malwarebytes.com' in html, "Missing partner recommendations"
    print(" [+] HTML structure and partner sections verified.")

    # 2. CSS Verification
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    assert '--neon-cyan' in css and '--neon-green' in css, "Missing CSS theme variables"
    assert '.risk-badge' in css and '.check-item' in css, "Missing card and badge styles"
    print(" [+] CSS styles and cyber defense theme verified.")

    # 3. Mathematical & Scoring Logic Verification
    print("[*] Validating 15-Point Hardening & Scoring Distribution...")
    
    # Extract point distribution from app.js
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()

    # Find points definitions
    import re
    points = [int(p) for p in re.findall(r'points:\s*(\d+)', js)]
    assert len(points) == 15, f"Expected exactly 15 checks, found {len(points)}"
    total_score = sum(points)
    assert total_score == 100, f"Total score must sum to exactly 100, got {total_score}"

    print(f" [+] Verified 15 defense checks totaling exactly {total_score} points.")
    print("\n[SUCCESS] ALL VERIFICATION CHECKS PASSED FOR MVP_13 (Exit Code 0).")

if __name__ == "__main__":
    verify_pc_audit()
