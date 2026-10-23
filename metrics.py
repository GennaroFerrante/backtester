import math

def total_return(returns):
    result  = float((1 + returns.fillna(0)).prod() - 1)
    return result

def annualized_return(returns):
    growth = (1 + returns).prod()
    years = len(returns) / 252
    return (growth ** (1 / years) - 1)

def annualized_volatility(returns):
    sd = returns.std()
    return (sd * math.sqrt(252))

def sharpe_ratio(returns, risk_free_rate=0.0):
    daily_rate = risk_free_rate / 252
    excess_daily_returns = returns - daily_rate
    return (excess_daily_returns.mean() / excess_daily_returns.std() * math.sqrt(252))

def max_drawdown(returns):
    equity_curve = (1 + returns).cumprod()
    running_peak = equity_curve.cummax()
    drawdown = ((equity_curve / running_peak) - 1).min()
    return drawdown