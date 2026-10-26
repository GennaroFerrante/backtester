from strategies import Strategy, BuyAndHold
from engine import Backtest
import pandas as pd
import numpy as np
import math
import pytest

def make_prices(days=800):
    rng = np.random.default_rng(seed=42)
    random_returns = rng.normal(0.0005, 0.01, days)
    return pd.Series(100 * (1 + random_returns).cumprod(), 
                     index=pd.date_range("2020-01-01", periods=days, freq="B"))

class FixedSignals(Strategy):
    """Test helper: returns whatever signals it's given."""
    def __init__(self, signals):
        self.signals = signals

    def generate_signals(self, prices):
        return self.signals

def make_timing_data(signal_values):
    prices = pd.Series([100.0, 110.0, 99.0, 120.0, 126.0], index=pd.date_range("2020-01-01", periods=5, freq="B"))
    signals = pd.Series(signal_values, index=pd.date_range("2020-01-01", periods=5, freq="B"))
    return prices, signals

random_prices = make_prices()
prices_zeroes = pd.Series([0.0, 0.0, 0.0])
prices_custom = pd.Series([100, 110, 99, 120, 126])

def test_never_invested_earns_nothing():
    start = 202
    signals = pd.Series(0, index=random_prices.index)
    result = Backtest(random_prices, FixedSignals(signals), start=start).run()
    assert result["total_return"] == 0
    assert result["days_invested"] == 0

def test_BAH_invested_matches_price_change():
    start = 202
    results = Backtest(random_prices, BuyAndHold(), start).run()
    expected = random_prices.iloc[-1] / random_prices.iloc[start - 1] - 1
    assert results["total_return"] == pytest.approx(expected)

def test_signal_on_day_1_earns_day_3_move():
    prices, signals = make_timing_data([0, 1, 0, 0, 0])
    result = Backtest(prices, FixedSignals(signals)).run()

    assert result["total_return"] == pytest.approx(120 / 99 - 1)
    assert result["days_invested"] == 1


def test_signal_on_day_2_earns_day_4_move():
    prices, signals = make_timing_data([0, 0, 1, 0, 0])
    result = Backtest(prices, FixedSignals(signals)).run()

    assert result["total_return"] == pytest.approx(126 / 120 - 1)
    assert result["days_invested"] == 1


def test_two_held_days_compound():
    prices, signals = make_timing_data([0, 1, 1, 0, 0])
    result = Backtest(prices, FixedSignals(signals)).run()

    assert result["total_return"] == pytest.approx((120 / 99) * (126 / 120) - 1)
    assert result["days_invested"] == 2