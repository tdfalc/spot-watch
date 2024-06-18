import requests
from datetime import datetime as dt, timedelta
from io import StringIO

import pandas as pd
import pytz


def _make_request(base_url: str, **kwargs) -> str:
    url = base_url + "&".join([f"{k}={v}" for k, v in kwargs.items()])
    with requests.get(url) as response:
        html = response.text
    return StringIO(html)


def _get_delivery_date(time_zone: str) -> dt:
    return dt.now(pytz.timezone(time_zone))


def _convert_to_utc(delivery_date: dt) -> dt:
    # Get the current date in time zone and normalize to midnight
    midnight = delivery_date.replace(hour=0, minute=0, second=0, microsecond=0)
    # Convert to utc
    return midnight.astimezone(pytz.utc)


def request_day_ahead_auction_results(
    base_url: str, market_area: str, time_zone: str
) -> pd.DataFrame:

    delivery_date = _get_delivery_date(time_zone)
    trading_date = delivery_date - timedelta(days=1)

    parameters = {
        "market_area": market_area,
        "auction": market_area,
        "modality": "Auction",
        "sub_modality": "DayAhead",
        "data_mode": "table",
        "trading_date": trading_date.strftime("%Y-%m-%d"),
        "delivery_date": delivery_date.strftime("%Y-%m-%d"),
    }

    html = _make_request(base_url, **parameters)

    columns = {"Volume(MWh)": "volume", "Price(£/MWh)": "price"}

    df = pd.read_html(html)[0]
    df.columns = [col.replace(" ", "") for col in df.columns]
    df.columns = df.columns.get_level_values(-1)
    print(df.columns)
    df = df.loc[:, columns.keys()].rename(columns=columns)
    df.convert_dtypes()

    auction_start = _convert_to_utc(delivery_date)
    auction_end = auction_start + timedelta(hours=len(df) - 1)

    df = df.set_index(pd.date_range(auction_start, auction_end, freq="1h"))
    df.index.name = "date_start"

    return df
