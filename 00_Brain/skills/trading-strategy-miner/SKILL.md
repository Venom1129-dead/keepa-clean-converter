---
name: trading-strategy-miner
description: Systematic mining, extraction, and normalization of crowdsourced trading ideas, PineScript indicators, GitHub algos, and academic finance papers into deterministic testable strategies.
---

# Trading Strategy Miner Skill

## 1. Purpose & Core Thesis
The internet is flooded with trading ideas, PineScript scripts, indicator combinations, and forum strategies. Most retail traders fail because they believe claims without rigorous testing.
This skill provides the automated protocol to:
1. Ingest trading ideas from public repositories, PineScript open-source scripts, TradingView strategies, and financial forums.
2. Strip away hype and qualitative vague statements.
3. Translate concepts into an exact, standardized JSON/Python specification:
   - `entry_long_conditions`
   - `entry_short_conditions`
   - `exit_profit_conditions`
   - `stop_loss_conditions`
   - `parameter_grid`

---

## 2. Standardized Strategy Specification Schema (`strategy_spec.json`)
Every mined idea must be normalized into this strict schema before reaching the backtest engine:

```json
{
  "strategy_id": "STRAT_2026_001_EMA_CROSS_RSI_FILTER",
  "name": "Triple EMA Trend with RSI Oversold Reversal Filter",
  "source_origin": "TradingView PineScript / GitHub Public Repo",
  "asset_classes": ["CRYPTO", "EQUITIES", "FOREX"],
  "timeframes": ["15m", "1h", "4h", "1d"],
  "indicators_required": [
    {"name": "EMA", "params": {"period_fast": 9, "period_mid": 21, "period_slow": 55}},
    {"name": "RSI", "params": {"period": 14, "oversold": 35, "overbought": 65}},
    {"name": "ATR", "params": {"period": 14}}
  ],
  "entry_rules": {
    "long": "close > EMA_55 and EMA_9 crosses_above EMA_21 and RSI > 45 and RSI < 65",
    "short": "close < EMA_55 and EMA_9 crosses_below EMA_21 and RSI < 55 and RSI > 35"
  },
  "exit_rules": {
    "take_profit_atr_multiple": 2.5,
    "stop_loss_atr_multiple": 1.25,
    "trailing_stop": true,
    "max_bars_in_trade": 48
  },
  "hypothesis": "Captures established trend continuation while avoiding late-stage exhaustion entries."
}
```

---

## 3. Mining Vectors & Sources
1. **GitHub Algorithmic Repositories:**
   - Search queries: `topic:algorithmic-trading`, `topic:backtesting-strategies`, `pinescript-strategies`.
   - Focus on repositories with testable logic rather than machine learning black boxes.
2. **PineScript Standard Library:**
   - Deconstruct core components: Donchian Channel Breakouts, SuperTrend, Bollinger Band Squeeze, MACD Zero-Lag, Volume Profile Value Area.
3. **Quantitative Academic Finance:**
   - Momentum Anomalies (Jegadeesh & Titman).
   - Short-Term Mean Reversion (Lehman).
   - Post-Earnings Announcement Drift (PEAD).
   - Funding Rate & Basis Arbitrage in Perpetual Futures.

---

## 4. Normalization Invariants
- **No Discretionary Ambiguity:** If a strategy says "look for bullish momentum", it must be converted to an exact mathematical formula (e.g. `ROC(10) > 1.5%` or `ADX(14) > 25`).
- **Parameter Decoupling:** Parameters must never be hardcoded into the execution logic; they must be exposed as configurable grid arrays for out-of-sample testing.
