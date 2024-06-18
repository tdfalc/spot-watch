from pathlib import Path
import os

import pandas as pd

from spot_watch.config import get_config
from spot_watch.request import request_day_ahead_auction_results
from spot_watch.plot import plot_day_ahead_auction_results


def save_day_ahead_auction_results(df: pd.DataFrame, savedir: Path) -> None:
    year = df.index[-1].year
    filename = savedir / f"auction_results_{year}.csv"
    if os.path.isfile(filename):
        df2 = pd.read_csv(filename, index_col="date_start", parse_dates=["date_start"])
        df = df2.combine_first(df)
    df.to_csv(filename)


if __name__ == "__main__":
    savedir = Path(__file__).parent / "docs"
    os.makedirs(savedir, exist_ok=True)

    config = get_config().GENERAL
    results = request_day_ahead_auction_results(**config)
    save_day_ahead_auction_results(results, savedir)
    plot_day_ahead_auction_results(results, Path("./docs/"), config.market_area)
