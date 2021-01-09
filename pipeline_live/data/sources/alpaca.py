import alpaca_trade_api as tradeapi

from .util import (
    daily_cache, parallelize
)


def list_symbols():
    with tradeapi.REST() as api:
        return [
            a.symbol for a in api.list_assets()
            if a.tradable and a.status == 'active'
        ]


def get_stockprices(limit=365, timespan='day'):
    all_symbols = list_symbols()

    @daily_cache(filename='alpaca_chart_{}'.format(limit))
    def get_stockprices_cached(all_symbols):
        return _get_stockprices(all_symbols, limit, timespan)

    return get_stockprices_cached(all_symbols)


def _get_stockprices(symbols, limit=365, timespan='day'):
    '''Get stock data (key stats and previous) from Alpaca.
    Just deal with Alpaca's 200 stocks per request limit.
    '''

    api = tradeapi.REST()

    def fetch(symbols):
        barset = api.get_barset(symbols, timespan, limit)
        data = {}
        for symbol in barset:
            df = barset[symbol].df
            # Update the index format for comparison with the trading calendar
            df.index = df.index.tz_convert('UTC').normalize()
            data[symbol] = df.asfreq('C')

        return data

    with api:
        return parallelize(fetch, splitlen=199)(symbols)
