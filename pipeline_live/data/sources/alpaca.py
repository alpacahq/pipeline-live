from datetime import timedelta
from alpaca_trade_api import TimeFrame, REST

from .util import (
    daily_cache, parallelize
)


def list_symbols():
    api = REST()
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

    api = REST()
    timeframe = TimeFrame.Minute if timespan == "minute" else TimeFrame.Day
    start = None

    #Data v1 used to handle this itself, so we have to do it manually now
    if timespan == 'minute':
        start = api.get_clock().timestamp.date() - timedelta(minutes=limit)
    else:
        start = api.get_clock().timestamp.date() - timedelta(days=limit)

    def fetch(symbols):
        data = {}
        for symbol in symbols:
            df = api.get_bars(
                symbol,
                start=start,
                limit=limit,
                timeframe=timeframe,
                adjustment='raw'
            ).df

            # Update the index format for comparison with the trading calendar
            if not df.empty:
                if df.index.tzinfo is None:
                    df.index = df.index\
                        .tz_localize('UTC')\
                        .tz_convert('US/Eastern')
                else:
                    df.index = df.index.tz_convert('US/Eastern')


            data[symbol] = df.asfreq('C') if timeframe != 'minute' else df

        return data

    return parallelize(fetch, splitlen=199)(symbols)
