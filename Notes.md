#Notes

#Mean Reversion Stategy
- Version 1 of a mean-reversion strategy: When the 50 day average drops below 1/3/5% of the 200 day average, buy, and when it reaches the 200 day average again, sell.
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

#Added Moving-Average-Crossover, trend filter, and RSI strategies
- Ran them at (50, 200, 0.99, 14) - Using 0.99 as a buy point because it consistently returns the highest results
- MR returned 94.24%, MAC returned 218.49%, TF returned 374.73%, RSI returns 271.89%, BAH returns 774.77%
- Still not outperforming the market for various reasons, mostly because not invested during periods of high growth
- MR in market for 600 days, MAC for 3374, TF for 3413, RSI for 1169, total for 4019

#Trend Filter
- Doesn't account for days where the price doesn't change, which is incredibly insignificant because there are likely no days in which the price is exactly the same