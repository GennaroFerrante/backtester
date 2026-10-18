import yfinance

#Get historical stock data
#Test strategy
#Test buy and hold
#Show results

ticker = "SPY"
all_data = yfinance.download(ticker, "2010-01-01", "2026-10-10")
close_prices = all_data["Close"][ticker]

def mean_reversion_strategy(short_period, long_period, buy_point):
    trades = []
    under = False
    long_avg = close_prices.rolling(long_period).mean().shift(1)
    short_avg = close_prices.rolling(short_period).mean().shift(1)
    for i in range(long_period + 1, len(all_data)):
        if (short_avg.iloc[i] < long_avg.iloc[i] * buy_point 
            and short_avg.iloc[i - 1] > long_avg.iloc[i - 1] * buy_point 
            and not under):
            trades.append(["buy", float(close_prices.iloc[i])])
            under = True
        if under:
            if short_avg.iloc[i] > long_avg.iloc[i]:
                trades.append(["sell", float(close_prices.iloc[i])])
                under = False
        if i == (len(all_data) - 1) and under:
            trades.append(["sell", float(close_prices.iloc[i])])
    return trades
    
short_period, long_period, buy_point = 50, 200, 0.95
results = mean_reversion_strategy(short_period, long_period, buy_point)

total = 1.0
for i in range(0, len(results), 2):
    buy_price = results[i][1]
    sell_price = results[i + 1][1]
    total *= sell_price / buy_price

total_percentage = (total - 1) * 100
buy_and_hold_percentage = (float(close_prices.iloc[-1] / close_prices.iloc[long_period]) - 1) * 100

print(total_percentage, buy_and_hold_percentage)