from strategies import (BuyAndHold, MeanReversion, MovingAverageCrossover,
                        TrendFilter, RelativeStrengthIndex, CombinedStrategy)
from engine import Backtest
from plots import plot_results
from data import load_prices
import pandas as pd
import itertools


markets = ["SPY", "QQQ", "IWM", "EFA", "TLT"]
periods = [("2000-01-01", "2010-12-31"), ("2010-01-01", "2026-10-20")]

for market in markets:
    for period in periods:
        close_prices = load_prices(market, period[0], period[1])
        start = 202
        cost = 0.001


        strategies_excluding_BAH = {
            "Mean reversion": MeanReversion(50, 200, 0.99),
            "MA crossover": MovingAverageCrossover(50, 200),
            "Trend filter": TrendFilter(200),
            "RSI": RelativeStrengthIndex(),
        }

        header = (f"{'Strategy':45} {'Total':>9} {'Annual':>8} {'Vol':>7} "
                f"{'Sharpe':>7} {'Max DD':>8} {'Days':>6} {'Trades':>7}")

        all_returns = {}

        bah = Backtest(close_prices, BuyAndHold(), start=start, cost=cost).run()
        all_returns["Buy and hold"] = bah["returns"]
        df = pd.DataFrame({'Total Return' : bah['total_return'], 'Annualized Return' : bah['annualized_return'], 
                        'Annualized Volatility' : bah['annualized_volatility'], 'Sharpe Ratio' : bah['sharpe_ratio'], 
                        'Max Drawdown' : bah['max_drawdown'], 'Days Invested' : bah['days_invested'], 'Trades' : bah['trades']}, 
                        index=["Buy and hold"])
        count = 0

        for size in range(1, 4):
            for combo in itertools.combinations(strategies_excluding_BAH.items(), size):
                label = " + ".join(name for name, strategy in combo)
                combined = CombinedStrategy([strategy for name, strategy in combo])
                result = Backtest(close_prices, combined, start=start, cost=cost).run()
                df.loc[len(df)] = {'Total Return' : result['total_return'], 'Annualized Return' : result['annualized_return'], 
                                'Annualized Volatility' : result['annualized_volatility'], 'Sharpe Ratio' : result['sharpe_ratio'], 
                                'Max Drawdown' : result['max_drawdown'], 'Days Invested' : result['days_invested'], 
                                'Trades' : result['trades']}
                
                new_index = list(df.index)
                new_index[count + 1] = label
                df.index = new_index
                all_returns[label] = result
                count += 1

        df[["Days Invested", "Trades"]] = df[["Days Invested", "Trades"]].astype(int)

        if period == ("2000-01-01", "2010-12-31"):
            df.round(4).to_csv(market + "_2000-2010_cost" + str(cost)+".csv")
        elif period == ("2010-01-01", "2026-10-20"):
            df.round(4).to_csv(market + "_2010-2026_cost" + str(cost)+".csv")

#plot_results({name: all_returns[name] for name in
              #["Buy and hold", "Trend filter", "Trend filter + RSI", "Mean reversion + Trend filter", "Mean reversion + Trend filter + RSI"]})