---
name: trading-data-harvester
description: Zero-cost historical data acquisition across crypto, equities, and macro economic series with lossless parquet/sqlite local caching and automatic deduplication.
---

# Trading Data Harvester Skill

## 1. Zero-Cost Historical Data Sources ($0.00 Policy)
In compliance with the Zero-Capital Policy, we never pay for expensive Bloomberg, Refinitiv, or Glassnode enterprise licenses. We harness verified, free, institutional-grade public archives:

1. **Binance Public Historical Data Archive (Crypto):**
   - Direct HTTP zip downloads from `data.binance.vision` (monthly and daily OHLCV klines, trades, and orderbook metrics back to 2017).
   - Cost: $0.00. No API key required.
2. **Yahoo Finance / Stooq Public API (Equities & Indices):**
   - Daily and hourly OHLCV bars for S&P 500, NASDAQ, sector ETFs, gold, oil, currencies.
   - Cost: $0.00.
3. **Federal Reserve Economic Data (FRED / Public St. Louis Fed):**
   - Macro interest rates (Fed Funds), CPI inflation, M2 Money Supply, Yield Curve (10Y-2Y spread), unemployment.
   - Cost: $0.00.
4. **SEC EDGAR Public Submissions (Fundamental & News):**
   - 10-K, 10-Q, 8-K filings and corporate insider trades.
   - Cost: $0.00.

---

## 2. Storage & Memory Architecture (Portability First)
To avoid filling disk space and breaking git portability:
- **Never commit massive raw CSVs to Git:** `.gitignore` must ignore `data/raw/` and `data/cache/`.
- **High-Performance Storage Format:** All downloaded OHLCV data is parsed and stored in compressed **Apache Parquet (`.parquet`)** or **SQLite (`.db`) with WAL mode**:
  - `snappy` or `zstd` compression reduces disk usage by 85–90% compared to raw CSV.
  - Sub-millisecond indexed queries by timestamp: `WHERE timestamp >= ? AND timestamp <= ?`.
- **Deduplication:** Automatic check prevents re-downloading existing date ranges.

---

## 3. Standard OHLCV Schema
Every ingested bar MUST conform to the normalized schema:

| Column | Type | Description |
| :--- | :--- | :--- |
| `timestamp` | `int64` | Unix Epoch timestamp in milliseconds (UTC) |
| `datetime` | `string` | ISO 8601 formatted datetime (e.g. `2026-11-20T12:00:00Z`) |
| `open` | `float64` | Open price for the bar |
| `high` | `float64` | Highest traded price during the interval |
| `low` | `float64` | Lowest traded price during the interval |
| `close` | `float64` | Final execution price for the bar |
| `volume` | `float64` | Total base asset volume traded |
| `quote_volume` | `float64` | Total quote asset volume traded (USD/USDT) |
| `trades_count` | `int32` | Number of individual fill transactions |

---

## 4. Portability & Integrity Verification
```bash
# Verifies data integrity, checks for missing timestamp gaps, and confirms zero corruption
python 05_Trading_AI/scripts/data_harvester.py --check-integrity
```
