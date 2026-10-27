import yfinance

def load_prices(ticker, start, end):
    all_data = yfinance.download(ticker, start, end)
    close_prices = all_data["Close"][ticker]
    return close_prices