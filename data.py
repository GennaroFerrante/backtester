import yfinance
ticker = "SPY"
all_data = yfinance.download(ticker, "2010-01-01", "2026-10-10")
close_prices = all_data["Close"][ticker]