---
name: trading-backtest-engine
description: Institutional-grade vectorized and event-driven historical backtesting engine with realistic slippage, maker/taker fees, order queue modeling, and strict zero-lookahead bias prevention.
---

# Trading Backtest Engine Skill

## 1. Core Principles: Preventing Backtest Delusions
99% of retail backtests show stellar profits because of hidden flaws:
1. **Lookahead Bias (Peeking into Future):** Using bar close data before the bar has completed, or calculating moving averages using `close[t]` to enter at `open[t]`.
2. **Zero Friction Delusion:** Assuming zero slippage, zero commission, and instant execution at the exact tick price.
3. **Survivorship Bias:** Testing only on coins or stocks that survived and pumped, ignoring those that went to zero or were delisted.
4. **Overfitting / Curve-Fitting:** Testing 10,000 parameter combinations until one randomly performs well in-sample.

This skill defines the strict deterministic protocol to eliminate all four flaws.

---

## 2. Friction & Execution Modeling Rules
Every backtest MUST deduct realistic trading costs:
- **Exchange Fees:**
  - Maker Fee: `0.02%` to `0.04%` (limit orders).
  - Taker Fee: `0.05%` to `0.075%` (market/stop orders).
- **Slippage Model:**
  - High Liquidity (BTC/ETH, Mega-cap Tech): `0.02%` to `0.05%` per execution.
  - Mid/Low Liquidity (Altcoins, Small-caps): `0.10%` to `0.35%` per execution.
  - High Volatility Spikes (CPI/FOMC news releases): `0.50%` to `1.50%` slippage penalty.
- **Borrow / Financing Costs:**
  - Funding rate deductions on perpetual futures (every 8 hours).
  - Margin interest on short equity positions.

---

## 3. Mathematical Metric Verification
Every backtested strategy must output the following quantitative scorecard:

```
======================================================================
                   EMPIRICAL BACKTEST SCORECARD
======================================================================
Strategy ID            : STRAT_001_EMA_CROSS_RSI
Sample Period          : 2022-01-01 -> 2026-11-20 (1,784 Days)
Total Trades (N)       : 412 trades (Min requirement: N >= 100)
----------------------------------------------------------------------
Win Rate (Accuracy)    : 54.37% (224 Wins / 188 Losses)
Profit Factor          : 1.84 (Gross Profits / Gross Losses)
Expected Value (EV)    : +$142.30 per trade (0.71% return per trade)
Max Drawdown (MDD)     : -14.2% (Peak-to-trough capital decline)
Sharpe Ratio (Ann.)    : 2.14 (Risk-free benchmark: 4.5% US T-Bill)
Sortino Ratio (Ann.)   : 3.42 (Penalizes only downside volatility)
Calmar Ratio           : 2.38 (Annualized Return / Max Drawdown)
----------------------------------------------------------------------
Statistical Significance:
T-Statistic            : 3.82 (p-value < 0.001 -> Statistically Significant)
Permutation Test (1000): Beat 98.4% of randomized price shuffles
======================================================================
```

---

## 4. Execution Step Verification
```bash
# Deterministic verification of the backtesting engine
python 05_Trading_AI/verifier/test_backtest_engine.py
```
- Must run in < 2.0 seconds using vector math (NumPy / Pandas arrays).
- Must match mathematically proven closed-form ground truths (e.g. perfect single-trade calculations).
