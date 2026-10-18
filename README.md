# Backtester

A Python tool for testing different stock trading strategies and comparing them against buying and holding using historical data

## Current Features
- Downloads daily historical price data using yfinance
- Mean-Reversion strategy using short-term and long-term rolling averages
- Compares buy-and-hold strategy to existing strategies

## How to run
pip install yfinance pandas
python backtest.py

## Status
Work in Progress - Needs more strategies, risk metrics, transaction costs, tests, possible interface