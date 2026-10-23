from strategies import MeanReversion, MovingAverageCrossover, TrendFilter, RelativeStrengthIndex, BuyAndHold
from engine import Backtest
from data import close_prices
from plots import plot_results

start = 202
strategies = {
    "Buy and hold": BuyAndHold(),
    "Mean reversion": MeanReversion(50, 200, 0.99),
    "MA crossover": MovingAverageCrossover(50, 200),
    "Trend filter": TrendFilter(200),
    "RSI": RelativeStrengthIndex(),
}

# header row
print(f"{'Strategy':15} {'Total':>9} {'Annual':>8} {'Vol':>7} {'Sharpe':>7} {'Max DD':>8} {'Days':>6}")
print("-" * 66)

all_returns = {}

for name, strategy in strategies.items():
    r = Backtest(close_prices, strategy, start=start).run()
    if name == "MA crossover" or name == "Buy and hold":
        all_returns[name] = r["returns"]
    print(f"{name:15} "
          f"{r['total_return']:9.1%} "
          f"{r['annualized_return']:8.1%} "
          f"{r['annualized_volatility']:7.1%} "
          f"{r['sharpe_ratio']:7.2f} "
          f"{r['max_drawdown']:8.1%} "
          f"{r['days_invested']:6.0f}")

plot_results(all_returns)