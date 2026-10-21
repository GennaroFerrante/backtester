from strategies import MeanReversion, MovingAverageCrossover, TrendFilter, RelativeStrengthIndex
from engine import Backtest
from data import close_prices

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