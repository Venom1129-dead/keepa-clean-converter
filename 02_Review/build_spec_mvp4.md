# Build Spec: On-Page Technical SEO & Schema Diff Chrome/Edge Extension
- **Asset ID:** MVP_04
- **Target Revenue:** $12 one-time license
- **Target Build Time:** <3 hours
- **Dependencies:** Manifest V3, Vanilla HTML/CSS/JS. 0 external paid APIs.

---

## 1. Problem Statement & Proof-of-Wallet
SEOs and agency freelancers pay $129–$249/month for Ahrefs or Semrush, or rely on outdated, insecure extensions (like Open SEO Stats, which was recently flagged as malicious by Microsoft Edge). Freelancers need a fast, privacy-first, 1-click tool to inspect on-page technical SEO, detect missing canonicals/schema, and export client-ready audits.

---

## 2. The 10% Wedge Solution
A zero-permission, local-DOM technical audit extension:
1. **Instant Meta & Head Audit:** Title tag (with pixel length warning), Meta Description, Robots tags (`noindex`/`nofollow`), Canonical tag validation (`self-referencing` vs `cross-domain`).
2. **Heading Tree Validator:** H1 through H6 hierarchy inspection, flagging multiple H1s or skipped heading levels.
3. **Structured Data (JSON-LD) Inspector:** Extracts and parses all `<script type="application/ld+json">` tags, validating syntax and displaying Schema types (`Product`, `Article`, `Organization`, `FAQPage`).
4. **Social Graph Preview:** Open Graph (`og:title`, `og:image`) and Twitter Card inspection.
5. **1-Click Client Export:**
   - Free Tier: On-screen live audit.
   - Pro ($12): Exports branded Markdown or CSV audit report for agency client deliverables.

---

## 3. Architecture & File Tree
```plaintext
03_Active_MVP_04/
├── extension/
│   ├── manifest.json   <-- Manifest V3 definition
│   ├── popup.html      <-- Audit tab panels & export controls
│   ├── popup.css       <-- Clean responsive dark UI
│   └── popup.js        <-- Content script injector & audit calculation engine
└── verifier/
    ├── test_page.html  <-- Test HTML fixture with intentionally broken SEO
    └── test_audit.py   <-- Deterministic parser verification suite
```

---

## 4. Deterministic Acceptance Criteria
- [ ] Valid Manifest V3 compliant with Chrome & Edge Web Store policies.
- [ ] Correctly identifies missing canonical tags, multiple H1s, and malformed JSON-LD.
- [ ] Generates clean Markdown audit report.
- [ ] Passes automated test suite with Exit Code 0.
