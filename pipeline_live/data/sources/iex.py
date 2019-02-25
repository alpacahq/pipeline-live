import iexfinance
import pandas as pd

from .util import (
    daily_cache, parallelize
)


def list_symbols():
    return [
        symbol['symbol'] for symbol in iexfinance.refdata.get_symbols()
    ]


def _ensure_dict(result, symbols):
    if len(symbols) == 1:
        return {symbols[0]: result}
    return result


class IEXGetter(object):

    def __init__(self, method):
        self._method = method

    def __call__(self):
        method_name = 'get_{}'.format(self._method)

        @daily_cache(filename='iex_{}.pkl'.format(self._method))
        def _get(all_symbols):
            def fetch(symbols):
                return _ensure_dict(
                    getattr(iexfinance.stocks.Stock(symbols), method_name)(),
                    symbols
                )

            return parallelize(fetch, splitlen=99)(all_symbols)

        all_symbols = list_symbols()
        return _get(all_symbols)


key_stats = IEXGetter('key_stats')
company = IEXGetter('company')
financials = IEXGetter('financials')


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
        charts = _ensure_dict(
            iexfinance.stocks.Stock(symbols).get_chart(range=chart_range),
            symbols
        )
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
