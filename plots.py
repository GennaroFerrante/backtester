import matplotlib.pyplot as plt

def plot_results(all_returns):
    fig, (top, bottom) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    for name, returns in all_returns.items():
        equity = (1 + returns.fillna(0)).cumprod()
        drawdown = equity / equity.cummax().clip(lower=1.0) - 1
        top.plot(equity, label=name)
        bottom.plot(drawdown, label=name)

    top.set_title("Growth of $1")
    top.set_yscale("log")
    top.legend()
    bottom.set_title("Drawdown")
    bottom.set_ylabel("Drop from peak")

    plt.tight_layout()
    plt.show()