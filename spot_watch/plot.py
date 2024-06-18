from pathlib import Path

import matplotlib.dates as mdates
import pandas as pd
from matplotlib import pyplot as plt


def plot_day_ahead_auction_results(
    results: pd.DataFrame, directory: Path, market_area: str
):
    fig, ax0 = plt.subplots(figsize=(7, 4))
    ax1 = ax0.twinx()

    ax0.plot(results.index, results.price, label="Price", color="C0")
    ax1.plot(results.index, results.volume, label="Volume", color="C1")

    trading_date = results.index[-1].strftime("%Y-%m-%d")
    ax0.set(
        ylabel="Price (£/MWh)",
        title=f"{market_area} Day-Ahead Auction (1hr): {trading_date}",
    )
    ax1.set(ylabel="Volume (MWh)")

    ax0.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H"))
    ax0.xaxis.set_major_locator(plt.MaxNLocator(6))

    for tick in ax0.get_xticklabels():
        tick.set_rotation(45)

    lines0, labels0 = ax0.get_legend_handles_labels()
    lines1, labels1 = ax1.get_legend_handles_labels()
    ax0.legend(lines0 + lines1, labels0 + labels1, loc=0)

    fig.savefig(directory / "day_ahead_auction", dpi=300, bbox_inches="tight")
