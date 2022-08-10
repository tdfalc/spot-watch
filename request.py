import requests
import re
from datetime import datetime as dt, timedelta

import pandas as pd


def _make_request(base_url: str, **kwargs) -> str:
    url = base_url + "&".join([f"{k}={v}" for k, v in kwargs.items()])
    with requests.get(url) as response:
        html = response.text
    return html


def _trading_date(html: str) -> dt:
    trading_date = re.findall(f'"filters\[trading_date\]" value="(\S\w+\s\w+\S\s\w+)', html)
    return dt.strptime(trading_date[0], "%d %b. %Y")


def request_day_ahead_auction_results(
    base_url: str, market_area: str, fmt: str = "%Y-%m-%d"
) -> pd.DataFrame:

    parameters = {
        "market_area": market_area,
        "modality": "Auction",
        "sub_modality": "DayAhead",
        "product": "60",
        "data_mode": "table",
    }

    html = _make_request(
        base_url,
        **parameters,
    )

    trading_date = _trading_date(html)
    delivery_date = trading_date + timedelta(days=1)

    columns = {"Volume(MWh)": "volume", "Price(£/MWh)": "price"}

    df = pd.read_html(html)[0]
    df.columns = df.columns.get_level_values(-1)
    df = df.loc[:, columns.keys()].rename(columns=columns)
    df.convert_dtypes()

    auction_start = delivery_date - timedelta(hours=1)
    auction_end = delivery_date + timedelta(hours=len(df) - 2)

    df = df.set_index(pd.date_range(auction_start, auction_end, freq="1H"))

    return df
