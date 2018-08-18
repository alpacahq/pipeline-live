import iexfinance

from .util import (
    daily_cache, parallelize, tradable_symbols
)


def list_symbols():
    return [
        symbol['symbol'] for symbol in iexfinance.get_available_symbols()
    ]


@daily_cache(filename='iex_key_stats.pkl')
def key_stats():
    def fetch(symbols):
        return iexfinance.Stock(symbols).get_key_stats()

    all_symbols = list_symbols()

    return parallelize(fetch, splitlen=99)(all_symbols)


@daily_cache(filename='iex_financials.pkl')
def financials():
    def fetch(symbols):
        return iexfinance.Stock(symbols).get_financials()

    all_symbols = list_symbols()

    return parallelize(fetch, splitlen=99)(all_symbols)
