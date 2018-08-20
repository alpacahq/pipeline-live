import iexfinance

from .util import (
    daily_cache, parallelize
)


def list_symbols():
    return [
        symbol['symbol'] for symbol in iexfinance.get_available_symbols()
    ]


def key_stats():
    all_symbols = list_symbols()
    return _key_stats(all_symbols)


@daily_cache(filename='iex_key_stats.pkl')
def _key_stats(all_symbols):
    def fetch(symbols):
        return iexfinance.Stock(symbols).get_key_stats()

    return parallelize(fetch, splitlen=99)(all_symbols)


def financials():
    all_symbols = list_symbols()
    return _financials(all_symbols)


@daily_cache(filename='iex_financials.pkl')
def _financials(all_symbols):
    def fetch(symbols):
        return iexfinance.Stock(symbols).get_financials()

    return parallelize(fetch, splitlen=99)(all_symbols)
