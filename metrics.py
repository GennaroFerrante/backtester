import math

# Metrics which can’t be calculated return 0

def total_return(returns):
    result  = float((1 + returns.fillna(0)).prod() - 1)
    return result

def annualized_return(returns):
    growth = (1 + returns.fillna(0)).prod()
    years = len(returns) / 252
    if years == 0:
        return 0.0
    return (growth ** (1 / years) - 1)

def annualized_volatility(returns):
    sd = returns.std()
    if math.isnan(sd):
        return 0.0
    return (sd * math.sqrt(252))

def sharpe_ratio(returns, risk_free_rate=0.0):
    daily_rate = risk_free_rate / 252
    excess_daily_returns = returns - daily_rate
    sd = excess_daily_returns.std()
    if math.isclose(sd, 0, abs_tol=1e-12) or math.isnan(sd):
        return 0.0
    return (excess_daily_returns.mean() / sd * math.sqrt(252))

def max_drawdown(returns):
    if len(returns) < 1:
        return 0.0
    equity_curve = (1 + returns.fillna(0)).cumprod()
    running_peak = equity_curve.cummax().clip(lower=1.0)
    return (equity_curve / running_peak - 1).min()