from strategies import MovingAverageCrossover, MeanReversion, TrendFilter, RelativeStrengthIndex, BuyAndHold
import numpy as np
import pandas as pd

def make_prices(days=800):
    rng = np.random.default_rng(seed=42)
    random_returns = rng.normal(0.0005, 0.01, days)
    return pd.Series(100 * (1 + random_returns).cumprod(), 
                     index=pd.date_range("2020-01-01", periods=days, freq="B"))

def check_for_look_ahead(strategy):
    prices = make_prices()
    full_signals = strategy.generate_signals(prices)

    assert full_signals.nunique() > 1, "strategy never changed position on test data"

    for cutoff in range(250, len(prices), 25):
        partial_signals = strategy.generate_signals(prices.iloc[:cutoff])
        pd.testing.assert_series_equal(full_signals.iloc[:cutoff], partial_signals)

def test_MAC_for_look_ahead():
    check_for_look_ahead(MovingAverageCrossover(50, 200))

def test_MR_for_look_ahead():
    check_for_look_ahead(MeanReversion(50, 200, 0.99))

def test_TF_for_look_ahead():
    check_for_look_ahead(TrendFilter(200))

def test_RSI_for_look_ahead():
    check_for_look_ahead(RelativeStrengthIndex())