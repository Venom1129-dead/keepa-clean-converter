# Build Spec: Freelancer Connects-ROI & Proposal Win-Rate Tracker
- **Asset ID:** MVP_05
- **Target Revenue:** $9 one-time license
- **Format:** In-browser Client-Side Web App (Vanilla JS + LocalStorage + CSV export)
- **Dependencies:** 0 paid APIs, 0 backend servers, 100% private in-browser memory.

---

## 1. Problem Statement & Proof-of-Wallet Signal
Following Upwork's shift to a flat 15% platform fee and aggressive proposal boost bidding (freelancers reporting 100–200 Connects spent per bid), solo freelancers and agencies are experiencing negative net ROI on small-to-medium contracts.
Verbatim Reddit Quote:
> "Upwork silently bumped the freelancer fee to 15%. Enough is enough. Our bidding team is burning connects (200+ per boost) but leads and conversions have tanked — what changed and what are we missing?" — r/Upwork

---

## 2. The 10% Wedge Solution
A privacy-first, zero-telemetry financial cockpit for freelancers:
1. **Connects Unit Economics Engine:**
   - Connect Cost Basis ($0.15 standard or custom currency)
   - Platform Fee Deduction (10%, 15%, or custom freelance fee)
   - Contract Gross vs. Net Realized Earnings
2. **Break-Even & Risk Threshold Calculator:**
   - Automatically calculates maximum viable Connect bid before negative ROI
   - Computes effective hourly rate after acquisition cost
3. **Proposal Performance & Win-Rate Analytics:**
   - Track bids by status (`Sent`, `Viewed`, `Interviewed`, `Won`, `Lost`)
   - Computes Conversion Funnel %: Win Rate, Cost-Per-Interview, Customer Acquisition Cost (CAC)
4. **Offline & Privacy-First:**
   - 100% stored in browser `localStorage`
   - Instant 1-click CSV backup and export

---

## 3. Architecture & File Tree
```plaintext
03_Active_MVP_05/
├── frontend/
│   ├── index.html       <-- Financial dashboard & proposal log
│   ├── app.js           <-- Calculation engine & LocalStorage store
│   └── styles.css       <-- Dark modern financial UI
└── verifier/
    ├── test_roi.py      <-- Deterministic formula verification suite
    └── sample_proposals.csv
```

---

## 4. Deterministic Acceptance Criteria
- [ ] Connects cost, fee deduction, net margin, and break-even calculations verified with unit tests.
- [ ] Passes automated test suite with Exit Code 0.
- [ ] Responsive, client-side web interface ready for static deployment.
