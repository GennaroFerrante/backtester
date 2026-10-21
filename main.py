import yfinance
import pandas as pd
from abc import ABC, abstractmethod

#Program gets historical stock data, and backtests different strategies with changeable parameters

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
            
class Backtest:
    def __init__(self, prices, strategy, start=0):
        self.prices = prices
        self.strategy = strategy
        self.start = start

    def run(self):
        signals = self.strategy.generate_signals(self.prices)
        positions = signals.shift(1).fillna(0)
        daily_returns = self.prices.pct_change()
        strategy_returns = positions.shift(1) * daily_returns

        # only count from the start day onward
        strategy_returns = strategy_returns.iloc[self.start:]
        positions = positions.iloc[self.start:]

        total = (1 + strategy_returns.fillna(0)).prod() - 1
        return float(total * 100), float(positions.sum())

ticker = "SPY"
all_data = yfinance.download(ticker, "2010-01-01", "2026-10-10")
close_prices = all_data["Close"][ticker]
start = 202
strategies = {
    "Mean reversion": MeanReversion(50, 200, 0.99),
    "MA crossover": MovingAverageCrossover(50, 200),
    "Trend filter": TrendFilter(200),
    "RSI": RelativeStrengthIndex(),
}

for name, strategy in strategies.items():
    total_return, days_invested = Backtest(close_prices, strategy, start=start).run()
    print(str(name) + " returned " + str(round(total_return, 2)) + "% over " + str(days_invested) + " days invested")

bah = (float(close_prices.iloc[-1] / close_prices.iloc[start - 1]) - 1) * 100
print("Buy and Hold returned " + str(round(bah, 2)) + "% over " + str(len(close_prices)) + " days invested")