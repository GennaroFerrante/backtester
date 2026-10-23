# Backtester

A Python tool for testing stock trading strategies on historical data and
comparing them against buying and holding.

## Features
- Downloads daily historical prices with yfinance
- Four strategies:
  - **Mean reversion:** buys when the short moving average falls a set
    percentage below the long one, sells when it recovers
  - **Moving average crossover:** holds while the short average is above the long one
  - **Trend filter:** holds while the price is above its long moving average
  - **RSI:** buys when the Relative Strength Index drops below 30, sells above 70
- Shared backtest engine reporting total return and days invested
- All strategies compared to buy-and-hold over the same dates

## Design
Each strategy is a class inheriting from `Strategy` and implementing
`generate_signals`, which returns 1 (holding) or 0 (in cash) for each day.
The `Backtest` engine handles timing, so every strategy acts only on data
available before the trade. Adding a strategy means writing one class.

## How to run
```
pip install yfinance pandas
python main.py
```

## Status
Work in progress. Planned: risk metrics (Sharpe ratio, max drawdown),
transaction costs, tests, and a web interface.