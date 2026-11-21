# Build Spec: Zero-Bloat DCA Position Sizer & Profit-Taking Ladder Cockpit
- **Asset ID:** MVP_07
- **Target Revenue:** $9 one-time lifetime license / Free Core
- **Format:** Client-Side Web Application (HTML5 + CSS3 + Vanilla JS)
- **Deployment:** GitHub Pages (100% Free Static Hosting)
- **Dependencies:** 0 paid APIs, 0 backend servers, 100% private in-browser memory.

---

## 1. Problem Statement & Proof-of-Wallet Signal
Retail investors and crypto/stock traders who dollar-cost-average (DCA) into assets face a recurring problem:
1. They make multiple staggered buys at different prices but don't know their exact weighted cost basis.
2. Exchange fees and gas costs silently erode net margins.
3. Most traders "round-trip" their profits (watching a 2x or 3x gain crash back to break-even or a loss) because they lack an automated profit-taking ladder with predefined sell tranches.
4. Existing tools (CoinTracker, CoinLedger, TradingView apps) charge $29–$99/month and demand sensitive API key access or wallet connects.

---

## 2. The 10% Wedge Solution
A privacy-first, zero-telemetry trading & DCA financial cockpit:
1. **Weighted Average Cost Basis Calculator:**
   - Multi-tranche buy entry: Price, Quantity, Exchange Fee.
   - Computes exact weighted entry price, total capital deployed, and total fees paid.
2. **Dynamic Profit-Taking Ladder (Take-Profit Tranches):**
   - Automatically generates a 4-tier exit ladder (e.g. Target 1: +25%, Target 2: +50%, Target 3: +100%, Target 4: Moonbag).
   - Computes exact realized cash return, net profit (after buy/sell fees), and remaining tokens held.
3. **Break-Even & Stop-Loss Floor:**
   - Computes exact price level required to break even after all transaction fees.
   - Shows portfolio drawdown / downside risk at user-defined stop-loss levels.
4. **100% Private & In-Browser:**
   - Zero wallet connects, zero API keys.
   - Stores portfolio history in `localStorage`.
   - 1-Click CSV portfolio export.

---

## 3. Architecture & File Tree
```plaintext
03_Active_MVP_07/
├── frontend/
│   ├── index.html       <-- Interactive DCA dashboard & exit ladder
│   ├── app.js           <-- Financial calculation engine & LocalStorage store
│   └── styles.css       <-- Dark financial terminal theme
└── verifier/
    ├── test_dca.py      <-- Deterministic verification suite
    └── sample_dca.json
```

---

## 4. Deterministic Acceptance Criteria
- [ ] Weighted average price, net fee impact, and laddered profit calculations verified with unit tests.
- [ ] Passes automated test suite with Exit Code 0.
- [ ] Deployed to live GitHub Pages repository under `Venom1129-dead/dca-profit-calculator`.
- [ ] Complete launch copy generated in `04_Launch_Queue/dca_calculator_launch_assets.md`.
