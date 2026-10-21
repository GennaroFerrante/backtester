from abc import ABC, abstractmethod
import pandas as pd

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, prices: pd.Series):
        """Return 1 (holding) or 0 (in cash) for each day."""

class MovingAverageCrossover(Strategy):
    def __init__(self, short_period, long_period):
        self.short_period = short_period
        self.long_period = long_period

    def generate_signals(self, prices):
        short_avg = prices.rolling(self.short_period).mean()
        long_avg = prices.rolling(self.long_period).mean()
        return (short_avg > long_avg).astype(int)

class MeanReversion(Strategy):
    def __init__(self, short_period, long_period, buy_point):
        self.short_period = short_period
        self.long_period = long_period
        self.buy_point = buy_point

    def generate_signals(self, prices):
        long_avg = prices.rolling(self.long_period).mean()
        short_avg = prices.rolling(self.short_period).mean()
        signals = [0]
        holding = False

        for i in range(1, len(prices)):
            if short_avg.iloc[i] < long_avg.iloc[i] * self.buy_point and short_avg.iloc[i - 1] > long_avg.iloc[i - 1] * self.buy_point and not holding:
                holding = True
            if short_avg.iloc[i] > long_avg.iloc[i] and holding:
                holding = False
            if holding:
                signals.append(1)
            elif not holding:
                signals.append(0)

        return pd.Series(signals, index=prices.index)

class TrendFilter(Strategy):
    def __init__(self, long_period):
        self.long_period = long_period

    def generate_signals(self, prices):
        long_avg = prices.rolling(self.long_period).mean()
        return (prices > long_avg).astype(int)

class RelativeStrengthIndex(Strategy):
    def __init__(self, lookback=14, buy_threshold=30, sell_threshold=70):
        self.lookback = lookback
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

    def calculate_rsi(self, prices):
        rsi_values = [float("nan")] * len(prices)
        avg_gain = avg_loss = 0.0

        for i in range(1, len(prices)):
            change = float(prices.iloc[i] - prices.iloc[i - 1])
            gain = max(change, 0)
            loss = max(-change, 0)

            if i <= self.lookback:
                avg_gain += gain/self.lookback
                avg_loss += loss/self.lookback
                if i < self.lookback:
                    continue
            elif i > self.lookback:
                avg_gain = ((avg_gain * (self.lookback - 1)) + gain) / self.lookback
                avg_loss = ((avg_loss * (self.lookback - 1)) + loss) / self.lookback

            if avg_loss == 0:
                rsi_values[i] = 100
            else:
                rs = avg_gain / avg_loss
                rsi_values[i] = 100 - 100 / (1 + rs)
        return pd.Series(rsi_values, index=prices.index)
    
    def generate_signals(self, prices):
        rsi = self.calculate_rsi(prices)
        signals = []
        holding = False

        for value in rsi:
            if pd.isna(value):
                signals.append(0)
                continue
            if value < self.buy_threshold and not holding:
                holding = True
            if value > self.sell_threshold and holding:
                holding = False
            if holding:
                signals.append(1)
            else:
                signals.append(0)

        return pd.Series(signals, index=prices.index)