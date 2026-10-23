from metrics import total_return, annualized_return, annualized_volatility, sharpe_ratio, max_drawdown


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
        return {
            "total_return": total_return(strategy_returns),
            "annualized_return": annualized_return(strategy_returns),
            "annualized_volatility": annualized_volatility(strategy_returns),
            "sharpe_ratio": sharpe_ratio(strategy_returns),
            "max_drawdown": max_drawdown(strategy_returns),
            "days_invested": float(positions.sum()),
            "returns" : strategy_returns
        }
