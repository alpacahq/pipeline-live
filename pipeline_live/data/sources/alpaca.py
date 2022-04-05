import alpaca_trade_api as tradeapi
from alpaca_trade_api import TimeFrame

from .util import (
    daily_cache, parallelize
)


def list_symbols():
    api = tradeapi.REST()
    return [a.symbol for a in api.list_assets(status="active") if a.tradable]

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
    timeframe = TimeFrame.Minute if timespan == "minute" else TimeFrame.Day

    def fetch(symbols):
        # Using V2 api to get the data. we cannot do 1 api call for all
        # symbols because the v1 `limit` was per symbol, where v2 it's for
        # overall response size; so we will iterate over each symbol with
        # the limit for each to replicate that behaviour

        data = {}
        for symbol in symbols:
            df = api.get_bars(symbol,
                              limit=limit,
                              timeframe=timeframe,
                              adjustment='raw').df

            # Update the index format for comparison with the trading calendar
            if df.index.tzinfo is None:
                df.index = df.index.tz_localize('UTC')

            data[symbol] = df.asfreq('C')

        return data

    return parallelize(fetch, splitlen=199)(symbols)
