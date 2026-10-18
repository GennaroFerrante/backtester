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