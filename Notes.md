# Notes

## Mean Reversion Strategy
- Version 1 of a mean-reversion strategy: When the 50 day average drops below 1%, 3%, or 5% below the 200 day average, buy, and when it reaches the 200 day average again, sell.
- Both strategies should start TRADING on the same day (NOT THE DAY THE DATA STARTS)
- SPY (5, 20, 0.99) - 224.24% MR (Mean-Reversion) vs. 874.48% BAH (Buy-and-Hold)
- SPY (5, 20, 0.97) - 226.24% MR vs. 874.48% BAH
- SPY (5, 20, 0.95) - 72.89% MR vs. 874.48% BAH
- SPY (10, 50, 0.99) - 130.16% MR vs. 793.11% BAH
- SPY (10, 50, 0.97) - 57.20% MR vs. 793.11% BAH
- SPY (10, 50, 0.95) - 57.42% vs. 793.11% BAH
- SPY (50, 200, 0.99) - 94.24% MR vs. 783.31% BAH
- SPY (50, 200, 0.97) - 73.71% MR vs. 783.31% BAH
- SPY (50, 200, 0.95) - 39.29% MR vs. 783.31% BAH
- Always profitable, but never beats the market. Probably due to not being invested during long periods of growth (usually held in cash during those periods)

## Added Moving-Average-Crossover, Trend Filter, and RSI strategies
- Ran them at (50, 200, 0.99, 14) - Using 0.99 as a buy point because it consistently returns the highest results over longer periods
- MR returned 94.24%, MAC returned 318.49%, TF returned 374.73%, RSI returns 271.89%, BAH returns 774.77%
- Still not outperforming the market for various reasons, mostly because not invested during periods of high growth
- MR in market for 600 days, MAC for 3374, TF for 3413, RSI for 1169, total for 4019

## Bugs caught
- Summed per-trade returns instead of compounding them
- Buy and hold started ~200 days earlier than the strategies could trade
- Look-ahead bias: trend filter and RSI decided using the same day's close they traded at. Fixed by deciding with the previous day's data
- RSI class never sold (`not holding` instead of `holding`); found by comparing the new class's results to the old function

## Refactor to classes
- Moved strategies into classes inheriting from a Strategy base class, with one shared Backtest engine that handles timing and returns
- Verified each class reproduces the old function's results before deleting the old code

## Something worth thinking about on 10/21/26
- Looking at days invested for each strategy with (50, 200, 0.99, 14), MR ran for 600 days, MAC ran for 3374 days, TF ran for 3413 days, and RSI ran for 1169 days, while the span was 4019 trading days
- MR returns roughly 0.111% per day invested, MAC returns 0.042%, TF returns 0.046%, RSI returns 0.112%, while BAH returns 0.054%
- Most of the loss (loss meaning no-gain) comes from not being invested during growth. It could be possible to combine strategies so that it limits missing out on growth

## Plots
- Compared to the BAH total equity curve and max drawdown curve, the TF strategy had a lower total equity curve but almot always maintained a higher max drawdown.
- RSI also had a lower total equity curve and max drawdown never was as low as BAH.
- MR greatly avoided the max drawdown in 2020 that BAH saw, but was nowhere near as close to total equity at any point
- MAC often had the same or lower (more negative) max drawdown that BAH had, while having a lower total equity

## Test Notes
- First look-ahead test missed a planted bug; replaced it with a truncation test that catches it.
