from pathlib import Path

from config import get_config
from request import request_day_ahead_auction_results
from plot import plot_day_ahead_auction_results

if __name__ == "__main__":
    config = get_config()
    base_url, market_area = config.GENERAL.base_url, config.GENERAL.market_area
    results = request_day_ahead_auction_results(base_url, market_area)
    plot_day_ahead_auction_results(results, Path("./docs/"), market_area)
