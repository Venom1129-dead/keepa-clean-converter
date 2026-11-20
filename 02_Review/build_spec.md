# Build Spec: Keepa-to-Clean-Excel Instant Converter & Epoch Fixer
**Target Revenue:** $14 one-time license  
**Target Build Time:** <3 hours  
**Dependencies:** Client-side HTML/JS/CSS (PapaParse + SheetJS). 0 external paid APIs.

---

## 1. Problem Statement & Proof-of-Wallet
Amazon FBA sellers paying €19/mo for Keepa Pro dump CSVs with 80+ columns and proprietary epoch timestamps (Keepa minutes since Jan 1, 2011). Competing browser tools like Gridwinner crash or hard-cap at 50 MB. Sellers spend hours manually cleaning these dumps in Excel or pay Upwork data assistants.

---

## 2. The 10% Wedge Solution
A fast, zero-server browser application that streams multi-hundred MB Keepa CSV dumps locally in client RAM using Web Workers:
1. **Epoch Conversion Engine:** Automatically converts Keepa epoch timestamps (`(keepa_time * 60 + 1293840000) * 1000`) into human-readable ISO dates (`YYYY-MM-DD`).
2. **Column Pruning:** Strips the 70+ noisy, unneeded columns down to the 10 core buying metrics:
   - ASIN
   - Title
   - Current BSR (Sales Rank)
   - 90-Day Avg BSR
   - Current Buy Box Price ($)
   - 90-Day Avg Buy Box Price ($)
   - Buy Box % (Amazon vs 3P)
   - FBA Seller Count
   - New Offer Count
   - Review Rating & Count
3. **Chunked Local Export:** Uses Web Worker streaming so 100MB+ files process smoothly without freezing the browser, then downloads a clean `.xlsx` or `.csv`.
4. **Monetization Gate:**
   - Free tier: Processes up to 50 rows for instant live preview and trust-building.
   - Pro unlock ($14): Gumroad / Lemon Squeezy license key verification unlocks unlimited rows and instant batch export.

---

## 3. Architecture & File Tree
```plaintext
03_Active_MVP/
├── frontend/
│   ├── index.html        <-- Drag-and-drop clean UI + 50-row preview table
│   ├── styles.css        <-- Clean Tailwind/Modern dark-mode CSS
│   ├── app.js            <-- UI event handling & Gumroad license check
│   └── worker.js         <-- Web Worker streaming PapaParse + Epoch math
└── verifier/
    └── test_converter.js <-- Automated sanity check on sample Keepa row
```

---

## 4. Acceptance Criteria & Verifier Rubric
- [ ] Loads sample Keepa CSV with 100+ columns without freezing.
- [ ] Epoch conversion produces correct 2025/2026 calendar dates.
- [ ] Export produces valid, clean Excel (.xlsx) file with exactly the 10 core columns.
- [ ] License modal triggers when processing >50 rows.
