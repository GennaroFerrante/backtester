from strategies import MovingAverageCrossover, MeanReversion, TrendFilter, RelativeStrengthIndex, CombinedStrategy, Strategy
import numpy as np
import pandas as pd

class FixedSignals(Strategy):
    """Test helper: returns whatever signals it's given."""
    def __init__(self, signals):
        self.signals = signals

    def generate_signals(self, prices):
        return self.signals

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

def test_CS_for_look_ahead():
    check_for_look_ahead(CombinedStrategy([TrendFilter(200), RelativeStrengthIndex()]))

def test_CS_holds_when_any_strategy_holds():
    dates = pd.date_range("2020-01-01", periods=4, freq="B")
    a = FixedSignals(pd.Series([1, 0, 0, 1], index=dates))
    b = FixedSignals(pd.Series([0, 0, 1, 1], index=dates))
    prices = pd.Series([100.0, 101.0, 102.0, 103.0], index=dates)

    combined = CombinedStrategy([a, b]).generate_signals(prices)
    assert list(combined) == [1, 0, 1, 1]