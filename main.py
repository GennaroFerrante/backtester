from strategies import (BuyAndHold, MeanReversion, MovingAverageCrossover,
                        TrendFilter, RelativeStrengthIndex, CombinedStrategy)
from engine import Backtest
from plots import plot_results
from data import load_prices
import itertools

start = 202
cost = 0.001
close_prices = load_prices("SPY", "2000-01-01", "2010-12-31")

strategies_excluding_BAH = {
    "Mean reversion": MeanReversion(50, 200, 0.99),
    "MA crossover": MovingAverageCrossover(50, 200),
    "Trend filter": TrendFilter(200),
    "RSI": RelativeStrengthIndex(),
}

header = (f"{'Strategy':45} {'Total':>9} {'Annual':>8} {'Vol':>7} "
          f"{'Sharpe':>7} {'Max DD':>8} {'Days':>6} {'Trades':>7}")


def print_row(label, r):
    print(f"{label:45} "
          f"{r['total_return']:9.1%} "
          f"{r['annualized_return']:8.1%} "
          f"{r['annualized_volatility']:7.1%} "
          f"{r['sharpe_ratio']:7.2f} "
          f"{r['max_drawdown']:8.1%} "
          f"{r['days_invested']:6.0f} "
          f"{r['trades']:7.0f}")

all_returns = {}

print(header)
print("-" * len(header))

bah = Backtest(close_prices, BuyAndHold(), start=start, cost=cost).run()
print_row("Buy and hold", bah)
all_returns["Buy and hold"] = bah["returns"]

for size in range(1, 4):
    print("-" * len(header))
    for combo in itertools.combinations(strategies_excluding_BAH.items(), size):
        label = " + ".join(name for name, strategy in combo)
        combined = CombinedStrategy([strategy for name, strategy in combo])
        result = Backtest(close_prices, combined, start=start, cost=cost).run()
        print_row(label, result)
        all_returns[label] = result["returns"]

#plot_results({name: all_returns[name] for name in
              #["Buy and hold", "Trend filter", "Trend filter + RSI", "Mean reversion + Trend filter", "Mean reversion + Trend filter + RSI"]})