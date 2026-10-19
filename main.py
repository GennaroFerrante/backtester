import yfinance

#Program gets historical stock data, and backtests different strategies with changeable parameters

ticker = "SPY"
all_data = yfinance.download(ticker, "2010-01-01", "2026-10-10")
close_prices = all_data["Close"][ticker]


def get_return(results):
    total = 1.0
    for i in range(0, len(results), 2):
        buy_price = results[i][1]
        sell_price = results[i + 1][1]
        total *= sell_price / buy_price

    total_percentage = (total - 1) * 100

    return total_percentage

def mean_reversion(short_period, long_period, buy_point):
    trades = []
    holding = False
    days_invested = 0
    long_avg = close_prices.rolling(long_period).mean().shift(1)
    short_avg = close_prices.rolling(short_period).mean().shift(1)
    for i in range(long_period + 1, len(all_data)):
        if holding:
            days_invested += 1
        if (short_avg.iloc[i] < long_avg.iloc[i] * buy_point 
            and short_avg.iloc[i - 1] > long_avg.iloc[i - 1] * buy_point 
            and not holding):
            trades.append(["buy", float(close_prices.iloc[i])])
            holding = True
        if short_avg.iloc[i] > long_avg.iloc[i] and holding:
            trades.append(["sell", float(close_prices.iloc[i])])
            holding = False
    if holding:
        trades.append(["sell", float(close_prices.iloc[-1])])
    print(days_invested)
    return trades

def moving_average_crossover(short_period, long_period):
    trades = []
    holding = False
    long_avg = close_prices.rolling(long_period).mean().shift(1)
    short_avg = close_prices.rolling(short_period).mean().shift(1)
    days_invested = 0
    for i in range(long_period + 1, len(all_data)):
        if holding:
            days_invested += 1
        if short_avg.iloc[i] > long_avg.iloc[i] and not holding:
            trades.append(["buy", float(close_prices.iloc[i])])
            holding = True
        if short_avg.iloc[i] < long_avg.iloc[i] and holding:
            trades.append(["sell", float(close_prices.iloc[i])])
            holding = False
    if holding:
        trades.append(["sell", float(close_prices.iloc[-1])])
    print(days_invested)
    return trades

def trend_filter(long_period):
    trades = []
    holding = False
    long_avg = close_prices.rolling(long_period).mean().shift(1)
    days_invested = 0
    for i in range(long_period + 1, len(all_data)):
        if holding:
            days_invested += 1
        if close_prices.iloc[i - 1] > long_avg.iloc[i] and not holding:
            trades.append(["buy", float(close_prices.iloc[i])])
            holding = True
        if close_prices.iloc[i - 1] < long_avg.iloc[i] and holding:
            trades.append(["sell", float(close_prices.iloc[i])])
            holding = False
    if holding:
        trades.append(["sell", float(close_prices.iloc[-1])])
    print(days_invested)
    return trades

def relative_strength_index(long_period, lookback):
    gains = 0
    losses = 0
    periodic_RSIs = [None]
    trades = []
    holding = False
    days_invested = 0
    for i in range(1, len(all_data)):
        if i <= lookback:
            if close_prices.iloc[i] > close_prices.iloc[i - 1]:
                gains += (close_prices.iloc[i] - close_prices.iloc[i - 1])
            if close_prices.iloc[i] < close_prices.iloc[i - 1]:
                losses += (close_prices.iloc[i - 1] - close_prices.iloc[i])
            avg_gain, avg_loss = gains / lookback, losses / lookback
            periodic_RSIs.append(None)
        else:
            if close_prices.iloc[i] > close_prices.iloc[i - 1]:
                avg_gain = (avg_gain * (lookback - 1) + (close_prices.iloc[i] - close_prices.iloc[i - 1])) / lookback
                avg_loss = (avg_loss * (lookback - 1)) / lookback
            if close_prices.iloc[i] < close_prices.iloc[i - 1]:
                avg_loss = (avg_loss * (lookback - 1) + (close_prices.iloc[i - 1] - close_prices.iloc[i])) / lookback
                avg_gain = (avg_gain * (lookback - 1)) / lookback
            if avg_loss == 0:
                rsi = 100
            else:
                rs = avg_gain / avg_loss
                rsi = 100 - (100/(1 + rs))
            periodic_RSIs.append(float(rsi))
    for i in range(long_period + 1, len(all_data)):
        if holding:
            days_invested += 1
        if periodic_RSIs[i - 1] is None:
            continue
        if periodic_RSIs[i - 1] < 30 and not holding:
            trades.append(["buy", float(close_prices.iloc[i])])
            holding = True
        if periodic_RSIs[i - 1] > 70 and holding:
            trades.append(["sell", float(close_prices.iloc[i])])
            holding = False
    if holding:
        trades.append(["sell", float(close_prices.iloc[-1])])
    print(days_invested)
    return trades

short_period, long_period, buy_point, lookback = 50, 200, 0.99, 14
bah_returns = (float(close_prices.iloc[-1] / close_prices.iloc[long_period + 1]) - 1) * 100
mr_returns = get_return(mean_reversion(short_period, long_period, buy_point))
mac_returns = get_return(moving_average_crossover(short_period, long_period))
tf_returns = get_return(trend_filter(long_period))
rsi_returns = get_return(relative_strength_index(long_period, lookback))
print(len(all_data) - long_period + 1)
print("MR Returns: " + str(mr_returns) + "%")
print("MAC Returns: " + str(mac_returns) + "%")
print("TF Returns: " + str(tf_returns) + "%")
print("RSI Returns: " + str(rsi_returns) +"%")
print("BAH Returns: " + str(bah_returns) +"%")