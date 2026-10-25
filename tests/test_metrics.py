from metrics import total_return, annualized_return, annualized_volatility, sharpe_ratio, max_drawdown
import pandas as pd
import math
import pytest

mixed_test = pd.Series([0.15, -0.3, 0.25, -0.05, 0.1])
positive_test = pd.Series([0.15, 0.3, 0.25, 0.05, 0.1])
negative_test = pd.Series([-0.15, -0.3, -0.25, -0.05, -0.1])
zeroes_test = pd.Series([0.0, 0.0, 0.0])
one_value_test = pd.Series([0.1])
first_negative_test = pd.Series([-0.1, 0.5, -0.05])
empty_test = pd.Series([], dtype=float)
constant_returns_test = pd.Series([0.1, 0.1, 0.1])

def test_total_return():
    assert total_return(mixed_test) == pytest.approx(0.05153125)

def test_total_return_all_positive():
    assert total_return(positive_test) == pytest.approx(1.15840625)

def test_total_return_all_negative():
    assert total_return(negative_test) == pytest.approx(-0.61845625)

def test_total_return_all_zero():
    assert total_return(zeroes_test) == pytest.approx(0)

def test_total_return_one_value():
    assert total_return(one_value_test) == pytest.approx(0.1)

def test_total_return_empty():
    assert total_return(empty_test) == pytest.approx(0)

def test_total_return_constant_returns():
    assert total_return(constant_returns_test) == pytest.approx(0.331)

def test_annualized_return():
    assert annualized_return(mixed_test) == pytest.approx(11.5845608396)

def test_annualized_return_all_positive():
    assert annualized_return(positive_test) == pytest.approx(69232939414678785.2476219362472)

def test_annualized_return_all_negative():
    assert annualized_return(negative_test) == pytest.approx(-1)

def test_annualized_return_all_zero():
    assert annualized_return(zeroes_test) == pytest.approx(0)

def test_annualized_return_one_value():
    assert annualized_return(one_value_test) == pytest.approx(26974702267.758007569296)

def test_annualized_return_empty():
    assert annualized_return(empty_test) == pytest.approx(0)

def test_annualized_return_constant_returns():
    assert annualized_return(constant_returns_test) == pytest.approx(26974702267.8)

def test_annualized_volatility():
    assert annualized_volatility(mixed_test) == pytest.approx(3.39543811606)

def test_annualized_volatility_all_positive():
    assert annualized_volatility(positive_test) == pytest.approx(1.64590400692)

def test_annualized_volatility_all_negative():
    assert annualized_volatility(negative_test) == pytest.approx(1.64590400692)

def test_annualized_volatility_all_zero():
    assert annualized_volatility(zeroes_test) == pytest.approx(0)

def test_annualized_volatility_one_value():
    assert annualized_volatility(one_value_test) == pytest.approx(0)

def test_annualized_volatility_empty():
    assert annualized_volatility(empty_test) == pytest.approx(0)

def test_annualized_volatility_constant_returns():
    assert annualized_volatility(constant_returns_test) == pytest.approx(0)

def test_sharpe_ratio():
    assert sharpe_ratio(mixed_test) == pytest.approx(2.22651679742)

def test_sharpe_ratio_all_positive():
    assert sharpe_ratio(positive_test) == pytest.approx(26.0282494118)

def test_sharpe_ratio_all_negative():
    assert sharpe_ratio(negative_test) == pytest.approx(-26.0282494118)

def test_sharpe_ratio_all_zero():
    assert sharpe_ratio(zeroes_test) == pytest.approx(0)

def test_sharpe_ratio_one_value():
    assert sharpe_ratio(one_value_test) == pytest.approx(0)

def test_sharpe_ratio_empty():
    assert sharpe_ratio(empty_test) == pytest.approx(0)

def test_sharpe_ratio_constant_returns():
    assert sharpe_ratio(constant_returns_test) == pytest.approx(0)

def test_max_drawdown():
    assert max_drawdown(mixed_test) == pytest.approx(-0.3)

def test_max_drawdown_all_positive():
    assert max_drawdown(positive_test) == pytest.approx(0)

def test_max_drawdown_all_negative():
    assert max_drawdown(negative_test) == pytest.approx(-0.61845625)
    
def test_max_drawdown_first_negative():
    assert max_drawdown(first_negative_test) == pytest.approx(-0.1)

def test_max_drawdown_all_zero():
    assert max_drawdown(zeroes_test) == pytest.approx(0)

def test_max_drawdown_one_value():
    assert max_drawdown(one_value_test) == pytest.approx(0)

def test_max_drawdown_empty():
    assert max_drawdown(empty_test) == pytest.approx(0)

def test_max_drawdown_constant_returns():
    assert max_drawdown(constant_returns_test) == pytest.approx(0)