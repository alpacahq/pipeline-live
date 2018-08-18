import alpaca_trade_api as tradeapi

from .util import (
    daily_cache, parallelize, tradable_symbols
)


@daily_cache(filename='polygon_companies.pkl')
def companies():
    all_symbols = tradable_symbols()

    def fetch(symbols):
        api = tradeapi.REST()
        params = {
            'symbols': ','.join(symbols),
        }
        response = api.polygon.get('/meta/symbols/company', params=params)
        return {
            o['symbol']: o for o in response
        }

    return parallelize(fetch, workers=25, splitlen=50)(all_symbols)


@daily_cache(filename='polygon_financials.pkl')
def financials():
    all_symbols = tradable_symbols()

    def fetch(symbols):
        api = tradeapi.REST()
        params = {
            'symbols': ','.join(symbols),
        }
        return api.polygon.get('/meta/symbols/financials', params=params)

    return parallelize(fetch, workers=25, splitlen=50)(all_symbols)
