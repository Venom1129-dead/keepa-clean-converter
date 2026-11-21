# BUILD SPECIFICATION: MVP_13 — PC Hardening & Privacy Audit Hub

## 1. Executive Summary & Market Fit
- **Category:** Cybersecurity, PC Privacy & Partner Programs
- **Source Research:** Google Doc Research — Partner Programs: *"Selling adguard / malwarebytes / easeus / tech items"*
- **Target Audience:** Privacy-conscious PC users, developers, remote workers, and gamers seeking cleaner, faster Windows environments.
- **Problem Solved:** Windows default telemetry, browser tracking, unencrypted DNS leaks, and lack of verified backup protocols.
- **The 10% Wedge:** An interactive 15-point System Hardening & Privacy Audit that calculates a live security score (0–100%), breaks vulnerabilities into 4 critical pillars, generates copyable PowerShell hardening snippets, and connects users to legitimate privacy partner solutions (AdGuard, Malwarebytes).

---

## 2. Technical Requirements
- **Format:** Pure HTML5, CSS3, Vanilla JavaScript (Zero external libraries, 100% client-side).
- **Core Pillars Assessed:**
  1. *OS Telemetry & Diagnostics* (Diagnostic data, advertising ID, location tracking)
  2. *Network & DNS Encryption* (DoH/DoT DNS encryption, WebRTC IP leak prevention)
  3. *Malware & Exploitation Defense* (Core isolation, tamper protection, ransomware shields)
  4. *Backup & Disaster Recovery* (Automated shadow copy, off-site encrypted backup)
- **Deployment:** Live on GitHub Pages (`https://venom1129-dead.github.io/pc-privacy-audit/`).

---

## 3. Directory Layout
```
03_Active_MVP_13/
├── frontend/
│   ├── index.html        # Interactive security audit dashboard
│   ├── styles.css        # Clean cyber-defense aesthetic
│   └── app.js            # Scoring algorithm, remediation generator, and storage
└── verifier/
    └── test_pc_audit.py  # Deterministic validation of scoring math and checklist
```
