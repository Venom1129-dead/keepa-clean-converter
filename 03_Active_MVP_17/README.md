# RE AI: Real Estate Cap Rate & Cash Flow Analyzer Cockpit
> **Autonomous AI Income Factory — Asset #17 (MVP_17)**  
> **Classification:** High-Yield Client-Side PropTech Underwriting Engine  
> **Portability:** 100% Zero-Spend, 100% Client-Side, Zero External Dependencies

---

## 1. Executive Summary
The **RE AI Real Estate Analyzer Cockpit** is an institutional-grade, single-file HTML5/JS underwriting engine designed for real estate investors, private lenders, and acquisitions analysts. It provides deterministic, real-time calculations for:
- **Net Operating Income (NOI)**
- **Capitalization Rate (Cap Rate %)**
- **Monthly & Annual Net Cash Flow**
- **Cash-on-Cash Return (CoC %)**
- **Debt Service Coverage Ratio (DSCR)**
- **Gross Rent Multiplier (GRM) & 1% Rule Meter**
- **Break-Even Occupancy Analysis**
- **10-Year Pro-Forma Cash Flow & Equity Trajectory**
- **5-Tier Sensitivity & Stress-Testing Matrix**
- **Executive 1-Page Printable PDF Deal Memo**

---

## 2. Core Mathematical Formulas
The application adheres strictly to standard commercial and residential underwriting mathematics:

1. **Monthly Mortgage Payment ($M$ - Principal & Interest):**
   $$M = P \cdot \frac{r(1+r)^n}{(1+r)^n - 1}$$
   - $P$ = Loan Amount ($\text{Purchase Price} - \text{Down Payment}$)
   - $r$ = Monthly interest rate ($\text{APR} / 12 / 100$)
   - $n$ = Total amortization months ($\text{Years} \times 12$)

2. **Gross Operating Income ($GOI$):**
   $$GOI = (\text{Monthly Gross Rent} \times 12) \times (1 - \text{Vacancy Rate}) + \text{Annual Other Income}$$

3. **Operating Expenses ($OpEx$):**
   $$OpEx = \text{Property Taxes} + \text{Insurance} + \text{Maintenance Reserve} + \text{Property Management} + \text{HOA} + \text{Utilities}$$

4. **Net Operating Income ($NOI$):**
   $$NOI = GOI - OpEx$$

5. **Capitalization Rate ($\text{Cap Rate}$):**
   $$\text{Cap Rate} = \left(\frac{NOI}{\text{Purchase Price}}\right) \times 100$$

6. **Annual Cash Flow:**
   $$\text{Cash Flow} = NOI - (\text{Monthly P\&I} \times 12)$$

7. **Cash-on-Cash Return ($\text{CoC}$):**
   $$\text{CoC} = \left(\frac{\text{Annual Cash Flow}}{\text{Total Initial Cash Invested}}\right) \times 100$$
   Where $\text{Total Cash Invested} = \text{Down Payment} + \text{Closing Costs} + \text{Initial Rehab}$.

8. **Debt Service Coverage Ratio ($DSCR$):**
   $$DSCR = \frac{NOI}{\text{Annual Debt Service}}$$

---

## 3. Architecture & Offline Air-Gap Compliance
- **Zero Runtime Dependencies:** No external CDNs, fonts, tracking scripts, or analytics.
- **Air-Gapped Ready:** Works 100% offline in any modern web browser.
- **Print Optimization:** Embedded `@media print` rules generate clean, lender-ready PDF deal memos.
- **Presets Built-In:**
  1. *Turnkey Single Family Rental ($320k)*
  2. *Highland Heights 4-Unit Quadplex ($680k)*
  3. *Cedar Park Distressed BRRRR Rehab ($210k)*
  4. *Metro Plaza Strip Center Triple-Net ($1.25M)*

---

## 4. Verification & Testing
Execute the deterministic test suite:
```bash
python 03_Active_MVP_17/verifier/test_re_ai.py
```
Expected output: **Exit Code 0**, verifying math formulas, element bindings, and offline zero-dependency rules.
