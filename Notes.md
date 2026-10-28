# Notes

## Mean Reversion Strategy
- Version 1 of a mean-reversion strategy: When the 50 day average drops 1%, 3%, or 5% below the 200 day average, buy, and when it reaches the 200 day average again, sell.
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
- Costs subtracted after trimming to `start` made pandas re-add the trimmed dates as NaN, so annualized return used the wrong number of days. Fixed by applying costs before trimming; added a test that the returns length matches the start date

## Refactor to classes
- Moved strategies into classes inheriting from a Strategy base class, with one shared Backtest engine that handles timing and returns
- Verified each class reproduces the old function's results before deleting the old code

## Something worth thinking about on 10/21/26
- Looking at days invested for each strategy with (50, 200, 0.99, 14), MR ran for 600 days, MAC ran for 3374 days, TF ran for 3413 days, and RSI ran for 1169 days, while the span was 4019 trading days
- MR returns roughly 0.111% per day invested, MAC returns 0.042%, TF returns 0.046%, RSI returns 0.112%, while BAH returns 0.054%
- Most of the loss (loss meaning no-gain) comes from not being invested during growth. It could be possible to combine strategies so that it limits missing out on growth

## Plots
- Compared to the BAH total equity curve and max drawdown curve, the TF strategy had a lower total equity curve but almost always maintained a shallower max drawdown.
- RSI also had a lower total equity curve and max drawdown never was as low as BAH.
- MR greatly avoided the max drawdown in 2020 that BAH saw, but was nowhere near as close to total equity at any point
- MAC often had the same or lower (more negative) max drawdown that BAH had, while having a lower total equity

## Test Notes
- Built metric tests with hand-calculated values and edge cases, truncation look-ahead tests for every strategy, engine timing tests, and GitHub Actions running everything on each push
- First look-ahead test missed a planted bug; replaced it with a truncation test that catches it.

## Combined Test Results
```
Strategy                                          Total   Annual     Vol  Sharpe   Max DD   Days
--------------------------------------------------------------------------------------------------- Buy and hold                                     761.2%    14.4%   16.9%    0.88   -33.7%   4022
Mean reversion                                    94.2%     4.2%    8.6%    0.52   -23.1%    600
MA crossover                                     312.0%     9.3%   14.4%    0.69   -33.7%   3380
Trend filter                                     367.4%    10.1%   11.8%    0.88   -23.5%   3419
RSI                                              271.9%     8.6%   13.2%    0.69   -28.3%   1169
Mean reversion + MA crossover                    700.3%    13.9%   16.8%    0.86   -33.7%   3980
Mean reversion + Trend filter                    804.2%    14.8%   14.2%    1.05   -29.5%   3818
Mean reversion + RSI                             210.2%     7.4%   13.6%    0.59   -28.3%   1284
MA crossover + Trend filter                      324.4%     9.5%   14.8%    0.69   -33.7%   3586
MA crossover + RSI                               932.5%    15.8%   16.6%    0.96   -33.7%   3907
Trend filter + RSI                               994.4%    16.2%   16.7%    0.98   -33.7%   3966
Mean reversion + MA crossover + Trend filter     721.0%    14.1%   16.8%    0.87   -33.7%   3985
Mean reversion + MA crossover + RSI              761.2%    14.4%   16.9%    0.88   -33.7%   4022
Mean reversion + Trend filter + RSI              844.2%    15.1%   16.8%    0.92   -33.7%   3996
MA crossover + Trend filter + RSI                898.1%    15.5%   16.8%    0.94   -33.7%   3992
```
- All run with long_period = 200, short_period = 50, buy_point = 0.99
- Best results come from TF+RSI, MAC+RSI, MAC+TF+RSI, MR+TF+RSI, MR+TF (returns, Sharpe, Max DD)
- TF+RSI is partly luck, seeing that it only skipped 56 days, which were losing days on average
- MR+TF beats BAH on every metric, so it may be better over longer periods and different parameters


## Caveats on combined results
- 11 combinations tested on the same data, so the best ones are partly luck (data snooping)
- No transaction costs yet (Week 7); results may shrink
- Cash earns 0%, and Sharpe uses a 0% risk-free rate
- Certain numbers changed because of a two-week change in the end date, as well as a one day delay in the start of trading
- All strategies were tested on SPY with close prices from yfinance between 2010 and 2026, start=202, risk free rate of 0, and with the Sharpe Ratio using the simple average of daily returns

## Combined Test Results for 2000-2010
```
Strategy                                          Total   Annual     Vol  Sharpe   Max DD   Days
------------------------------------------------------------------------------------------------
Buy and hold                                      12.9%     1.2%   22.0%    0.16   -55.2%   2564
Mean reversion                                   -45.1%    -5.7%   19.1%   -0.21   -62.9%   1018
MA crossover                                     114.0%     7.8%   10.6%    0.76   -15.7%   1447
Trend filter                                      56.9%     4.5%    9.9%    0.50   -23.3%   1467
RSI                                              -17.7%    -1.9%   19.8%    0.00   -55.2%   1280
Mean reversion + MA crossover                     17.4%     1.6%   21.8%    0.18   -53.3%   2465
Mean reversion + Trend filter                    -13.1%    -1.4%   21.3%    0.04   -58.1%   2385
Mean reversion + RSI                             -26.5%    -3.0%   20.2%   -0.05   -56.3%   1419
MA crossover + Trend filter                      118.0%     8.0%   11.0%    0.75   -15.7%   1603
MA crossover + RSI                                23.5%     2.1%   21.6%    0.20   -55.2%   2420
Trend filter + RSI                                20.2%     1.8%   21.5%    0.19   -55.2%   2413
Mean reversion + MA crossover + Trend filter      20.8%     1.9%   21.8%    0.19   -53.3%   2521
Mean reversion + MA crossover + RSI               10.3%     1.0%   22.0%    0.15   -55.2%   2559
Mean reversion + Trend filter + RSI                7.0%     0.7%   21.8%    0.14   -55.2%   2519
MA crossover + Trend filter + RSI                 23.8%     2.1%   21.6%    0.21   -55.2%   2453
```
- Rankings flipped compared to 2010-2026
- Trend strategies did best: MAC +114% (-15.7% DD), TF +57% (-23.3% DD) vs. BAH +13% (-55.2% DD)
- Dip-buying strategies failed: MR -45%, RSI -18%. In long bear markets, big drops kept falling instead of rebounding
- 2010-2026's best combinations didn't hold up: MR+TF went from best on every measure to a worse drawdown than BAH (-58.1%)
- Most robust: TF alone. Sharpe at least as good as BAH in both periods (0.88 vs 0.88, 0.50 vs 0.16), max DD ~-23% in both
- Lesson: strategies depend on market regime. Dip-buying works in bull markets with quick recoveries; trend-following works in long declines
- Picking the best combination from one period overfits to that period (data snooping)

## Transaction Costs (10/27/26)
- Added a cost of 0.1% of the amount traded on every position change (roughly covers commissions, bid-ask spread, and slippage)
- Each buy and each sell counts as one trade

### 2010-2026, 0.1% cost
```
Strategy                                          Total   Annual     Vol  Sharpe   Max DD   Days  Trades
--------------------------------------------------------------------------------------------------------
Buy and hold                                     761.2%    14.4%   16.9%    0.88   -33.7%   4022       0
--------------------------------------------------------------------------------------------------------
Mean reversion                                    91.5%     4.2%    8.6%    0.51   -23.2%    600      14
MA crossover                                     306.2%     9.2%   14.4%    0.68   -33.7%   3380      14
Trend filter                                     332.2%     9.6%   11.8%    0.84   -25.0%   3419      78
RSI                                              260.2%     8.4%   13.2%    0.67   -28.3%   1169      32
--------------------------------------------------------------------------------------------------------
Mean reversion + MA crossover                    689.1%    13.8%   16.8%    0.86   -33.7%   3980      14
Mean reversion + Trend filter                    756.6%    14.4%   14.2%    1.02   -30.1%   3818      54
Mean reversion + RSI                             201.0%     7.1%   13.6%    0.58   -28.3%   1284      30
MA crossover + Trend filter                      308.5%     9.2%   14.8%    0.67   -33.7%   3586      38
MA crossover + RSI                               920.2%    15.7%   16.6%    0.96   -33.7%   3907      12
Trend filter + RSI                               966.2%    16.0%   16.7%    0.97   -33.7%   3966      26
--------------------------------------------------------------------------------------------------------
Mean reversion + MA crossover + Trend filter     709.5%    14.0%   16.8%    0.87   -33.7%   3985      14
Mean reversion + MA crossover + RSI              761.2%    14.4%   16.9%    0.88   -33.7%   4022       0
Mean reversion + Trend filter + RSI              825.5%    15.0%   16.8%    0.92   -33.7%   3996      20
MA crossover + Trend filter + RSI                892.1%    15.5%   16.8%    0.94   -33.7%   3992       6
```

### 2000-2010, 0.1% cost
```
(paste table here)
```

### Findings
- TF hit hardest: 78 trades (price crosses its 200-day average often in choppy markets). 2010-2026 return fell from 367% to 332%, and its Sharpe dropped below BAH (0.84 vs 0.88)
- MAC barely affected: only 14 trades, since two averages cross much less often than price crosses one
- Combinations often trade less than their parts (TF + RSI: 26 trades vs. 78 for TF alone), since one strategy is often still holding when the other steps out
- Verified the cost code by hand: return after costs = no-cost growth x 0.999^trades (TF: 4.674 x 0.925 = 4.32 -> 332%)

### Limitations
- BAH and any strategy already holding on the start day get their first position free (the buy happens before `start` and is trimmed away)
- Cost is a flat percentage; real costs vary with market conditions and trade size