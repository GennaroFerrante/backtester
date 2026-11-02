from strategies import TrendFilter, MovingAverageCrossover, BuyAndHold
from engine import Backtest
from data import load_prices
import matplotlib.pyplot as plt
import pandas as pd

market = "SPY"
periods = [("2000-01-01", "2010-12-31"), ("2010-01-01", "2026-10-20")]

for period in periods:
    close_prices = load_prices(market, period[0], period[1])
    start = 302
    cost = 0.001
    bah_sharpe = Backtest(close_prices, BuyAndHold(), start=start, cost=cost).run()["sharpe_ratio"]
    tf_rows = []

    for i in range(50, 301, 10):
        r = Backtest(close_prices, TrendFilter(i), start=start, cost=cost).run()
        tf_rows.append({"window": i, "sharpe": r["sharpe_ratio"],
                        "max_drawdown": r["max_drawdown"], "trades": r["trades"]})
    tf = pd.DataFrame(tf_rows)

    fig, ax = plt.subplots()
    ax.plot(tf["window"], tf["sharpe"], marker="o", label="Trend filter")
    ax.axhline(bah_sharpe, linestyle="--", color="gray", label="Buy and hold")
    ax.set_xlabel("Window (days)")
    ax.set_ylabel("Sharpe ratio")
    ax.legend()

    plt.show()

    mac_rows = []

    for i in range(100, 301, 10):
        for j in range(10, 100, 10):
            if j < i:
                result = Backtest(close_prices, MovingAverageCrossover(j, i), start=start, cost=cost).run()
                mac_rows.append({"short": j, "long": i, "sharpe": result["sharpe_ratio"]})

    df = pd.DataFrame(mac_rows)
    if period == ("2000-01-01", "2010-12-31"):
        tf.to_csv("2000-2010_sweep_TF.csv", index=False)
        df.to_csv("2000-2010_sweep_MAC.csv", index=False)
    if period == ("2010-01-01", "2026-10-20"):
        tf.to_csv("2010-2026_sweep_TF.csv", index=False)
        df.to_csv("2010-2026_sweep_MAC.csv", index=False)

    grid = df.pivot(index="short", columns="long", values="sharpe")

    fig, ax = plt.subplots(figsize=(10, 5))
    image = ax.imshow(grid, cmap="viridis", aspect="auto", origin="lower")
    ax.set_xticks(range(len(grid.columns)), grid.columns)
    ax.set_yticks(range(len(grid.index)), grid.index)
    ax.set_xlabel("Long window (days)")
    ax.set_ylabel("Short window (days)")
    fig.colorbar(image, ax=ax, label="Sharpe ratio")
    plt.show()