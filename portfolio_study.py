from strategies import BuyAndHold, MovingAverageCrossover, TrendFilter, MeanReversion, CombinedStrategy
from engine import Backtest
from data import load_prices
from metrics import total_return, annualized_return, annualized_volatility, sharpe_ratio, max_drawdown
import pandas as pd

markets = ["SPY", "IWM", "EFA", "TLT"]
periods = [("2000-01-01", "2010-12-31"), ("2010-01-01", "2026-10-20")]
start, cost = 202, 0.001
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

strategies = {
    "Buy and hold": BuyAndHold(),
    "Trend filter": TrendFilter(200),
    "MA crossover": MovingAverageCrossover(50, 200),
    "Mean reversion + Trend filter": CombinedStrategy([MeanReversion(50, 200, 0.99), TrendFilter(200)]),
}

for start_date, end_date in periods:
    returns = {}
    for market in markets:
        prices = load_prices(market, start_date, end_date)
        for name, strategy in strategies.items():
            result = Backtest(prices, strategy, start=start, cost=cost).run()
            returns[(name, market)] = result["returns"].rename(market)
            
        portfolios = {name: {m: name for m in markets} for name in strategies}
        portfolios["Trend filter on stocks, hold TLT"] = {
        "SPY": "Trend filter", "IWM": "Trend filter", "EFA": "Trend filter", "TLT": "Buy and hold"}
        rows = {}
    for label, choices in portfolios.items():
        combined = pd.concat([returns[(name, m)] for m, name in choices.items()], axis=1).dropna()
        daily = combined.mean(axis=1)
        rows[label] = {
            "Total Return": total_return(daily),
            "Annualized Return": annualized_return(daily),
            "Annualized Volatility": annualized_volatility(daily),
            "Sharpe Ratio": sharpe_ratio(daily),
            "Max Drawdown": max_drawdown(daily),
            "First Date": daily.index[0].date(),
        }

    table = pd.DataFrame.from_dict(rows, orient="index")
    print(f"\nPortfolio {start_date[:4]}-{end_date[:4]}")
    print(table.round(3))