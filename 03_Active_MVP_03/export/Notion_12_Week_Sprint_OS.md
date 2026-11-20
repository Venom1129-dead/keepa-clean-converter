# Zero-Bloat 12-Week Year Sprint & Operations OS for Notion
> A lightweight, high-velocity execution operating system. Zero paid Notion AI credits required. Powered 100% by native Notion 2.0 formulas and automated rollups.

---

## 🏛️ System Architecture

```
                  ┌─────────────────────────────────┐
                  │      DATABASE 1: GOALS          │
                  │  (1–3 Non-Negotiable Outcomes)  │
                  └───────────────┬─────────────────┘
                                  │ 1:Many
                  ┌───────────────▼─────────────────┐
                  │    DATABASE 2: WEEKLY TACTICS   │
                  │   (Lead Measures & Execution)   │
                  └───────────────┬─────────────────┘
                                  │ 1:Many
                  ┌───────────────▼─────────────────┐
                  │    DATABASE 3: DAILY SPRINT     │
                  │   (Binary Completion & Logs)    │
                  └─────────────────────────────────┘
```

---

## 1. Database 1: Goals & Vision
| Property Name | Property Type | Description / Formula |
|---|---|---|
| **Goal Title** | Title | The primary quarterly outcome (e.g., "$10k MRR", "Launch 3 MVPs") |
| **Quarter** | Select | `Q1`, `Q2`, `Q3`, `Q4` |
| **Target Date** | Date | End of Week 12 deadline |
| **Status** | Status | `Not Started`, `In Progress`, `Achieved`, `Deferred` |
| **Weekly Tactics** | Relation | Linked to Database 2 (Weekly Tactics) |
| **Overall Goal Progress** | Formula | `let(total, length(prop("Weekly Tactics")), completed, length(filter(prop("Weekly Tactics"), current.prop("Status") == "Completed")), if(total == 0, "░░░░░░░░░░ 0%", let(pct, round((completed / total) * 100), let(filled, round((pct / 100) * 10), repeat("▓", filled) + repeat("░", 10 - filled) + " " + pct + "%"))))` |

---

## 2. Database 2: Weekly Tactics (Lead Measures)
| Property Name | Property Type | Description / Formula |
|---|---|---|
| **Tactic** | Title | Specific recurring action (e.g., "Publish 2 Reddit value posts/week") |
| **Goal** | Relation | Linked to Database 1 (Goals) |
| **Target Frequency** | Number | Target times per week (e.g., `5`) |
| **Week Number** | Select | `Week 1` through `Week 12` |
| **Daily Logs** | Relation | Linked to Database 3 (Daily Sprint) |
| **Weekly Execution Score** | Formula | `let(total, prop("Target Frequency"), completed, length(filter(prop("Daily Logs"), current.prop("Completed?"))), if(total <= 0, "░░░░░░░░░░ 0%", let(pct, min(100, round((completed / total) * 100)), let(filled, round((pct / 100) * 10), if(pct >= 85, "🟢 ", "🔴 ") + repeat("▓", filled) + repeat("░", 10 - filled) + " " + pct + "%"))))` |

---

## 3. Database 3: Daily Sprint Scorecard
| Property Name | Property Type | Description |
|---|---|---|
| **Date** | Date | Today's date |
| **Tactic Linked** | Relation | Linked to Database 2 |
| **Completed?** | Checkbox | Binary 1 or 0 execution check |
| **Daily Blockers / Friction** | Text | Quick note on what slowed execution |

---

## 4. Native Formula Cheat Sheet (Copy-Paste)

### A. Dynamic Unicode Progress Bar Formula
```javascript
let(
  pct, prop("Score %"),
  filled, round((pct / 100) * 10),
  repeat("▓", filled) + repeat("░", 10 - filled) + " " + pct + "%"
)
```

### B. High-Performance Execution Score (85% Target Threshold)
```javascript
let(
  total, prop("Target Frequency"),
  done, prop("Completed Count"),
  if(total <= 0, "0%", 
    let(pct, round((done / total) * 100),
      if(pct >= 85, "🏆 On Track (" + pct + "%)", "⚠️ Execution Gap (" + pct + "%)")
    )
  )
)
```
