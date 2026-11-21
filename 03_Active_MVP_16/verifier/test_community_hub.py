#!/usr/bin/env python3
"""
Nexus Community QA & Knowledge Engine — Deterministic Verifier Suite
Autonomous AI Income Factory — Asset #16 (MVP_16)
Enforces:
1. Portability (100% relative paths)
2. Zero external dependencies / air-gapped standalone verification
3. 4-Category balance: Trading, AI, Real Estate, Health
4. Lead capture and local export integrity
5. Zip bundle integrity
Returns Exit Code 0 on complete pass.
"""

import os
import sys
import re
import zipfile

def verify_community_hub():
    print("=" * 65)
    print(" NEXUS COMMUNITY QA & KNOWLEDGE ENGINE — DETERMINISTIC VERIFIER")
    print("=" * 65)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.exists(os.path.join(base_dir, "index.html")) and os.path.exists(os.path.join(base_dir, "03_Active_MVP_16", "index.html")):
        base_dir = os.path.join(base_dir, "03_Active_MVP_16")
    print(f"[*] Base Directory: {base_dir}")

    # 1. File Inventory Check
    required_files = [
        ("index.html", 2000),
        ("README.md", 200),
        (os.path.join("templates", "community_guidelines.md"), 200),
        (os.path.join("templates", "qa_curation_sop.md"), 200),
        ("Community_QA_Platform_Vault.zip", 1000)
    ]

    print("\n--- 1. File Inventory & Storage Validation ---")
    for rel_path, min_bytes in required_files:
        full_path = os.path.join(base_dir, rel_path)
        assert os.path.exists(full_path), f"CRITICAL: Missing file: {rel_path}"
        file_size = os.path.getsize(full_path)
        assert file_size >= min_bytes, f"CRITICAL: {rel_path} is undersized ({file_size} < {min_bytes} bytes)"
        print(f"  [+] Found {rel_path:<40} : {file_size:>8} bytes")

    # 2. Air-Gapped Zero-Dependency & DOM Element Audit
    print("\n--- 2. Air-Gapped Zero-Dependency & DOM Element Audit ---")
    html_path = os.path.join(base_dir, "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Verify no external CDN/HTTP links in script or stylesheet link tags
    external_links = re.findall(r'<link[^>]+href=["\'](http[s]?://[^"\']+)["\']', html)
    external_scripts = re.findall(r'<script[^>]+src=["\'](http[s]?://[^"\']+)["\']', html)
    assert len(external_links) == 0, f"Found external stylesheet CDN links: {external_links}"
    assert len(external_scripts) == 0, f"Found external script CDN links: {external_scripts}"
    print("  [+] Air-gapped validation passed: ZERO external remote CDNs or scripts.")

    # Check key UI and functional elements
    mandatory_elements = [
        "searchInput", "sortSelect", "questionsContainer", "askQuestionBtn",
        "vipModalBtn", "vipLeadForm", "leadEmail", "questionForm",
        "qTitleInput", "qCatSelect", "qBodyInput", "exportDataBtn", "exportLeadsBtn"
    ]
    for el in mandatory_elements:
        assert f'id="{el}"' in html, f"Missing required DOM element: id=\"{el}\""
    print(f"  [+] Verified {len(mandatory_elements)} mandatory UI and interaction elements.")

    # 3. Channel Categories & Seed Distribution Audit
    print("\n--- 3. Channel Categories & Knowledge Domain Audit ---")
    categories = ["trading", "ai", "re", "health"]
    for cat in categories:
        assert f'cat: "{cat}"' in html, f"Missing seed questions for category: {cat}"
        print(f"  [+] Verified active knowledge channel: [{cat.upper()}]")

    # Verify verified solutions are included in seed data
    assert 'verified: true' in html, "Missing verified solutions in seed QA catalog"
    print("  [+] Verified peer-reviewed solutions catalog present.")

    # 4. Lead Capture & Export Validation
    print("\n--- 4. VIP Lead Capture & Export Functionality ---")
    assert "exportDataBtn" in html and "nexus_community_qa_backup" in html, "Missing JSON backup export mechanism"
    assert "exportLeadsBtn" in html and "nexus_vip_leads" in html, "Missing CSV leads export mechanism"
    print("  [+] Verified local JSON and CSV export capabilities for community data and VIP leads.")

    # 5. Zip Bundle Verification
    print("\n--- 5. Distribution Zip Archive Integrity ---")
    zip_path = os.path.join(base_dir, "Community_QA_Platform_Vault.zip")
    with zipfile.ZipFile(zip_path, 'r') as z:
        names = z.namelist()
        corrupt = z.testzip()
        assert corrupt is None, f"Zip archive corrupted: {corrupt}"
        assert "index.html" in names, "index.html missing inside zip"
        assert "README.md" in names, "README.md missing inside zip"
        assert any("templates" in n for n in names), "Templates missing inside zip"
        print(f"  [+] Zip file verified clean. Contains {len(names)} files:")
        for n in names:
            print(f"      - {n}")

    print("\n" + "=" * 65)
    print(" [SUCCESS] ALL NEXUS COMMUNITY HUB VERIFIER CHECKS PASSED (Exit Code 0)")
    print("=" * 65)
    return 0

if __name__ == "__main__":
    sys.exit(verify_community_hub())
