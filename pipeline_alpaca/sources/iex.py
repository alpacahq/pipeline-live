import iexfinance
import pandas as pd

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


def get_stockprices(chart_range='1y'):
    '''
    This is a proxy to the main fetch function to cache
    the result based on the chart range parameter.
    '''

    all_symbols = list_symbols()

    @daily_cache(filename='iex_chart_{}'.format(chart_range))
    def get_stockprices_cached(all_symbols):
        return _get_stockprices(all_symbols, chart_range)

    return get_stockprices_cached(all_symbols)


def _get_stockprices(symbols, chart_range='1y'):
    '''Get stock data (key stats and previous) from IEX.
    Just deal with IEX's 100 stocks limit per request.
    '''

    def fetch(symbols):
        charts = iexfinance.Stock(symbols).get_chart(range=chart_range)
        result = {}
        for symbol, obj in charts.items():
            df = pd.DataFrame(
                obj,
                columns=('date', 'open', 'high', 'low', 'close', 'volume'),
            ).set_index('date')
            df.index = pd.to_datetime(df.index, utc=True)
            result[symbol] = df
        return result

    return parallelize(fetch, splitlen=99)(symbols)
