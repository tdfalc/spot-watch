from pathlib import Path

import pandas as pd
import matplotlib.dates as mdates
from matplotlib import pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_day_ahead_auction_results(
    results: pd.DataFrame, savedir: Path, market_area: str
) -> None:
    _plot_day_ahead_auction_results_pyplot(results, savedir, market_area)
    _plot_day_ahead_auction_results_plotly(results, savedir, market_area)


def _plot_day_ahead_auction_results_pyplot(
    results: pd.DataFrame, savedir: Path, market_area: str
) -> None:
    fig, ax0 = plt.subplots(figsize=(7, 4))
    ax1 = ax0.twinx()

    ax0.plot(results.index, results.price, label="Price", color="C0")
    ax1.plot(results.index, results.volume, label="Volume", color="C1")

    ax0.set(
        ylabel="Price (£/MWh)",
        title=f"{market_area} Day-Ahead Auction (1hr)",
    )
    ax1.set(ylabel="Volume (MWh)")

    ax0.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H"))
    ax0.xaxis.set_major_locator(plt.MaxNLocator(6))

    for tick in ax0.get_xticklabels():
        tick.set_rotation(45)

    lines0, labels0 = ax0.get_legend_handles_labels()
    lines1, labels1 = ax1.get_legend_handles_labels()
    ax0.legend(lines0 + lines1, labels0 + labels1, loc=0)

    fig.savefig(savedir / "day_ahead_auction.png", dpi=300, bbox_inches="tight")


def _plot_day_ahead_auction_results_plotly(
    results: pd.DataFrame, savedir: Path, market_area: str
) -> None:

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=results.index,
            y=results.price,
            name="Price (£/MWh)",
            line_color="blue",
            mode="lines+markers",
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=results.index,
            y=results.volume,
            name="Volume (MWh)",
            line_color="darkorange",
            mode="lines+markers",
        ),
        secondary_y=True,
    )

    fig.update_layout(
        title_text=f"{market_area} Day-Ahead Auction (1hr)",
        template="simple_white",
        showlegend=False,
    )

    fig.update_xaxes(title_text="Time (UTC)", showgrid=False)

    fig.update_yaxes(
        title_text="Price (£/MWh)",
        title_font_color="blue",
        secondary_y=False,
        showgrid=False,
    )

    fig.update_yaxes(
        title_text="Volume (MWh)",
        title_font_color="darkorange",
        secondary_y=True,
        showgrid=False,
    )

    fig.write_html(savedir / "day_ahead_auction.html")
