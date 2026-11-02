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
Strategy                                          Total   Annual     Vol  Sharpe   Max DD   Days  Trades
--------------------------------------------------------------------------------------------------------
Buy and hold                                      12.9%     1.2%   22.0%    0.16   -55.2%   2564       0
--------------------------------------------------------------------------------------------------------
Mean reversion                                   -45.6%    -5.8%   19.1%   -0.22   -63.0%   1018       8
MA crossover                                     111.4%     7.6%   10.6%    0.75   -15.7%   1447      12
Trend filter                                      43.8%     3.6%    9.9%    0.41   -25.0%   1467      87
RSI                                              -18.8%    -2.0%   19.8%   -0.00   -55.2%   1280      13
--------------------------------------------------------------------------------------------------------
Mean reversion + MA crossover                     16.0%     1.5%   21.8%    0.18   -53.3%   2465      12
Mean reversion + Trend filter                    -18.6%    -2.0%   21.3%    0.01   -58.8%   2385      65
Mean reversion + RSI                             -27.5%    -3.1%   20.2%   -0.06   -56.7%   1419      13
MA crossover + Trend filter                      109.0%     7.5%   11.0%    0.71   -16.0%   1603      42
MA crossover + RSI                                23.0%     2.1%   21.6%    0.20   -55.2%   2420       4
Trend filter + RSI                                16.9%     1.5%   21.5%    0.18   -55.2%   2413      28
--------------------------------------------------------------------------------------------------------
Mean reversion + MA crossover + Trend filter      18.6%     1.7%   21.8%    0.19   -53.3%   2521      18
Mean reversion + MA crossover + RSI               10.1%     0.9%   22.0%    0.15   -55.2%   2559       2
Mean reversion + Trend filter + RSI                4.7%     0.5%   21.8%    0.13   -55.2%   2519      22
MA crossover + Trend filter + RSI                 22.9%     2.0%   21.6%    0.20   -55.2%   2453       8
```

### Findings (2010-2026 with costs)
- TF hit hardest: 78 trades (price crosses its 200-day average often in choppy markets). 2010-2026 return fell from 367% to 332%, and its Sharpe dropped below BAH (0.84 vs 0.88)
- MAC barely affected: only 14 trades, since two averages cross much less often than price crosses one
- Combinations often trade less than their parts (TF + RSI: 26 trades vs. 78 for TF alone), since one strategy is often still holding when the other steps out
- Verified the cost code by hand: return after costs = no-cost growth x 0.999^trades (TF: 4.674 x 0.925 = 4.32 -> 332%)

### Limitations
- BAH and any strategy already holding on the start day get their first position free (the buy happens before `start` and is trimmed away)
- Cost is a flat percentage; real costs vary with market conditions and trade size

### Findings (2000-2010 with costs)
- TF traded 87 times in ~10 years (~8.5/year) vs. 78 in 16 years (~5/year) for 2010-2026.
  Choppier market = more crossings of the 200-day average = higher costs (57% -> 44%)
- MAC is the strongest strategy here even after costs: +111% vs. BAH +13%, Sharpe 0.75 vs. 0.16,
  max DD -15.7% vs. -55.2%, with only 12 trades
- Costs didn't change the ranking: dip-buying strategies (MR, RSI) still lost money

### Comparing both periods with costs
- Trend strategies consistently reduced drawdowns: TF max DD was -25.0% in both periods vs.
  BAH's -33.7% and -55.2%
- In the bull market (2010-2026), trend strategies trailed BAH slightly on Sharpe
  (TF 0.84, MAC 0.68 vs. 0.88). In the bear-heavy decade (2000-2010), they beat it by a lot
  (TF 0.41, MAC 0.75 vs. 0.16)
- No strategy or combination beat BAH on every measure in both periods
- Trend-following acts more like insurance than a way to beat the market: it costs a little
  in good decades and saves a lot in bad ones

## Multiple markets (10/28/26), 0.1% cost
- Markets: SPY, QQQ, IWM (small caps), EFA (international), TLT (long-term bonds)
- Full tables saved in results/
- Note: EFA and TLT data start later, so their 2000-2010 tests begin ~2002-2003

### Trend filter vs. buy-and-hold
| Market | Period | TF Sharpe | BAH Sharpe | TF Max DD | BAH Max DD | TF trades |
|---|---|---|---|---|---|---|
| SPY | 2000–2010 | 0.41 | 0.16 | −25% | −55% | 87 |
| SPY | 2010–2026 | 0.84 | 0.88 | −25% | −34% | 78 |
| QQQ | 2000–2010 | 0.41 | 0.06 | −23% | −77% | 89 |
| QQQ | 2010–2026 | 0.83 | 0.95 | −26% | −35% | 86 |
| EFA | 2000–2010 | 0.92 | 0.42 | −16% | −61% | 49 |
| EFA | 2010–2026 | 0.41 | 0.46 | −27% | −34% | 126 |
| IWM | 2000–2010 | 0.19 | 0.40 | −39% | −59% | 107 |
| IWM | 2010–2026 | 0.45 | 0.56 | −34% | −41% | 127 |
| TLT | 2000–2010 | 0.10 | 0.40 | −23% | −27% | 87 |
| TLT | 2010–2026 | 0.03 | 0.16 | −50% | −48% | 185 |

### Findings
- TF reduced max drawdown vs. BAH in all 8 stock runs, confirming the SPY result
- TF beat BAH on Sharpe in SPY, EFA, and QQQ during 2000-2010; trailed slightly
  in every 2010-2026 bull market
- QQQ 2000-2010 (dot-com crash) is the strongest case for trend-following:
  BAH -27% with -77% max DD; TF +61% with -23% DD; MAC +73% with -30% DD
- Exceptions: IWM 2000-2010 (TF Sharpe 0.19 vs. 0.40, small caps did well early
  in the decade) and TLT both periods (bonds chop around their average; TF made
  185 trades in TLT 2010-2026 and still had a worse DD than BAH)
- MAC inconsistent: strong on SPY and QQQ 2000-2010, weak on IWM and EFA
- MR + TF had the best Sharpe on SPY, IWM, and EFA for 2010-2026, so it fits that
  era, not just SPY. Mixed in 2000-2010: failed on SPY, beat BAH on QQQ
- Dip-buying failed badly in crashes: on QQQ 2000-2010, RSI lost 61% and MR + RSI
  lost 66%, with drawdowns worse than BAH
- MR on TLT 2000-2010: Sharpe 0.88, max DD -6%, but only 12 trades

### Bugs caught
- QQQ 2000-2010 file first contained TLT 2010-2026 results (caught because days
  invested was 4022, the length of the other window). Fixed and rerun

## Equal-weight portfolio (11/01/26), 0.1% cost
- 25% each in SPY, IWM, EFA, TLT, rebalanced daily (rebalancing cost not modeled)
- Portfolio dates: 2003-05-19 to 2010 (EFA/TLT start later, so it misses the
  dot-com crash) and 2010-10-21 to 2026

```
2003-2010                          Total  Annual   Vol  Sharpe  Max DD
Buy and hold                       87.7%    8.6%  16.7%  0.58  -42.6%
Trend filter                       55.8%    6.0%   9.5%  0.66  -14.7%
MA crossover                       65.2%    6.8%  10.1%  0.70  -16.0%
Mean reversion + Trend filter      69.0%    7.1%  15.4%  0.52  -40.2%
Trend filter on stocks, hold TLT   68.5%    7.1%   9.5%  0.77  -14.2%

2010-2026                          Total  Annual   Vol  Sharpe  Max DD
Buy and hold                      296.0%    9.0%  12.9%  0.73  -28.0%
Trend filter                      125.1%    5.2%   8.4%  0.65  -16.1%
MA crossover                      106.5%    4.6%   9.9%  0.51  -26.2%
Mean reversion + Trend filter     319.2%    9.4%  11.1%  0.86  -28.0%
Trend filter on stocks, hold TLT  144.5%    5.8%   8.7%  0.69  -21.9%
```

### Findings
- Diversification alone lowered drawdown (2010-2026: -28% vs. -34% for SPY)
  but also lowered Sharpe (0.73 vs. 0.88), since SPY was the best market
- 2003-2010: TF on stocks + hold TLT was best on Sharpe, drawdown, and
  volatility; only total return trailed BAH
- 2010-2026: trend portfolios cut drawdowns but trailed BAH on Sharpe;
  insurance was expensive in a long bull market
- Holding TLT beat timing it in both periods (agrees with TF failing on bonds)
- MR + TF: best Sharpe in 2010-2026, worst in 2003-2010, so it is still a
  bull-market strategy. It was also chosen using 2010-2026 data
- To do: rerun SPY alone from 2003-05-19 so the 2000s comparison is fair

## Week 9: Parameter sweeps (11/02/26), SPY, 0.1% cost, start = 302
- TF windows 50-300 (step 10); MAC short 10-90 x long 100-300 (step 10)
- Full results saved in results/sweep_*.csv

### Trend filter
- 2010-2026: plateau. Sharpe 0.69-0.85 for every window from 90-300 days;
  best 140 (0.85), default 200 (0.81). Short windows (50-80) worse
- 2000-2010: Sharpe rises with window length, ~0.10 at 100-110 to 0.68 at
  290; trades fall from 169 to 29. Slower signals worked better in a choppy,
  crash-heavy decade
- Out-of-sample: 2010-2026's best (140) scored 0.35 in 2000-2010, below that
  decade's median (0.39)
- Robust result: almost every window beat BAH Sharpe in 2000-2010; almost none
  did in 2010-2026. The insurance role doesn't depend on the exact window

### MA crossover
- 2010-2026: nearly flat surface (most settings 0.65-0.78); best 10/220 (0.86)
  looks like noise on a flat field
- 2000-2010: long windows >= 170 clearly better (median 0.64 vs 0.37);
  best 50/220 (0.83)
- Out-of-sample: 10/220 scored 0.51 in 2000-2010; 50/220 scored 0.68 in
  2010-2026 (below that period's median)
- Default 50/200: 0.71 and 0.66, solid in both, best in neither

### Conclusion
- Defaults (200, 50/200) were not overfit
- The best exact setting changes with the market regime, so optimizing on
  one period doesn't carry over. Long windows (~200+) are sound in both