"""
Vectorized & Event-Driven Historical Backtesting Engine
Deterministic evaluation of crowd trading strategies, technical indicators, and news signals.
Includes realistic slippage, maker/taker fees, and Sharpe/Sortino/Drawdown metrics.
"""

import math
import json
import os

class BacktestEngine:
    def __init__(self, initial_capital=10000.0, maker_fee=0.0002, taker_fee=0.0005, slippage=0.0005):
        self.initial_capital = float(initial_capital)
        self.maker_fee = float(maker_fee)
        self.taker_fee = float(taker_fee)
        self.slippage = float(slippage)

    def run_backtest(self, bars, signals, risk_per_trade=0.02, atr_stop_mult=2.0, take_profit_mult=3.0):
        """
        bars: list of dicts [{'timestamp', 'open', 'high', 'low', 'close', 'volume', 'atr'}]
        signals: list of ints [0 (neutral), 1 (long), -1 (short)] aligned with bars
        """
        capital = self.initial_capital
        equity_curve = [capital]
        trades = []
        position = None  # {'type': 'LONG'/'SHORT', 'entry_price', 'shares', 'stop_loss', 'take_profit', 'entry_idx'}

        n_bars = len(bars)
        if n_bars == 0 or len(signals) != n_bars:
            raise ValueError("Bars and signals must be non-empty and matching in length.")

        for i in range(1, n_bars):
            bar = bars[i]
            prev_bar = bars[i - 1]
            sig = signals[i - 1]  # Signal generated at close of previous bar, executed at open of current bar (zero lookahead)
            open_price = bar['open']
            atr = bar.get('atr', open_price * 0.02)

            # 1. Manage active position exit conditions
            if position is not None:
                pos_type = position['type']
                exit_price = None
                exit_reason = None

                # Check Stop Loss / Take Profit against bar's High / Low
                if pos_type == 'LONG':
                    if bar['low'] <= position['stop_loss']:
                        exit_price = position['stop_loss'] * (1.0 - self.slippage)
                        exit_reason = 'STOP_LOSS'
                    elif bar['high'] >= position['take_profit']:
                        exit_price = position['take_profit'] * (1.0 - self.slippage)
                        exit_reason = 'TAKE_PROFIT'
                    elif sig == -1:  # Reverse signal
                        exit_price = open_price * (1.0 - self.slippage)
                        exit_reason = 'SIGNAL_REVERSE'

                elif pos_type == 'SHORT':
                    if bar['high'] >= position['stop_loss']:
                        exit_price = position['stop_loss'] * (1.0 + self.slippage)
                        exit_reason = 'STOP_LOSS'
                    elif bar['low'] <= position['take_profit']:
                        exit_price = position['take_profit'] * (1.0 + self.slippage)
                        exit_reason = 'TAKE_PROFIT'
                    elif sig == 1:  # Reverse signal
                        exit_price = open_price * (1.0 + self.slippage)
                        exit_reason = 'SIGNAL_REVERSE'

                if exit_price is not None:
                    # Execute Exit
                    gross_pnl = (exit_price - position['entry_price']) * position['shares'] if pos_type == 'LONG' else (position['entry_price'] - exit_price) * position['shares']
                    fee = (position['entry_price'] * position['shares'] * self.taker_fee) + (exit_price * position['shares'] * self.taker_fee)
                    net_pnl = gross_pnl - fee
                    capital += net_pnl
                    trades.append({
                        'type': pos_type,
                        'entry_idx': position['entry_idx'],
                        'exit_idx': i,
                        'entry_price': position['entry_price'],
                        'exit_price': exit_price,
                        'shares': position['shares'],
                        'gross_pnl': gross_pnl,
                        'fee': fee,
                        'net_pnl': net_pnl,
                        'exit_reason': exit_reason
                    })
                    position = None

            # 2. Check for new position entry
            if position is None and sig != 0 and capital > 100.0:
                stop_dist = max(atr * atr_stop_mult, open_price * 0.005)
                risk_amount = capital * risk_per_trade
                shares = risk_amount / stop_dist

                if sig == 1:  # LONG
                    entry_price = open_price * (1.0 + self.slippage)
                    stop_loss = entry_price - stop_dist
                    take_profit = entry_price + (stop_dist * take_profit_mult)
                    position = {
                        'type': 'LONG',
                        'entry_idx': i,
                        'entry_price': entry_price,
                        'shares': shares,
                        'stop_loss': stop_loss,
                        'take_profit': take_profit
                    }
                elif sig == -1:  # SHORT
                    entry_price = open_price * (1.0 - self.slippage)
                    stop_loss = entry_price + stop_dist
                    take_profit = entry_price - (stop_dist * take_profit_mult)
                    position = {
                        'type': 'SHORT',
                        'entry_idx': i,
                        'entry_price': entry_price,
                        'shares': shares,
                        'stop_loss': stop_loss,
                        'take_profit': take_profit
                    }

            equity_curve.append(capital)

        # Calculate institutional metrics
        metrics = self._calculate_metrics(trades, equity_curve)
        return {
            'initial_capital': self.initial_capital,
            'final_capital': capital,
            'equity_curve': equity_curve,
            'trades': trades,
            'metrics': metrics
        }

    def _calculate_metrics(self, trades, equity_curve):
        n_trades = len(trades)
        if n_trades == 0:
            return {
                'total_trades': 0,
                'win_rate': 0.0,
                'profit_factor': 0.0,
                'total_return_pct': 0.0,
                'max_drawdown_pct': 0.0,
                'sharpe_ratio': 0.0,
                'sortino_ratio': 0.0
            }

        wins = [t['net_pnl'] for t in trades if t['net_pnl'] > 0]
        losses = [abs(t['net_pnl']) for t in trades if t['net_pnl'] <= 0]

        win_rate = (len(wins) / n_trades) * 100.0
        gross_profit = sum(wins)
        gross_loss = sum(losses)
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else (999.0 if gross_profit > 0 else 0.0)

        total_return_pct = ((equity_curve[-1] - self.initial_capital) / self.initial_capital) * 100.0

        # Maximum Drawdown calculation
        peak = equity_curve[0]
        max_dd = 0.0
        for eq in equity_curve:
            if eq > peak:
                peak = eq
            dd = (peak - eq) / peak if peak > 0 else 0.0
            if dd > max_dd:
                max_dd = dd
        max_drawdown_pct = max_dd * 100.0

        # Per-trade returns for Sharpe & Sortino
        returns = [t['net_pnl'] / self.initial_capital for t in trades]
        mean_ret = sum(returns) / n_trades
        variance = sum((r - mean_ret) ** 2 for r in returns) / n_trades if n_trades > 1 else 0.0
        std_dev = math.sqrt(variance)

        # Downside deviation for Sortino
        downside_var = sum((min(0.0, r)) ** 2 for r in returns) / n_trades if n_trades > 1 else 0.0
        downside_std = math.sqrt(downside_var)

        sharpe = (mean_ret / std_dev * math.sqrt(252)) if std_dev > 0 else 0.0
        sortino = (mean_ret / downside_std * math.sqrt(252)) if downside_std > 0 else 0.0

        return {
            'total_trades': n_trades,
            'win_rate': round(win_rate, 2),
            'profit_factor': round(profit_factor, 2),
            'total_return_pct': round(total_return_pct, 2),
            'max_drawdown_pct': round(max_drawdown_pct, 2),
            'sharpe_ratio': round(sharpe, 2),
            'sortino_ratio': round(sortino, 2)
        }
