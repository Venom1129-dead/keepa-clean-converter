---
name: trading-statistical-verifier
description: Claude's brutal mathematical audit to reject data-snooping bias, p-hacking, and overfitting using Walk-Forward Optimization, Monte Carlo permutation tests, and Deflated Sharpe Ratios.
---

# Trading Statistical Verifier & Kill-Switch Skill

## 1. Role: The Brutal Gatekeeper
Claude acts as the Chief Risk Officer and Chief Verifier. In trading, 95% of proposed strategies are statistical noise that fail in live markets. Claude's mandate is to ruthlessly stress-test and reject any strategy that exhibits:
- Data-snooping bias (cherry-picked date ranges).
- Overfitting (too many tuned indicator parameters).
- Inadequate sample size (e.g. only 15 trades over 3 years).
- Catastrophic tail risk (high win rate but one trade wipes out 80% of account).

---

## 2. The 5-Point Verification Gauntlet
Every strategy candidate must pass all 5 gates before being approved for paper or live execution:

### Gate 1: Minimum Sample Size ($N \ge 100$)
- A backtest with fewer than 100 trades is statistically insignificant. T-test power is too weak to distinguish skill from luck.

### Gate 2: Walk-Forward Optimization (WFO)
- Split data into:
  - **In-Sample (Train, 70%):** Parameter optimization.
  - **Out-of-Sample (Test, 30%):** Blind evaluation on unseen future data.
- **Passing Criterion:** Out-of-sample Sharpe Ratio must retain at least **65%** of the In-sample Sharpe Ratio. If in-sample Sharpe is 3.0 and out-of-sample drops to 0.8, the strategy is overfitted and immediately **KILLED**.

### Gate 3: Monte Carlo Permutation Test (1,000 Shuffles)
- Randomly shuffle the order of historical trade returns 1,000 times.
- Calculate the maximum drawdown distribution under worst-case sequencing.
- **Passing Criterion:** The strategy's maximum drawdown in 95% of permutations must not exceed 25% of total capital.

### Gate 4: Deflated Sharpe Ratio (DSR) & P-Value
- Uses the Marcos López de Prado mathematical formula adjusting for the number of trials tested ($K$ strategies):
  $$\text{DSR} = \Phi\left(\frac{(\widehat{\text{SR}} - \text{SR}^*) \sqrt{T-1}}{\sqrt{1 - \widehat{\gamma}_3 \widehat{\text{SR}} + \frac{\widehat{\gamma}_4 - 1}{4}\widehat{\text{SR}}^2}}\right)$$
- If an AI tested 500 combinations to find one with Sharpe 2.0, the DSR will adjust the p-value.
- **Passing Criterion:** $p\text{-value} < 0.05$.

### Gate 5: Asymmetric Tail Risk / Profit Factor
- **Passing Criterion:** Profit Factor $\ge 1.50$ AND Max Single-Trade Loss $\le 3.0\%$ of portfolio equity.

---

## 3. Deterministic Verdicts in HANDOFF.md
- **`PASS: VERIFIED_ROBUST`**: All 5 gauntlet tests passed with Exit Code 0. Promoted to Paper Trading pool.
- **`FAIL: KILLED_OVERFIT`**: Failed WFO or DSR test. Detailed failure log written to `00_Brain/memory/lessons/`.
