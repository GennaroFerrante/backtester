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
