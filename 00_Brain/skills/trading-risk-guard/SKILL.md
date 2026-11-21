---
name: trading-risk-guard
description: Dynamic risk management, fractional Kelly position sizing, ATR-based trailing stops, volatility parity, and catastrophic drawdown kill-switches.
---

# Trading Risk Guard & Capital Protection Skill

## 1. Capital Preservation Invariant
Rule #1: Never risk ruin.
Even a system with a 70% win rate will go bankrupt if position sizing is too aggressive.
This skill enforces mathematical, algorithmic risk management before any order is submitted.

---

## 2. Dynamic Position Sizing Algorithms

### 1. Fractional Kelly Criterion ($f^*$)
$$\text{Kelly Fraction} = \frac{p \cdot b - q}{b}$$
Where:
- $p$ = Historical win rate
- $q = 1 - p$ (Loss rate)
- $b$ = Win/Loss payoff ratio ($\frac{\text{Average Win}}{\text{Average Loss}}$)

**Invariant:** To protect against regime shifts and drawdown clustering, we use **Quarter-Kelly ($0.25 \times f^*$)** or **Half-Kelly ($0.5 \times f^*$)**, capped at a maximum of **2.0% equity risk per trade**.

### 2. ATR Volatility Parity Sizing
Position size scales inversely with market volatility:
$$\text{Units} = \frac{\text{Account Equity} \times \text{Risk \%}}{\text{ATR}(14) \times \text{Multiplier}}$$
- In quiet market regimes (low ATR), position size expands safely.
- In violent market crashes (high ATR), position size contracts automatically to prevent slippage wipeouts.

---

## 3. Circuit Breakers & Emergency Kill-Switches
Every running algorithm must be wired to the hardware risk guard:
1. **Daily Max Loss Limit (Circuit Breaker):** If cumulative daily losses reach **-3.0%** of account equity, all open positions are flattened immediately and trading is halted until the next UTC day.
2. **Weekly Drawdown Cap:** If weekly drawdown exceeds **-6.0%**, the system goes into `IDLE_COOLDOWN` mode for 48 hours to prevent tilt.
3. **Correlation Risk Ceiling:** The system will never hold more than 3 simultaneous positions with a 30-day price correlation $> 0.70$ (e.g. BTC, ETH, and SOL all long together).
4. **Exchange Outage / API Disconnect Watchdog:** If WebSocket heartbeat is lost for $> 15$ seconds, pending orders are cancelled and defensive stops remain pinned on the exchange book.
