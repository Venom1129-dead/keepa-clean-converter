---
name: trading-paper-executor
description: Zero-risk simulated live paper execution on official exchange testnets with sub-second order management, execution latency logging, and slippage verification.
---

# Trading Paper Executor Skill

## 1. Zero-Risk Validation Phase ($0.00 Capital Risk)
Before putting a single real dollar into any algorithm, it must trade live on public testnets for a minimum of **14 consecutive calendar days** or **50 live executions**:
- **Alpaca Markets Paper Trading (Equities & Crypto):** Free instant paper keys, zero deposit required.
- **Binance Futures Testnet (Crypto):** Free public testnet with 15,000 USDT mock balance.
- **Bybit Testnet (Derivatives):** Free mock funds.

---

## 2. Order Execution Architecture
- **Order Types:**
  - Post-Only Limit Orders for maker fee capture (`0.02%` rebate or low fee).
  - Immediate-or-Cancel (IOC) for time-critical momentum fills.
  - Bracket Orders: Every entry order is atomically accompanied by a Stop-Loss and Take-Profit order submitted to the exchange matching engine.
- **WebSocket State Machine:**
  - Subscribes to live Level-2 orderbook (`depthUpdate`) and user data streams (`executionReport`).
  - Tracks fill latency: Measures time from signal emission to exchange ACK (target: $< 80\text{ ms}$).

---

## 3. Discrepancy Auditing (Backtest vs Live Paper)
The executor calculates the **Execution Tracking Error**:
$$\text{Tracking Error} = \text{Paper Return} - \text{Backtest Expected Return}$$
If live paper trading yields $> 1.5\%$ worse returns than the backtest over 50 trades, trading is immediately paused to investigate execution slippage, hidden latency, or adverse selection.

---

## 4. Portability & Mock Mode
When offline or on a machine without network access, the executor automatically falls back to `MockExchangeClient` running entirely in memory, ensuring that verification suites (`python 05_Trading_AI/verifier/test_executor.py`) run with Exit Code 0 anywhere.
