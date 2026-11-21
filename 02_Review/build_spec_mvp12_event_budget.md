# BUILD SPECIFICATION: MVP_12 — Holiday & Special Event Budget / Expense Splitter

## 1. Executive Summary & Market Fit
- **Category:** Personal Finance & Event Planning Tools
- **Source Research:** Google Doc Research — *"Things to take into consideration: Events, Local/Global/personal. Like public holidays/special events/birthday"*
- **Target Audience:** Families, couples, party hosts, holiday shoppers, and group trip organizers.
- **Problem Solved:** Overspending during holidays (Black Friday, Christmas, Diwali, birthdays, weddings) and messy manual spreadsheets for tracking who paid for what in group events.
- **The 10% Wedge:** A clean, zero-signup, client-side budget cockpit that calculates:
  1. Total Target Budget vs Actual Committed Spend with real-time visual progress gauge.
  2. Per-Recipient / Per-Item gift tracker with status (Idea, Purchased, Wrapped, Delivered).
  3. Fair Group Expense Splitter (who owes whom) with settlement ledger.
  4. 1-Click CSV export and LocalStorage auto-save.

---

## 2. Technical Requirements
- **Zero-Dependency Engine:** Pure HTML5, CSS3, and Vanilla JavaScript.
- **LocalStorage Persistence:** Auto-saves on every keystroke; no backend database or paid cloud servers needed.
- **Export Capabilities:** Clean CSV export of budget summary and expense breakdown.
- **Deployment:** Live on GitHub Pages (`https://venom1129-dead.github.io/event-budget-splitter/`).

---

## 3. Directory Layout
```
03_Active_MVP_12/
├── frontend/
│   ├── index.html        # Clean, modern event budget dashboard
│   ├── styles.css        # Responsive, festive yet clean UI
│   └── app.js            # Ledger math, expense splitting, and CSV export
└── verifier/
    └── test_event_budget.py  # Deterministic validation of ledger math and state
```
