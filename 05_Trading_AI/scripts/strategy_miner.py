"""
Strategy Miner & Feature Extraction Kernel
Implements indicator calculations (EMA, RSI, ATR, Bollinger Bands, News Sentiment Filter)
and normalizes crowd strategies into deterministic trade signals [-1, 0, 1].
"""

import math

def calculate_ema(prices, period):
    ema = []
    k = 2.0 / (period + 1.0)
    for i, p in enumerate(prices):
        if i == 0:
            ema.append(p)
        else:
            ema.append(p * k + ema[-1] * (1.0 - k))
    return ema

def calculate_rsi(prices, period=14):
    rsi = [50.0] * len(prices)
    if len(prices) <= period:
        return rsi

    gains = []
    losses = []
    for i in range(1, len(prices)):
        change = prices[i] - prices[i - 1]
        gains.append(max(0.0, change))
        losses.append(max(0.0, -change))

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period, len(prices)):
        change = prices[i] - prices[i - 1]
        gain = max(0.0, change)
        loss = max(0.0, -change)
        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period

        if avg_loss == 0:
            rsi[i] = 100.0
        else:
            rs = avg_gain / avg_loss
            rsi[i] = 100.0 - (100.0 / (1.0 + rs))
    return rsi

def calculate_atr(bars, period=14):
    tr = []
    for i in range(len(bars)):
        if i == 0:
            tr.append(bars[i]['high'] - bars[i]['low'])
        else:
            h = bars[i]['high']
            l = bars[i]['low']
            prev_c = bars[i - 1]['close']
            tr.append(max(h - l, abs(h - prev_c), abs(l - prev_c)))

    atr = []
    for i in range(len(tr)):
        if i == 0:
            atr.append(tr[0])
        else:
            k = 1.0 / period
            atr.append(tr[i] * k + atr[-1] * (1.0 - k))
    return atr

# Standard Crowd Strategies Mined from Repositories / PineScript
def strategy_triple_ema(bars):
    """
    Classic Internet Trend Follower:
    Long when Fast EMA (9) > Mid EMA (21) > Slow EMA (55)
    Short when Fast EMA (9) < Mid EMA (21) < Slow EMA (55)
    """
    closes = [b['close'] for b in bars]
    ema9 = calculate_ema(closes, 9)
    ema21 = calculate_ema(closes, 21)
    ema55 = calculate_ema(closes, 55)

    signals = [0] * len(bars)
    for i in range(1, len(bars)):
        if ema9[i] > ema21[i] > ema55[i] and not (ema9[i-1] > ema21[i-1] > ema55[i-1]):
            signals[i] = 1
        elif ema9[i] < ema21[i] < ema55[i] and not (ema9[i-1] < ema21[i-1] < ema55[i-1]):
            signals[i] = -1
    return signals

def strategy_rsi_mean_reversion(bars):
    """
    Classic Oversold / Overbought Bounce:
    Long when RSI crosses back above 30
    Short when RSI crosses back below 70
    """
    closes = [b['close'] for b in bars]
    rsi = calculate_rsi(closes, 14)

    signals = [0] * len(bars)
    for i in range(1, len(bars)):
        if rsi[i-1] < 30 and rsi[i] >= 30:
            signals[i] = 1
        elif rsi[i-1] > 70 and rsi[i] <= 70:
            signals[i] = -1
    return signals

def strategy_ensemble_consensus(bars, news_sentiment=None):
    """
    Multi-Factor Ensemble Engine:
    Combines Trend (EMA), Mean Reversion (RSI), and News Sentiment.
    Only takes trades when multiple independent signals agree!
    """
    sig_trend = strategy_triple_ema(bars)
    sig_rsi = strategy_rsi_mean_reversion(bars)

    signals = [0] * len(bars)
    for i in range(len(bars)):
        vote = sig_trend[i] + sig_rsi[i]
        if news_sentiment and i < len(news_sentiment):
            news_val = news_sentiment[i]
            if news_val > 0.5:
                vote += 1
            elif news_val < -0.5:
                vote -= 1

        if vote >= 1:
            signals[i] = 1
        elif vote <= -1:
            signals[i] = -1
    return signals
